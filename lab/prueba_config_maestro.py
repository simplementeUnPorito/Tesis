"""Banco: configuraciones del esclavo a traves del serial del maestro.

Manda comandos dirigidos (0xBD) por el USB del maestro y espera el ACK
(tipo 0x07) que vuelve del esclavo. Al final hace una captura corta en tiempo
real con el ADC de verdad para ver que la cadena sigue andando.

  python lab/prueba_config_maestro.py
"""
import argparse
import sys
import time

import serial

PASOS = [
    ('PGA x4', 0xA6, 2), ('PGA x8', 0xA6, 3),
    ('PGAout x8', 0xA8, 3), ('PGAout x16', 0xA8, 4),
    ('decimacion 2', 0xBB, 2), ('decimacion 1', 0xBB, 1),
    ('ADC +-2,5 V', 0xBA, 1),
    ('stream crudo', 0xB7, 0),
    ('vista LPo', 0xAC, 4), ('vista normal', 0xAC, 0xFF),
    ('forzar PI 3 s', 0xAB, 3),
]


def directed(node, sub, p):
    return bytes([0xAB, 0xBD, node, sub, p, node ^ sub ^ p])


def cmd4(c, p):
    return bytes([0xAB, c, p, c ^ p])


def cmd5(c, v):
    lo, hi = v & 0xFF, (v >> 8) & 0xFF
    return bytes([0xAB, c, lo, hi, c ^ lo ^ hi])


def paquetes(ma, segundos):
    buf = bytearray()
    fin = time.time() + segundos
    while time.time() < fin:
        buf += ma.read(4096)
        i = 0
        while len(buf) - i >= 6:
            if buf[i] != 0x56:
                i += 1
                continue
            yield bytes(buf[i:i + 6])
            i += 6
        del buf[:i]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--master', default='COM6')
    ap.add_argument('--slave', default='COM8')
    ap.add_argument('--nodo', type=int, default=2)
    args = ap.parse_args(argv)
    sl = serial.Serial(args.slave, 115200, timeout=0.2)
    ma = serial.Serial(args.master, 921600, timeout=0.05)
    time.sleep(12.0)
    ma.reset_input_buffer()
    fallas = 0
    for nombre, sub, p in PASOS:
        ma.write(directed(args.nodo, sub, p))
        ack = None
        for pk in paquetes(ma, 6.0):
            if pk[1] == args.nodo and pk[2] == 0x07 and pk[3] == sub:
                ack = pk[4]
                break
        ok = ack is not None and ack != 0
        fallas += 0 if ok else 1
        print('%-16s sub=0x%02X p=%3d -> %s' % (nombre, sub, p,
              'ack=%d' % ack if ack is not None else 'SIN ACK'))
    # captura real corta en tiempo real compartido
    sl.write(b'capmode 1 1 0 0\n')
    time.sleep(0.5)
    ma.write(cmd4(0xAF, 5))
    time.sleep(0.2)
    ma.write(cmd4(0xA2, 1))
    time.sleep(3.5)
    ma.reset_input_buffer()
    ma.write(cmd5(0xA3, 300))
    n = 0
    estados = []
    for pk in paquetes(ma, 30.0):
        if pk[2] == 0x00 and pk[1] == args.nodo:
            n += 1
        elif pk[2] == 0x01 and pk[1] == 0:
            if not estados or estados[-1] != pk[5]:
                estados.append(pk[5])
            if 3 in estados and estados[-1] == 2:
                break
    print('captura real: %d muestras (esperadas 9000), estados=%s' % (n, estados))
    if n != 9000:
        fallas += 1
    print('OK' if fallas == 0 else 'FALLAS=%d' % fallas)
    return 0 if fallas == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
