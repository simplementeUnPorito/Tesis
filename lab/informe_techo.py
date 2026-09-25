"""informe_techo.py - que ganancias sirven, y por que las otras no.

Lee `resultados.jsonl` de una campana y contesta, en el orden de prioridad
acordado, las cuatro preguntas del proyecto:

  1. COBERTURA        que pares quedan estables.
  2. REPRODUCIBILIDAD de los que pasan, cuales pasan en TODAS sus condiciones.
     Un par que pasa una vez de tres no es estable, es afortunado.
  3. VELOCIDAD        cuanto tardan, separado por origen del punto inicial.
  4. MARGEN           cuanto rango libre les queda: en banda con el actuador
     contra el tope es un PASA que la primera deriva termica se lleva puesto.

Y dos cruces que solo esta campana puede dar:

  * GANANCIA TOTAL vs REPARTO: el cuarteto x4/x16, x8/x8, x2/x32 y x32/x2 son
    los cuatro ganancia 64 por caminos distintos.  Si los cuatro se comportan
    igual, lo que manda es la ganancia; si no, manda el reparto, y entonces
    "el techo" no es un numero sino una region.
  * MEMORIA vs CONTROL: el mismo par con la politica de puntos encendida y
    apagada.  Es la unica forma de saber si sembrar sirve o si el par venia
    encaminado igual.

No abre el puerto: se puede correr mientras la campana mide.
"""
import argparse
import collections
import json
import os


def cargar(salida):
    f = os.path.join(salida, 'resultados.jsonl')
    if not os.path.exists(f):
        return []
    with open(f, encoding='utf-8') as fh:
        return [json.loads(l) for l in fh if l.strip()]


def _par(r):
    return '%s/%s' % (r.get('pga'), r.get('pgaout'))


def _paso(r):
    """Aprobado por el criterio ESTRICTO: quieto y con rango libre."""
    return r.get('nota') is not None and not r.get('fragil')


def _mediana(xs):
    xs = sorted(x for x in xs if x is not None)
    return xs[len(xs) // 2] if xs else None


def cobertura(rs):
    print('=' * 72)
    print('1. COBERTURA  -  que pares quedan estables')
    print('=' * 72)
    print('%-10s %6s %5s %5s %6s %6s  %-6s %s'
          % ('par', 'gan', 'vis', 'pasa', 'nota', 'IDAC3', 'fragil', 'veredictos'))
    por = collections.defaultdict(list)
    for r in rs:
        por[(r.get('ganancia') or 0, _par(r))].append(r)
    buenos = []
    for (gan, par), v in sorted(por.items()):
        pasan = [r for r in v if _paso(r)]
        notas = [r.get('nota') for r in v if r.get('nota')]
        i3 = [abs(r['idac_final'][3]) for r in v
              if r.get('idac_final') and r['idac_final'][3] is not None]
        fr = sum(1 for r in v if r.get('fragil'))
        ver = collections.Counter(r.get('veredicto') for r in v)
        print('x%-9s %6d %5d %5d %6s %6s  %-6s %s'
              % (par, gan, len(v), len(pasan),
                 min(notas) if notas else '-',
                 max(i3) if i3 else '-',
                 '%d/%d' % (fr, len(v)),
                 dict(ver)))
        if pasan:
            buenos.append((gan, par, len(pasan), len(v)))
    print()
    if buenos:
        techo = max(g for g, _, _, _ in buenos)
        print('GANANCIA MAS ALTA CON AL MENOS UN PASE ESTRICTO: %d  (%s)'
              % (techo, ', '.join('x%s' % p for g, p, _, _ in buenos if g == techo)))
        solidos = [(g, p) for g, p, n, t in buenos if n == t and t >= 2]
        if solidos:
            print('GANANCIA MAS ALTA QUE PASA EN TODAS SUS CONDICIONES: %d  (%s)'
                  % (max(g for g, _ in solidos),
                     ', '.join('x%s' % p for g, p in solidos
                               if g == max(gg for gg, _ in solidos))))
        else:
            print('NINGUN par paso todas sus condiciones: no hay techo REPRODUCIBLE')
    else:
        print('ningun par paso el criterio estricto todavia')
    print()


def reproducibilidad(rs):
    print('=' * 72)
    print('2. REPRODUCIBILIDAD  -  pasa siempre, o pasa a veces')
    print('=' * 72)
    por = collections.defaultdict(dict)
    for r in rs:
        por[(r.get('ganancia') or 0, _par(r))][(r.get('vuelta'),
                                                r.get('condicion'),
                                                r.get('brazo'))] = r
    print('%-10s %6s %26s %s' % ('par', 'gan', 'pasa/total', 'donde falla'))
    for (gan, par), v in sorted(por.items()):
        ok = [k for k, r in v.items() if _paso(r)]
        mal = [k for k, r in v.items() if not _paso(r)]
        print('x%-9s %6d %26s %s'
              % (par, gan, '%d/%d' % (len(ok), len(v)),
                 ', '.join('v%s %s %s' % k for k in sorted(mal, key=str)[:3])
                 or '-'))
    print()


def velocidad(rs):
    print('=' * 72)
    print('3. VELOCIDAD  -  cuanto tarda, segun de donde salio el punto inicial')
    print('=' * 72)
    por = collections.defaultdict(list)
    for r in rs:
        if r.get('t_estable_s') is not None:
            por[r.get('origen') or 'sin dato'].append(r['t_estable_s'])
    print('%-16s %5s %9s %9s %9s' % ('origen', 'n', 'mediana', 'min', 'max'))
    for o, xs in sorted(por.items(), key=lambda kv: -len(kv[1])):
        print('%-16s %5d %8.1fs %8.1fs %8.1fs'
              % (o, len(xs), _mediana(xs), min(xs), max(xs)))
    print()
    print('Residuo de correccion (codigos finales menos los sembrados).  Es la')
    print('medida de que tan bueno es el modelo: si tiende a cero, la semilla')
    print('ya cae donde el lazo la iba a dejar.')
    res = [r['residuo'] for r in rs if r.get('residuo')]
    if res:
        for j, nombre in enumerate(('IDAC0', 'IDAC1', 'IDAC2', 'IDAC3')):
            xs = [x[j] for x in res if x[j] is not None]
            if xs:
                print('  %-6s n=%-4d mediana=%+5s  peor=%+d'
                      % (nombre, len(xs), _mediana(xs),
                         max(xs, key=abs)))
    else:
        print('  (todavia sin ninguna visita con semilla aplicada)')
    print()


def memoria_vs_control(rs):
    print('=' * 72)
    print('4. MEMORIA vs CONTROL  -  sembrar, sirve?')
    print('=' * 72)
    por = collections.defaultdict(dict)
    for r in rs:
        por[(r.get('vuelta'), _par(r), r.get('condicion'))][r.get('brazo')] = r
    filas = []
    for k, v in sorted(por.items(), key=str):
        m, c = v.get('MEMORIA'), v.get('CONTROL')
        if not m or not c:
            continue
        filas.append((k, m, c))
    if not filas:
        print('todavia no hay ningun par con los dos brazos medidos')
        print()
        return
    print('%-22s %-10s %-10s %-9s %-9s' % ('par / condicion', 'MEM', 'CTRL',
                                           't_MEM', 't_CTRL'))
    gana = pierde = empata = 0
    for (vu, par, cond), m, c in filas:
        tm, tc = m.get('t_estable_s'), c.get('t_estable_s')
        if tm is not None and tc is not None:
            if tm < tc * 0.8:
                gana += 1
            elif tc < tm * 0.8:
                pierde += 1
            else:
                empata += 1
        print('v%s x%-14s %-10s %-10s %-9s %-9s'
              % (vu, '%s %s' % (par, cond),
                 '%s%s' % (m.get('nota') or '-', '*' if m.get('fragil') else ''),
                 '%s%s' % (c.get('nota') or '-', '*' if c.get('fragil') else ''),
                 tm if tm is not None else '-', tc if tc is not None else '-'))
    print()
    print('la memoria gana en %d, pierde en %d, empata en %d (umbral 20 %%)'
          % (gana, pierde, empata))
    print('* = fragil (|IDAC3| > 200: en banda pero sin rango para derivar)')
    print()


def cuarteto(rs):
    """Los cuatro caminos a ganancia 64.  Manda la ganancia o el reparto?"""
    los64 = [r for r in rs if r.get('ganancia') == 64]
    if not los64:
        return
    print('=' * 72)
    print('5. GANANCIA TOTAL vs REPARTO  -  los cuatro caminos a 64')
    print('=' * 72)
    por = collections.defaultdict(list)
    for r in los64:
        por[_par(r)].append(r)
    print('%-10s %5s %5s %8s %8s %8s'
          % ('par', 'vis', 'pasa', 'mediana', 'LPo_mV', 'IDAC3'))
    for par, v in sorted(por.items()):
        pasan = [r for r in v if _paso(r)]
        t = _mediana([r.get('t_estable_s') for r in v])
        lp = _mediana([abs(r['LPo_final_mV']) for r in v
                       if r.get('LPo_final_mV') is not None])
        i3 = _mediana([abs(r['idac_final'][3]) for r in v
                       if r.get('idac_final') and r['idac_final'][3] is not None])
        print('x%-9s %5d %5d %8s %8s %8s'
              % (par, len(v), len(pasan),
                 '%.0fs' % t if t is not None else '-',
                 '%.1f' % lp if lp is not None else '-',
                 i3 if i3 is not None else '-'))
    print()
    print('Si los cuatro se parecen, lo que manda es la GANANCIA TOTAL y el')
    print('techo es un numero.  Si no, manda el REPARTO entre PGA y PGAout, y')
    print('entonces hay pares de ganancia alta usables que un barrido por')
    print('ganancia total nunca encuentra.')
    print()


def temperatura(rs, salida):
    t = [r.get('temp_ambiente_C') for r in rs if r.get('temp_ambiente_C')]
    csv = os.path.join(salida, 'temperatura.csv')
    n = (sum(1 for _ in open(csv, encoding='utf-8')) - 1
         if os.path.exists(csv) else 0)
    print('=' * 72)
    print('6. TEMPERATURA')
    print('=' * 72)
    print('filas registradas durante la campana: %d' % n)
    if t:
        print('anotada en las visitas: %.1f a %.1f C (rango %.1f)'
              % (min(t), max(t), max(t) - min(t)))
        print('OJO: es temperatura del AIRE, no de la juntura.  Sirve para ver')
        print('si la deriva acompana al ambiente, no como valor absoluto.')
    else:
        print('las visitas todavia no estan anotadas; correr:')
        print('  python lab/temperatura_ambiente.py --anotar %s'
              % os.path.join(salida, 'resultados.jsonl'))
    print()


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('salida')
    a = ap.parse_args()
    rs = cargar(a.salida)
    if not rs:
        print('sin visitas todavia en %s' % a.salida)
        return 1
    med = [r for r in rs if r.get('veredicto') != 'INMEDIBLE']
    print()
    print('%d visitas (%d medibles, %d inmedibles), %d pares'
          % (len(rs), len(med), len(rs) - len(med),
             len(set(_par(r) for r in rs))))
    print()
    cobertura(rs)
    reproducibilidad(rs)
    velocidad(rs)
    memoria_vs_control(rs)
    cuarteto(rs)
    temperatura(rs, a.salida)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
