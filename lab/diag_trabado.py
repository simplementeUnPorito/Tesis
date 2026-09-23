"""diag_trabado.py - por que el barrido no avanza: cronometra cada paso.

Imprime un sello de tiempo antes y despues de cada operacion del primer par,
asi se ve exactamente cual bloquea en vez de suponerlo.
"""
import re, threading, time, serial

PUERTO = 'COM8'
_est = {}
_vivo = [True]
_t0 = time.time()


def log(msg):
    print('[%6.1f s] %s' % (time.time() - _t0, msg), flush=True)


def _leer(s):
    p = re.compile(r'#CTL 0 (\d+) (-?\d+)')
    n = 0
    try:
        while _vivo[0]:
            ln = s.readline().decode('utf-8', 'replace')
            m = p.search(ln)
            if m:
                _est[int(m.group(1))] = int(m.group(2))
                n += 1
                if n in (1, 10, 100):
                    log('lector: %d tramas #CTL (ultima clave %s)' % (n, m.group(1)))
    except Exception as e:
        log('LECTOR MURIO: %r' % (e,))


log('abriendo puerto')
s = serial.Serial()
s.port, s.baudrate, s.timeout = PUERTO, 115200, 0.3
s.dtr = s.rts = False
s.open()
log('puerto abierto')
threading.Thread(target=_leer, args=(s,), daemon=True).start()
time.sleep(2.0)
log('claves vistas tras 2 s: %d' % len(_est))

for texto in ('pga 0', 'pgaout 0', 'ctl get 0', 'ctl get 1'):
    log('write %r ...' % texto)
    s.write((texto + '\n').encode())
    log('write %r OK' % texto)
    time.sleep(1.0)

log('esperando confirmacion PGA=0 PGAOUT=0 (hasta 20 s)')
for i in range(100):
    if _est.get(0) == 0 and _est.get(1) == 0:
        log('CONFIRMADO')
        break
    time.sleep(0.2)
else:
    log('NO confirmo: PGA=%s PGAOUT=%s' % (_est.get(0), _est.get(1)))

log('muestreando 10 s')
for i in range(5):
    time.sleep(2.0)
    log('  LP=%s estado=%s banda=%s' % (_est.get(0x130), _est.get(0x100),
                                        _est.get(0x102)))
_vivo[0] = False
time.sleep(0.5)
s.close()
log('fin')
