"""temperatura_ambiente.py - anota la temperatura ambiente del banco.

El nodo NO tiene sensor de temperatura: no hay componente DieTemp en el
proyecto y agregarlo obliga a re-sintetizar el TopDesign, que mueve pines. En
vez de eso se usa la temperatura del aire en la ubicacion del banco, que para
una placa dentro de una casa es un proxy razonable de la deriva lenta -no de
la temperatura de la juntura, que corre por encima y mas rapido-.

Ubicacion: plus code M9G7+69 Asuncion -> -25.3244, -57.6373. La precision del
punto es irrelevante: la temperatura del aire a 2 km a la redonda es la misma.

Dos modos:

  --vigilar   agrega una fila a un CSV cada N minutos mientras se mide. Sirve
              para tener el dato aunque despues no haya internet.
  --anotar    toma un resultados.jsonl ya medido y le agrega a cada visita la
              temperatura de SU hora, interpolada de la serie horaria. No abre
              el puerto serie y se puede correr cuantas veces se quiera.

Fuente: Open-Meteo (sin clave). Si no hay internet, --vigilar lo dice y sigue
intentando; --anotar falla ruidosamente en vez de inventar un numero.
"""
import argparse
import csv
import json
import os
import time
import urllib.request
from datetime import datetime, timedelta, timezone

LAT, LON = -25.3244, -57.6373
TZ = timezone(timedelta(hours=-3))          # America/Asuncion
URL_ACTUAL = ('https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s'
              '&current=temperature_2m,relative_humidity_2m&timezone=UTC')
URL_HORARIO = ('https://api.open-meteo.com/v1/forecast?latitude=%s&longitude=%s'
               '&hourly=temperature_2m,relative_humidity_2m&timezone=UTC'
               '&past_days=%d&forecast_days=2')


def _pedir(url, timeout=20):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))


def actual():
    d = _pedir(URL_ACTUAL % (LAT, LON))['current']
    return d['time'], d['temperature_2m'], d.get('relative_humidity_2m')


def serie_horaria(dias_atras=3):
    h = _pedir(URL_HORARIO % (LAT, LON, dias_atras))['hourly']
    fuera = []
    for t, temp, hum in zip(h['time'], h['temperature_2m'],
                            h['relative_humidity_2m']):
        if temp is None:
            continue
        ts = datetime.fromisoformat(t).replace(tzinfo=timezone.utc)
        fuera.append((ts, temp, hum))
    return sorted(fuera)


def interpolar(serie, cuando):
    """Temperatura a una hora dada, interpolando entre las dos horas vecinas.

    Devuelve None si la hora cae fuera de la serie: mejor un hueco que un
    numero inventado por extrapolacion."""
    if not serie or cuando < serie[0][0] or cuando > serie[-1][0]:
        return None, None
    for i in range(1, len(serie)):
        t0, a0, h0 = serie[i - 1]
        t1, a1, h1 = serie[i]
        if t0 <= cuando <= t1:
            span = (t1 - t0).total_seconds()
            f = 0.0 if span == 0 else (cuando - t0).total_seconds() / span
            hum = None if (h0 is None or h1 is None) else round(h0 + (h1 - h0) * f, 1)
            return round(a0 + (a1 - a0) * f, 2), hum
    return None, None


def vigilar(ruta, cada_min):
    nuevo = not os.path.exists(ruta)
    while True:
        try:
            t, temp, hum = actual()
            with open(ruta, 'a', newline='', encoding='utf-8') as fh:
                w = csv.writer(fh)
                if nuevo:
                    w.writerow(['utc', 'local', 'temp_C', 'humedad_pct'])
                    nuevo = False
                w.writerow([t, datetime.now(TZ).isoformat(timespec='seconds'),
                            temp, hum])
            print('%s  %.1f C  %s%%' % (t, temp, hum), flush=True)
        except Exception as e:
            print('sin dato de temperatura (%r); se reintenta' % e, flush=True)
        time.sleep(cada_min * 60)


def anotar(jsonl, salida=None):
    serie = serie_horaria()
    if not serie:
        raise SystemExit('no se pudo traer la serie horaria')
    filas = []
    sin = 0
    with open(jsonl, encoding='utf-8') as fh:
        for ln in fh:
            if not ln.strip():
                continue
            r = json.loads(ln)
            marca = r.get('marca')
            if marca:
                # `marca` es hora LOCAL sin desplazamiento; se la ancla a -03.
                cuando = datetime.fromisoformat(marca).replace(tzinfo=TZ)
                temp, hum = interpolar(serie, cuando.astimezone(timezone.utc))
            else:
                temp = hum = None
            if temp is None:
                sin += 1
            r['temp_ambiente_C'] = temp
            r['humedad_pct'] = hum
            filas.append(r)
    destino = salida or jsonl
    tmp = destino + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        for r in filas:
            fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    os.replace(tmp, destino)
    temps = [r['temp_ambiente_C'] for r in filas if r['temp_ambiente_C'] is not None]
    print('anotadas %d visitas (%d sin dato)' % (len(filas), sin))
    if temps:
        print('temperatura durante la campana: %.1f a %.1f C (rango %.1f)'
              % (min(temps), max(temps), max(temps) - min(temps)))
        print('OJO: es temperatura del AIRE, no de la juntura.  Sirve para ver')
        print('si la deriva acompana al ambiente, no como valor absoluto.')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--vigilar', metavar='CSV')
    ap.add_argument('--cada', type=int, default=10, help='minutos (def. 10)')
    ap.add_argument('--anotar', metavar='JSONL')
    ap.add_argument('--salida', metavar='JSONL')
    a = ap.parse_args()
    if a.vigilar:
        vigilar(a.vigilar, a.cada)
    elif a.anotar:
        anotar(a.anotar, a.salida)
    else:
        t, temp, hum = actual()
        print('%s  %.1f C  %s%%  (%.4f, %.4f)' % (t, temp, hum, LAT, LON))


if __name__ == '__main__':
    raise SystemExit(main())
