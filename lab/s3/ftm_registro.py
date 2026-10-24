"""Registro de los reportes FTM de los esclavos y calibracion de distancia.

Escucha {"type":"ftm"} en el WebSocket del maestro durante un rato y guarda cada
reporte en un CSV junto con la distancia declarada (cinta) de esa posicion.
Con varias posiciones ajusta d_declarada = escala*d_ftm (+ offset con >= 3
distancias), igual que el panel de la web (sync_panel.js).

  python lab/s3/ftm_registro.py --nodo 2 --declarada 4.60 --s 60
  python lab/s3/ftm_registro.py --ajustar            (usa todo el CSV)
"""
import argparse
import csv
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from maestro_ws import Maestro  # noqa: E402

C = 299792458.0
CSV = os.path.join(os.path.dirname(__file__), 'ftm_registro.csv')
CAMPOS = ['t', 'nodo', 'declarada_m', 'status', 'sessions', 'frames_total', 'frames_valid',
          'window', 'rtt_med_ps', 'rtt_mad_ps', 'rtt_p95_ps', 'rssi_med', 'dist_sdk_cm',
          'skew_ppb', 'resid_ns', 'age_ms', 'channel', 'init_err', 'ev_status', 'd_ftm_m']


def registrar(nodo, declarada, segundos):
    nuevo = not os.path.exists(CSV)
    f = open(CSV, 'a', newline='')
    w = csv.DictWriter(f, fieldnames=CAMPOS)
    if nuevo:
        w.writeheader()
    filas = []

    def on_text(t, o):
        if not isinstance(o, dict) or o.get('type') != 'ftm':
            return
        if nodo and o.get('node') != nodo:
            return
        d = o['rtt_med_ps'] * 1e-12 * C / 2 if o.get('window') else ''
        fila = {k: o.get(k, '') for k in CAMPOS}
        fila.update(t=round(t, 2), nodo=o.get('node'), declarada_m=declarada, d_ftm_m=d)
        w.writerow(fila)
        filas.append(fila)
        print({k: fila[k] for k in ('nodo', 'status', 'window', 'rtt_med_ps', 'd_ftm_m',
                                    'skew_ppb', 'resid_ns', 'init_err', 'ev_status')})

    m = Maestro()
    m.on_text = on_text
    m.connect()
    time.sleep(segundos)
    m.close()
    f.close()
    print(f'{len(filas)} reportes -> {CSV}')


def ajustar():
    pts = {}
    for r in csv.DictReader(open(CSV)):
        if r['d_ftm_m'] and r['declarada_m'] and int(r['window'] or 0) >= 16:
            pts.setdefault(int(r['nodo']), []).append((float(r['d_ftm_m']), float(r['declarada_m'])))
    for n, p in sorted(pts.items()):
        x = np.array([a for a, _ in p])
        y = np.array([b for _, b in p])
        distintas = len(set(np.round(y, 2)))
        if distintas >= 3:
            A = np.vstack([x, np.ones_like(x)]).T
            (k, b), *_ = np.linalg.lstsq(A, y, rcond=None)
        else:
            k, b = float(x @ y / (x @ x)), 0.0
        res = y - (k * x + b)
        print(f'S{n}: {len(p)} reportes, {distintas} distancias -> escala {k:.4f} offset {b:.3f} m, '
              f'residuo max {np.abs(res).max():.3f} m')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nodo', type=int, default=0)
    ap.add_argument('--declarada', type=float, default=None)
    ap.add_argument('--s', type=float, default=30)
    ap.add_argument('--ajustar', action='store_true')
    a = ap.parse_args()
    if a.ajustar:
        ajustar()
    else:
        registrar(a.nodo, '' if a.declarada is None else a.declarada, a.s)


if __name__ == '__main__':
    main()
