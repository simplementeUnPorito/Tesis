"""Las mismas curvas del informe de alimentacion en varias escalas.

Una escala comun muestra las curvas grandes y aplasta las chicas; por eso cada
figura repite las curvas en lineal comun, symlog comun y zoom (o escala
propia por panel). Reusa los cargadores de informe_alimentacion e
informe_sd_resumen.

  python lab/informe_escalas.py --salida lab/informe_alimentacion
"""
import argparse
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import informe_alimentacion as ia  # noqa: E402
import informe_sd_resumen as isd  # noqa: E402

FS = ia.FS


def _captura_ambos(digi):
    # Los dos modulos parchean ruido_sd.no_utilizable con su propio _CAP; el
    # ultimo import gana. Este llena los dos.
    ia._CAP['digi'] = digi.copy()
    isd._CAP['digi'] = digi.copy()
    return ''


ia.rs.no_utilizable = _captura_ambos
LIMPIAS = ('Cargador', 'Dos powerbanks', 'Dos\npowerbanks')


def _curvas_tx():
    out = []
    for e, d in ia.CONFIGS:
        if not os.path.isdir(os.path.join(ia.LAB, d)):
            continue
        dd = ia.cargar(d)
        if 'RF240' not in dd:
            continue
        p = np.mean([x['promedio'] for x in dd['RF240']], axis=0)
        p = p - np.nanmean(p[:ia.rs.VENTANA_ANTES])
        ping = None
        if 'PING' in dd:
            ping = np.mean([x['promedio'] for x in dd['PING']], axis=0)
            ping = ping - np.nanmean(ping[:ia.rs.VENTANA_ANTES])
        out.append((e.replace('\n', ' '), p, ping, dd))
    return out


def _tres_escalas(curvas, titulo, ylabel, zoom_filtro, zoom_lim, salida, xlabel):
    """curvas: [(etiqueta, y)]; zoom_filtro(etiqueta) -> bool."""
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.8))
    colores = plt.cm.tab10(np.linspace(0, 1, 10))
    for i, (e, y) in enumerate(curvas):
        t = ia.t_ventana(y.size)
        c = colores[i % 10]
        axs[0].plot(t, y, lw=1, color=c, label=e)
        axs[1].plot(t, y, lw=1, color=c, label=e)
        if zoom_filtro(e):
            axs[2].plot(t, y, lw=1, color=c, label=e)
    axs[0].set_title('lineal, escala comun')
    axs[1].set_yscale('symlog', linthresh=0.1)
    axs[1].set_title('symlog comun (lineal entre +-0,1 mV)')
    axs[2].set_ylim(*zoom_lim)
    axs[2].set_title('zoom %.2g a %.2g mV (las chicas)' % zoom_lim)
    for ax in axs:
        ax.grid(alpha=.3)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
    axs[0].legend(fontsize=6.5)
    axs[2].legend(fontsize=6.5)
    fig.suptitle(titulo)
    fig.tight_layout()
    fig.savefig(salida, dpi=130)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--salida', default=os.path.join(ia.LAB, 'informe_alimentacion'))
    args = ap.parse_args(argv)
    os.makedirs(args.salida, exist_ok=True)
    plt.rcParams.update({'font.size': 9})

    # 1) brote de TX, SEo PGA x4
    tx = _curvas_tx()
    curvas = [(e, p) for e, p, _, _ in tx]
    limpias = lambda e: any(k.replace('\n', ' ') in e for k in LIMPIAS)  # noqa: E731
    _tres_escalas(curvas, 'Brote promedio de cada transmision en SEo (PGA x4), por alimentacion',
                  'SEo [mV]', limpias, (-0.15, 0.15),
                  os.path.join(args.salida, 'tx_escalas.png'), 'tiempo desde la transmision [ms]')

    # 1b) solo las limpias contra su PING (lo que queda es el ping I2C)
    fig, axs = plt.subplots(1, 3, figsize=(13, 3.2), sharey=True)
    for ax, (e, p, ping, _) in zip(axs, [x for x in tx if limpias(x[0])]):
        t = ia.t_ventana(p.size)
        if ping is not None:
            ax.plot(t, ping, color='#7f8c8d', lw=1, label='sin transmitir (PING)')
        ax.plot(t, p, color='#c0392b', lw=1, label='transmitiendo (RF240)')
        ax.set_title(e)
        ax.grid(alpha=.3)
        ax.set_xlabel('tiempo desde la transmision [ms]')
    axs[0].set_ylabel('SEo [mV]')
    axs[0].legend(fontsize=7)
    fig.suptitle('Configuraciones limpias: transmitir y no transmitir dan la misma curva')
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'tx_limpias_zoom.png'), dpi=130)
    plt.close(fig)

    # 2) senal cruda con escala propia por panel
    n = int(2 * FS)
    fig, axs = plt.subplots(len(tx), 1, figsize=(10, 1.5 * len(tx)), sharex=True)
    for ax, (e, _, _, dd) in zip(axs, tx):
        x = dd['RF240'][0]['x']
        seg = x[FS:FS + n] - np.median(x[FS:FS + n])
        ax.plot(np.arange(seg.size) / FS, seg, lw=.5, color='#2c3e50')
        ax.set_ylabel(e, rotation=0, ha='right', va='center', fontsize=8)
        ax.text(1.0, 1.0, 'rango %.2f mV' % np.ptp(seg), transform=ax.transAxes,
                ha='right', va='top', fontsize=7)
        ax.grid(alpha=.3)
    axs[-1].set_xlabel('tiempo [s]')
    fig.suptitle('Senal cruda en SEo transmitiendo, cada panel con su propia escala [mV]')
    fig.tight_layout()
    fig.savefig(os.path.join(args.salida, 'senal_cruda_escala_propia.png'), dpi=130)
    plt.close(fig)

    # 3) brote de la SD: PSoC contra ESP
    psoc = isd.cargar(os.path.join(isd.SD, 'E10_sd_alim_esp'))
    cargador = isd.cargar(os.path.join(isd.SD, 'E12_psoc_cargador'))
    esp_usb = isd.cargar(os.path.join(ia.LAB, 'ruido_sd_20261021_ferrita', 'E14_esd_ferrita'))
    esp_pb = isd.cargar(os.path.join(ia.LAB, 'ruido_rf_20261021_2powerbanks', 'R9b_lpo_campo'))
    curvas = [('SD por el PSoC (E10)', isd.prom(psoc, 'P4')),
              ('SD por el PSoC, PSoC en cargador (E12)', isd.prom(cargador, 'P4')),
              ('SD en el ESP, dos USB a la misma PC (E14)', isd.prom(esp_usb, 'ESD')),
              ('SD en el ESP, dos powerbanks', isd.prom(esp_pb, 'ESD'))]
    _tres_escalas(curvas, 'Brote promedio de cada escritura en la SD (LPo, PGA x8, PGAout x16)',
                  'LPo [mV]', lambda e: 'ESP' in e, (-1.0, 1.0),
                  os.path.join(args.salida, 'sd_escalas.png'), 'tiempo desde la escritura [ms]')
    print('ok')


if __name__ == '__main__':
    main()
