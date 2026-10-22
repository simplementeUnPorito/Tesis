"""Marcas de eje legibles para escalas log y symlog: '10 mV', '0,1 mV', '-1 mV'.

matplotlib rotula log/symlog con potencias (10^0, -10^-1), que no se leen
como voltaje. valores_con_unidad(ax) reemplaza esas marcas por valores 1-2-5
dentro del rango visible, con la unidad y coma decimal.
"""
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

_MANTISAS = (1, 2, 5)


def _formato(v, unidad):
    if v == 0:
        return '0'
    txt = ('%g' % v).replace('-', '−').replace('.', ',')
    return '%s %s' % (txt, unidad) if unidad else txt


def _candidatos(lo, hi, con_negativos, umbral):
    out = []
    for e in range(-4, 5):
        for m in _MANTISAS:
            v = m * 10.0 ** e
            if v < umbral:
                continue
            out.append(v)
            if con_negativos:
                out.append(-v)
    if con_negativos:
        out.append(0.0)
    return sorted(v for v in out if lo <= v <= hi)


def valores_con_unidad(ax, eje='y', unidad='mV', max_marcas=9):
    """Aplica marcas con unidad al eje 'x' o 'y' de ax (log o symlog)."""
    axis = ax.yaxis if eje == 'y' else ax.xaxis
    lo, hi = (ax.get_ylim() if eje == 'y' else ax.get_xlim())
    lo, hi = min(lo, hi), max(lo, hi)
    escala = axis.get_scale()
    if escala == 'symlog':
        umbral = axis.get_transform().linthresh
        vals = _candidatos(lo, hi, True, umbral)
        # menos marcas: solo potencias de 10 si hay demasiadas
        if len(vals) > max_marcas:
            vals = [v for v in vals if v == 0 or abs(np.log10(abs(v)) % 1) < 1e-9]
    else:
        vals = _candidatos(max(lo, 1e-12), hi, False, 0)
        if len(vals) > max_marcas:
            vals = [v for v in vals if abs(np.log10(v) % 1) < 1e-9]
    axis.set_major_locator(FixedLocator(vals))
    axis.set_major_formatter(FuncFormatter(lambda v, _p: _formato(v, unidad)))
    axis.set_minor_locator(NullLocator())
