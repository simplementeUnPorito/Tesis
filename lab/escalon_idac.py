"""escalon_idac.py - autoridad de CUALQUIER IDAC sobre TODOS los taps.

Generaliza `escalon_idac3.py`.  La pregunta que contesta es siempre la misma
-cuantos mV mueve un codigo de este actuador, en cada punto de la cadena- pero
ahora para los cuatro IDAC y a la ganancia que se pida, que es lo unico que
permite separar que escala con que.

## Por que tanta ceremonia

Cada una de estas precauciones esta porque su ausencia ya produjo un numero
falso en este banco:

* **El PI se congela ensanchando la banda muerta, nunca con `ctl pause`.**
  Pausado, el firmware deja de barrer los taps Y bloquea `ctl_write`: la
  telemetria se congela y los comandos `idac` no escriben.  Trece lecturas
  identicas al ultimo digito parecian una etapa saturada y era el instrumento
  apagado.
* **Se espera REGIMEN, no un valor.**  Arrancar con LPo "dentro de banda" pero
  derivando 8 mV/min arrastra 48 mV en una permanencia de 360 s y se come el
  escalon.  Un valor no dice nada sobre una tasa.
* **Se verifica que la inyeccion llego**, leyendo el codigo de vuelta despues
  de forzar un `ctl report`.  Los codigos de IDAC viajan solo en el reporte
  periodico; leer antes devuelve la foto anterior y da falsos negativos.
* **Se apaga el recentrado lento**, que mueve un codigo cada `CP_RECENTER_MS`
  aun con el PI congelado y corre el escalon por debajo.
* **Esquema A-B-A-B-A** con el estimador que compara cada B contra el promedio
  de la A anterior y la posterior: eso cancela la deriva lineal.  Promediar
  (B1-A1) con (B2-A2) NO la cancela, las dos quedan sesgadas igual.
* **Sondeo adaptativo**: antes del escalon grande se prueba uno chico y se
  mide cuanto movio, para dimensionar el grande sin clavar una etapa contra
  el riel.  A PGA x50 un escalon a ciegas satura la cadena.

## Uso

    python lab/escalon_idac.py --idac 0 --pga 2 --pgaout 4
    python lab/escalon_idac.py --idac 2 --pga 0 --pgaout 5 --salida x1x24.json

Devuelve, por cada tap, los mV por codigo con su dispersion entre las dos
estimaciones.  Si las dos difieren mucho, lo dice en vez de promediar.
"""
import argparse
import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

CP_DEADBAND_UV, CP_HOLD_UV = 8, 36
CP_SETTLED_BAND_UV, CP_RECENTER_MS = 41, 46

ANCHAS = ((CP_SETTLED_BAND_UV, 95000), (CP_DEADBAND_UV, 90000),
          (CP_HOLD_UV, 85000))
FABRICA = ((CP_HOLD_UV, 25000), (CP_DEADBAND_UV, 45000),
           (CP_SETTLED_BAND_UV, 60000))
NOMBRE_CP = {8: 'DEADBAND_UV', 36: 'HOLD_UV', 41: 'SETTLED_BAND_UV',
             46: 'RECENTER_MS'}
TAPS = ('SEo', 'BPo', 'OPA_SUM', 'SUM', 'LP')
# Pasado esto la lectura ya no es de la etapa sino de su limite.
SATURADO_UV = 105000
TOLERANCIA_CODIGOS = 3


def poner(idx, valor, intentos=4):
    for k in range(intentos):
        bt._sink = []
        bt._cmd('ctl set %d %d' % (idx, valor), 0.8)
        bt._cmd('ctl apply', 2.0)
        acks = [l.strip() for l in bt._sink if 'CTL_ACK' in l]
        bt._sink = None
        bt._cmd('ctl report', 0.8)
        time.sleep(1.5)
        if bt._est.get(idx) == valor:
            return True
        if k == intentos - 1:
            print('  %-16s %d -> %s  %s'
                  % (NOMBRE_CP.get(idx, idx), valor, bt._est.get(idx), acks))
    return False


def leer_taps():
    """Los cinco taps en uV, con su bandera de validez."""
    v, ok = [], []
    for i in range(5):
        v.append(bt._est.get(bt.K_TAP + 4 * i))
        ok.append(bt._est.get(bt.K_TAP + 4 * i + 1))
    return v, ok


def observar(segundos, etiqueta, paso=5.0):
    serie = []
    t0 = time.time()
    while time.time() - t0 < segundos and bt._vivo:
        time.sleep(paso)
        v, ok = leer_taps()
        if all(x is None for x in v):
            continue
        serie.append({'t': round(time.time() - t0, 1), 'taps': v,
                      'valido': ok,
                      'idac': [bt._est.get(bt.K_IDAC + i) for i in range(4)]})
    if serie:
        u = serie[-1]
        print('  %-10s %s' % (etiqueta, '  '.join(
            '%s=%s' % (TAPS[i], '%.1f' % (u['taps'][i] / 1000.0)
                       if u['taps'][i] is not None else '-')
            for i in range(5))), flush=True)
    return serie


def cola(serie, tap, n=6):
    """Promedio del final de un tramo para un tap: el valor ya asentado."""
    xs = [f['taps'][tap] for f in serie[-n:] if f['taps'][tap] is not None]
    return sum(xs) / len(xs) if xs else None


def inyectar(idac, codigo):
    """Escribe y VERIFICA, con reporte fresco de por medio."""
    bt._cmd('idac %d %d' % (idac, codigo), 0.4)
    time.sleep(1.5)
    bt._cmd('ctl report', 0.8)
    time.sleep(1.5)
    leido = bt._est.get(bt.K_IDAC + idac)
    if leido is None or abs(leido - codigo) > TOLERANCIA_CODIGOS:
        print('  !! se pidio IDAC%d=%d y el nodo dice %s' % (idac, codigo, leido))
        return False
    return True


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', default='COM8')
    ap.add_argument('--idac', type=int, required=True, choices=(0, 1, 2, 3))
    ap.add_argument('--pga', type=int, default=2)
    ap.add_argument('--pgaout', type=int, default=4)
    ap.add_argument('--escalon', type=int, default=0,
                    help='codigos; 0 = dimensionar con el sondeo adaptativo')
    ap.add_argument('--objetivo-mv', type=float, default=40.0,
                    help='cuanto se quiere mover el tap de referencia')
    ap.add_argument('--tap-referencia', type=int, default=4,
                    help='tap con el que se dimensiona el escalon (def. LP)')
    ap.add_argument('--permanencia', type=float, default=360.0)
    ap.add_argument('--ventana-regimen', type=float, default=180.0)
    ap.add_argument('--deriva-max', type=float, default=1.0)
    ap.add_argument('--espera-regimen', type=float, default=1800.0)
    ap.add_argument('--salida', default=None)
    a = ap.parse_args()

    bt.PUERTO = a.port
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        print('FALLA: sin adquisicion')
        return 3
    if not bt._fijar_ganancia(a.pga, a.pgaout):
        print('FALLA: el nodo no confirma la ganancia')
        return 3
    print('IDAC%d a PGA x%d / PGAout x%d'
          % (a.idac, bt.CODIGOS[a.pga], bt.CODIGOS[a.pgaout]))

    # 1. Congelar el PI PRIMERO.  Al reves no converge: con la config de
    #    fabrica hay pares que no se asientan nunca, asi que la tasa de deriva
    #    nunca baja del umbral.  Lo que tiene que quedar quieto es la PLANTA.
    guardados = {}
    for idx, val in ANCHAS:
        guardados[idx] = bt._est.get(idx)
        if not poner(idx, val):
            print('FALLA: sin banda ancha el PI pelea el escalon; se aborta')
            for i2, v2 in FABRICA:
                poner(i2, v2)
            return 4
    guardados[CP_RECENTER_MS] = bt._est.get(CP_RECENTER_MS)
    if guardados[CP_RECENTER_MS]:
        poner(CP_RECENTER_MS, 0)
    print('  PI congelado: DEADBAND=%s HOLD=%s SETTLED=%s recentrado=%s'
          % (bt._est.get(8), bt._est.get(36), bt._est.get(41),
             bt._est.get(46)))

    datos = {'idac': a.idac, 'pga': bt.CODIGOS[a.pga],
             'pgaout': bt.CODIGOS[a.pgaout], 'taps': list(TAPS), 'tramos': []}
    try:
        # 2. Esperar REGIMEN de la planta.
        print('esperando regimen (deriva <= %.1f mV/min en %s)'
              % (a.deriva_max, TAPS[a.tap_referencia]))
        t0, tasa = time.time(), None
        while time.time() - t0 < a.espera_regimen and bt._vivo:
            v = observar(a.ventana_regimen, 'sondeo', paso=10.0)
            xs = [(f['t'], f['taps'][a.tap_referencia]) for f in v
                  if f['taps'][a.tap_referencia] is not None]
            if len(xs) < 3 or xs[-1][0] <= xs[0][0]:
                continue
            tasa = ((xs[-1][1] - xs[0][1]) / 1000.0
                    / ((xs[-1][0] - xs[0][0]) / 60.0))
            print('    deriva %.2f mV/min' % tasa, flush=True)
            if abs(tasa) <= a.deriva_max:
                break
        if tasa is None or abs(tasa) > a.deriva_max:
            print('FALLA: no llego a regimen; medir aca daria la deriva, no '
                  'el actuador')
            return 5
        datos['deriva_mV_min'] = tasa

        base = bt._est.get(bt.K_IDAC + a.idac)
        datos['base'] = base

        # 3. Sondeo adaptativo: un escalon CHICO para dimensionar el grande.
        #    A ganancia alta un escalon a ciegas satura la cadena y se mide el
        #    riel en vez del actuador.
        paso = a.escalon
        if not paso:
            for prueba in (5, 15, 40):
                destino = max(-255, min(255, base - prueba))
                if destino == base or not inyectar(a.idac, destino):
                    continue
                v0 = cola(observar(90.0, 'sondeo %+d' % (destino - base)),
                          a.tap_referencia)
                inyectar(a.idac, base)
                observar(90.0, 'vuelta')
                v1 = cola(observar(30.0, 'ref'), a.tap_referencia)
                if v0 is None or v1 is None:
                    continue
                mv_cod = abs(v0 - v1) / 1000.0 / abs(destino - base)
                print('  sondeo: %.4f mV por codigo (parcial, 90 s)' % mv_cod)
                if mv_cod > 0.001:
                    paso = int(max(4, min(200, a.objetivo_mv / mv_cod)))
                    break
            if not paso:
                print('FALLA: el sondeo no detecto respuesta; no se puede '
                      'dimensionar el escalon')
                return 6
        alto = max(-255, min(255, base - paso))
        print('\nescalon: IDAC%d %d -> %d (%+d codigos)'
              % (a.idac, base, alto, alto - base))
        datos['alto'] = alto

        # 4. A-B-A-B-A
        for codigo, etiqueta in ((base, 'A1'), (alto, 'B1'), (base, 'A2'),
                                 (alto, 'B2'), (base, 'A3')):
            if not inyectar(a.idac, codigo):
                print('  se aborta: la inyeccion no llego')
                break
            s = observar(a.permanencia, etiqueta)
            datos['tramos'].append({'nombre': etiqueta, 'codigo': codigo,
                                    'serie': s})
            if not bt._vivo:
                break

        # 5. Estimacion por tap, cancelando la deriva lineal.
        por = {t['nombre']: t for t in datos['tramos']}
        dcod = alto - base
        datos['pendiente_mV_por_codigo'] = {}
        print('\n%-9s %12s %12s %12s %s'
              % ('tap', 'B1 vs A1A2', 'B2 vs A2A3', 'promedio', 'saturado?'))
        for i, nombre in enumerate(TAPS):
            est = []
            for b, antes, desp in (('B1', 'A1', 'A2'), ('B2', 'A2', 'A3')):
                if not all(k in por for k in (b, antes, desp)):
                    continue
                vb = cola(por[b]['serie'], i)
                va = cola(por[antes]['serie'], i)
                vd = cola(por[desp]['serie'], i)
                if None in (vb, va, vd):
                    continue
                est.append((vb - (va + vd) / 2.0) / 1000.0 / dcod)
            sat = any(abs(f['taps'][i]) >= SATURADO_UV
                      for t in datos['tramos'] for f in t['serie']
                      if f['taps'][i] is not None)
            if est:
                prom = sum(est) / len(est)
                datos['pendiente_mV_por_codigo'][nombre] = {
                    'valor': prom, 'estimaciones': est, 'saturado': sat}
                print('%-9s %12s %12s %12.4f %s'
                      % (nombre,
                         '%.4f' % est[0] if len(est) > 0 else '-',
                         '%.4f' % est[1] if len(est) > 1 else '-',
                         prom,
                         'SI, no vale' if sat else ''))
            else:
                print('%-9s %12s %12s %12s' % (nombre, '-', '-', 'sin dato'))
    finally:
        print('\ndevolviendo el nodo')
        if 'base' in datos and datos['base'] is not None:
            inyectar(a.idac, datos['base'])
        for idx, val in FABRICA:
            poner(idx, val)
        if guardados.get(CP_RECENTER_MS):
            poner(CP_RECENTER_MS, guardados[CP_RECENTER_MS])
        print('  DEADBAND=%s HOLD=%s SETTLED=%s recentrado=%s'
              % (bt._est.get(8), bt._est.get(36), bt._est.get(41),
                 bt._est.get(46)))
        salida = a.salida or ('lab/autoridad/idac%d_pga%d_pgaout%d.json'
                              % (a.idac, bt.CODIGOS[a.pga],
                                 bt.CODIGOS[a.pgaout]))
        os.makedirs(os.path.dirname(salida), exist_ok=True)
        with open(salida, 'w', encoding='utf-8') as fh:
            json.dump(datos, fh, ensure_ascii=False, indent=1)
        print('  crudo en %s' % salida)
        bt._vivo = False
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
