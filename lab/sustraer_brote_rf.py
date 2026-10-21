"""Evalua la sustraccion sincronica del brote de radio.

Uso: python lab/sustraer_brote_rf.py DIR [DIR...] [--ref PING]
       [--largo-ms 40] [--salida DIR]
"""
import argparse
import glob
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import welch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import espectro_condiciones, ruido_sd  # noqa: E402


FS = 2604.0
NPERSEG = 2048
METODOS = ('original', 'global LOO', 'propia', 'propia ajustada')


def _segmentos(x, posiciones, antes, despues):
    """Devuelve segmentos completos y sus posiciones, en orden temporal."""
    pos = np.asarray(posiciones, dtype=np.int64)
    pos = np.unique(pos[(pos - antes >= 0) & (pos + despues < x.size)])
    if pos.size == 0:
        return np.empty((0, antes + despues + 1)), pos
    return np.stack([x[i - antes:i + despues + 1] for i in pos]), pos


def _restar(x, posiciones, plantilla, antes, ajustar=False):
    """Resta secuencialmente; los solapamientos se modifican varias veces."""
    y = x.copy()
    if plantilla is None:
        return y
    largo = plantilla.size
    energia = float(np.dot(plantilla, plantilla))
    for pos in posiciones:
        inicio = int(pos) - antes
        tramo = y[inicio:inicio + largo]
        escala = 1.0
        if ajustar and energia > 0.0:
            escala = float(np.dot(tramo, plantilla) / energia)
        tramo -= escala * plantilla
    return y


def cargar(dirs, referencia, antes, despues):
    por_condicion = {}
    descartadas = 0
    sin_marcas = 0
    for directorio in dirs:
        for ruta in sorted(glob.glob(os.path.join(directorio, '*.txt'))):
            meta, _, digi, _, _ = ruido_sd.ar.cargar(ruta)
            if digi.size < NPERSEG:
                continue
            x = espectro_condiciones.limpiar(digi)
            if ruido_sd.no_utilizable(x):
                descartadas += 1
                continue
            condicion = meta.get('cond', '?')
            marcas = meta.get('marcas_muestra') or []
            if not marcas and condicion != referencia:
                sin_marcas += 1
                continue
            x = (x - x.mean()) * ruido_sd.ar.UV_POR_CUENTA
            segmentos, posiciones = _segmentos(x, marcas, antes, despues)
            if marcas and posiciones.size == 0:
                sin_marcas += 1
                continue
            por_condicion.setdefault(condicion, []).append({
                'ruta': ruta, 'x': x, 'segmentos': segmentos,
                'posiciones': posiciones,
            })
    return por_condicion, descartadas, sin_marcas


def _preparar_plantillas(capturas):
    segmentos_por_captura = [c['segmentos'] for c in capturas]
    for indice, captura in enumerate(capturas):
        propios = captura['segmentos']
        plantilla_propia = propios.mean(axis=0) if propios.size else None
        ajenos = [s for j, s in enumerate(segmentos_por_captura)
                  if j != indice and s.size]
        plantilla_global = (np.concatenate(ajenos).mean(axis=0)
                            if ajenos else None)
        captura['_plantilla_global'] = plantilla_global
        captura['_plantilla_propia'] = plantilla_propia


def _potencia_5_50(x):
    f, p = welch(x, fs=FS, nperseg=NPERSEG)
    mascara = (f >= 5.0) & (f <= 50.0)
    return float(np.trapezoid(p[mascara], f[mascara]))


def analizar(por_condicion, antes):
    resumen = {}
    for condicion, capturas in por_condicion.items():
        _preparar_plantillas(capturas)
        series = {metodo: [] for metodo in METODOS}
        for captura in capturas:
            x = captura['x']
            pos = captura['posiciones']
            propia = captura['_plantilla_propia']
            series['original'].append(x)
            series['global LOO'].append(
                _restar(x, pos, captura['_plantilla_global'], antes))
            series['propia'].append(_restar(x, pos, propia, antes))
            series['propia ajustada'].append(
                _restar(x, pos, propia, antes, ajustar=True))
        resumen[condicion] = {
            'n': len(capturas),
            'rms': {m: float(np.mean([np.std(x) for x in xs]))
                    for m, xs in series.items()},
            'psd': {m: float(np.mean([_potencia_5_50(x) for x in xs]))
                    for m, xs in series.items()},
        }
    return resumen


def _fmt(valor, decimales=1):
    return ('%.*f' % (decimales, valor)) if np.isfinite(valor) else '-'


def escribir_md(ruta, resumen, referencia, descartadas, sin_marcas, largo_ms):
    ref = resumen.get(referencia)
    lineas = [
        '# Sustraccion del brote RF', '',
        ('Ventana: -5 ms a +%g ms. RMS en uV sin media; potencia Welch '
         '(fs=2604 Hz, nperseg=2048) integrada entre 5 y 50 Hz en uV^2.'
         % largo_ms),
        ('Capturas descartadas por riel: %d. Capturas sin marcas omitidas: %d.'
         % (descartadas, sin_marcas)),
    ]
    if ref:
        lineas.append('Las capturas %s sin marcas se usan solo como referencia; '
                      'a/b/c son identicos al original.' % referencia)
    lineas += [
        '',
        '| condicion | n | RMS orig | RMS a global LOO | RMS b propia | '
        'RMS c ajustada | orig/ref | a/ref | b/ref | c/ref | PSD orig | '
        'PSD a | PSD b | PSD c |',
        '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|',
    ]
    orden = sorted(resumen, key=lambda c: (c != referencia, c))
    for condicion in orden:
        r = resumen[condicion]
        ratios = []
        for metodo in METODOS:
            denominador = ref['rms'][metodo] if ref else float('nan')
            ratios.append(r['rms'][metodo] / denominador
                          if denominador > 0 else float('nan'))
        lineas.append('| %s | %d | %s | %s | %s | %s | %s | %s | %s | %s | '
                      '%s | %s | %s | %s |' % (
                          condicion, r['n'],
                          *[_fmt(r['rms'][m]) for m in METODOS],
                          *[_fmt(v, 2) for v in ratios],
                          *[_fmt(r['psd'][m], 1) for m in METODOS]))
    lineas += ['', '---', 'Generado por `lab/sustraer_brote_rf.py`.', '']
    texto = '\n'.join(lineas)
    with open(ruta, 'w', encoding='utf-8') as fh:
        fh.write(texto)
    return texto


def escribir_png(ruta, resumen, referencia):
    condiciones = sorted(resumen, key=lambda c: (c != referencia, c))
    x = np.arange(len(condiciones), dtype=float)
    ancho = 0.19
    fig, ax = plt.subplots(figsize=(max(8, 1.5 * len(condiciones)), 5))
    for indice, metodo in enumerate(METODOS):
        valores = [resumen[c]['rms'][metodo] for c in condiciones]
        ax.bar(x + (indice - 1.5) * ancho, valores, ancho, label=metodo)
    if referencia in resumen:
        ax.axhline(resumen[referencia]['rms']['original'], color='black',
                   ls='--', lw=1.2, label='ref %s' % referencia)
    ax.set_xticks(x, condiciones, rotation=20, ha='right')
    ax.set_ylabel('RMS (uV, sin media)')
    ax.set_title('Sustraccion sincronica del brote RF')
    ax.grid(axis='y', alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='+')
    ap.add_argument('--ref', default='PING')
    ap.add_argument('--largo-ms', type=float, default=40.0)
    ap.add_argument('--salida')
    args = ap.parse_args(argv)
    if args.largo_ms <= 0:
        ap.error('--largo-ms debe ser positivo')
    salida = args.salida or os.path.join(args.dirs[0], 'sustraccion')
    os.makedirs(salida, exist_ok=True)
    antes = int(round(0.005 * FS))
    despues = int(round(args.largo_ms / 1000.0 * FS))
    por, descartadas, sin_marcas = cargar(
        args.dirs, args.ref, antes, despues)
    if not por:
        print('sin capturas utilizables')
        return 1
    resumen = analizar(por, antes)
    texto = escribir_md(os.path.join(salida, 'sustraccion.md'), resumen,
                        args.ref, descartadas, sin_marcas, args.largo_ms)
    escribir_png(os.path.join(salida, 'sustraccion.png'), resumen, args.ref)
    print(texto, end='')
    return 0


if __name__ == '__main__':
    sys.exit(main())
