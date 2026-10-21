"""Figura del silencio de radio (radiosil): transitorio de arranque y ruido en banda.

Uso: python lab/figura_silencio_rf.py [--raiz lab/ruido_rf_20261020]

Junta las capturas de banco de W1c (OFF), W11, W12c, W12d y W12e por
condicion (BASE, OFF, SIL, SIL500, SIL1000). Panel izquierdo: std por
ventana de 50 ms en el primer segundo (mediana entre capturas, como
transitorio_arranque.py). Panel derecho: RMS en 5-50 Hz por condicion (media
y desvio). Las capturas que tocan un riel quedan fuera del panel derecho.
Escribe RAIZ/figuras/rf_silencio.png y rf_silencio.md.
"""
import argparse
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import welch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import ruido_sd, espectro_condiciones as ec  # noqa: E402
from lab.transitorio_arranque import FS, _capturas  # noqa: E402

DIRS = ['W1c_reposo', 'W11_silencio', 'W12c_silencio_1000', 'W12d_silencio_500', 'W12e_silencio_500']
ORDEN = ['BASE', 'OFF', 'SIL', 'SIL500', 'SIL1000']
ETIQUETA = {'BASE': 'radio encendida', 'OFF': 'radio apagada a mano', 'SIL': 'radiosil inmediato',
            'SIL500': 'radiosil 500 ms', 'SIL1000': 'radiosil 1000 ms'}


def rms_banda(dirs):
    import glob
    por = {}
    for d in dirs:
        for ruta in sorted(glob.glob(os.path.join(d, '*.txt'))):
            meta, _, digi, _, _ = ruido_sd.ar.cargar(ruta)
            if ruido_sd.no_utilizable(np.asarray(digi)):
                continue
            x = ec.limpiar(digi) * ruido_sd.ar.UV_POR_CUENTA
            x = x - x.mean()
            f, p = welch(x, fs=FS, nperseg=min(8192, x.size))
            m = (f >= 5) & (f <= 50)
            por.setdefault(meta['cond'], []).append(np.sqrt(np.sum(p[m]) * (f[1] - f[0])))
    return por


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--raiz', default='lab/ruido_rf_20261020')
    a = ap.parse_args(argv)
    dirs = [os.path.join(a.raiz, d) for d in DIRS if os.path.isdir(os.path.join(a.raiz, d))]
    por_cond, k = _capturas(dirs, 50.0, 1000.0)
    banda = rms_banda(dirs)
    conds = [c for c in ORDEN if c in por_cond]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    t = (np.arange(k) + 0.5) * 50
    lin = ['# Silencio de radio: transitorio y ruido en banda', '',
           'Directorios: ' + ', '.join(os.path.basename(d) for d in dirs), '',
           '| condicion | capturas | al riel | std 0-50 ms [mV] | std 100-150 ms [mV] | RMS 5-50 Hz [uV] |',
           '|---|---|---|---|---|---|']
    for c in conds:
        caps = por_cond[c]
        med = np.nanmedian(np.asarray([x['ventanas'] for x in caps], dtype=float), axis=0)
        ax1.semilogy(t, med, marker='o', ms=3, label='%s (n=%d)' % (ETIQUETA[c], len(caps)))
        b = np.asarray(banda.get(c, [np.nan]))
        lin.append('| %s | %d | %d | %.1f | %.1f | %.0f ± %.0f |' % (
            ETIQUETA[c], len(caps), sum(x['rechazada'] for x in caps), med[0], med[2],
            np.nanmean(b), np.nanstd(b)))
    ax1.set_xlabel('ms desde el inicio de la captura')
    ax1.set_ylabel('std por ventana de 50 ms [mV] (mediana)')
    ax1.set_title('Transitorio de arranque')
    ax1.grid(alpha=0.3, which='both')
    ax1.legend(fontsize=8)
    medias = [np.nanmean(banda.get(c, [np.nan])) for c in conds]
    desv = [np.nanstd(banda.get(c, [np.nan])) for c in conds]
    ax2.bar(range(len(conds)), medias, yerr=desv, capsize=4,
            color=['tab:red' if c == 'BASE' else 'tab:gray' if c == 'OFF' else 'tab:blue' for c in conds])
    ax2.set_xticks(range(len(conds)))
    ax2.set_xticklabels([ETIQUETA[c] for c in conds], rotation=20, ha='right', fontsize=8)
    ax2.set_ylabel('RMS 5-50 Hz en LPo [µV]')
    ax2.set_title('Ruido en la banda útil (capturas válidas)')
    ax2.grid(alpha=0.3, axis='y')
    fig.suptitle('Silencio de radio durante el muestreo (LPo, PGA x8, PGAout x16)')
    fig.tight_layout()
    sal = os.path.join(a.raiz, 'figuras')
    os.makedirs(sal, exist_ok=True)
    fig.savefig(os.path.join(sal, 'rf_silencio.png'), dpi=150)
    open(os.path.join(sal, 'rf_silencio.md'), 'w', encoding='utf-8').write('\n'.join(lin) + '\n')
    print('\n'.join(lin))
    return 0


if __name__ == '__main__':
    sys.exit(main())
