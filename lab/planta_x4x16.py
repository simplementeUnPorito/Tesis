"""planta_x4x16.py - las dos pendientes reales, medidas EN ESTE punto.

Todo lo que se decidio hasta ahora sobre las ganancias altas salio de numeros
medidos en OTRO punto de operacion. El 2026-09-25 eso costo una prueba entera:
del estado {SUMo -28,7 mV, LPo -3,4 mV} se dedujo "el cero de LPo esta en SUMo
= -29 mV", se puso el objetivo ahi, y la etapa termino contra el riel. El
detalle que faltaba es que aquel punto tenia **IDAC3 = -242** y el punto al que
se aplico tenia **IDAC3 = +233**: 475 codigos de diferencia. Ese -29 no era una
propiedad de la etapa sino el cero *para aquel IDAC3*.

No existe "el cero de SUMo". LPo depende de los dos:

    LPo = a * SUMo + b * IDAC3 + c

Esto mide `a` y `b` donde importa, con tres precauciones que el banco ya
aprendio a los golpes:

  * NO se usa `ctl pause`: pausado el firmware deja de barrer los taps y
    ademas bloquea `ctl_write`, asi que la telemetria se congela y los
    comandos `idac` no escriben. Trece lecturas identicas al ultimo digito
    parecian una etapa saturada y eran el instrumento apagado.
  * En vez de pausar se ENSANCHA la banda muerta: dentro de ella el PI se
    congela solo, pero el barrido y los reportes siguen vivos. El lazo queda
    pasivo y el instrumento despierto.
  * Se verifica que LPo este RESPONDIENDO antes de creerle a una pendiente. Un
    tap saturado da pendiente cero y se parece mucho a "el actuador no sirve".

Uso:  python lab/planta_x4x16.py --port COM8
"""
import argparse
import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

CP_OPA_TARGET_UV = 20
CP_DEADBAND_UV = 8
CP_HOLD_UV = 36
CP_FINE_MID = 37
CP_SETTLED_BAND_UV = 41

# Ensanchar la banda muerta tiene DOS reglas de consistencia en el firmware
# (`control_config_valid`): HOLD tiene que ser estrictamente MENOR que
# DEADBAND, y SETTLED_BAND no puede ser menor que DEADBAND.  Con SETTLED_BAND
# en su valor de fabrica (60 mV), pedir DEADBAND = 95 mV hace que el `apply`
# rechace la config ENTERA -verificado por lectura: el nodo seguia diciendo
# 45000-.  Por eso se ensanchan las tres, y en este orden.
BANDA_SETTLED = 95000
BANDA_MUERTA = 90000
BANDA_HOLD = 85000
SATURADO_UV = 105000       # pasado esto la lectura ya no es de la etapa


def _param(idx):
    bt._cmd('ctl report', 0.8)
    time.sleep(1.5)
    return bt._est.get(idx)


def _set(idx, valor, nombre=''):
    bt._cmd('ctl set %d %d' % (idx, valor), 0.4)
    bt._cmd('ctl apply', 1.5)
    leido = _param(idx)
    ok = leido == valor
    print('  %-16s %d -> nodo dice %s%s'
          % (nombre or ('param %d' % idx), valor, leido,
             '' if ok else '   <-- NO TOMO'))
    return ok


def _tap():
    return (bt._est.get(bt.K_TAP + 12), bt._est.get(bt.K_TAP + 16),
            bt._est.get(bt.K_TAP + 17))


def _promedio(n=4, espera=2.0):
    su, lp = [], []
    for _ in range(n):
        time.sleep(espera)
        s, l, _v = _tap()
        if s is not None:
            su.append(s)
        if l is not None:
            lp.append(l)
    return (sum(su) / len(su) if su else None,
            sum(lp) / len(lp) if lp else None)


def barrer_idac3(base, paso, n, espera):
    print('\n--- pendiente de IDAC3 sobre LPo (SUMo fijo) ---')
    print('  %8s %11s %11s %s' % ('IDAC3', 'SUMo_mV', 'LPo_mV', ''))
    filas = []
    for k in range(n):
        c = max(-255, min(255, base + k * paso))
        bt._cmd('idac 3 %d' % c, 0.3)
        time.sleep(espera)
        su, lp = _promedio()
        if lp is None:
            continue
        sat = abs(lp) >= SATURADO_UV
        filas.append((c, su, lp, sat))
        print('  %8d %11.2f %11.2f %s'
              % (c, su / 1000.0 if su else 0, lp / 1000.0,
                 'SATURADO: esta lectura no vale' if sat else ''), flush=True)
    utiles = [f for f in filas if not f[3]]
    if len(utiles) >= 2:
        dc = utiles[-1][0] - utiles[0][0]
        dl = utiles[-1][2] - utiles[0][2]
        if dc:
            print('  b = %.3f mV por codigo de IDAC3  (%d codigos utiles)'
                  % (dl / 1000.0 / dc, dc))
            return dl / 1000.0 / dc, filas
    print('  NO se pudo medir: %d lecturas fuera de saturacion' % len(utiles))
    return None, filas


def barrer_idac1(base, espera):
    """El par lento cruza el acople de 680 uF: tau ~ 30-44 s, hay que esperar.

    Un barrido corto aca no mide la pendiente de regimen sino la instantanea,
    que en esta planta da 18,8 mV/cod cuando en regimen son 12,3."""
    print('\n--- pendiente de IDAC1 sobre SUMo y LPo ---')
    print('  %8s %11s %11s' % ('IDAC1', 'SUMo_mV', 'LPo_mV'))
    filas = []
    for c in (base, base + 1, base + 2, base):
        bt._cmd('idac 1 %d' % c, 0.3)
        time.sleep(espera)
        su, lp = _promedio()
        if su is None or lp is None:
            continue
        filas.append((c, su, lp))
        print('  %8d %11.2f %11.2f' % (c, su / 1000.0, lp / 1000.0), flush=True)
    ida = [f for f in filas[:3]]
    if len(ida) >= 2:
        dc = ida[-1][0] - ida[0][0]
        if dc:
            print('  SUMo: %.2f mV por codigo de IDAC1'
                  % ((ida[-1][1] - ida[0][1]) / 1000.0 / dc))
            print('  LPo : %.2f mV por codigo de IDAC1'
                  % ((ida[-1][2] - ida[0][2]) / 1000.0 / dc))
    return filas


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', default='COM8')
    ap.add_argument('--pga', type=int, default=2)
    ap.add_argument('--pgaout', type=int, default=4)
    ap.add_argument('--espera-rapida', type=float, default=8.0)
    ap.add_argument('--espera-lenta', type=float, default=100.0)
    ap.add_argument('--salida', default='lab/planta')
    ap.add_argument('--sin-aprender', action='store_true',
                    help='el nodo ya esta aprendido en este par: no re-aprender')
    a = ap.parse_args()

    bt.PUERTO = a.port
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        print('FALLA: sin adquisicion')
        return 3

    print('1. deshaciendo el objetivo mal puesto y volviendo a lo conocido')
    guardados = {}
    for idx, nombre, valor in ((CP_OPA_TARGET_UV, 'OPA_TARGET_UV', 0),
                               (CP_FINE_MID, 'FINE_MID', 240)):
        guardados[idx] = _param(idx)
        _set(idx, valor, nombre)

    print('\n2. re-aprendiendo con el objetivo de fabrica')
    t0 = time.time()
    if a.sin_aprender:
        print('   (saltado: el nodo ya esta aprendido en este par)')
        bt._fijar_ganancia(a.pga, a.pgaout)
        time.sleep(10)
    else:
        bt._fijar_ganancia(0, 0)
        time.sleep(40)
        bt._fijar_ganancia(a.pga, a.pgaout)
        time.sleep(3)
        bt._cmd('ctl learn', 1.0)
        while time.time() - t0 < 900 and bt._vivo:
            time.sleep(10)
            su, lp, val = _tap()
            est = bt.ESTADO.get(bt._est.get(bt.K_ESTADO), '?')
            if (est != 'APRENDIENDO' and val == 1 and lp is not None
                    and abs(lp) < 90000):
                break
    su, lp, val = _tap()
    idac = [bt._est.get(bt.K_IDAC + i) for i in range(4)]
    print('   aprendido en %.0f s: SUMo=%.2f LPo=%.2f valido=%s IDAC=%s'
          % (time.time() - t0, su / 1000.0, lp / 1000.0, val, idac))
    if val != 1:
        print('   OJO: LPo quedo fuera de ventana; las pendientes van a salir')
        print('   de una etapa saturada y NO valen.  Se mide igual para dejar')
        print('   constancia, pero el resultado hay que leerlo con eso.')

    print('\n3. ensanchando la banda muerta para que el PI se quede quieto')
    for idx, nombre, valor in (
            (CP_SETTLED_BAND_UV, 'SETTLED_BAND_UV', BANDA_SETTLED),
            (CP_DEADBAND_UV, 'DEADBAND_UV', BANDA_MUERTA),
            (CP_HOLD_UV, 'HOLD_UV', BANDA_HOLD)):
        guardados[idx] = _param(idx)
        if not _set(idx, valor, nombre):
            # Sin banda ancha el PI pelea cada paso -piso un escalon inyectado
            # en 1,5 s- y la pendiente sale contaminada.  Abortar y devolver
            # todo es mejor que medir basura con buena presentacion.
            print('   sin banda ancha la pendiente no vale: se aborta')
            for i2, v2 in guardados.items():
                if v2 is not None:
                    _set(i2, v2)
            bt._vivo = False
            return 6

    resultados = {'inicial': {'sumo_uv': su, 'lpo_uv': lp, 'idac': idac}}
    try:
        base3 = bt._est.get(bt.K_IDAC + 3) or 0
        b, filas3 = barrer_idac3(base3 - 80, 20, 9, a.espera_rapida)
        bt._cmd('idac 3 %d' % base3, 0.3)
        time.sleep(a.espera_rapida)
        resultados['idac3'] = {'pendiente_mV_por_codigo': b, 'filas': filas3}

        base1 = bt._est.get(bt.K_IDAC + 1) or 0
        filas1 = barrer_idac1(base1, a.espera_lenta)
        resultados['idac1'] = {'filas': filas1}
    finally:
        print('\n4. devolviendo todo a como estaba')
        for idx, valor in guardados.items():
            if valor is not None:
                _set(idx, valor)
        os.makedirs(a.salida, exist_ok=True)
        with open(os.path.join(a.salida, 'planta.json'), 'w',
                  encoding='utf-8') as fh:
            json.dump(resultados, fh, ensure_ascii=False, indent=1)
        bt._vivo = False
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
