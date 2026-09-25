"""diag_ganancia_alta.py - por que no se llega a ganancia > 50.

No decide nada: mira. Fija un par y sigue SUMo, LPo y los cuatro IDAC durante
varios minutos, imprimiendo la trayectoria. Contesta tres preguntas que el
barrido no puede contestar porque corta antes:

  1. LPo, ¿esta fuera de ventana de verdad, o entra despues de los 60 s que
     usa la guarda de INMEDIBLE?  Con tau ~ 30-44 s, 60 s son 1,5 constantes
     de tiempo: puede estar cortando pares que si convergen.
  2. ¿Que riela primero, SUMo o LPo?  Si es SUMo, el problema es el par lento
     (aguas arriba) y no PGAout.
  3. ¿El lazo se esta MOVIENDO?  Unos IDAC quietos con el tap afuera es un
     lazo sin autoridad; unos IDAC moviendose es un lazo que todavia busca.

Uso:

    python lab/diag_ganancia_alta.py --port COM8 --pares 2,3 2,4 2,5
    (los pares son codigos: 2=x4, 3=x8, 4=x16, 5=x24)
"""
import argparse
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

TAPS = {'SEo': 0, 'BP': 1, 'OPAs': 2, 'SUM': 3, 'LP': 4}
VENTANA_MV = 97.0


def _tap(i):
    v = bt._est.get(bt.K_TAP + 4 * i)
    ok = bt._est.get(bt.K_TAP + 4 * i + 1)
    return (v / 1000.0 if v is not None else None), ok


def seguir(pga, pgaout, minutos, paso=4.0):
    print('\n=== x%d / x%d   (ganancia %d) ==='
          % (bt.CODIGOS[pga], bt.CODIGOS[pgaout],
             bt.CODIGOS[pga] * bt.CODIGOS[pgaout]), flush=True)
    if not bt._fijar_ganancia(pga, pgaout):
        print('  el nodo no confirma la ganancia'); return
    t0 = time.time()
    print('  %6s %9s %9s %9s %9s  %-18s %s'
          % ('t', 'SEo', 'BPo', 'SUMo', 'LPo', 'IDAC', 'estado'))
    en_ventana = None
    while time.time() - t0 < minutos * 60 and bt._vivo:
        fila = []
        for n in ('SEo', 'BP', 'SUM', 'LP'):
            v, ok = _tap(TAPS[n])
            fila.append('%8.1f%s' % (v, '*' if ok != 1 else ' ')
                        if v is not None else '     -   ')
        idac = [bt._est.get(bt.K_IDAC + i) for i in range(4)]
        est = bt.ESTADO.get(bt._est.get(bt.K_ESTADO), '?')
        lp, lpok = _tap(TAPS['LP'])
        if lpok == 1 and lp is not None and abs(lp) <= VENTANA_MV and en_ventana is None:
            en_ventana = time.time() - t0
        print('  %5.0fs %s  %-18s %s'
              % (time.time() - t0, ' '.join(fila), str(idac), est), flush=True)
        time.sleep(paso)
    print('  -> LPo entro en ventana a los %s'
          % ('%.0f s' % en_ventana if en_ventana is not None else 'NUNCA'))
    print('     (* = lectura fuera de la ventana de validez del ADC)')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port')
    ap.add_argument('--pares', nargs='+', required=True,
                    help='codigos pga,pgaout (0=x1 1=x2 2=x4 3=x8 4=x16 5=x24 6=x32 7=x48 8=x50)')
    ap.add_argument('--minutos', type=float, default=6.0)
    a = ap.parse_args()

    bt.PUERTO = a.port or bt._detectar_puerto()
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        print('sin adquisicion valida'); return 3
    for t in a.pares:
        x, y = t.split(',')
        seguir(int(x), int(y), a.minutos)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
