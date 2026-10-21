#!/usr/bin/env python3
"""Prueba E2E de RADIOSIL entre un esclavo y el maestro.

No abre puertos al importarse. Requiere pyserial y debe ejecutarse de forma
explícita desde la raíz del repositorio (o desde cualquier otro directorio).
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import queue
import sys
import threading
import time
from typing import BinaryIO, TextIO


REPO_ROOT = Path(__file__).resolve().parents[1]
PYTHON_INTERFACE = REPO_ROOT / "src" / "interfaces" / "python"
sys.path.insert(0, str(PYTHON_INTERFACE))
# protocol.py importa "config" sin paquete
sys.path.insert(0, str(PYTHON_INTERFACE / "geophone_scope"))

from geophone_scope import config, protocol  # noqa: E402


SLAVE_BAUD = 115_200
PACKET_LEN = 6
PTYPE_ACK = 0x07
PTYPE_STATUS_HELLO = 0xFD
PTYPE_READY = 0xFE
MODE_ACK_TIMEOUT_SECONDS = 10.0
ARM_READ_SECONDS = 5.0
ACQUISITION_TIMEOUT_SECONDS = 60.0


def now_text() -> str:
    return datetime.now().astimezone().isoformat(timespec="milliseconds")


def log(message: str) -> None:
    print(f"[{now_text()}] {message}", flush=True)


@dataclass
class SlaveLine:
    sequence: int
    timestamp: str
    text: str


class SlaveReader:
    """Lee y registra todas las líneas del esclavo en un hilo."""

    def __init__(self, serial_port: object, raw_log: TextIO) -> None:
        self.serial_port = serial_port
        self.raw_log = raw_log
        self.stop_event = threading.Event()
        self.network_ready = threading.Event()
        self.lines: queue.Queue[SlaveLine] = queue.Queue()
        self._sequence = 0
        self._lock = threading.Lock()
        self.thread = threading.Thread(
            target=self._run, name="lector-esclavo", daemon=True
        )

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.thread.join(timeout=2.0)

    def checkpoint(self) -> int:
        with self._lock:
            return self._sequence

    def _run(self) -> None:
        while not self.stop_event.is_set():
            try:
                raw = self.serial_port.readline()
            except Exception as exc:  # El hilo no debe ocultar una falla serial.
                log(f"ERROR lector esclavo: {exc}")
                return
            if not raw:
                continue
            text = raw.decode("utf-8", errors="replace").rstrip("\r\n")
            timestamp = now_text()
            with self._lock:
                self._sequence += 1
                item = SlaveLine(self._sequence, timestamp, text)
            self.raw_log.write(f"[{timestamp}] {text}\n")
            self.raw_log.flush()
            log(f"ESCLAVO {text}")
            self.lines.put(item)
            if ("AP '" in text and "en canal" in text) or "[ESPNOW] ready" in text:
                self.network_ready.set()

    def wait_for_mode(self, enabled: bool, after: int) -> tuple[bool, bool]:
        expected = f"#RADIOSIL {1 if enabled else 0}"
        deadline = time.monotonic() + MODE_ACK_TIMEOUT_SECONDS
        saw_return = False
        deferred: list[SlaveLine] = []
        matched = False
        while time.monotonic() < deadline:
            try:
                item = self.lines.get(timeout=min(0.25, deadline - time.monotonic()))
            except queue.Empty:
                continue
            if item.sequence <= after:
                continue
            deferred.append(item)
            saw_return |= "#RADIOSIL vuelve" in item.text
            if expected in item.text:
                matched = True
                break
        for item in deferred:
            self.lines.put(item)
        return matched, saw_return

    def saw_return_since(self, after: int) -> bool:
        found = False
        retained: list[SlaveLine] = []
        while True:
            try:
                item = self.lines.get_nowait()
            except queue.Empty:
                break
            retained.append(item)
            if item.sequence > after and "#RADIOSIL vuelve" in item.text:
                found = True
        for item in retained:
            self.lines.put(item)
        return found

    def saw_start_markers_since(self, after: int) -> tuple[bool, bool]:
        hot_wait = False
        start_ok = False
        retained: list[SlaveLine] = []
        while True:
            try:
                item = self.lines.get_nowait()
            except queue.Empty:
                break
            retained.append(item)
            if item.sequence > after:
                hot_wait |= "HOT_WAIT n=" in item.text
                start_ok |= "START_OK" in item.text
        for item in retained:
            self.lines.put(item)
        return hot_wait, start_ok


@dataclass
class AttemptResult:
    number: int
    radiosil: bool
    expected: int
    received: int = 0
    seconds: float = 0.0
    mode_ack: bool = False
    radiosil_returned: bool = False
    hot_wait: bool = False
    start_ok: bool = False
    completed: bool = False
    counts: Counter[int] = field(default_factory=Counter)
    ack_count: int = 0
    status_count: int = 0
    ready_count: int = 0
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.mode_ack and self.completed and not self.error


def record_packet(packet: protocol.Packet, result: AttemptResult, events: TextIO) -> None:
    timestamp = now_text()
    if packet.ptype == config.PTYPE_DATA:
        result.counts[packet.node_id] += 1
        kind = "DATA"
    elif packet.ptype == PTYPE_ACK:
        result.ack_count += 1
        kind = "ACK"
    elif packet.ptype == PTYPE_STATUS_HELLO:
        result.status_count += 1
        kind = "STATUS/HELLO"
    elif packet.ptype == PTYPE_READY:
        result.ready_count += 1
        kind = "READY"
    else:
        kind = f"TYPE_{packet.ptype:#04x}"
    events.write(f"[{timestamp}] {kind} {packet!r}\n")
    events.flush()


def read_master(
    master: object,
    duration: float,
    result: AttemptResult,
    raw_file: BinaryIO,
    events: TextIO,
    stop_at_expected: bool,
) -> None:
    deadline = time.monotonic() + duration
    pending = bytearray()
    while time.monotonic() < deadline:
        waiting = int(getattr(master, "in_waiting", 0))
        chunk = master.read(max(1, waiting))
        if not chunk:
            continue
        raw_file.write(chunk)
        raw_file.flush()
        pending.extend(chunk)

        while True:
            try:
                header_at = pending.index(config.PKT_HEADER)
            except ValueError:
                pending.clear()
                break
            if header_at:
                del pending[:header_at]
            if len(pending) < PACKET_LEN:
                break
            frame = bytes(pending[:PACKET_LEN])
            del pending[:PACKET_LEN]
            packet = protocol.decode_packet(frame)
            if packet is None:
                continue
            record_packet(packet, result, events)
            if stop_at_expected and result.counts:
                result.received = max(result.counts.values())
                if result.received >= result.expected:
                    return


def wait_for_network_ready(
    master: object,
    reader: SlaveReader,
    timeout: float,
) -> bool:
    deadline = time.monotonic() + timeout
    pending = bytearray()
    status_node: int | None = None

    log(
        f"Esperando hasta {timeout:g} s por red del esclavo y "
        "STATUS/HELLO en el maestro..."
    )
    while time.monotonic() < deadline:
        waiting = int(getattr(master, "in_waiting", 0))
        chunk = master.read(max(1, waiting))
        if chunk:
            pending.extend(chunk)
            while True:
                try:
                    header_at = pending.index(config.PKT_HEADER)
                except ValueError:
                    pending.clear()
                    break
                if header_at:
                    del pending[:header_at]
                if len(pending) < PACKET_LEN:
                    break
                frame = bytes(pending[:PACKET_LEN])
                del pending[:PACKET_LEN]
                packet = protocol.decode_packet(frame)
                if (
                    packet is not None
                    and packet.ptype == config.PTYPE_STATUS
                    and packet.node_id != config.MASTER_NODE_ID
                ):
                    status_node = packet.node_id
                    log(f"Maestro recibió STATUS/HELLO del esclavo {status_node:#04x}.")

        if reader.network_ready.is_set() and status_node is not None:
            log(f"Red lista; esclavo detectado por el maestro: {status_node:#04x}.")
            return True

    missing = []
    if not reader.network_ready.is_set():
        missing.append("línea de red del esclavo")
    if status_node is None:
        missing.append("STATUS/HELLO del esclavo en el maestro")
    log(f"ERROR: timeout de red tras {timeout:g} s; falta: {', '.join(missing)}.")
    return False


def send_mode(slave: object, reader: SlaveReader, enabled: bool) -> tuple[bool, bool, int]:
    checkpoint = reader.checkpoint()
    command = b"radiosil on\n" if enabled else b"radiosil off\n"
    slave.write(command)
    slave.flush()
    log(f"Enviado al esclavo: {command.decode().strip()}")
    acknowledged, saw_return = reader.wait_for_mode(enabled, checkpoint)
    if acknowledged:
        log(f"Confirmado por el esclavo: #RADIOSIL {1 if enabled else 0}")
    else:
        log(f"ADVERTENCIA: no llegó #RADIOSIL {1 if enabled else 0}")
    return acknowledged, saw_return, checkpoint


def run_attempt(
    master: object,
    slave: object,
    reader: SlaveReader,
    number: int,
    radiosil: bool,
    lots: int,
    log_dir: Path,
) -> AttemptResult:
    expected = lots * 30
    result = AttemptResult(number=number, radiosil=radiosil, expected=expected)
    mode_name = "on" if radiosil else "off"
    raw_path = log_dir / f"maestro_intento_{number:02d}_{mode_name}.bin"
    events_path = log_dir / f"maestro_intento_{number:02d}_{mode_name}.log"

    try:
        result.mode_ack, result.radiosil_returned, checkpoint = send_mode(
            slave, reader, radiosil
        )
        master.reset_input_buffer()
        with raw_path.open("wb") as raw_file, events_path.open(
            "w", encoding="utf-8", newline="\n"
        ) as events:
            events.write(
                f"[{now_text()}] intento={number} radiosil={mode_name} "
                f"lotes={lots} esperadas={expected}\n"
            )
            master.write(protocol.encode_std(config.CMD_ARM, 1))
            master.flush()
            log(f"Intento {number}: ARM; leyendo {ARM_READ_SECONDS:.0f} s")
            read_master(
                master, ARM_READ_SECONDS, result, raw_file, events, False
            )

            master.write(protocol.encode_std(config.CMD_STREAM, 1))
            master.write(protocol.encode_std16(config.CMD_START, lots))
            master.flush()
            started = time.monotonic()
            log(
                f"Intento {number}: STREAM=1, START N={lots}; "
                f"objetivo={expected} muestras"
            )
            read_master(
                master,
                ACQUISITION_TIMEOUT_SECONDS,
                result,
                raw_file,
                events,
                True,
            )
            result.seconds = time.monotonic() - started
            result.received = max(result.counts.values(), default=0)
            result.completed = result.received >= expected
            result.radiosil_returned |= reader.saw_return_since(checkpoint)
            result.hot_wait, result.start_ok = reader.saw_start_markers_since(checkpoint)
    except Exception as exc:
        result.error = f"{type(exc).__name__}: {exc}"
        log(f"ERROR intento {number}: {result.error}")
    finally:
        try:
            master.write(protocol.encode_std(config.CMD_STREAM, 0))
            master.flush()
            log(f"Intento {number}: STREAM=0")
        except Exception as exc:
            if not result.error:
                result.error = f"No se pudo detener STREAM: {exc}"
            log(f"ERROR al detener STREAM en intento {number}: {exc}")

    counts = ", ".join(
        f"{node:#04x}:{count}" for node, count in sorted(result.counts.items())
    ) or "ninguno"
    log(
        f"Intento {number}: {result.received}/{expected} en {result.seconds:.2f} s; "
        f"nodos={counts}; #RADIOSIL vuelve={'sí' if result.radiosil_returned else 'no'}"
    )
    return result


def table(results: list[AttemptResult]) -> str:
    rows = [
        "| Intento | RADIOSIL | Recibidas/esperadas | Por nodo | Segundos | #RADIOSIL vuelve | HOT_WAIT n= | START_OK | ACK | STATUS/HELLO | READY | Resultado |",
        "|---:|:---:|---:|:---|---:|:---:|:---:|:---:|---:|---:|---:|:---:|",
    ]
    for item in results:
        status = "OK" if item.ok else f"FALLÓ{': ' + item.error if item.error else ''}"
        node_counts = ", ".join(
            f"{node:#04x}: {count}" for node, count in sorted(item.counts.items())
        ) or "—"
        rows.append(
            f"| {item.number} | {'on' if item.radiosil else 'off'} | "
            f"{item.received}/{item.expected} | {node_counts} | {item.seconds:.2f} | "
            f"{'sí' if item.radiosil_returned else 'no'} | "
            f"{'sí' if item.hot_wait else 'no'} | {'sí' if item.start_ok else 'no'} | "
            f"{item.ack_count} | {item.status_count} | {item.ready_count} | {status} |"
        )
    for radiosil in (True, False):
        mode_results = [item for item in results if item.radiosil == radiosil]
        if mode_results:
            ok_count = sum(item.ok for item in mode_results)
            rows.append(
                f"| Resumen | {'on' if radiosil else 'off'} | — | — | — | — | — | — | — | — | — | "
                f"{ok_count}/{len(mode_results)} OK |"
            )
    return "\n".join(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM8", help="puerto del esclavo (default: COM8)")
    parser.add_argument("--maestro", default="COM6", help="puerto del maestro (default: COM6)")
    parser.add_argument("--rep", type=int, default=2, help="intentos con RADIOSIL on (default: 2)")
    parser.add_argument("--control", type=int, default=1, help="intentos con RADIOSIL off (default: 1)")
    parser.add_argument(
        "--intercalar", action="store_true",
        help="alternar intentos RADIOSIL on/off mientras queden de ambos modos",
    )
    parser.add_argument(
        "--espera-red-s",
        type=float,
        default=120.0,
        help="timeout para esperar red y STATUS/HELLO (default: 120)",
    )
    parser.add_argument(
        "-N", "--n", "--lotes", dest="lots", type=int, default=100,
        help="lotes solicitados; cada lote equivale a 30 muestras (default: 100)",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=Path("lab/ruido_rf_20261020/radiosil_e2e/resultado.md"),
        help="informe Markdown de salida",
    )
    args = parser.parse_args()
    if args.rep < 0:
        parser.error("--rep debe ser >= 0")
    if args.control < 0:
        parser.error("--control debe ser >= 0")
    if args.espera_red_s <= 0:
        parser.error("--espera-red-s debe ser > 0")
    if not 1 <= args.lots <= 0xFFFF:
        parser.error("--lotes/--n debe estar entre 1 y 65535")
    return args


def main() -> int:
    args = parse_args()
    try:
        import serial
    except ImportError:
        log("ERROR: falta pyserial (módulo 'serial')")
        return 2

    output_path = args.salida.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    slave_log_path = output_path.parent / "esclavo_raw.log"
    results: list[AttemptResult] = []
    slave = None
    master = None
    reader: SlaveReader | None = None

    try:
        slave_log = slave_log_path.open("w", encoding="utf-8", newline="\n")
        try:
            log(
                f"Abriendo esclavo {args.port} a {SLAVE_BAUD}; abrirlo reinicia ESP/PSoC."
            )
            slave = serial.Serial(args.port, SLAVE_BAUD, timeout=0.25, write_timeout=2)
            reader = SlaveReader(slave, slave_log)
            reader.start()
            log(f"Abriendo maestro {args.maestro} a {config.BAUD}.")
            master = serial.Serial(
                args.maestro, config.BAUD, timeout=0.10, write_timeout=2
            )
            if not wait_for_network_ready(master, reader, args.espera_red_s):
                log("Prueba abortada antes de iniciar intentos.")
                return 2
            if args.intercalar:
                plan = []
                for index in range(max(args.rep, args.control)):
                    if index < args.rep:
                        plan.append(True)
                    if index < args.control:
                        plan.append(False)
            else:
                plan = [True] * args.rep + [False] * args.control
            for number, radiosil in enumerate(plan, start=1):
                results.append(
                    run_attempt(
                        master, slave, reader, number, radiosil, args.lots, output_path.parent
                    )
                )
        finally:
            if reader is not None:
                reader.stop()
            if master is not None and master.is_open:
                try:
                    master.write(protocol.encode_std(config.CMD_STREAM, 0))
                    master.flush()
                except Exception as exc:
                    log(f"ADVERTENCIA durante cleanup STREAM=0: {exc}")
                finally:
                    master.close()
            if slave is not None and slave.is_open:
                try:
                    slave.close()
                except Exception as exc:
                    log(f"ADVERTENCIA al cerrar esclavo: {exc}")
            try:
                slave_log.close()
            except Exception as exc:
                log(f"ADVERTENCIA al cerrar log del esclavo: {exc}")
    except Exception as exc:
        log(f"ERROR fatal: {type(exc).__name__}: {exc}")
        if not results:
            return 2

    report = table(results)
    print("\n" + report, flush=True)
    output_path.write_text(
        "# Resultado prueba RADIOSIL E2E\n\n"
        f"Generado: {now_text()}\n\n"
        f"Esclavo: `{args.port}` @ {SLAVE_BAUD}; maestro: `{args.maestro}` @ {config.BAUD}; "
        f"N={args.lots}.\n\n{report}\n",
        encoding="utf-8",
    )
    log(f"Informe: {output_path}")
    log(f"Logs crudos: {output_path.parent}")
    expected_attempts = args.rep + args.control
    return 0 if len(results) == expected_attempts and all(r.ok for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
