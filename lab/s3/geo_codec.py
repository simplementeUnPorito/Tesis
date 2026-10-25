"""Decodificador GeoZ (v1 y v2) en Python, igual a master/data/js/geo_codec.js.

decode(payload) -> (values[30] int, flags[30] int). Lanza ValueError si el
lote no es valido.
"""
N = 30
ORDER_MASK, ESCAPE, HAS_FLAGS, FORMAT_V2 = 0x03, 0x04, 0x08, 0x10


def _s24(b, p):
    u = b[p] | (b[p + 1] << 8) | (b[p + 2] << 16)
    return u - 0x1000000 if u & 0x800000 else u


def _unzz(v):
    return -(v // 2) - 1 if v % 2 else v // 2


class _Bits:
    def __init__(self, b, pos):
        self.b, self.start, self.bit = b, pos, 0

    def read(self):
        if self.bit >= (len(self.b) - self.start) * 8:
            raise ValueError('GeoZ truncado')
        v = (self.b[self.start + (self.bit >> 3)] >> (7 - (self.bit & 7))) & 1
        self.bit += 1
        return v

    def end(self):
        return self.start + (self.bit + 7) // 8


def _flags(b, pos, mode):
    f = [0] * N
    if mode & HAS_FLAGS:
        at = 0
        while at < N:
            if pos + 2 > len(b):
                raise ValueError('RLE truncado')
            v, run = b[pos], b[pos + 1]
            pos += 2
            if run == 0 or at + run > N:
                raise ValueError('RLE invalido')
            f[at:at + run] = [v] * run
            at += run
    if pos != len(b):
        raise ValueError('bytes sobrantes')
    return f


def _pred(x, i, order):
    if order == 0:
        return 0
    if order == 1:
        return x[i - 1]
    if order == 2:
        return 2 * x[i - 1] - x[i - 2]
    return 3 * x[i - 1] - 3 * x[i - 2] + x[i - 3]


def decode(payload):
    b = bytes(payload)
    mode = b[0]
    x = [0] * N
    if mode & ESCAPE:
        for i in range(N):
            x[i] = _s24(b, 1 + 3 * i)
        return x, _flags(b, 91, mode)
    if not mode & FORMAT_V2:
        k = b[4]
        x[0] = _s24(b, 1)
        r = _Bits(b, 5)
        for i in range(1, N):
            q = 0
            while r.read() == 1:
                q += 1
            rem = 0
            for _ in range(k):
                rem = rem * 2 + r.read()
            v = (x[i - 1] + _unzz(q * (1 << k) + rem)) % 0x1000000
            x[i] = v - 0x1000000 if v >= 0x800000 else v
        return x, _flags(b, r.end(), mode)
    order = mode & ORDER_MASK
    k = b[1]
    for i in range(order):
        x[i] = _s24(b, 2 + 3 * i)
    r = _Bits(b, 2 + 3 * order)
    for i in range(order, N):
        q = 0
        while r.read() == 0:
            q += 1
        rem = 0
        for _ in range(k):
            rem = rem * 2 + r.read()
        x[i] = _pred(x, i, order) + _unzz(q * (1 << k) + rem)
    return x, _flags(b, r.end(), mode)
