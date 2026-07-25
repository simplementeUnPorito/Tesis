#!/usr/bin/env python3
"""Configura la red del enlace del maestro y verifica que la STA se asocie.

No reflashea nada: la config del enlace vive en NVS y se carga por HTTP
(``POST /enlace/config`` -> ``web_server.h``), justamente para que subir la SPA
(que borra LittleFS) no se lleve la red guardada. El maestro corre WIFI_AP_STA,
así que su AP en 192.168.4.1 sigue vivo mientras la STA se asocia al router de
casa: no hace falta elegir entre una y otra.

Por qué verifica tanto: ya pasó guardar ``S21`` en vez de ``S21 Ultra de Elías
David`` y el maestro se quedó sin asociar **en silencio** (el propio
web_server.h lo documenta). Acá el SSID se confirma contra el escaneo del propio
ESP antes de escribirlo, y después se relee el status hasta ver ``sta=up`` con
IP. Si algo no cierra, el script falla ruidosamente.

Uso
---
    python link_config.py --show
    python link_config.py --scan
    python link_config.py --ssid "Flia. Martinez" --pass "..." --site casa
    python link_config.py --ssid "..." --pass "..." --no-verify-scan

Código de salida 0 sólo si la STA quedó asociada con IP (salvo --show/--scan).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HOST_DEFAULT = "192.168.4.1"
RECONNECT = (Path(__file__).resolve().parents[2] / "src" / "firmware" / "esp32" /
             "Nodo comunicación" / "master" / "reconnect_geonetwork.py")


def log(msg: str) -> None:
    print(msg, flush=True)


def http_get(host: str, path: str, timeout_s: float = 20.0) -> tuple[int, str]:
    try:
        with urllib.request.urlopen(f"http://{host}{path}", timeout=timeout_s) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:
        return 0, str(exc)


def http_post(host: str, path: str, fields: dict[str, str],
              timeout_s: float = 25.0) -> tuple[int, str]:
    data = urllib.parse.urlencode(fields).encode()
    req = urllib.request.Request(f"http://{host}{path}", data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", "replace")
    except Exception as exc:
        return 0, str(exc)


def parse_status(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def ensure_on_ap(host: str, timeout_s: float = 120.0) -> bool:
    """Deja la PC en GeoNetwork reusando el script del maestro (no duplicarlo)."""
    code, _ = http_get(host, "/health", timeout_s=4)
    if code == 200:
        return True
    if not RECONNECT.is_file():
        log(f"[link] no encuentro {RECONNECT}")
        return False
    log("[link] la PC no ve el maestro; reconectando a GeoNetwork…")
    done = subprocess.run([sys.executable, str(RECONNECT), "--timeout", str(int(timeout_s))],
                          cwd=str(RECONNECT.parent), text=True)
    return done.returncode == 0


def scan(host: str, attempts: int = 14) -> list[tuple[int, int, str]]:
    """``GET /enlace/scan`` devuelve 202 mientras escanea; formato '<ch> <rssi> <ssid>'.

    El escaneo **tira la conexión del cliente**: el ESP32 tiene una sola radio y
    para escanear la saca del canal del AP, así que la PC se cae de GeoNetwork a
    mitad del pedido (WinError 10053/10060). No es un error del script ni de la
    red: hay que reconectarse y volver a preguntar. El resultado queda cacheado
    en el ESP, así que el segundo pedido lo devuelve sin re-escanear.
    """
    for attempt in range(attempts):
        code, body = http_get(host, "/enlace/scan", timeout_s=25)
        if code == 200:
            nets = []
            for line in body.splitlines():
                m = re.match(r"^\s*(-?\d+)\s+(-?\d+)\s+(.+?)\s*$", line)
                if m:
                    nets.append((int(m.group(1)), int(m.group(2)), m.group(3)))
            if nets:
                return nets
            log("[link] scan devolvió lista vacía; reintento")
        elif code == 202:
            log("[link] scan en curso…")
        else:
            log(f"[link] scan cortó el enlace (esperado, la radio cambió de canal); "
                f"reconectando [{attempt + 1}/{attempts}]")
            ensure_on_ap(host, timeout_s=60)
        time.sleep(3)
    return []


def wait_sta_up(host: str, timeout_s: float = 60.0) -> dict[str, str]:
    """Espera sta=up con IP. El firmware reintenta cada LINK_STA_RETRY_MS=20 s."""
    deadline = time.time() + timeout_s
    last: dict[str, str] = {}
    while time.time() < deadline:
        code, body = http_get(host, "/enlace/status", timeout_s=15)
        if code == 200:
            last = parse_status(body)
            if last.get("sta") == "up" and last.get("ip"):
                return last
            log(f"[link] sta={last.get('sta')} ip={last.get('ip') or '-'} "
                f"canal={last.get('channel')} err={last.get('last_error') or '-'}")
        time.sleep(5)
    return last


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--host", default=HOST_DEFAULT)
    ap.add_argument("--ssid")
    ap.add_argument("--pass", dest="password")
    ap.add_argument("--site")
    ap.add_argument("--server-url")
    ap.add_argument("--auto", choices=["0", "1"])
    ap.add_argument("--distance-mm", type=int)
    ap.add_argument("--show", action="store_true", help="mostrar status y salir")
    ap.add_argument("--scan", action="store_true", help="listar redes vistas por el ESP y salir")
    ap.add_argument("--no-verify-scan", action="store_true",
                    help="escribir el SSID sin confirmarlo contra el escaneo")
    ap.add_argument("--timeout", type=float, default=90.0, help="espera de sta=up")
    args = ap.parse_args()

    if not ensure_on_ap(args.host):
        log("[link] FALLÓ: no llego al maestro. Probá "
            "'python device_reset.py master --wait-http'.")
        return 1

    if args.show or not args.ssid:
        code, body = http_get(args.host, "/enlace/status")
        log(f"=== /enlace/status ({code}) ===\n{body}")
        if not args.scan:
            return 0 if code == 200 else 1

    if args.scan:
        nets = scan(args.host)
        log("=== redes vistas por el ESP (canal rssi ssid) ===")
        for ch, rssi, ssid in nets:
            log(f"  ch={ch:2d} rssi={rssi:4d}  {ssid}")
        if not args.ssid:
            return 0 if nets else 1

    fields: dict[str, str] = {}
    if args.ssid is not None:
        if not args.no_verify_scan:
            nets = scan(args.host)
            names = [n[2] for n in nets]
            if names and args.ssid not in names:
                near = [n for n in names if args.ssid.lower()[:8] in n.lower()]
                log(f"[link] FALLÓ: el ESP no ve el SSID {args.ssid!r}.")
                log(f"       ve: {names}")
                if near:
                    log(f"       ¿quisiste decir {near}?")
                log("       (el ESP32 no ve 5 GHz; si el router hace band-steering, "
                    "revisá que el SSID exista en 2.4 GHz). Forzá con --no-verify-scan.")
                return 1
            if not names:
                log("[link] aviso: el escaneo vino vacío; escribo el SSID igual")
            else:
                ch = next(n[0] for n in nets if n[2] == args.ssid)
                log(f"[link] SSID {args.ssid!r} confirmado por el ESP en canal {ch}")
                log("       (los esclavos ESP-NOW adoptan el canal del maestro; "
                    "si el router salta de canal, esperar la re-adopción)")
        fields["ssid"] = args.ssid
    if args.password is not None:
        fields["pass"] = args.password
    if args.site is not None:
        fields["site"] = args.site
    if args.server_url is not None:
        fields["server_url"] = args.server_url
    if args.auto is not None:
        fields["auto"] = args.auto
    if args.distance_mm is not None:
        fields["distance_mm"] = str(args.distance_mm)

    shown = dict(fields)
    if "pass" in shown:
        shown["pass"] = "*" * len(shown["pass"])
    log(f"[link] POST /enlace/config {shown}")
    code, body = http_post(args.host, "/enlace/config", fields)
    if code != 200:
        log(f"[link] FALLÓ el POST ({code}): {body}")
        return 1
    log(f"=== status devuelto por el POST ===\n{body}")

    st = wait_sta_up(args.host, args.timeout)
    if st.get("sta") == "up" and st.get("ip"):
        log(f"[link] OK: asociado a {st.get('ssid')} ip={st['ip']} canal={st.get('channel')}")
        log(f"[link] cola intacta: {st.get('queue_files')} archivo(s), "
            f"{st.get('queue_bytes')} B")
        return 0
    log(f"[link] FALLÓ: la STA no subió en {args.timeout:.0f}s "
        f"(sta={st.get('sta')} err={st.get('last_error') or '-'})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
