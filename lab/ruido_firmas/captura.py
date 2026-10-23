"""Captura escenarios de ruido usando exclusivamente el USB del maestro."""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from comun import FS_DEFAULT

SCENARIOS = [
    ("base_clasico", 0, 280),
    ("async_comp", 1, 1500),
    ("async_sd", 2, 1500),
    ("rt_comp", 5, 1500),
    ("rt_sd", 6, 1500),
]


def cmd4(command, param=0):
    return bytes((0xAB, command, param & 0xFF, (command ^ param) & 0xFF))


def cmd5(command, value):
    lo, hi = value & 0xFF, (value >> 8) & 0xFF
    return bytes((0xAB, command, lo, hi, command ^ lo ^ hi))


class PacketParser:
    def __init__(self):
        self.buffer = bytearray()

    def feed(self, chunk):
        self.buffer.extend(chunk)
        packets = []
        while len(self.buffer) >= 6:
            if self.buffer[0] != 0x56:
                try:
                    pos = self.buffer.index(0x56, 1)
                    del self.buffer[:pos]
                except ValueError:
                    self.buffer.clear()
                    break
                if len(self.buffer) < 6:
                    break
            packets.append(bytes(self.buffer[:6]))
            del self.buffer[:6]
        return packets


def signed24(b2, b1, b0):
    value = (b2 << 16) | (b1 << 8) | b0
    return value - 0x1000000 if value & 0x800000 else value


def capture_one(port, scenario, mode, n_batches, node, timeout_s):
    expected = n_batches * 30
    port.reset_input_buffer()
    port.write(cmd4(0xA4)); port.flush()
    time.sleep(1.0)
    port.write(cmd4(0xAF, mode)); port.flush()
    time.sleep(0.2)
    port.write(cmd4(0xA2, 1)); port.flush()
    time.sleep(3.5)
    port.reset_input_buffer()
    port.write(cmd5(0xA3, n_batches)); port.flush()

    parser = PacketParser()
    samples, flags, states = [], [], []
    pending_flags = 0
    seen_active = False
    start = time.monotonic()
    while time.monotonic() - start < timeout_s:
        for packet in parser.feed(port.read(4096)):
            pkt_node, kind = packet[1], packet[2]
            if kind == 0xFB and pkt_node == node:
                pending_flags = packet[3]
            elif kind == 0x00 and pkt_node == node:
                samples.append(signed24(packet[3], packet[4], packet[5]))
                flags.append(pending_flags)
                pending_flags = 0
            elif kind == 0x01 and pkt_node == 0:
                state = packet[5]
                if not states or state != states[-1]:
                    states.append(state)
                seen_active |= state in (3, 5)
        if seen_active and states and states[-1] == 2:
            break
    else:
        port.write(cmd4(0xA4)); port.flush()
        raise TimeoutError(f"{scenario}: timeout tras {timeout_s:.0f} s; {len(samples)}/{expected} muestras")

    if len(samples) != expected:
        raise RuntimeError(f"{scenario}: llegaron {len(samples)} muestras, se esperaban {expected}; estados={states}")
    return np.asarray(samples, dtype=np.int32), np.asarray(flags, dtype=np.uint8), states, time.monotonic() - start


def estimate_minutes(scenarios, repeats, fs):
    # Incluye adquisición, armado y transferencia USB de paquetes de 6 bytes
    # (10 bits/byte con framing serial). En tiempo real esa transferencia se
    # solapa, pero contarla también deja una estimación conservadora.
    acquisition = sum(n * 30 / fs + 4.7 + n * 30 * 6 * 10 / 921600
                      for _, _, n in scenarios) * repeats
    return (12.0 + acquisition) / 60.0


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--puerto", default="COM6", help="USB del maestro (default: COM6)")
    parser.add_argument("--placa", required=True, help="etiqueta estable de la placa")
    parser.add_argument("--salida", default="lab/ruido_firmas/capturas")
    parser.add_argument("--repeticiones", "-R", type=int, default=3)
    parser.add_argument("--nodo", type=int, default=2)
    parser.add_argument("--fs", type=float, default=FS_DEFAULT)
    parser.add_argument("--timeout-s", type=float, default=180.0)
    parser.add_argument("--rapido", action="store_true", help="smoke run de menos de 3 minutos")
    parser.add_argument("--solo", choices=[s[0] for s in SCENARIOS], action="append",
                        help="limitar escenarios; se puede repetir")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.repeticiones < 1:
        raise SystemExit("--repeticiones debe ser >= 1")
    scenarios = [s for s in SCENARIOS if not args.solo or s[0] in args.solo]
    repeats = args.repeticiones
    if args.rapido:
        repeats = 1
        scenarios = [(name, mode, min(n, 200 if mode == 0 else 250)) for name, mode, n in scenarios]
    estimate = estimate_minutes(scenarios, repeats, args.fs)
    print(f"Plan: {len(scenarios)} escenarios x {repeats} repeticiones; estimado {estimate:.1f} min")
    if estimate > 15.0:
        raise SystemExit("El plan estimado supera 15 min; reduzca --repeticiones o use --rapido")

    import serial
    output = Path(args.salida) / args.placa
    output.mkdir(parents=True, exist_ok=True)
    print("Conecte solo el USB del maestro; esclavo y PSoC deben estar desconectados del PC.")
    with serial.Serial(args.puerto, 921600, timeout=0.05) as master:
        print("El maestro se reinició al abrir el puerto; esperando 12 s...")
        time.sleep(12.0)
        failures = 0
        for name, mode, n_batches in scenarios:
            for repetition in range(1, repeats + 1):
                stamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
                stem = f"{args.placa}_{name}_r{repetition:02d}_{datetime.now():%Y%m%d_%H%M%S}"
                print(f"[{name} r{repetition}] modo={mode}, N={n_batches}...", flush=True)
                try:
                    samples, flags, states, elapsed = capture_one(
                        master, name, mode, n_batches, args.nodo, args.timeout_s)
                except (TimeoutError, RuntimeError) as exc:
                    failures += 1
                    print(f"  ERROR: {exc}", file=sys.stderr)
                    continue
                metadata = {
                    "samples": int(samples.size), "marked_samples": int(np.count_nonzero(flags)),
                    "fs": args.fs, "mode": mode, "n_batches": n_batches, "scenario": name,
                    "timestamp": stamp, "placa": args.placa, "node": args.nodo,
                    "board_label": args.placa,
                    "master_states": states, "elapsed_s": elapsed,
                }
                np.savez_compressed(output / f"{stem}.npz", samples=samples, flags=flags,
                                    fs=np.float64(args.fs), mode=np.int16(mode),
                                    n_batches=np.int32(n_batches), scenario=np.str_(name),
                                    timestamp=np.str_(stamp), placa=np.str_(args.placa),
                                    board_label=np.str_(args.placa))
                (output / f"{stem}.json").write_text(
                    json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                print(f"  OK: {samples.size} muestras, {metadata['marked_samples']} marcadas, {elapsed:.1f} s")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
