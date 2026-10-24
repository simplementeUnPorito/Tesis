"""Compresion sin perdida de lotes de 30 muestras (24 bits + flags) sobre
capturas reales. Cada lote se comprime solo (un lote perdido o retransmitido
se decodifica sin los demas)."""
import glob, zlib, numpy as np

caps = sorted(glob.glob('../ruido_firmas/capturas/*/*.npz'))
B = 30

def bits_rice(res, k):
    u = np.where(res >= 0, 2 * res, -2 * res - 1).astype(np.int64)   # zigzag
    return int(np.sum((u >> k) + 1 + k))

def best_rice(res):
    return min((bits_rice(res, k), k) for k in range(0, 24))

def lpc_res(x, order):
    x = x.astype(np.int64)
    if order == 0: return x
    if order == 1: return np.diff(x, prepend=0)
    r = x.copy()
    for _ in range(order): r = np.diff(r, prepend=0)
    return r

def batch_bits(x, flags):
    # cabecera: seq32 + nodo + orden(3b) + k(5b) + primeras muestras crudas segun orden
    best = None
    for order in range(0, 4):
        res = lpc_res(x, order)
        warm = res[:order]; rest = res[order:]
        b, k = best_rice(rest)
        total = 8 * 6 + 8 + order * 24 + b
        if best is None or total < best[0]: best = (total, order, k)
    # flags: 1 bit "hay flags"; si hay, run-length simple (byte por cambio)
    fb = 1
    if flags.any():
        changes = np.count_nonzero(np.diff(flags.astype(int), prepend=0))
        fb += 8 * (2 * changes + 1)
    raw = 8 * 6 + B * 24 + 1 + (B * 8 if flags.any() else 0)   # escape crudo
    return min(best[0] + fb, raw), best[1]

tot = {'actual': 0, 'campos': 0, 'rice': 0, 'zlib': 0}
per = []; orders = np.zeros(4, int)
for f in caps:
    d = np.load(f); x = d['samples'].astype(np.int64); fl = d['flags']
    n = (len(x) // B) * B
    for i in range(0, n, B):
        xb = x[i:i + B]; fb = fl[i:i + B]
        bb, o = batch_bits(xb, fb)
        orders[o] += 1
        per.append(bb / 8)
        tot['actual'] += 334
        tot['campos'] += 6 + B * 3 + (B if fb.any() else 0) + 1
        tot['rice'] += bb / 8
        packed = (xb & 0xFFFFFF).astype('<i4').tobytes() + fb.tobytes()
        tot['zlib'] += 6 + len(zlib.compress(packed, 9))
per = np.array(per)
nb = len(per)
print(f'capturas {len(caps)}, lotes {nb}')
for k, v in tot.items():
    print(f'{k:7s} {v / nb:7.1f} B/lote   relacion {334 * nb / v:5.2f}x')
print(f'rice: media {per.mean():.1f} p95 {np.percentile(per, 95):.1f} max {per.max():.1f} B')
print('ordenes elegidos', dict(enumerate(orders)))
