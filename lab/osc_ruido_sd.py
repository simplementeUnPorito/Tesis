"""E9: analiza un CSV del TDS 2004B (4 canales, CH1 = CS de la SD).

Uso: python lab/osc_ruido_sd.py ARCHIVO.csv "nombre CH2" "nombre CH3" "nombre CH4"
Imprime, por canal, el nivel medio (respecto del tramo antes del disparo) en
los tramos con CS bajo y CS alto, y guarda una figura junto al CSV."""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def cargar(ruta):
    filas = [l.rstrip('\n').split(',') for l in open(ruta, encoding='latin-1')]
    canales = []
    for c in range(4):
        t = np.array([float(f[6 * c + 3]) for f in filas])
        v = np.array([float(f[6 * c + 4]) for f in filas])
        canales.append((t, v))
    return canales


def main():
    ruta = sys.argv[1]
    nombres = ['CS'] + (sys.argv[2:5] + ['CH2', 'CH3', 'CH4'])[:3]
    ch = cargar(ruta)
    t = ch[0][0] * 1e3                      # ms
    cs = ch[0][1]
    bajo = cs < 0.5 * (cs.max() + cs.min())
    pre = t < 0
    # Tramo de CS bajo mas largo despues del disparo: la escritura del bloque.
    print('CS: %.2f..%.2f V, bajo %.1f %% del registro, primer bajo en %.2f ms' %
          (cs.min(), cs.max(), 100 * bajo.mean(),
           t[np.argmax(bajo)] if bajo.any() else float('nan')))
    cambios = np.flatnonzero(np.diff(bajo.astype(int)))
    print('flancos de CS en ms:', ' '.join('%.2f' % t[i] for i in cambios[:20]))
    fig, ejes = plt.subplots(4, 1, sharex=True, figsize=(9, 8))
    for k in range(4):
        v = ch[k][1]
        if k:
            v = v - v[pre].mean()
            print('%-22s ruido pre %.2f mVrms | media CS bajo %+.3f mV | CS alto(post) %+.3f mV | p2p %.2f mV' %
                  (nombres[k], 1e3 * v[pre].std(), 1e3 * v[bajo].mean() if bajo.any() else float('nan'),
                   1e3 * v[~bajo & ~pre].mean(), 1e3 * np.ptp(v)))
        ejes[k].plot(t, v * (1 if k == 0 else 1e3), lw=0.6)
        ejes[k].set_ylabel(nombres[k] + (' [V]' if k == 0 else ' [mV]'))
        ejes[k].grid(alpha=0.3)
        if k:
            # promedio movil de 0,5 ms para ver escalones bajo el ruido
            n = 25
            ejes[k].plot(t, 1e3 * np.convolve(v, np.ones(n) / n, 'same'), 'r', lw=1)
    ejes[-1].set_xlabel('tiempo desde el flanco de CS [ms]')
    fig.tight_layout()
    fig.savefig(ruta.rsplit('.', 1)[0] + '.png', dpi=120)


if __name__ == '__main__':
    main()
