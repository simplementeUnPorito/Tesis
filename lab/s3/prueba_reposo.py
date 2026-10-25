"""Capturas separadas por reposo largo del maestro (sin trafico ESP-NOW).

Reproduce la falla de 2026-10-24: tras 45 s de maestro callado el esclavo
reescaneaba canales y se perdia el ARM/PRESTART de la captura siguiente.

  python lab/s3/prueba_reposo.py --reposo 60 --veces 3
"""
import argparse
import json
import glob
import subprocess
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument('--reposo', type=float, default=60)
ap.add_argument('--veces', type=int, default=3)
a = ap.parse_args()
fallas = 0
for k in range(a.veces):
    print(f'reposo {a.reposo:.0f} s...', flush=True)
    time.sleep(a.reposo)
    subprocess.run([sys.executable, 'lab/s3/captura_ws.py', '--modo', 'async', '--almacen', '1',
                    '--n', '300', '--timeout', '90', '--zweb'], capture_output=True)
    r = json.load(open(sorted(glob.glob('lab/s3/capturas/*/resumen.json'))[-1]))
    linea = ' | '.join(f"S{n}: {v['muestras']}" for n, v in r['nodos'].items() if n != '3')
    ok = all(v['muestras'] == 9000 for n, v in r['nodos'].items() if n != '3')
    fallas += 0 if ok else 1
    print(f'{k + 1}: {linea} {"OK" if ok else "FALLA"}', flush=True)
print(f'fallas {fallas}/{a.veces}')
