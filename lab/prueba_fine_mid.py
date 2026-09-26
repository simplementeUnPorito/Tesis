"""prueba_fine_mid.py - a que altura hay que descargar el vernier.

`CP_FINE_MID` es el umbral a partir del cual el firmware le saca carga a IDAC3
y se la pasa a IDAC2, que tiene mucha mas autoridad.  Esta en **240 de 255**:
el 94 % del rango.  O sea que el alivio recien llega cuando al actuador fino
ya no le queda nada, y mientras tanto el lazo puede plantarse en 174 o en 234
-medido el 2026-09-25 a x4/x16- y quedarse ahi, en banda pero sin margen para
absorber una deriva termica.

Esto mide, para varios valores del umbral, tres cosas sobre el MISMO par:

    |IDAC3| final   cuanto margen le quedo al actuador fino
    pico a pico     si se quedo quieto de verdad
    t_estable       cuanto tardo en entrar en banda

No hace falta reflashear: `ctl set` + `ctl apply` cambian el valor en caliente
y no se persiste salvo que alguien mande `ctl save`.  Al terminar se devuelve
el valor original, pase lo que pase.

Cada condicion se mide dos veces y en orden ida y vuelta (A B C C B A) porque
la placa deriva: medir todas las A y despues todas las B mezclaria el efecto
del umbral con el paso del tiempo.

Uso:  python lab/prueba_fine_mid.py --port COM8 --valores 240 120 60
"""
import argparse
import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

CP_FINE_MID = 37
PAR_NEUTRO = (0, 0)          # x1/x1: desde aca se entra a todo


def _set(idx, valor):
    """Deja un parametro y verifica que el nodo lo haya tomado.

    Verificar es obligatorio, no una cortesia: `ctl set` solo STAGEA, el valor
    recien vive despues de `apply`, y ya se perdio un dia entero de mediciones
    con un eje congelado por no comprobar que la consigna cambio."""
    bt._cmd('ctl set %d %d' % (idx, valor), 0.4)
    bt._cmd('ctl apply', 1.5)
    bt._cmd('ctl report', 0.8)
    time.sleep(1.5)
    leido = bt._est.get(idx)
    if leido != valor:
        print('    !! se pidio %s=%d y el nodo dice %s' % (idx, valor, leido))
        return False
    return True


def _medir(pga, pgaout, ventana):
    bt._fijar_ganancia(*PAR_NEUTRO)
    time.sleep(60)
    serie, t_banda, lp0, n0, ok = bt._visitar(pga, pgaout, ventana)
    return bt._analizar(pga, pgaout, serie, t_banda, lp0, n0, ventana, ok)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', default='COM8')
    ap.add_argument('--pga', type=int, default=2)
    ap.add_argument('--pgaout', type=int, default=4)
    ap.add_argument('--valores', type=int, nargs='+', default=[240, 120, 60])
    ap.add_argument('--ventana', type=int, default=420)
    ap.add_argument('--salida', default='lab/fine_mid')
    a = ap.parse_args()

    bt.PUERTO = a.port
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        print('FALLA: sin adquisicion')
        return 3

    bt._cmd('ctl report', 0.8)
    time.sleep(1.5)
    original = bt._est.get(CP_FINE_MID)
    print('CP_FINE_MID original: %s' % original)
    if original is None:
        print('FALLA: el nodo no reporta CP_FINE_MID')
        return 4

    os.makedirs(a.salida, exist_ok=True)
    crudo = os.path.join(a.salida, 'resultados.jsonl')
    # Ida y vuelta: cancela la deriva lineal de la placa.
    orden = list(a.valores) + list(reversed(a.valores))
    print('orden (ida y vuelta): %s' % orden)
    print()
    print('%-8s %-9s %-5s %-6s %-8s %-7s %-7s %s'
          % ('FINE_MID', 'estricto', 'nota', 'fragil', 't_est', 'pp_mV',
             'LPo_mV', 'IDAC final'))
    try:
        for valor in orden:
            if not bt._vivo:
                break
            if not _set(CP_FINE_MID, valor):
                continue
            v = _medir(a.pga, a.pgaout, a.ventana)
            v['fine_mid'] = valor
            v['marca'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            with open(crudo, 'a', encoding='utf-8') as fh:
                fh.write(json.dumps(v, ensure_ascii=False) + '\n')
                fh.flush()
                os.fsync(fh.fileno())
            print('%-8d %-9s %-5s %-6s %-8s %-7s %-7s %s'
                  % (valor, v['veredicto_estricto'], v['nota'], v['fragil'],
                     v['t_estable_s'], v['LPo_pp_final_mV'],
                     v['LPo_final_mV'], v['idac_final']), flush=True)
    finally:
        # Devolver el valor original SIEMPRE: si esto queda a medias, la
        # campana que viene despues mide un lazo distinto sin saberlo.
        if bt._vivo:
            _set(CP_FINE_MID, original)
            print('\nCP_FINE_MID devuelto a %s' % original)
        bt._vivo = False
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
