"""prueba_lazo_cerrado.py - la memoria de puntos NO abrio el lazo.

Es una compuerta, no una medicion: si falla, no se suelta ninguna campana.

La memoria de puntos de trabajo hace que el nodo arranque cerca del punto
bueno en vez de buscarlo. El riesgo de eso es sutil y silencioso: que el nodo
quede APOYADO en un valor guardado en vez de REGULANDO. Un nodo asi se ve
perfecto en el banco -esta en banda, quieto, converge rapido- y falla en campo
en cuanto cambia la temperatura, porque lo que lo tenia centrado era una tabla
y no un lazo.

La unica forma de distinguir las dos cosas es perturbarlo y ver si vuelve.

    1. llevarlo a un par conocido y esperar a que se asiente
    2. inyectar un escalon en un IDAC hasta sacar LPo de la banda
    3. NO tocar nada mas y ver si el lazo lo trae de vuelta solo

Si vuelve, el lazo esta cerrado y la tabla es lo que dice ser: una condicion
inicial. Si no vuelve, la memoria de puntos rompio el control y hay que
revertirla.

Uso:

    python lab/prueba_lazo_cerrado.py --port COM8
    python lab/prueba_lazo_cerrado.py --port COM8 --pga 6 --pgaout 6

Codigo de salida 0 si el lazo cierra, 1 si no, 3 si no se pudo ni preparar.
"""
import argparse
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

# Banda muerta del lazo (CP_DEADBAND_UV). Adentro el controlador DECIDE no
# corregir, asi que volver a estar adentro es exactamente "volvio".
BANDA_UV = 45000
# Para que el lazo despierte en modo estable hacen falta lecturas seguidas
# afuera de CP_SETTLED_BAND_UV (60 mV): si el escalon no llega ahi, no se
# estaria probando nada.
DESPIERTA_UV = 60000


def _log(msg):
    print('%s  %s' % (time.strftime('%H:%M:%S'), msg), flush=True)


def _lp():
    """LPo en uV, o None si la lectura no es valida."""
    if bt._est.get(bt.K_TAP + 17) != 1:
        return None
    return bt._est.get(bt.K_TAP + 16)


def _esperar_asentado(limite_s, banda_uv=BANDA_UV, firmes=8):
    """Espera a que LPo quede dentro de la banda y QUIETO.

    Quieto se mide por tasa sobre una ventana de tiempo explicita, no
    comparando contra la lectura anterior: entre dos vueltas del lazo LPo no
    cambia y ese criterio degenera en 'esperar una vuelta'."""
    fin = time.time() + limite_s
    seguidas = 0
    while time.time() < fin and bt._vivo:
        v = _lp()
        if v is not None and abs(v) <= banda_uv:
            seguidas += 1
            if seguidas >= firmes:
                return v
        else:
            seguidas = 0
        time.sleep(2.0)
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port')
    ap.add_argument('--pga', type=int, default=0, help='codigo 0..8 (def. x1)')
    ap.add_argument('--pgaout', type=int, default=0)
    ap.add_argument('--etapa', type=int, default=3,
                    help='IDAC a perturbar (def. 3, el fino)')
    ap.add_argument('--asentar', type=int, default=300,
                    help='segundos para asentarse antes de perturbar')
    ap.add_argument('--recuperar', type=int, default=420,
                    help='segundos que se le dan para volver')
    args = ap.parse_args(argv)

    bt.PUERTO = args.port or bt._detectar_puerto()
    _log('puerto: %s' % bt.PUERTO)
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        _log('sin adquisicion valida: no se puede probar nada')
        return 3

    if not bt._fijar_ganancia(args.pga, args.pgaout):
        _log('el nodo no confirmo x%d/x%d' %
             (bt.CODIGOS[args.pga], bt.CODIGOS[args.pgaout]))
        return 3

    _log('esperando a que se asiente (hasta %d s)...' % args.asentar)
    lp0 = _esperar_asentado(args.asentar)
    if lp0 is None:
        _log('NO se asento: la prueba no aplica, el nodo no estaba en banda')
        return 3
    idac0 = [bt._est.get(bt.K_IDAC + i) for i in range(4)]
    _log('asentado: LPo=%.1f mV  IDAC=%s' % (lp0 / 1000.0, idac0))

    # --- escalon ---------------------------------------------------------
    # El paso se BUSCA en vez de fijarlo: la pendiente de IDAC3 cambia hasta
    # 25x segun el punto de trabajo (0,6 a 15 mV/codigo, medido 2026-09-18),
    # asi que un numero fijo o no saca a LPo de la banda o lo tira contra el
    # riel. Se agranda hasta que LPo realmente sale, y nada mas.
    base = idac0[args.etapa]
    if base is None:
        _log('no hay lectura del IDAC %d' % args.etapa)
        return 3
    movido = None
    for paso in (20, 40, 80, 140, 200):
        for signo in (1, -1):
            code = max(-255, min(255, base + signo * paso))
            if code == base:
                continue
            bt._cmd('idac %d %d' % (args.etapa, code), 0.5)
            time.sleep(4.0)
            # VERIFICAR que el escalon llego.  Hasta el 2026-09-26 el comando
            # manual escribia el DAC sin avisarle al lazo, y el PI reescribia
            # su propio valor en el tick siguiente: la inyeccion se deshacia en
            # ~3 s y la telemetria nunca la mostraba.  Esta prueba reportaba
            # "perturbe y el lazo volvio solo" sin haber perturbado nada, que
            # es peor que no tener prueba.
            leido = bt._est.get(bt.K_IDAC + args.etapa)
            if leido != code:
                _log('  !! se pidio IDAC%d=%d y el nodo dice %s: el escalon NO '
                     'llego, no hay nada que probar' % (args.etapa, code, leido))
                return 4
            time.sleep(4.0)
            v = _lp()
            fuera = v is None or abs(v) > DESPIERTA_UV
            _log('  escalon IDAC%d: %d -> %d (confirmado)   LPo=%s'
                 % (args.etapa, base, code,
                    'INVALIDO' if v is None else '%.1f mV' % (v / 1000.0)))
            if fuera:
                movido = code
                break
        if movido is not None:
            break
    if movido is None:
        _log('FALLA: ningun escalon saco a LPo de la banda. O el actuador no '
             'tiene autoridad en este punto, o la lectura no responde: en los '
             'dos casos la prueba no puede afirmar que el lazo cierre.')
        return 1

    # --- y ahora no se toca nada mas -------------------------------------
    _log('perturbado. A partir de aca NO se toca nada: se mira si vuelve '
         '(hasta %d s).' % args.recuperar)
    t0 = time.time()
    lp1 = _esperar_asentado(args.recuperar)
    dt = time.time() - t0
    idac1 = [bt._est.get(bt.K_IDAC + i) for i in range(4)]

    if lp1 is None:
        _log('')
        _log('FALLA: el lazo NO trajo a LPo de vuelta en %d s.' % args.recuperar)
        _log('       LPo final=%s  IDAC=%s' %
             (_lp(), idac1))
        _log('       El nodo estaba APOYADO en el punto guardado, no regulando.')
        _log('       No soltar la campana: revertir la memoria de puntos.')
        return 1

    _log('')
    _log('PASA: volvio a %.1f mV en %.0f s sin que nadie lo tocara.'
         % (lp1 / 1000.0, dt))
    _log('      IDAC antes=%s  despues=%s' % (idac0, idac1))
    _log('      El lazo esta cerrado: la tabla es condicion inicial, no muleta.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
