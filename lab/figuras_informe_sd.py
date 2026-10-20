"""Figuras matriciales del informe del ruido de la SD (por configuracion).

Uso: python lab/figuras_informe_sd.py  -> lab/ruido_sd_20261019/informe/*.png
Excluye los canales del osciloscopio que estaban mal conectados (CH3 de m1-m3).
"""
import os
import sys
import glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import ruido_sd  # noqa: E402

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ruido_sd_20261019')
OSC = os.path.join(RAIZ, 'E9_osciloscopio')
SAL = os.path.join(RAIZ, 'informe')
FS = 2604.0
COL = {'placa': '#1f77b4', 'jpsoc': '#d62728', 'esp': '#2ca02c', 'carg': '#9467bd'}
CONF = [('placa', 'SD en la placa'), ('jpsoc', 'SD con jumpers\nal kit del PSoC'),
        ('esp', 'SD alimentada\ndesde el ESP32'), ('carg', 'PSoC en cargador\naislado')]


def osc(nombre):
    f = [l.rstrip('\n').split(',') for l in open(os.path.join(OSC, nombre), encoding='latin-1')]
    t = np.array([float(x[3]) for x in f]) * 1e3
    ch = [np.array([float(x[6 * c + 4]) for x in f]) for c in range(4)]
    return t, ch


def suave(v, n=25):
    return np.convolve(v, np.ones(n) / n, 'same')


def rel_mv(t, v):
    return suave((v - v[t < 0].mean()) * 1e3)


def sombra_cs(ax, t, cs):
    bajo = cs < 0.5 * (cs.max() + cs.min())
    if bajo.any():
        i = np.flatnonzero(bajo)
        ax.axvspan(t[i[0]], t[i[-1]], color='0.92', zorder=0)


def matriz_osciloscopio():
    arch = {'placa': 'm4_pgao_entrada_vref.csv', 'jpsoc': 'm5_jumpers_pgao_entrada_vref.csv',
            'esp': 'm6_sd_alim_esp_pgao_entrada_vref.csv', 'carg': 'm7_psoc_cargador.csv'}
    filas = [(1, 'PGAo (salida de PGAout)'), (2, 'Entrada en corto'), (3, 'VREF (P3[6])')]
    fig, ax = plt.subplots(3, 4, figsize=(14, 8), sharex=True, sharey='row')
    for j, (k, nom) in enumerate(CONF):
        t, ch = osc(arch[k])
        for i, (c, fn) in enumerate(filas):
            a = ax[i, j]
            sombra_cs(a, t, ch[0])
            a.plot(t, rel_mv(t, ch[c]), color=COL[k], lw=1.3)
            a.axhline(0, color='0.5', lw=0.6)
            a.grid(alpha=0.25)
            if i == 0:
                a.set_title(nom, fontsize=10)
            if j == 0:
                a.set_ylabel(fn + '\n[mV]', fontsize=9)
            if i == 2:
                a.set_xlabel('ms desde que baja CS')
    fig.suptitle('Osciloscopio por configuración (gris: CS bajo). '
                 'Promedio de 64-128 disparos, media móvil de 0,5 ms', fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, 'fig_osciloscopio_matriz.png'), dpi=130)


def cadena_placa():
    # Solo canales validos: m1 CH2 (GND SD) y CH4 (VCC); m2 CH2 (SEo) y CH4 (masa
    # analogica); m3 CH2 (Vref_LP) y CH4 (Vref_PGA). El CH3 de m1-m3 se descarta.
    paneles = [('m1_cs_gndsd_entrada_vdda.csv', 1, 'GND del módulo SD'),
               ('m2_seo_pgao_masaanalogica.csv', 3, 'Masa analógica del front-end'),
               ('m3_vref_lp_adder_pga.csv', 1, 'Vref_LP (P0[7])'),
               ('m3_vref_lp_adder_pga.csv', 3, 'Vref_PGA (P3[0])'),
               ('m2_seo_pgao_masaanalogica.csv', 1, 'SEo (salida del PGA, P2[7])'),
               ('m1_cs_gndsd_entrada_vdda.csv', 3, 'VCC del PSoC')]
    fig, ax = plt.subplots(2, 3, figsize=(13, 6.5), sharex=True)
    for a, (f, c, nom) in zip(ax.flat, paneles):
        t, ch = osc(f)
        sombra_cs(a, t, ch[0])
        a.plot(t, rel_mv(t, ch[c]), color=COL['placa'], lw=1.3)
        a.axhline(0, color='0.5', lw=0.6)
        a.set_title(nom, fontsize=10)
        a.set_ylabel('mV')
        a.grid(alpha=0.25)
    for a in ax[1]:
        a.set_xlabel('ms desde que baja CS')
    fig.suptitle('SD en la placa: la masa se mueve y las referencias la siguen (gris: CS bajo)',
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, 'fig_cadena_placa.png'), dpi=130)


def promedio(dir_, cond):
    ps = []
    for r in sorted(glob.glob(os.path.join(RAIZ, dir_, '*.txt'))):
        m = ruido_sd._medir(r)
        if m and m['cond'] == cond and np.isfinite(m['promedio']).all():
            ps.append(m['promedio'] - m['promedio'][:20].mean())
    return np.mean(ps, axis=0) if ps else None


def eje_ms(n):
    return (np.arange(n) - 20) / FS * 1e3


def matriz_mux():
    exps = [('placa', 'E6_slew'), ('esp', 'E10_sd_alim_esp'), ('carg', 'E12_psoc_cargador')]
    nombres = dict(CONF)
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
    for a, (k, d) in zip(ax, exps):
        for cond, color, lw, lab in (('BASE', '0.55', 1.2, 'control (BASE)'),
                                     ('P4', COL[k], 1.8, 'escritura real (P4)')):
            p = promedio(d, cond)
            if p is not None:
                a.plot(eje_ms(len(p)), p, color=color, lw=lw, label=lab)
        a.axvline(0, color='k', ls='--', lw=0.7)
        a.set_title(nombres[k].replace('\n', ' '), fontsize=10)
        a.set_xlabel('ms desde la escritura')
        a.grid(alpha=0.25)
    ax[0].set_ylabel('LPo [cuentas ADC]')
    ax[0].legend(fontsize=8)
    fig.suptitle('Brote promedio en LPo medido con el ADC del PSoC (PGA x8, PGAout x16)',
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, 'fig_mux_matriz.png'), dpi=130)


def descomposicion_placa():
    paneles = [('E4_modos', [('BASE', 'control'), ('P1', 'solo CS'),
                             ('P2', 'bus, tarjeta deseleccionada'), ('P4', 'escritura real')],
                'E4: qué parte de la escritura'),
               ('E5_div', [('P4D6', 'divisor 6'), ('P4', 'divisor 12'), ('P4D24', 'divisor 24'),
                           ('P4D48', 'divisor 48')], 'E5: velocidad del reloj SPI'),
               ('E6_slew', [('P4', 'slew normal'), ('P4S1', 'slew lento'), ('P4S2', 'slew rápido')],
                'E6: pendiente de los flancos')]
    fig, ax = plt.subplots(1, 3, figsize=(14, 4), sharey=True)
    for a, (d, conds, tit) in zip(ax, paneles):
        for cond, lab in conds:
            p = promedio(d, cond)
            if p is not None:
                a.plot(eje_ms(len(p)), p, lw=1.4, label=lab)
        a.axvline(0, color='k', ls='--', lw=0.7)
        a.set_title(tit, fontsize=10)
        a.set_xlabel('ms desde la acción')
        a.grid(alpha=0.25)
        a.legend(fontsize=8)
    ax[0].set_ylabel('LPo [cuentas ADC]')
    fig.suptitle('SD en la placa: el brote sigue la corriente de la tarjeta, no los flancos',
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, 'fig_descomposicion_placa.png'), dpi=130)


if __name__ == '__main__':
    os.makedirs(SAL, exist_ok=True)
    matriz_osciloscopio()
    cadena_placa()
    matriz_mux()
    descomposicion_placa()
    print('listo:', SAL)
