"""Figuras del informe del ruido por radio (ESP-NOW) sobre el front-end.

Uso: python lab/figuras_informe_rf.py [--raiz lab/ruido_rf_20261020] [--salida DIR]
Escribe rf_potencia.png, rf_taps.png, rf_ganancia.png, rf_formas.png y rf_resumen.csv.
Tolera directorios o condiciones ausentes: omite el panel o la serie y lo anuncia.
"""
import argparse
import csv
import glob
import json
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import ruido_sd  # noqa: E402
from lab import figuras_informe_sd as fsd  # noqa: E402

GANANCIAS = (1, 2, 4, 8, 16, 24, 32, 48, 50)   # codigo PGA 0..8 (ganancia_ruido_sd.py)
UV = 1e6 / 52429.0                              # uV por cuenta (analisis_ruido.UV_POR_CUENTA)
FILAS = []


def omitir(txt):
    print('OMITIDO: ' + txt, file=sys.stderr)


def capturas(raiz, dir_, cond):
    """Lista de dicts (p2p, promedio, pga, pgaout, tap) de las capturas utiles."""
    out = []
    for r in sorted(glob.glob(os.path.join(raiz, dir_, '*.txt'))):
        try:
            with open(r, encoding='utf-8') as archivo:
                meta = json.loads(archivo.readline())['meta']
        except (OSError, ValueError, KeyError):
            continue
        if str(meta.get('cond', meta.get('condicion'))).upper() != cond:
            continue
        m = ruido_sd._medir(r)   # None si no utilizable (tocó un riel)
        if not m or not np.isfinite(m['promedio']).all():
            continue
        out.append({'p2p': m['p2p_cuentas'], 'prom': m['promedio'] - m['promedio'][:20].mean(),
                    'pga': meta.get('pga'), 'pgaout': meta.get('pgaout'), 'tap': meta.get('tap')})
    return out


def ms(x):
    x = np.asarray([c['p2p'] for c in x], float)
    return float(x.mean()), (float(x.std(ddof=1)) if x.size > 1 else 0.0), x.size


def prom(caps):
    return np.mean([c['prom'] for c in caps], axis=0)


def reg(fig, serie, cond, caps, ganancia=None, extra=''):
    m, s, n = ms(caps)
    FILAS.append({'figura': fig, 'serie': serie, 'cond': cond, 'n': n,
                  'p2p_cuentas': m, 'std_cuentas': s,
                  'p2p_uV_salida': m * UV, 'ganancia': ganancia or '',
                  'p2p_uV_entrada': (m * UV / ganancia) if ganancia else '', 'nota': extra})
    return m, s


def g_total(c):
    return GANANCIAS[c['pga']] * GANANCIAS[c['pgaout']]


def fig_potencia(raiz, sal):
    d = 'W3b_potencia_pgaout1'
    pts = []
    for p in (2, 8, 14, 21):
        c = capturas(raiz, d, 'RF240P%d' % p)
        if c:
            pts.append((p, c))
        else:
            omitir('%s RF240P%d' % (d, p))
    if not pts:
        omitir('rf_potencia.png sin datos')
        return
    g = g_total(pts[0][1][0])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    xs, ys, es = [], [], []
    for p, c in pts:
        m, s = reg('rf_potencia', 'RF240', 'RF240P%d' % p, c, g, 'potencia %d dBm' % p)
        xs.append(p)
        ys.append(m)
        es.append(s)
    ax.errorbar(xs, ys, es, fmt='o-', capsize=4, color='#d62728', label='RF240 (240 B)')
    ping = capturas(raiz, 'W5_lpo_pgaout1', 'PING')
    if ping:
        m, s = reg('rf_potencia', 'PING', 'PING', ping, g, 'referencia W5_lpo_pgaout1')
        ax.axhline(m, color='0.4', ls='--', label='PING (referencia)')
        ax.axhspan(m - s, m + s, color='0.85')
    else:
        omitir('referencia PING de W5_lpo_pgaout1')
    ax.set_xlabel('Potencia de transmisión [dBm]')
    ax.set_ylabel('p2p del brote en LPo [cuentas ADC]')
    sec = ax.secondary_yaxis('right', functions=(lambda v: v * UV / g, lambda v: v * g / UV))
    sec.set_ylabel('referido a la entrada [µV] (÷ %d)' % g)
    ax.set_title('Brote en LPo vs potencia de transmisión (PGA x%d, PGAout x%d)' % (
        GANANCIAS[pts[0][1][0]['pga']], GANANCIAS[pts[0][1][0]['pgaout']]), fontsize=10)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(sal, 'rf_potencia.png'), dpi=150)
    plt.close(fig)


def fig_taps(raiz, sal):
    cols = [('W5_tap0', 'tap 0'), ('W5_tap1', 'tap 1'), ('W5_tap2', 'tap 2'),
            ('W5_tap3', 'tap 3'), ('W5_lpo_pgaout1', 'LPo')]
    datos = []
    for d, nom in cols:
        ping, rf = capturas(raiz, d, 'PING'), capturas(raiz, d, 'RF240')
        if not ping or not rf:
            omitir('%s sin PING/RF240' % d)
            continue
        c = ping[0]
        etq = '%s\nPGA x%d, PGAout x%d' % (nom, GANANCIAS[c['pga']], GANANCIAS[c['pgaout']])
        reg('rf_taps', nom, 'PING', ping, None, etq.replace('\n', ' '))
        reg('rf_taps', nom, 'RF240', rf, None, etq.replace('\n', ' '))
        datos.append((etq, ping, rf))
    if not datos:
        omitir('rf_taps.png sin datos')
        return
    n = len(datos)
    fig = plt.figure(figsize=(3 * max(n, 3), 7))
    gs = fig.add_gridspec(2, n, height_ratios=[1.1, 1])
    ab = fig.add_subplot(gs[0, :])
    w = 0.38
    for i, (etq, ping, rf) in enumerate(datos):
        for k, (c, col, lab) in enumerate(((ping, '0.5', 'PING'), (rf, '#d62728', 'RF240'))):
            m, s, _ = ms(c)
            ab.bar(i + (k - 0.5) * w, m, w, yerr=s, capsize=3, color=col,
                   label=lab if i == 0 else None)
    ab.set_xticks(range(n))
    ab.set_xticklabels([d[0] for d in datos], fontsize=8)
    ab.set_ylabel('p2p del brote [cuentas ADC]')
    ab.legend(fontsize=8)
    ab.grid(alpha=0.25, axis='y')
    ab.set_title('p2p por tap: PING vs RF240 (media ± desvío entre capturas)', fontsize=10)
    brotes = []
    for i, (etq, ping, rf) in enumerate(datos):
        a = fig.add_subplot(gs[1, i])
        p_ping, p_rf = prom(ping), prom(rf)
        a.plot(fsd.eje_ms(p_ping.size), p_ping, color='0.5', lw=1.3, label='PING')
        a.plot(fsd.eje_ms(p_rf.size), p_rf, color='#d62728', lw=1.3, label='RF240')
        a.set_title(etq.split('\n')[0], fontsize=9)
        a.set_xlabel('ms desde la marca')
        a.grid(alpha=0.25)
        brotes.append(a)
        if i == 0:
            a.set_ylabel('cuentas ADC')
            a.legend(fontsize=7)
    fsd.zoom(brotes, -5, 31)
    fig.tight_layout()
    fig.savefig(os.path.join(sal, 'rf_taps.png'), dpi=150)
    plt.close(fig)


def fig_ganancia(raiz, sal):
    # SEo es la salida del PGA: la ganancia que le corresponde es solo la del PGA.
    pts = []
    for code in (0, 2, 4):
        d = 'W9_ganancia_pga%d' % code
        ping, rf = capturas(raiz, d, 'PING'), capturas(raiz, d, 'RF240')
        if ping and rf:
            pts.append((code, ping, rf))
        else:
            omitir('%s ausente o sin PING/RF240' % d)
    if not pts:
        omitir('rf_ganancia.png: no existen datos W9_ganancia_pga{0,2,4}')
        return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
    gs = [GANANCIAS[p[0]] for p in pts]
    for k, (cond, col) in enumerate((('PING', '0.5'), ('RF240', '#d62728'))):
        ys = np.array([ms(p[1 + k])[0] for p in pts])
        es = np.array([ms(p[1 + k])[1] for p in pts])
        for p, g in zip(pts, gs):
            reg('rf_ganancia', cond, cond, p[1 + k], g, 'SEo, PGA x%d' % g)
        ga = np.array(gs, float)
        ax[0].errorbar(gs, ys, es, fmt='o-', capsize=3, color=col, label=cond)
        ax[1].errorbar(gs, ys * UV / ga, es * UV / ga, fmt='o-', capsize=3, color=col, label=cond)
    g0 = np.array(gs, float)
    y0 = ms(pts[0][2])[0]
    ax[0].plot(g0, y0 * g0 / g0[0], 'k:', label='guía: constante a la entrada')
    ax[0].plot(g0, np.full_like(g0, y0), 'b:', label='guía: constante a la salida')
    ax[1].plot(g0, y0 * UV / g0 * g0[0] / g0[0], 'b:', label='guía: constante a la salida')
    ax[1].plot(g0, np.full_like(g0, y0 * UV / g0[0]), 'k:', label='guía: constante a la entrada')
    ax[0].set_ylabel('p2p en SEo [cuentas ADC]')
    ax[1].set_ylabel('p2p referido a la entrada [µV]')
    for a in ax:
        a.set_xscale('log')
        a.set_yscale('log')
        a.set_xlabel('Ganancia del PGA')
        a.grid(alpha=0.25, which='both')
        a.set_xticks(gs)
        a.set_xticklabels(['x%d' % g for g in gs])
        a.legend(fontsize=7)
    fig.suptitle('Brote en SEo vs ganancia del PGA: ¿entra antes o después del amplificador?',
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(sal, 'rf_ganancia.png'), dpi=150)
    plt.close(fig)


def fig_formas(raiz, sal, raiz_sd):
    series = [('PING', 'W5_lpo_pgaout1', 'PING', '0.4'),
              ('RF10', 'W5_lpo_pgaout1', 'RF10', '#1f77b4'),
              ('RF240', 'W5_lpo_pgaout1', 'RF240', '#d62728')]
    for d in ('W4b_rx_pgaout1', 'W5_lpo_pgaout1'):
        if capturas(raiz, d, 'RX'):
            series.append(('RX', d, 'RX', '#2ca02c'))
            break
    else:
        omitir('condición RX')
    if capturas(raiz, 'W5c_lpo_pgaout1', 'RF240'):
        series.append(('RF240 (W5c)', 'W5c_lpo_pgaout1', 'RF240', '#ff7f0e'))
    else:
        omitir('W5c_lpo_pgaout1')
    fig, ax = plt.subplots(figsize=(8, 4.8))
    g = None
    n = 0
    for nom, d, cond, col in series:
        c = capturas(raiz, d, cond)
        if not c:
            omitir('%s/%s' % (d, cond))
            continue
        g = g or g_total(c[0])
        reg('rf_formas', nom, cond, c, g_total(c[0]), d)
        p = prom(c)
        ax.plot(fsd.eje_ms(p.size), p, color=col, lw=1.4, label=nom)
        n += 1
    real = None
    for d in sorted(glob.glob(os.path.join(raiz_sd, 'E*'))):
        if not os.path.isdir(d):
            continue
        for cond in ('REAL', 'P4'):
            c = [x for x in capturas(raiz_sd, os.path.basename(d), cond)
                 if (x['pga'], x['pgaout'], x['tap']) == (3, 0, 4)]
            if c:
                real = (os.path.basename(d), cond, c)
                break
        if real:
            break
    if real:
        reg('rf_formas', 'SD real', real[1], real[2], g_total(real[2][0]), real[0])
        p = prom(real[2])
        ax.plot(fsd.eje_ms(p.size), p, color='k', lw=1.4,
                label='escritura SD real (%s)' % real[0])
    else:
        omitir('escritura SD real PGA x8 / PGAout x1 / tap 4 en %s' % raiz_sd)
    if not n and not real:
        omitir('rf_formas.png sin datos')
        plt.close(fig)
        return
    ax.axvline(0, color='k', ls='--', lw=0.7)
    fsd.zoom(ax, -5, 31)
    ax.set_xlabel('ms desde la marca')
    ax.grid(alpha=0.25)
    ax.set_ylabel('LPo [cuentas ADC]')
    if g:
        sec = ax.secondary_yaxis(
            'right', functions=(lambda v: v * UV / g, lambda v: v * g / UV))
        sec.set_ylabel('referido a la entrada [µV] (÷ %d)' % g)
    ax.set_title('Brote promedio en LPo, PGA x8 / PGAout x1, misma escala', fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(sal, 'rf_formas.png'), dpi=150)
    plt.close(fig)


def main():
    aq = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('--raiz', default=os.path.join(aq, 'ruido_rf_20261020'))
    ap.add_argument('--salida')
    a = ap.parse_args()
    FILAS.clear()
    sal = a.salida or os.path.join(a.raiz, 'figuras')
    os.makedirs(sal, exist_ok=True)
    fig_potencia(a.raiz, sal)
    fig_taps(a.raiz, sal)
    fig_ganancia(a.raiz, sal)
    fig_formas(a.raiz, sal, os.path.join(aq, 'ruido_sd_20261019'))
    campos = ['figura', 'serie', 'cond', 'n', 'p2p_cuentas', 'std_cuentas', 'p2p_uV_salida',
              'ganancia', 'p2p_uV_entrada', 'nota']
    with open(os.path.join(sal, 'rf_resumen.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, campos)
        w.writeheader()
        w.writerows(FILAS)
    print('listo:', sal)


if __name__ == '__main__':
    main()
