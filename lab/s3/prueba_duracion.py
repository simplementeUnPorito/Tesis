"""Cuanto aguanta el tiempo real sin limite, con y sin decimacion.

Fija N (decimacion) en los nodos, arranca tiempo real sin limite (lotes
comprimidos a la web) y cada 10 s compara los lotes recibidos con los que
deberian haber salido a la Fs efectiva (2604/N). Si el atraso no crece, el
enlace sostiene esa Fs indefinidamente; si crece, se informa a que ritmo y
cuanto tardaria en llenarse el respaldo del esclavo. Al final STOP y mide
cuanto tarda en vaciarse.

  python lab/s3/prueba_duracion.py --n 1 --s 300
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from maestro_ws import Maestro  # noqa: E402

FS = 2604.0
SPB = 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=1, help='decimacion')
    ap.add_argument('--s', type=float, default=300)
    ap.add_argument('--nodos', default='2,4')
    ap.add_argument('--almacen', type=int, default=1)
    ap.add_argument('--sync', type=int, default=0, help='0 FTM activo, 1 FTM pausado, 2 radio apagada')
    a = ap.parse_args()
    nodos = [int(x) for x in a.nodos.split(',')]
    seqs = {n: -1 for n in nodos}
    count = {n: 0 for n in nodos}
    m = Maestro(reconnect=True)
    m.on_reconnect = lambda: m.send_json({'cmd': 'ZWEB', 'on': 1})

    def on_z(t, n, seq, payload):
        if n in seqs:
            seqs[n] = max(seqs[n], seq)
            count[n] += 1

    m.on_zbatch = on_z
    m.connect()
    m.send_json({'cmd': 'ZWEB', 'on': 1})
    m.std(0xA4)
    time.sleep(2)
    for n in nodos:
        m.directed(n, 0xBB, a.n)
        time.sleep(0.5)
    time.sleep(2)
    m.std(0xAF, (a.almacen & 3) | 4)
    m.std(0xB8, a.sync)
    m.std16(0xAD, 0)
    m.std(0xA2)
    time.sleep(2.5)
    t0 = time.time()
    m.std16(0xA3, 0)
    fs = FS / a.n
    filas = []
    print(f'N={a.n} Fs={fs:.1f} Hz -> {fs / SPB:.1f} lotes/s por nodo; {a.s:.0f} s')
    while time.time() - t0 < a.s:
        time.sleep(10)
        el = time.time() - t0
        esperado = el * fs / SPB
        fila = {'t': round(el, 1), 'reconex': m.reconnects}
        for n in nodos:
            fila[f'S{n}_lotes'] = count[n]
            fila[f'S{n}_atraso'] = round(esperado - count[n], 1)
        filas.append(fila)
        print(fila, flush=True)
    m.std(0xA4)
    t_stop = time.time()
    total_stop = dict(count)
    last = dict(count)
    quieto = time.time()
    while time.time() - t_stop < 120:
        time.sleep(1)
        if count != last:
            last = dict(count)
            quieto = time.time()
        elif time.time() - quieto > 5:
            break
    drenaje = quieto - t_stop
    m.close()
    # ritmo de crecimiento del atraso (lotes/s) en la segunda mitad
    ritmo = {}
    if len(filas) >= 4:
        a1, a2 = filas[len(filas) // 2], filas[-1]
        for n in nodos:
            ritmo[n] = round((a2[f'S{n}_atraso'] - a1[f'S{n}_atraso']) / (a2['t'] - a1['t']), 3)
    res = {'N': a.n, 'fs': fs, 'segundos': a.s, 'filas': filas, 'al_stop': total_stop, 'reconexiones': m.reconnects,
           'final': count, 'drenaje_s': round(drenaje, 1), 'atraso_crece_lotes_por_s': ritmo}
    os.makedirs('lab/s3/duracion', exist_ok=True)
    json.dump(res, open(f'lab/s3/duracion/N{a.n}_{int(a.s)}s_nodos{a.nodos.replace(",", "-")}_sync{a.sync}.json', 'w'), indent=1)
    print('final', count, 'drenaje tras STOP', round(drenaje, 1), 's; atraso crece (lotes/s):', ritmo)


if __name__ == '__main__':
    main()
