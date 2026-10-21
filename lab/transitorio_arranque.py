"""Cuantifica el transitorio de ruido al inicio de capturas."""

import argparse
import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import ruido_sd, espectro_condiciones as ec


FS = 2604.0


def _fmt(valor):
    return '-' if not np.isfinite(valor) else '%.6g' % valor


def _capturas(directorios, ventana_ms, hasta_ms):
    muestras_hasta = int(round(hasta_ms * FS / 1000.0))
    k = int(np.floor(hasta_ms / ventana_ms + 1e-12))
    limites = [(int(round(i * ventana_ms * FS / 1000.0)),
                int(round((i + 1) * ventana_ms * FS / 1000.0)))
               for i in range(k)]
    por_condicion = {}

    for directorio in directorios:
        for ruta in sorted(glob.glob(os.path.join(directorio, '*.txt'))):
            meta, _, digi, _, _ = ruido_sd.ar.cargar(ruta)
            x_en_cuentas = np.asarray(digi)
            x = ec.limpiar(digi) * ruido_sd.ar.UV_POR_CUENTA / 1000.0
            ventanas = []
            for inicio, fin_nominal in limites:
                fin = min(fin_nominal, muestras_hasta, len(x))
                ventanas.append(np.std(x[inicio:fin]) if fin > inicio else np.nan)
            regimen = np.std(x[muestras_hasta:]) if len(x) > muestras_hasta else np.nan
            por_condicion.setdefault(meta['cond'], []).append({
                'ventanas': ventanas,
                'regimen': regimen,
                'rechazada': bool(ruido_sd.no_utilizable(x_en_cuentas)),
            })
    return por_condicion, k


def _resumir(por_condicion, k, ventana_ms):
    filas = []
    for condicion, capturas in sorted(por_condicion.items()):
        ventanas = np.asarray([c['ventanas'] for c in capturas], dtype=float)
        medianas = np.nanmedian(ventanas, axis=0)
        regimen = float(np.nanmedian([c['regimen'] for c in capturas]))
        candidatos = np.flatnonzero(medianas <= 1.2 * regimen)
        asentamiento = ((int(candidatos[0]) + 1) * ventana_ms
                        if np.isfinite(regimen) and candidatos.size else np.nan)
        filas.append({
            'condicion': condicion,
            'n': len(capturas),
            'rechazadas': sum(c['rechazada'] for c in capturas),
            'ventanas': medianas[:k],
            'regimen': regimen,
            'asentamiento': asentamiento,
        })
    return filas


def _guardar_md(ruta, filas, k):
    columnas = (['condicion', 'n', 'rechazadas'] +
                ['std ventana %d (mV)' % (i + 1) for i in range(k)] +
                ['regimen (mV)', 'asentamiento (ms)'])
    lineas = ['| ' + ' | '.join(columnas) + ' |',
              '|' + '|'.join(['---'] * len(columnas)) + '|']
    for fila in filas:
        valores = ([fila['condicion'], str(fila['n']), str(fila['rechazadas'])] +
                   [_fmt(x) for x in fila['ventanas']] +
                   [_fmt(fila['regimen']), _fmt(fila['asentamiento'])])
        lineas.append('| ' + ' | '.join(valores) + ' |')
    with open(ruta, 'w', encoding='utf-8') as archivo:
        archivo.write('\n'.join(lineas) + '\n')


def _guardar_png(ruta, filas, ventana_ms):
    fig, ax = plt.subplots(figsize=(9, 5))
    for fila in filas:
        tiempos = np.arange(1, len(fila['ventanas']) + 1) * ventana_ms
        ax.plot(tiempos, fila['ventanas'], marker='o', ms=3,
                label='%s (n=%d)' % (fila['condicion'], fila['n']))
    ax.set_yscale('log')
    ax.set_xlabel('Tiempo desde el inicio (ms)')
    ax.set_ylabel('Desvio estandar (mV)')
    ax.set_title('Transitorio de arranque')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=160)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directorios', nargs='+', metavar='DIR')
    parser.add_argument('--ventana-ms', type=float, default=50.0)
    parser.add_argument('--hasta-ms', type=float, default=1000.0)
    parser.add_argument('--salida')
    args = parser.parse_args()
    if (args.ventana_ms <= 0 or args.hasta_ms <= 0 or
            args.ventana_ms > args.hasta_ms):
        parser.error('--ventana-ms debe ser positiva y no superar --hasta-ms')

    salida = args.salida or os.path.join(args.directorios[0], 'transitorio')
    os.makedirs(salida, exist_ok=True)
    por_condicion, k = _capturas(args.directorios, args.ventana_ms, args.hasta_ms)
    if not por_condicion:
        parser.error('no se encontraron capturas .txt')
    filas = _resumir(por_condicion, k, args.ventana_ms)
    _guardar_md(os.path.join(salida, 'transitorio.md'), filas, k)
    _guardar_png(os.path.join(salida, 'transitorio.png'), filas, args.ventana_ms)


if __name__ == '__main__':
    main()
