"""Figuras del informe de alimentacion/masa (ruido de TX, SD y baliza).

Configuraciones y experimentos fijos (2026-10-21); para otra placa, editar
CONFIGS / LPO. Escribe PNG y resumen.json en --salida.

  python lab/informe_alimentacion.py --salida lab/informe_alimentacion
"""
import argparse
import glob
import json
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
# (etiqueta, carpeta del experimento SEo PGA x4 con PING y RF240)
CONFIGS = [
    ('Dos USB a la misma PC\n(PSoC por KitProg)', 'ruido_rf_20261021_ferrita_conSD/W9_ganancia_pga2'),
    ('Todo desde\nel ESP', 'ruido_rf_20261021_alim_esp/P1_potencia_seo_x4'),
    ('Powerbank\nen estrella', 'ruido_rf_20261021_bateria/R8_seo_x4'),
    ('Powerbank\n+ 1 mF', 'ruido_rf_20261021_bateria_caps/R8_seo_x4'),
    ('Cargador\naislado (PSoC)', 'ruido_rf_20261021_ferrita_fuente/W9_ganancia_pga2'),
    ('Dos\npowerbanks', 'ruido_rf_20261021_2powerbanks/R8_seo_x4'),
    ('Dos powerbanks,\nferrita en corto', 'ruido_rf_20261021_ferrita_corto/R8_seo_x4'),
    ('Una bateria, union\nde masas en placa (1a)', 'ruido_rf_20261022_bateria_unica_punto/R8_seo_x4'),
    ('Una bateria, union\nde masas en placa (2a)', 'ruido_rf_20261022_bateria_unica_punto_rep/R8_seo_x4'),
    ('Una bateria,\nestrella real', 'ruido_rf_20261022_bateria_estrella/R8_seo_x4'),
]
# LPo ganancia de campo (x8 x16): BASE, ESD, RF240
LPO = [
    ('Dos powerbanks,\nferrita entre planos', 'ruido_rf_20261021_2powerbanks/R9b_lpo_campo'),
    ('Dos powerbanks,\nferrita en corto', 'ruido_rf_20261021_ferrita_corto/R9_lpo_campo'),
    ('Una bateria, union\nde masas en placa', 'ruido_rf_20261022_bateria_unica_punto_rep/R9_lpo_campo'),
    ('Una bateria,\nestrella real', 'ruido_rf_20261022_bateria_estrella/R9_lpo_campo'),
]
# una bateria: raiz con R8_seo_x4 y R9_lpo_campo (o R9b)
ESTRELLA = [
    ('Una bateria, lazo de masa', 'ruido_rf_20261022_bateria_unica_punto_rep'),
    ('Una bateria, estrella real', 'ruido_rf_20261022_bateria_estrella'),
    ('Dos powerbanks', 'ruido_rf_20261021_2powerbanks'),
]
_CAP = {}


def _sin_descarte(digi):
    _CAP['digi'] = digi.copy()
    return ''


rs.no_utilizable = _sin_descarte


def cargar(directorio):
    """{cond: [ {p2p, rms, promedio, x(mV)} ]} sin descartar por riel."""
    out = {}
    for ruta in sorted(glob.glob(os.path.join(LAB, directorio, '*.txt'))):
        r = rs._medir(ruta)
        if r is None:
            continue
        x = _CAP['digi'] * ar.UV_POR_CUENTA / 1000.0
        fr, p = welch(x - x.mean(), FS, nperseg=4096)
        b = (fr >= 5) & (fr <= 50)
        out.setdefault(r['cond'], []).append({
            'p2p': r['p2p_uV'] / 1000.0,
            'rms': float(np.sqrt(np.trapezoid(p[b], fr[b]))),
            'promedio': np.asarray(r['promedio']) * ar.UV_POR_CUENTA / 1000.0,
            'x': x, 'fr': fr, 'psd': p})
    return out


def exceso(datos, cond, ctrl):
    if cond not in datos or ctrl not in datos:
        return float('nan')
    a = np.mean([d['rms'] for d in datos[cond]])
    c = np.mean([d['rms'] for d in datos[ctrl]])
    return float(np.sqrt(max(a * a - c * c, 0.0)))


def t_ventana(n):
    return (np.arange(n) - rs.VENTANA_ANTES) / FS * 1000.0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=os.path.join(LAB, 'informe_alimentacion'))
    args = ap.parse_args(argv)
    os.makedirs(args.salida, exist_ok=True)
    plt.rcParams.update({'font.size': 9})
    resumen = {'seo_x4': [], 'lpo_campo': []}

    datos = [(et, cargar(d)) for et, d in CONFIGS if os.path.isdir(os.path.join(LAB, d))]
    for et, dd in datos:
        resumen['seo_x4'].append({
            'config': et.replace('\n', ' '),
            'brote_tx_mV': float(np.mean([d['p2p'] for d in dd.get('RF240', [])])) if 'RF240' in dd else None,
            'exceso_tx_mV': exceso(dd, 'RF240', 'PING'),
            'ping_mV': float(np.mean([d['rms'] for d in dd['PING']])) if 'PING' in dd else None,
            'off_mV': float(np.mean([d['rms'] for d in dd['OFF']])) if 'OFF' in dd else None,
        })

    # 1) barras: exceso por TX en banda (log)
    fig, ax = plt.subplots(figsize=(13, 3.8))
    et = [e for e, _ in datos]
    ex = [max(exceso(dd, 'RF240', 'PING'), 1e-3) for _, dd in datos]
    col = ['#c0392b' if v > 0.1 else '#27ae60' for v in ex]
    ax.bar(range(len(ex)), ex, color=col)
    ax.set_yscale('log')
    ax.set_xticks(range(len(et)), et, fontsize=8)
    ax.set_ylabel('exceso por TX, RMS 5-50 Hz')
    ax.set_title('Ruido que agrega cada transmision ESP-NOW (SEo, PGA x4)')
    for i, v in enumerate(ex):
        ax.text(i, v * 1.15, ('%.3f mV' % v).replace('.', ',') if v > 1e-3 else '~0', ha='center')
    valores_con_unidad(ax)
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'exceso_tx.png'), dpi=130)
    plt.close(fig)

    # 2) brote promedio sincronizado (temporal)
    filas = -(-len(datos) // 3)
    fig, axs = plt.subplots(filas, 3, figsize=(10, 2.5 * filas), sharex=True, squeeze=False)
    for ax in axs.flat[len(datos):]:
        ax.set_visible(False)
    for ax, (e, dd) in zip(axs.flat, datos):
        for cond, c in (('PING', '#7f8c8d'), ('RF240', '#c0392b')):
            if cond in dd:
                prom = np.mean([d['promedio'] for d in dd[cond]], axis=0)
                prom = prom - np.nanmean(prom[:rs.VENTANA_ANTES])
                ax.plot(t_ventana(prom.size), prom, color=c, lw=1, label=cond)
        ax.set_title(e.replace('\n', ' '))
        ax.grid(alpha=.3)
    for ax in axs[-1]:
        ax.set_xlabel('tiempo desde la transmision [ms]')
    for ax in axs[:, 0]:
        ax.set_ylabel('SEo [mV]')
    axs.flat[0].legend()
    fig.suptitle('Brote promedio sincronizado con cada transmision (cada panel con su escala)')
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'brote_promedio.png'), dpi=130)
    plt.close(fig)

    # 3) senal cruda 2 s transmitiendo (misma escala)
    fig, axs = plt.subplots(len(datos), 1, figsize=(10, 1.4 * len(datos)), sharex=True, sharey=True)
    n = int(2 * FS)
    for ax, (e, dd) in zip(axs, datos):
        if 'RF240' in dd:
            x = dd['RF240'][0]['x']
            seg = x[FS:FS + n] - np.median(x[FS:FS + n])
            ax.plot(np.arange(seg.size) / FS, seg, lw=.5, color='#2c3e50')
        ax.set_ylabel(e.replace('\n', ' '), rotation=0, ha='right', va='center', fontsize=8)
        ax.grid(alpha=.3)
    axs[-1].set_xlabel('tiempo [s]')
    fig.suptitle('Senal cruda en SEo (PGA x4) mientras el esclavo transmite, misma escala [mV]')
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'senal_cruda.png'), dpi=130)
    plt.close(fig)

    # 4) espectro del fondo (PING)
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    for e, dd in datos:
        if 'PING' in dd:
            p = np.mean([d['psd'] for d in dd['PING']], axis=0)
            ax.semilogy(dd['PING'][0]['fr'], np.sqrt(p) * 1000, lw=.8, label=e.replace('\n', ' '))
    ax.axvspan(5, 50, color='#f1c40f', alpha=.15, label='banda 5-50 Hz')
    ax.set_xlim(0, 1302)
    valores_con_unidad(ax, unidad='µV/√Hz')
    ax.set_xlabel('frecuencia [Hz]')
    ax.set_ylabel('densidad [uV/sqrt(Hz)]')
    ax.set_title('Fondo sin transmitir (PING): el cargador agrega su tono de ~600 Hz')
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'espectro_fondo.png'), dpi=130)
    plt.close(fig)

    # 5) LPo ganancia de campo: BASE / ESD / RF240
    lpo = [(e, cargar(d)) for e, d in LPO if os.path.isdir(os.path.join(LAB, d))]
    if lpo:
        fig, axs = plt.subplots(1, 2, figsize=(10, 3.4))
        conds = ['BASE', 'ESD', 'RF240']
        w = 0.8 / len(lpo)
        for i, (e, dd) in enumerate(lpo):
            v = [np.mean([d['rms'] for d in dd[c]]) if c in dd else np.nan for c in conds]
            axs[0].bar(np.arange(3) + i * w, v, w, label=e.replace('\n', ' '))
            resumen['lpo_campo'].append({'config': e.replace('\n', ' '), **{
                c: {'rms_mV': (float(np.mean([d['rms'] for d in dd[c]])) if c in dd else None),
                    'brote_mV': (float(np.mean([d['p2p'] for d in dd[c]])) if c in dd else None)}
                for c in conds}})
            if 'RF240' in dd:
                prom = np.mean([d['promedio'] for d in dd['RF240']], axis=0)
                prom = prom - np.nanmean(prom[:rs.VENTANA_ANTES])
                axs[1].plot(t_ventana(prom.size), prom, lw=1, label=e.replace('\n', ' '))
        axs[0].set_xticks(np.arange(3) + w * (len(lpo) - 1) / 2, ['base', 'SD escribiendo', 'TX'])
        axs[0].set_ylabel('RMS 5-50 Hz [mV]')
        axs[0].set_title('LPo, ganancia de campo x8 x16')
        axs[0].legend(fontsize=7)
        axs[1].set_xlabel('tiempo desde la transmision [ms]')
        axs[1].set_ylabel('LPo [mV]')
        axs[1].set_title('Brote promedio de TX en LPo')
        axs[1].grid(alpha=.3)
        axs[1].legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(os.path.join(args.salida, 'lpo_campo.png'), dpi=130)
        plt.close(fig)

    # 6) una bateria: lazo de masa contra estrella real (contra dos powerbanks)
    trio = [(e, d) for e, d in ESTRELLA if os.path.isdir(os.path.join(LAB, d, 'R8_seo_x4'))]
    if trio:
        fig, axs = plt.subplots(1, 3, figsize=(13, 3.6))
        colores = ['#c0392b', '#2980b9', '#27ae60']
        for (e, d), c in zip(trio, colores):
            for ax, exp in ((axs[0], 'R8_seo_x4'), (axs[1], 'R9_lpo_campo')):
                ruta = os.path.join(d, exp)
                # R9b (4 capturas por condicion) manda sobre R9 si existe
                if exp == 'R9_lpo_campo' and os.path.isdir(os.path.join(LAB, d, 'R9b_lpo_campo')):
                    ruta = os.path.join(d, 'R9b_lpo_campo')
                dd = cargar(ruta)
                if 'RF240' in dd:
                    prom = np.mean([x['promedio'] for x in dd['RF240']], axis=0)
                    prom = prom - np.nanmean(prom[:rs.VENTANA_ANTES])
                    ax.plot(t_ventana(prom.size), prom, lw=1.2, color=c, label=e)
                if exp == 'R9_lpo_campo':
                    v = [np.mean([x['rms'] for x in dd[k]]) if k in dd else np.nan
                         for k in ('BASE', 'ESD', 'RF240')]
                    i = colores.index(c)
                    axs[2].bar(np.arange(3) + i * 0.27, v, 0.27, color=c, label=e)
        axs[0].set_title('Brote de TX en SEo (PGA x4)')
        axs[0].set_ylabel('SEo [mV]')
        axs[1].set_title('Brote de TX en LPo (x8 x16)')
        axs[1].set_ylabel('LPo [mV]')
        for ax in axs[:2]:
            ax.set_xlabel('tiempo desde la transmision [ms]')
            ax.grid(alpha=.3)
        axs[0].legend(fontsize=7)
        axs[2].set_yscale('log')
        axs[2].set_xticks(np.arange(3) + 0.27, ['base', 'SD del ESP', 'TX'])
        axs[2].set_ylabel('RMS 5-50 Hz')
        axs[2].set_title('LPo x8 x16, ruido en banda')
        valores_con_unidad(axs[2])
        fig.suptitle('Una bateria: lazo de masa en la placa contra estrella real (y dos powerbanks)')
        fig.tight_layout()
        fig.savefig(os.path.join(args.salida, 'bateria_estrella.png'), dpi=130)
        plt.close(fig)

    with open(os.path.join(args.salida, 'resumen.json'), 'w', encoding='utf-8') as f:
        json.dump(resumen, f, indent=1, ensure_ascii=False)
    print(json.dumps(resumen, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
