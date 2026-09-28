"""experimento_ruido.py - cuanto ruido AGREGAN la SD y la radio, y si depende
de la ganancia.

El firmware ya sabe que la SD mete espigas: en `main.cpp` esta escrito que su
drenaje "escribe un sector cada 57,6 ms durante el muestreo y cada escritura
mete una espiga en la senial". Lo que NO esta medido es cuanto, con que forma
espectral, y sobre todo **si depende de la ganancia**, que es la pregunta que
dice DONDE se acopla:

  * si el ruido entra ANTES del PGA, escala con la ganancia igual que la
    senial y el impacto en la relacion senial/ruido es constante;
  * si entra DESPUES (referencia del ADC, nodo sumador), referido a la entrada
    BAJA al subir la ganancia.

Medir el RMS referido a la entrada contra la ganancia distingue esos dos casos.
Es mucho mas util que un "si, depende".

## Como esta armado

La captura es siempre la ruta LIMPIA que queda en RAM (hasta 512 lotes, ~5,8 s)
y se vuelca despues por USB con `dumpusb`. Eso es deliberado: la captura tiene
que estar libre de radio, y leer los datos por ESP-NOW la contaminaria. La
lectura puede ser sucia porque ocurre DESPUES.

La SD y la radio entran como estresores controlados en paralelo (`sdstress`,
`rftest`), no como camino de datos. Asi las cuatro condiciones difieren en UNA
sola cosa:

    BASE     nada                      SD       escrituras a la SD
    RF       trafico ESP-NOW           SD_RF    las dos

## Por que ABBA y no A-despues-B

El acople de 680 uF tiene tau ~ 30-44 s y la placa deriva. Medir todas las A y
despues todas las B mezcla la diferencia entre condiciones con la deriva del
tiempo. Cada bloque se corre hacia adelante y hacia atras (A B C D D C B A),
que cancela la deriva lineal.

## Uso

    python lab/experimento_ruido.py --port COM8 --pares 0,0 6,6 --repeticiones 3
    python lab/analisis_ruido.py lab/ruido_<fecha>          (no abre el puerto)

El modo `--piso` mide el piso de ruido ABSOLUTO del instrumento y EXIGE que la
entrada este terminada o en corto. Es una intervencion fisica: el script se
niega a correr si no se la confirma explicitamente.
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

# Una captura de hasta PSOC_CAPTURE_MAX_BATCHES (512) lotes queda en RAM; pasado
# eso el firmware la manda SOLO a la SD del PSoC y entonces las muestras no
# pasan por el ESP y `dumpusb` no las ve.  500 deja margen.
LOTES = 500
# Para saber cuanto dura de verdad una captura: 500 lotes de 30 muestras a
# 2604 Hz son 5,76 s.  El host tiene que esperar eso antes de volcar.
MUESTRAS_POR_LOTE = 30
FS_HZ = 2604.0
MUESTRAS_POR_LOTE = 30
FS_NATIVA = 2604.0

# El drenaje real de la SD escribe un sector cada 57,6 ms.  Se usa ese periodo
# para que el estresor sea electricamente equivalente a lo que pasa en campo.
SD_PERIODO_MS = 58
# Trafico ESP-NOW con el tamanio y la cadencia del envio real de lotes.
RF_PERIODO_MS = 20
RF_BYTES = 200

CONDICIONES = ('BASE', 'SD', 'RF', 'SD_RF')

SALIDA_POR_OMISION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'ruido_%s' % time.strftime('%Y%m%d'))


def _log(msg):
    print('%s  %s' % (time.strftime('%H:%M:%S'), msg), flush=True)


# ------------------------------------------------------------------ volcado

def _volcar(timeout=180.0):
    """Pide el volcado y devuelve (cabecera, [(seq, hex), ...]).

    Lee del sumidero del hilo lector en vez de abrir el puerto de nuevo: dos
    procesos sobre el mismo adaptador se mezclan los comandos."""
    bt._sink = lineas = []
    try:
        bt._cmd('dumpusb', 0.2)
        cabecera, lotes, fin, perdidos = None, [], False, []
        limite = time.time() + timeout
        vistas = 0
        while time.time() < limite and not fin:
            while vistas < len(lineas):
                ln = lineas[vistas].strip()
                vistas += 1
                if ln.startswith('#DUMP_BEGIN'):
                    cabecera = dict(
                        p.split('=', 1) for p in ln.split()[1:] if '=' in p)
                elif ln.startswith('#DUMP '):
                    partes = ln.split()
                    if len(partes) >= 3:
                        lotes.append((int(partes[1]), partes[2]))
                elif ln.startswith('#DUMP_MISS'):
                    # El firmware no encontro ese lote en RAM. No es ruido: es
                    # un hueco, y hay que verlo como tal y no como una captura
                    # mas corta.
                    perdidos.append(ln.split()[-1])
                elif ln.startswith('#DUMP_END'):
                    fin = True
            if not fin:
                time.sleep(0.2)
        return cabecera, lotes, fin, perdidos
    finally:
        bt._sink = None


def _guardar(ruta, cabecera, lotes, meta):
    with open(ruta, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps({'meta': meta, 'cabecera': cabecera}) + '\n')
        for seq, hx in lotes:
            fh.write('%d %s\n' % (seq, hx))
        fh.flush()
        os.fsync(fh.fileno())


# --------------------------------------------------------------- estresores

def _estresor(condicion, ms):
    """Arranca los estresores de la condicion. No bloquean: corren en el
    `loop()` del ESP mientras la captura pasa."""
    if condicion in ('SD', 'SD_RF'):
        bt._cmd('sdstress %d %d' % (ms, SD_PERIODO_MS), 0.3)
    if condicion in ('RF', 'SD_RF'):
        bt._cmd('rftest %d %d %d' % (ms, RF_PERIODO_MS, RF_BYTES), 0.3)


def _cortar_estresores():
    bt._cmd('sdstress 0 0', 0.2)
    bt._cmd('rftest 0 0 0', 0.2)


# ------------------------------------------------------------------ campana

def _una_corrida(par, condicion, rep, salida, meta_extra):
    pga, pgaout = par
    dur_ms = int((LOTES * MUESTRAS_POR_LOTE / FS_NATIVA) * 1000) + 4000
    nombre = 'p%d%d_%s_r%d.txt' % (pga, pgaout, condicion, rep)
    ruta = os.path.join(salida, nombre)
    if os.path.exists(ruta):
        return 'ya estaba'

    _estresor(condicion, dur_ms)
    t0 = time.time()
    # `capwait` bloquea en el firmware hasta que la captura termina.  La
    # captura PAUSA el lazo de control por si sola (control_prepare_capture),
    # asi que las cuatro condiciones lo tienen pausado igual y esa no es una
    # variable del experimento.
    # `capwait` bloquea EN EL FIRMWARE, pero `_cmd` no espera respuesta: manda
    # y duerme lo que se le diga.  Con 0,5 s el host volcaba cuando iban 5
    # lotes de 500 y las veinte corridas fallaban en 30 segundos (2026-09-28).
    # Hay que esperar lo que la captura REALMENTE tarda, mas margen.
    _dur = LOTES * MUESTRAS_POR_LOTE / float(FS_HZ)
    bt._cmd('capwait %d' % LOTES, _dur + 3.0)
    t_cap = time.time() - t0
    _cortar_estresores()

    cabecera, lotes, completo, perdidos = _volcar()
    if perdidos:
        return 'el firmware no tenia %d lotes en RAM (%s...)' % (
            len(perdidos), ','.join(perdidos[:5]))
    if not completo or not lotes:
        return 'volcado incompleto (%d lotes)' % len(lotes)
    # Si el firmware devolvio menos lotes de los pedidos, la captura no se
    # completo y el RMS saldria de un pedazo distinto en cada condicion.
    if len(lotes) < LOTES:
        return 'captura corta: %d de %d lotes' % (len(lotes), LOTES)

    meta = dict(meta_extra)
    meta.update({'pga_cod': pga, 'pgaout_cod': pgaout,
                 'pga': bt.CODIGOS[pga], 'pgaout': bt.CODIGOS[pgaout],
                 'condicion': condicion, 'repeticion': rep,
                 'lotes': len(lotes), 'segundos_captura': round(t_cap, 1),
                 'marca': time.strftime('%Y-%m-%dT%H:%M:%S'),
                 'sd_periodo_ms': SD_PERIODO_MS,
                 'rf_periodo_ms': RF_PERIODO_MS, 'rf_bytes': RF_BYTES})
    _guardar(ruta, cabecera, lotes, meta)
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port')
    ap.add_argument('--output', default=SALIDA_POR_OMISION)
    ap.add_argument('--pares', nargs='+', default=['0,0'],
                    help='codigos pga,pgaout separados por coma')
    ap.add_argument('--repeticiones', type=int, default=3)
    ap.add_argument('--asentar', type=int, default=90,
                    help='segundos de asentamiento tras cambiar de ganancia')
    ap.add_argument('--piso', action='store_true',
                    help='mide el piso ABSOLUTO; exige la entrada terminada')
    ap.add_argument('--entrada-terminada', action='store_true',
                    help='confirma fisicamente que la entrada esta en corto')
    args = ap.parse_args(argv)

    if args.piso and not args.entrada_terminada:
        print('El piso de ruido absoluto NO se puede medir con el geofono\n'
              'conectado: lo que mide es el movimiento del suelo mas el\n'
              'instrumento. Termina o cortocircuita la entrada y volve a\n'
              'correr con --entrada-terminada.\n'
              'Para medir solo cuanto AGREGAN la SD y la radio no hace falta:\n'
              'el par intercalado ABBA cancela lo que haga el geofono.',
              file=sys.stderr)
        return 2

    pares = []
    for t in args.pares:
        a, b = t.split(',')
        pares.append((int(a), int(b)))

    os.makedirs(args.output, exist_ok=True)
    bt.PUERTO = args.port or bt._detectar_puerto()
    _log('puerto: %s' % bt.PUERTO)
    threading.Thread(target=bt._leer, daemon=True).start()
    signal.signal(signal.SIGINT, bt._pedir_salida)
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        _log('sin adquisicion valida: se aborta')
        return 3

    meta_extra = {'modo': 'piso' if args.piso else 'delta',
                  'entrada_terminada': bool(args.entrada_terminada)}

    hechas = saltadas = 0
    for par in pares:
        if not bt._vivo:
            break
        _log('=== par x%d/x%d ===' % (bt.CODIGOS[par[0]], bt.CODIGOS[par[1]]))
        if not bt._fijar_ganancia(par[0], par[1]):
            _log('  !! el nodo no confirma la ganancia: se saltea el par')
            continue
        # El punto de operacion tiene que estar quieto ANTES de medir ruido, o
        # la correccion del lazo se cuela en el espectro.
        _log('  asentando %d s...' % args.asentar)
        fin = time.time() + args.asentar
        while time.time() < fin and bt._vivo:
            time.sleep(1.0)

        for rep in range(1, args.repeticiones + 1):
            if not bt._vivo:
                break
            # Ida y vuelta: cancela la deriva lineal dentro del bloque.
            orden = list(CONDICIONES) + list(reversed(CONDICIONES))
            for i, cond in enumerate(orden):
                if not bt._vivo:
                    break
                problema = _una_corrida(par, cond, rep * 10 + i,
                                        args.output, meta_extra)
                if problema == 'ya estaba':
                    saltadas += 1
                elif problema:
                    _log('  !! %s %s: %s' % (cond, rep, problema))
                else:
                    hechas += 1
                    _log('  %-5s r%d  ok' % (cond, rep))

    _cortar_estresores()
    _log('terminado: %d corridas nuevas, %d ya estaban, en %s'
         % (hechas, saltadas, args.output))
    _log('analiza con: python lab/analisis_ruido.py %s' % args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
