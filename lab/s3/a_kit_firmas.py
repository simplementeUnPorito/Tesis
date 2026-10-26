"""Pasa capturas de captura_ws.py al formato de lab/ruido_firmas (samples, flags).

  python lab/s3/a_kit_firmas.py lab/s3/capturas/<stamp> [...] --placa SIM_S3 --escenario rt_sd

Por cada nodo<n>.npz escribe lab/ruido_firmas/capturas/<placa>/<escenario>_<stamp>_n<n>.npz.
Las muestras con NaN (lotes perdidos) se descartan: la captura tiene que estar
completa para entrar al kit, como en captura.py.
"""
import argparse
import json
from pathlib import Path

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('capturas', nargs='+')
    ap.add_argument('--placa', default='SIM_S3')
    ap.add_argument('--escenario', default='rt_sd')
    ap.add_argument('--fs', type=float, default=2000.0,
                    help='Fs de la captura; usar la informada por HELLO (2000 en modo SOC)')
    ap.add_argument('--out', default='lab/ruido_firmas/capturas')
    a = ap.parse_args()
    out = Path(a.out) / a.placa
    out.mkdir(parents=True, exist_ok=True)
    for cap in a.capturas:
        cap = Path(cap)
        for f in sorted(cap.glob('nodo*.npz')):
            z = np.load(f)
            x, m = z['raw'], z['marks']
            if np.isnan(x).any():
                print(f'{f}: {int(np.isnan(x).sum())} NaN, se descarta')
                continue
            n = f.stem.replace('nodo', '')
            stem = f'{a.escenario}_{cap.name}_n{n}'
            np.savez_compressed(out / f'{stem}.npz', samples=x.astype(np.float64),
                                flags=m.astype(np.uint8), fs=np.float64(a.fs), mode=np.int16(0),
                                n_batches=np.int32(x.size // 30), scenario=np.str_(a.escenario),
                                timestamp=np.str_(cap.name), placa=np.str_(a.placa),
                                board_label=np.str_(a.placa))
            meta = {'samples': int(x.size), 'marked_samples': int(np.count_nonzero(m)), 'fs': a.fs,
                    'scenario': a.escenario, 'timestamp': cap.name, 'placa': a.placa, 'node': int(n)}
            (out / f'{stem}.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')
            print(f'{stem}: {x.size} muestras, {meta["marked_samples"]} marcadas')


if __name__ == '__main__':
    main()
