"""Figuras de resumen del ruido de la SD (ensayos E1-E14, 2026-10-19 a 21).

Lee las capturas de lab/ruido_sd_20261019 y lab/ruido_sd_20261021_ferrita /
ruido_rf_20261021_2powerbanks y escribe PNG en --salida:
  sd_modos_temporal.png  brote promedio por modo de sonda (E4)
  sd_modos_barras.png    p2p por modo (E4), divisor (E5) y slew (E6)
  sd_retorno.png         donde vuelve la corriente (E10-E12): barras + forma
  sd_psoc_vs_esp.png     SD escrita por el PSoC contra SD en el ESP

  python lab/informe_sd_resumen.py --salida lab/informe_alimentacion
"""
import argparse
import glob
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.signal import welch  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analisis_ruido as ar  # noqa: E402
import ruido_sd as rs  # noqa: E402
from ejes_mv import valores_con_unidad  # noqa: E402

FS = 2604
LAB = os.path.dirname(os.path.abspath(__file__))
SD = os.path.join(LAB, 'ruido_sd_20261019')
_CAP = {}


def _sin_descarte(digi):
    _CAP['digi'] = digi.copy()
    return ''


rs.no_utilizable = _sin_descarte


def cargar(directorio, prefijo=''):
    out = {}
    for ruta in sorted(glob.glob(os.path.join(directorio, prefijo + '*.txt'))):
        r = rs._medir(ruta)
        if r is None:
            continue
        x = _CAP['digi'] * ar.UV_POR_CUENTA / 1000.0
        fr, p = welch(x - x.mean(), FS, nperseg=4096)
        b = (fr >= 5) & (fr <= 50)
        prom = np.asarray(r['promedio']) * ar.UV_POR_CUENTA / 1000.0
        prom = prom - np.nanmean(prom[:rs.VENTANA_ANTES])
        out.setdefault(r['cond'], []).append({
            'p2p': r['p2p_uV'] / 1000.0, 'promedio': prom,
            'rms': float(np.sqrt(np.trapezoid(p[b], fr[b])))})
    return out


def t_ms(n):
    return (np.arange(n) - rs.VENTANA_ANTES) / FS * 1000.0


def media(dd, cond, campo):
    v = [d[campo] for d in dd.get(cond, [])]
    return (float(np.mean(v)), float(np.std(v))) if v else (np.nan, np.nan)


def prom(dd, cond):
    return np.mean([d['promedio'] for d in dd[cond]], axis=0)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=os.path.join(LAB, 'informe_alimentacion'))
    args = ap.parse_args(argv)
    os.makedirs(args.salida, exist_ok=True)
    plt.rcParams.update({'font.size': 9})

    # E4: modos de la sonda, temporal
    e4 = cargar(os.path.join(SD, 'E4_modos'))
    nombres = {'BASE': 'base', 'P1': 'P1 solo CS', 'P2': 'P2 bus, tarjeta sin seleccionar',
               'P3': 'P3 bus, MOSI fijo', 'P4': 'P4 escritura real', 'P5': 'P5 escritura con marca'}
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    for c in ['BASE', 'P1', 'P2', 'P3']:
        if c in e4:
            p = prom(e4, c)
            axs[0].plot(t_ms(p.size), p, lw=1, label=nombres[c])
    for c in ['BASE', 'P4', 'P5']:
        if c in e4:
            p = prom(e4, c)
            axs[1].plot(t_ms(p.size), p, lw=1, label=nombres[c])
    axs[0].set_title('Sin escribir: solo el bus (P2, P3) mueve la senal')
    axs[1].set_title('Escribiendo: la transferencia y el busy de la tarjeta')
    for ax in axs:
        ax.set_xlabel('tiempo desde la escritura [ms]')
        ax.set_ylabel('LPo [mV]')
        ax.grid(alpha=.3)
        ax.legend(fontsize=7)
    fig.suptitle('E4: brote promedio de la SD del PSoC por modo (LPo, PGA x8, PGAout x16)')
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'sd_modos_temporal.png'), dpi=130)
    plt.close(fig)

    # E4/E5/E6: barras
    e5 = cargar(os.path.join(SD, 'E5_div'))
    e6 = cargar(os.path.join(SD, 'E6_slew'))
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.2), gridspec_kw={'width_ratios': [3, 2, 1.6]})
    cs = [c for c in ['BASE', 'P1', 'P2', 'P3', 'P4', 'P5'] if c in e4]
    m = [media(e4, c, 'p2p') for c in cs]
    axs[0].bar(cs, [a for a, _ in m], yerr=[b for _, b in m], color=['#7f8c8d', '#7f8c8d', '#e67e22', '#e67e22', '#c0392b', '#c0392b'][:len(cs)])
    axs[0].set_title('E4: modo (CS, bus, escritura)')
    axs[0].set_ylabel('p2p del brote [mV]')
    for ax, dd, tit in ((axs[1], e5, 'E5: divisor del SPI'), (axs[2], e6, 'E6: slew de los pines')):
        cs2 = sorted(dd, key=lambda c: (c != 'BASE', c != 'P4', int(''.join(ch for ch in c[2:] if ch.isdigit()) or 0)))
        m2 = [media(dd, c, 'p2p') for c in cs2]
        ax.bar([c.replace('P4', '') or 'normal' for c in cs2], [a for a, _ in m2],
               yerr=[b for _, b in m2], color='#c0392b')
        ax.set_title(tit)
    for ax in axs:
        ax.grid(alpha=.3, axis='y')
    fig.suptitle('Lo que importa es la corriente de la tarjeta, no los flancos ni la velocidad del bus')
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'sd_modos_barras.png'), dpi=130)
    plt.close(fig)

    # E10-E12: retorno
    casos = [('E10: SD alimentada\ndesde el ESP', 'E10_sd_alim_esp'),
             ('E11: sin masas\ndel osciloscopio', 'E11_sin_masa_osc'),
             ('E12: PSoC en\ncargador aislado', 'E12_psoc_cargador')]
    dat = [(e, cargar(os.path.join(SD, d))) for e, d in casos]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    x = np.arange(len(dat))
    for i, c in enumerate(['BASE', 'P4']):
        m = [media(dd, c, 'p2p') for _, dd in dat]
        axs[0].bar(x + (i - .5) * .38, [a for a, _ in m], .38, yerr=[b for _, b in m],
                   label=c, color=['#7f8c8d', '#c0392b'][i])
    axs[0].set_xticks(x, [e for e, _ in dat])
    axs[0].set_ylabel('p2p del brote [mV]')
    axs[0].set_title('Brote de escritura (P4) segun por donde vuelve la corriente')
    axs[0].legend()
    for e, dd in dat:
        if 'P4' in dd:
            p = prom(dd, 'P4')
            axs[1].plot(t_ms(p.size), p, lw=1, label=e.replace('\n', ' '))
    axs[1].set_xlabel('tiempo desde la escritura [ms]')
    axs[1].set_ylabel('LPo [mV]')
    axs[1].set_title('Forma del brote')
    axs[1].grid(alpha=.3)
    axs[1].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'sd_retorno.png'), dpi=130)
    plt.close(fig)

    # SD en el PSoC contra SD en el ESP
    psoc = cargar(os.path.join(SD, 'E10_sd_alim_esp'))
    esp_usb = cargar(os.path.join(LAB, 'ruido_sd_20261021_ferrita', 'E14_esd_ferrita'))
    esp_pb = cargar(os.path.join(LAB, 'ruido_rf_20261021_2powerbanks', 'R9b_lpo_campo'))
    filas = [('SD escrita por el PSoC\n(E10, 19/10)', psoc, 'P4'),
             ('SD en el ESP, dos USB a\nla misma PC (E14, ferrita)', esp_usb, 'ESD'),
             ('SD en el ESP,\ndos powerbanks', esp_pb, 'ESD')]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
    for i, (e, dd, c) in enumerate(filas):
        b = media(dd, 'BASE', 'rms')
        s = media(dd, c, 'rms')
        axs[0].bar(i - .19, b[0], .38, yerr=b[1], color='#7f8c8d', label='base' if i == 0 else None)
        axs[0].bar(i + .19, s[0], .38, yerr=s[1], color='#c0392b', label='escribiendo' if i == 0 else None)
        axs[0].text(i + .19, s[0] * 1.15, ('%.2f mV' % s[0]).replace('.', ','), ha='center', fontsize=8)
        if c in dd:
            p = prom(dd, c)
            axs[1].plot(t_ms(p.size), p, lw=1, label=e.replace('\n', ' '))
    axs[0].set_yscale('log')
    axs[0].set_xticks(range(len(filas)), [e for e, _, _ in filas], fontsize=7)
    axs[0].set_ylabel('RMS 5-50 Hz [mV]')
    axs[0].set_title('LPo x8 x16: ruido en banda')
    axs[0].legend(fontsize=7)
    valores_con_unidad(axs[0])
    axs[1].set_yscale('symlog', linthresh=1)
    axs[1].set_xlabel('tiempo desde la escritura [ms]')
    axs[1].set_ylabel('LPo [mV] (escala symlog)')
    axs[1].set_title('Brote promedio de la escritura')
    axs[1].grid(alpha=.3)
    axs[1].legend(fontsize=7)
    valores_con_unidad(axs[1])
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'sd_psoc_vs_esp.png'), dpi=130)
    plt.close(fig)
    # E3: amplitud del brote contra la ganancia, en mV y con ganancias x1..x16
    import csv
    with open(os.path.join(SD, 'ganancia', 'ganancia.csv'), encoding='utf-8') as f:
        filas_g = list(csv.DictReader(f))
    mv = ar.UV_POR_CUENTA / 1000.0
    paneles = [('Salida del PGA (tap 0), PGAout x16', 'Ganancia del PGA',
                lambda r: r['tap'] == '0', 'pga_ganancia'),
               ('LPo (tap 4), PGA x8', 'Ganancia de PGAout',
                lambda r: r['tap'] == '4' and r['pga_ganancia'] == '8', 'pgaout_ganancia')]
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.6))
    for ax, (tit, xl, filtro, col) in zip(axs, paneles):
        sel = sorted((r for r in filas_g if filtro(r)), key=lambda r: float(r[col]))
        g = np.array([float(r[col]) for r in sel])
        for campo, color, et in (('busy', '#c0392b', 'busy de la tarjeta'),
                                 ('transfer', '#2980b9', 'transferencia (|valor|)')):
            y = np.abs([float(r[campo + '_media']) for r in sel]) * mv
            e = np.array([float(r[campo + '_std']) for r in sel]) * mv
            ax.errorbar(g, y, yerr=e, marker='o', color=color, label=et, capsize=3)
        ref = abs(float(sel[0]['busy_media'])) * mv
        ax.plot(g, ref * g / g[0], '--', color='#7f8c8d', label='proporcional a la ganancia')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xticks(g, ['x%g' % v for v in g])
        ax.xaxis.set_minor_locator(plt.NullLocator())
        ax.set_xlabel(xl)
        ax.set_ylabel('amplitud del brote')
        ax.set_title(tit)
        ax.grid(alpha=.3)
        ax.legend(fontsize=7)
        valores_con_unidad(ax)
    fig.suptitle('E3: brote de la SD contra la ganancia')
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'sd_ganancia.png'), dpi=130)
    plt.close(fig)

    for e, dd, c in filas:
        print(e.replace('\n', ' '), 'base', media(dd, 'BASE', 'rms'), c, media(dd, c, 'rms'), 'p2p', media(dd, c, 'p2p'))


if __name__ == '__main__':
    main()
