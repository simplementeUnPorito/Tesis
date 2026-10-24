"""Verifica las firmas de ruido contra la verdad del PSoC simulado (sim_psoc).

El simulador suma un artefacto conocido en cada muestra marcada:
  I2C 0x08       +3000 decreciente en ceil(fs/1000) muestras desde el inicio de la racha
  SD_IO 0x01     rampa hasta +8000 en ceil(5 fs/1000) muestras, luego +8000
  RADIO_TX 0x04  +6000 solo en la primera muestra de la racha
  AP_BEACON 0x10 +2000 en cada muestra marcada
Se reconstruye la serie "solo artefactos" desde las marcas de cada captura, se
estima con el mismo ajuste conjunto de firmas.py (mismo pasa-altos) y se
compara con la plantilla estimada sobre los datos reales que paso por toda la
cadena (PSoC simulado -> ESP -> radio -> maestro -> web).

  python lab/s3/verificar_firmas.py lab/ruido_firmas/capturas/SIM_S3
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'ruido_firmas'))
from comun import load_capture, capture_files, event_runs  # noqa: E402
from firmas import fit_joint_templates, FLAG_TYPES  # noqa: E402

BITS = {'I2C': 0x08, 'SD_IO': 0x01, 'RADIO_TX': 0x04, 'AP_BEACON': 0x10}


def verdad(flags, fs):
    a = np.zeros(flags.size)
    n_i2c = math.ceil(fs / 1000)
    n_sd = math.ceil(fs * 5 / 1000)
    for s, e in event_runs(flags, BITS['I2C']):
        for k in range(s, min(e, s + n_i2c)):
            a[k] += 3000 * (n_i2c - (k - s)) / n_i2c
    for s, e in event_runs(flags, BITS['SD_IO']):
        for k in range(s, e):
            a[k] += 8000 * min(k - s + 1, n_sd) / n_sd
    for s, _ in event_runs(flags, BITS['RADIO_TX']):
        a[s] += 6000
    for s, e in event_runs(flags, BITS['AP_BEACON']):
        a[s:e] += 2000
    return a


def main():
    carpeta = sys.argv[1]
    pre, largo, hp = 4, 32, 150.0
    reales, verdades = [], []
    for f in capture_files(carpeta):
        r = load_capture(f)
        fs = float(r.get('fs', 2604.0))
        x = np.asarray(r['samples'], float)
        reales.append({'samples': x - np.median(x), 'flags': r['flags'], 'fs': fs})
        verdades.append({'samples': verdad(np.asarray(r['flags'], np.uint8), fs), 'flags': r['flags'], 'fs': fs})
    tr = fit_joint_templates(reales, pre, largo, hp=hp)
    tv = fit_joint_templates(verdades, pre, largo, hp=hp)
    out = {}
    print(f'{len(reales)} capturas; plantilla onset, pre={pre}, largo={largo}, hp={hp} Hz')
    for nombre in BITS:
        a, b = tr[nombre]['onset'], tv[nombre]['onset']
        corr = float(np.corrcoef(a, b)[0, 1]) if np.std(a) > 0 and np.std(b) > 0 else float('nan')
        amp = float(np.abs(a).max() / max(np.abs(b).max(), 1e-9))
        lag = int(np.argmax(np.abs(a)) - np.argmax(np.abs(b)))
        ok = corr > 0.9 and 0.8 < amp < 1.25 and lag == 0
        out[nombre] = {'correlacion': corr, 'amplitud_estimada_sobre_verdad': amp, 'desfase_muestras': lag, 'ok': ok}
        print(f'{nombre:10s} correlacion={corr:6.3f}  amplitud est/verdad={amp:5.2f}  desfase={lag:+d}  '
              f'{"OK" if ok else "REVISAR"}')
    for nombre in ('SD_SYNC', 'MASTER_RX'):
        if nombre in tr:
            print(f'{nombre:10s} sin artefacto inyectado: pico estimado {np.abs(tr[nombre]["onset"]).max():.0f} cuentas')
    Path(carpeta, 'verificacion_simulador.json').write_text(json.dumps(out, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
