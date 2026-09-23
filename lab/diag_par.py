"""diag_par.py - foto completa de la cadena en UN par de ganancias.

    py -3 diag_par.py <cod_pga> <cod_pgaout> [segundos]

Registra los cinco taps (SEo/BP/OPA_SUM/SUM/LP), sus banderas de validez, los
cuatro IDAC, el estado y la bandera de banda, y escribe un CSV crudo al lado
del resumen.  Existe porque banco_pi.py da veredictos y para arreglar un par
que falla hace falta ver QUE se movio y que no.
"""
import sys, time, threading, re, csv, os, serial

PUERTO = 'COM8'
CODIGOS = [1, 2, 4, 8, 16, 24, 32, 48, 50]
TAP = ['SEo', 'BP', 'OPAs', 'SUM', 'LP']
K_ESTADO, K_BANDA, K_OBJETIVO = 0x100, 0x102, 0x10A

_est, _vivo, _puerto = {}, True, {}


def _leer():
    s = serial.Serial()
    s.port, s.baudrate, s.timeout = PUERTO, 115200, 0.3
    s.dtr = s.rts = False
    for i in range(30):
        try:
            s.open(); break
        except Exception as e:
            if i == 29:
                print('NO ABRE %s: %s' % (PUERTO, e), flush=True); os._exit(2)
            time.sleep(2)
    _puerto['s'] = s
    while _vivo:
        m = re.search(r'#CTL 0 (\d+) (-?\d+)',
                      s.readline().decode('utf-8', 'replace'))
        if m:
            _est[int(m.group(1))] = int(m.group(2))
    s.close()


def _cmd(texto):
    for _ in range(40):
        if 's' in _puerto:
            break
        time.sleep(0.5)
    _puerto['s'].write((texto + chr(10)).encode())
    time.sleep(1.5)


def main(pga, pgaout, segundos=300):
    _cmd('pga %d' % pga)
    _cmd('pgaout %d' % pgaout)
    _est.clear()
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'diag_x%d_x%d.csv' % (CODIGOS[pga], CODIGOS[pgaout]))
    cab = ['t', 'estado', 'banda', 'obj'] + TAP + [n + '_ok' for n in TAP] + \
          ['I0', 'I1', 'I2', 'I3']
    filas = []
    t0 = time.time()
    while time.time() - t0 < segundos:
        time.sleep(2)
        f = [round(time.time() - t0), _est.get(K_ESTADO), _est.get(K_BANDA),
             _est.get(K_OBJETIVO)]
        f += [_est.get(0x120 + 4 * i) for i in range(5)]
        f += [_est.get(0x121 + 4 * i) for i in range(5)]
        f += [_est.get(0x110 + i) for i in range(4)]
        filas.append(f)
    with open(ruta, 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(cab); w.writerows(filas)

    print('par x%d/x%d  (%d muestras -> %s)' %
          (CODIGOS[pga], CODIGOS[pgaout], len(filas), ruta))
    print('%5s %3s %2s %6s %s %s' % ('t', 'est', 'bd', 'obj',
                                 ''.join('%8s' % n for n in TAP),
                                 ''.join('%5s' % n for n in ('I0', 'I1', 'I2', 'I3'))))
    paso = max(1, len(filas) // 25)
    for f in filas[::paso]:
        mv = ''.join(('%8.1f' % (v / 1000.0)) if v is not None else '       ?'
                     for v in f[4:9])
        idac = ''.join(('%5s' % v) for v in f[14:18])
        obj = ('%6.1f' % (f[3] / 1000.0)) if f[3] is not None else '     ?'
        print('%5s %3s %2s %s %s %s' % (f[0], f[1], f[2], obj, mv, idac))
    # que actuador se movio y cuanto: el diagnostico util de una corrida
    for j, n in enumerate(('I0', 'I1', 'I2', 'I3')):
        vals = [f[14 + j] for f in filas if f[14 + j] is not None]
        if vals:
            print('  %s: %d -> %d  (rango %d..%d)' %
                  (n, vals[0], vals[-1], min(vals), max(vals)))
    for i, n in enumerate(TAP):
        vals = [f[4 + i] for f in filas if f[4 + i] is not None]
        oks = [f[9 + i] for f in filas if f[9 + i] is not None]
        if vals:
            print('  %-4s %8.1f -> %8.1f mV  (%.1f..%.1f)  valido %d/%d' %
                  (n, vals[0] / 1000.0, vals[-1] / 1000.0,
                   min(vals) / 1000.0, max(vals) / 1000.0,
                   sum(1 for v in oks if v == 1), len(oks)))


if __name__ == '__main__':
    threading.Thread(target=_leer, daemon=True).start()
    time.sleep(1.5)
    a = [int(x) for x in sys.argv[1:]]
    main(*a)
    _vivo = False
    time.sleep(0.3)
    os._exit(0)
