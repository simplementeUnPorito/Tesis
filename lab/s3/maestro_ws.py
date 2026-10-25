"""Cliente del maestro por WebSocket, igual que la web (ws://192.168.4.1/ws).

Paquetes de 6 bytes 0x56 [nodo][tipo][b2][b1][b0]; comandos como JSON plano
(ver master/data/js/protocol.js). Sirve de base para los bancos de lab/s3.

  python lab/s3/maestro_ws.py estado [segundos]
"""
import json
import sys
import threading
import time
from collections import defaultdict

import websocket

URL = 'ws://192.168.4.1/ws'
PKT = 0x56
ZPKT = 0x57   # lote comprimido: [0x57][nodo][seq LE24][len][GeoZ]
PT_DATA, PT_HB, PT_ACK = 0x00, 0x01, 0x07
PT_BATCH, PT_BATCH_END, PT_MARK = 0xFA, 0xF9, 0xFB
PT_LAT, PT_STATUS, PT_READY = 0xFC, 0xFD, 0xFE


def hex2(b):
    return '%02X' % (b & 0xFF)


class Maestro:
    def __init__(self, url=URL, verbose=False):
        self.url = url
        self.verbose = verbose
        self.packets = []          # (t, nodo, tipo, b2, b1, b0)
        self.texts = []            # (t, dict|str)
        self.lock = threading.Lock()
        self.ws = None
        self.on_packet = None
        self.on_text = None
        self.on_zbatch = None
        self.zbytes = 0
        self.zrecords = 0

    def connect(self, timeout=10):
        self.ws = websocket.create_connection(self.url, timeout=timeout)
        self.ws.settimeout(0.5)
        self._run = True
        self._th = threading.Thread(target=self._reader, daemon=True)
        self._th.start()
        return self

    def close(self):
        self._run = False
        try:
            self.ws.close()
        except Exception:
            pass

    def _reader(self):
        while self._run:
            try:
                op, data = self.ws.recv_data()
            except websocket.WebSocketTimeoutException:
                continue
            except Exception as e:
                if self._run and self.verbose:
                    print('WS cerrado:', e)
                self._run = False
                return
            t = time.time()
            self.total_bytes = getattr(self, "total_bytes", 0) + len(data)
            if op == websocket.ABNF.OPCODE_TEXT:
                s = data.decode('utf-8', 'replace')
                try:
                    obj = json.loads(s)
                except Exception:
                    obj = s
                with self.lock:
                    self.texts.append((t, obj))
                if self.on_text:
                    self.on_text(t, obj)
                if self.verbose:
                    print('TXT', s[:200])
                continue
            i = 0
            while i < len(data):
                if data[i] == ZPKT and i + 6 <= len(data):
                    n = data[i + 5]
                    if i + 6 + n > len(data):
                        break
                    seq = data[i + 2] | (data[i + 3] << 8) | (data[i + 4] << 16)
                    self.zbytes += 6 + n
                    self.zrecords += 1
                    if self.on_zbatch:
                        self.on_zbatch(t, data[i + 1], seq, data[i + 6:i + 6 + n])
                    i += 6 + n
                    continue
                if data[i] != PKT or i + 6 > len(data):
                    i += 1
                    continue
                p = (t, data[i + 1], data[i + 2], data[i + 3], data[i + 4], data[i + 5])
                with self.lock:
                    self.packets.append(p)
                if self.on_packet:
                    self.on_packet(p)
                i += 6

    # ── comandos ──────────────────────────────────────────────────────────
    def send_json(self, obj):
        self.ws.send(json.dumps(obj))

    def std(self, cmd, param=0):
        self.send_json({'cmd': hex2(cmd), 'param': param & 0xFF})

    def std16(self, cmd, value):
        self.send_json({'cmd': hex2(cmd), 'value': value & 0xFFFF})

    def directed(self, node, sub, param=0, param2=None):
        o = {'cmd': 'BD', 'node': node, 'sub': hex2(sub), 'param': param & 0xFF}
        if param2 is not None:
            o['param2'] = param2 & 0xFF
        self.send_json(o)

    def snapshot(self):
        with self.lock:
            return list(self.packets), list(self.texts)


def resumen_estado(packets, texts):
    nodos = defaultdict(dict)
    for (_, n, tp, b2, b1, b0) in packets:
        if tp == PT_STATUS:
            nodos[n][b2] = (b1, b0)
        elif tp == PT_HB:
            nodos[n]['hb'] = (b2, b1, b0)
    return nodos


def main():
    seg = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
    m = Maestro().connect()
    m.std(0xA5)   # STATUS
    time.sleep(seg)
    pk, tx = m.snapshot()
    m.close()
    print(f'{len(pk)} paquetes, {len(tx)} textos en {seg:.0f} s')
    for n, subs in sorted(resumen_estado(pk, tx).items()):
        print(f'nodo {n:3d}:', {('%02X' % k if isinstance(k, int) else k): v for k, v in sorted(subs.items(), key=lambda kv: str(kv[0]))})
    tipos = defaultdict(int)
    for (_, n, tp, *_r) in pk:
        tipos[(n, tp)] += 1
    print('conteo (nodo,tipo):', dict(sorted(tipos.items())))
    for t, o in tx[-10:]:
        print('texto:', str(o)[:200])


if __name__ == '__main__':
    main()
