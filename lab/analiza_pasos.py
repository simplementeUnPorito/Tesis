"""analiza_pasos.py - saca la dinamica real de cada actuador de un CSV de diag_par.

    py -3 analiza_pasos.py diag_x50_x1.csv [tap]

Busca cada cambio AISLADO de un IDAC (ningun otro se movio y nadie vuelve a
moverse durante la ventana de observacion) y mide como responde el tap elegido
(LP por defecto) a 2, 5, 10, 20 y 40 s.  De ahi salen dos numeros que el lazo
necesita y hoy estan puestos a ojo:

  * la PENDIENTE de regimen (mV por codigo) de cada actuador en ese punto,
  * el TIEMPO DE ESTABLECIMIENTO, que es lo que deberia valer el intervalo
    entre pasos del rescate (CP_RESCUE_MS).  Esperar menos mide un transitorio
    y corrige de menos; esperar de mas hace lento el arranque.
"""
import sys, csv, collections

VENTANAS = (2, 5, 10, 20, 40, 60)


def main(ruta, tap='LP'):
    with open(ruta) as fh:
        filas = [r for r in csv.DictReader(fh)]

    def num(r, k):
        v = r.get(k)
        return int(v) if v not in (None, '', 'None') else None

    t = [num(r, 't') for r in filas]
    y = [num(r, tap) for r in filas]
    idacs = ['I0', 'I1', 'I2', 'I3']
    cod = {n: [num(r, n) for r in filas] for n in idacs}

    print('%s  (%d muestras, %d..%d s)' % (ruta, len(filas), t[0], t[-1]))
    resumen = collections.defaultdict(list)
    for i in range(1, len(filas)):
        cambia = [n for n in idacs
                  if cod[n][i] is not None and cod[n][i - 1] is not None
                  and cod[n][i] != cod[n][i - 1]]
        if len(cambia) != 1:
            continue
        n = cambia[0]
        d = cod[n][i] - cod[n][i - 1]
        if y[i - 1] is None:
            continue
        base = y[i - 1]
        fila = []
        for w in VENTANAS:
            # ultima muestra dentro de la ventana en la que NINGUN idac se
            # volvio a mover: si algo se movio, la respuesta ya no es de d.
            j = i
            while j + 1 < len(filas) and t[j + 1] - t[i - 1] <= w:
                if any(cod[m][j + 1] != cod[m][j] for m in idacs
                       if cod[m][j + 1] is not None and cod[m][j] is not None):
                    break
                j += 1
            if t[j] - t[i - 1] < w * 0.6 or y[j] is None:
                fila.append(None)
            else:
                fila.append((y[j] - base) / 1000.0)
        print('  t=%4ds %s %+d  %s -> %s' % (
            t[i - 1], n, d, '%.1f' % (base / 1000.0),
            ' '.join(('%5.1f' % v) if v is not None else '    -' for v in fila)))
        if fila[-1] is not None or fila[-2] is not None:
            ult = fila[-1] if fila[-1] is not None else fila[-2]
            resumen[n].append((d, ult))
    print('  %14s %s' % ('', ' '.join('%5ds' % w for w in VENTANAS)))
    print()
    for n in idacs:
        if not resumen[n]:
            continue
        p = [u / d for d, u in resumen[n] if d]
        print('%s: %d pasos aislados, pendiente %.2f..%.2f mV/codigo (mediana %.2f)'
              % (n, len(p), min(p), max(p), sorted(p)[len(p) // 2]))


if __name__ == '__main__':
    main(*sys.argv[1:])
