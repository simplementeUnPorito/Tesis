#!/usr/bin/env python3
"""Dispersion del flanco SYNC entre esclavos, por START, desde el log del maestro.

Cada esclavo informa a que hora del reloj MAC del maestro subio SYNC, segun su
modelo FTM:
  [SYNCBC] broadcast real_maestro=...   START por broadcast (al llegar el paquete)
  [SYNCFTM] objetivo_maestro=... real_maestro=...   START programado por FTM
Los informes de un mismo START caen a menos de 2 s entre si en el log.

Uso: python lab/s3/dispersion_start.py lab/s3/maestro.log
"""
import re
import statistics
import sys

PAT = re.compile(r'^(\d\d):(\d\d):(\d\d) .*\[S(\d)>\].*\[(SYNCBC|SYNCFTM|SYNCRX)\].*?real_maestro=(\d+).*?conv=(\d)')


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'lab/s3/maestro.log'
    eventos = []
    for line in open(path, encoding='utf-8', errors='replace'):
        m = PAT.search(line)
        if not m or m.group(7) != '1':
            continue
        t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        eventos.append((t, m.group(5), int(m.group(4)), int(m.group(6))))
    grupos = []
    for ev in sorted(eventos):
        if grupos and ev[0] - grupos[-1][-1][0] <= 2 and ev[1] == grupos[-1][-1][1] \
                and ev[2] not in [e[2] for e in grupos[-1]]:
            grupos[-1].append(ev)
        else:
            grupos.append([ev])
    por_metodo = {}
    for g in grupos:
        if len(g) < 2:
            continue
        vals = [e[3] for e in g]
        spread = max(vals) - min(vals)
        por_metodo.setdefault(g[0][1], []).append(spread)
        print(f'{g[0][1]:8s} nodos={sorted(e[2] for e in g)} dispersion={spread} us')
    for k, v in por_metodo.items():
        print(f'\n{k}: {len(v)} STARTs, dispersion mediana {statistics.median(v)} us, '
              f'max {max(v)} us, min {min(v)} us')


if __name__ == '__main__':
    main()
