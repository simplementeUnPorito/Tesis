"""Lleva la cadena a una ganancia y espera que el lazo calibre (sin capturar).

Sirve para dejar el nodo listo antes de medir con el geofono conectado.

  python lab/calibrar_campo.py --port COM8 [--pga 3 --pgaout 4] [--max-s 600]
"""
import argparse
import os
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt  # noqa: E402
from lab import ruido_sd as rs       # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', default='COM8')
    ap.add_argument('--pga', type=int, default=3)
    ap.add_argument('--pgaout', type=int, default=4)
    ap.add_argument('--max-s', type=int, default=600)
    args = ap.parse_args(argv)
    bt.PUERTO = args.port
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        rs._log('sin adquisicion valida')
        return 3
    rs._log('x%d/x%d: calibrando...' % (bt.CODIGOS[args.pga], bt.CODIGOS[args.pgaout]))
    visita = rs._esperar_convergencia(args.pga, args.pgaout, args.max_s, latido_s=30.0)
    if visita is None:
        rs._log('NO CALIBRO')
        return 1
    _, t_banda, _, _, _ = visita
    foto = bt._foto()
    rs._log('CALIBRADO: en banda a %.0f s; estado=%s, taps=%s uV, idac=%s' % (
        t_banda, bt.ESTADO.get(foto.get('estado'), foto.get('estado')),
        foto.get('tap'), foto.get('idac')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
