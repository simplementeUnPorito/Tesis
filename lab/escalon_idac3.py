"""escalon_idac3.py - la ganancia de continua de IDAC3, medida bien.

Un barrido monotono de IDAC3 con 8 s por paso dio 0,129 mV/codigo el
2026-09-25.  Ese numero NO es confiable y la razon esta anotada dos veces en
este proyecto: en esta planta los barridos monotonos miden deriva, y esperar
poco sobre una etapa lenta da la pendiente INSTANTANEA y no la de regimen
(ya paso: 18,8 mV/cod medidos contra 12,3 reales).

La prueba de que ahi habia deriva: con el lazo corriendo se vio LPo oscilando
+-90 mV mientras IDAC3 se movia tres codigos en mil segundos.  O sea que LPo
se mueve solo, y en un barrido rapido buena parte del cambio que uno le
atribuye al actuador es esa cola.

Aca se mide de la unica forma que separa las dos cosas:

  * permanencias LARGAS (varias constantes de tiempo), no 8 s;
  * escalones ALTERNADOS A-B-A-B, que cancelan la deriva lineal y ademas
    dicen si el efecto se repite -si la ida y la vuelta no coinciden, lo que
    se esta midiendo no es el actuador-;
  * un tramo inicial SIN tocar nada, para medir cuanto deriva por su cuenta y
    poder compararlo con el efecto del escalon.  Si la deriva es del mismo
    orden que el efecto, el numero no sirve y hay que decirlo.

El PI se deja pasivo ensanchando la banda muerta (nunca con `ctl pause`, que
apaga el barrido de taps y bloquea ctl_write).

Uso:  python lab/escalon_idac3.py --port COM8 --escalon 100
"""
import argparse
import json
import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import barrido_total as bt          # noqa: E402

CP_DEADBAND_UV = 8
CP_HOLD_UV = 36
CP_SETTLED_BAND_UV = 41
CP_RECENTER_MS = 46

# Tolerancia de la guarda de inyeccion, en codigos.  No puede ser cero: el
# recentrado lento del firmware mueve UN codigo cada CP_RECENTER_MS, asi que
# una guarda exacta aborta por su culpa.  Pero tiene que ser chica, porque lo
# que tiene que atrapar es la falla real -la inyeccion que no llega, que se vio
# como 154 contra 255 pedidos, o sea cien codigos-.
TOLERANCIA_CODIGOS = 3

# Reglas de `control_config_valid`: HOLD < DEADBAND y SETTLED_BAND >= DEADBAND.
# Para ensanchar hay que ir SETTLED, DEADBAND, HOLD; para volver, al reves.
ANCHAS = ((CP_SETTLED_BAND_UV, 95000), (CP_DEADBAND_UV, 90000),
          (CP_HOLD_UV, 85000))
FABRICA = ((CP_HOLD_UV, 25000), (CP_DEADBAND_UV, 45000),
           (CP_SETTLED_BAND_UV, 60000))
NOMBRE = {CP_DEADBAND_UV: 'DEADBAND_UV', CP_HOLD_UV: 'HOLD_UV',
          CP_SETTLED_BAND_UV: 'SETTLED_BAND_UV'}


def poner(idx, valor, intentos=4):
    """Fija un parametro y lo verifica leyendolo de vuelta.

    Reintenta porque las dos fallas posibles son transitorias o de orden: un
    `ctl set` puede no llegar, y un `apply` puede rechazar la config entera
    por una regla que todavia no se cumple.  Ademas `ctl_staged` es pegajoso:
    lo que quedo de un apply rechazado viaja en el siguiente."""
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
                  % (NOMBRE.get(idx, idx), valor, bt._est.get(idx), acks))
    return False


def observar(segundos, etiqueta, paso=5.0):
    """Sigue LPo y devuelve la serie (t, LPo, valido, IDAC3)."""
    serie = []
    t0 = time.time()
    while time.time() - t0 < segundos and bt._vivo:
        time.sleep(paso)
        lp = bt._est.get(bt.K_TAP + 16)
        su = bt._est.get(bt.K_TAP + 12)
        val = bt._est.get(bt.K_TAP + 17)
        i3 = bt._est.get(bt.K_IDAC + 3)
        if lp is None:
            continue
        serie.append({'t': round(time.time() - t0, 1), 'lpo_uv': lp,
                      'sumo_uv': su, 'valido': val, 'idac3': i3})
    if serie:
        ult = [f['lpo_uv'] for f in serie[-6:]]
        print('  %-12s  LPo final %8.2f mV   (pp de la cola %.1f mV, IDAC3=%s)'
              % (etiqueta, ult[-1] / 1000.0,
                 (max(ult) - min(ult)) / 1000.0, serie[-1]['idac3']),
              flush=True)
    return serie


def cola(serie, n=6):
    """Promedio del final de un tramo: el valor ya asentado."""
    xs = [f['lpo_uv'] for f in serie[-n:]]
    return sum(xs) / len(xs) if xs else None


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port', default='COM8')
    ap.add_argument('--pga', type=int, default=2)
    ap.add_argument('--pgaout', type=int, default=4)
    ap.add_argument('--escalon', type=int, default=100)
    ap.add_argument('--permanencia', type=float, default=300.0)
    ap.add_argument('--deriva', type=float, default=180.0)
    ap.add_argument('--ventana-regimen', type=float, default=180.0,
                    help='ventana para medir la tasa de deriva')
    ap.add_argument('--deriva-max', type=float, default=1.0,
                    help='mV/min tolerados antes de empezar a medir')
    ap.add_argument('--espera-sano', type=float, default=1800.0,
                    help='segundos de gracia para que el lazo asiente')
    ap.add_argument('--salida', default='lab/escalon_idac3.json')
    a = ap.parse_args()

    bt.PUERTO = a.port
    threading.Thread(target=bt._leer, daemon=True).start()
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        print('FALLA: sin adquisicion')
        return 3

    bt._fijar_ganancia(a.pga, a.pgaout)
    # Esperar a que el lazo asiente ANTES de congelarlo.  Medir la pendiente
    # de un actuador sobre una etapa saturada da cero y se lee como "el
    # actuador no sirve", que es una conclusion falsa que este banco ya estuvo
    # a punto de sacar dos veces.
    # OJO con el orden: primero se congela el PI, DESPUES se espera
    # regimen.  Al reves no converge: con la configuracion de fabrica
    # este par no se asienta -pico a pico de 60 mV y el lazo moviendo
    # IDAC3 solo-, asi que la tasa nunca baja del umbral.  Lo que hay
    # que dejar quieto es la PLANTA, y para eso el lazo tiene que estar
    # afuera primero.
    # El firmware RECHAZA `ctl apply` mientras aprende, y un cambio de
    # ganancia lo mete en aprendizaje: sin esta espera los siete pasos de la
    # matriz fallaron seguidos el 2026-09-27 con "sin banda ancha".  Su
    # hermano escalon_idac.py ya lo contempla.
    print('esperando a que termine el aprendizaje')
    _t0 = time.time()
    while time.time() - _t0 < 1500 and bt._vivo:
        bt._cmd('ctl report', 0.8)
        time.sleep(1.5)
        if bt._est.get(bt.K_ESTADO) != 1:
            break
        time.sleep(20)
    if bt._est.get(bt.K_ESTADO) == 1:
        print('FALLA: sigue aprendiendo; no se puede configurar')
        return 7
    print('ensanchando la banda muerta (PI pasivo, telemetria viva)')
    # Y apagar el recentrado lento: mueve un codigo de IDAC3 cada
    # CP_RECENTER_MS hacia el centro, aun con el PI congelado, y durante una
    # permanencia de 360 s eso corre el escalon por debajo.  Se restaura al
    # final junto con las bandas.
    recentrado = bt._est.get(CP_RECENTER_MS)
    if recentrado:
        poner(CP_RECENTER_MS, 0)
    for idx, val in ANCHAS:
        if not poner(idx, val):
            print('FALLA: sin banda ancha el PI pelea el escalon; se aborta')
            for i2, v2 in FABRICA:
                poner(i2, v2)
            return 4
    print('  ok: DEADBAND=%s HOLD=%s SETTLED=%s'
          % (bt._est.get(8), bt._est.get(36), bt._est.get(41)))

    print('esperando REGIMEN: no alcanza con que LPo este adentro, tiene que')
    print('estar QUIETO.  Un valor no dice nada sobre una tasa: la primera')
    print('corrida arranco con LPo en -26,7 mV y derivando 8 mV/min, que sobre')
    print('una permanencia de 360 s son 48 mV y se come cualquier escalon.')
    t0 = time.time()
    tasa = None
    while time.time() - t0 < a.espera_sano and bt._vivo:
        ventana = observar(a.ventana_regimen, 'sondeo', paso=10.0)
        if len(ventana) < 3:
            continue
        dt = ventana[-1]['t'] - ventana[0]['t']
        if dt <= 0:
            continue
        tasa = ((ventana[-1]['lpo_uv'] - ventana[0]['lpo_uv']) / 1000.0
                / (dt / 60.0))
        adentro = (ventana[-1]['valido'] == 1
                   and abs(ventana[-1]['lpo_uv']) < 60000)
        print('    deriva %.2f mV/min, LPo %.1f mV, valido=%s'
              % (tasa, ventana[-1]['lpo_uv'] / 1000.0, ventana[-1]['valido']),
              flush=True)
        if adentro and abs(tasa) <= a.deriva_max:
            break
    if tasa is None or abs(tasa) > a.deriva_max:
        print('FALLA: el nodo no llego a regimen en %.0f s (ultima deriva %s '
              'mV/min, tope %.1f).  Medir aca daria un numero de la deriva, no '
              'del actuador.' % (a.espera_sano, tasa, a.deriva_max))
        return 5
    print('  en regimen: deriva %.2f mV/min, LPo %.1f mV, IDAC=%s'
          % (tasa, bt._est.get(bt.K_TAP + 16) / 1000.0,
             [bt._est.get(bt.K_IDAC + i) for i in range(4)]))
    base = bt._est.get(bt.K_IDAC + 3)
    alto = max(-255, min(255, base + a.escalon))
    print('\nIDAC3 base=%d, escalon a %d (%+d codigos)'
          % (base, alto, alto - base))
    datos = {'base': base, 'alto': alto, 'tramos': []}

    try:
        # 1. Cuanto deriva SIN tocar nada.  Sin este numero no se puede decir
        #    si el efecto del escalon es senial o es la cola del acople.
        print('\n--- deriva libre (no se toca nada) ---')
        libre = observar(a.deriva, 'deriva')
        datos['tramos'].append({'nombre': 'deriva', 'idac3': base,
                                'serie': libre})
        if len(libre) >= 2:
            dt = libre[-1]['t'] - libre[0]['t']
            dv = (libre[-1]['lpo_uv'] - libre[0]['lpo_uv']) / 1000.0
            datos['deriva_mV_por_min'] = dv / (dt / 60.0) if dt else None
            print('  deriva libre: %.2f mV/min' % datos['deriva_mV_por_min'])

        # 2. A-B-A-B.  La deriva lineal se cancela entre pares consecutivos y
        #    la repeticion dice si el efecto es reproducible.
        print('\n--- escalones alternados ---')
        niveles = [(base, 'A1'), (alto, 'B1'), (base, 'A2'),
                   (alto, 'B2'), (base, 'A3')]
        for codigo, etiqueta in niveles:
            bt._cmd('idac 3 %d' % codigo, 0.4)
            # Verificar que la inyeccion LLEGO.  Hasta el 2026-09-26 el lazo la
            # deshacia en 3 s y la telemetria mostraba el valor viejo, asi que
            # el barrido entero medio deriva creyendo medir el actuador.
            # Pedir un reporte FRESCO antes de leer.  Los codigos de IDAC
            # viajan solo en el reporte periodico -cada 5 s, o cada 30 con el
            # nodo asentado-, asi que leer a los pocos segundos devuelve la
            # foto ANTERIOR y la guarda aborta por su cuenta: se vio fallar una
            # si y una no con el comando llegando siempre (el log del ESP lo
            # mostraba).  `ctl report` pone el contador en cero y emite ya.
            time.sleep(1.5)
            bt._cmd('ctl report', 0.8)
            time.sleep(1.5)
            leido = bt._est.get(bt.K_IDAC + 3)
            if leido is None or abs(leido - codigo) > TOLERANCIA_CODIGOS:
                print('  !! se pidio IDAC3=%d y el nodo dice %s: la inyeccion '
                      'no llego, se aborta' % (codigo, leido))
                break
            s_ = observar(a.permanencia, etiqueta)
            datos['tramos'].append({'nombre': etiqueta, 'idac3': codigo,
                                    'serie': s_})
            if not bt._vivo:
                break

        por = {t['nombre']: cola(t['serie']) for t in datos['tramos']
               if t['nombre'] != 'deriva'}
        dcod = alto - base
        # Cada B se compara contra la A ANTERIOR y la POSTERIOR.  Promediar
        # esas dos cancela la deriva lineal; promediar (B1-A1) con (B2-A2)
        # NO la cancela -las dos quedan sesgadas en el mismo sentido-, que era
        # el error del primer intento.
        estimaciones = []
        for b, antes, despues in (('B1', 'A1', 'A2'), ('B2', 'A2', 'A3')):
            if all(por.get(k) is not None for k in (b, antes, despues)):
                e = (por[b] - (por[antes] + por[despues]) / 2.0) / 1000.0
                estimaciones.append((b, e))
                print('  %s contra el promedio de %s y %s: %+.2f mV'
                      % (b, antes, despues, e))
        if estimaciones and dcod:
            prom = sum(e for _, e in estimaciones) / len(estimaciones)
            datos['b_mV_por_codigo'] = prom / dcod
            datos['estimaciones_mV'] = dict(estimaciones)
            print('  efecto de %+d codigos: %+.2f mV' % (dcod, prom))
            print('  b = %.4f mV por codigo de IDAC3' % datos['b_mV_por_codigo'])
            print('  autoridad total: %.0f mV sobre los 510 codigos'
                  % (abs(datos['b_mV_por_codigo']) * 510))
            if len(estimaciones) == 2:
                dif = abs(estimaciones[0][1] - estimaciones[1][1])
                print('  las dos estimaciones difieren %.2f mV' % dif)
                if dif > abs(prom) / 3.0:
                    print('  OJO: difieren demasiado entre si.  Hay curvatura o')
                    print('  ruido que el ABA no cancela; el numero es flojo.')
                else:
                    print('  concuerdan: el numero es solido.')
        else:
            print('  no se pudo estimar: faltan tramos')
    finally:
        print('\ndevolviendo IDAC3 y las bandas')
        bt._cmd('idac 3 %d' % base, 0.4)
        for idx, val in FABRICA:
            poner(idx, val)
        if recentrado:
            poner(CP_RECENTER_MS, recentrado)
        print('  DEADBAND=%s HOLD=%s SETTLED=%s'
              % (bt._est.get(8), bt._est.get(36), bt._est.get(41)))
        with open(a.salida, 'w', encoding='utf-8') as fh:
            json.dump(datos, fh, ensure_ascii=False, indent=1)
        print('  crudo en %s' % a.salida)
        bt._vivo = False
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
