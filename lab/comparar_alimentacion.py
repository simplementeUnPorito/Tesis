"""Compara configuraciones de alimentacion/masa con experimentos cortos de radio.

Para cada raiz (una configuracion) y cada experimento, mide por condicion:
p2p del brote promedio sincronizado, RMS 5-50 Hz y el estado del lazo (IDAC y
LPo del metadato). Luego da el exceso de la condicion estresora sobre su
control (RF240 sobre PING, BASE sobre OFF) en cuadratura, que es lo que se
compara entre configuraciones.

No descarta capturas por riel (ruido_sd lo hace): informa el % de muestras en
el riel para que se juzgue a mano.

Uso:
  python lab/comparar_alimentacion.py RAIZ1 RAIZ2 ... [--exp W9_ganancia_pga2 W10_lpo W1c_reposo]
"""
import argparse
import glob
import json
import os
import sys

import numpy as np
from scipy.signal import welch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analisis_ruido as ar  # noqa: E402
import ruido_sd as rs  # noqa: E402

FS = 2604
PARES = {'RF240': 'PING', 'BASE': 'OFF', 'RF240B': 'PING', 'SIL500': 'BASE'}
_CAPTURA = {}


def _sin_descarte(digi):
    _CAPTURA['digi'] = digi.copy()
    return ''


rs.no_utilizable = _sin_descarte


def medir(ruta):
    r = rs._medir(ruta)
    with open(ruta, encoding='utf-8') as f:
        meta = json.loads(f.readline())['meta']
    x = _CAPTURA['digi'] * ar.UV_POR_CUENTA / 1000.0
    fr, p = welch(x - x.mean(), FS, nperseg=4096)
    banda = (fr >= 5) & (fr <= 50)
    lazo = meta.get('lazo', {})
    return {'cond': r['cond'], 'p2p': r['p2p_uV'] / 1000.0,
            'rms': float(np.sqrt(np.trapezoid(p[banda], fr[banda]))),
            'riel': float(np.mean(x < 735) * 100),
            'idac': tuple(lazo.get('idac', [])),
            'lpo': lazo.get('lpo_uv', 0) / 1000.0}


def resumen(directorio):
    por_cond = {}
    for ruta in sorted(glob.glob(os.path.join(directorio, '*.txt'))):
        m = medir(ruta)
        por_cond.setdefault(m['cond'], []).append(m)
    return por_cond


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('raices', nargs='+')
    ap.add_argument('--exp', nargs='+',
                    default=['W9_ganancia_pga2', 'W10_lpo', 'W1c_reposo'])
    args = ap.parse_args(argv)
    for exp in args.exp:
        print('\n## %s\n' % exp)
        print('| configuracion | cond | n | brote p2p mV | RMS 5-50 mV | riel %'
              ' | exceso RMS mV | IDAC (LPo mV) |')
        print('|---|---|---|---|---|---|---|---|')
        for raiz in args.raices:
            d = os.path.join(raiz, exp)
            if not os.path.isdir(d):
                continue
            pc = resumen(d)
            for cond, filas in sorted(pc.items()):
                p2p = np.array([f['p2p'] for f in filas])
                rms = np.array([f['rms'] for f in filas])
                exceso = ''
                ctrl = PARES.get(cond)
                if ctrl in pc:
                    rc = np.mean([f['rms'] for f in pc[ctrl]])
                    exceso = '%.3f' % np.sqrt(max(np.mean(rms) ** 2 - rc ** 2, 0.0))
                estados = sorted({'%s (%.0f)' % (list(f['idac']), f['lpo'])
                                  for f in filas})
                print('| %s | %s | %d | %.2f ± %.2f | %.3f ± %.3f | %.1f | %s | %s |' % (
                    os.path.basename(os.path.normpath(raiz)), cond, len(filas),
                    p2p.mean(), p2p.std(), rms.mean(), rms.std(),
                    np.mean([f['riel'] for f in filas]), exceso,
                    '; '.join(estados[:3])))


if __name__ == '__main__':
    main()
