"""Ruido de las capturas de campo de prueba_radiosil_maestro.py, con y sin radiosil.

Uso: python lab/analizar_e2e_radiosil.py DIR [--fs 2604] [--nodo 2]

Lee los maestro_intento_NN_{on,off}.bin (bytes crudos del maestro), toma las
muestras PTYPE_DATA del nodo en el orden recibido y calcula por intento el
RMS total, el RMS en 5-50 Hz y en la baliza (8,5-11 Hz: a 1024 puntos la línea más cercana) y la std de los
primeros 50 ms y de 50-150 ms. Las unidades son las del protocolo (value24,
cuentas del ADC); los cocientes on/off no dependen de ellas. Escribe
DIR/analisis.md y DIR/analisis.png.
"""
import argparse
import glob
import os
import re
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import welch

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'src', 'interfaces', 'python'))
# protocol.py importa "config" sin paquete
sys.path.insert(0, os.path.join(RAIZ, 'src', 'interfaces', 'python', 'geophone_scope'))
from geophone_scope import config, protocol  # noqa: E402


def muestras(ruta, nodo):
    datos = open(ruta, 'rb').read()
    out = []
    i = 0
    while i + config.PKT_LEN <= len(datos):
        if datos[i] != config.PKT_HEADER:
            i += 1   # resincronizar
            continue
        p = protocol.decode_packet(datos[i:i + config.PKT_LEN])
        if p is not None and p.ptype == config.PTYPE_DATA and p.node_id == nodo:
            out.append(p.value24)
        i += config.PKT_LEN
    return np.asarray(out, dtype=float)


def banda(f, p, lo, hi):
    m = (f >= lo) & (f <= hi)
    return float(np.sqrt(np.sum(p[m]) * (f[1] - f[0]))) if m.any() else float('nan')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('dir')
    ap.add_argument('--fs', type=float, default=2604.0)
    ap.add_argument('--nodo', type=int, default=2)
    a = ap.parse_args(argv)
    fs = a.fs
    filas, psd = [], {}
    for ruta in sorted(glob.glob(os.path.join(a.dir, 'maestro_intento_*_*.bin'))):
        m = re.search(r'intento_(\d+)_(on|off)\.bin$', ruta)
        if not m:
            continue
        x = muestras(ruta, a.nodo)
        if x.size < 512:
            filas.append(dict(n=int(m.group(1)), modo=m.group(2), muestras=x.size))
            continue
        x = x - x.mean()
        f, p = welch(x, fs=fs, nperseg=min(1024, x.size))
        psd.setdefault(m.group(2), []).append((f, p))
        k50, k150 = int(0.05 * fs), int(0.15 * fs)
        filas.append(dict(n=int(m.group(1)), modo=m.group(2), muestras=x.size,
                          rms=x.std(), b550=banda(f, p, 5, 50), bal=banda(f, p, 8.5, 11.0),
                          s0=x[:k50].std(), s1=x[k50:k150].std()))
    lin = ['# Ruido en capturas de campo (maestro), con y sin radiosil', '',
           'Unidades: value24 del protocolo (cuentas del ADC). Nodo %d, fs %.0f Hz.' % (a.nodo, fs), '',
           '| intento | radiosil | muestras | RMS total | RMS 5-50 Hz | RMS 9,77 Hz | std 0-50 ms | std 50-150 ms |',
           '|---|---|---|---|---|---|---|---|']
    for r in filas:
        if 'rms' in r:
            lin.append('| %d | %s | %d | %.1f | %.1f | %.1f | %.1f | %.1f |' % (
                r['n'], r['modo'], r['muestras'], r['rms'], r['b550'], r['bal'], r['s0'], r['s1']))
        else:
            lin.append('| %d | %s | %d | | | | | |' % (r['n'], r['modo'], r['muestras']))
    lin += ['', '| radiosil | n | RMS total | RMS 5-50 Hz | RMS 9,77 Hz | std 0-50 ms | std 50-150 ms |',
            '|---|---|---|---|---|---|---|']
    res = {}
    for modo in ('off', 'on'):
        rs = [r for r in filas if r['modo'] == modo and 'rms' in r]
        if not rs:
            continue
        res[modo] = {k: (np.mean([r[k] for r in rs]), np.std([r[k] for r in rs])) for k in ('rms', 'b550', 'bal', 's0', 's1')}
        lin.append('| %s | %d | %s |' % (modo, len(rs), ' | '.join('%.1f ± %.1f' % res[modo][k] for k in ('rms', 'b550', 'bal', 's0', 's1'))))
    if len(res) == 2:
        lin.append('| on/off | | %s |' % ' | '.join('×%.2f' % (res['on'][k][0] / res['off'][k][0]) for k in ('rms', 'b550', 'bal', 's0', 's1')))
    open(os.path.join(a.dir, 'analisis.md'), 'w', encoding='utf-8').write('\n'.join(lin) + '\n')
    fig, ax = plt.subplots(figsize=(9, 5))
    for modo, lst in psd.items():
        f = lst[0][0]
        ax.loglog(f[1:], np.sqrt(np.mean([p for _, p in lst], axis=0))[1:], label='radiosil %s (n=%d)' % (modo, len(lst)))
    ax.axvspan(5, 50, alpha=0.1)
    ax.set_xlabel('Hz')
    ax.set_ylabel('cuentas/√Hz')
    ax.grid(alpha=0.3, which='both')
    ax.legend()
    ax.set_title('Capturas de campo recibidas por el maestro')
    fig.tight_layout()
    fig.savefig(os.path.join(a.dir, 'analisis.png'), dpi=120)
    print('\n'.join(lin))
    return 0


if __name__ == '__main__':
    sys.exit(main())
