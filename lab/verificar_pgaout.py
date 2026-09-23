"""verificar_pgaout.py - comprueba que `pgaout N` cambie de verdad la ganancia.

El 2026-09-19 el comando `pgaout` de la consola USB del esclavo mandaba
PSOC_CMD_PGAVDAC en vez de PSOC_CMD_PGAOUT, asi que no cambiaba nada y un
barrido de horas midio un eje congelado sin dar ninguna senal de error. Esta
comprobacion existe para que eso no vuelva a pasar en silencio: pide varios
pares y exige que el firmware confirme los dos codigos con `ctl get`.
"""
import re, sys, threading, time, serial

PUERTO = 'COM8'
PARES = ((2, 5), (2, 0), (3, 3), (4, 5), (8, 1), (2, 5))

_est = {}
_vivo = [True]


def _leer(s):
    p = re.compile(r'#CTL 0 (\d+) (-?\d+)')
    while _vivo[0]:
        m = p.search(s.readline().decode('utf-8', 'replace'))
        if m:
            _est[int(m.group(1))] = int(m.group(2))


def probar(s, pga, pgaout):
    _est.pop(0, None); _est.pop(1, None)
    s.write(('pga %d\n' % pga).encode()); time.sleep(1.5)
    s.write(('pgaout %d\n' % pgaout).encode()); time.sleep(1.5)
    for _ in range(3):
        s.write(b'ctl get 0\n'); time.sleep(0.4)
        s.write(b'ctl get 1\n'); time.sleep(0.4)
        for _ in range(15):
            if _est.get(0) == pga and _est.get(1) == pgaout:
                print('  PGA=%d PGAOUT=%d  OK' % (pga, pgaout), flush=True)
                return True
            time.sleep(0.2)
    print('  PGA=%d PGAOUT=%d  <<< NO TOMO (firmware dice PGA=%s PGAOUT=%s)'
          % (pga, pgaout, _est.get(0), _est.get(1)), flush=True)
    return False


def main():
    s = serial.Serial()
    s.port, s.baudrate, s.timeout = PUERTO, 115200, 0.3
    s.dtr = s.rts = False
    for i in range(30):
        try:
            s.open(); break
        except Exception as e:
            if i == 29:
                print('NO ABRE %s: %s' % (PUERTO, e)); raise SystemExit(2)
            time.sleep(2)
    threading.Thread(target=_leer, args=(s,), daemon=True).start()
    time.sleep(1.0)
    ok = sum(probar(s, a, b) for a, b in PARES)
    _vivo[0] = False; time.sleep(0.4); s.close()
    print('\nresultado: %d de %d pares confirmados' % (ok, len(PARES)))
    return 0 if ok == len(PARES) else 1


if __name__ == '__main__':
    sys.exit(main())
