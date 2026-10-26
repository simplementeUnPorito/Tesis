#!/usr/bin/env python3
"""Matriz automatizada del banco S3.

Ejecuta cada prueba por separado, conserva el tramo correspondiente de
``maestro.log`` y genera un resumen que se puede leer sin revisar datos crudos.
Usar ``--dry-run`` para ver el plan sin conectarse al banco.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, NamedTuple


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parents[1]
CAPTURAS_DIR = SCRIPT_DIR / "capturas"
DURACION_DIR = SCRIPT_DIR / "duracion"
MATRIZ_DIR = SCRIPT_DIR / "matriz"
SPB = 30


class Prueba(NamedTuple):
    id: str
    tipo: str
    descripcion: str
    parametros: dict[str, Any]


def parsear_nodos(texto: str) -> list[int]:
    """Convierte una lista de nodos y rechaza valores ambiguos."""
    partes = [p.strip() for p in texto.split(",") if p.strip()]
    if not partes:
        raise ValueError("la lista de nodos está vacía")
    try:
        nodos = [int(p) for p in partes]
    except ValueError as exc:
        raise ValueError("los nodos deben ser números separados por comas") from exc
    if len(nodos) != len(set(nodos)):
        raise ValueError("la lista de nodos tiene repetidos")
    if any(n < 1 or n > 254 for n in nodos):
        raise ValueError("cada nodo debe estar entre 1 y 254")
    return nodos


def _nodo(datos: dict[str, Any], numero: int) -> dict[str, Any] | None:
    nodos = datos.get("nodos", {})
    return nodos.get(str(numero), nodos.get(numero))


def resumir_captura(
    datos: dict[str, Any],
    nodos: list[int],
    lotes_esperados: int | None = None,
    mismos_lotes: bool = False,
) -> dict[str, Any]:
    """Evalúa solamente las cifras producidas por captura_ws.py."""
    por_nodo: dict[str, Any] = {}
    correcto = True
    vistos: list[int] = []
    cifras: list[str] = []
    for numero in nodos:
        original = _nodo(datos, numero)
        if original is None:
            por_nodo[str(numero)] = {"error": "nodo ausente"}
            cifras.append(f"S{numero}: ausente")
            correcto = False
            continue
        actual = {
            "lotes_vistos": int(original.get("lotes_vistos", -1)),
            "n_faltan": int(original.get("n_faltan", -1)),
            "nan": int(original.get("nan", -1)),
            "muestras": int(original.get("muestras", -1)),
        }
        por_nodo[str(numero)] = actual
        vistos.append(actual["lotes_vistos"])
        nodo_ok = actual["n_faltan"] == 0 and actual["nan"] == 0
        if lotes_esperados is not None:
            nodo_ok = nodo_ok and actual["lotes_vistos"] == lotes_esperados
        correcto = correcto and nodo_ok
        cifras.append(
            f"S{numero}: lotes={actual['lotes_vistos']}, faltan={actual['n_faltan']}, "
            f"NaN={actual['nan']}"
        )
    if mismos_lotes and (len(vistos) != len(nodos) or len(set(vistos)) != 1):
        correcto = False
    return {"pass": correcto, "por_nodo": por_nodo, "cifras": "; ".join(cifras)}


def resumir_log(lineas: list[str]) -> dict[str, int]:
    """Cuenta incidentes del maestro sin inflar eventos de varias líneas."""
    return {
        "txstall": sum("[TXSTALL]" in l and "sin avisos" in l.lower() for l in lineas),
        "no_response_ftm": sum("[FTM]" in l and re.search(r"\bev=3\b", l) is not None for l in lineas),
        "responder_sin_respuesta": sum("responder sin respuesta" in l.lower() for l in lineas),
        "vigia": sum("vigia" in l.lower() for l in lineas),
        "reinicios_esclavos": sum("boot chip=" in l and re.search(r"\[S\d+>\]", l) is not None for l in lineas),
        "panicos": sum("guru meditation" in l.lower() or "panic'ed" in l.lower() for l in lineas),
        "coredump": sum("[COREDUMP]" in l and "no hay" not in l.lower() for l in lineas),
    }


def resumir_sync(
    lineas: list[str], nodos: list[int], exigir_ftm: bool = False, limite_us: int = 20
) -> dict[str, Any]:
    """Extrae el START y la dispersión de las conversiones válidas del tramo."""
    starts = [int(m.group(1)) for l in lineas if (m := re.search(r"\[MASTER\] START\b.*?\bftm=(\d+)", l))]
    eventos: dict[str, dict[int, int]] = {"SYNCFTM": {}, "SYNCRX": {}, "SYNCBC": {}}
    patron = re.compile(r"\[S(\d+)>\].*?\[(SYNCFTM|SYNCRX|SYNCBC)\].*?real_maestro=(\d+)")
    for linea in lineas:
        m = patron.search(linea)
        if not m or ("conv=" in linea and re.search(r"\bconv=1\b", linea) is None):
            continue
        numero = int(m.group(1))
        if numero in nodos:
            eventos[m.group(2)][numero] = int(m.group(3))
    orden = ["SYNCFTM"] if exigir_ftm else ["SYNCRX", "SYNCBC", "SYNCFTM"]
    metodo = next((nombre for nombre in orden if eventos[nombre]), None)
    valores = eventos[metodo] if metodo else {}
    dispersion = max(valores.values()) - min(valores.values()) if len(valores) >= 2 else None
    start_ftm = starts[-1] if starts else None
    completo = set(valores) == set(nodos)
    correcto = completo and dispersion is not None
    if exigir_ftm:
        correcto = correcto and start_ftm == 1 and dispersion <= limite_us
    return {
        "pass": correcto,
        "start_ftm": start_ftm,
        "metodo": metodo,
        "nodos": sorted(valores),
        "real_maestro": {str(n): v for n, v in sorted(valores.items())},
        "dispersion_us": dispersion,
    }


def resumir_duracion(datos: dict[str, Any], nodos: list[int]) -> dict[str, Any]:
    """Valida el total drenado y calcula el peor atraso observado."""
    esperado = round(float(datos["segundos"]) * float(datos["fs"]) / SPB)
    tolerancia = esperado * 0.01
    finales: dict[str, int | None] = {}
    atrasos: dict[str, float | None] = {}
    correcto = True
    for numero in nodos:
        clave = str(numero)
        valor = datos.get("final", {}).get(clave, datos.get("final", {}).get(numero))
        final = int(valor) if valor is not None else None
        finales[clave] = final
        if final is None or abs(final - esperado) > tolerancia:
            correcto = False
        serie = [f.get(f"S{numero}_atraso") for f in datos.get("filas", [])]
        validos = [float(x) for x in serie if x is not None]
        atrasos[clave] = max(validos) if validos else None
    cifras = "; ".join(
        f"S{n}: final={finales[str(n)]}, atraso_max={atrasos[str(n)]}" for n in nodos
    )
    return {
        "pass": correcto,
        "esperado": esperado,
        "tolerancia": tolerancia,
        "final": finales,
        "atraso_maximo": atrasos,
        "cifras": cifras,
    }


def armar_plan(
    solo: set[str], saltar: set[str], con_ota: bool, con_duracion: bool
) -> list[Prueba]:
    pruebas = [Prueba("estado", "estado", "HTTP, HELLO y modelos FTM", {})]
    for almacen in range(3):
        pruebas.append(Prueba(f"async_{almacen}", "captura", f"async, almacén {almacen}, 200 lotes", {"modo": "async", "almacen": almacen, "n": 200, "sync": 0}))
    for almacen in range(3):
        pruebas.append(Prueba(f"rt_{almacen}", "captura", f"tiempo real, almacén {almacen}, 600 lotes", {"modo": "rt", "almacen": almacen, "n": 600, "sync": 0}))
    pruebas.extend([
        Prueba("rapida_1", "captura", "rápida, almacén 1, 200 lotes", {"modo": "rapida", "almacen": 1, "n": 200, "sync": 0}),
        Prueba("rt_sinlimite", "captura", "tiempo real sin límite durante 30 s", {"modo": "rt", "almacen": 1, "n": 0, "stop_s": 30, "sync": 0}),
        Prueba("droptest", "captura", "tiempo real con descarte 1 de cada 7", {"modo": "rt", "almacen": 1, "n": 600, "droptest": 7, "sync": 0}),
    ])
    for sync in range(3):
        pruebas.append(Prueba(f"sync_{sync}", "captura", f"sincronismo {sync}, 300 lotes", {"modo": "rt", "almacen": 1, "n": 300, "sync": sync}))
    pruebas.extend([
        Prueba("ota", "ota", "OTA de un esclavo y recuperación", {}),
        Prueba("duracion", "duracion", "captura prolongada y drenaje", {}),
        Prueba("salud", "salud", "incidentes en todo el tramo de la matriz", {}),
    ])
    conocidos = {p.id for p in pruebas}
    desconocidos = (solo | saltar) - conocidos
    if desconocidos:
        raise ValueError("pruebas desconocidas: " + ", ".join(sorted(desconocidos)))
    resultado = []
    for prueba in pruebas:
        habilitada = (prueba.id != "ota" or con_ota or prueba.id in solo)
        habilitada = habilitada and (prueba.id != "duracion" or con_duracion or prueba.id in solo)
        if solo:
            habilitada = habilitada and prueba.id in solo
        if prueba.id in saltar:
            habilitada = False
        if habilitada:
            resultado.append(prueba)
    return resultado


def contar_lineas(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8", errors="replace") as archivo:
        return sum(1 for _ in archivo)


def leer_log(path: Path, desde: int) -> tuple[list[str], int]:
    if not path.exists():
        return [], 0
    with path.open("r", encoding="utf-8", errors="replace") as archivo:
        todas = archivo.readlines()
    return [l.rstrip("\r\n") for l in todas[desde:]], len(todas)


def _importar_maestro():
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    from maestro_ws import Maestro, PT_HB, PT_STATUS

    return Maestro, PT_HB, PT_STATUS


def preparar_banco(log_path: Path, nodos: list[int], timeout: float = 45.0) -> dict[str, Any]:
    """Manda STOP y espera estado estable y modelos FTM vigentes."""
    Maestro, PT_HB, _ = _importar_maestro()
    estado = {"valor": None}
    modelos: set[int] = set()
    maestro = Maestro(reconnect=True)

    def paquete(p):
        _, numero, tipo, _b2, _b1, b0 = p
        if tipo == PT_HB and numero in (0, 0xFF):
            estado["valor"] = b0

    def texto(_t, obj):
        if isinstance(obj, dict) and obj.get("type") == "ftm" and int(obj.get("model_ok", 0)) == 1:
            modelos.add(int(obj.get("node", -1)))

    maestro.on_packet = paquete
    maestro.on_text = texto
    inicio_log = contar_lineas(log_path)
    t0 = time.monotonic()
    try:
        maestro.connect()
        maestro.std(0xA4)
        maestro.std(0xA5)
        while time.monotonic() - t0 < timeout:
            nuevas, _ = leer_log(log_path, inicio_log)
            for linea in nuevas:
                m = re.search(r"\[FTM\] S(\d+).*?\bmodelo=1\b", linea)
                if m:
                    modelos.add(int(m.group(1)))
            if estado["valor"] in (0, 2) and set(nodos) <= modelos:
                return {"estado": estado["valor"], "modelos": sorted(modelos), "espera_s": round(time.monotonic() - t0, 2)}
            time.sleep(0.5)
    finally:
        maestro.close()
    faltan = sorted(set(nodos) - modelos)
    raise TimeoutError(f"el banco no volvió a IDLE/ARMED con modelos FTM; estado={estado['valor']}, faltan={faltan}")


def mandar_stop() -> None:
    Maestro, _, _ = _importar_maestro()
    maestro = Maestro()
    try:
        maestro.connect(timeout=5)
        maestro.std(0xA4)
        time.sleep(0.5)
    finally:
        maestro.close()


def ejecutar_estado(log_path: Path, inicio_log: int, nodos: list[int]) -> dict[str, Any]:
    Maestro, _, PT_STATUS = _importar_maestro()
    codigo_http = None
    error_http = None
    try:
        with urllib.request.urlopen("http://192.168.4.1/", timeout=10) as respuesta:
            codigo_http = respuesta.status
    except Exception as exc:  # el detalle queda en el JSON de la prueba
        error_http = str(exc)

    hellos: set[int] = set()
    modelos: set[int] = set()
    maestro = Maestro(reconnect=True)

    def paquete(p):
        _, numero, tipo, subtipo, _b1, _b0 = p
        if tipo == PT_STATUS and subtipo == 0x01 and numero in nodos:
            hellos.add(numero)

    maestro.on_packet = paquete
    t0 = time.monotonic()
    try:
        maestro.connect()
        maestro.std(0xA5)
        while time.monotonic() - t0 < 30:
            lineas, _ = leer_log(log_path, inicio_log)
            for linea in lineas:
                m = re.search(r"\[FTM\] S(\d+).*?\bmodelo=1\b", linea)
                if m:
                    modelos.add(int(m.group(1)))
            if set(nodos) <= hellos and set(nodos) <= modelos:
                break
            time.sleep(0.5)
    finally:
        maestro.close()
    correcto = codigo_http == 200 and set(nodos) <= hellos and set(nodos) <= modelos
    return {
        "pass": correcto,
        "http": codigo_http,
        "error_http": error_http,
        "hello_ws": sorted(hellos),
        "modelo_ftm_log": sorted(modelos),
        "cifras": f"HTTP={codigo_http}; HELLO={sorted(hellos)}; FTM modelo=1={sorted(modelos)}",
    }


def _inventario_json(carpeta: Path) -> dict[Path, int]:
    if not carpeta.exists():
        return {}
    return {p.resolve(): p.stat().st_mtime_ns for p in carpeta.rglob("*.json")}


def _json_nuevo(carpeta: Path, antes: dict[Path, int]) -> Path:
    despues = _inventario_json(carpeta)
    candidatos = [p for p, mtime in despues.items() if p not in antes or mtime != antes[p]]
    if not candidatos:
        raise FileNotFoundError(f"no apareció un JSON nuevo en {carpeta}")
    return max(candidatos, key=lambda p: despues[p])


def ejecutar_subproceso(comando: list[str], timeout: float) -> dict[str, Any]:
    proceso = subprocess.run(
        comando,
        cwd=REPO_DIR,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return {"codigo_salida": proceso.returncode, "stdout": proceso.stdout, "stderr": proceso.stderr}


def ejecutar_captura(prueba: Prueba, nodos: list[int]) -> dict[str, Any]:
    antes = _inventario_json(CAPTURAS_DIR)
    p = prueba.parametros
    comando = [
        sys.executable, str(SCRIPT_DIR / "captura_ws.py"),
        "--modo", str(p["modo"]), "--almacen", str(p["almacen"]),
        "--sync", str(p.get("sync", 0)), "--n", str(p["n"]),
        "--nodos", ",".join(map(str, nodos)),
    ]
    if p.get("stop_s"):
        comando += ["--stop-s", str(p["stop_s"])]
    if p.get("droptest"):
        comando += ["--droptest", str(p["droptest"])]
    proceso = ejecutar_subproceso(comando, timeout=420)
    if proceso["codigo_salida"] != 0:
        raise RuntimeError(f"captura_ws.py terminó con {proceso['codigo_salida']}: {proceso['stderr'][-1000:]}")
    resumen_path = _json_nuevo(CAPTURAS_DIR, antes)
    datos = json.loads(resumen_path.read_text(encoding="utf-8"))
    resumen = resumir_captura(
        datos,
        nodos,
        lotes_esperados=p["n"] if p["n"] else None,
        mismos_lotes=p["n"] == 0,
    )
    resumen.update({"captura": str(resumen_path), "subproceso": proceso})
    return resumen


def ejecutar_ota(log_path: Path, inicio_log: int, nodo: int, entorno: str) -> dict[str, Any]:
    t0 = time.monotonic()
    comando = [sys.executable, str(SCRIPT_DIR / "ota.py"), "--node", str(nodo), "--env", entorno, "--timeout", "90"]
    proceso = ejecutar_subproceso(comando, timeout=180)
    hello = False
    modelo = False
    while time.monotonic() - t0 <= 90 and not (hello and modelo):
        lineas, _ = leer_log(log_path, inicio_log)
        hello = any(re.search(rf"\bHELLO node={nodo}\b", l) for l in lineas)
        modelo = any(re.search(rf"\[FTM\] S{nodo}\b.*?\bmodelo=1\b", l) for l in lineas)
        if not (hello and modelo):
            time.sleep(0.5)
    demora = time.monotonic() - t0
    correcto = proceso["codigo_salida"] == 0 and hello and modelo and demora <= 90
    return {
        "pass": correcto,
        "nodo": nodo,
        "entorno": entorno,
        "hello": hello,
        "modelo_ftm": modelo,
        "recuperacion_s": round(demora, 2),
        "cifras": f"S{nodo}: HELLO={hello}, modelo={modelo}, recuperación={demora:.1f} s",
        "subproceso": proceso,
    }


def ejecutar_duracion(nodos: list[int], segundos: float, lineas: list[str] | None = None) -> dict[str, Any]:
    antes = _inventario_json(DURACION_DIR)
    comando = [
        sys.executable, str(SCRIPT_DIR / "prueba_duracion.py"), "--n", "1", "--s", str(segundos),
        "--nodos", ",".join(map(str, nodos)), "--almacen", "1", "--sync", "0",
    ]
    proceso = ejecutar_subproceso(comando, timeout=segundos + 180)
    if proceso["codigo_salida"] != 0:
        raise RuntimeError(f"prueba_duracion.py terminó con {proceso['codigo_salida']}: {proceso['stderr'][-1000:]}")
    resumen_path = _json_nuevo(DURACION_DIR, antes)
    datos = json.loads(resumen_path.read_text(encoding="utf-8"))
    resumen = resumir_duracion(datos, nodos)
    resumen.update({"duracion_json": str(resumen_path), "subproceso": proceso})
    if lineas is not None:
        incidentes = resumir_log(lineas)
        claves = ("txstall", "responder_sin_respuesta", "reinicios_esclavos", "panicos")
        resumen["incidentes"] = {k: incidentes[k] for k in claves}
        resumen["pass"] = resumen["pass"] and all(incidentes[k] == 0 for k in claves)
    return resumen


def guardar_json(path: Path, datos: dict[str, Any]) -> None:
    path.write_text(json.dumps(datos, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


def generar_markdown(resultados: list[dict[str, Any]], stamp: str) -> str:
    filas = [
        f"# Matriz de pruebas S3 — {stamp}", "",
        "| Prueba | Resultado | Cifras clave | Duración |",
        "|---|---:|---|---:|",
    ]
    for r in resultados:
        cifras = str(r.get("cifras", r.get("error", ""))).replace("|", "\\|").replace("\n", " ")
        filas.append(f"| {r['id']} | {'PASS' if r['pass'] else 'FAIL'} | {cifras} | {r['duracion_s']:.1f} s |")
    aprobadas = sum(r["pass"] for r in resultados)
    filas += ["", f"Resultado: **{aprobadas}/{len(resultados)} PASS**.", ""]
    return "\n".join(filas)


def _csv_set(texto: str) -> set[str]:
    return {x.strip() for x in texto.split(",") if x.strip()}


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Matriz automatizada del banco S3")
    parser.add_argument("--dry-run", action="store_true", help="mostrar el plan sin conectarse")
    parser.add_argument("--nodos", default="2,3,4")
    parser.add_argument("--log", default=str(SCRIPT_DIR / "maestro.log"))
    parser.add_argument("--solo", default="", help="IDs separados por comas")
    parser.add_argument("--saltar", default="", help="IDs separados por comas")
    parser.add_argument("--con-ota", action="store_true")
    parser.add_argument("--ota-node", type=int, default=4)
    parser.add_argument("--ota-env", default="slaveS3_4")
    parser.add_argument("--con-duracion", action="store_true")
    parser.add_argument("--duracion-s", type=float, default=120.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    # En Windows dejamos UTF-8 explícito para que los mensajes rioplatenses no
    # dependan de la página de códigos de la consola que lance la matriz.
    for flujo in (sys.stdout, sys.stderr):
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8")
    args = crear_parser().parse_args(argv)
    try:
        nodos = parsear_nodos(args.nodos)
        plan = armar_plan(_csv_set(args.solo), _csv_set(args.saltar), args.con_ota, args.con_duracion)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    if any(p.id == "ota" for p in plan) and args.ota_node not in nodos:
        print(f"Error: el nodo OTA {args.ota_node} no está en --nodos", file=sys.stderr)
        return 2
    if args.duracion_s <= 0:
        print("Error: --duracion-s debe ser mayor que cero", file=sys.stderr)
        return 2
    if not plan:
        print("Error: no quedó ninguna prueba seleccionada", file=sys.stderr)
        return 2
    if args.dry_run:
        print(f"Plan para nodos {','.join(map(str, nodos))} ({len(plan)} pruebas):")
        for i, prueba in enumerate(plan, 1):
            extra = ""
            if prueba.id == "ota":
                extra = f" [S{args.ota_node}, {args.ota_env}]"
            elif prueba.id == "duracion":
                extra = f" [{args.duracion_s:g} s]"
            print(f"{i:2d}. {prueba.id}: {prueba.descripcion}{extra}")
        print("Dry-run: no se abrió HTTP/WS, no se mandó STOP y no se ejecutaron subprocesos.")
        return 0

    log_path = Path(args.log).resolve()
    if not log_path.exists():
        print(f"Error: no existe el log {log_path}", file=sys.stderr)
        return 2
    stamp = time.strftime("%Y%m%d_%H%M%S")
    salida = MATRIZ_DIR / stamp
    salida.mkdir(parents=True, exist_ok=False)
    matriz_inicio = contar_lineas(log_path)
    resultados: list[dict[str, Any]] = []

    for prueba in plan:
        print(f"\n[{prueba.id}] {prueba.descripcion}", flush=True)
        inicio = contar_lineas(log_path)
        medicion_inicio = inicio
        t0 = time.monotonic()
        resultado: dict[str, Any] = {"id": prueba.id, "pass": False}
        try:
            preparacion = None
            if prueba.tipo != "salud":
                preparacion = preparar_banco(log_path, nodos)
                # El JSON conserva también la preparación, pero un PASS sólo
                # puede apoyarse en evidencia generada desde acá en adelante.
                medicion_inicio = contar_lineas(log_path)
            if prueba.tipo == "estado":
                resultado.update(ejecutar_estado(log_path, medicion_inicio, nodos))
            elif prueba.tipo == "captura":
                resultado.update(ejecutar_captura(prueba, nodos))
                tramo_parcial, _ = leer_log(log_path, medicion_inicio)
                if prueba.id.startswith("sync_"):
                    modo = int(prueba.id.rsplit("_", 1)[1])
                    sync = resumir_sync(tramo_parcial, nodos, exigir_ftm=modo == 0)
                    resultado["sincronismo"] = sync
                    if modo == 0:
                        resultado["pass"] = resultado["pass"] and sync["pass"]
                    resultado["cifras"] += f"; {sync['metodo']} dispersión={sync['dispersion_us']} us; START ftm={sync['start_ftm']}"
            elif prueba.tipo == "ota":
                resultado.update(ejecutar_ota(log_path, medicion_inicio, args.ota_node, args.ota_env))
            elif prueba.tipo == "duracion":
                resultado.update(ejecutar_duracion(nodos, args.duracion_s))
                tramo_parcial, _ = leer_log(log_path, medicion_inicio)
                incidentes = resumir_log(tramo_parcial)
                claves = ("txstall", "responder_sin_respuesta", "reinicios_esclavos", "panicos")
                resultado["incidentes"] = {k: incidentes[k] for k in claves}
                resultado["pass"] = resultado["pass"] and all(incidentes[k] == 0 for k in claves)
                resultado["cifras"] += "; incidentes=" + json.dumps(resultado["incidentes"], ensure_ascii=False)
            elif prueba.tipo == "salud":
                tramo_matriz, _ = leer_log(log_path, matriz_inicio)
                incidentes = resumir_log(tramo_matriz)
                resultado.update({
                    "pass": all(v == 0 for v in incidentes.values()),
                    "incidentes": incidentes,
                    "cifras": ", ".join(f"{k}={v}" for k, v in incidentes.items()),
                })
            resultado["preparacion"] = preparacion
        except Exception as exc:
            resultado["error"] = f"{type(exc).__name__}: {exc}"
            resultado["cifras"] = resultado["error"]
            print(f"  ERROR: {resultado['error']}", flush=True)
            try:
                mandar_stop()
            except Exception as stop_exc:
                resultado["error_stop"] = str(stop_exc)
        tramo, fin = leer_log(log_path, inicio)
        resultado.update({
            "duracion_s": round(time.monotonic() - t0, 3),
            "log_linea_inicio": inicio + 1,
            "log_linea_medicion": medicion_inicio + 1,
            "log_linea_fin": fin,
            "tramo_log": tramo,
        })
        guardar_json(salida / f"{prueba.id}.json", resultado)
        resultados.append(resultado)
        print(f"  {'PASS' if resultado['pass'] else 'FAIL'} — {resultado.get('cifras', '')}", flush=True)

    resumen = {
        "stamp": stamp,
        "nodos": nodos,
        "log": str(log_path),
        "salida": str(salida),
        "pass": all(r["pass"] for r in resultados),
        "aprobadas": sum(r["pass"] for r in resultados),
        "total": len(resultados),
        "resultados": [{k: v for k, v in r.items() if k != "tramo_log"} for r in resultados],
    }
    guardar_json(salida / "resumen.json", resumen)
    (salida / "resumen.md").write_text(generar_markdown(resultados, stamp), encoding="utf-8")
    print(f"\nResumen: {salida / 'resumen.md'}")
    return 0 if resumen["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
