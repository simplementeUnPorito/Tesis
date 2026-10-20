"""Analiza como escala con la ganancia el transitorio de escritura SD."""

import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from lab import ruido_sd as rs  # noqa: E402


FS_HZ = 2604.0
INDICE_MARCA = 20
GANANCIAS = (1, 2, 4, 8, 16, 24, 32, 48, 50)
DATOS = Path(__file__).resolve().parent / "ruido_sd_20261019"
SALIDA = DATOS / "ganancia"
PATRONES = ("E3_pga*", "E3b_tap0_pga*", "E3_pgaout*", "E2_tap0", "E2_tap4")
METRICAS = ("transfer", "busy", "p2p")


def _meta(ruta):
    """Lee exclusivamente la cabecera JSON de una captura."""
    with ruta.open("r", encoding="utf-8") as archivo:
        cabecera = json.loads(archivo.readline())
    meta = cabecera["meta"]
    return {
        "cond": str(meta.get("cond", meta.get("condicion", ""))).upper(),
        "tap": int(meta["tap"]),
        "pga": int(meta["pga"]),
        "pgaout": int(meta["pgaout"]),
    }


def _rutas():
    directorios = set()
    for patron in PATRONES:
        directorios.update(p for p in DATOS.glob(patron) if p.is_dir())
    for directorio in sorted(directorios):
        if "descartado_sin_convergencia" in directorio.parts:
            continue
        yield from sorted(directorio.glob("*.txt"))


def _media_std(valores):
    x = np.asarray(valores, dtype=float)
    if x.size == 1:
        return float(x[0]), 0.0
    return float(x.mean()), float(x.std(ddof=1))


def _medir_grupos():
    grupos = defaultdict(lambda: {"BASE": [], "P4": []})
    descartadas = 0
    for ruta in _rutas():
        meta = _meta(ruta)
        if meta["cond"] not in ("BASE", "P4"):
            continue
        medida = rs._medir(str(ruta))
        if medida is None:
            descartadas += 1
            continue
        clave = (meta["tap"], meta["pga"], meta["pgaout"])
        grupos[clave][meta["cond"]].append(np.asarray(medida["promedio"], dtype=float))

    tiempo_ms = (np.arange(rs.VENTANA_ANTES + rs.VENTANA_DESPUES + 1)
                 - INDICE_MARCA) * 1000.0 / FS_HZ
    mascara_transfer = (tiempo_ms >= 2.0) & (tiempo_ms <= 7.0)
    mascara_busy = (tiempo_ms >= 9.0) & (tiempo_ms <= 20.0)
    filas = []
    omitidos = []
    for (tap, pga, pgaout), capturas in sorted(grupos.items()):
        if not capturas["BASE"] or not capturas["P4"]:
            omitidos.append((tap, pga, pgaout))
            continue
        base = np.mean(np.stack(capturas["BASE"]), axis=0)
        valores = {metrica: [] for metrica in METRICAS}
        for promedio in capturas["P4"]:
            diferencia = promedio - base
            diferencia -= diferencia[:INDICE_MARCA].mean()
            transfer = float(diferencia[mascara_transfer].mean())
            busy = float(np.max(np.abs(diferencia[mascara_busy])))
            valores["transfer"].append(transfer)
            valores["busy"].append(busy)
            valores["p2p"].append(float(np.ptp(diferencia)))

        ganancia_pga = GANANCIAS[pga]
        ganancia_pgaout = GANANCIAS[pgaout]
        divisor = ganancia_pga * (ganancia_pgaout if tap == 4 else 1)
        fila = {
            "tap": tap,
            "pga_codigo": pga,
            "pga_ganancia": ganancia_pga,
            "pgaout_codigo": pgaout,
            "pgaout_ganancia": ganancia_pgaout,
            "ganancia_normalizacion": divisor,
            "n": len(capturas["P4"]),
            "n_base": len(capturas["BASE"]),
        }
        for metrica in METRICAS:
            media, std = _media_std(valores[metrica])
            fila[metrica + "_media"] = media
            fila[metrica + "_std"] = std
            fila[metrica + "_por_ganancia_media"] = media / divisor
            fila[metrica + "_por_ganancia_std"] = std / divisor
        filas.append(fila)
    return filas, descartadas, omitidos


def _ajustar(filas, selector, eje):
    puntos = sorted((float(f[eje]), float(f["busy_media"]),
                     float(f["transfer_media"])) for f in filas if selector(f))
    if len({p[0] for p in puntos}) < 2:
        return {"estado": "datos insuficientes", "puntos": puntos}
    x = np.asarray([p[0] for p in puntos])
    escala = {}
    for indice, metrica in ((1, "busy"), (2, "transfer")):
        y = np.asarray([p[indice] for p in puntos])
        a, b = np.polyfit(x, y, 1)
        pred = a * x + b
        s = float(np.max(np.abs(pred)))
        escala[metrica] = {
            "a": float(a),
            "b": float(b),
            "fraccion_g1": float(b / (a + b)) if a + b else float("nan"),
            "fraccion_g8": float(b / (8.0 * a + b)) if 8.0 * a + b else float("nan"),
            "b_aprox_cero": bool(abs(b) <= 0.10 * s),
            "a_aprox_cero": bool(abs(a) * (x.max() - x.min()) <= 0.10 * s),
        }
    return {"estado": "ok", "puntos": puntos, "metricas": escala}


def _interpretacion(nombre, ajuste):
    if ajuste["estado"] != "ok":
        return "%s: datos insuficientes para interpretar (se requieren al menos dos ganancias)." % nombre
    partes = []
    for metrica in ("busy", "transfer"):
        dato = ajuste["metricas"][metrica]
        if dato["b_aprox_cero"] and not dato["a_aprox_cero"]:
            texto = "entra en la entrada (referido a entrada aproximadamente constante)"
        elif dato["a_aprox_cero"] and not dato["b_aprox_cero"]:
            texto = "entra en la referencia/salida del PGA"
        elif dato["a_aprox_cero"] and dato["b_aprox_cero"]:
            texto = "señal aproximadamente nula; interpretación no concluyente"
        else:
            texto = "mezcla de términos de entrada y referencia/salida"
        partes.append("%s: %s" % (metrica, texto))
    return "%s: %s; %s." % (nombre, partes[0], partes[1])


def _guardar_csv(filas):
    campos = [
        "tap", "pga_codigo", "pga_ganancia", "pgaout_codigo",
        "pgaout_ganancia", "ganancia_normalizacion", "n", "n_base",
    ]
    for metrica in METRICAS:
        campos.extend((metrica + "_media", metrica + "_std",
                       metrica + "_por_ganancia_media",
                       metrica + "_por_ganancia_std"))
    with (SALIDA / "ganancia.csv").open("w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(filas)


def _fmt(valor):
    return "%.6g" % valor


def _texto_ajuste(titulo, ajuste):
    lineas = ["### " + titulo, ""]
    if ajuste["estado"] != "ok":
        lineas.append("Datos insuficientes: se requieren al menos dos ganancias distintas.")
        return lineas
    lineas.extend((
        "| métrica | a [cuentas/ganancia] | b [cuentas] | b/(aG+b), G=1 | b/(aG+b), G=8 |",
        "|---|---:|---:|---:|---:|",
    ))
    for metrica in ("busy", "transfer"):
        dato = ajuste["metricas"][metrica]
        lineas.append("| %s | %s | %s | %s | %s |" % (
            metrica, _fmt(dato["a"]), _fmt(dato["b"]),
            _fmt(dato["fraccion_g1"]), _fmt(dato["fraccion_g8"])))
    return lineas


def _guardar_markdown(filas, ajuste_tap0, ajuste_tap4, descartadas, omitidos):
    lineas = [
        "# Ganancia del ruido SD", "",
        "Las métricas están en cuentas ADC. Cada valor se informa como media ± desvío muestral entre capturas P4 válidas; a cada P4 se le restó el promedio BASE del grupo y luego la media pre-marca (índices 0–19). La figura usa `|transfer|` porque el eje vertical es logarítmico; la tabla y los ajustes conservan su signo.", "",
        "| tap | PGA (cód./gan.) | PGAout (cód./gan.) | n P4 | n BASE | transfer | busy | p2p | transfer/gan. | busy/gan. | p2p/gan. |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for fila in filas:
        valores = []
        for metrica in METRICAS:
            valores.append("%s ± %s" % (_fmt(fila[metrica + "_media"]),
                                         _fmt(fila[metrica + "_std"])))
        norm = []
        for metrica in METRICAS:
            norm.append("%s ± %s" % (
                _fmt(fila[metrica + "_por_ganancia_media"]),
                _fmt(fila[metrica + "_por_ganancia_std"])))
        lineas.append("| {tap} | {pga_codigo}/x{pga_ganancia} | {pgaout_codigo}/x{pgaout_ganancia} | {n} | {n_base} | {tr} | {bu} | {p2p} | {trn} | {bun} | {p2pn} |".format(
            tr=valores[0], bu=valores[1], p2p=valores[2],
            trn=norm[0], bun=norm[1], p2pn=norm[2], **fila))

    lineas.extend(("", "## Ajustes lineales", "",
                   "Modelo: `y = a·G + b`. Criterio explícito (10%): con `S=max|a·G+b|` en los puntos observados, `b≈0` si `|b|≤0,1·S`; `a≈0` si `|a|·(Gmax−Gmin)≤0,1·S`.", ""))
    lineas.extend(_texto_ajuste("Tap 0 vs PGA", ajuste_tap0))
    lineas.extend(("", "**Interpretación (una línea):** " + _interpretacion("Tap 0 vs PGA", ajuste_tap0), ""))
    lineas.extend(_texto_ajuste("Tap 4 vs PGAout, PGA fijo x8", ajuste_tap4))
    lineas.extend(("", "**Interpretación (una línea):** " + _interpretacion("Tap 4 vs PGAout con PGA x8", ajuste_tap4), ""))
    lineas.append("Capturas descartadas por `_medir`: %d. Grupos omitidos por faltar BASE o P4 válidos: %s." % (
        descartadas, ", ".join(map(str, omitidos)) if omitidos else "ninguno"))
    lineas.extend(("", "---", "IA principal: Codex (modelo no reportado) · Delegados: ninguno · Fallbacks: ninguno", ""))
    (SALIDA / "ganancia.md").write_text("\n".join(lineas), encoding="utf-8")


def _guardar_figura(filas):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    configuraciones = (
        ("Tap 0", lambda f: f["tap"] == 0, "pga_ganancia", "Ganancia PGA"),
        ("Tap 4, PGA x8", lambda f: f["tap"] == 4 and f["pga_ganancia"] == 8,
         "pgaout_ganancia", "Ganancia PGAout"),
    )
    fig, ejes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    for eje_plot, (titulo, selector, eje_x, etiqueta_x) in zip(ejes, configuraciones):
        seleccion = sorted((f for f in filas if selector(f)), key=lambda f: f[eje_x])
        for metrica, etiqueta, color in (("busy", "busy", "tab:red"),
                                         ("transfer", "|transfer|", "tab:blue")):
            x = np.asarray([f[eje_x] for f in seleccion], dtype=float)
            y = np.abs(np.asarray([f[metrica + "_media"] for f in seleccion],
                                  dtype=float))
            error = np.asarray([f[metrica + "_std"] for f in seleccion], dtype=float)
            positivos = (x > 0) & (y > 0)
            if positivos.any():
                eje_plot.errorbar(x[positivos], y[positivos], yerr=error[positivos],
                                   marker="o", capsize=3, color=color, label=etiqueta)
        positivos_y = [f[m + "_media"] for f in seleccion for m in ("busy", "transfer")
                       if f[m + "_media"] > 0]
        positivos_x = [f[eje_x] for f in seleccion if f[eje_x] > 0]
        if positivos_x and positivos_y:
            xmin, xmax = min(positivos_x), max(positivos_x)
            if xmin == xmax:
                xmin, xmax = xmin / 1.6, xmax * 1.6
            xref = np.geomspace(xmin, xmax, 100)
            centro_x = float(np.sqrt(xmin * xmax))
            centro_y = float(np.exp(np.mean(np.log(positivos_y))))
            eje_plot.plot(xref, centro_y * xref / centro_x, "--", color="0.4",
                           label="pendiente 1")
        eje_plot.set_xscale("log")
        eje_plot.set_yscale("log")
        eje_plot.set(title=titulo, xlabel=etiqueta_x, ylabel="amplitud [cuentas ADC]")
        eje_plot.grid(True, which="both", alpha=0.25)
        eje_plot.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(SALIDA / "ganancia.png", dpi=160)
    plt.close(fig)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    filas, descartadas, omitidos = _medir_grupos()
    if not filas:
        print("No hay grupos con capturas BASE y P4 válidas.", file=sys.stderr)
        return 1
    ajuste_tap0 = _ajustar(filas, lambda f: f["tap"] == 0, "pga_ganancia")
    ajuste_tap4 = _ajustar(
        filas, lambda f: f["tap"] == 4 and f["pga_ganancia"] == 8,
        "pgaout_ganancia")
    _guardar_csv(filas)
    _guardar_markdown(filas, ajuste_tap0, ajuste_tap4, descartadas, omitidos)
    _guardar_figura(filas)
    print("Generados %d grupos en %s" % (len(filas), SALIDA))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
