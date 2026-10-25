"""Lee el log humano del maestro S3 (entorno masterS3_log) desde la UART0.

El puerto mezcla paquetes binarios 0x56 de 6 bytes con lineas de texto: se
quitan los paquetes y se guardan las lineas con hora en lab/s3/maestro.log.

  python lab/s3/log_maestro.py [COM14] [--reset]
"""
import sys
import time

import serial

args = [x for x in sys.argv[1:] if not x.startswith('--')]
port = args[0] if args else 'COM14'
reset = '--reset' in sys.argv
s = serial.Serial()
s.port, s.baudrate, s.timeout = port, 921600, 0.2
s.dtr = False
s.rts = False
s.open()
if reset:   # pulso en EN por RTS (puente CH343 con auto-reset): ver el arranque
    s.rts = True
    time.sleep(0.15)
    s.rts = False
out = open('lab/s3/maestro.log', 'a', encoding='utf-8', buffering=1)
buf = bytearray()
while True:
    buf += s.read(4096)
    # sacar paquetes binarios 0x56 [nodo][tipo][b2][b1][b0]
    i = 0
    clean = bytearray()
    while i < len(buf):
        if buf[i] == 0x56 and i + 6 <= len(buf) and buf[i + 2] in (0x00, 0x01, 0x07, 0xF9, 0xFA, 0xFB, 0xFC, 0xFD, 0xFE):
            i += 6
            continue
        if buf[i] == 0x56 and i + 6 > len(buf):
            break
        clean.append(buf[i])
        i += 1
    buf = buf[i:]
    for line in clean.decode('latin1').replace('\r', '').split('\n'):
        line = ''.join(c for c in line if c.isprintable())
        if len(line) > 2:
            out.write(time.strftime('%H:%M:%S ') + line + '\n')
