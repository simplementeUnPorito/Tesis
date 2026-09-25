"""analisis_ruido.py - cuanto agregan la SD y la radio, y donde se acoplan.

Lee los volcados de `experimento_ruido.py` y produce:

  * RMS de banda ancha y RMS en 10-50 Hz, que es la banda util REAL de campo
    (verificada por cinco caminos distintos, no la banda de diseno);
  * el delta de cada condicion contra BASE, que es la respuesta a "cuanto
    agrega";
  * ese delta contra la ganancia, REFERIDO A LA ENTRADA, que es lo que dice
    DONDE se acopla el ruido: si el delta referido a la entrada no cambia con
    la ganancia, el ruido entra antes del PGA; si baja al subir la ganancia,
    entra despues;
  * la comparacion DENTRO de cada captura entre las muestras marcadas con
    escritura de SD y las que no. El firmware las marca solo
    (SAMPLE_FLAG_SD_WRITE), y comparar adentro de una misma captura elimina la
    deriva por completo: es mas fuerte que comparar dos capturas separadas;
  * lotes faltantes. Si la SD le roba DMA o CPU al PSoC el danio son MUESTRAS
    PERDIDAS, no ruido. Las dos cosas se ven como "peor senial" y son fallas
    distintas con arreglos distintos, asi que se informan por separado.

Uso:

    python lab/analisis_ruido.py lab/ruido_20261015
    python lab/analisis_ruido.py lab/ruido_20261015 --csv ruido.csv
"""
import argparse
import csv
import glob
import json
import os
import sys

import numpy as np

try:
    from scipy.signal import welch
except ImportError:                     # pragma: no cover
    welch = None

FS_NATIVA = 2604.0
MUESTRAS_POR_LOTE = 30
# Banda util real medida en campo (10-50 Hz), NO la banda objetivo del disenio.
BANDA = (10.0, 50.0)
# Cuentas del ADC a microvolts.  El dominio del banco son CUENTAS; este factor
# solo sirve para informar en unidades fisicas y se cancela en cualquier
# cociente entre condiciones, que es lo que de verdad se mide aca.
UV_POR_CUENTA = 1e6 / 52429.0
FLAG_SD_WRITE = 0x01
FLAG_SD_SYNC = 0x02
GANANCIAS = [1, 2, 4, 8, 16, 24, 32, 48, 50]


def cargar(ruta):
    """Devuelve (meta, seqs, digi, flags, gain).

    `digi` es la muestra de 24 bits CON SIGNO.  Ojo: `raw_lo/raw_hi` son solo
    los 16 bits BAJOS de ese mismo numero, asi que se envuelven y no sirven
    para nada cuantitativo."""
    with open(ruta, encoding='utf-8') as fh:
        cab = json.loads(fh.readline())
        seqs, crudo = [], []
        for linea in fh:
            partes = linea.split()
            if len(partes) < 2:
                continue
            seqs.append(int(partes[0]))
            crudo.append(bytes.fromhex(partes[1]))
    if not crudo:
        return cab.get('meta', {}), np.array([]), np.array([]), np.array([]), None
    b = np.frombuffer(b''.join(crudo), dtype=np.uint8)
    b = b.reshape(-1, 10)
    digi = (b[:, 5].astype(np.int32)
            | (b[:, 6].astype(np.int32) << 8)
            | (b[:, 7].astype(np.int32) << 16))
    digi = np.where(digi & 0x800000, digi | ~0xFFFFFF, digi)
    return (cab.get('meta', {}), np.array(seqs), digi.astype(np.float64),
            b[:, 9].copy(), int(b[0, 8]))


def lotes_faltantes(seqs):
    """Lotes que el firmware nunca entrego. No es ruido: es dato perdido."""
    if seqs.size == 0:
        return 0
    esperados = np.arange(seqs.min(), seqs.max() + 1)
    return int(len(np.setdiff1d(esperados, seqs)))


def rms_banda(x, fs=FS_NATIVA, banda=BANDA):
    """RMS dentro de la banda, quitando la continua.

    Se quita la media porque el offset del punto de trabajo es justamente lo
    que el lazo deja donde puede, y no es ruido."""
    x = x - x.mean()
    if welch is not None:
        nper = min(len(x), 4096)
        f, p = welch(x, fs=fs, nperseg=nper)
    else:
        n = len(x)
        vent = np.hanning(n)
        esp = np.abs(np.fft.rfft(x * vent)) ** 2
        f = np.fft.rfftfreq(n, 1.0 / fs)
        p = esp * 2.0 / (fs * (vent ** 2).sum())
    sel = (f >= banda[0]) & (f <= banda[1])
    if not sel.any():
        return float('nan')
    df = f[1] - f[0]
    return float(np.sqrt(np.sum(p[sel]) * df))


def resumen(ruta):
    meta, seqs, digi, flags, _ = cargar(ruta)
    if digi.size == 0:
        return None
    marcadas = (flags & (FLAG_SD_WRITE | FLAG_SD_SYNC)) != 0
    fila = {
        'archivo': os.path.basename(ruta),
        'pga': meta.get('pga'), 'pgaout': meta.get('pgaout'),
        'ganancia': (meta.get('pga') or 0) * (meta.get('pgaout') or 0),
        'condicion': meta.get('condicion'),
        'repeticion': meta.get('repeticion'),
        'muestras': int(digi.size),
        'lotes_faltantes': lotes_faltantes(seqs),
        'rms_ancha_cuentas': float(np.std(digi)),
        'rms_banda_cuentas': rms_banda(digi),
        'pico_a_pico_cuentas': float(digi.max() - digi.min()),
        'muestras_marcadas_sd': int(marcadas.sum()),
    }
    # Comparacion DENTRO de la captura: elimina la deriva por construccion.
    if marcadas.any() and (~marcadas).any():
        fila['rms_durante_sd'] = float(np.std(digi[marcadas]))
        fila['rms_fuera_de_sd'] = float(np.std(digi[~marcadas]))
    else:
        fila['rms_durante_sd'] = None
        fila['rms_fuera_de_sd'] = None
    fila['rms_banda_uV'] = fila['rms_banda_cuentas'] * UV_POR_CUENTA
    # Referido a la entrada por la ganancia NOMINAL.  Ojo: ignora las
    # ganancias fijas de las etapas intermedias, asi que sirve para comparar
    # ENTRE ganancias -que es la pregunta- y no como un valor absoluto.
    g = fila['ganancia'] or 1
    fila['rms_banda_uV_ref_entrada'] = fila['rms_banda_uV'] / g
    return fila


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('directorio')
    ap.add_argument('--csv')
    args = ap.parse_args(argv)

    rutas = sorted(glob.glob(os.path.join(args.directorio, '*.txt')))
    filas = [f for f in (resumen(r) for r in rutas) if f]
    if not filas:
        print('no hay volcados en %s' % args.directorio, file=sys.stderr)
        return 1

    if args.csv:
        with open(args.csv, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
            w.writeheader()
            w.writerows(filas)
        print('csv: %s' % args.csv)

    perdidos = sum(f['lotes_faltantes'] for f in filas)
    print('\n%d corridas, %d lotes faltantes en total' % (len(filas), perdidos))
    if perdidos:
        print('  OJO: lotes faltantes NO son ruido, son dato perdido. Si la SD\n'
              '  le roba DMA o CPU al PSoC el danio es este, y no se arregla\n'
              '  con blindaje ni con filtros.')

    # --- delta por condicion, contra BASE, por ganancia ------------------
    print('\n== RMS en %g-%g Hz, en cuentas del ADC ==' % BANDA)
    print('%-12s %-6s %8s %8s %8s %8s' %
          ('par', 'n', 'BASE', 'SD', 'RF', 'SD_RF'))
    pares = sorted({(f['pga'], f['pgaout']) for f in filas})
    for par in pares:
        v = {}
        for cond in ('BASE', 'SD', 'RF', 'SD_RF'):
            xs = [f['rms_banda_cuentas'] for f in filas
                  if (f['pga'], f['pgaout']) == par and f['condicion'] == cond]
            v[cond] = float(np.median(xs)) if xs else float('nan')
        n = sum(1 for f in filas if (f['pga'], f['pgaout']) == par)
        print('x%-4d/x%-4d %6d %8.1f %8.1f %8.1f %8.1f'
              % (par[0], par[1], n, v['BASE'], v['SD'], v['RF'], v['SD_RF']))

    print('\n== cuanto AGREGA cada cosa (veces sobre BASE) ==')
    for par in pares:
        base = [f['rms_banda_cuentas'] for f in filas
                if (f['pga'], f['pgaout']) == par and f['condicion'] == 'BASE']
        if not base:
            continue
        b = float(np.median(base))
        fila = []
        for cond in ('SD', 'RF', 'SD_RF'):
            xs = [f['rms_banda_cuentas'] for f in filas
                  if (f['pga'], f['pgaout']) == par and f['condicion'] == cond]
            fila.append((float(np.median(xs)) / b) if xs and b else float('nan'))
        print('x%-4d/x%-4d  SD %5.2fx   RF %5.2fx   SD+RF %5.2fx'
              % (par[0], par[1], fila[0], fila[1], fila[2]))

    # --- donde se acopla -------------------------------------------------
    print('\n== delta referido a la ENTRADA contra ganancia ==')
    print('   si NO cambia con la ganancia -> el ruido entra ANTES del PGA')
    print('   si BAJA al subir la ganancia -> entra DESPUES')
    for cond in ('SD', 'RF', 'SD_RF'):
        puntos = []
        for par in pares:
            g = par[0] * par[1]
            base = [f['rms_banda_uV_ref_entrada'] for f in filas
                    if (f['pga'], f['pgaout']) == par and f['condicion'] == 'BASE']
            xs = [f['rms_banda_uV_ref_entrada'] for f in filas
                  if (f['pga'], f['pgaout']) == par and f['condicion'] == cond]
            if base and xs:
                d = float(np.median(xs)) - float(np.median(base))
                puntos.append((g, d))
        if len(puntos) >= 2:
            print('  %-6s %s' % (cond, '  '.join('g=%d:%.3f uV' % p
                                                 for p in sorted(puntos))))
        else:
            print('  %-6s hacen falta al menos dos ganancias para decir algo'
                  % cond)

    # --- dentro de la captura --------------------------------------------
    dentro = [f for f in filas if f['rms_durante_sd'] is not None]
    print('\n== dentro de la MISMA captura: muestras marcadas por el firmware ==')
    if dentro:
        for f in dentro:
            print('  %-28s durante SD %8.1f   fuera %8.1f   %5.2fx  (n=%d)'
                  % (f['archivo'], f['rms_durante_sd'], f['rms_fuera_de_sd'],
                     f['rms_durante_sd'] / f['rms_fuera_de_sd']
                     if f['rms_fuera_de_sd'] else float('nan'),
                     f['muestras_marcadas_sd']))
    else:
        print('  ninguna captura trajo muestras marcadas con escritura de SD.')
        print('  Si esperabas que las hubiera, el estresor no estaba corriendo')
        print('  durante la captura: eso invalida la condicion, no la mide.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
