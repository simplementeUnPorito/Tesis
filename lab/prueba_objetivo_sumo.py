"""prueba_objetivo_sumo.py - el aprendizaje, encuentra el objetivo de SUMo?

El cero de LPo NO esta en SUMo = 0. Medido a x50/x1: LPo se anula con SUMo
cerca de -19 mV, y la etapa amplifica ~-6,6 desde ahi. A x4/x16, de la medicion
del 2026-09-25 (SUMo -28,69 mV -> LPo -3,38 mV), el cero esta en SUMo ~ -29 mV.
Con `CP_OPA_TARGET_UV` = 0 el aprendizaje apunta SUMo a CERO, o sea a ~190 mV
de donde LPo se anula: por construccion LPo queda afuera y IDAC3 tiene que
taparlo gastando casi todo su rango. De ahi sale la fragilidad.

El firmware ya tiene el remedio: si con el objetivo de fabrica LPo queda fuera
de banda, **biseca el objetivo de SUMo** anotando con que SUMo quedo LPo de
cada lado. Pero esa biseccion corre SOLO durante el aprendizaje, y en una
campana normal el perfil ya esta aprendido, asi que nunca se ejecuta. Ademas
`0x10A` se emite solo cuando el objetivo CAMBIA, asi que si no se dispara no
hay forma de saber cuanto vale: el silencio y el "no se movio" se ven igual.

Esto fuerza un re-aprendizaje mirando el mecanismo de cerca y contesta:

  1. la expansion/biseccion del objetivo, se dispara?  (clave 0x10A)
  2. si se dispara, a que valor de SUMo llega?
  3. con ese objetivo, donde queda LPo y cuanto rango le sobra a IDAC3?

Si se dispara y aterriza cerca de -29 mV, el mecanismo anda y el problema es
que el aprendizaje no se rehace por par.  Si no se dispara, el mecanismo esta
roto y hay que arreglarlo antes de medir ningun techo.

Uso:  python lab/prueba_objetivo_sumo.py --port COM8
"""
import argparse
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

CP_FINE_MID = 37
CP_OPA_TARGET_UV = 20


def _leer_param(idx):
    bt._cmd('ctl report', 0.8)
    time.sleep(1.5)
    return bt._est.get(idx)


def _set(idx, valor):
    bt._cmd('ctl set %d %d' % (idx, valor), 0.4)
    bt._cmd('ctl apply', 1.5)
    leido = _leer_param(idx)
    print('  parametro %d: se pidio %d, el nodo dice %s%s'
          % (idx, valor, leido, '' if leido == valor else '   <-- NO TOMO'))
    return leido == valor


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', default='COM8')
    ap.add_argument('--pga', type=int, default=2)
    ap.add_argument('--pgaout', type=int, default=4)
    ap.add_argument('--minutos', type=float, default=22.0)
    ap.add_argument('--fine-mid', type=int, default=240,
                    help='valor al que dejar CP_FINE_MID antes de empezar')
    ap.add_argument('--objetivo', type=int,
                    help='fijar CP_OPA_TARGET_UV (uV) antes de aprender; '
                         'sin esto se deja como esta')
    a = ap.parse_args()

    bt.PUERTO = a.port
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        print('FALLA: sin adquisicion')
        return 3

    # Lo primero: dejar CP_FINE_MID como corresponde.  La prueba anterior lo
    # movio y si murio a mitad de camino quedo en otro valor; medir sobre un
    # lazo distinto del que uno cree es la forma mas barata de perder una noche.
    print('restaurando el lazo a su configuracion conocida')
    _set(CP_FINE_MID, a.fine_mid)
    objetivo0 = _leer_param(CP_OPA_TARGET_UV)
    print('  CP_OPA_TARGET_UV actual: %s' % objetivo0)
    if a.objetivo is not None and a.objetivo != objetivo0:
        # OJO: CP_OPA_TARGET_UV esta en la lista de compatibilidad de
        # perfil, asi que cambiarlo TIRA el perfil aprendido.  Aca es lo
        # que se busca -vamos a re-aprender igual-, pero no se puede
        # hacer al descuido en medio de una campana.
        if not _set(CP_OPA_TARGET_UV, a.objetivo):
            print('FALLA: el objetivo no se pudo fijar')
            return 5
    print()

    print('entrando al par desde x1/x1 (para que el cambio sea real)')
    bt._fijar_ganancia(0, 0)
    time.sleep(45)
    bt._est.pop(bt.K_OBJETIVO, None)
    bt._fijar_ganancia(a.pga, a.pgaout)
    time.sleep(3)

    print('forzando re-aprendizaje de x%d/x%d'
          % (bt.CODIGOS[a.pga], bt.CODIGOS[a.pgaout]))
    bt._cmd('ctl learn', 1.0)
    print()
    print('  %6s %-13s %9s %10s %7s  %-20s %s'
          % ('t', 'estado', 'SUMo_mV', 'LPo_mV', 'val', 'IDAC', 'objetivo_uV'))
    t0 = time.time()
    objetivos = []
    ultimo = None
    while time.time() - t0 < a.minutos * 60 and bt._vivo:
        time.sleep(5.0)
        obj = bt._est.get(bt.K_OBJETIVO)
        if obj is not None and obj != ultimo:
            objetivos.append((round(time.time() - t0, 1), obj))
            ultimo = obj
        su = bt._est.get(bt.K_TAP + 12)
        lp = bt._est.get(bt.K_TAP + 16)
        val = bt._est.get(bt.K_TAP + 17)
        est = bt.ESTADO.get(bt._est.get(bt.K_ESTADO), '?')
        print('  %5.0fs %-13s %9s %10s %7s  %-20s %s'
              % (time.time() - t0, est,
                 '%.1f' % (su / 1000.0) if su is not None else '-',
                 '%.1f' % (lp / 1000.0) if lp is not None else '-',
                 val,
                 str([bt._est.get(bt.K_IDAC + i) for i in range(4)]),
                 obj if obj is not None else '-'), flush=True)
        if est == 'ESTABLE' and time.time() - t0 > 120:
            break

    print()
    if objetivos:
        print('LA BISECCION DEL OBJETIVO SI SE DISPARO, %d veces:'
              % len(objetivos))
        for t, o in objetivos:
            print('    a los %6.1fs -> SUMo objetivo = %+d uV (%.1f mV)'
                  % (t, o, o / 1000.0))
        print('  valor final: %+d uV' % objetivos[-1][1])
    else:
        print('LA BISECCION DEL OBJETIVO NO SE DISPARO NI UNA VEZ.')
        print('  O LPo entro en banda con el objetivo de fabrica -y entonces')
        print('  no hacia falta-, o el disparador no se cumple nunca.  Mirar')
        print('  la columna LPo de arriba para saber cual de las dos.')
    lp = bt._est.get(bt.K_TAP + 16)
    i3 = bt._est.get(bt.K_IDAC + 3)
    print()
    print('estado final: LPo=%s uV   IDAC3=%s   (rango +-255)' % (lp, i3))
    bt._vivo = False
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
