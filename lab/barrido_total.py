"""barrido_total.py - barrido EXHAUSTIVO de las 81 combinaciones de ganancia.

    python3 barrido_total.py [repeticiones] [ventana_s] [--reanudar]
                              [--reintentar-invalidas] [--port PUERTO]

Recorre las 9 ganancias del PGA por las 9 de PGAout, varias veces, y deja un
informe con todo lo que hace falta para decidir el punto de operacion del nodo:
donde converge CADA IDAC, cuanto tarda, cuanto tiempo pasa en cada estado del
control, cuantos aprendizajes le costo y con que parametros estaba configurado
el controlador en esa ganancia.

Pensado para dejarlo corriendo horas:

  * ESCRIBE A MEDIDA QUE MIDE.  Cada visita se agrega a `resultados.jsonl` en
    cuanto termina, asi un corte de luz o un Ctrl-C no se lleva la tanda.
  * `--reanudar` saltea las visitas que ya estan en ese archivo.
  * `--reintentar-invalidas` elimina las visitas INVALIDA anteriores y mide
    solamente esas posiciones de nuevo (implica `--reanudar`).
  * El informe Markdown se regenera entero en cada visita, asi que siempre hay
    un informe completo de lo medido hasta ese momento.
  * Corta cada visita apenas el veredicto esta decidido; solo las que fallan
    consumen la ventana entera.

Salidas, todas en `lab/barrido_total/`:

  | archivo | contenido |
  |---|---|
  | `resultados.jsonl` | una linea JSON por visita, con la serie cruda |
  | `INFORME.md` | informe legible, regenerado en cada visita |
  | `resumen.csv` | una fila por visita, para graficar |

Ojo con los tiempos: cada par arranca donde lo dejo el anterior, asi que el
tiempo de convergencia depende del camino. Por eso se informa el LPo de partida
y se repite el barrido varias veces.
"""
import argparse
import csv
import glob
import json
import os
import re
import signal
import sys
import threading
import time

import serial

# ---------------------------------------------------------------- constantes

PUERTO = None
BAUD = 115200
CODIGOS = [1, 2, 4, 8, 16, 24, 32, 48, 50]      # indice -> ganancia real
TAP = ['SEo', 'BP', 'OPAs', 'SUM', 'LP']
ESTADO = {0: 'FALTA_APRENDER', 1: 'APRENDIENDO', 2: 'REGULANDO', 3: 'FALLADO',
          4: 'PAUSADO'}

K_ESTADO, K_PERFIL, K_BANDA = 0x100, 0x101, 0x102
K_REVISION, K_UPTIME = 0x104, 0x105
K_FALLO_APRENDIZAJE, K_AUTOSAVE = 0x108, 0x109
K_OBJETIVO, K_FACTOR_LENTO = 0x10A, 0x10B
K_IDAC = 0x110                                   # 0x110 + i, i en 0..3
K_TAP = 0x120                                    # 0x120 + 4i valor, +1 valido
# Memoria de puntos de trabajo (firmware v6).
K_ORIGEN, K_ACIERTOS, K_FALLOS = 0x140, 0x141, 0x142
K_CANDIDATOS, K_POLITICA, K_CTX_SUMO = 0x143, 0x144, 0x145
K_PUNTOS_VALIDOS = 0x146
K_SEMILLA = 0x148                                # 0x148 + i, i en 0..3
K_RES_SLOW, K_RES_FAST = 0x14C, 0x14D
CP_COUNT = 49                                    # los parametros llegan en 0..48

ORIGEN = {0: 'NADA', 1: 'APRENDIZAJE', 2: 'PUNTO_EEPROM', 3: 'VECINO',
          4: 'INTERPOLADO', 5: 'SIEMBRA_VECINO', 6: 'PERFIL'}

# Umbrales de la NOTA de calidad, en mV.  El rango util de LPo es +-97 mV (la
# ventana de validez menos el ruido), asi que la nota dice cuanto rango LIBRE
# queda: A conserva el 75 %, B la mitad, C un cuarto.  A cae casi exacto sobre
# CP_HOLD_UV (25 mV), la banda en la que el propio lazo se declara centrado.
NOTA_A, NOTA_B, NOTA_C = 24.3, 48.5, 73.0
# Pico a pico maximo para considerar que se quedo QUIETO.
QUIETO_PP_MV = 30.0
# Un IDAC pasado esto esta contra su tope: en banda pero sin autoridad para
# corregir.  Un punto asi no se puede sembrar: al primer cambio se cae.
IDAC_TOPE = 200
# Muestras VALIDAS minimas de LPo para que el pico a pico signifique algo.  Se
# calcula sobre las ultimas 15; con menos la ventana no esta llena y un pp de
# 0,0 mV sobre una sola muestra parece quietud perfecta cuando es falta de
# dato.  Medido: 21 de 191 visitas del historico caian en esa trampa.
# Cuantas medidas NUEVAS -no lineas repetidas- hacen falta para dar una
# nota, y cuanto tiempo real tienen que abarcar.  Ocho medidas a 20 s son
# 160 s: mas de tres constantes de tiempo del acople, que es lo que hace
# falta para que "quieto" signifique algo.
MUESTRAS_VALIDAS_MIN = 6
SPAN_QUIETUD_MIN_S = 150.0

# Nombres de los parametros, en el orden del enum ControlParameter.
CP_NOMBRE = [
    'PGA', 'PGAOUT', 'AVERAGE', 'CAPACITOR', 'PERIOD_MS',
    'TAU_MS', 'KP_NUM', 'KP_DEN', 'DEADBAND_UV', 'ENTER_MS',
    'FINE_STEP', 'RESCUE_STEP', 'RESCUE_MS', 'SUM_BAND_UV',
    'COARSE_STEP', 'FINE_SLOPE_UV', 'COARSE_SLOPE_UV',
    'SLOW0_SLOPE_UV', 'SLOW1_SLOPE_UV', 'SLOW_TAU_MS',
    'OPA_TARGET_UV', 'LEARN_BAND_UV', 'LEARN_TIMEOUT_MS',
    'SCAN_MS', 'REPORT_MS', 'CAPTURE_CHANNEL', 'SETTLE_SAMPLES',
    'VALID_LOW_UV', 'VALID_HIGH_UV', 'MARGIN_UV',
    'INITIAL2', 'INITIAL3', 'STABLE_UV', 'STABLE_MS',
    'FINE_LIMIT', 'COARSE_LIMIT',
    'HOLD_UV', 'FINE_MID', 'COARSE_MS', 'QUIET_MS',
    'SETTLED_MS', 'SETTLED_BAND_UV', 'WAKE_COUNT',
    'SCAN_SETTLED_MS', 'REPORT_SETTLED_MS',
    'RECENTER_UV', 'RECENTER_MS',
    'PUNTO_POLICY', 'PUNTO_ARG',
]
# Los que de verdad definen el lazo en un punto de ganancia: son los que van al
# informe. El resto queda en el JSON.
CP_INTERESANTES = ['PGA', 'PGAOUT', 'FINE_SLOPE_UV', 'COARSE_SLOPE_UV',
                   'SLOW0_SLOPE_UV', 'SLOW1_SLOPE_UV', 'OPA_TARGET_UV',
                   'RESCUE_STEP', 'RESCUE_MS', 'COARSE_MS', 'FINE_MID',
                   'HOLD_UV', 'DEADBAND_UV', 'SUM_BAND_UV', 'SLOW_TAU_MS']

VENTANA_UV = 97000          # |LPo| aceptable: la ventana de validez menos ruido
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'barrido_total')

# ---------------------------------------------------------------- telemetria

_est = {}
# Sumidero opcional de lineas crudas.  Sirve para que otro experimento capture
# un volcado (`#DUMP ...`) SIN abrir el puerto por segunda vez: dos procesos
# sobre el mismo adaptador se mezclan los comandos y el resultado no es de
# nadie.  Es una lista a la que el hilo lector agrega; `append` es atomico.
_sink = None
_vivo = True
_puerto = {}
_serial_lock = threading.Lock()
_lector_error = None
_ultimo_ctl = 0.0
# Cuantas veces se reabrio el puerto.  El USB del ESP se re-enumera solo
# cada tanto (PermissionError 13 en ClearCommError) y eso NO es una falla
# del nodo: es el adaptador reapareciendo.  Quien mida tiene que poder
# enterarse, porque una reconexion en medio de una visita reinicia al ESP
# y la visita deja de ser comparable; pero la campana no se aborta por eso.
_reconexiones = 0
# Tope real: si el puerto no vuelve en este tiempo, ahi si es un cuelgue.
ESPERA_RECONEXION_S = 600.0


class TelemetriaVencida(RuntimeError):
    pass


class Inmedible(RuntimeError):
    """LPo no responde Y el lazo no se mueve: no hay nada que medir.

    Es un resultado, no un error: acota la ganancia usable.  Se declara
    DENTRO de la ventana de medicion y no en una pasada aparte, porque
    una pasada aparte obliga a un segundo cambio de ganancia y el
    firmware emite el origen del punto UNA sola vez, en el cambio."""

    def __init__(self, validas, movimientos, segundos):
        RuntimeError.__init__(self, 'LPo valido %d veces y los IDAC quietos en %.0f s' % (validas, segundos))
        self.validas = validas
        self.movimientos = movimientos
        self.segundos = segundos


def _detectar_puerto():
    """Elige un puerto estable sin asumir Windows ni un /dev/tty concreto."""
    pedido = os.environ.get('BARRIDO_PORT')
    if pedido:
        return pedido

    candidatos = []
    if os.name == 'nt':
        # Mantiene el banco historico como valor por omision en Windows.
        candidatos = ['COM8']
    else:
        candidatos.extend(sorted(glob.glob('/dev/serial/by-id/*')))
        candidatos.extend(sorted(glob.glob('/dev/ttyUSB*')))
        candidatos.extend(sorted(glob.glob('/dev/ttyACM*')))
    if not candidatos:
        raise RuntimeError('no se encontro puerto serie; use --port o BARRIDO_PORT')
    return candidatos[0]


def _abrir_puerto(limite_s):
    """Abre el puerto reintentando hasta `limite_s`.  Devuelve None si no pudo."""
    t0 = time.monotonic()
    while _vivo:
        s = serial.Serial()
        s.port, s.baudrate, s.timeout = PUERTO, BAUD, 0.3
        s.dtr = s.rts = False
        if os.name != 'nt':
            # Evita que dos barridos abran simultaneamente el mismo adaptador.
            s.exclusive = True
        try:
            s.open()
            return s
        except Exception:
            try:
                s.close()
            except Exception:
                pass
            if time.monotonic() - t0 >= limite_s:
                return None
            time.sleep(2)
    return None


def _esperar_puerto(limite_s=None):
    """Bloquea mientras el puerto este caido y el lector lo este reabriendo.

    Levanta RuntimeError si no vuelve.  Quien llama trata eso como lo que es:
    esta visita se perdio, la campana sigue."""
    limite = ESPERA_RECONEXION_S if limite_s is None else limite_s
    t0 = time.monotonic()
    while _lector_error or 's' not in _puerto:
        if not _vivo:
            raise RuntimeError('detenido')
        if time.monotonic() - t0 >= limite:
            raise RuntimeError(_lector_error or 'puerto %s ausente' % PUERTO)
        time.sleep(1.0)


def _leer():
    """Hilo lector: mantiene `_est` con el ultimo valor de cada clave.

    Reconecta.  Una campana de ocho horas ve al menos una re-enumeracion del
    USB, y antes eso mataba la noche entera: el hilo salia, `_lector_error`
    quedaba puesto para siempre y toda visita posterior levantaba la misma
    excepcion aunque el puerto ya hubiera vuelto.  Ahora el error es
    TRANSITORIO mientras el puerto este ausente y solo se vuelve definitivo
    si no vuelve en `ESPERA_RECONEXION_S`."""
    global _lector_error, _ultimo_ctl, _reconexiones
    patron = re.compile(r'#CTL 0 (\d+) (-?\d+)')
    primera = True
    while _vivo:
        s = _abrir_puerto(60.0 if primera else ESPERA_RECONEXION_S)
        if s is None:
            if _vivo:
                _lector_error = 'NO ABRE %s' % PUERTO
                print(_lector_error, flush=True)
            return
        _puerto['s'] = s
        _lector_error = None
        if not primera:
            _reconexiones += 1
            # El ESP se reinicio al re-enumerarse: la telemetria vieja es de
            # otra vida del nodo y no se mezcla con la nueva.
            _est.clear()
            _ultimo_ctl = 0.0
            print('%s recuperado (reconexion %d)' % (PUERTO, _reconexiones),
                  flush=True)
        primera = False
        try:
            while _vivo:
                linea = s.readline().decode('utf-8', 'replace')
                sumidero = _sink
                if sumidero is not None:
                    sumidero.append(linea)
                m = patron.search(linea)
                if m:
                    _est[int(m.group(1))] = int(m.group(2))
                    _ultimo_ctl = time.monotonic()
        except Exception as e:
            if not _vivo:
                break
            _lector_error = 'se perdio %s: %s' % (PUERTO, e)
            print(_lector_error, flush=True)
        finally:
            _puerto.pop('s', None)
            try:
                s.close()
            except Exception:
                pass


def _cmd(texto, espera=1.5):
    for _ in range(150):
        if 's' in _puerto:
            break
        time.sleep(0.5)
    if 's' not in _puerto:
        print('NO ABRE %s: el lector nunca tomo el puerto' % PUERTO, flush=True)
        raise SystemExit(2)
    _esperar_puerto()
    try:
        with _serial_lock:
            _puerto['s'].write((texto + '\n').encode())
            _puerto['s'].flush()
    except Exception:
        # Se cayo justo al escribir: el lector ya esta reconectando.  Una
        # sola oportunidad mas, y si tampoco, que lo maneje quien llamo.
        _esperar_puerto()
        with _serial_lock:
            _puerto['s'].write((texto + '\n').encode())
            _puerto['s'].flush()
    time.sleep(espera)


def _reset_psoc_desde_esp(verificar=True):
    """Pide al ESP el pulso GPIO19 que reinicia al PSoC.

    No usa KitProg, PSoC Creator ni scripts del host. Por eso funciona igual
    desde Windows o desde un servidor Linux conectado al USB del ESP32.

    DOS cosas que antes faltaban y que costaron media campana:

    1. El ESP **rechaza** `psocreset` si hay una captura activa
       (``[USB] psocreset rechazado: captura/transferencia activa``), y
       `_asegurar_adquisicion` deja justamente una captura corriendo.  O sea
       que el primer reset del programa funcionaba y todos los siguientes no.
       Hay que mandar `stop` antes.

    2. Nadie miraba si el nodo se habia reiniciado.  La campana del
       2026-09-26 hizo siete visitas etiquetadas FRIO con el PSoC llevando
       4,6 h de uptime ininterrumpido: un tercio del experimento decia
       "arranque en frio" sobre algo que no lo era, y el log del esclavo lo
       venia avisando sin que nadie lo leyera.

    Devuelve True solo si el uptime del PSoC volvio a empezar.  Quien llama
    tiene que tratar el False como "no se pudo enfriar" y saltear la visita:
    medir sobre una condicion que no es la de la etiqueta es peor que no
    medir.
    """
    global _ultimo_ctl
    antes = None
    if verificar:
        _cmd('ctl report', 0.8)
        time.sleep(1.2)
        antes = _est.get(K_UPTIME)
    _cmd('stop', 0.8)                  # sin esto el ESP rechaza el reset
    _cmd('psocreset', 0.5)
    _est.clear()                       # no aceptar telemetria anterior al reset
    _ultimo_ctl = 0.0
    if not verificar:
        return True
    # El firmware auto-calibra al arrancar; entrar antes de que termine mide
    # el transitorio de la calibracion, no el arranque.
    time.sleep(30)
    if not _asegurar_adquisicion():
        print('tras el psocreset no vuelve la adquisicion', flush=True)
        return False
    _cmd('ctl report', 0.8)
    time.sleep(1.2)
    despues = _est.get(K_UPTIME)
    if despues is None or (antes is not None and despues >= antes):
        print('el psocreset NO reinicio el nodo (uptime %s -> %s)'
              % (antes, despues), flush=True)
        return False
    return True


def _foto():
    """Una muestra de todo lo que interesa, en el instante actual."""
    # El PSoC puede seguir controlando normalmente sin emitir un reporte
    # espontaneo durante mas de diez segundos. No convertir ese silencio en un
    # falso cuelgue: cuando la foto envejece, pedirla activamente por el mismo
    # canal que ya usa la guarda de arranque. Esto deja la recuperacion de un
    # caso predecible dentro del programa, sin despertar al operador Codex.
    if not _ultimo_ctl or time.monotonic() - _ultimo_ctl > 5.0:
        anterior = _ultimo_ctl
        _cmd('ctl report', 0.2)
        for _ in range(20):
            if _ultimo_ctl > anterior:
                # Dar tiempo a que termine el bloque: el primer #CTL actualiza
                # el reloj, pero la foto usa claves que llegan mas abajo.
                time.sleep(0.2)
                break
            if _lector_error:
                _esperar_puerto()
                raise TelemetriaVencida('se reconecto %s durante la foto'
                                        % PUERTO)
            time.sleep(0.1)
    if not _ultimo_ctl or time.monotonic() - _ultimo_ctl > 10.0:
        raise TelemetriaVencida('no llega telemetria #CTL desde hace 10 s')
    return {
        't': None,
        'estado': _est.get(K_ESTADO),
        'banda': _est.get(K_BANDA),
        'perfil': _est.get(K_PERFIL),
        'uptime': _est.get(K_UPTIME),
        'idac': [_est.get(K_IDAC + i) for i in range(4)],
        'tap': [_est.get(K_TAP + 4 * i) for i in range(5)],
        'valido': [_est.get(K_TAP + 4 * i + 1) for i in range(5)],
        # Milisegundos desde que el firmware TOMO esa medida.  Sin esto
        # no hay como distinguir una lectura nueva de la misma linea
        # repetida, y el firmware repite: ya calibrado baja el barrido a
        # 20 s y los reportes a 30 s (CP_SCAN_SETTLED_MS /
        # CP_REPORT_SETTLED_MS).  O sea que justo en el caso BUENO una
        # ventana de 15 muestras a 2 s contiene una o dos medidas de
        # verdad, copiadas quince veces.
        'edad': [_est.get(K_TAP + 4 * i + 2) for i in range(5)],
    }


def _distintas(serie, tap=4, tolerancia_s=1.0):
    """Las fotos que traen una medida NUEVA de ese tap, no una repetida.

    El firmware publica la EDAD de cada tap (`now - ctl_stamp[i]`), asi que
    el instante en que tomo la medida se reconstruye restando: `t - edad`.
    Dos fotos con el mismo instante reconstruido son la MISMA medida
    publicada dos veces.

    No alcanza con pedir que la edad BAJE -fue mi primer intento-: si el
    barrido y el reporte van al mismo ritmo, la edad sale casi constante
    entre medidas distintas y se perderian todas menos la primera.  El
    instante reconstruido no tiene esa ambiguedad.

    Hace falta porque el firmware repite: ya calibrado baja el barrido a
    20 s y los reportes a 30 s (CP_SCAN_SETTLED_MS / CP_REPORT_SETTLED_MS).
    Contar lineas en vez de medidas daba pico a pico 0,0 mV por construccion
    justo en el caso BUENO, que es la forma en que este banco ya se engano
    una vez y produjo 39 semillas falsas de 68."""
    fuera = []
    sello_prev = None
    for f in serie:
        e = f.get('edad', [None] * 5)[tap]
        t = f.get('t')
        if e is None or e < 0 or t is None:
            # Sin edad no se puede deduplicar; se cuenta, que es lo
            # conservador para un banco que ya perdio datos por confiar.
            fuera.append(f)
            sello_prev = None
            continue
        sello = t - e / 1000.0
        if sello_prev is None or abs(sello - sello_prev) > tolerancia_s:
            fuera.append(f)
            sello_prev = sello
    return fuera


def _taps_frescos(max_edad_ms=10000):
    """Verdadero si los cinco taps tienen una medida publicada y reciente.

    ``valido=0`` significa que la tension esta fuera del rango analogico, no
    que la adquisicion este detenida. Ese dato debe llegar al analisis para
    producir FALLA/INVALIDA, pero no puede bloquear el arranque del barrido.
    """
    for i in range(5):
        base = K_TAP + 4 * i
        if _est.get(base) is None:
            return False
        edad = _est.get(base + 2)
        if edad is None or edad < 0 or edad > max_edad_ms:
            return False
    return True


def _asegurar_adquisicion():
    """Ceba y comprueba el muestreo de control cuando arranca sin IRQ.

    En esta implementacion de superMaquina se observo que, tras un arranque en
    frio, el bypass puede quedar sin publicar muestras aunque UART, I2C y el
    ADC respondan. Una captura minima inicializa esa ruta y, al terminar, el
    firmware vuelve solo al control. Es una recuperacion determinista: nunca
    se acepta el cebado hasta ver los cinco taps publicados y frescos. El bit
    de validez no se exige: una tension fuera de rango sigue siendo una medida
    nueva y sera clasificada por el analisis de la visita.
    """
    _cmd('ctl report', 0.2)
    time.sleep(0.3)
    if _taps_frescos():
        return True
    for intento in range(1, 4):
        print('    .. taps sin datos: cebando adquisicion (%d/3)' % intento,
              flush=True)
        # Una captura minima anterior puede haber dejado al ESP en STOPPED
        # con el buffer lleno. En ese estado ``startwait`` se ignora. Vaciar
        # solamente ese buffer de captura devuelve la maquina a WAIT_ARM sin
        # tocar pines, ganancias ni el estado del controlador del PSoC.
        _cmd('clear', 0.5)
        # Aunque LAB_STARTWAIT termina pronto, el bloque de telemetria y el
        # vaciado serie pueden seguir llegando. Dar el mismo margen que la
        # utilidad diagnostica evita evaluar una foto parcial.
        _cmd('startwait 5', 4.0)
        for _ in range(4):
            _cmd('ctl report', 0.2)
            time.sleep(0.5)
            if _taps_frescos():
                print('    .. adquisicion activa: 5/5 taps recientes',
                      flush=True)
                return True
    return False


# ------------------------------------------------------------------ medicion

def _fijar_ganancia(pga, pgaout, intentos=4):
    """Pone el par de ganancias y COMPRUEBA que el firmware lo haya tomado.

    No alcanza con mandar el comando. El 2026-09-19 un `else` en el ESP tapaba
    el caso PGAOUT y mandaba PGAVDAC en su lugar: `pgaout N` no cambiaba nada y
    el barrido midio durante horas un eje congelado, con resultados ordenados y
    reproducibles. `ctl get 0` y `ctl get 1` hacen que el PSoC emita CP_PGA y
    CP_PGAOUT en el acto, asi que se puede exigir la confirmacion en vez de
    suponerla."""
    for intento in range(intentos):
        _est.pop(0, None); _est.pop(1, None)
        _cmd('pga %d' % pga)
        _cmd('pgaout %d' % pgaout)
        _cmd('ctl get 0', 0.4)
        _cmd('ctl get 1', 0.4)
        for _ in range(25):                      # hasta ~5 s por intento
            if _est.get(0) == pga and _est.get(1) == pgaout:
                return True
            time.sleep(0.2)
        _cmd('ctl get 0', 0.4)
        _cmd('ctl get 1', 0.4)
        time.sleep(1.0)
    # AUTO-RECUPERACION. Si el nodo no confirma, lo mas probable es que el
    # PSoC se haya quedado mudo. El ESP pulsa GPIO19 y el firmware PSoC llama a
    # CySoftwareReset(); no hace falta KitProg ni una maquina Windows.
    # Sin esto el barrido sigue horas marcando INVALIDA y hace falta que alguien
    # mire; con esto se arregla solo y la tanda de varias horas no se pierde.
    print('    !! el firmware NO tomo x%d/x%d (dice PGA=%s PGAOUT=%s) '
          '-> reseteando PSoC'
          % (CODIGOS[pga], CODIGOS[pgaout], _est.get(0), _est.get(1)),
          flush=True)
    # Se hacen hasta tres intentos acotados y, si ninguno funciona, la tanda
    # aborta abajo conservando todo lo ya escrito.
    for reset_n in range(1, 4):
        try:
            _reset_psoc_desde_esp()
        except Exception as e:
            print('    !! reset %d fallo: %r' % (reset_n, e), flush=True)
            continue
        time.sleep(30)                  # el firmware auto-calibra al arrancar
        if not _asegurar_adquisicion():
            print('    !! reset %d sin adquisicion valida' % reset_n,
                  flush=True)
            continue
        for _ in range(2):
            _est.pop(0, None); _est.pop(1, None)
            _cmd('pga %d' % pga)
            _cmd('pgaout %d' % pgaout)
            _cmd('ctl get 0', 0.4)
            _cmd('ctl get 1', 0.4)
            for _ in range(25):
                if _est.get(0) == pga and _est.get(1) == pgaout:
                    print('    .. recuperado tras reset %d' % reset_n,
                          flush=True)
                    return True
                time.sleep(0.2)
    print('    !! sigue mudo despues del reset', flush=True)
    return False


def _visitar(pga, pgaout, ventana, muestreo=2.0, firmes=MUESTRAS_VALIDAS_MIN,
             limite_mult=4,
             sondeo_s=0.0, sondeo_validas=3):
    """Cambia a ese par y lo observa hasta que el veredicto este decidido.

    `firmes` muestras seguidas dentro de la ventana y quietas bastan para
    declararlo: esperar mas no cambia el veredicto y multiplica lo que tarda
    el barrido. Las que fallan si consumen la ventana entera, porque ahi la
    espera ES la prueba."""
    lp0 = (_est.get(K_TAP + 16)
           if _est.get(K_TAP + 17) == 1 else None)
    lp0 = lp0 / 1000.0 if lp0 is not None else None
    n_antes = _est.get(K_AUTOSAVE)

    # El origen y la semilla los emite el firmware como EVENTO al aplicar el
    # punto, o sea DENTRO del cambio de ganancia.  Hay que borrarlos ANTES,
    # nunca despues: `_est` guarda el ultimo valor de cada clave, asi que si
    # esta visita aprende de cero (y no emite nada) la semilla de la visita
    # ANTERIOR quedaria atribuida a esta y el residuo saldria inventado.
    _est.pop(K_ORIGEN, None)
    for _i in range(4):
        _est.pop(K_SEMILLA + _i, None)

    confirmada = _fijar_ganancia(pga, pgaout)
    if not confirmada:
        # No tiene sentido consumir hasta 4 ventanas observando una ganancia
        # que el firmware no tomo.  Ademas, continuar con el siguiente par
        # suele producir una cascada de INVALIDA (ocurrio en la vuelta 2 del
        # barrido vertical del 2026-09-20).  El resultado parcial ya esta en
        # disco y una reanudacion puede seguir despues de recuperar el nodo.
        raise RuntimeError('el nodo no confirma x%d/x%d despues del reset'
                           % (CODIGOS[pga], CODIGOS[pgaout]))
    _est.pop(K_FALLO_APRENDIZAJE, None)
    _est.pop(K_OBJETIVO, None)

    serie, t0 = [], time.time()
    t_banda, tope = None, ventana
    limite = ventana * limite_mult
    # Sondeo de medibilidad, integrado a la ventana.  Antes vivia en el
    # experimento y hacia SU PROPIO cambio de ganancia: eso gastaba el
    # evento de origen/semilla del firmware -que se emite una sola vez, al
    # cambiar- y despues esta funcion lo borraba, asi que toda visita salia
    # con origen None y residuo None.  Ademas el lazo llevaba ya hasta 300 s
    # convergiendo cuando arrancaba el reloj, y el t_estable medido era una
    # ficcion.  Un solo cambio de ganancia, un solo reloj.
    sondeo_validas_n = 0
    sondeo_movs = 0
    sondeo_idac = None
    while time.time() - t0 < tope:
        time.sleep(muestreo)
        f = _foto()
        f['t'] = round(time.time() - t0, 1)
        serie.append(f)
        if t_banda is None and f['banda'] == 1:
            t_banda = f['t']
        if sondeo_s > 0.0:
            if f['valido'][4] == 1:
                sondeo_validas_n += 1
            idac_ahora = tuple(_est.get(K_IDAC + _j) for _j in range(4))
            if sondeo_idac is not None and idac_ahora != sondeo_idac:
                sondeo_movs += 1
            sondeo_idac = idac_ahora
            if (f['t'] >= sondeo_s and t_banda is None and
                    sondeo_validas_n < sondeo_validas and sondeo_movs == 0):
                raise Inmedible(sondeo_validas_n, sondeo_movs, f['t'])
        if t_banda is not None:
            # Se corta cuando la quietud ya esta DEMOSTRADA sobre los
            # ultimos SPAN_QUIETUD_MIN_S segundos: mismo criterio que usa
            # el veredicto, para que no puedan discrepar.
            nuevas = [x for x in _distintas(serie, 4)
                      if x['tap'][4] is not None and x['valido'][4] == 1]
            if nuevas:
                t_fin = nuevas[-1]['t']
                vf = [x for x in nuevas
                      if x['t'] >= t_fin - SPAN_QUIETUD_MIN_S]
                ult = [x['tap'][4] for x in vf]
                span = t_fin - vf[0]['t'] if vf else 0.0
                if (len(ult) >= firmes and
                        span >= SPAN_QUIETUD_MIN_S * 0.9 and
                        all(abs(v) <= VENTANA_UV for v in ult) and
                        max(ult) - min(ult) < 30000):
                    break
        # PRORROGA 1.  Un par que aterriza justo antes de que se acabe la
        # ventana no alcanza a demostrar que se sostiene, y quedaba marcado
        # FALLA con LPo centrado: medido x4/x8, estable a los 216 s de una
        # ventana de 240 y con LPo en -2,1 mV.  Eso no es un fallo, es un par
        # lento.  Se estira lo justo para que pueda probarlo.
        lp = f['tap'][4] if f['valido'][4] == 1 else None
        if (tope == ventana and time.time() - t0 >= ventana - muestreo * 2 and
                lp is not None and abs(lp) <= VENTANA_UV):
            # La prorroga tiene que alcanzar para DEMOSTRAR la quietud, no
            # solo para tomar `firmes` muestras.  La cuenta vieja
            # (muestreo*(firmes+2) = 16 s) venia de cuando el criterio era un
            # numero de muestras; ahora la quietud exige SPAN_QUIETUD_MIN_S de
            # tiempo real, asi que 16 s no rescatan a nadie.  Medido sobre la
            # vuelta 1: 5 de 72 visitas quedaron en FALLA habiendo entrado en
            # banda -dos de ellas con LPo en -0,1 y 9,3 mV-, o sea falla del
            # instrumento y no del circuito.
            tope = ventana + SPAN_QUIETUD_MIN_S + muestreo * 4
        # PRORROGA 2.  Si al vencerse la ventana el nodo TODAVIA esta
        # aprendiendo, no fracaso: no termino.  Medido a PGA x16, tres pares
        # seguidos pasaron los 240 s enteros en APRENDIENDO, y un aprendizaje
        # en frio a ganancia alta puede tardar 600-800 s.  Cortar ahi y
        # escribir FALLA seria medir mi ventana, no el nodo.  Se le da hasta
        # `limite` y, si al llegar sigue aprendiendo, se informa como tal.
        if (f['estado'] == 1 and tope < limite and
                time.time() - t0 >= tope - muestreo * 2):
            tope = min(limite, tope + ventana)
    return serie, t_banda, lp0, n_antes, confirmada


def _config_actual():
    """Los parametros con los que el controlador esta corriendo ahora.

    El firmware los manda cada 30 reportes, asi que pueden ser de la visita
    anterior; el informe lo aclara comparando PGA/PGAOUT con lo pedido."""
    return {CP_NOMBRE[i]: _est.get(i) for i in range(CP_COUNT)
            if _est.get(i) is not None}


def _analizar(pga, pgaout, serie, t_banda, lp0, n_antes, ventana, confirmada):
    """Del crudo a los numeros que se miran."""
    def col(campo, idx=None):
        out = []
        for f in serie:
            v = f[campo][idx] if idx is not None else f[campo]
            if v is not None:
                out.append(v)
        return out

    # Solo lecturas NUEVAS: ver `_distintas`.  Contar lineas de telemetria
    # en vez de medidas hacia que una etapa asentada -o sea, el caso que
    # queremos premiar- diera pico a pico 0,0 mV por repeticion.
    lp_fotos = [f for f in _distintas(serie, 4)
                if f['tap'][4] is not None and f['valido'][4] == 1]
    lp = [f['tap'][4] for f in lp_fotos]
    # Desde cuando LPo ya NO vuelve a salir: el 't_banda' del firmware marca el
    # primer cruce, y un rescate que cruza de riel a riel lo marca al pasar.
    t_estable, ultimo_afuera = None, None
    for f in serie:
        v = f['tap'][4]
        if f['valido'][4] != 1 or v is None or abs(v) > VENTANA_UV:
            ultimo_afuera = f['t']
    if lp:
        if ultimo_afuera is None:
            t_estable = serie[0]['t']
        else:
            for f in serie:
                if (f['t'] > ultimo_afuera and f['valido'][4] == 1 and
                        f['tap'][4] is not None and
                        abs(f['tap'][4]) <= VENTANA_UV):
                    t_estable = f['t']; break

    # La quietud se prueba sobre los ultimos SPAN_QUIETUD_MIN_S segundos,
    # no sobre las ultimas N medidas.  Tomar "las ultimas 8" no sirve: con
    # el lazo todavia buscando el barrido va a 2 s y ocho medidas abarcan
    # 14 s, que no prueban nada sobre una planta de tau ~ 30-44 s; ya
    # asentado el barrido va a 20 s y ocho medidas abarcan 160 s.  O sea
    # que un numero fijo de muestras mide un tiempo distinto en cada
    # regimen, justo al reves de lo que hace falta.  El minimo de medidas
    # queda solo como proteccion contra un barrido detenido.
    cola, span_s = [], 0.0
    if lp_fotos:
        t_fin = lp_fotos[-1]['t']
        ventana_final = [f for f in lp_fotos
                         if f['t'] >= t_fin - SPAN_QUIETUD_MIN_S]
        cola = [f['tap'][4] for f in ventana_final]
        span_s = t_fin - ventana_final[0]['t'] if ventana_final else 0.0
    dentro = bool(cola) and all(abs(v) <= VENTANA_UV for v in cola)
    quieto = bool(cola) and (max(cola) - min(cola)) < 30000
    pasa = dentro and t_banda is not None and t_estable is not None

    # ---- nota de calidad -------------------------------------------------
    # El veredicto de arriba se conserva TAL CUAL para que las 191 visitas ya
    # medidas sigan siendo comparables.  La nota es el criterio nuevo y va
    # aparte: pasar exige quedarse QUIETO y no clavado contra el riel, y
    # ademas se puntua cuanto rango libre quedo.
    lp_final_mV = (lp[-1] / 1000.0) if lp else None
    pp_mV = ((max(cola) - min(cola)) / 1000.0) if cola else None
    # 0,9 de holgura: la ultima medida cae donde cae, y exigir el span
    # exacto rechazaria una ventana que se quedo a un segundo.
    respaldado = (len(cola) >= MUESTRAS_VALIDAS_MIN and
                  span_s >= SPAN_QUIETUD_MIN_S * 0.9)
    if lp_final_mV is None or pp_mV is None or not respaldado:
        nota = None
    elif pp_mV >= QUIETO_PP_MV:
        nota = None                       # se movia: no hay punto que sembrar
    else:
        a = abs(lp_final_mV)
        nota = ('A' if a <= NOTA_A else 'B' if a <= NOTA_B
                else 'C' if a <= NOTA_C else 'D')
    # Fragil: en banda pero con el actuador fino contra su tope.
    _i3 = serie[-1]['idac'][3] if serie else None
    fragil = (abs(_i3) > IDAC_TOPE) if _i3 is not None else None
    # Estricto = quieto y con rango libre de sobra.  'D' es quieto CONTRA el
    # riel, que es justo lo que no queremos llamar exito.  Y tampoco pasa
    # si quedo FRAGIL: LPo perfecto con IDAC3 a 248 de 255 es un punto sin
    # autoridad, que la primera deriva termica se lleva puesto.  Un solo
    # numero con un solo significado; `fragil` queda como el motivo.
    pasa_estricto = bool(confirmada and nota in ('A', 'B', 'C')
                         and not fragil)

    # Cuanto tiempo paso en cada estado, y cuantas veces volvio a aprender.
    tiempo_estado, aprendizajes, previo = {}, 0, None
    for i, f in enumerate(serie):
        e = f['estado']
        if e is None:
            continue
        dt = (serie[i]['t'] - serie[i - 1]['t']) if i else serie[0]['t']
        tiempo_estado[e] = round(tiempo_estado.get(e, 0.0) + dt, 1)
        if previo is not None and e == 1 and previo != 1:
            aprendizajes += 1
        previo = e

    idac_fin = serie[-1]['idac'] if serie else [None] * 4
    idac_rango = []
    for i in range(4):
        v = col('idac', i)
        idac_rango.append([min(v), max(v)] if v else [None, None])

    taps = {}
    for i, n in enumerate(TAP):
        v, ok = col('tap', i), col('valido', i)
        taps[n] = {
            'final_mV': round(v[-1] / 1000.0, 1) if v else None,
            'min_mV': round(min(v) / 1000.0, 1) if v else None,
            'max_mV': round(max(v) / 1000.0, 1) if v else None,
            'valido_pct': round(100.0 * sum(1 for x in ok if x == 1) / len(ok), 1)
                          if ok else None,
        }

    # Codigos con los que arranco el par, emitidos por el firmware como evento
    # al aplicar el punto.  El residuo es la resta contra los finales.
    # Solo hay residuo si de verdad se partio de una semilla.  Sin esta
    # guarda, una visita que APRENDIO de cero heredaba el origen y la semilla
    # de la visita anterior -son globales del firmware- y se le calculaba un
    # residuo contra un punto que nunca uso.  Medido el 2026-09-24: el brazo
    # de CONTROL copiaba el residuo del brazo de MEMORIA anterior.
    _CON_SEMILLA = (2, 3, 4, 5)          # EEPROM, VECINO, INTERPOLADO, SIEMBRA
    semilla = [_est.get(K_SEMILLA + i) for i in range(4)]
    if (_est.get(K_ORIGEN) in _CON_SEMILLA
            and all(v is not None for v in semilla)
            and all(v is not None for v in idac_fin)):
        residuo = [idac_fin[i] - semilla[i] for i in range(4)]
    else:
        semilla = None
        residuo = None

    n_post = _est.get(K_AUTOSAVE)
    return {
        'pga_cod': pga, 'pgaout_cod': pgaout,
        'pga': CODIGOS[pga], 'pgaout': CODIGOS[pgaout],
        'ganancia': CODIGOS[pga] * CODIGOS[pgaout],
        # Tres veredictos, no dos: un nodo que sigue aprendiendo cuando se
        # acaba el tiempo no fracaso, no termino.  Mezclarlos seria informar
        # el largo de mi ventana como si fuera una propiedad del hardware.
        'veredicto': ('PASA' if pasa else
                      ('APRENDIENDO' if (serie and serie[-1]['estado'] == 1)
                       else 'FALLA')) if confirmada else 'INVALIDA',
        'ganancia_confirmada': confirmada,
        'quieto': quieto,
        # ---- criterio nuevo, en paralelo al viejo ------------------------
        # 'veredicto' se deja intacto para poder comparar contra las 191
        # visitas ya medidas; el estricto es el que exige quietud y margen.
        'veredicto_estricto': ('PASA' if pasa_estricto else
                               ('APRENDIENDO'
                                if (serie and serie[-1]['estado'] == 1)
                                else 'FALLA')) if confirmada else 'INVALIDA',
        'nota': nota,
        'fragil': fragil,
        'muestras_validas_LPo': len(lp),
        'muestras_totales_LPo': sum(1 for f in serie
                                    if f['tap'][4] is not None),
        'span_quietud_s': round(span_s, 1),
        # ---- memoria de puntos de trabajo --------------------------------
        # De donde salio la condicion inicial de esta visita.  Sin esto no se
        # puede distinguir "la semilla sirvio" de "venia bien encaminado".
        'origen': ORIGEN.get(_est.get(K_ORIGEN), _est.get(K_ORIGEN)),
        'origen_cod': _est.get(K_ORIGEN),
        'politica_puntos': _est.get(K_POLITICA),
        'punto_aciertos': _est.get(K_ACIERTOS),
        'punto_fallos': _est.get(K_FALLOS),
        'candidatos_ram': _est.get(K_CANDIDATOS),
        'puntos_validos': _est.get(K_PUNTOS_VALIDOS),
        'ctx_sumo_mV': _est.get(K_CTX_SUMO),
        'semilla': semilla,
        # RESIDUO DE CORRECCION: cuanto tuvo que mover el lazo desde el valor
        # modelado.  Es la medida de calidad del modelo y el insumo de las
        # campanas siguientes: residuo -> 0 significa que la semilla acerto.
        'residuo': residuo,
        'residuo_firmware': [_est.get(K_RES_SLOW), _est.get(K_RES_FAST)],
        't_banda_s': t_banda,
        't_estable_s': t_estable,
        'duracion_s': serie[-1]['t'] if serie else 0,
        'ventana_s': ventana,
        'LPo_inicial_mV': round(lp0, 1) if lp0 is not None else None,
        'LPo_final_mV': round(lp[-1] / 1000.0, 1) if lp else None,
        'LPo_pp_final_mV': round((max(cola) - min(cola)) / 1000.0, 1) if cola else None,
        'idac_final': idac_fin,
        'idac_rango': idac_rango,
        'taps': taps,
        'tiempo_en_estado_s': {ESTADO.get(k, str(k)): v
                               for k, v in sorted(tiempo_estado.items())},
        'aprendizajes': aprendizajes,
        'fallo_aprendizaje': _est.get(K_FALLO_APRENDIZAJE),
        'objetivo_sumo_uV': _est.get(K_OBJETIVO),
        'factor_pendiente_lenta_x1000': _est.get(K_FACTOR_LENTO),
        'autosaves': (n_post - n_antes) if (n_post is not None and
                                            n_antes is not None) else None,
        'perfil': serie[-1]['perfil'] if serie else None,
        'uptime_ms': serie[-1]['uptime'] if serie else None,
        'config': _config_actual(),
        'serie': [{'t': f['t'], 'estado': f['estado'], 'banda': f['banda'],
                   'idac': f['idac'], 'tap': f['tap']} for f in serie],
    }


# ------------------------------------------------------------------ informes

def _cargar(ruta):
    if not os.path.exists(ruta):
        return []
    out = []
    with open(ruta, encoding='utf-8') as fh:
        for linea in fh:
            linea = linea.strip()
            if linea:
                try:
                    out.append(json.loads(linea))
                except ValueError:
                    pass          # linea cortada por un corte de luz: se ignora
    return out


def _escribir_csv(res, ruta):
    # Las columnas nuevas van al final para no reordenar las que ya existen;
    # S0..S3 y R0..R3 se expanden igual que I0..I3 con idac_final.  Las
    # visitas viejas no tienen estas claves: quedan vacias, no rompen nada.
    campos = ['vuelta', 'pga', 'pgaout', 'ganancia', 'veredicto', 't_banda_s',
              't_estable_s', 'LPo_inicial_mV', 'LPo_final_mV',
              'LPo_pp_final_mV', 'I0', 'I1', 'I2', 'I3', 'aprendizajes',
              'objetivo_sumo_uV', 'factor_pendiente_lenta_x1000',
              'veredicto_estricto', 'nota', 'fragil', 'muestras_validas_LPo',
              'origen', 'politica_puntos', 'punto_aciertos', 'punto_fallos',
              'candidatos_ram', 'ctx_sumo_mV',
              'S0', 'S1', 'S2', 'S3', 'R0', 'R1', 'R2', 'R3']
    with open(ruta, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for r in res:
            fila = {k: r.get(k) for k in campos if k in r}
            fila['vuelta'] = r.get('vuelta')
            for i in range(4):
                fila['I%d' % i] = (r['idac_final'][i]
                                   if r.get('idac_final') else None)
                fila['S%d' % i] = (r['semilla'][i]
                                   if r.get('semilla') else None)
                fila['R%d' % i] = (r['residuo'][i]
                                   if r.get('residuo') else None)
            w.writerow(fila)


def _pct(xs, q):
    """Percentil por rango mas cercano.

    UNA sola convencion para todos los percentiles del informe.  Mezclarlas
    -mediana por `len//2` y p90 por `0.9*(len-1)`- hacia que con pocas
    muestras el p90 saliera MENOR que la mediana, que es imposible y delata
    el bug recien cuando alguien lo mira dos veces."""
    if not xs:
        return None
    xs = sorted(xs)
    k = int(round(q * (len(xs) - 1)))
    return xs[max(0, min(len(xs) - 1, k))]


def _informe(res, ruta, t_inicio):
    pasa = [r for r in res if r['veredicto'] == 'PASA']
    por_par = {}
    for r in res:
        por_par.setdefault((r['pga'], r['pgaout']), []).append(r)

    L = []
    L.append('# Barrido exhaustivo de ganancias\n')
    vueltas_esperadas = max((r.get('vuelta') or 0 for r in res), default=0)
    total_esperado = len(CODIGOS) ** 2 * vueltas_esperadas
    faltantes = max(0, total_esperado - len(res))
    aprend = [r for r in res if r['veredicto'] == 'APRENDIENDO']
    fallan = [r for r in res if r['veredicto'] == 'FALLA']
    invalidas = [r for r in res if r['veredicto'] == 'INVALIDA']
    L.append('Generado el %s. %d visitas medidas sobre %d pares distintos: '
             '%d PASA (%.0f %%), %d FALLA, %d que seguian APRENDIENDO al '
             'vencerse el tiempo, %d INVALIDA.\n'
             % (time.strftime('%Y-%m-%d %H:%M'), len(res), len(por_par),
                len(pasa), 100.0 * len(pasa) / len(res) if res else 0,
                len(fallan), len(aprend), len(invalidas)))
    if faltantes:
        L.append('\n**Barrido incompleto:** faltan **%d de %d** visitas '
                 'esperadas. El informe conserva lo valido, pero los pares '
                 'sin todas sus vueltas no se consideran recomendados.\n'
                 % (faltantes, total_esperado))
    if invalidas:
        L.append('\n**INVALIDA no cuenta como medicion**: el firmware no '
                 'confirmo la ganancia pedida. Esas visitas deben repetirse; '
                 'no se usan para recomendar ni descartar pares.\n')
    if aprend:
        L.append('\n**APRENDIENDO no es un fallo**: el nodo no habia terminado '
                 'de buscar su punto cuando se acabo el tiempo asignado. Un '
                 'aprendizaje en frio a ganancia alta puede tardar 600-800 s. '
                 'Informarlo como fallo seria medir la ventana del banco y no '
                 'el nodo.\n')
    L.append('Horas de banco acumuladas: %.1f.\n'
             % (sum((r.get('duracion_s') or 0) for r in res) / 3600.0))
    L.append('\n**Criterio.** `estable` es el instante desde el cual LPo ya no '
             'vuelve a salir de la ventana de +-97 mV. El "primer cruce" que '
             'declara el firmware puede ser un rescate cruzando de un riel al '
             'otro, y como numero de convergencia miente.\n')
    L.append('\nCada par arranca donde lo dejo el anterior, asi que el tiempo '
             'depende del camino: por eso se repite el barrido y se informa el '
             'LPo de partida.\n')

    # --- tabla principal, ordenada por ganancia conjunta
    L.append('\n## Todos los pares\n')
    L.append('| PGA | PGAout | ganancia | visitas | PASA | estable mediana | '
             'estable peor | LPo final | I0 | I1 | I2 | I3 |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for (pg, po), rs in sorted(por_par.items(),
                               key=lambda kv: (kv[0][0] * kv[0][1], kv[0][0])):
        ok = [r for r in rs if r['veredicto'] == 'PASA']
        ts = sorted(r['t_estable_s'] for r in ok if r['t_estable_s'] is not None)
        med = ('%.0f s' % ts[len(ts) // 2]) if ts else '—'
        peor = ('%.0f s' % ts[-1]) if ts else '—'
        lpf = ok[-1]['LPo_final_mV'] if ok else rs[-1]['LPo_final_mV']
        idac = (ok[-1] if ok else rs[-1]).get('idac_final') or [None] * 4
        L.append('| x%d | x%d | **%d** | %d | %d | %s | %s | %s mV | %s | %s | %s | %s |'
                 % (pg, po, pg * po, len(rs), len(ok), med, peor,
                    lpf if lpf is not None else '—',
                    idac[0], idac[1], idac[2], idac[3]))

    # --- los que sirven de verdad
    L.append('\n## Recomendados\n')
    L.append('Pares que pasaron **todas** sus visitas, con LPo final dentro de '
             '+-60 mV (banda del modo estable) y mediana de estabilizacion por '
             'debajo de 60 s. Ordenados por ganancia.\n')
    L.append('| PGA | PGAout | ganancia | estable mediana | LPo final | visitas |')
    L.append('|---|---|---|---|---|---|')
    hay = False
    for (pg, po), rs in sorted(por_par.items(),
                               key=lambda kv: -(kv[0][0] * kv[0][1])):
        ok = [r for r in rs if r['veredicto'] == 'PASA']
        vueltas_presentes = {r.get('vuelta') for r in rs}
        if (len(ok) != len(rs) or not ok or
                vueltas_presentes != set(range(1, vueltas_esperadas + 1))):
            continue
        ts = sorted(r['t_estable_s'] for r in ok if r['t_estable_s'] is not None)
        if not ts or ts[len(ts) // 2] > 60:
            continue
        lpf = ok[-1]['LPo_final_mV']
        if lpf is None or abs(lpf) > 60:
            continue
        hay = True
        L.append('| x%d | x%d | **%d** | %.0f s | %s mV | %d/%d |'
                 % (pg, po, pg * po, ts[len(ts) // 2], lpf, len(ok), len(rs)))
    if not hay:
        L.append('| — | — | — | — | — | — |')

    # --- los que no
    malos = [(k, v) for k, v in por_par.items()
             if any(r['veredicto'] == 'FALLA' for r in v)]
    if malos:
        L.append('\n## Pares con al menos un fallo\n')
        L.append('| PGA | PGAout | ganancia | PASA/visitas | aprendizajes | '
                 'LPo final | SUM valido | nota |')
        L.append('|---|---|---|---|---|---|---|---|')
        for (pg, po), rs in sorted(malos, key=lambda kv: kv[0][0] * kv[0][1]):
            ok = sum(1 for r in rs if r['veredicto'] == 'PASA')
            u = rs[-1]
            nota = ('nunca declaro banda' if u['t_banda_s'] is None
                    else 'entro y se fue')
            L.append('| x%d | x%d | %d | %d/%d | %d | %s mV | %s %% | %s |'
                     % (pg, po, pg * po, ok, len(rs), u['aprendizajes'],
                        u['LPo_final_mV'], u['taps']['SUM']['valido_pct'], nota))

    # --- parametros del controlador
    L.append('\n## Parametros del controlador\n')
    L.append('Los que definen el lazo, tal como los reporto el firmware en la '
             'ultima visita de cada par. Las pendientes de IDAC2 y del par '
             'lento las escala el firmware con la ganancia de PGAout, asi que '
             'cambian de par en par.\n')
    L.append('| PGA | PGAout | ' + ' | '.join(CP_INTERESANTES[2:]) + ' |')
    L.append('|---' * (2 + len(CP_INTERESANTES[2:])) + '|')
    for (pg, po), rs in sorted(por_par.items(),
                               key=lambda kv: (kv[0][0] * kv[0][1], kv[0][0])):
        c = rs[-1].get('config') or {}
        L.append('| x%d | x%d | ' % (pg, po) +
                 ' | '.join(str(c.get(n, '—')) for n in CP_INTERESANTES[2:]) + ' |')

    # --- velocidad por origen del punto ------------------------------------
    # 'origen' es de donde salio la condicion inicial de la visita (memoria
    # de puntos, vecino, interpolado, aprendizaje en frio...). Esta tabla es
    # la que contesta si esa memoria sirve: si el origen importa, tiene que
    # verse en el tiempo hasta estable y en la nota de calidad.
    L.append('\n## Velocidad por origen del punto\n')
    con_origen = [r for r in res if r.get('origen') is not None]
    if not con_origen:
        L.append('Todavia no hay visitas con `origen` registrado.\n')
    else:
        por_origen = {}
        for r in con_origen:
            por_origen.setdefault(r['origen'], []).append(r)
        L.append('| origen | n | estable mediana | estable p90 | nota A | '
                 'nota B | nota C | nota D |')
        L.append('|---|---|---|---|---|---|---|---|')
        for origen, rs in sorted(por_origen.items()):
            ts = sorted(r['t_estable_s'] for r in rs
                        if r.get('t_estable_s') is not None)
            med = ('%.0f s' % _pct(ts, 0.5)) if ts else '—'
            p90 = ('%.0f s' % _pct(ts, 0.9)) if ts else '—'
            notas = {n: sum(1 for r in rs if r.get('nota') == n)
                     for n in ('A', 'B', 'C', 'D')}
            L.append('| %s | %d | %s | %s | %d | %d | %d | %d |'
                     % (origen, len(rs), med, p90,
                        notas['A'], notas['B'], notas['C'], notas['D']))

    # --- residuo de correccion ----------------------------------------------
    # 'residuo' es cuanto tuvo que mover el lazo desde la semilla aplicada al
    # arrancar el par. APRENDIZAJE no arranca de una semilla (busca desde
    # cero) y no tiene este dato, asi que se excluye junto con los None.
    L.append('\n## Residuo de correccion\n')
    con_residuo = [r for r in res
                   if r.get('origen') not in (None, 'APRENDIZAJE')
                   and r.get('residuo') is not None]
    if not con_residuo:
        L.append('Todavia no hay visitas con `residuo` registrado.\n')
    else:
        por_origen_r = {}
        for r in con_residuo:
            por_origen_r.setdefault(r['origen'], []).append(r)
        L.append('| origen | n | I0 mediana | I0 max | I1 mediana | I1 max | '
                 'I2 mediana | I2 max | I3 mediana | I3 max |')
        L.append('|---|---|---|---|---|---|---|---|---|---|')
        for origen, rs in sorted(por_origen_r.items()):
            cols = []
            for i in range(4):
                vals = sorted(abs(r['residuo'][i]) for r in rs)
                cols.append('%d' % vals[len(vals) // 2])
                cols.append('%d' % vals[-1])
            L.append('| %s | %d | %s |'
                     % (origen, len(rs), ' | '.join(cols)))
        L.append('\nResiduo cercano a cero significa que la semilla acerto: '
                 'el lazo no tuvo que corregir casi nada desde el punto de '
                 'partida calculado. Residuo grande es la senal de que el '
                 'modelo (o el punto guardado) esta desactualizado.\n')

    # --- detalle por par
    L.append('\n## Detalle por par\n')
    for (pg, po), rs in sorted(por_par.items(),
                               key=lambda kv: (kv[0][0] * kv[0][1], kv[0][0])):
        L.append('\n### x%d / x%d — ganancia %d\n' % (pg, po, pg * po))
        L.append('| vuelta | veredicto | estable | 1er cruce | LPo ini | '
                 'LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | '
                 'tiempo por estado |')
        L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
        for r in rs:
            idac = r.get('idac_final') or [None] * 4
            est = ', '.join('%s %.0fs' % (k, v)
                            for k, v in r['tiempo_en_estado_s'].items())
            L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d | %s |'
                     % (r.get('vuelta'), r['veredicto'],
                        ('%.0f s' % r['t_estable_s']) if r['t_estable_s'] is not None else '—',
                        ('%.0f s' % r['t_banda_s']) if r['t_banda_s'] is not None else '—',
                        r['LPo_inicial_mV'], r['LPo_final_mV'],
                        r['LPo_pp_final_mV'],
                        idac[0], idac[1], idac[2], idac[3],
                        r['aprendizajes'], est))
        u = rs[-1]
        if u.get('objetivo_sumo_uV') is not None:
            L.append('\nObjetivo de SUMo bisecado: **%.1f mV**.'
                     % (u['objetivo_sumo_uV'] / 1000.0))
        if u.get('factor_pendiente_lenta_x1000') not in (None, 1000):
            L.append('\nCorreccion medida del modelo del par lento: **%.2fx**.'
                     % (u['factor_pendiente_lenta_x1000'] / 1000.0))
        L.append('\nTaps en la ultima visita: ' +
                 ', '.join('%s %s mV (%s %% valido)'
                           % (n, u['taps'][n]['final_mV'],
                              u['taps'][n]['valido_pct']) for n in TAP) + '.')

    with open(ruta, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(L) + '\n')


# ---------------------------------------------------------------------- main

def arrancar_enlace():
    """Prueba de vida ACTIVA del enlace antes de medir nada.

    Se factoriza de main() para que cualquier experimento que use estas
    primitivas arranque igual y no reimplemente el handshake."""
    # Guarda de arranque. En Linux abrir el CP2102 reinicia el ESP32; luego el
    # esclavo tarda unos segundos en arrancar y el PSoC no esta obligado a
    # emitir metadata espontaneamente. Pedir `ctl report` hace que la prueba
    # de vida sea activa y evita confundir silencio valido con puerto tomado.
    # Se conserva el limite total de ~30 s: un nodo realmente ocupado/mudo
    # falla ruidosamente y el supervisor aplica su backoff.
    for intento_arranque in range(10):
        if len(_est) > 0:
            break
        if _lector_error:
            _esperar_puerto()
        _cmd('ctl report', 0.2)
        for _ in range(6):
            if len(_est) > 0:
                break
            if _lector_error:
                _esperar_puerto()
            time.sleep(0.5)
        if len(_est) > 0:
            break
    else:
        print('SIN TELEMETRIA en 30 s: el lector no tomo %s (otro proceso lo '
              'tiene?). Se aborta en vez de colgarse en silencio.' % PUERTO,
              flush=True)
        raise SystemExit(3)



def main(repeticiones=3, ventana=240, reanudar=False,
         reintentar_invalidas=False):
    os.makedirs(SALIDA, exist_ok=True)
    crudo = os.path.join(SALIDA, 'resultados.jsonl')
    hechas = set()
    res = []
    if reanudar or reintentar_invalidas:
        res = _cargar(crudo)
        if reintentar_invalidas:
            n_invalidas = sum(1 for r in res
                              if r.get('veredicto') == 'INVALIDA')
            res = [r for r in res if r.get('veredicto') != 'INVALIDA']
            # Reescritura segura: una INVALIDA no es una medicion y no debe
            # quedar duplicada cuando su reemplazo valido se agregue abajo.
            temporal = crudo + '.tmp'
            with open(temporal, 'w', encoding='utf-8') as fh:
                for r in res:
                    fh.write(json.dumps(r, ensure_ascii=False) + '\n')
            os.replace(temporal, crudo)
            print('se retiraron %d visitas INVALIDA para repetirlas'
                  % n_invalidas, flush=True)
        hechas = {(r['pga_cod'], r['pgaout_cod'], r['vuelta']) for r in res}
        print('reanudando: %d visitas ya medidas' % len(res), flush=True)

    arrancar_enlace()

    # Cebar ANTES de cambiar la primera ganancia. Una captura pausa el control;
    # hacerla durante CONTROL_LEARNING cancelaria ese aprendizaje y restauraria
    # el perfil anterior. En este punto el firmware acaba de arrancar o sigue
    # en su perfil guardado, por lo que el cebado es inocuo.
    if not _asegurar_adquisicion():
        print('SIN ADQUISICION: los cinco taps siguen sin actualizar despues de '
              '3 cebados; se aborta antes de medir.', flush=True)
        raise SystemExit(4)

    total = repeticiones * len(CODIGOS) * len(CODIGOS)
    t_inicio = time.time()
    hecho = len(hechas)
    print('%d pares x %d vueltas = %d visitas, ventana %d s'
          % (len(CODIGOS) ** 2, repeticiones, total, ventana), flush=True)
    print('peor caso %.1f h; con corte temprano, bastante menos\n'
          % (total * ventana / 3600.0), flush=True)

    for vuelta in range(1, repeticiones + 1):
        print('=== vuelta %d de %d' % (vuelta, repeticiones), flush=True)
        for pga in range(len(CODIGOS)):
            for pgaout in range(len(CODIGOS)):
                if (pga, pgaout, vuelta) in hechas:
                    continue
                for intento_visita in range(1, 4):
                    try:
                        serie, t_banda, lp0, n0, ok = _visitar(
                            pga, pgaout, ventana)
                        break
                    except TelemetriaVencida as e:
                        if intento_visita == 3:
                            raise
                        print('    !! %s durante x%d/x%d; reset %d/2'
                              % (e, CODIGOS[pga], CODIGOS[pgaout],
                                 intento_visita), flush=True)
                        _reset_psoc_desde_esp()
                        time.sleep(30)
                        if not _asegurar_adquisicion():
                            raise RuntimeError('reset sin adquisicion valida')
                r = _analizar(pga, pgaout, serie, t_banda, lp0, n0, ventana, ok)
                r['vuelta'] = vuelta
                r['marca'] = time.strftime('%Y-%m-%d %H:%M:%S')
                res.append(r)
                hecho += 1
                # Al disco AHORA: una tanda de horas no se puede perder por un
                # Ctrl-C o un corte de luz.
                with open(crudo, 'a', encoding='utf-8') as fh:
                    fh.write(json.dumps(r, ensure_ascii=False) + '\n')
                _informe(res, os.path.join(SALIDA, 'INFORME.md'), t_inicio)
                _escribir_csv(res, os.path.join(SALIDA, 'resumen.csv'))

                transcurrido = time.time() - t_inicio
                falta = (transcurrido / hecho) * (total - hecho) if hecho else 0
                print('  x%-3d/x%-3d g=%-4d %-5s estable %-7s LPo %-7s '
                      'I=%s  [%d/%d, faltan ~%.1f h]'
                      % (CODIGOS[pga], CODIGOS[pgaout],
                         CODIGOS[pga] * CODIGOS[pgaout], r['veredicto'],
                         # ASCII a proposito: la consola de Windows no es UTF-8
                         # y un guion largo sale como basura en el log en vivo.
                         ('%.0fs' % r['t_estable_s']) if r['t_estable_s'] is not None else '-',
                         ('%.1f' % r['LPo_final_mV']) if r['LPo_final_mV'] is not None else '-',
                         r['idac_final'], hecho, total, falta / 3600.0),
                      flush=True)

    print('\nlisto: %s' % os.path.join(SALIDA, 'INFORME.md'), flush=True)


def _argumentos(argv):
    p = argparse.ArgumentParser(
        description='Barrido reanudable de las 81 combinaciones PGA/PGAout')
    p.add_argument('repeticiones', nargs='?', type=int, default=3)
    p.add_argument('ventana_s', nargs='?', type=int, default=240)
    p.add_argument('--port', help='puerto serie (o variable BARRIDO_PORT)')
    p.add_argument('--output', default=os.environ.get('BARRIDO_OUTPUT', SALIDA),
                   help='directorio de resultados')
    p.add_argument('--reanudar', action='store_true')
    p.add_argument('--reintentar-invalidas', action='store_true')
    return p.parse_args(argv)


def _pedir_salida(_signum=None, _frame=None):
    global _vivo
    _vivo = False
    raise KeyboardInterrupt


if __name__ == '__main__':
    ns = _argumentos(sys.argv[1:])
    PUERTO = ns.port or _detectar_puerto()
    SALIDA = os.path.abspath(ns.output)
    signal.signal(signal.SIGTERM, _pedir_salida)
    signal.signal(signal.SIGINT, _pedir_salida)
    print('puerto=%s salida=%s' % (PUERTO, SALIDA), flush=True)
    threading.Thread(target=_leer, daemon=True).start()
    time.sleep(1.5)
    try:
        try:
            main(repeticiones=ns.repeticiones,
                 ventana=ns.ventana_s,
                 reanudar=ns.reanudar or ns.reintentar_invalidas,
                 reintentar_invalidas=ns.reintentar_invalidas)
        except KeyboardInterrupt:
            print('\ninterrumpido; los resultados terminados quedan guardados',
                  flush=True)
    finally:
        _vivo = False
        time.sleep(0.3)
