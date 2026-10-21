"""Compara dos raices de campanas de ruido por experimento y condicion.

Uso: python lab/comparar_campanas.py RAIZ_A RAIZ_B [--etiquetas A B]
     [--salida DIR] [--por-config]
Por condicion: p2p del brote promedio (ruido_sd._medir) y RMS total / RMS
5-50 Hz (Welch, como espectro_condiciones). Compatible si
|A-B| < 2*sqrt(sdA^2/nA + sdB^2/nB) sobre el p2p.
"""
import argparse
import glob
import os
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.signal import welch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lab import espectro_condiciones as ec  # noqa: E402
from lab import ruido_sd  # noqa: E402

BANDA = (5.0, 50.0)


def _medir_captura(ruta):
    """Devuelve (cond, clave_config, p2p_uV), o None si no es medible."""
    try:
        meta, _, digi, _, _ = ruido_sd.ar.cargar(ruta)
    except Exception as e:  # archivo roto o parcial
        print('ignorado %s: %s' % (ruta, e), file=sys.stderr)
        return None
    cond = meta.get('cond', meta.get('condicion', '?'))
    clave = (meta.get('tap'), meta.get('pga'), meta.get('pgaout'))
    p2p = float('nan')
    try:
        r = ruido_sd._medir(ruta)
        if r is not None:
            p2p = float(r['p2p_uV'])
    except Exception as e:
        print('_medir fallo %s: %s' % (ruta, e), file=sys.stderr)
    return cond, clave, p2p


def leer_raiz(raiz):
    """Lee p2p y espectros agrupados por experimento y condicion."""
    out = {}
    if not os.path.isdir(raiz):
        print('raiz inexistente: %s' % raiz, file=sys.stderr)
        return out
    for d in sorted(os.listdir(raiz)):
        ruta = os.path.join(raiz, d)
        if not os.path.isdir(ruta):
            continue
        conds, clave = {}, None
        for r in sorted(glob.glob(os.path.join(ruta, '*.txt'))):
            m = _medir_captura(r)
            if m is None:
                continue
            clave = clave or m[1]
            conds.setdefault(m[0], {'p2p': [], 'rms': [], 'banda': []})[
                'p2p'].append(m[2])
        # Reutiliza la carga/limpieza de espectro_condiciones, que devuelve
        # una senal en uV por captura utilizable.
        espectros, _ = ec.cargar([ruta])
        for cond, xs in espectros.items():
            datos = conds.setdefault(
                cond, {'p2p': [], 'rms': [], 'banda': []})
            for x in xs:
                datos['rms'].append(float(np.std(x)))
                f, p = welch(x, fs=ec.FS, nperseg=min(8192, x.size))
                datos['banda'].append(float(np.sqrt(
                    ec.potencia_banda(f, p, *BANDA))))
        if conds:
            out[d] = {'clave': clave, 'conds': conds}
    return out


def _ms(vals):
    x = np.asarray(vals, dtype=float)
    x = x[np.isfinite(x)]
    if x.size == 0:
        return float('nan'), float('nan'), 0
    return float(x.mean()), (float(x.std(ddof=1)) if x.size > 1 else 0.0), x.size


def emparejar(A, B, por_config):
    """Lista de (nombre, conds_A, conds_B)."""
    if not por_config:
        return [(n, A[n]['conds'], B[n]['conds']) for n in A if n in B]

    def agrupar(R):
        g = {}
        for e in R.values():
            conds = g.setdefault(e['clave'], {})
            for c, v in e['conds'].items():
                dst = conds.setdefault(
                    c, {'p2p': [], 'rms': [], 'banda': []})
                for metrica in dst:
                    dst[metrica].extend(v[metrica])
        return g
    ga, gb = agrupar(A), agrupar(B)
    return [('tap%s_pga%s_pgaout%s' % k, ga[k], gb[k]) for k in ga if k in gb]


def _f(v, fmt='%.3g'):
    return fmt % v if np.isfinite(v) else '-'


def comparar(A, B, por_config):
    filas = []
    for nombre, ca, cb in emparejar(A, B, por_config):
        for cond in sorted(set(ca) & set(cb)):
            pa = _ms(ca[cond]['p2p'])
            pb = _ms(cb[cond]['p2p'])
            ta = _ms(ca[cond]['rms'])
            tb = _ms(cb[cond]['rms'])
            ba = _ms(ca[cond]['banda'])
            bb = _ms(cb[cond]['banda'])
            if pa[2] and pb[2]:
                err = 2 * np.sqrt(pa[1] ** 2 / pa[2] + pb[1] ** 2 / pb[2])
                compat = bool(abs(pa[0] - pb[0]) < err)
            else:
                compat = None
            filas.append((nombre, cond, pa[2], pb[2],
                          pa, pb, ba, bb, ta, tb, compat))
    return filas


def escribir_md(ruta, filas, ea, eb, raiz_a, raiz_b):
    L = ['# Comparacion de campanas', '',
         '%s = `%s`, %s = `%s`' % (ea, raiz_a, eb, raiz_b), '',
         'p2p = brote promedio (uV); RMS en uV. Compatible: '
         '|A-B| < 2*sqrt(sdA^2/nA + sdB^2/nB) sobre el p2p.', '']
    comp = tot = 0
    for exp in dict.fromkeys(f[0] for f in filas):
        L += ['## %s' % exp, '',
              '| cond | n %s | n %s | p2p %s | p2p %s | B/A | '
              'RMS 5-50 %s | RMS 5-50 %s | B/A | compatible |' % (ea, eb, ea, eb, ea, eb),
              '|---|---|---|---|---|---|---|---|---|---|']
        for f in (x for x in filas if x[0] == exp):
            _, cond, na, nb, pa, pb, ba, bb, ta, tb, ok = f
            rp = pb[0] / pa[0] if pa[0] else float('nan')
            rr = bb[0] / ba[0] if ba[0] else float('nan')
            tot += ok is not None
            comp += bool(ok)
            L.append('| %s | %d | %d | %s+-%s | %s+-%s | %s | %s+-%s | %s+-%s | %s | %s |' % (
                cond, na, nb, _f(pa[0]), _f(pa[1], '%.2g'), _f(pb[0]),
                _f(pb[1], '%.2g'), _f(rp, '%.2f'),
                _f(ba[0]), _f(ba[1], '%.2g'), _f(bb[0]), _f(bb[1], '%.2g'),
                _f(rr, '%.2f'),
                'n/d' if ok is None else ('si' if ok else 'NO')))
        L.append('')
    L.append('**Resumen: %d de %d condiciones compatibles** (%d sin dato).'
             % (comp, tot, len(filas) - tot))
    with open(ruta, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(L) + '\n')


def escribir_png(ruta, filas, ea, eb):
    fig, ax = plt.subplots(figsize=(6, 6))
    pts = [(f[4][0], f[5][0], f[0]) for f in filas
           if np.isfinite(f[4][0]) and np.isfinite(f[5][0])
           and f[4][0] > 0 and f[5][0] > 0]
    for exp in dict.fromkeys(p[2] for p in pts):
        s = [p for p in pts if p[2] == exp]
        ax.scatter([p[0] for p in s], [p[1] for p in s], s=25, label=exp)
    if pts:
        lo = min(min(p[0], p[1]) for p in pts) / 1.5
        hi = max(max(p[0], p[1]) for p in pts) * 1.5
        ax.plot([lo, hi], [lo, hi], 'k--', lw=1)
        ax.legend(fontsize=6)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('p2p %s (uV)' % ea)
    ax.set_ylabel('p2p %s (uV)' % eb)
    ax.set_title('p2p del brote promedio')
    ax.grid(True, which='both', alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta, dpi=130)
    plt.close(fig)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('raiz_a')
    ap.add_argument('raiz_b')
    ap.add_argument('--etiquetas', nargs=2, default=['A', 'B'])
    ap.add_argument('--salida', default=None)
    ap.add_argument('--por-config', action='store_true')
    a = ap.parse_args(argv)
    salida = a.salida or os.getcwd()
    os.makedirs(salida, exist_ok=True)
    A, B = leer_raiz(a.raiz_a), leer_raiz(a.raiz_b)
    filas = comparar(A, B, a.por_config)
    ea, eb = a.etiquetas
    escribir_md(os.path.join(salida, 'comparacion.md'), filas, ea, eb,
                a.raiz_a, a.raiz_b)
    escribir_png(os.path.join(salida, 'comparacion.png'), filas, ea, eb)
    print('%d condiciones comunes; salida en %s' % (len(filas), salida))
    return 0


if __name__ == '__main__':
    sys.exit(main())
