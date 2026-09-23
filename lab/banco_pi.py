"""banco_pi.py - banco de pruebas del lazo PI: devuelve veredictos, no logs.

    py -3 banco_pi.py arranque     tiempo hasta banda desde un reset del PSoC
    py -3 banco_pi.py ganancias    barrido de pares de ganancia
    py -3 banco_pi.py estado       foto del lazo ahora

Todo va por la consola USB del esclavo (COM8). El maestro queda fuera a
proposito: su USB se traba y se des-enumera solo (2026-09-18), y para probar el
lazo no hace falta radio.

Criterio de exito: el lazo declara BANDA y ademas |LPo| se queda dentro de la
ventana hasta el final. "Volvio a banda" y "quedo bien" no son lo mismo: un
rescate puede cruzar de un riel al otro y marcar banda al pasar.
"""
import sys, time, threading, re, subprocess, serial

PUERTO = 'COM8'
CODIGOS = [1, 2, 4, 8, 16, 24, 32, 48, 50]
K_ESTADO, K_BANDA = 0x100, 0x102
K_SUMO, K_LPO = 0x12C, 0x130
K_I2, K_I3 = 0x112, 0x113
VENTANA_UV = 97000

_est = {}
_vivo = True
_puerto = {}


def _leer():
    s = serial.Serial()
    s.port = PUERTO
    s.baudrate = 115200
    s.timeout = 0.3
    s.dtr = False
    s.rts = False
    # El puerto puede quedar tomado unos segundos por la corrida anterior o por
    # el flasheo; reintentar es mas barato que perder un barrido de una hora.
    for intento in range(30):
        try:
            s.open()
            break
        except Exception as e:
            if intento == 29:
                print('NO ABRE %s: %s' % (PUERTO, e), flush=True)
                raise SystemExit(2)
            time.sleep(2)
    _puerto['s'] = s
    while _vivo:
        ln = s.readline().decode('utf-8', 'replace')
        m = re.search(r'#CTL 0 (\d+) (-?\d+)', ln)
        if m:
            _est[int(m.group(1))] = int(m.group(2))
    s.close()


def _cmd(texto, espera=1.5):
    # La espera tiene que cubrir los reintentos del lector (30 x 2 s), o el
    # primer comando sale antes de que el puerto exista y todo el barrido
    # muere con KeyError.
    for _ in range(150):
        if 's' in _puerto:
            break
        time.sleep(0.5)
    if 's' not in _puerto:
        print('NO ABRE %s: el lector nunca tomo el puerto' % PUERTO, flush=True)
        raise SystemExit(2)
    _puerto['s'].write((texto + chr(10)).encode())
    time.sleep(espera)


def _fijar_ganancia(pga, pgaout, intentos=3):
    """Pone el par y EXIGE que el firmware confirme los dos codigos.

    Mandar el comando no alcanza: el 2026-09-19 `pgaout` mandaba PGAVDAC por un
    `else` de mas en el ESP, no cambiaba nada, y este banco midio horas un eje
    congelado sin dar una sola senal de error. `ctl get 0` y `ctl get 1` hacen
    que el PSoC emita CP_PGA y CP_PGAOUT en el acto."""
    for _ in range(intentos):
        _est.pop(0, None); _est.pop(1, None)
        _cmd('pga %d' % pga)
        _cmd('pgaout %d' % pgaout)
        for _ in range(3):
            _cmd('ctl get 0', 0.4)
            _cmd('ctl get 1', 0.4)
            for _ in range(15):
                if _est.get(0) == pga and _est.get(1) == pgaout:
                    return True
                time.sleep(0.2)
    return False


def _mv(k):
    return _est[k] / 1000.0 if k in _est else None


def _esperar_banda(limite_s, muestreo=5, firmes=12):
    """Espera hasta que el veredicto este DECIDIDO, no hasta que se acabe la
    ventana. Un par que ya declaro banda y lleva `firmes` muestras seguidas
    adentro y quieto no va a cambiar de veredicto por esperarlo mas, y esperarlo
    igual multiplica por cinco lo que tarda un barrido. Los que fallan si
    consumen la ventana entera: ahi la espera es la prueba."""
    t0 = time.time()
    t_banda = None
    serie = []
    while time.time() - t0 < limite_s:
        time.sleep(muestreo)
        lp = _mv(K_LPO)
        if lp is not None:
            serie.append((round(time.time() - t0), lp))
        if t_banda is None and _est.get(K_BANDA) == 1:
            t_banda = round(time.time() - t0)
        if t_banda is not None and len(serie) >= firmes:
            ult = [v for _, v in serie[-firmes:]]
            if (all(abs(v) * 1000 <= VENTANA_UV for v in ult) and
                    max(ult) - min(ult) < 30.0):
                break
    return t_banda, serie


def _t_estable(serie):
    """Instante desde el cual LPo ya NO vuelve a salir de la ventana. El
    't_banda' del firmware marca el primer cruce, y un rescate que cruza de un
    riel al otro marca banda al pasar: ese numero miente sobre cuanto tardo en
    quedarse. Este es el que va a la tabla."""
    ultimo_afuera = None
    for t, v in serie:
        if abs(v) * 1000 > VENTANA_UV:
            ultimo_afuera = t
    if ultimo_afuera is None:
        return serie[0][0]
    for t, _ in serie:
        if t > ultimo_afuera:
            return t
    return None


def _veredicto(t_banda, serie, cola=6):
    if not serie:
        return 'FALLA (sin datos)'
    ultimos = [v for _, v in serie[-cola:]]
    dentro = all(abs(v) * 1000 <= VENTANA_UV for v in ultimos)
    quieto = (max(ultimos) - min(ultimos)) < 30.0
    if t_banda is None:
        return 'FALLA (nunca declaro banda; LPo final %.1f mV)' % ultimos[-1]
    if not dentro:
        return 'FALLA (banda a los %ds pero termino en %.1f mV)' % (t_banda, ultimos[-1])
    est = _t_estable(serie)
    return 'PASA (estable %ss, 1er cruce %ds, LPo %.1f mV, %s)' % (
        est, t_banda, ultimos[-1], 'quieto' if quieto else 'aun moviendose')


def prueba_arranque():
    subprocess.run(['powershell', '-NoProfile', '-File',
                    r'C:\Github\Tesis\src\firmware\psoc\reset_psoc.ps1'],
                   capture_output=True)
    _est.clear()
    t_banda, serie = _esperar_banda(200)
    print('  LPo:', ' '.join('%ds:%.0f' % p for p in serie[::3]))
    print('ARRANQUE:', _veredicto(t_banda, serie))


def prueba_ganancias(pares=((8, 0), (3, 3), (2, 5), (2, 3), (4, 2), (5, 2)),
                     vueltas=1, ventana=520):
    """Barrido de pares. Con vueltas=2 la segunda pasada mide lo que tarda al
    VOLVER a un par ya visitado, que es el caso de uso real y el que aprovecha
    la memoria de puntos de trabajo del firmware.

    Ojo: cada par arranca donde lo dejo el anterior, asi que los tiempos no son
    comparables entre corridas distintas. Por eso se informa LPo de partida."""
    print('%-11s %-7s %s' % ('par', 'LPo0', 'veredicto'))
    print('-' * 78)
    for vuelta in range(vueltas):
        if vueltas > 1:
            print('--- vuelta %d' % (vuelta + 1), flush=True)
        for pga, pgaout in pares:
            lp0 = _mv(K_LPO)
            if not _fijar_ganancia(pga, pgaout):
                print('x%-3d/x%-4d %-7s INVALIDA (el firmware no tomo la ganancia)'
                      % (CODIGOS[pga], CODIGOS[pgaout], ''), flush=True)
                continue
            _est.clear()
            t_banda, serie = _esperar_banda(ventana)
            print('x%-3d/x%-4d %-7s %s' % (
                CODIGOS[pga], CODIGOS[pgaout],
                ('%.0f' % lp0) if lp0 is not None else '?',
                _veredicto(t_banda, serie)), flush=True)
            # traza cruda: sin esto un FALLA no dice si se quedo corto,
            # si se paso, o si nunca se movio.
            print('      LPo:', ' '.join('%d:%.0f' % p for p in serie[::4]),
                  flush=True)


def prueba_convergencia(pga=2, pgaout=5, segundos=300):
    """Forma de la convergencia en un par: donde se planta y si el vernier
    sigue moviendose cuando LPo se queda quieto."""
    _cmd('pga %d' % pga)
    _cmd('pgaout %d' % pgaout)
    _est.clear()
    t0 = time.time()
    serie = []
    while time.time() - t0 < segundos:
        time.sleep(2)
        if K_LPO in _est:
            serie.append((round(time.time() - t0), _mv(K_LPO), _est.get(K_I3), _est.get(0x110), _mv(K_SUMO), _est.get(0x111)))
    print('par x%d/x%d' % (CODIGOS[pga], CODIGOS[pgaout]))
    print('  LPo :', ' '.join('%d:%.0f' % (t, v) for t, v, _, _, _, _ in serie[::10]))
    print('  I3  :', ' '.join('%d:%s' % (t, i) for t, _, i, _, _, _ in serie[::10]))
    print('  I0/I1:', ' '.join('%d:%s/%s' % (t, a, b) for t, _, _, a, _, b in serie[::10]))
    print('  SUMo:', ' '.join('%d:%.0f' % (t, v) for t, _, _, _, v, _ in serie[::10] if v is not None))
    fin = [v for _, v, _, _, _, _ in serie[-30:]]
    i3f = [i for _, _, i, _, _, _ in serie[-30:] if i is not None]
    print('  ultimo minuto: LPo %.1f..%.1f mV, IDAC3 %s..%s' % (
        min(fin), max(fin), min(i3f) if i3f else '?', max(i3f) if i3f else '?'))


def prueba_estado():
    time.sleep(8)
    print('estado=%s banda=%s LPo=%s SUMo=%s I2=%s I3=%s' % (
        _est.get(K_ESTADO), _est.get(K_BANDA), _mv(K_LPO), _mv(K_SUMO),
        _est.get(K_I2), _est.get(K_I3)))


if __name__ == '__main__':
    threading.Thread(target=_leer, daemon=True).start()
    time.sleep(1.5)
    que = sys.argv[1] if len(sys.argv) > 1 else 'estado'
    extra = [int(a) for a in sys.argv[2:]]
    if que == 'ganancias' and extra:
        prueba_ganancias(vueltas=extra[0], ventana=extra[1] if len(extra) > 1 else 520)
        _vivo = False
        time.sleep(0.3)
        raise SystemExit
    if que == 'convergencia' and extra:
        prueba_convergencia(*extra)
        _vivo = False
        time.sleep(0.3)
        raise SystemExit
    {'arranque': prueba_arranque,
     'convergencia': prueba_convergencia,
     'ganancias': prueba_ganancias,
     'estado': prueba_estado}[que]()
    _vivo = False
    time.sleep(0.3)
