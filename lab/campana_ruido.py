"""Orquesta campanas repetibles de medicion de ruido sin modificar ruido_sd.py."""

from __future__ import annotations

import argparse
import csv
import json
import os
import queue
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


LAB = Path(__file__).resolve().parent
RUIDO_SD = LAB / "ruido_sd.py"
ESPECTRO = LAB / "espectro_condiciones.py"
TRANSITORIO_ARRANQUE = LAB / "transitorio_arranque.py"


def _paso(exp: str, cond: list[str], rep: int = 3, pga: int = 3,
           pgaout: int = 0, tap: int = 4, nota: str = "",
           requiere_maestro: bool = False) -> dict[str, Any]:
    return {"exp": exp, "cond": cond, "rep": rep, "pga": pga,
            "pgaout": pgaout, "tap": tap, "nota": nota,
            "requiere_maestro": requiere_maestro}


def _plan_rf() -> list[dict[str, Any]]:
    plan = [
        _paso("W1_radio", ["BASE", "OFF"], pgaout=4,
               nota="Radio apagada"),
        _paso("W1b_ping", ["BASE", "PING"], pgaout=4,
               nota="Actividad de ping"),
        _paso("W5_lpo_pgaout1", ["PING", "RF10", "RF240", "RX"],
               nota="Comparacion RF y recepcion en LPo", requiere_maestro=True),
        _paso("W3b_potencia", ["RF240P2", "RF240P8", "RF240P14", "RF240P21"],
               rep=2, nota="Barrido de potencia RF"),
        _paso("W8_uso_real", ["PING", "RF240T29", "RF240T58"],
               pga=3, pgaout=0, tap=4, rep=3),
        _paso("W10_difusion", ["RF240", "RF240B", "RF10B"],
               pga=3, pgaout=0, tap=4, rep=3),
    ]
    plan.extend(
        _paso(f"W5_tap{tap}", ["PING", "RF240"], rep=2, pgaout=4,
               tap=tap, nota=f"Comparacion RF en tap {tap}")
        for tap in range(4)
    )
    plan.extend(
        _paso(f"W9_ganancia_pga{pga}", ["PING", "RF240"], rep=2,
               pga=pga, tap=0, nota=f"Comparacion de ganancia PGA {pga}")
        for pga in (0, 2, 4)
    )
    plan.extend([
        _paso("W1c_reposo", ["BASE", "OFF"], rep=4, pga=3,
               pgaout=4, tap=4,
               nota="radio en reposo encendida vs apagada (lineas de baliza)"),
        _paso("W3c_potencia_pgaout1",
               ["PING", "RF240P2", "RF240P8", "RF240P14", "RF240P21"],
               rep=3, pga=3, pgaout=0, tap=4),
        _paso("W11_silencio", ["BASE", "SIL", "OFF"], rep=4, pga=3,
               pgaout=4, tap=4,
               nota="radiosil inmediato (requiere firmware con radiosil)"),
        _paso("W12c_silencio_1000", ["BASE", "SIL1000", "SIL"], rep=3,
               pga=3, pgaout=4, tap=4,
               nota="radiosil con 1 s entre el apagado y el arranque"),
        _paso("W12e_silencio_500", ["BASE", "SIL500"], rep=6,
               pga=3, pgaout=4, tap=4,
               nota="radiosil 500 ms (valor recomendado) vs radio encendida"),
    ])
    for pga in (0, 2, 4):
        plan.append(_paso(f"W13_reposo_seo_pga{pga}", ["BASE", "OFF"], rep=3,
                          pga=pga, pgaout=0, tap=0,
                          nota="baliza en SEo segun la ganancia del PGA"))
    return plan


def _plan_sd() -> list[dict[str, Any]]:
    return [
        _paso("SD_base_real", ["BASE", "REAL"],
               nota="Control sin escritura y escritura SD real"),
        _paso("SD_p1_p5", ["BASE", "P1", "P2", "P3", "P4", "P5"],
               nota="Barrido de modos de sonda SD"),
    ]


PLANES = {"rf": _plan_rf, "sd": _plan_sd}


def cargar_plan(nombre_o_archivo: str | os.PathLike[str]) -> list[dict[str, Any]]:
    clave = str(nombre_o_archivo).lower()
    if clave in PLANES:
        return PLANES[clave]()
    with Path(nombre_o_archivo).open(encoding="utf-8") as fh:
        plan = json.load(fh)
    if not isinstance(plan, list):
        raise ValueError("el plan JSON debe ser una lista")
    requeridas = {"exp", "cond", "rep", "pga", "pgaout", "tap", "nota"}
    normalizado = []
    for indice, original in enumerate(plan, 1):
        if not isinstance(original, dict) or not requeridas <= original.keys():
            faltan = requeridas - set(original if isinstance(original, dict) else ())
            raise ValueError(f"paso {indice} invalido; faltan: {', '.join(sorted(faltan))}")
        paso = dict(original)
        if not isinstance(paso["cond"], list) or not paso["cond"]:
            raise ValueError(f"paso {indice}: cond debe ser una lista no vacia")
        paso["requiere_maestro"] = bool(
            paso.get("requiere_maestro", "RX" in (str(c).upper() for c in paso["cond"])))
        normalizado.append(paso)
    return normalizado


def filtrar_plan(plan: Iterable[dict[str, Any]], solo: str | None) -> list[dict[str, Any]]:
    if not solo:
        return list(plan)
    prefijos = tuple(x.strip() for x in solo.split(",") if x.strip())
    return [paso for paso in plan if str(paso["exp"]).startswith(prefijos)]


def comando_medicion(paso: dict[str, Any], raiz: Path, port: str,
                     maestro: str | None = None, nota: str = "") -> list[str]:
    comando = [sys.executable, str(RUIDO_SD), "correr", "--port", port]
    if maestro:
        comando += ["--maestro", maestro]
    comando += ["--raiz", str(Path(raiz)), "--exp", str(paso["exp"]),
                "--cond", *map(str, paso["cond"]), "--rep", str(paso["rep"]),
                "--pga", str(paso["pga"]), "--pgaout", str(paso["pgaout"])]
    if paso.get("tap") is not None:
        comando += ["--tap", str(paso["tap"])]
    nota_completa = "; ".join(x for x in (nota.strip(), str(paso.get("nota", "")).strip()) if x)
    comando += ["--nota", nota_completa]
    return comando


@dataclass(frozen=True)
class ResultadoProceso:
    estado: str
    motivo: str = ""
    retorno: int | None = None


def _marca() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _log(fh: Any, texto: str) -> None:
    fh.write(f"[{_marca()}] {texto}\n")
    fh.flush()


def ejecutar_con_vigilancia(comando: list[str], log: Path,
                            silencio_s: float, limite_s: float,
                            intervalo_s: float = 0.5) -> ResultadoProceso:
    """Ejecuta y mata el proceso si no produce salida o excede el limite."""
    log = Path(log)
    log.parent.mkdir(parents=True, exist_ok=True)
    eventos: queue.Queue[str | None] = queue.Queue()
    inicio = ultima_salida = time.monotonic()
    with log.open("a", encoding="utf-8", errors="replace") as fh:
        _log(fh, "$ " + subprocess.list2cmdline(comando))
        proceso = subprocess.Popen(
            comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )

        def leer() -> None:
            assert proceso.stdout is not None
            for linea in iter(proceso.stdout.readline, ""):
                eventos.put(linea)
            eventos.put(None)

        hilo = threading.Thread(target=leer, daemon=True)
        hilo.start()
        motivo = ""
        fin_salida = False
        while proceso.poll() is None:
            try:
                linea = eventos.get(timeout=intervalo_s)
                if linea is None:
                    fin_salida = True
                else:
                    fh.write(f"[{_marca()}] {linea}")
                    fh.flush()
                    ultima_salida = time.monotonic()
            except queue.Empty:
                pass
            ahora = time.monotonic()
            if ahora - ultima_salida >= silencio_s:
                motivo = "silencio"
            elif ahora - inicio >= limite_s:
                motivo = "tope total"
            if motivo:
                proceso.kill()
                proceso.wait(timeout=10)
                _log(fh, f"!! colgado ({motivo})")
                return ResultadoProceso("colgado", motivo, proceso.returncode)

        while not fin_salida:
            try:
                linea = eventos.get_nowait()
            except queue.Empty:
                break
            if linea is None:
                fin_salida = True
            else:
                fh.write(f"[{_marca()}] {linea}")
        retorno = proceso.returncode
        _log(fh, f"fin (codigo {retorno})")
        estado = ("ok" if retorno == 0 else
                  "no_convergio" if retorno == 3 else "error")
        return ResultadoProceso(estado,
                                "" if retorno == 0 else f"codigo {retorno}", retorno)


def _puertos() -> set[str]:
    try:
        from serial.tools import list_ports
    except ImportError:
        return set()
    return {p.device.upper() for p in list_ports.comports()}


def _puerto_presente(puerto: str | None) -> bool:
    return bool(puerto) and puerto.upper() in _puertos()


def esperar_puerto(puerto: str, limite_s: float = 600.0,
                   intervalo_s: float = 2.0) -> bool:
    fin = time.monotonic() + limite_s
    while time.monotonic() < fin:
        if _puerto_presente(puerto):
            return True
        time.sleep(min(intervalo_s, max(0.0, fin - time.monotonic())))
    return _puerto_presente(puerto)


def _ejecutar_auxiliar(comando: list[str], log: Path) -> int:
    with Path(log).open("a", encoding="utf-8", errors="replace") as fh:
        _log(fh, "$ " + subprocess.list2cmdline(comando))
        resultado = subprocess.run(comando, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True,
                                   encoding="utf-8", errors="replace")
        for linea in resultado.stdout.splitlines():
            _log(fh, linea)
        _log(fh, f"fin (codigo {resultado.returncode})")
        return resultado.returncode


def _cargar_estado(ruta: Path) -> dict[str, Any]:
    try:
        dato = json.loads(ruta.read_text(encoding="utf-8"))
        return dato if isinstance(dato, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _guardar_estado(ruta: Path, estado: dict[str, Any]) -> None:
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    temporal.write_text(json.dumps(estado, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    os.replace(temporal, ruta)


def _fmt(media: float, desvio: float) -> str:
    return "%.3g+-%.2g" % (media, desvio)


def _tabla_resumen(csv_ruta: Path) -> list[tuple[str, int, str, str]]:
    with csv_ruta.open(newline="", encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    referencia = next((f for f in filas if f["cond"] == "BASE"), None)
    if referencia is None:
        referencia = next((f for f in filas if f["cond"] == "PING"), None)
    ref_media = float(referencia["p2p_cuentas_media"]) if referencia else 0.0
    ref_std = float(referencia["p2p_cuentas_std"]) if referencia else 0.0
    tabla = []
    for fila in filas:
        media = float(fila["p2p_cuentas_media"])
        desvio = float(fila["p2p_cuentas_std"])
        if fila is referencia:
            veredicto = "referencia"
        elif referencia:
            veredicto = "EFECTO" if abs(media - ref_media) > 3.0 * ref_std else "sin efecto"
        else:
            veredicto = "sin referencia"
        tabla.append((fila["cond"], int(fila["n"]), _fmt(media, desvio), veredicto))
    return tabla


def escribir_campana_md(raiz: Path, estado: dict[str, Any] | None = None) -> Path:
    raiz = Path(raiz)
    estado = estado or {}
    pasos = estado.get("pasos", estado)
    nombres = {p.name for p in raiz.iterdir() if p.is_dir() and (p / "resumen.csv").exists()}
    nombres.update(k for k, v in pasos.items() if isinstance(v, dict))
    lineas = ["# Campaña de ruido", ""]
    for nombre in sorted(nombres):
        info = pasos.get(nombre, {})
        etiqueta = info.get("estado", "sin estado") if isinstance(info, dict) else str(info)
        lineas += [f"## {nombre}", "", f"Estado: {etiqueta}", ""]
        csv_ruta = raiz / nombre / "resumen.csv"
        if csv_ruta.exists():
            lineas += ["| cond | n | p2p cuentas | veredicto |",
                       "|---|---:|---:|---|"]
            lineas += [f"| {cond} | {n} | {p2p} | {veredicto} |"
                       for cond, n, p2p, veredicto in _tabla_resumen(csv_ruta)]
            lineas.append("")
        else:
            lineas += ["Sin resumen disponible.", ""]
    salida = raiz / "campana.md"
    salida.write_text("\n".join(lineas), encoding="utf-8")
    return salida


def correr(args: argparse.Namespace) -> int:
    raiz = Path(args.raiz).resolve()
    raiz.mkdir(parents=True, exist_ok=True)
    log = raiz / "campana.log"
    estado_ruta = raiz / "campana_estado.json"
    estado = _cargar_estado(estado_ruta)
    pasos_estado = estado.setdefault("pasos", {})
    plan = filtrar_plan(cargar_plan(args.plan), args.solo)
    if not plan:
        raise ValueError("el filtro --solo no selecciono pasos")

    for paso in plan:
        exp = str(paso["exp"])
        previo = pasos_estado.get(exp, {})
        if previo.get("estado") == "ok" and not args.rehacer:
            with log.open("a", encoding="utf-8") as fh:
                _log(fh, f"-- {exp}: ya terminado, se saltea")
            continue
        requiere_maestro = bool(paso.get("requiere_maestro")) or any(
            str(c).upper() == "RX" for c in paso["cond"])
        razon = None
        if not _puerto_presente(args.port):
            razon = f"puerto {args.port} no disponible"
        elif requiere_maestro and not _puerto_presente(args.maestro):
            razon = f"maestro {args.maestro or '(no indicado)'} no disponible"
        if razon:
            pasos_estado[exp] = {"estado": "salteado", "motivo": razon,
                                 "fecha": _marca()}
            _guardar_estado(estado_ruta, estado)
            with log.open("a", encoding="utf-8") as fh:
                _log(fh, f"-- {exp}: salteado ({razon})")
            continue

        comando = comando_medicion(paso, raiz, args.port, args.maestro, args.nota)
        limite_s = int(paso["rep"]) * len(paso["cond"]) * 90 + 600
        resultado = ejecutar_con_vigilancia(
            comando, log, args.silencio_min * 60.0, limite_s)
        if resultado.estado == "colgado":
            reaparecio = esperar_puerto(args.port, 600.0)
            if reaparecio and (not requiere_maestro or _puerto_presente(args.maestro)):
                with log.open("a", encoding="utf-8") as fh:
                    _log(fh, f"-- {exp}: reintento unico")
                resultado = ejecutar_con_vigilancia(
                    comando, log, args.silencio_min * 60.0, limite_s)
            elif not reaparecio:
                resultado = ResultadoProceso("colgado", "el puerto no reaparecio")

        directorio = raiz / exp
        if directorio.exists():
            _ejecutar_auxiliar([sys.executable, str(RUIDO_SD), "resumir", str(directorio)], log)
            _ejecutar_auxiliar([sys.executable, str(ESPECTRO), str(directorio)], log)
            _ejecutar_auxiliar(
                [sys.executable, str(TRANSITORIO_ARRANQUE), str(directorio)], log)
        pasos_estado[exp] = {"estado": resultado.estado, "motivo": resultado.motivo,
                             "retorno": resultado.retorno, "fecha": _marca()}
        _guardar_estado(estado_ruta, estado)

    escribir_campana_md(raiz, estado)
    return 0 if all(pasos_estado.get(str(p["exp"]), {}).get("estado") == "ok"
                    for p in plan) else 1


def resumir(args: argparse.Namespace) -> int:
    raiz = Path(args.raiz).resolve()
    escribir_campana_md(raiz, _cargar_estado(raiz / "campana_estado.json"))
    return 0


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="subcomando", required=True)
    cp = subs.add_parser("correr")
    cp.add_argument("--plan", required=True, help="rf, sd o archivo JSON")
    cp.add_argument("--raiz", required=True)
    cp.add_argument("--port", default="COM8")
    cp.add_argument("--maestro")
    cp.add_argument("--solo")
    cp.add_argument("--nota", default="")
    cp.add_argument("--silencio-min", type=float, default=6.0)
    cp.add_argument("--rehacer", action="store_true")
    cp.set_defaults(func=correr)
    rp = subs.add_parser("resumir")
    rp.add_argument("--raiz", required=True)
    rp.set_defaults(func=resumir)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = crear_parser().parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
