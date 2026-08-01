#!/usr/bin/env python3
"""Reset por comandos de cualquiera de los tres dispositivos del banco.

NUNCA programa nada. Sólo resetea. Esto es deliberado: la rama del PSoC está
sin terminar y reflashear el esclavo cuelga el PSoC (ver
docs/plan_pruebas_precampo.md §Trampas). Si algún día hay que programar, se
hace a mano, no desde acá.

Dispositivos
------------
``master``  ESP32 maestro en COM8 @921600. Reset por la línea EN vía DTR/RTS del
            CP210x (la misma secuencia que usa esptool para su hard reset). Se
            verifica leyendo el banner de la ROM y, si la PC está en GeoNetwork,
            pegándole a http://192.168.4.1/health.
``slave``   ESP32 esclavo en COM12 @115200 (env slave2, GEOPHONE placa entera).
            Mismo mecanismo. OJO: resetear el ESP esclavo puede dejar al PSoC
            colgado; usar ``--and-psoc`` para encadenar el ToggleReset.
``psoc``    PSoC5 vía KitProg (COM6) con ppcli: ``ToggleReset 0 100``. Reusa el
            patrón validado en slave/psoc_reset_recovery_test.py (E17). Tras el
            reset el PSoC re-corre su auto-calibración y tarda entre 10 s y
            ~4 min; hasta que termina RECHAZA configs. ``--wait-autocal`` espera.

Uso
---
    python device_reset.py --list
    python device_reset.py master
    python device_reset.py slave --and-psoc
    python device_reset.py psoc --wait-autocal
    python device_reset.py all --json

Código de salida 0 si todos los resets pedidos verificaron, 1 si alguno falló.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

try:
    import serial
    import serial.tools.list_ports as list_ports
except ImportError:  # pragma: no cover
    print("falta pyserial: python -m pip install pyserial", file=sys.stderr)
    raise SystemExit(2)


# ── Configuración del banco (2026-07-24) ─────────────────────────────────────
DEVICES = {
    "master": {"port": "COM8", "baud": 921600, "role": "ESP32 maestro"},
    "slave": {"port": "COM12", "baud": 115200, "role": "ESP32 esclavo (slave2/GEO)"},
}
MASTER_HOST = "192.168.4.1"

PPCLI_DIR_DEFAULT = r"C:\Program Files (x86)\Cypress\Programmer"
KITPROG_RE = re.compile(r"^<(KitProg[^\r\n]*)$", re.M)
PPCLI_OK_RE = re.compile(r"^0 OK$", re.M)

# La ROM del ESP32 imprime "rst:0x..." y "boot:0x..." a 115200 sin importar el
# baud de la app, así que a 921600 el banner puede salir como basura. Por eso se
# acepta cualquiera de estas señales de vida, no sólo el banner.
BOOT_MARKERS = (
    re.compile(rb"rst:0x", re.I),
    re.compile(rb"boot:0x", re.I),
    re.compile(rb"ets [A-Z]", re.I),
    re.compile(rb"\[ENLACE\]"),
    re.compile(rb"\[MAESTRO\]"),
    re.compile(rb"GeoNetwork"),
    re.compile(rb"ESP-ROM"),
    re.compile(rb"PSOC|psoc"),
    re.compile(rb"cpu_start|app_init|entry 0x"),
)

AUTOCAL_DEADLINE_S = 300.0


def log(msg: str) -> None:
    print(msg, flush=True)


# ── Reset de ESP32 por líneas de control del CP210x ───────────────────────────
def esp32_reset(port: str, baud: int, listen_s: float = 6.0) -> dict:
    """Baja EN y la vuelve a subir; escucha el arranque para verificar.

    EN va atado a RTS y IO0 a DTR en el circuito de auto-reset. Con DTR en False
    (IO0 alto) el chip arranca en modo aplicación, no en el bootloader serie:
    esto resetea, no deja al ESP esperando un flasheo.
    """
    result = {"device_port": port, "baud": baud, "ok": False, "detail": "", "log": ""}
    try:
        with serial.Serial(port, baud, timeout=0.2) as ser:
            ser.dtr = False          # IO0 alto -> arranca la app, no el bootloader
            ser.rts = True           # EN bajo  -> chip en reset
            time.sleep(0.12)
            ser.reset_input_buffer()
            ser.rts = False          # EN alto  -> sale del reset
            deadline = time.time() + listen_s
            blob = b""
            while time.time() < deadline:
                blob += ser.read(4096)
                if any(m.search(blob) for m in BOOT_MARKERS):
                    break
                time.sleep(0.05)
    except serial.SerialException as exc:
        result["detail"] = f"no se pudo abrir {port}: {exc}"
        return result

    text = blob.decode("utf-8", "replace")
    result["log"] = text[-1200:]
    hit = next((m.pattern.decode() for m in BOOT_MARKERS if m.search(blob)), None)
    if hit:
        result["ok"] = True
        result["detail"] = f"arrancó (marcador {hit!r}, {len(blob)} B leídos)"
    elif blob:
        # Hubo tráfico pero ilegible: a 921600 el banner de ROM sale a 115200 y
        # se ve como basura. Tráfico == vida, así que cuenta como reset OK.
        result["ok"] = True
        result["detail"] = f"arrancó (tráfico serie {len(blob)} B, banner ilegible por baud)"
    else:
        result["detail"] = "reset enviado pero el puerto quedó mudo"
    return result


def master_health(host: str = MASTER_HOST, timeout_s: float = 3.0) -> bool:
    try:
        with urllib.request.urlopen(f"http://{host}/health", timeout=timeout_s) as resp:
            body = resp.read().decode("utf-8", "replace")
            return resp.status == 200 and "ok" in {l.strip() for l in body.splitlines()}
    except Exception:
        return False


def wait_master_http(host: str = MASTER_HOST, timeout_s: float = 45.0) -> bool:
    """El AP tarda unos segundos en volver y Windows en re-asociarse."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if master_health(host):
            return True
        time.sleep(2)
    return False


# ── Reset del PSoC por KitProg/ppcli ──────────────────────────────────────────
def ppcli_run(lines: list[str], ppcli_dir: str, timeout_s: float = 60.0) -> str:
    handle, path = tempfile.mkstemp(suffix=".cli", text=True)
    try:
        with os.fdopen(handle, "w", encoding="ascii", newline="\r\n") as stream:
            stream.write("\n".join(lines) + "\n")
        done = subprocess.run(
            [os.path.join(ppcli_dir, "ppcli.exe"), f"--runfile {path.replace(os.sep, '/')}"],
            cwd=ppcli_dir, capture_output=True, text=True, timeout=timeout_s,
        )
        return done.stdout + done.stderr
    finally:
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass


def discover_kitprog(ppcli_dir: str) -> str | None:
    match = KITPROG_RE.search(ppcli_run(["GetPorts", "quit"], ppcli_dir))
    return match.group(1).strip() if match else None


def psoc_reset(ppcli_dir: str = PPCLI_DIR_DEFAULT, kitprog: str | None = None) -> dict:
    result = {"device_port": "KitProg", "ok": False, "detail": "", "log": ""}
    exe = os.path.join(ppcli_dir, "ppcli.exe")
    if not os.path.isfile(exe):
        result["detail"] = f"no existe {exe}"
        return result
    kitprog = kitprog or discover_kitprog(ppcli_dir)
    if not kitprog:
        result["detail"] = "GetPorts no reportó ningún KitProg"
        return result
    out = ppcli_run([
        f'OpenPort "{kitprog}" "{ppcli_dir}\\"',
        "SetProtocol 8",
        "SetProtocolClock 152",
        "SetProtocolConnector 1",
        "ToggleReset 0 100",
        "ClosePort",
        "quit",
    ], ppcli_dir)
    result["log"] = out[-1200:]
    result["kitprog"] = kitprog
    ok = bool(PPCLI_OK_RE.search(out)) and "ToggleReset" in out and "error" not in out.lower()
    result["ok"] = ok
    result["detail"] = f"ToggleReset en {kitprog}" if ok else "ppcli no reportó 0 OK"
    return result


def wait_autocal(port: str = "COM12", baud: int = 115200,
                 deadline_s: float = AUTOCAL_DEADLINE_S) -> dict:
    """Pregunta ``probe`` al esclavo hasta que el PSoC contesta sano.

    Tras un ToggleReset el PSoC corre auto-calibración y rechaza configs; el
    esclavo es el único que puede preguntarle. Si el esclavo no tiene los
    comandos USB compilados esto va a dar timeout: no es fatal, sólo significa
    que hay que esperar a ojo.
    """
    result = {"ok": False, "detail": "", "elapsed_s": 0.0}
    started = time.time()
    try:
        with serial.Serial(port, baud, timeout=0.3) as ser:
            while time.time() - started < deadline_s:
                ser.reset_input_buffer()
                ser.write(b"probe\r\n")
                ser.flush()
                blob = b""
                until = time.time() + 4.0
                while time.time() < until:
                    blob += ser.read(2048)
                    if b"psoc=1" in blob or b"IDLE" in blob:
                        break
                if b"psoc=1" in blob or b"IDLE" in blob:
                    result["ok"] = True
                    result["detail"] = blob.decode("utf-8", "replace")[-300:]
                    break
                time.sleep(5)
    except serial.SerialException as exc:
        result["detail"] = f"no se pudo abrir {port}: {exc}"
        return result
    result["elapsed_s"] = round(time.time() - started, 1)
    if not result["ok"]:
        result["detail"] = f"sin respuesta sana en {deadline_s:.0f}s (auto-cal puede seguir corriendo)"
    return result


def list_ports_cmd() -> None:
    log("Puertos serie visibles:")
    for p in list_ports.comports():
        tag = ""
        for name, cfg in DEVICES.items():
            if cfg["port"] == p.device:
                tag = f"   <-- {name} ({cfg['role']})"
        if "KitProg" in (p.description or ""):
            tag = "   <-- psoc (KitProg, reset por ppcli)"
        log(f"  {p.device:6s} {p.description}{tag}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("device", nargs="?", choices=["master", "slave", "psoc", "all"],
                    help="qué resetear")
    ap.add_argument("--list", action="store_true", help="listar puertos y salir")
    ap.add_argument("--port", help="sobrescribir el puerto del dispositivo")
    ap.add_argument("--baud", type=int, help="sobrescribir el baud")
    ap.add_argument("--and-psoc", action="store_true",
                    help="tras resetear el esclavo, ToggleReset al PSoC")
    ap.add_argument("--wait-autocal", action="store_true",
                    help="tras el reset del PSoC, esperar a que la auto-cal termine")
    ap.add_argument("--wait-http", action="store_true",
                    help="tras resetear el maestro, esperar a que /health responda")
    ap.add_argument("--ppcli-dir", default=PPCLI_DIR_DEFAULT)
    ap.add_argument("--json", action="store_true", help="salida JSON para scripts")
    args = ap.parse_args()

    if args.list or not args.device:
        list_ports_cmd()
        return 0

    targets = ["master", "slave", "psoc"] if args.device == "all" else [args.device]
    if args.device == "slave" and args.and_psoc:
        targets.append("psoc")

    report: dict[str, dict] = {}
    for target in targets:
        log(f"\n=== RESET {target.upper()} ===")
        if target == "psoc":
            res = psoc_reset(args.ppcli_dir)
            if res["ok"] and args.wait_autocal:
                log("[psoc] esperando auto-calibración (hasta 5 min)…")
                res["autocal"] = wait_autocal()
                log(f"[psoc] auto-cal: {res['autocal']['detail']}")
        else:
            cfg = DEVICES[target]
            res = esp32_reset(args.port or cfg["port"], args.baud or cfg["baud"])
            if target == "master" and res["ok"]:
                # El reset baja el AP; verificar por HTTP es lo que de verdad
                # dice que el maestro volvió, no el banner serie.
                res["http_ok"] = wait_master_http() if args.wait_http else master_health()
                log(f"[master] /health: {'OK' if res['http_ok'] else 'sin respuesta'}")
        report[target] = res
        log(f"[{target}] {'OK' if res['ok'] else 'FALLÓ'}: {res['detail']}")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if all(r["ok"] for r in report.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
