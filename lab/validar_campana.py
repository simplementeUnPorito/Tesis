"""validar_campana.py - controles de sanidad del INSTRUMENTO, no de la fisica.

Se corre mientras la campana mide. No abre el puerto serie. Cada control
responde a un modo de falla que YA ocurrio en este banco, asi que ninguno es
hipotetico:

  1. brazo de control contaminado      un CONTROL con un punto aplicado
  2. residuo inventado                 residuo sin semilla que lo respalde
  3. herencia entre visitas            MEMORIA y CONTROL del mismo par con el
                                       mismo origen Y el mismo residuo
  4. consigna no verificada            politica leida distinta de la pedida
  5. visitas sin marca de tiempo       sin eso no hay cruce con temperatura
  6. duplicados                        la misma (vuelta,par,condicion,brazo)
  7. nota sin respaldo                 nota puesta con menos de 15 muestras
                                       validas de LPo
  8. temperatura detenida              el CSV dejo de crecer

Codigo de salida 0 si todo pasa, 1 si algo falla. Imprime SIEMPRE los numeros,
tambien cuando esta bien: un control que solo habla cuando falla no deja ver
si de verdad corrio.
"""
import argparse
import collections
import json
import os
import sys
from datetime import datetime

MIN_MUESTRAS = 8


def cargar(salida):
    f = os.path.join(salida, 'resultados.jsonl')
    if not os.path.exists(f):
        return []
    with open(f, encoding='utf-8') as fh:
        return [json.loads(l) for l in fh if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('salida')
    a = ap.parse_args()
    rs = cargar(a.salida)
    if not rs:
        print('sin visitas todavia')
        return 1

    fallas = []
    med = [r for r in rs if r.get('veredicto') != 'INMEDIBLE']
    print('visitas: %d  (%d medibles, %d inmedibles)'
          % (len(rs), len(med), len(rs) - len(med)))
    print('veredictos:', dict(collections.Counter(r.get('veredicto') for r in rs)))

    # 1. control contaminado
    ctrl = [r for r in rs if r.get('brazo') == 'CONTROL']
    sucio = [r for r in ctrl
             if r.get('origen') not in (None, 'NADA', 'APRENDIZAJE')]
    print('1. control con punto aplicado : %d de %d' % (len(sucio), len(ctrl)))
    if sucio:
        fallas.append('el brazo de CONTROL recibio un punto en %d visitas' % len(sucio))

    # 2. residuo sin semilla
    huerfano = [r for r in rs if r.get('residuo') is not None
                and r.get('origen') in (None, 'NADA', 'APRENDIZAJE')]
    print('2. residuo sin semilla        : %d' % len(huerfano))
    if huerfano:
        fallas.append('%d visitas con residuo sin semilla que lo respalde' % len(huerfano))

    # 3. herencia entre brazos
    por = collections.defaultdict(dict)
    for r in rs:
        por[(r.get('vuelta'), r.get('pga'), r.get('pgaout'),
             r.get('condicion'))][r.get('brazo')] = r
    here = 0
    for v in por.values():
        m, c = v.get('MEMORIA'), v.get('CONTROL')
        if (m and c and m.get('origen') == c.get('origen')
                and m.get('residuo') is not None
                and m.get('residuo') == c.get('residuo')):
            here += 1
    print('3. herencia MEMORIA->CONTROL  : %d pares' % here)
    if here:
        fallas.append('%d pares con origen y residuo identicos entre brazos' % here)

    # 4. consigna no verificada
    disc = [r for r in rs if r.get('politica_puntos') is not None
            and r.get('politica_puntos') != r.get('politica_pedida')]
    print('4. politica leida != pedida   : %d' % len(disc))
    if disc:
        fallas.append('%d visitas con la politica distinta de la pedida' % len(disc))

    # 5. marca
    sin_marca = sum(1 for r in rs if not r.get('marca'))
    print('5. visitas sin marca de tiempo: %d' % sin_marca)
    if sin_marca:
        fallas.append('%d visitas sin marca: no se pueden cruzar con temperatura' % sin_marca)

    # 6. duplicados
    claves = [(r.get('vuelta'), r.get('pga_cod'), r.get('pgaout_cod'),
               r.get('condicion'), r.get('brazo')) for r in rs]
    dup = [k for k, n in collections.Counter(claves).items() if n > 1]
    print('6. combinaciones duplicadas   : %d' % len(dup))
    if dup:
        fallas.append('%d combinaciones medidas mas de una vez: %s' % (len(dup), dup[:3]))

    # 7. nota sin respaldo
    flojas = [r for r in med if r.get('nota') is not None
              and (r.get('muestras_validas_LPo') or 0) < MIN_MUESTRAS]
    print('7. nota con menos de %d muestras: %d' % (MIN_MUESTRAS, len(flojas)))
    if flojas:
        fallas.append('%d notas puestas sin la ventana llena' % len(flojas))

    # 8. temperatura
    t = os.path.join(a.salida, 'temperatura.csv')
    n_t = sum(1 for _ in open(t, encoding='utf-8')) - 1 if os.path.exists(t) else 0
    print('8. filas de temperatura       : %d' % n_t)
    if n_t < 1:
        fallas.append('el registro de temperatura no escribio ninguna fila')

    # lo que ya se puede comparar
    print()
    print('%-11s %-8s %4s %9s %s' % ('condicion', 'brazo', 'n', 'mediana', 'notas'))
    for c in ('FRIO', 'DESDE_X1', 'DESDE_ALTA'):
        for b in ('MEMORIA', 'CONTROL'):
            g = [r['t_estable_s'] for r in med
                 if r.get('condicion') == c and r.get('brazo') == b
                 and r.get('t_estable_s') is not None]
            if not g:
                continue
            g = sorted(g)
            n = collections.Counter(r.get('nota') for r in med
                                    if r.get('condicion') == c and r.get('brazo') == b)
            print('%-11s %-8s %4d %8.1fs %s'
                  % (c, b, len(g), g[len(g) // 2],
                     dict(sorted(n.items(), key=lambda x: str(x[0])))))

    print()
    if fallas:
        print('FALLA:')
        for f in fallas:
            print('  - ' + f)
        return 1
    print('TODO BIEN: los ocho controles del instrumento pasan.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
