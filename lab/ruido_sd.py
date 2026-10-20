"""Mide y resume el transitorio que producen las escrituras de la SD.

La captura queda en RAM y se vuelca despues por USB.  El estresor ``sdprobe``
corre en paralelo, de modo que el camino de lectura no contamina la medida.
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

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import analisis_ruido as ar       # noqa: E402
from lab import barrido_total as bt        # noqa: E402
from lab import experimento_ruido as er    # noqa: E402

VENTANA_ANTES = 20
VENTANA_DESPUES = 80
PERIODO_SD_MS = 58
SDPROBE_CADA = 150   # 5 lotes x 30 muestras: cadencia del drenaje real
BATCH = 30
# Rieles medidos de los taps (2026-09-05): 746-760 mV abajo, 1114-1122 arriba.
# Se toma el mas restrictivo y un margen: una captura con alguna muestra fuera
# de [RIEL_BAJO_MV, RIEL_ALTO_MV] toco un riel y no es utilizable (el brote
# queda recortado o la etapa no responde). Lo que importa es eso, no la banda.
RIEL_BAJO_MV = 760.0 + 10.0
RIEL_ALTO_MV = 1114.0 - 10.0
MARCA_UMBRAL = 30000  # cuentas: salto de una muestra que solo puede ser una marca
SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      'ruido_sd_20261019')


def _log(mensaje):
    print('%s  %s' % (time.strftime('%H:%M:%S'), mensaje), flush=True)


def _condicion(texto):
    """Devuelve (nombre, modo, divisor, slew, esd) de una condicion."""
    nombre = texto.upper()
    if nombre == 'BASE':
        return nombre, None, None, None, False
    if nombre == 'REAL':
        return nombre, 4, 0, 0, False
    if nombre == 'ESD':
        return nombre, None, None, None, True
    m = re.fullmatch(r'P(\d+)(?:D(\d+))?(?:S(\d+))?', nombre)
    if not m:
        raise argparse.ArgumentTypeError(
            'condicion invalida %r; use BASE, REAL, ESD o '
            'P<modo>[d<div>][s<slew>]' % texto)
    return (nombre, int(m.group(1)), int(m.group(2) or 0),
            int(m.group(3) or 0), False)


def _parar_probe():
    bt._cmd('sdprobe 0 %d 0 0 0' % PERIODO_SD_MS, 0.2)


def _esperar_posiciones_espsd(lineas, espera_s=3.0):
    """Extrae la primera linea ``#ESPSD pos n ...`` del lector de ``bt``."""
    patron = re.compile(r'^#ESPSD pos (\d+)(?:\s+(.*))?$')
    limite = time.monotonic() + espera_s
    vistas = 0
    while time.monotonic() < limite:
        while vistas < len(lineas):
            linea = lineas[vistas].strip()
            vistas += 1
            m = patron.fullmatch(linea)
            if not m:
                continue
            posiciones = ([int(p) for p in m.group(2).split()]
                          if m.group(2) else [])
            if len(posiciones) == int(m.group(1)):
                return posiciones
        time.sleep(0.05)
    return None


def _lazo_en_banda(espera_s=180.0):
    """Devuelve la foto del lazo si esta REGULANDO, en banda y con LPo dentro
    de la ventana; si no, espera hasta `espera_s` y devuelve None. Capturar con
    el calibrador todavia moviendose mide su transitorio, no la SD."""
    fin = time.time() + espera_s
    while bt._vivo:
        try:
            f = bt._foto()
        except bt.TelemetriaVencida:
            # Tras un volcado el #CTL tarda en volver: no es un cuelgue.
            if time.time() >= fin:
                return None
            time.sleep(2.0)
            continue
        lp = f['tap'][4] if f['valido'][4] == 1 else None
        if f['estado'] == 2 and lp is not None:
            return f
        if time.time() >= fin:
            return None
        time.sleep(2.0)
    return None


def _una_corrida(args, condicion, repeticion, salida):
    nombre, modo, divisor, slew, esd = condicion
    ruta = os.path.join(
        salida, 'p%d%d_%s_r%02d.txt' %
        (args.pga, args.pgaout, nombre, repeticion))
    if os.path.exists(ruta):
        return 'ya estaba'
    lazo = _lazo_en_banda()
    if lazo is None:
        return 'lazo aprendiendo: no se captura'

    duracion = args.lotes * er.MUESTRAS_POR_LOTE / float(er.FS_HZ)
    duracion_ms = int(duracion * 1000) + 4000
    lineas_espsd = [] if esd else None
    if esd:
        bt._sink = lineas_espsd
    marcas_lote = None
    if esd:
        try:
            try:
                bt._cmd('espsd %d 5' % duracion_ms, 0.3)
                bt._cmd('clear', 0.8)
                bt._cmd('startwait %d' % args.lotes, duracion + 5.0)
            finally:
                bt._cmd('espsd 0', 0.2)
            marcas_lote = _esperar_posiciones_espsd(lineas_espsd)
        finally:
            bt._sink = None
        if marcas_lote is None:
            return 'sin posiciones ESPSD'
    else:
        if modo is not None:
            bt._cmd('sdprobe %d %d %d %d %d' %
                    (duracion_ms, PERIODO_SD_MS, modo, divisor, slew), 0.3)
        try:
            bt._cmd('clear', 0.8)
            bt._cmd('startwait %d' % args.lotes, duracion + 5.0)
        finally:
            _parar_probe()

    cabecera, lotes, completo, perdidos = er._volcar()
    if perdidos:
        return 'faltan %d lotes en RAM' % len(perdidos)
    if not completo or len(lotes) < args.lotes:
        return 'captura corta: %d de %d lotes' % (len(lotes), args.lotes)
    meta = {
        'cond': nombre, 'condicion': nombre, 'modo': modo, 'div': divisor,
        'slew': slew, 'tap': args.tap, 'pga': args.pga,
        'pgaout': args.pgaout, 'nota': args.nota,
        'hora': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'repeticion': repeticion, 'lotes': len(lotes),
        'lazo': {'estado': lazo['estado'], 'banda': lazo['banda'],
                 'lpo_uv': lazo['tap'][4], 'idac': lazo['idac']},
    }
    if marcas_lote is not None:
        meta['marcas_lote'] = marcas_lote
    er._guardar(ruta, cabecera, lotes, meta)
    return None


def correr(args):
    salida = os.path.join(SALIDA, args.exp)
    os.makedirs(salida, exist_ok=True)
    bt.PUERTO = args.port
    _log('puerto: %s' % bt.PUERTO)
    threading.Thread(target=bt._leer, daemon=True).start()
    signal.signal(signal.SIGINT, bt._pedir_salida)
    bt.arrancar_enlace()
    if not bt._asegurar_adquisicion():
        _log('sin adquisicion valida: se aborta')
        return 3
    # Un probe armado por una corrida cortada contaminaria los BASE.
    _parar_probe()
    # El ESP arma P4/P5 solo si sabe que hay SD; tras abrir el puerto ese
    # estado puede no estar: sin esto el sdprobe responde "sin sd" y la
    # condicion P4 se mide SIN escribir (paso el 2026-10-20 con E9).
    bt._cmd('sdinfo', 5.0)
    # Cambiar la ganancia descalibra la cadena: se espera a que el lazo
    # converja y se quede quieto (mismo criterio que barrido_total), no un
    # tiempo fijo. A ganancia alta aprender puede tardar 600-800 s.
    _log('x%d/x%d: esperando que el lazo converja...' %
         (bt.CODIGOS[args.pga], bt.CODIGOS[args.pgaout]))
    for intento in range(3):
        try:
            serie, t_banda, _, _, _ = bt._visitar(args.pga, args.pgaout, 240)
            break
        except bt.TelemetriaVencida as exc:
            # Tras un volcado el #CTL tarda en volver: reintentar, no abortar.
            _log('telemetria vencida (%s), reintento %d' % (exc, intento + 1))
            time.sleep(10.0)
        except RuntimeError as exc:
            _log('el nodo no confirma la ganancia: %s' % exc)
            return 3
    else:
        _log('sin telemetria tras 3 intentos')
        return 3
    ult = serie[-1] if serie else {}
    _log('lazo quieto (t_banda=%s, estado=%s, LPo=%s uV); la utilidad la '
         'decide el analisis por rieles' % (t_banda, ult.get('estado'),
                                            (ult.get('tap') or [None] * 5)[4]))
    if args.tap is not None:
        # `view T` (0xAC) elige el tap que digitaliza la captura; solo en IDLE.
        bt._cmd('view %d' % args.tap, 1.5)

    hechas = saltadas = 0
    try:
        for rep in range(1, args.rep + 1):
            if not bt._vivo:
                break
            # Ida y vuelta: A B C C B A cancela la deriva lineal.
            orden = args.cond + list(reversed(args.cond))
            for indice, condicion in enumerate(orden):
                if not bt._vivo:
                    break
                numero = rep * 10 + indice
                problema = _una_corrida(args, condicion, numero, salida)
                if problema == 'ya estaba':
                    saltadas += 1
                elif problema:
                    _log('!! %s r%02d: %s' %
                         (condicion[0], numero, problema))
                else:
                    hechas += 1
                    _log('%-10s r%02d ok' % (condicion[0], numero))
    finally:
        _parar_probe()
    _log('terminado: %d nuevas, %d existentes, en %s' %
         (hechas, saltadas, salida))
    return 0


def _ventanas(digi, marcas):
    """Promedio sincrono y mascara de muestras fuera de todos los bursts."""
    centros = np.flatnonzero(marcas)
    centros = centros[(centros >= VENTANA_ANTES) &
                      (centros + VENTANA_DESPUES < digi.size)]
    if centros.size == 0:
        return np.array([]), np.zeros(digi.size, dtype=bool), 0
    ventanas = np.stack([
        digi[i - VENTANA_ANTES:i + VENTANA_DESPUES + 1] for i in centros])
    ocupada = np.zeros(digi.size, dtype=bool)
    for i in centros:
        ocupada[i - VENTANA_ANTES:i + VENTANA_DESPUES + 1] = True
    return ventanas, ~ocupada, int(centros.size)


def _desmarcar(digi):
    """En capturas a RAM la marca SD viaja en los bits 21-22 del int24 (XOR
    contra el signo, como decodeSdMarks() del ESP, que solo la quita en los
    lotes leidos de la SD). Devuelve (digi limpio, flags de marca)."""
    v = digi.astype(np.int64)
    rep = np.where(v < 0, 3, 0)
    marca = ((v >> 21) & 3) ^ rep
    v = v ^ (marca << 21)
    return v.astype(np.float64), marca.astype(np.uint8)


def no_utilizable(digi):
    """Motivo por el que la captura toco un riel, o '' si es utilizable."""
    mv_min = float(np.min(digi)) * ar.UV_POR_CUENTA / 1000.0
    mv_max = float(np.max(digi)) * ar.UV_POR_CUENTA / 1000.0
    if mv_min < RIEL_BAJO_MV or mv_max > RIEL_ALTO_MV:
        return 'excursion %.0f..%.0f mV fuera de %.0f..%.0f' % (
            mv_min, mv_max, RIEL_BAJO_MV, RIEL_ALTO_MV)
    return ''


def _marcas_desde_meta(meta, cantidad):
    marcas = np.zeros(cantidad, dtype=bool)
    if 'marcas_lote' in meta:
        posiciones = np.asarray(meta['marcas_lote'], dtype=np.int64) * BATCH
        posiciones = posiciones[(posiciones >= 0) & (posiciones < cantidad)]
        marcas[posiciones] = True
    else:
        marcas[SDPROBE_CADA::SDPROBE_CADA] = True
    return marcas


def _medir(ruta):
    meta, seqs, digi, flags, _ = ar.cargar(ruta)
    if digi.size == 0:
        return None
    # La marca XOR no sobrevive la trama de captura a RAM (el ESP la entrega
    # en 18 bits). ESD registra los lotes reales; BASE y las sondas del PSoC
    # conservan las posiciones fijas que sirven como control plano.
    marcas = _marcas_desde_meta(meta, digi.size)
    # La muestra marcada trae el XOR de la marca corrido a 18 bits (+65536):
    # es un artefacto de codificacion, no ruido. Se interpola con sus vecinas.
    idx = np.flatnonzero(marcas)
    idx = idx[(idx > 0) & (idx < digi.size - 1)]
    digi = digi.copy()
    digi[idx] = 0.5 * (digi[idx - 1] + digi[idx + 1])
    # El modo 5 pone una segunda marca (SYNC = +131072) al empezar el busy, en
    # una posicion que no es fija. Cualquier muestra AISLADA que se separe mas
    # de MARCA_UMBRAL de sus dos vecinas es esa marca: el ruido real es mucho
    # menor y nunca dura una sola muestra con ese tamano.
    centro = digi[1:-1]
    aisladas = np.flatnonzero(
        (np.abs(centro - digi[:-2]) > MARCA_UMBRAL) &
        (np.abs(centro - digi[2:]) > MARCA_UMBRAL)) + 1
    digi[aisladas] = 0.5 * (digi[aisladas - 1] + digi[aisladas + 1])
    motivo = no_utilizable(digi)
    if motivo:
        print('NO UTILIZABLE %s: %s' % (os.path.basename(ruta), motivo),
              file=sys.stderr)
        return None
    ventanas, fuera, n_validas = _ventanas(digi, marcas)
    if not n_validas:
        promedio = np.full(VENTANA_ANTES + VENTANA_DESPUES + 1, np.nan)
        p2p = energia = razon = float('nan')
    else:
        promedio = ventanas.mean(axis=0)
        base = float(promedio[:VENTANA_ANTES].mean())
        burst = promedio - base
        p2p = float(np.ptp(burst))
        energia = float(np.sum(burst ** 2))
        rms_ventanas = float(np.std(ventanas - ventanas.mean(axis=1)[:, None]))
        rms_fuera = float(np.std(digi[fuera])) if fuera.any() else float('nan')
        razon = rms_ventanas / rms_fuera if rms_fuera else float('nan')
    return {
        'cond': meta.get('cond', meta.get('condicion', 'DESCONOCIDA')),
        'n_marcas': int(marcas.sum()), 'p2p_cuentas': p2p,
        'p2p_uV': p2p * ar.UV_POR_CUENTA, 'energia': energia,
        'ratio_rms': razon, 'lotes_perdidos': ar.lotes_faltantes(seqs),
        'promedio': promedio,
    }


def _media_std(valores):
    x = np.asarray(valores, dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return float('nan'), float('nan')
    return float(x.mean()), float(x.std(ddof=1)) if x.size > 1 else 0.0


def _fmt(par):
    return '%.3g+-%.2g' % par


def resumir(args):
    filas = [f for f in (_medir(r) for r in sorted(
        glob.glob(os.path.join(args.directorio, '*.txt')))) if f]
    if not filas:
        print('no hay volcados en %s' % args.directorio, file=sys.stderr)
        return 1
    condiciones = sorted({f['cond'] for f in filas},
                         key=lambda x: (x != 'BASE', x))
    resumen = []
    for cond in condiciones:
        xs = [f for f in filas if f['cond'] == cond]
        fila = {'cond': cond, 'n': len(xs)}
        for clave in ('n_marcas', 'p2p_cuentas', 'p2p_uV', 'energia',
                      'ratio_rms', 'lotes_perdidos'):
            fila[clave] = _media_std([x[clave] for x in xs])
        resumen.append(fila)
        _guardar_figura(args.directorio, cond, xs)
    _guardar_figura_conjunta(args.directorio, condiciones, filas)

    encabezado = 'cond n marcas p2p[count] p2p[uV] energia ratio lost'
    print(encabezado)
    for f in resumen:
        print('%s %d %s %s %s %s %s %s' %
              (f['cond'], f['n'], _fmt(f['n_marcas']),
               _fmt(f['p2p_cuentas']), _fmt(f['p2p_uV']),
               _fmt(f['energia']), _fmt(f['ratio_rms']),
               _fmt(f['lotes_perdidos'])))
    _guardar_tablas(args.directorio, resumen)

    base = next((f for f in resumen if f['cond'] == 'BASE'), None)
    veredictos = []
    if base:
        media_base, std_base = base['p2p_cuentas']
        for f in resumen:
            if f is base:
                continue
            delta = f['p2p_cuentas'][0] - media_base
            efecto = abs(delta) > 3.0 * std_base
            veredictos.append('%s=%s (delta p2p %.3g)' %
                              (f['cond'], 'EFECTO' if efecto else 'sin efecto',
                               delta))
    print('veredicto: ' + ('; '.join(veredictos) if veredictos
                           else 'falta BASE o una condicion comparable'))
    return 0


def _guardar_figura(directorio, condicion, filas):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    curvas = np.stack([f['promedio'] for f in filas])
    curva = np.nanmean(curvas, axis=0)
    x = np.arange(-VENTANA_ANTES, VENTANA_DESPUES + 1)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.plot(x, curva, lw=1.3)
    ax.axvline(0, color='tab:red', lw=0.8)
    ax.set(xlabel='muestras desde la marca', ylabel='cuentas ADC',
           title='Burst promedio - %s' % condicion)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    seguro = re.sub(r'[^A-Za-z0-9_.-]', '_', condicion)
    fig.savefig(os.path.join(directorio, 'burst_%s.png' % seguro), dpi=150)
    plt.close(fig)


def _guardar_figura_conjunta(directorio, condiciones, filas):
    """Todas las condiciones superpuestas, en ms y relativas a su propia base
    (media de las muestras previas a la marca), para comparar formas."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    x_ms = np.arange(-VENTANA_ANTES, VENTANA_DESPUES + 1) * 1000.0 / er.FS_HZ
    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    for cond in condiciones:
        curva = np.nanmean(np.stack(
            [f['promedio'] for f in filas if f['cond'] == cond]), axis=0)
        curva = curva - np.nanmean(curva[:VENTANA_ANTES])
        ax.plot(x_ms, curva, lw=1.3, label=cond)
    ax.axvline(0, color='0.4', lw=0.8, ls='--')
    ax.set(xlabel='tiempo desde el inicio de la accion [ms]',
           ylabel='cuentas ADC (respecto a la base previa)',
           title='Brote promedio por condicion - %s' %
           os.path.basename(os.path.normpath(directorio)))
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(directorio, 'bursts_conjunto.png'), dpi=150)
    plt.close(fig)


def _guardar_tablas(directorio, filas):
    columnas = ['cond', 'n', 'n_marcas', 'p2p_cuentas', 'p2p_uV',
                'energia', 'ratio_rms', 'lotes_perdidos']
    csv_ruta = os.path.join(directorio, 'resumen.csv')
    with open(csv_ruta, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        cabecera = ['cond', 'n']
        for clave in columnas[2:]:
            cabecera.extend([clave + '_media', clave + '_std'])
        w.writerow(cabecera)
        for f in filas:
            datos = [f['cond'], f['n']]
            for clave in columnas[2:]:
                datos.extend(f[clave])
            w.writerow(datos)
    with open(os.path.join(directorio, 'resumen.md'), 'w', encoding='utf-8') as fh:
        fh.write('| cond | n | marcas | p2p cuentas | p2p uV | energia | ratio | perdidos |\n')
        fh.write('|---|---:|---:|---:|---:|---:|---:|---:|\n')
        for f in filas:
            fh.write('| %s | %d | %s | %s | %s | %s | %s | %s |\n' %
                     (f['cond'], f['n'], _fmt(f['n_marcas']),
                      _fmt(f['p2p_cuentas']), _fmt(f['p2p_uV']),
                      _fmt(f['energia']), _fmt(f['ratio_rms']),
                      _fmt(f['lotes_perdidos'])))


def autotest(_args):
    rng = np.random.default_rng(20261019)
    esperado = 1000.0
    digi = rng.normal(0.0, 2.0, 4000)
    marcas = np.zeros(digi.size, dtype=bool)
    forma = np.zeros(VENTANA_ANTES + VENTANA_DESPUES + 1)
    forma[VENTANA_ANTES:VENTANA_ANTES + 11] = np.linspace(0, esperado, 11)
    forma[VENTANA_ANTES + 11:VENTANA_ANTES + 31] = np.linspace(esperado, 0, 20)
    for centro in range(300, 3700, 300):
        marcas[centro] = True
        digi[centro - VENTANA_ANTES:centro + VENTANA_DESPUES + 1] += forma
    ventanas, _, _ = _ventanas(digi, marcas)
    obtenido = float(np.ptp(ventanas.mean(axis=0)))
    if abs(obtenido - esperado) / esperado > 0.10:
        print('AUTOTEST FAIL: p2p %.2f, esperado %.2f' % (obtenido, esperado))
        return 1
    marcas_esd = _marcas_desde_meta({'marcas_lote': [2, 7, 11]}, 400)
    if np.flatnonzero(marcas_esd).tolist() != [60, 210, 330]:
        print('AUTOTEST FAIL: conversion de marcas_lote')
        return 1
    print('AUTOTEST PASS: p2p %.2f, esperado %.2f' % (obtenido, esperado))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='subcomando', required=True)
    cp = sub.add_parser('correr')
    cp.add_argument('--port', required=True)
    cp.add_argument('--exp', required=True)
    cp.add_argument('--cond', nargs='+', required=True, type=_condicion)
    cp.add_argument('--rep', type=int, default=3)
    cp.add_argument('--lotes', type=int, default=250)
    cp.add_argument('--pga', type=int, default=0)
    cp.add_argument('--pgaout', type=int, default=0)
    cp.add_argument('--tap', type=int)
    cp.add_argument('--nota', default='')
    cp.set_defaults(func=correr)
    rp = sub.add_parser('resumir')
    rp.add_argument('directorio')
    rp.add_argument('--csv', action='store_true',
                    help='compatibilidad: resumen.csv siempre se guarda')
    rp.set_defaults(func=resumir)
    ap_test = sub.add_parser('autotest')
    ap_test.set_defaults(func=autotest)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())
