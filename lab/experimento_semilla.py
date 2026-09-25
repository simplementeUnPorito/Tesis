"""experimento_semilla.py - mide si la memoria de puntos sirve, y desde donde.

La pregunta que contesta NO es "cuanto tarda el nodo en converger". Es:

    cuando el nodo arranca desde un punto guardado, ¿converge porque la
    semilla sirvio, o porque ya venia bien encaminado?

Esa diferencia no se puede ver en un barrido comun, porque cada par hereda el
estado del anterior. Por eso cada candidato se mide en TRES condiciones de
entrada distintas y, ademas, contra un BRAZO DE CONTROL con la memoria
apagada:

  | condicion   | como se prepara                        | que aisla            |
  |-------------|----------------------------------------|----------------------|
  | FRIO        | psocreset por GPIO19 y esperar el boot | el arranque real     |
  | DESDE_X1    | pasar por x1/x1 y dejar asentar        | venir de ganancia 1  |
  | DESDE_ALTA  | pasar por x32/x32 y dejar asentar      | venir de ganancia alta |

  | brazo      | politica | que mide                                        |
  |------------|----------|-------------------------------------------------|
  | MEMORIA    | 1..3     | la cascada de seleccion de puntos               |
  | CONTROL    | 0        | el firmware como estaba antes: sin esto no hay  |
  |            |          | con que comparar y cualquier mejora es un relato |

Cada visita se anexa a `resultados.jsonl` apenas termina, asi que cortar el
experimento no cuesta ninguna medicion ya hecha. Reanudar saltea las
combinaciones (par, condicion, brazo, vuelta) que ya estan en el archivo.

Uso:

    python lab/experimento_semilla.py --port COM8 --sembrar
    python lab/experimento_semilla.py --port COM8 --reanudar

Se detiene solo, y sin perder nada, con Ctrl-C, con SIGTERM, o creando el
archivo `.run/STOP` dentro del directorio de salida.
"""
import argparse
import json
import os
import signal
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

# Par intermedio de "ganancia alta" para la tercera condicion. Se elige x32/x32
# porque la fila de PGA x32 es la de mejor cobertura del historico (8 de 9
# pares con punto conocido), o sea que preparar la condicion casi nunca falla
# y lo que se mide es el par objetivo, no el intermedio.
# Par intermedio de "ganancia alta".  Fue x32/x32 y se cambio el 2026-09-25:
# ese par resulto INMEDIBLE (LPo fuera de ventana), o sea que la condicion
# DESDE_ALTA ni siquiera se establecia y producia una sola visita util de cada
# seis.  x48/x1 es el de MAYOR ganancia que hoy mide bien, y ademas la
# ganancia alta la pone el PGA -que es el que carga el acople de 680 uF- en
# vez del PGAout, que es lo que rielaba LPo.
PAR_ALTO = (7, 0)                            # codigos, = x48 / x1
PAR_BAJO = (0, 0)                            # codigos, = x1 / x1

CONDICIONES = ('FRIO', 'DESDE_X1', 'DESDE_ALTA')

# Muestras del sondeo previo, a 2 s cada una.  150 = 300 s, que cubre con
# holgura los ~250 s que tarda x4/x16 en aterrizar.  Se corta apenas LPo
# responde, asi que un par sano no paga esta espera.
# Cuanto se le da a LPo para dar senales de vida ANTES de declararlo
# inmedible, dentro de la misma ventana de medicion.  Con 60 s se
# condenaba a x4/x16 -el unico par con ganancia 64 demostrada-, que
# tarda ~250 s en aterrizar.  Los 23 INMEDIBLE de ganancia 100 a 200
# del 2026-09-25 midieron mi impaciencia, no el techo del circuito.
# El corte exige las DOS cosas: LPo sin responder Y los IDAC quietos.
SONDEO_S = 300.0

SALIDA_POR_OMISION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'experimento_semilla_%s' % time.strftime('%Y%m%d'))


# --------------------------------------------------------------- utilidades

def _log(msg):
    print('%s  %s' % (time.strftime('%H:%M:%S'), msg), flush=True)


def _politica(valor, intentos=4):
    """Fija la politica y COMPRUEBA que quedo, leyendola de vuelta.

    No alcanza con mandarla.  `CP_PUNTO_POLICY` es config persistida con valor
    de fabrica 2, y un `psocreset` la devuelve a 2: si la condicion FRIO
    resetea despues de fijarla, el brazo de CONTROL mide con la memoria
    ENCENDIDA y la referencia del experimento deja de ser referencia.
    Medido el 2026-09-24: el brazo de control salia con origen PUNTO_EEPROM.

    No pasa por `ctl apply`: un apply reinicia el lazo y tirar el punto de
    trabajo en el medio de un experimento contaminaria la visita siguiente."""
    for _ in range(intentos):
        bt._est.pop(bt.K_POLITICA, None)
        bt._cmd('ctl punto policy %d' % valor, 0.4)
        bt._cmd('ctl report', 0.6)
        for _ in range(10):
            leido = bt._est.get(bt.K_POLITICA)
            if leido == valor:
                return True
            time.sleep(0.3)
    _log('    !! la politica NO quedo en %d (lee %s)'
         % (valor, bt._est.get(bt.K_POLITICA)))
    return False


def _sembrar(archivo, incluir_fragiles=False):
    """Carga la tabla de puntos con lo ya medido en campanas anteriores.

    Devuelve la lista de pares sembrados, en el orden en que conviene
    medirlos."""
    with open(archivo, encoding='utf-8') as fh:
        datos = json.load(fh)
    puntos = datos['puntos']
    if not incluir_fragiles:
        puntos = [p for p in puntos if not p.get('fragil')]
    _log('sembrando %d puntos desde %s' % (len(puntos), archivo))
    ok = 0
    for p in puntos:
        c = p['codes']
        bt._cmd('ctl punto %d %d %d %d %d'
                % (p['par'], c[0], c[1], c[2], c[3]), 0.5)
        ok += 1
    _log('sembrados %d puntos' % ok)
    return puntos


def _preparar(condicion, espera_s):
    """Deja el banco en la condicion de entrada pedida.

    Devuelve el par en el que quedo el nodo, o None si la condicion no se
    pudo establecer -en ese caso la visita se saltea: medir sobre una
    condicion que no es la que dice la etiqueta es peor que no medir-.

    Las tres condiciones dejan el nodo en un par CONCRETO, incluida FRIO.
    Antes FRIO solo resetaba y esperaba, y el nodo arrancaba en el par que
    tenia guardado en el perfil: si ese par era justo el que se iba a
    medir, no habia cambio de ganancia, el firmware no emitia el evento
    del punto -o sea, la politica de puntos no se ejercia- y el cronometro
    arrancaba sobre algo ya asentado.  Se vio en la primera visita:
    PASA nota A con t_estable = 2,0 s y origen vacio.  Eso no es un pase,
    es un no-evento.

    Lo que distingue a FRIO no es entonces de donde viene, sino que viene
    con la RAM en blanco: el reset borra el pool de candidatos y deja solo
    lo que sobrevive en EEPROM.  Esa es justamente la diferencia que la
    condicion existe para medir."""
    if condicion == 'FRIO':
        bt._reset_psoc_desde_esp()
        # El firmware auto-calibra al arrancar; entrar antes de que termine
        # mide el transitorio de la calibracion, no el arranque.
        time.sleep(30)
        if not bt._asegurar_adquisicion():
            return None
        par = PAR_BAJO
    else:
        par = PAR_BAJO if condicion == 'DESDE_X1' else PAR_ALTO
    if not bt._fijar_ganancia(par[0], par[1]):
        return None
    # Esperar varias constantes de tiempo del acople de 680 uF (tau ~ 30-44 s).
    # Sin esta espera la "condicion de entrada" seria un transitorio y las tres
    # condiciones terminarian pareciendose entre si.
    fin = time.time() + espera_s
    while time.time() < fin and bt._vivo:
        time.sleep(1.0)
    return par if bt._vivo else None


def _stop_pedido(salida):
    return os.path.exists(os.path.join(salida, '.run', 'STOP'))


# ------------------------------------------------------------------- campana

def _plan(puntos, pares_extra, vueltas, politica, explicito=False):
    """Orden explicito de las visitas.

    Primero lo sembrado -que es la hipotesis a validar-, y los pares sin punto
    conocido al FINAL: si la noche se corta, se corta en lo menos valioso."""
    items = []
    sembrados = [(p['pga_cod'], p['pgaout_cod']) for p in puntos]
    # Por GANANCIA, no por indice de par.  Dos razones:
    #
    # 1. Lo informativo esta en la ganancia alta -ahi es donde la busqueda a
    #    ciegas no encuentra la ventana-, asi que va PRIMERO: si la noche se
    #    corta, se corta en lo que menos importa.
    # 2. Recorrer siempre en el mismo sentido ata la ganancia a la HORA: las
    #    bajas se medirian siempre temprano y las altas siempre de madrugada,
    #    y un efecto termico se leeria como efecto de ganancia.  Invirtiendo
    #    el sentido en cada vuelta, cada par cae en dos momentos distintos de
    #    la noche y la temperatura se ve como diferencia DENTRO del par.
    # Con una lista EXPLICITA se respeta el orden dado: si alguien la escribe
    # a mano es porque quiere medir algo primero -tipicamente el control
    # positivo, el par que ya se sabe que anda-.  Reordenar por ganancia lo
    # mandaba al final, que es donde no sirve si la campana se corta.
    ganancia = lambda pr: bt.CODIGOS[pr[0]] * bt.CODIGOS[pr[1]]
    for vuelta in range(1, vueltas + 1):
        if explicito:
            orden = sembrados if vuelta % 2 == 1 else list(reversed(sembrados))
        else:
            orden = sorted(sembrados, key=ganancia, reverse=(vuelta % 2 == 1))
        for par in orden + pares_extra:
            for condicion in CONDICIONES:
                for brazo, pol in (('MEMORIA', politica), ('CONTROL', 0)):
                    items.append((vuelta, par, condicion, brazo, pol))
    return items


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', help='puerto serie (por omision autodetecta)')
    ap.add_argument('--output', default=SALIDA_POR_OMISION)
    ap.add_argument('--semilla', default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'semilla_puntos.json'))
    ap.add_argument('--sembrar', action='store_true',
                    help='carga la tabla de puntos antes de medir')
    ap.add_argument('--incluir-fragiles', action='store_true',
                    help='siembra tambien los puntos con IDAC3 contra el tope')
    ap.add_argument('--politica', type=int, default=2,
                    help='0 off, 1 unico, 2 vecino, 3 interpolado (def. 2)')
    ap.add_argument('--vueltas', type=int, default=1)
    ap.add_argument('--ventana', type=int, default=240)
    ap.add_argument('--espera-contexto', type=int, default=60,
                    help='segundos de asentamiento del par intermedio')
    ap.add_argument('--reanudar', action='store_true')
    ap.add_argument('--huerfanos', action='store_true',
                    help='mide tambien los pares sin punto conocido, al final')
    ap.add_argument('--pares', nargs='+',
                    help='lista explicita pga,pgaout (codigos) en vez de la '
                         'semilla; sirve para apuntar al cuadrante util')
    args = ap.parse_args(argv)

    os.makedirs(os.path.join(args.output, '.run'), exist_ok=True)
    crudo = os.path.join(args.output, 'resultados.jsonl')

    bt.PUERTO = args.port or bt._detectar_puerto()
    _log('puerto: %s' % bt.PUERTO)
    threading.Thread(target=bt._leer, daemon=True).start()
    signal.signal(signal.SIGINT, bt._pedir_salida)
    try:
        signal.signal(signal.SIGTERM, bt._pedir_salida)
    except (AttributeError, ValueError):
        pass
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        _log('sin adquisicion valida al arrancar: se aborta')
        return 3

    with open(args.semilla, encoding='utf-8') as fh:
        datos = json.load(fh)
    if args.pares:
        # Lista explicita: se apunta al cuadrante donde HOY se puede medir, en
        # vez de al que la semilla historica sugeria.  Medido el 2026-09-25:
        # con PGAout >= x8 el 93 % de las visitas salen con LPo fuera de
        # ventana, y con PGA >= x32 el que se riela es SUMo.
        puntos = []
        for t in args.pares:
            a, b = (int(x) for x in t.split(','))
            puntos.append({'pga_cod': a, 'pgaout_cod': b,
                           'pga': bt.CODIGOS[a], 'pgaout': bt.CODIGOS[b],
                           'par': a * 9 + b, 'codes': None, 'fragil': False})
    else:
        puntos = [p for p in datos['puntos']
                  if args.incluir_fragiles or not p.get('fragil')]
    if not args.pares:
        puntos.sort(key=lambda p: p['par'])

    pares_extra = []
    if args.huerfanos:
        sembrados = {(p['pga_cod'], p['pgaout_cod']) for p in datos['puntos']}
        pares_extra = [(a, b) for a in range(9) for b in range(9)
                       if (a, b) not in sembrados]

    hechas = set()
    if args.reanudar and os.path.exists(crudo):
        for r in bt._cargar(crudo):
            hechas.add((r.get('vuelta'), r.get('pga_cod'), r.get('pgaout_cod'),
                        r.get('condicion'), r.get('brazo')))
        _log('reanudando: %d visitas ya medidas' % len(hechas))

    if args.sembrar:
        _politica(0)          # sembrar sin que la cascada mueva nada
        _sembrar(args.semilla, args.incluir_fragiles)

    plan = _plan(puntos, pares_extra, args.vueltas, args.politica,
                 explicito=bool(args.pares))
    _log('plan: %d visitas (%d pares sembrados, %d huerfanos, %d vueltas)'
         % (len(plan), len(puntos), len(pares_extra), args.vueltas))

    hecho = 0
    # NO se saltean las otras combinaciones de un par que dio INMEDIBLE.
    # Se probo y se revirtio el 2026-09-25: saltear generaliza de UNA condicion
    # a las seis, y la premisa del experimento es justamente que la condicion
    # de entrada cambia donde aterriza la cadena.  Un par inmedible en frio
    # puede ser medible viniendo de x1/x1, y saltando nunca se sabria.  El
    # ahorro ya lo da la deteccion rapida: 60 s en vez de 960.
    for vuelta, (pga, pgaout), condicion, brazo, pol in plan:
        # "Venir de x1/x1" hacia x1/x1 no es una transicion: la preparacion
        # deja el nodo donde ya esta, `_fijar_ganancia` no dispara ningun
        # cambio de ganancia y la visita mide sin que nada se reinicialice.
        # Medirla seria inventar una condicion que no existe.
        if ((condicion == 'DESDE_X1' and (pga, pgaout) == PAR_BAJO) or
                (condicion == 'DESDE_ALTA' and (pga, pgaout) == PAR_ALTO)):
            continue
        if not bt._vivo or _stop_pedido(args.output):
            _log('parada pedida: se cierra sin perder lo ya escrito')
            break
        clave = (vuelta, pga, pgaout, condicion, brazo)
        if clave in hechas:
            continue

        _log('--- v%d  x%d/x%d  %s  %s (politica %d)'
             % (vuelta, bt.CODIGOS[pga], bt.CODIGOS[pgaout],
                condicion, brazo, pol))
        # La politica se fija DESPUES de preparar: la preparacion de FRIO es un
        # psocreset, y el reset devuelve la politica a su valor de fabrica.
        # Fijarla antes era fijarla y perderla.
        # Toda la preparacion va dentro de la red: si el USB se re-enumera
        # aca -y en ocho horas se re-enumera- antes moria main() con la
        # campana a medio hacer.  Ahora se pierde ESTA visita y sigue.
        reconex0 = bt._reconexiones
        try:
            par_previo = _preparar(condicion, args.espera_contexto)
            if par_previo is None:
                _log('    !! no se pudo establecer la condicion: se saltea')
                continue
            if par_previo == (pga, pgaout):
                # Sin cambio de ganancia no hay nada que medir: el
                # firmware no emite el punto y el cronometro arranca
                # sobre una etapa ya asentada.
                _log('    !! el par de entrada es el mismo que se va a '
                     'medir: se saltea')
                continue
            if not _politica(pol):
                _log('    !! sin politica confirmada no se mide: se saltea')
                continue
        except (RuntimeError, bt.TelemetriaVencida) as e:
            _log('    !! preparando: %s; se saltea la visita' % e)
            continue
        if not bt._vivo or _stop_pedido(args.output):
            break

        # `_visitar` devuelve la serie cruda; el diccionario de la visita lo
        # arma `_analizar`, igual que en barrido_total.main().
        try:
            for intento in range(1, 4):
                try:
                    serie, t_banda, lp0, n0, ok = bt._visitar(
                        pga, pgaout, args.ventana, sondeo_s=SONDEO_S)
                    break
                except bt.TelemetriaVencida as e:
                    if intento == 3:
                        raise
                    _log('    !! %s; reintento %d/2' % (e, intento))
                    bt._reset_psoc_desde_esp()
                    time.sleep(30)
                    bt._asegurar_adquisicion()
            visita = bt._analizar(pga, pgaout, serie, t_banda, lp0, n0,
                                  args.ventana, ok)
        except bt.Inmedible as e:
            # Tiene que ir ANTES del except generico: Inmedible hereda de
            # RuntimeError.  Y es un RESULTADO -acota la ganancia usable-,
            # asi que se escribe, no se descarta.
            _log('    INMEDIBLE: LPo valido %d veces y los IDAC no se '
                 'movieron en %.0f s' % (e.validas, e.segundos))
            with open(crudo, 'a', encoding='utf-8') as fh:
                fh.write(json.dumps({
                    'marca': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'pga_cod': pga, 'pgaout_cod': pgaout,
                    'pga': bt.CODIGOS[pga], 'pgaout': bt.CODIGOS[pgaout],
                    'ganancia': bt.CODIGOS[pga] * bt.CODIGOS[pgaout],
                    'vuelta': vuelta, 'condicion': condicion,
                    'brazo': brazo, 'politica_pedida': pol,
                    'par_previo': '%d/%d' % (bt.CODIGOS[par_previo[0]],
                                             bt.CODIGOS[par_previo[1]]),
                    'politica_puntos': bt._est.get(bt.K_POLITICA),
                    'veredicto': 'INMEDIBLE',
                    'veredicto_estricto': 'INMEDIBLE',
                    'sondeo_s': e.segundos,
                    'sondeo_validas': e.validas,
                    'movimientos_idac': e.movimientos,
                    'origen': bt.ORIGEN.get(bt._est.get(bt.K_ORIGEN)),
                    'idac_final': [bt._est.get(bt.K_IDAC + i)
                                   for i in range(4)],
                }, ensure_ascii=False) + chr(10))
                fh.flush()
                os.fsync(fh.fileno())
            hecho += 1
            continue
        except (RuntimeError, bt.TelemetriaVencida) as e:
            _log('    !! %s' % e)
            continue
        if bt._reconexiones != reconex0:
            # El puerto se cayo y volvio en medio de la medicion.  El ESP
            # arranco de cero ahi adentro: la serie mezcla dos vidas del
            # nodo y el t_estable no significa nada.  Se descarta la
            # visita en vez de guardar un numero sin dueno.
            _log('    !! reconexion de %s durante la visita: se descarta'
                 % bt.PUERTO)
            try:
                bt._asegurar_adquisicion()
            except (RuntimeError, bt.TelemetriaVencida):
                pass
            continue
        # Sin marca de tiempo no se puede cruzar la visita con la temperatura
        # ambiente ni separar la deriva termica de la ganancia, que es la
        # mitad del sentido de correr esto de noche.
        visita['marca'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        visita['vuelta'] = vuelta
        visita['condicion'] = condicion
        visita['brazo'] = brazo
        visita['politica_pedida'] = pol
        visita['par_previo'] = '%d/%d' % (bt.CODIGOS[par_previo[0]],
                                         bt.CODIGOS[par_previo[1]])
        visita['par_intermedio'] = ('%d/%d' % (bt.CODIGOS[PAR_ALTO[0]],
                                               bt.CODIGOS[PAR_ALTO[1]])
                                    if condicion == 'DESDE_ALTA' else
                                    '%d/%d' % (bt.CODIGOS[PAR_BAJO[0]],
                                               bt.CODIGOS[PAR_BAJO[1]])
                                    if condicion == 'DESDE_X1' else None)
        with open(crudo, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(visita, ensure_ascii=False) + '\n')
            fh.flush()
            os.fsync(fh.fileno())
        hecho += 1
        _log('    %s / %s  nota=%s  origen=%s  t_estable=%s  residuo=%s'
             % (visita.get('veredicto'), visita.get('veredicto_estricto'),
                visita.get('nota'), visita.get('origen'),
                visita.get('t_estable_s'), visita.get('residuo')))

    _log('terminado: %d visitas nuevas en %s' % (hecho, crudo))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
