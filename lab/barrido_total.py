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
CP_COUNT = 47                                    # los parametros llegan en 0..46

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
_vivo = True
_puerto = {}
_serial_lock = threading.Lock()
_lector_error = None
_ultimo_ctl = 0.0


class TelemetriaVencida(RuntimeError):
    pass


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


def _leer():
    """Hilo lector: mantiene `_est` con el ultimo valor de cada clave."""
    global _lector_error, _ultimo_ctl
    s = serial.Serial()
    s.port, s.baudrate, s.timeout = PUERTO, BAUD, 0.3
    s.dtr = s.rts = False
    if os.name != 'nt':
        # Evita que dos barridos abran simultaneamente el mismo adaptador.
        s.exclusive = True
    for intento in range(30):
        try:
            s.open(); break
        except Exception as e:
            if intento == 29:
                _lector_error = 'NO ABRE %s: %s' % (PUERTO, e)
                print(_lector_error, flush=True)
                return
            time.sleep(2)
    _puerto['s'] = s
    patron = re.compile(r'#CTL 0 (\d+) (-?\d+)')
    try:
        while _vivo:
            m = patron.search(s.readline().decode('utf-8', 'replace'))
            if m:
                _est[int(m.group(1))] = int(m.group(2))
                _ultimo_ctl = time.monotonic()
    except Exception as e:
        if _vivo:
            _lector_error = 'se perdio %s: %s' % (PUERTO, e)
            print(_lector_error, flush=True)
    finally:
        s.close()


def _cmd(texto, espera=1.5):
    for _ in range(150):
        if 's' in _puerto:
            break
        time.sleep(0.5)
    if 's' not in _puerto:
        print('NO ABRE %s: el lector nunca tomo el puerto' % PUERTO, flush=True)
        raise SystemExit(2)
    if _lector_error:
        raise RuntimeError(_lector_error)
    with _serial_lock:
        _puerto['s'].write((texto + '\n').encode())
        _puerto['s'].flush()
    time.sleep(espera)


def _reset_psoc_desde_esp():
    """Pide al ESP el pulso GPIO19 que reinicia al PSoC.

    No usa KitProg, PSoC Creator ni scripts del host. Por eso funciona igual
    desde Windows o desde un servidor Linux conectado al USB del ESP32.
    """
    global _ultimo_ctl
    _cmd('psocreset', 0.2)
    _est.clear()                       # no aceptar telemetria anterior al reset
    _ultimo_ctl = 0.0


def _foto():
    """Una muestra de todo lo que interesa, en el instante actual."""
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
    }


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


def _visitar(pga, pgaout, ventana, muestreo=2.0, firmes=15, limite_mult=4):
    """Cambia a ese par y lo observa hasta que el veredicto este decidido.

    `firmes` muestras seguidas dentro de la ventana y quietas bastan para
    declararlo: esperar mas no cambia el veredicto y multiplica lo que tarda
    el barrido. Las que fallan si consumen la ventana entera, porque ahi la
    espera ES la prueba."""
    lp0 = _est.get(K_TAP + 16)
    lp0 = lp0 / 1000.0 if lp0 is not None else None
    n_antes = _est.get(K_AUTOSAVE)

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
    while time.time() - t0 < tope:
        time.sleep(muestreo)
        f = _foto()
        f['t'] = round(time.time() - t0, 1)
        serie.append(f)
        if t_banda is None and f['banda'] == 1:
            t_banda = f['t']
        if t_banda is not None and len(serie) >= firmes:
            ult = [x['tap'][4] for x in serie[-firmes:] if x['tap'][4] is not None]
            if (len(ult) == firmes and
                    all(abs(v) <= VENTANA_UV for v in ult) and
                    max(ult) - min(ult) < 30000):
                break
        # PRORROGA 1.  Un par que aterriza justo antes de que se acabe la
        # ventana no alcanza a demostrar que se sostiene, y quedaba marcado
        # FALLA con LPo centrado: medido x4/x8, estable a los 216 s de una
        # ventana de 240 y con LPo en -2,1 mV.  Eso no es un fallo, es un par
        # lento.  Se estira lo justo para que pueda probarlo.
        lp = f['tap'][4]
        if (tope == ventana and time.time() - t0 >= ventana - muestreo * 2 and
                lp is not None and abs(lp) <= VENTANA_UV):
            tope = ventana + muestreo * (firmes + 2)
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

    lp = col('tap', 4)
    # Desde cuando LPo ya NO vuelve a salir: el 't_banda' del firmware marca el
    # primer cruce, y un rescate que cruza de riel a riel lo marca al pasar.
    t_estable, ultimo_afuera = None, None
    for f in serie:
        v = f['tap'][4]
        if v is not None and abs(v) > VENTANA_UV:
            ultimo_afuera = f['t']
    if lp:
        if ultimo_afuera is None:
            t_estable = serie[0]['t']
        else:
            for f in serie:
                if f['t'] > ultimo_afuera:
                    t_estable = f['t']; break

    cola = lp[-15:] if len(lp) >= 15 else lp
    dentro = bool(cola) and all(abs(v) <= VENTANA_UV for v in cola)
    quieto = bool(cola) and (max(cola) - min(cola)) < 30000
    pasa = dentro and t_banda is not None and t_estable is not None

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
    campos = ['vuelta', 'pga', 'pgaout', 'ganancia', 'veredicto', 't_banda_s',
              't_estable_s', 'LPo_inicial_mV', 'LPo_final_mV',
              'LPo_pp_final_mV', 'I0', 'I1', 'I2', 'I3', 'aprendizajes',
              'objetivo_sumo_uV', 'factor_pendiente_lenta_x1000']
    with open(ruta, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        for r in res:
            fila = {k: r.get(k) for k in campos if k in r}
            fila['vuelta'] = r.get('vuelta')
            for i in range(4):
                fila['I%d' % i] = (r['idac_final'][i]
                                   if r.get('idac_final') else None)
            w.writerow(fila)


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
            raise RuntimeError(_lector_error)
        _cmd('ctl report', 0.2)
        for _ in range(6):
            if len(_est) > 0:
                break
            if _lector_error:
                raise RuntimeError(_lector_error)
            time.sleep(0.5)
        if len(_est) > 0:
            break
    else:
        print('SIN TELEMETRIA en 30 s: el lector no tomo %s (otro proceso lo '
              'tiene?). Se aborta en vez de colgarse en silencio.' % PUERTO,
              flush=True)
        raise SystemExit(3)

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
