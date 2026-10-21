"""Espectro y RMS del ruido por condicion (para efectos sin evento sincronizable).

Uso: python lab/espectro_condiciones.py DIR [DIR...] [--salida DIR] [--ref BASE]
       [--banda LO HI]

Por captura: limpia los artefactos de una muestra (como ruido_sd._medir),
descarta las que tocan un riel (ruido_sd.no_utilizable), quita la media y
calcula RMS y PSD de Welch. Por condicion: RMS medio +- desvio, cociente
contra la referencia, potencia en bandas de interes (baliza WiFi de 102,4 ms
= 9,77 Hz; periodo de 57,6 ms = 17,36 Hz y armonicos) y las lineas que mas
crecen respecto de la referencia. Escribe espectro.md, espectro.csv y psd.png.
"""
import argparse
import csv
import glob
import json
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import welch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import ruido_sd  # noqa: E402

FS = 2604.0
BANDAS = {'baliza 9,77 Hz': (9.0, 10.6), 'baliza x2': (19.0, 20.1),
          '57,6 ms (17,36 Hz)': (17.0, 17.7), '57,6 ms x2': (34.3, 35.1),
          '57,6 ms x3': (51.6, 52.6), 'red 50 Hz': (49.5, 50.5)}


def limpiar(digi):
    d = np.asarray(digi, dtype=float).copy()
    c = d[1:-1]
    ais = np.flatnonzero((np.abs(c - d[:-2]) > ruido_sd.MARCA_UMBRAL) &
                         (np.abs(c - d[2:]) > ruido_sd.MARCA_UMBRAL)) + 1
    d[ais] = 0.5 * (d[ais - 1] + d[ais + 1])
    if d.size > 1 and abs(d[0] - d[1]) > ruido_sd.MARCA_UMBRAL:
        d[0] = d[1]
    return d


def cargar(dirs):
    por = {}
    descartadas = 0
    for d in dirs:
        for r in sorted(glob.glob(os.path.join(d, '*.txt'))):
            meta, _, digi, _, _ = ruido_sd.ar.cargar(r)
            if digi.size < 2048:
                continue
            x = limpiar(digi)
            if ruido_sd.no_utilizable(x):
                descartadas += 1
                continue
            x = (x - x.mean()) * ruido_sd.ar.UV_POR_CUENTA
            por.setdefault(meta.get('cond', '?'), []).append(x)
    return por, descartadas


def potencia_banda(f, p, lo, hi):
    m = (f >= lo) & (f <= hi)
    if not m.any():
        m[np.argmin(np.abs(f - 0.5 * (lo + hi)))] = True
    return float(np.sum(p[m]) * (f[1] - f[0]))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('dirs', nargs='+')
    ap.add_argument('--salida')
    ap.add_argument('--ref', default='BASE')
    ap.add_argument('--banda', nargs=2, type=float, metavar=('LO', 'HI'),
                    default=(5.0, 50.0))
    a = ap.parse_args(argv)
    if a.banda[0] >= a.banda[1]:
        ap.error('--banda requiere LO < HI')
    banda_lo, banda_hi = a.banda
    banda_col = 'RMS %g-%g Hz uV' % (banda_lo, banda_hi)
    baliza_col = 'RMS 9,77 Hz uV'
    sal = a.salida or os.path.join(a.dirs[0], 'espectro')
    os.makedirs(sal, exist_ok=True)
    por, desc = cargar(a.dirs)
    if not por:
        print('sin capturas utilizables')
        return 1
    ref = a.ref if a.ref in por else sorted(por)[0]
    res = {}
    for cond, xs in por.items():
        rms = np.array([x.std() for x in xs])
        psds = [welch(x, fs=FS, nperseg=min(8192, len(x))) for x in xs]
        f = psds[0][0]
        p = np.mean([q for _, q in psds], axis=0)
        rms_banda = np.sqrt([potencia_banda(fi, pi, banda_lo, banda_hi)
                             for fi, pi in psds])
        rms_baliza = np.sqrt([potencia_banda(fi, pi, 9.5, 10.1)
                              for fi, pi in psds])
        res[cond] = dict(n=len(xs), rms=rms, rms_banda=rms_banda,
                         rms_baliza=rms_baliza, f=f, p=p)
    fr, pr = res[ref]['f'], res[ref]['p']
    filas = []
    for cond, r in sorted(res.items(), key=lambda kv: (kv[0] != ref, kv[0])):
        bandas = {k: potencia_banda(r['f'], r['p'], lo, hi) for k, (lo, hi) in BANDAS.items()}
        bref = {k: potencia_banda(fr, pr, lo, hi) for k, (lo, hi) in BANDAS.items()}
        m = (r['f'] >= 1) & (r['f'] <= 1300)
        cociente = r['p'][m] / np.maximum(pr[m], 1e-12)
        top = np.argsort(cociente)[::-1][:6]
        lineas = ', '.join('%.1f Hz x%.1f' % (r['f'][m][i], cociente[i]) for i in top)
        rms_banda_sd = r['rms_banda'].std(ddof=1) if r['n'] > 1 else 0.0
        rms_baliza_sd = r['rms_baliza'].std(ddof=1) if r['n'] > 1 else 0.0
        filas.append(dict(cond=cond, n=r['n'], rms=r['rms'].mean(), rms_sd=r['rms'].std(ddof=1) if r['n'] > 1 else 0.0,
                          **{banda_col: '%.1f +- %.1f' % (r['rms_banda'].mean(), rms_banda_sd),
                             baliza_col: '%.1f +- %.1f' % (r['rms_baliza'].mean(), rms_baliza_sd)},
                          ratio=r['rms'].mean() / res[ref]['rms'].mean(),
                          **{('banda ' + k): bandas[k] / bref[k] for k in BANDAS}, lineas=lineas))
    with open(os.path.join(sal, 'espectro.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    lin = ['# Espectro por condicion', '',
           'Referencia: %s. Capturas descartadas por riel: %d. RMS en uV (sin media).' % (ref, desc), '',
           '| cond | n | RMS uV | %s | %s | vs %s | %s | lineas que mas crecen |' %
           (banda_col, baliza_col, ref, ' | '.join(BANDAS)),
           '|---|---|---|---|---|---|%s|---|' % '|'.join(['---'] * len(BANDAS))]
    for r in filas:
        lin.append('| %s | %d | %.0f +- %.0f | %s | %s | x%.2f | %s | %s |' % (
            r['cond'], r['n'], r['rms'], r['rms_sd'], r[banda_col], r[baliza_col], r['ratio'],
            ' | '.join('x%.2f' % r['banda ' + k] for k in BANDAS), r['lineas']))
    open(os.path.join(sal, 'espectro.md'), 'w', encoding='utf-8').write('\n'.join(lin) + '\n')
    fig, ax = plt.subplots(figsize=(10, 5))
    for cond, r in res.items():
        ax.loglog(r['f'][1:], np.sqrt(r['p'][1:]), lw=1.1, label='%s (n=%d)' % (cond, r['n']))
    ax.set_xlabel('Hz')
    ax.set_ylabel('uV/sqrt(Hz)')
    ax.grid(alpha=0.3, which='both')
    ax.legend()
    ax.set_title('PSD de LPo por condicion')
    fig.tight_layout()
    fig.savefig(os.path.join(sal, 'psd.png'), dpi=120)
    print('\n'.join(lin))
    return 0


if __name__ == '__main__':
    sys.exit(main())
