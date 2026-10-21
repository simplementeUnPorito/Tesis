"""Extraccion y persistencia de firmas temporales de fuentes de ruido."""
import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import ruido_sd  # noqa: E402


FS = 2604
GANANCIAS = (1, 2, 4, 8, 16, 24, 32, 48, 50)


def segmentos(x, posiciones, antes, despues):
    """Recorta eventos validos y resta la media de sus ``antes`` muestras."""
    x = np.asarray(x, dtype=np.float64)
    antes, despues = int(antes), int(despues)
    filas = []
    for pos in np.asarray(posiciones, dtype=np.int64).ravel():
        if pos - antes < 0 or pos + despues >= x.size:
            continue
        fila = x[pos - antes:pos + despues + 1].copy()
        base = fila[:antes].mean() if antes else 0.0
        filas.append(fila - base)
    ancho = antes + despues + 1
    return np.asarray(filas, dtype=np.float64).reshape((-1, ancho))


def _limpiar(digi, marcas):
    x = np.asarray(digi, dtype=np.float64).copy()
    idx = np.flatnonzero(marcas)
    idx = idx[(idx > 0) & (idx < x.size - 1)]
    x[idx] = 0.5 * (x[idx - 1] + x[idx + 1])
    centro = x[1:-1]
    aisladas = np.flatnonzero(
        (np.abs(centro - x[:-2]) > ruido_sd.MARCA_UMBRAL) &
        (np.abs(centro - x[2:]) > ruido_sd.MARCA_UMBRAL)) + 1
    x[aisladas] = 0.5 * (x[aisladas - 1] + x[aisladas + 1])
    return x


def _nulo_p95(xs, marcas_por_cap, antes, despues, cantidad, cuentas, repeticiones=20):
    """Percentil 95 de la varianza explicada por componente en segmentos sin evento."""
    ancho = antes + despues + 1
    fracs = []
    for r in range(repeticiones):
        rng = np.random.default_rng(1000 + r)
        filas = []
        for x, marcas, n in zip(xs, marcas_por_cap, cuentas):
            n_inicios = max(0, x.size - ancho + 1)
            ocupado = np.zeros(n_inicios + 1, dtype=bool)
            for m in marcas:
                ocupado[max(0, m - antes - ancho + 1):max(0, m + despues + 1)] = True
            libres = np.flatnonzero(~ocupado[:n_inicios])
            if libres.size == 0:
                continue
            for s0 in rng.choice(libres, size=n):
                fila = x[s0:s0 + ancho].copy()
                filas.append(fila - (fila[:antes].mean() if antes else 0.0))
        f = np.zeros(cantidad)
        if len(filas) > 1:
            m = np.asarray(filas)
            sv = np.linalg.svd(m - m.mean(axis=0), compute_uv=False) ** 2
            if sv.sum():
                v = sv[:cantidad] / sv.sum()
                f[:v.size] = v
        fracs.append(f)
    return np.percentile(np.asarray(fracs), 95, axis=0)


def extraer(dirs, cond, antes_ms=10, despues_ms=None, k=3):
    """Extrae la firma de ``cond`` desde volcados en uno o mas directorios.

    Devuelve media, desviacion por muestra y los primeros ``k`` componentes
    PCA, junto con su fraccion de varianza explicada y metadatos de captura.
    Con ``despues_ms=None`` la ventana posterior es el minimo entre 60 ms y
    0.92 veces la mediana del espaciado entre eventos menos ``antes``. Las
    componentes significativas son las primeras cuya varianza supera el p95
    de segmentos aleatorios sin evento (``k_significativas``). Las capturas que
    tocaron un riel se descartan; mezclar configuraciones es un error.
    """
    if isinstance(dirs, (str, os.PathLike)):
        dirs = [dirs]
    dirs = [os.fspath(d) for d in dirs]
    antes = int(round(float(antes_ms) * FS / 1000.0))
    condiciones = {str(c).upper() for c in (cond if isinstance(cond, (list, tuple, set)) else [cond])}
    caps, configuracion = [], None

    for directorio in dirs:
        rutas = [directorio] if os.path.isfile(directorio) else sorted(glob.glob(os.path.join(directorio, '*.txt')))
        for ruta in rutas:
            meta, _, digi, _, _ = ruido_sd.ar.cargar(ruta)
            condicion = str(meta.get('cond', meta.get('condicion', ''))).upper()
            if condicion not in condiciones or digi.size == 0:
                continue
            marcas = ruido_sd._marcas_desde_meta(meta, digi.size)
            x = _limpiar(digi, marcas)
            motivo = ruido_sd.no_utilizable(x)
            if motivo:
                print('NO UTILIZABLE %s: %s' % (os.path.basename(ruta), motivo), file=sys.stderr)
                continue
            cfg = tuple(int(meta[n]) for n in ('tap', 'pga', 'pgaout'))
            if configuracion is None:
                configuracion = cfg
            elif cfg != configuracion:
                raise ValueError('configuraciones mezcladas: %r y %r' % (configuracion, cfg))
            caps.append((x, np.flatnonzero(marcas)))

    if despues_ms is None:
        esp = np.concatenate([np.diff(m) for _, m in caps if m.size > 1] or [np.empty(0)])
        despues = int(round(0.060 * FS))
        if esp.size:
            despues = min(despues, int(0.92 * np.median(esp)) - antes)
        despues = max(despues, 1)
    else:
        despues = int(round(float(despues_ms) * FS / 1000.0))

    todas, xs, marcas_cap, cuentas = [], [], [], []
    for x, marcas in caps:
        seg = segmentos(x, marcas, antes, despues)
        if seg.size:
            todas.append(seg)
            xs.append(x)
            marcas_cap.append(marcas)
            cuentas.append(seg.shape[0])
    n_capturas = len(todas)

    if not todas:
        raise ValueError('sin eventos utilizables para condicion %s en %s' % (cond, ', '.join(dirs)))
    matriz = np.vstack(todas)
    media = matriz.mean(axis=0)
    centrada = matriz - media
    _, s, vt = np.linalg.svd(centrada, full_matrices=False)
    cantidad = min(int(k), vt.shape[0])
    componentes = vt[:cantidad]
    energia = s ** 2
    varianza = energia[:cantidad] / energia.sum() if energia.sum() else np.zeros(cantidad)
    nulo = _nulo_p95(xs, marcas_cap, antes, despues, cantidad, cuentas)
    sig = 0
    while sig < cantidad and varianza[sig] > nulo[sig]:
        sig += 1
    tap, pga, pgaout = configuracion
    factor_pga, factor_pgaout = GANANCIAS[pga], GANANCIAS[pgaout]
    return {
        'media': media, 'componentes': componentes,
        'varianza_explicada': varianza, 'std': matriz.std(axis=0),
        'varianza_nula_p95': nulo, 'k_significativas': int(sig),
        'n_eventos': int(matriz.shape[0]), 'n_capturas': n_capturas,
        'antes': antes, 'despues': despues, 'fs': FS,
        'tap': tap, 'pga': pga, 'pgaout': pgaout,
        'ganancia_total': factor_pga if tap == 0 else factor_pga * factor_pgaout,
        'cond': '/'.join(sorted(condiciones)), 'dirs': dirs,
    }


def guardar(firma, ruta_base):
    """Guarda los arrays en ``ruta_base.npz`` y los metadatos en JSON."""
    ruta_base = os.fspath(ruta_base)
    padre = os.path.dirname(os.path.abspath(ruta_base))
    os.makedirs(padre, exist_ok=True)
    nombres = ('media', 'componentes', 'varianza_explicada', 'std', 'varianza_nula_p95')
    np.savez_compressed(ruta_base + '.npz', **{n: firma[n] for n in nombres})
    meta = {k: v for k, v in firma.items() if k not in nombres}
    with open(ruta_base + '.json', 'w', encoding='utf-8') as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def cargar(ruta_base):
    """Carga y devuelve una firma escrita previamente por :func:`guardar`."""
    ruta_base = os.fspath(ruta_base)
    with open(ruta_base + '.json', encoding='utf-8') as fh:
        firma = json.load(fh)
    with np.load(ruta_base + '.npz') as datos:
        firma.update({n: datos[n] for n in datos.files})
    return firma


def _desplazar(v, d):
    """Desplaza ``v`` d muestras (positivo = retrasa) repitiendo el borde."""
    if d == 0:
        return v
    out = np.empty_like(v)
    if d > 0:
        out[d:] = v[:-d]
        out[:d] = v[0]
    else:
        out[:d] = v[-d:]
        out[d:] = v[-1]
    return out


def _pasaaltos(x):
    from scipy.signal import butter, sosfiltfilt
    return sosfiltfilt(butter(4, 60.0, btype='highpass', fs=FS, output='sos'), x)


def restar(x, posiciones, firma, k=None, corrimiento=2, base=True, escala=1, modo='libre'):
    """Resta la firma de cada evento segun ``modo``.

    ``libre``: ajusta media, k componentes y recta, probando corrimientos
    enteros en [-corrimiento, corrimiento] (menor residuo). ``fija``: resta la
    media con amplitud 1 y sin componentes; el corrimiento maximiza la
    correlacion de versiones pasaaltos (Butterworth 4, 60 Hz, filtfilt).
    ``alta``: ajusta media y componentes por minimos cuadrados solo sobre
    versiones pasaaltos sin baseline y resta las plantillas completas.
    ``k=None`` usa ``k_significativas`` de la firma (todas si no existe).
    Devuelve la senal limpia y un arreglo (n, 2 + nf) con posicion,
    corrimiento y coeficientes (NaN si el evento no cabe).
    """
    if modo not in ('libre', 'fija', 'alta'):
        raise ValueError('modo desconocido: %r' % (modo,))
    x = np.asarray(x, dtype=np.float64).copy()
    antes, despues = int(firma['antes']), int(firma['despues'])
    comps = np.asarray(firma['componentes'], dtype=np.float64)
    if k is None:
        k = int(firma['k_significativas']) if 'k_significativas' in firma else comps.shape[0]
    kk = 0 if modo == 'fija' else min(int(k), comps.shape[0])
    plantillas = [np.asarray(firma['media'], dtype=np.float64) * escala]
    plantillas += [c * escala for c in comps[:kk]]
    nf = len(plantillas)
    ancho = antes + despues + 1
    t = np.arange(ancho, dtype=np.float64) / ancho
    rango = range(-int(corrimiento), int(corrimiento) + 1)
    if modo != 'libre':
        x_hp = _pasaaltos(x)
        plant_hp = [_pasaaltos(p) for p in plantillas]
    coefs = []
    for pos in np.asarray(posiciones, dtype=np.int64).ravel():
        fila = np.full(2 + nf, np.nan)
        fila[0] = pos
        if pos - antes < 0 or pos + despues >= x.size:
            coefs.append(fila)
            continue
        seg = x[pos - antes:pos + despues + 1]
        if modo == 'fija':
            seg_hp = x_hp[pos - antes:pos + despues + 1]
            d = max(rango, key=lambda d: float(seg_hp @ _desplazar(plant_hp[0], d)))
            x[pos - antes:pos + despues + 1] = seg - _desplazar(plantillas[0], d)
            fila[1], fila[2] = d, 1.0
        elif modo == 'alta':
            seg_hp = x_hp[pos - antes:pos + despues + 1]
            mejor = None
            for d in rango:
                A = np.column_stack([_desplazar(p, d) for p in plant_hp])
                c = np.linalg.lstsq(A, seg_hp, rcond=None)[0]
                res = float(np.sum((seg_hp - A @ c) ** 2))
                if mejor is None or res < mejor[0]:
                    mejor = (res, d, c)
            _, d, c = mejor
            full = np.column_stack([_desplazar(p, d) for p in plantillas])
            x[pos - antes:pos + despues + 1] = seg - full @ c
            fila[1] = d
            fila[2:] = c
        else:
            mejor = None
            for d in rango:
                cols = [_desplazar(p, d) for p in plantillas]
                A = np.column_stack(cols + ([np.ones(ancho), t] if base else []))
                c = np.linalg.lstsq(A, seg, rcond=None)[0]
                res = float(np.sum((seg - A @ c) ** 2))
                if mejor is None or res < mejor[0]:
                    mejor = (res, d, c, A)
            _, d, c, A = mejor
            x[pos - antes:pos + despues + 1] = seg - A[:, :nf] @ c[:nf]
            fila[1] = d
            fila[2:] = c[:nf]
        coefs.append(fila)
    return x, np.asarray(coefs).reshape((-1, 2 + nf))


def _rms(x):
    return float(np.sqrt(np.mean((x - x.mean()) ** 2)))


def _rms_banda(x, lo=5.0, hi=50.0):
    from scipy.signal import welch
    f, pxx = welch(x - x.mean(), fs=FS, nperseg=min(8192, x.size))
    m = (f >= lo) & (f <= hi)
    return float(np.sqrt(np.sum(pxx[m]) * (f[1] - f[0])))


def _cargar_capturas(dirs, condiciones):
    """Lista de (ruta, x_limpio_en_cuentas, indices_de_marcas) utilizables."""
    out = []
    for d in dirs:
        for ruta in sorted(glob.glob(os.path.join(d, '*.txt'))):
            meta, _, digi, _, _ = ruido_sd.ar.cargar(ruta)
            cond = str(meta.get('cond', meta.get('condicion', ''))).upper()
            if cond not in condiciones or digi.size == 0:
                continue
            marcas = ruido_sd._marcas_desde_meta(meta, digi.size)
            x = _limpiar(digi, marcas)
            if ruido_sd.no_utilizable(x):
                continue
            out.append((ruta, x, np.flatnonzero(marcas)))
    return out


def _como_conjunto(c):
    return {str(v).upper() for v in (c if isinstance(c, (list, tuple, set)) else [c])}


MODOS = (('fija', 'fija', 0), ('alta_k0', 'alta', 0), ('alta_ksig', 'alta', None), ('libre_k0', 'libre', 0))


def evaluar(dirs, cond, ref_cond, modos=MODOS):
    """Leave-one-capture-out: cuanto exceso de ruido se elimina por modo.

    ``modos`` es una secuencia de (nombre, modo, k). Devuelve {nombre:
    metricas}: RMS en uV (total y 5-50 Hz) antes/despues/ref, fraccion de
    exceso eliminada y distorsion RMS(restar(x+s)-restar(x)-s)/RMS(s) de un
    paquete gaussiano de 20 Hz inyectado en capturas de referencia.
    """
    if isinstance(dirs, (str, os.PathLike)):
        dirs = [dirs]
    dirs = [os.fspath(d) for d in dirs]
    uv = ruido_sd.ar.UV_POR_CUENTA
    caps = _cargar_capturas(dirs, _como_conjunto(cond))
    caps_ref = _cargar_capturas(dirs, _como_conjunto(ref_cond))
    if len(caps) < 2:
        raise ValueError('hace falta >=2 capturas de %s en %s' % (cond, ', '.join(dirs)))
    ref_tot = [_rms(c[1]) * uv for c in caps_ref]
    ref_ban = [_rms_banda(c[1]) * uv for c in caps_ref]
    rng = np.random.default_rng(12345)
    nombres = ('tot_a', 'tot_d', 'ban_a', 'ban_d', 'exceso', 'distorsion')
    acum = {m[0]: {n: [] for n in nombres} for m in modos}
    ancho = int(0.3 * FS)
    tt = np.arange(ancho) / FS
    paquete = np.exp(-0.5 * ((tt - 0.15) / 0.05) ** 2) * np.sin(2 * np.pi * 20 * tt)
    for i, (_, x, pos) in enumerate(caps):
        firma = extraer([c[0] for j, c in enumerate(caps) if j != i], cond, k=3)
        ta, ba = _rms(x) * uv, _rms_banda(x) * uv
        for nom, modo, k in modos:
            y, _ = restar(x, pos, firma, k=k, modo=modo)
            a = acum[nom]
            a['tot_a'].append(ta)
            a['tot_d'].append(_rms(y) * uv)
            a['ban_a'].append(ba)
            a['ban_d'].append(_rms_banda(y) * uv)
            if ref_tot and ta != np.mean(ref_tot):
                a['exceso'].append((ta - a['tot_d'][-1]) / (ta - np.mean(ref_tot)))
        for _, xr, _ in caps_ref:
            n = xr.size
            falsas = pos[pos < n]
            if falsas.size == 0 or n < 2 * ancho:
                continue
            instantes = rng.integers(0, n - ancho, size=3)
            paq = np.zeros(n)
            for s0 in instantes:
                paq[s0:s0 + ancho] += 5 * _rms(xr) * paquete
            for nom, modo, k in modos:
                limpio, _ = restar(xr, falsas, firma, k=k, modo=modo)
                resta, _ = restar(xr + paq, falsas, firma, k=k, modo=modo)
                errs = []
                for s0 in instantes:
                    w = slice(s0, s0 + ancho)
                    dif = (resta[w] - limpio[w]) - paq[w]
                    errs.append(np.sqrt(np.mean(dif ** 2)) / np.sqrt(np.mean(paq[w] ** 2)))
                acum[nom]['distorsion'].append(float(np.mean(errs)))
    media = lambda v: float(np.mean(v)) if len(v) else float('nan')
    return {k: {'tot_a': media(a['tot_a']), 'tot_d': media(a['tot_d']), 'tot_ref': media(ref_tot),
                'ban_a': media(a['ban_a']), 'ban_d': media(a['ban_d']), 'ban_ref': media(ref_ban),
                'exceso': media(a['exceso']), 'distorsion': media(a['distorsion']), 'n_capturas': len(caps)}
            for k, a in acum.items()}


def _casos_evaluacion(lab):
    sd = os.path.join(lab, 'ruido_sd_20261019')
    rf = os.path.join(lab, 'ruido_rf_20261020')
    w5 = [os.path.join(rf, 'W5_lpo_pgaout1'), os.path.join(rf, 'W5c_lpo_pgaout1')]
    return [
        ('rf_tx_240', w5, 'RF240', 'PING'),
        ('rf_tx_10', w5, 'RF10', 'PING'),
        ('sd_escritura', [os.path.join(sd, 'E3_pgaout0')], ('P4', 'REAL'), 'BASE'),
        ('rf_rx', [os.path.join(rf, 'W4c_rx_pgaout16')], 'RX', 'PING'),
        ('rf_tx_240_SEo', [os.path.join(rf, 'W9_ganancia_pga2')], 'RF240', 'PING'),
    ]


def _evaluar_todas(salida):
    lab = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(salida, exist_ok=True)
    ks = [m[0] for m in MODOS]
    filas, datos = [], []
    cab = ('| caso | modo | RMS antes [uV] | despues | ref | 5-50 Hz antes | despues | ref | '
           'exceso eliminado | distorsion |\n|---|---|---:|---:|---:|---:|---:|---:|---:|---:|\n')
    for nombre, dirs, cond, ref in _casos_evaluacion(lab):
        faltan = [d for d in dirs if not os.path.isdir(d)]
        if faltan:
            print('AVISO: se omite %s: no existe %s' % (nombre, ', '.join(faltan)), file=sys.stderr)
            continue
        try:
            res = evaluar(dirs, cond, ref, MODOS)
        except ValueError as exc:
            print('AVISO: se omite %s: %s' % (nombre, exc), file=sys.stderr)
            continue
        datos.append((nombre, res))
        for k in ks:
            r = res[k]
            filas.append('| %s | %s | %.2f | %.2f | %.2f | %.2f | %.2f | %.2f | %.3f | %.3f |' % (
                nombre, k, r['tot_a'], r['tot_d'], r['tot_ref'], r['ban_a'], r['ban_d'],
                r['ban_ref'], r['exceso'], r['distorsion']))
        print(nombre, {k: round(res[k]['exceso'], 3) for k in ks},
              {k: round(res[k]['distorsion'], 3) for k in ks})
    if not datos:
        raise RuntimeError('ningun caso evaluable')
    with open(os.path.join(salida, 'evaluacion.md'), 'w', encoding='utf-8') as fh:
        fh.write('# Evaluacion de resta de firmas (leave-one-capture-out)\n\n' + cab + '\n'.join(filas) +
                 '\n\n---\nIA principal: Codex GPT-5; Delegados: Claude Sonnet 5.5 (implementacion); '
                 'Fallbacks: ninguno.\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    w = 0.8 / len(ks)
    for j, k in enumerate(ks):
        xs = np.arange(len(datos)) + j * w
        a1.bar(xs, [d[1][k]['exceso'] for d in datos], w, label=k)
        a2.bar(xs, [d[1][k]['distorsion'] for d in datos], w, label=k)
    for ax, tit in ((a1, 'fraccion de exceso eliminada'), (a2, 'distorsion del paquete 20 Hz')):
        ax.set_xticks(np.arange(len(datos)) + w)
        ax.set_xticklabels([d[0] for d in datos], rotation=20, fontsize=7)
        ax.set_title(tit)
        ax.grid(alpha=.2)
        ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(salida, 'evaluacion.png'), dpi=150)
    plt.close(fig)


def _catalogo(lab):
    sd = os.path.join(lab, 'ruido_sd_20261019')
    rf = os.path.join(lab, 'ruido_rf_20261020')
    entradas = [
        ('sd_escritura', ('P4', 'REAL'), [os.path.join(sd, 'E3_pgaout0')]),
    ]
    entradas += [('sd_escritura', 'P4', [os.path.join(sd, 'E2_tap%d' % t)]) for t in range(5)]
    entradas += [
        ('rf_tx_240', 'RF240', [os.path.join(rf, 'W5_lpo_pgaout1'), os.path.join(rf, 'W5c_lpo_pgaout1')]),
    ]
    entradas += [('rf_tx_240', 'RF240', [os.path.join(rf, 'W5_tap%d' % t)]) for t in range(4)]
    entradas += [('rf_tx_240', 'RF240', [os.path.join(rf, 'W9_ganancia_pga%d' % p)]) for p in (0, 2, 3, 4)]
    entradas += [
        ('rf_tx_10', 'RF10', [os.path.join(rf, 'W5_lpo_pgaout1'), os.path.join(rf, 'W5c_lpo_pgaout1')]),
        ('rf_tx_10', 'RF10', [os.path.join(rf, 'W9_rf10_pga0')]),
        ('rf_rx', 'RX', [os.path.join(rf, 'W4b_rx_pgaout1')]),
        ('rf_rx', 'RX', [os.path.join(rf, 'W4c_rx_pgaout16')]),
        ('i2c_ping', 'PING', [os.path.join(rf, 'W5c_lpo_pgaout1')]),
        ('i2c_ping', 'PING', [os.path.join(rf, 'W4c_rx_pgaout16')]),
        ('i2c_ping', 'PING', [os.path.join(rf, 'W9_ganancia_pga0')]),
    ]
    return entradas


def _informes(firmas, salida):
    cab = '| fuente | config | n eventos | p2p media [uV] | varianza k=1 | k=2 | k=3 | k_significativas | archivo |\n'
    sep = '|---|---|---:|---:|---:|---:|---:|---:|---|\n'
    filas = []
    for fuente, nombre, f in firmas:
        ve = list(f['varianza_explicada']) + [float('nan')] * 3
        p2p_uv = float(np.ptp(f['media'])) * ruido_sd.ar.UV_POR_CUENTA
        cfg = 'tap%d pga%d pgaout%d' % (f['tap'], f['pga'], f['pgaout'])
        filas.append('| %s | %s | %d | %.3f | %.4f | %.4f | %.4f | %d | %s |' %
                     (fuente, cfg, f['n_eventos'], p2p_uv, ve[0], ve[1], ve[2],
                      f.get('k_significativas', -1), nombre + '.npz'))
    with open(os.path.join(salida, 'firmas.md'), 'w', encoding='utf-8') as fh:
        fh.write('# Firmas de ruido\n\n' + cab + sep + '\n'.join(filas) +
                 '\n\n---\nIA principal: Codex GPT-5; Delegados: ninguno; Fallbacks: ninguno.\n')

    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    n = len(firmas)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 3.2 * rows), squeeze=False)
    for ax, (fuente, nombre, f) in zip(axes.flat, firmas):
        t = (np.arange(f['media'].size) - f['antes']) * 1000.0 / f['fs']
        media, std = f['media'], f['std']
        ax.fill_between(t, media - std, media + std, alpha=.22)
        ax.plot(t, media, lw=1.3, label='media')
        escala = np.max(np.abs(media)) or 1.0
        for i, comp in enumerate(f['componentes'][:3]):
            maximo = np.max(np.abs(comp)) or 1.0
            ax.plot(t, comp * escala / maximo, lw=.8, label='PC%d' % (i + 1))
        ax.axvline(0, color='.4', lw=.6, ls='--')
        ax.set_title(nombre, fontsize=8)
        ax.grid(alpha=.2)
        ax.legend(fontsize=6, ncol=4)
    for ax in axes.flat[n:]:
        ax.axis('off')
    fig.supxlabel('tiempo [ms]')
    fig.supylabel('cuentas ADC')
    fig.tight_layout()
    fig.savefig(os.path.join(salida, 'firmas.png'), dpi=150)
    plt.close(fig)


def _extraer_todas(salida):
    lab = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(salida, exist_ok=True)
    hechas = []
    for fuente, cond, dirs in _catalogo(lab):
        faltan = [d for d in dirs if not os.path.isdir(d)]
        if faltan:
            print('AVISO: se omite %s (%s): no existe %s' % (fuente, cond, ', '.join(faltan)), file=sys.stderr)
            continue
        try:
            firma = extraer(dirs, cond)
        except ValueError as exc:
            print('AVISO: se omite %s (%s): %s' % (fuente, cond, exc), file=sys.stderr)
            continue
        nombre = '%s_tap%d_pga%d_pgaout%d' % (fuente, firma['tap'], firma['pga'], firma['pgaout'])
        base = os.path.join(salida, nombre)
        guardar(firma, base)
        hechas.append((fuente, nombre, firma))
        print('%s: %d eventos' % (nombre, firma['n_eventos']))
    if not hechas:
        raise RuntimeError('no se extrajo ninguna firma')
    _informes(hechas, salida)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='orden', required=True)
    p = sub.add_parser('extraer')
    p.add_argument('--todas', action='store_true', required=True)
    p.add_argument('--salida', default=os.path.join(os.path.dirname(__file__), 'firmas'))
    e = sub.add_parser('evaluar')
    e.add_argument('--todas', action='store_true', required=True)
    e.add_argument('--salida', default=os.path.join(os.path.dirname(__file__), 'firmas'))
    args = parser.parse_args(argv)
    if args.orden == 'evaluar':
        _evaluar_todas(os.path.abspath(args.salida))
    else:
        _extraer_todas(os.path.abspath(args.salida))


if __name__ == '__main__':
    main()
