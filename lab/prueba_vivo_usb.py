"""Banco de la captura en vivo por USB, sin el maestro.

Abre el esclavo, espera el arranque y corre una lista de pasos. Cada paso es
un comando y la marca que lo da por terminado. Guarda todo el monitor en el
log y resume las lineas #LIVE / #LIVE_END / #LDUMP_END.

  python lab/prueba_vivo_usb.py --port COM8 --log lab/vivo/p1.log \
      "capmode 1 0 1" "livecap 300=#LIVECAP" "livedump=#LDUMP_END"

Un paso "cmd=MARCA" espera la marca; sin "=" solo espera 0,5 s.
"""
import argparse
import os
import sys
import time

import serial


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', default='COM8')
    ap.add_argument('--log', required=True)
    ap.add_argument('--boot-s', type=float, default=9.0)
    ap.add_argument('--timeout-s', type=float, default=180.0)
    ap.add_argument('pasos', nargs='+')
    args = ap.parse_args(argv)

    os.makedirs(os.path.dirname(os.path.abspath(args.log)), exist_ok=True)
    log = open(args.log, 'w', encoding='utf-8')
    p = serial.Serial(args.port, 115200, timeout=0.2)
    t0 = time.time()

    def leer_hasta(marca, limite):
        fin = time.time() + limite
        while time.time() < fin:
            linea = p.readline().decode('utf-8', 'replace').rstrip()
            if not linea:
                continue
            log.write('%8.2f %s\n' % (time.time() - t0, linea))
            log.flush()
            if linea.startswith(('#LIVE', '#LDUMP_END', '#LDUMP ', '#CAPMODE', '#RTSIM')) \
                    and not linea.startswith('#LIVE act'):
                print(linea)
            if marca and marca in linea:
                if linea.startswith('#LIVE act'):
                    print(linea)
                return True
        return False

    leer_hasta(None, args.boot_s)
    ok = True
    for paso in args.pasos:
        cmd, _, marca = paso.partition('=')
        log.write('>>> %s\n' % cmd)
        print('>>>', cmd)
        p.write((cmd + '\n').encode())
        if marca:
            if not leer_hasta(marca, args.timeout_s):
                print('TIMEOUT esperando', marca)
                ok = False
                break
        else:
            leer_hasta(None, 0.5)
    leer_hasta(None, 1.0)
    p.close()
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
