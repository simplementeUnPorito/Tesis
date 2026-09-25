#!/usr/bin/env python3
"""Elige, para cada par (PGA, PGAOUT), el mejor punto de partida (IDAC0..3)
a partir de campañas de autocalibración de banco (resultados.jsonl).

Lee una o más campañas en formato JSON Lines (una visita por línea),
deduplica por (marca, pga, pgaout, vuelta) porque una campaña puede arrastrar
como semilla las visitas de una campaña anterior, puntúa cada visita y
selecciona el mejor punto no fragil por par de ganancias.

Sólo biblioteca estándar. Ver `lab/test_semilla_puntos.py` para los tests.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ganancias reales posibles; el CÓDIGO de una ganancia es su índice en esta lista.
GANANCIAS = [1, 2, 4, 8, 16, 24, 32, 48, 50]

# Umbrales de calidad (en mV), sobre |LPo_final_mV|.
UMBRAL_NOTA_A = 24.3
UMBRAL_NOTA_B = 48.5
UMBRAL_NOTA_C = 73.0

# Ventana válida del tap LPo es ±97 mV; "no clavado contra el riel" se exige
# más estricto que la ventana completa (coincide con el umbral de nota C).
UMBRAL_NO_CLAVADO = 73.0

# Pico a pico máximo (mV) para considerar la visita "quieta".
UMBRAL_PP_QUIETO = 30.0

# IDAC3 se considera frágil (sin autoridad de corrección) por encima de este valor absoluto.
UMBRAL_IDAC_FRAGIL = 200

# Tope físico de un IDAC de 8 bits con signo tal como se usa en este firmware.
TOPE_IDAC = 255

# Periodo de muestreo del barrido (barrido_total.py): una muestra de LPo cada 2 s.
MUESTREO_S = 2.0

# LPo_pp_final_mV se calcula en barrido_total.py sobre las últimas 15 muestras
# VÁLIDAS de LPo (lp[-15:]). Si hay menos de 15 muestras válidas la ventana no
# está llena: max-min de pocos puntos (o de uno solo) da un pp artificialmente
# bajo -- incluso 0.0 -- que no significa quietud sino ausencia de dato.
MIN_MUESTRAS_VALIDAS = 15


def ganancia_a_codigo(ganancia: float) -> int:
    """Devuelve el código (índice) de una ganancia real en la lista GANANCIAS."""
    return GANANCIAS.index(ganancia)


def cargar_visitas(rutas: list[str]) -> tuple[list[dict], list[dict]]:
    """Lee las rutas jsonl dadas y devuelve (visitas_crudas, fuentes).

    `fuentes` es una lista de {"ruta": ..., "visitas": N} para reportar
    cuántas visitas aportó cada archivo.
    """
    visitas: list[dict] = []
    fuentes: list[dict] = []
    for ruta in rutas:
        path = Path(ruta)
        n = 0
        with path.open(encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                visitas.append(json.loads(linea))
                n += 1
        fuentes.append({"ruta": str(ruta), "visitas": n})
    return visitas, fuentes


def deduplicar(visitas: list[dict]) -> list[dict]:
    """Deduplica visitas por la tupla (marca, pga, pgaout, vuelta).

    Cuando dos campañas comparten una visita (la más nueva arrastra la
    semilla de la más vieja), sobrevive la última leída para esa clave;
    en la práctica el contenido es idéntico para claves duplicadas.
    """
    vistas: dict[tuple, dict] = {}
    for v in visitas:
        clave = (v["marca"], v["pga"], v["pgaout"], v["vuelta"])
        vistas[clave] = v
    return list(vistas.values())


def penal(x: float) -> float:
    """Penalización por exceso de un IDAC por encima de 200 (en valor absoluto)."""
    return max(0.0, x - UMBRAL_IDAC_FRAGIL) * 5


def n_validas(r: dict) -> int:
    """Cantidad de muestras VÁLIDAS de LPo que tuvo la visita.

    El pico a pico (`LPo_pp_final_mV`) se calcula en barrido_total.py sobre
    `lp[-15:]`, donde `lp` son sólo las muestras válidas de LPo (el `serie`
    del JSONL está truncado a 15 frames y no trae un campo `valido`, así
    que no sirve para contar). El dato autoritativo es `taps.LP.valido_pct`
    combinado con `duracion_s`, sabiendo que el muestreo del barrido es de
    2 s por muestra.
    """
    v = (r.get("taps") or {}).get("LP", {}).get("valido_pct")
    d = r.get("duracion_s")
    if v is None or d is None:
        return 0
    return int(round(v / 100.0 * (d / MUESTREO_S)))


def nota_de(lpo_abs: float, pp: float | None, muestras_validas: int) -> str | None:
    """Clasifica |LPo_final_mV| en una nota A/B/C/D según los umbrales fijos.

    Replica la lógica autoritativa de `_analizar()` en `barrido_total.py`
    (líneas ~483-493): antes de mirar pp y |LPo|, exige que la ventana del
    pico a pico esté llena (al menos MIN_MUESTRAS_VALIDAS muestras válidas
    de LPo) y que la visita esté quieta (`pp < UMBRAL_PP_QUIETO`). Sin
    ambas guardas, `LPo_pp_final_mV` puede mentir: con pocas muestras
    válidas el pico a pico de una lista corta (incluso de una sola
    muestra) da artificialmente bajo -- hasta 0.0 exacto -- y eso no es
    quietud, es ausencia de dato. Sin nota, la visita no es sembrable
    (devuelve None).
    """
    if muestras_validas < MIN_MUESTRAS_VALIDAS:
        return None
    if pp is None or pp >= UMBRAL_PP_QUIETO:
        return None
    if lpo_abs <= UMBRAL_NOTA_A:
        return "A"
    if lpo_abs <= UMBRAL_NOTA_B:
        return "B"
    if lpo_abs <= UMBRAL_NOTA_C:
        return "C"
    return "D"


def pasa_estricto(pp: float, lpo_abs: float) -> bool:
    """True si la visita está quieta (pp < 30 mV) y no clavada contra el riel
    (|LPo_final_mV| <= 73 mV, dentro de la ventana válida de ±97 mV)."""
    return pp < UMBRAL_PP_QUIETO and lpo_abs <= UMBRAL_NO_CLAVADO


def es_fragil(idac_final: list[int]) -> bool:
    """True si IDAC3 está contra su tope (sin autoridad de corrección)."""
    return abs(idac_final[3]) > UMBRAL_IDAC_FRAGIL


def score_de(lpo_abs: float, idac_final: list[int]) -> float:
    """Puntaje de una visita candidata; MENOR es mejor."""
    return 2 * lpo_abs + penal(abs(idac_final[3])) + penal(abs(idac_final[2]))


def evaluar_visita(v: dict) -> dict:
    """Calcula los campos derivados (nota, fragil, score, pasa_estricto) de una visita."""
    lpo = v.get("LPo_final_mV")
    pp = v.get("LPo_pp_final_mV")
    idac = v.get("idac_final")
    lpo_abs = abs(lpo) if lpo is not None else None
    muestras_validas = n_validas(v)
    resultado = {
        "lpo_abs": lpo_abs,
        "muestras_validas": muestras_validas,
        "nota": nota_de(lpo_abs, pp, muestras_validas) if lpo_abs is not None else None,
        "pasa_estricto": pasa_estricto(pp, lpo_abs) if pp is not None and lpo_abs is not None else False,
        "fragil": es_fragil(idac) if idac and len(idac) == 4 else None,
        "score": score_de(lpo_abs, idac) if lpo_abs is not None and idac and len(idac) == 4 else None,
    }
    return resultado


def elegir_mejores(visitas: list[dict]) -> dict[tuple, dict]:
    """Elige, por par (pga_cod, pgaout_cod), la mejor visita candidata.

    Candidatas: nota A o B, con idac_final completo (4 valores).
    Preferencia: primero no-frágil sobre frágil, luego menor score.
    Devuelve un diccionario {(pga_cod, pgaout_cod): visita_enriquecida},
    donde cada visita enriquecida lleva además "n_candidatas": cuántas
    visitas candidatas (nota A/B) compitieron por ese par.
    """
    mejores: dict[tuple, dict] = {}
    n_candidatas: dict[tuple, int] = {}
    for v in visitas:
        idac = v.get("idac_final")
        if not idac or len(idac) != 4:
            continue
        evalu = evaluar_visita(v)
        if evalu["nota"] not in ("A", "B"):
            continue

        clave = (v["pga_cod"], v["pgaout_cod"])
        candidato = {**v, **evalu}
        n_candidatas[clave] = n_candidatas.get(clave, 0) + 1

        actual = mejores.get(clave)
        if actual is None or _mejor_que(candidato, actual):
            mejores[clave] = candidato

    for clave, v in mejores.items():
        v["n_candidatas"] = n_candidatas[clave]
    return mejores


def _mejor_que(a: dict, b: dict) -> bool:
    """True si el candidato `a` es preferible al candidato `b`.

    Regla: no-frágil siempre gana a frágil, aunque el frágil tenga mejor
    (menor) |LPo|; en igualdad de fragilidad, gana el menor score.
    """
    if a["fragil"] != b["fragil"]:
        return b["fragil"] and not a["fragil"]
    return a["score"] < b["score"]


def construir_reporte(mejores: dict[tuple, dict], fuentes: list[dict]) -> dict:
    """Arma el diccionario de salida (JSON) a partir de los mejores puntos elegidos."""
    puntos = []
    for (pga_cod, pgaout_cod), v in sorted(mejores.items()):
        par = pga_cod * 9 + pgaout_cod
        puntos.append({
            "pga": v["pga"],
            "pgaout": v["pgaout"],
            "pga_cod": pga_cod,
            "pgaout_cod": pgaout_cod,
            "par": par,
            "codes": list(v["idac_final"]),
            "lpo_mv": v["LPo_final_mV"],
            "nota": v["nota"],
            "fragil": v["fragil"],
            "score": v["score"],
            "muestras_validas": v["muestras_validas"],
            "visitas": v["n_candidatas"],
        })

    pares_totales = len(GANANCIAS) * len(GANANCIAS)
    pares_sembrados = sorted(p["par"] for p in puntos)
    pares_no_fragiles = sorted(p["par"] for p in puntos if not p["fragil"])
    todos = set(range(pares_totales))
    pares_faltantes = sorted(todos - set(pares_sembrados))

    return {
        "generado": datetime.now(timezone.utc).astimezone().isoformat(),
        "fuentes": fuentes,
        "puntos": puntos,
        "cobertura": {
            "pares_totales": pares_totales,
            "pares_sembrados": len(pares_sembrados),
            "pares_no_fragiles": len(pares_no_fragiles),
            "pares_faltantes": pares_faltantes,
        },
    }


def imprimir_comandos(reporte: dict, incluir_fragiles: bool) -> list[str]:
    """Devuelve las líneas `punto <par> <c0> <c1> <c2> <c3>` ordenadas por par."""
    lineas = []
    for p in sorted(reporte["puntos"], key=lambda p: p["par"]):
        if p["fragil"] and not incluir_fragiles:
            continue
        c0, c1, c2, c3 = p["codes"]
        lineas.append(f"punto {p['par']} {c0} {c1} {c2} {c3}")
    return lineas


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Elige los mejores puntos de partida de autocalibración por par (PGA, PGAOUT).",
    )
    parser.add_argument(
        "--entrada",
        action="append",
        dest="entradas",
        default=None,
        help="Ruta a un resultados.jsonl (repetible). Por defecto usa las dos campañas conocidas.",
    )
    parser.add_argument(
        "--salida",
        default="lab/semilla_puntos.json",
        help="Ruta del JSON de salida (por defecto lab/semilla_puntos.json).",
    )
    parser.add_argument(
        "--comandos",
        action="store_true",
        help="En vez de emitir el JSON, imprime líneas 'punto <par> <c0> <c1> <c2> <c3>'.",
    )
    parser.add_argument(
        "--incluir-fragiles",
        action="store_true",
        help="Con --comandos, incluye también los puntos frágiles (por defecto se omiten).",
    )
    args = parser.parse_args(argv)

    entradas = args.entradas or [
        "lab/barrido_local_20260922/resultados.jsonl",
        "lab/barrido_reaprendizaje_20260923/resultados.jsonl",
    ]

    visitas_crudas, fuentes = cargar_visitas(entradas)
    visitas = deduplicar(visitas_crudas)
    mejores = elegir_mejores(visitas)
    reporte = construir_reporte(mejores, fuentes)

    if args.comandos:
        lineas = imprimir_comandos(reporte, args.incluir_fragiles)
        salida_texto = "\n".join(lineas)
        print(salida_texto)
    else:
        salida_texto = json.dumps(reporte, ensure_ascii=False, indent=2)
        print(salida_texto)
        cobertura = reporte["cobertura"]
        print(
            f"# cobertura: {cobertura['pares_sembrados']}/{cobertura['pares_totales']} pares sembrados, "
            f"{cobertura['pares_no_fragiles']} no fragiles, "
            f"{len(cobertura['pares_faltantes'])} faltantes",
            file=sys.stderr,
        )

    salida_path = Path(args.salida)
    salida_path.parent.mkdir(parents=True, exist_ok=True)
    salida_path.write_text(json.dumps(reporte, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
