"""Captura de punta a punta por el WebSocket del maestro, igual que la web.

Arma los lotes por numero de secuencia (0xFA), deja huecos (NaN) para los que
faltan, los pide con FILL como la web y guarda crudo + marcas por nodo.

  python lab/s3/captura_ws.py --modo async --n 200
  python lab/s3/captura_ws.py --modo rt --n 600 --droptest 7
  python lab/s3/captura_ws.py --modo rt --n 0 --stop-s 20     (sin limite)

--almacen 0 RAM PSoC, 1 RAM compartida, 2 RAM+SD. --sync 0/1/2 (FTM activo,
pausado, radio apagada). Salida: lab/s3/capturas/<stamp>/ (npz + resumen.json).
"""
import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from geo_codec import decode as geoz_decode  # noqa: E402
from maestro_ws import (Maestro, PT_DATA, PT_BATCH, PT_BATCH_END, PT_MARK, PT_HB)  # noqa: E402

SPB = 30
ST_NAMES = {0: 'IDLE', 1: 'ARMING', 2: 'ARMED', 3: 'RUNNING', 4: 'STOPPING', 5: 'DUMPING',
            6: 'PRESTART', 7: 'SCOPE_MULTI'}


class Nodo:
    def __init__(self, n):
        self.n = n
        self.raw = {}          # posicion -> valor 24 bits
        self.marks = {}        # posicion -> flags
        self.seq_next = 0
        self.missing = set()
        self.asked = {}
        self.mode = 'append'
        self.pos = 0           # proxima posicion en modo append
        self.fill_pos = 0
        self.fill_left = 0
        self.pending_mark = 0
        self.batches_seen = 0
        self.dups = 0
        self.fills_ok = 0
        self.total_end = None

    def batch(self, seq):
        self.batches_seen += 1
        if seq == self.seq_next:
            self.mode = 'append'
            self.pos = seq * SPB
            self.seq_next += 1
        elif seq > self.seq_next:
            for s in range(self.seq_next, seq):
                self.missing.add(s)
            self.mode = 'append'
            self.pos = seq * SPB
            self.seq_next = seq + 1
        elif seq in self.missing:
            self.missing.discard(seq)
            self.fills_ok += 1
            self.mode = 'fill'
            self.fill_pos = seq * SPB
            self.fill_left = SPB
        else:
            self.dups += 1
            self.mode = 'skip'
            self.fill_left = SPB

    def end(self, total):
        self.total_end = total
        for s in range(self.seq_next, total):
            self.missing.add(s)
        self.seq_next = max(self.seq_next, total)

    def data(self, v):
        if self.mode == 'skip':
            self.pending_mark = 0
            self.fill_left -= 1
            if self.fill_left <= 0:
                self.mode = 'append'
            return
        p = self.fill_pos if self.mode == 'fill' else self.pos
        if self.pending_mark:
            self.marks[p] = self.pending_mark
            self.pending_mark = 0
        self.raw[p] = v
        if self.mode == 'fill':
            self.fill_pos += 1
            self.fill_left -= 1
            if self.fill_left <= 0:
                self.mode = 'append'
        else:
            self.pos += 1

    def arrays(self):
        n = self.seq_next * SPB
        if self.raw:
            n = max(n, max(self.raw) + 1)
        x = np.full(n, np.nan)
        for p, v in self.raw.items():
            x[p] = v
        m = np.zeros(n, dtype=np.uint8)
        for p, f in self.marks.items():
            if p < n:
                m[p] = f
        return x, m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--modo', choices=['async', 'rt', 'rapida'], default='async')
    ap.add_argument('--almacen', type=int, default=1)
    ap.add_argument('--sync', type=int, default=0)
    ap.add_argument('--n', type=int, default=200, help='lotes; 0 = sin limite (solo rt)')
    ap.add_argument('--stop-s', type=float, default=0.0)
    ap.add_argument('--droptest', type=int, default=0, help='el maestro descarta 1 de cada K lotes')
    ap.add_argument('--timeout', type=float, default=240.0)
    ap.add_argument('--nodos', default='', help='lista de nodos esperados, ej 2,4')
    ap.add_argument('--out', default='lab/s3/capturas')
    ap.add_argument('--zweb', action='store_true', help='pedir lotes comprimidos a la web (0x57)')
    a = ap.parse_args()

    mode_byte = a.almacen & 3
    if a.modo == 'rt':
        mode_byte |= 4
    elif a.modo == 'rapida':
        mode_byte |= 8
    nodos = {}
    estado = {'master': None, 'hist': []}
    m = Maestro()

    def on_packet(p):
        _, n, tp, b2, b1, b0 = p
        v24u = (b2 << 16) | (b1 << 8) | b0
        if tp == PT_HB and n in (0, 0xFF):
            if estado['master'] != b0:
                estado['hist'].append((time.time(), b0))
            estado['master'] = b0
            return
        if n == 0 or n >= 0xF0:
            return
        nd = nodos.setdefault(n, Nodo(n))
        if tp == PT_DATA:
            nd.data(v24u - (1 << 24) if v24u & 0x800000 else v24u)
        elif tp == PT_BATCH:
            nd.batch(v24u)
        elif tp == PT_BATCH_END:
            nd.end(v24u)
        elif tp == PT_MARK:
            nd.pending_mark |= b2

    def on_zbatch(t, n, seq, payload):
        nd = nodos.setdefault(n, Nodo(n))
        try:
            vals, flags = geoz_decode(payload)
        except Exception as e:
            print('lote Z invalido', n, seq, e)
            return
        nd.batch(seq)
        for v, f in zip(vals, flags):
            if f:
                nd.pending_mark |= f
            nd.data(v)

    m.on_packet = on_packet
    m.on_zbatch = on_zbatch
    m.connect()
    if a.zweb:
        m.send_json({'cmd': 'ZWEB', 'on': 1})
    time.sleep(1.0)
    m.send_json({'cmd': 'DROPTEST', 'every': a.droptest})
    m.std(0xAF, mode_byte)
    m.std(0xB8, a.sync)
    m.std16(0xAD, 0)          # HAMMER = mismo largo
    m.std(0xA2, 0)            # ARM: los esclavos contestan ARM_ACK
    time.sleep(2.5)
    t0 = time.time()
    m.std16(0xA3, a.n)        # START
    print(f'START modo=0x{mode_byte:02X} sync={a.sync} n={a.n} droptest={a.droptest}')
    stop_sent = False
    vio_running = False
    fin = None
    while time.time() - t0 < a.timeout:
        time.sleep(0.5)
        st = estado['master']
        if st in (3, 5):
            vio_running = True
        if a.stop_s and not stop_sent and time.time() - t0 > a.stop_s:
            m.std(0xA4)
            stop_sent = True
            print(f'{time.time() - t0:6.1f} s STOP')
        # pedir huecos como la web (cada 0,5 s, sin repetir antes de 3 s)
        ahora = time.time()
        for nd in nodos.values():
            pend = sorted(s for s in nd.missing if ahora - nd.asked.get(s, 0) > 3)
            i = 0
            while i < len(pend):
                j = i
                while j + 1 < len(pend) and pend[j + 1] == pend[j] + 1 and j - i < 63:
                    j += 1
                m.send_json({'cmd': 'FILL', 'node': nd.n, 'seq': pend[i], 'count': j - i + 1})
                for s in pend[i:j + 1]:
                    nd.asked[s] = ahora
                i = j + 1
        if vio_running and st in (0, 2) and fin is None:
            fin = time.time()
            print(f'{fin - t0:6.1f} s fin de captura (estado {ST_NAMES.get(st)})')
        if fin and (all(not nd.missing for nd in nodos.values()) or time.time() - fin > 20):
            break
    m.send_json({'cmd': 'DROPTEST', 'every': 0})
    time.sleep(0.5)
    pk, tx = m.snapshot()
    m.close()

    stamp = time.strftime('%Y%m%d_%H%M%S')
    out = os.path.join(a.out, stamp)
    os.makedirs(out, exist_ok=True)
    res = {'args': vars(a), 'mode_byte': mode_byte, 'ws_bytes_total': getattr(m, 'total_bytes', 0), 'ws_bytes_z': m.zbytes, 'ws_records_z': m.zrecords, 'duracion_s': time.time() - t0,
           'estados': [(round(t - t0, 2), ST_NAMES.get(s, s)) for t, s in estado['hist']],
           'textos': [o for _, o in tx if isinstance(o, dict) and o.get('type') not in ('link', 'ftm')][:50],
           'nodos': {}}
    for n, nd in sorted(nodos.items()):
        x, mk = nd.arrays()
        np.savez_compressed(os.path.join(out, f'nodo{n}.npz'), raw=x, marks=mk)
        nan = int(np.isnan(x).sum())
        r = {'lotes_vistos': nd.batches_seen, 'seq_next': nd.seq_next, 'total_end': nd.total_end,
             'muestras': int(x.size), 'nan': nan, 'faltan_lotes': sorted(nd.missing)[:50],
             'n_faltan': len(nd.missing), 'duplicados': nd.dups, 'rellenos_ok': nd.fills_ok,
             'marcas': {f'0x{b:02X}': int(((mk & b) != 0).sum()) for b in (1, 2, 4, 8, 16, 32)}}
        if a.n:
            r['esperadas'] = a.n * SPB
        res['nodos'][n] = r
        print(f'nodo {n}: {json.dumps(r)}')
    json.dump(res, open(os.path.join(out, 'resumen.json'), 'w'), indent=1, default=str)
    print('->', out)


if __name__ == '__main__':
    main()
