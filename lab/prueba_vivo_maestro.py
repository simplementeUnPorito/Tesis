"""Banco de la captura en vivo de punta a punta por el USB del maestro.

Hace de MATLAB contra el maestro (COM6, paquetes de 6 bytes) y deja abierto
el esclavo (COM8) para fijar la rampa de banco y guardar su log. Verifica que
llegue todo en orden: con la rampa, la muestra k del nodo vale k (24 bits).

  python lab/prueba_vivo_maestro.py --modo 5 --n 2000
  python lab/prueba_vivo_maestro.py --modo 5 --n 0 --stop-s 20

--modo es CAPMODE: bits 0-1 almacenamiento (0 PSoC, 1 compartido, 2 SD),
bit 2 tiempo real (4). Asincronico: el maestro descarga al final.
"""
import argparse
import os
import sys
import threading
import time

import serial


def cmd4(c, p):
    return bytes([0xAB, c, p & 0xFF, (c ^ p) & 0xFF])


def cmd5(c, v):
    lo, hi = v & 0xFF, (v >> 8) & 0xFF
    return bytes([0xAB, c, lo, hi, c ^ lo ^ hi])


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--master', default='COM6')
    ap.add_argument('--slave', default='COM8')
    ap.add_argument('--modo', type=int, required=True)
    ap.add_argument('--n', type=int, required=True, help='lotes; 0 = sin limite')
    ap.add_argument('--stop-s', type=float, default=0.0)
    ap.add_argument('--ramp', type=int, default=1)
    ap.add_argument('--nodo', type=int, default=2)
    ap.add_argument('--timeout-s', type=float, default=180.0)
    ap.add_argument('--log', default='lab/vivo/maestro.log')
    ap.add_argument('--solo-maestro', action='store_true',
                    help='como la web: el modo llega solo por el PRESTART del maestro '
                         '(sin capmode por USB; datos reales, sin rampa)')
    ap.add_argument('--slave-cmd', action='append', default=[],
                    help='comando extra al esclavo antes de capturar')
    args = ap.parse_args(argv)
    os.makedirs(os.path.dirname(args.log), exist_ok=True)

    sl = serial.Serial(args.slave, 115200, timeout=0.2)
    slog = open(args.log.replace('.log', '_esclavo.log'), 'w', encoding='utf-8')
    corriendo = True

    def leer_esclavo():
        while corriendo:
            linea = sl.readline().decode('utf-8', 'replace').rstrip()
            if linea:
                slog.write(linea + '\n')
                if linea.startswith(('#LIVE_END', '#CAPMODE', '#LIVE act')):
                    print('[esclavo]', linea)
    threading.Thread(target=leer_esclavo, daemon=True).start()
    ma = serial.Serial(args.master, 921600, timeout=0.05)
    time.sleep(12.0)  # los dos se resetean al abrir el puerto
    if not args.solo_maestro:
        sl.write(('capmode %d %d %d %d\n' % (args.modo & 3, (args.modo >> 2) & 1, args.ramp,
                                             (args.modo >> 3) & 1)).encode())
        time.sleep(0.5)
    for c in args.slave_cmd:
        sl.write((c + '\n').encode())
        time.sleep(0.3)

    ma.reset_input_buffer()
    ma.write(cmd4(0xA4, 0))           # cerrar lo que haya quedado de antes
    time.sleep(2.0)
    ma.write(cmd4(0xAF, args.modo))
    time.sleep(0.2)
    ma.write(cmd4(0xA2, 1))          # ARM, 1 esclavo
    time.sleep(3.5)
    ma.reset_input_buffer()
    t0 = time.time()
    ma.write(cmd5(0xA3, args.n))
    print('START n=%d modo=%d' % (args.n, args.modo))

    buf = bytearray()
    muestras = 0
    malas = 0
    primera_mala = None
    estados = []
    parado = False
    fin = None
    ultimo_stat = 0.0
    while time.time() - t0 < args.timeout_s:
        buf += ma.read(4096)
        i = 0
        while len(buf) - i >= 6:
            if buf[i] != 0x56:
                i += 1
                continue
            nodo, tipo = buf[i + 1], buf[i + 2]
            val = (buf[i + 3] << 16) | (buf[i + 4] << 8) | buf[i + 5]
            if tipo == 0x00 and nodo == args.nodo:
                if args.ramp and val != (muestras & 0xFFFFFF):
                    malas += 1
                    if primera_mala is None:
                        primera_mala = (muestras, val)
                muestras += 1
            elif tipo == 0x01 and nodo == 0:
                estado = buf[i + 5]
                if not estados or estados[-1] != estado:
                    estados.append(estado)
                    print('  %6.2f s estado maestro=%d muestras=%d' % (time.time() - t0, estado, muestras))
            i += 6
        del buf[:i]
        if time.time() - ultimo_stat >= 2.0:
            ultimo_stat = time.time()
            sl.write(b'livestat\n')
        if not parado and args.stop_s > 0 and time.time() - t0 >= args.stop_s:
            ma.write(cmd4(0xA4, 0))
            parado = True
            print('  STOP a %.1f s' % (time.time() - t0))
        # ARMED=2 despues de RUNNING=3 (tiempo real) o de DUMPING=5
        if len(estados) >= 2 and estados[-1] in (0, 2) and (3 in estados):
            fin = time.time() - t0
            break
    corriendo = False
    time.sleep(0.3)
    lotes = muestras / 30.0
    print('RESULTADO modo=%d n=%d muestras=%d lotes=%.1f malas=%d primera_mala=%s fin=%s' %
          (args.modo, args.n, muestras, lotes, malas, primera_mala,
           '%.2f s' % fin if fin else 'TIMEOUT'))
    ok = fin is not None and malas == 0 and (args.n == 0 or muestras == args.n * 30)
    print('OK' if ok else 'FALLA')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
