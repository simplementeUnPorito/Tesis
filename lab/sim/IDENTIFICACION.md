# Identificación de la planta con saturación por etapa

## Alcance y reproducibilidad

**SIMULADO.** `lab/sim/identificacion.py` es un ajuste *offline*: sólo lee
`lab/autoridad/*.json` y `lab/campana_techo/resultados.jsonl`. No abre un
puerto serie, no referencia COM8 y no escribe firmware. Se ejecutó con:

```text
python lab/sim/test_identificacion.py
python lab/sim/identificacion.py
```

La primera prueba pasó (1/1). Los números de abajo son la salida de la
segunda ejecución, redondeados a 0,01 mV.

## Datos, separación y modelo

**MEDIDO.** El ajuste usa las series A--B--A--B--A con el lazo congelado. Se
reservaron enteras, antes de calcular parámetros:

| Retenida (no vista por el ajuste) | Razón |
|---|---|
| `idac0_pgax16.json` | interpolación de PGA para IDAC0 |
| `paso4_idac1.json` | invariancia de IDAC1 al PGA |
| `paso6_idac2.json` | propagación de IDAC2 de PGAout x4 a x24 |

**MEDIDO.** Las trazas antiguas `descartadas/idac0_pgax16` y
`descartadas/idac0_pgax32` no existen; las antiguas disponibles continúan
fuera del ajuste de pendiente. Sus muestras sólo se usan, junto con la
campaña independiente de 72 visitas, para extremos de riel.

**DEDUCIDO — estructura identificada.** Cada camino se representa por
`y(t)=clip(yA+k·Δcode·(1-exp(-t/tau)), L-, L+)`. A la resolución de 5 s no
hay transición resoluble: los primeros puntos de cada meseta ya están en el
régimen de la meseta; por lo tanto sólo puede afirmarse `tau < 5 s` para los
caminos observables. La ganancia es la pendiente A--B--A--B--A no saturada.
Para IDAC0, SEo y BPo se ajustan como potencia de PGA; para IDAC1 no se
escala con PGA; para IDAC2 OPA_SUM no escala con PGAout y SUM/LP se propagan
por la ganancia de PGAout. IDAC3 se conserva como camino posterior a PGAout,
pero tiene una sola condición medida (x24), por lo que no tiene validación
retenida ni extrapolación a los pares del criterio.

**MEDIDO — saturadores independientes del ajuste.** Se fijaron de la
campaña cerrada, no para reducir el error retenido:

| Etapa/tap | L- mV | L+ mV |
|---|---:|---:|
| SEo | -261,2 | +121,3 |
| BPo | -221,7 | +122,7 |
| OPA_SUM | -264,0 | +112,4 |
| SUM | -258,1 | +111,2 |
| LP | -283,3 | +131,8 |

Esto respeta los rieles asimétricos. Las pendientes marcadas `saturado:true`
no entran en el cálculo de `k`; sus series sí establecen que una salida quedó
en el límite.

## Error en el conjunto retenido

**SIMULADO contra MEDIDO.** La predicción parte del valor A observado de la
propia corrida retenida (condición inicial) y pronostica B. `NI` significa
que no existe pendiente no saturada para ese camino: inventarla convertiría
un riel en una pendiente.

| Retenida | Tap | Medido B mV | Simulado B mV | Error mV |
|---|---|---:|---:|---:|
| IDAC0 x16 | SEo | -70,46 | -64,52 | +5,94 |
|  | BPo | -8,17 | -8,03 | +0,14 |
|  | OPA_SUM / SUM / LP | +112,03 / +110,71 / -263,50 | NI | NI |
| IDAC1 x50 | SEo | -12,21 | -11,79 | +0,42 |
|  | BPo | -10,91 | -11,25 | -0,35 |
|  | OPA_SUM | +2,50 | +3,65 | +1,15 |
|  | SUM | +2,45 | +3,66 | +1,21 |
|  | LP | +6,34 | NI | NI |
| IDAC2, PGAout x24 | SEo | -7,35 | -8,05 | -0,70 |
|  | BPo | -7,31 | -8,00 | -0,69 |
|  | OPA_SUM | -9,75 | -10,47 | -0,73 |
|  | SUM | -154,14 | -91,98 | +62,17 |
|  | LP | +113,52 | +131,80 (riel) | +18,28 |

**DEDUCIDO.** La estructura predice razonablemente los caminos previos a
PGAout, pero falla justamente en la transferencia PGAout/SUM a x24: el error
de 62,17 mV en SUM es mucho mayor que la ventana ADC completa (242,31 mV)
en fracción útil y fuerza LP al riel alto. No se ajustó ningún parámetro para
ocultar ese error.

## Puerta cerrada: criterio de aceptación

**DESAPROBADO.** La prueba ciega de lazo cerrado no se puede acreditar con
esta planta, por dos razones observables:

1. **SIMULADO/MEDIDO:** la validación retenida ya falla para IDAC2→SUM/LP;
   la planta no puede predecir con precisión el único camino que el arnés
   rápido usa para compensar PGAout alto.
2. **SIMULADO:** `sim_aprendizaje.py --campaign` aún decide el resultado con
   la tabla literal `baseline_ok` y con códigos IDAC3 fijos en `_case`; no
   conecta una planta a `runtime_host.c`. Su salida reproduce x4/x16 y
   x16/x16 por construcción, no por identificación, y por eso no se cuenta
   como (a), (b) ni (c). Además, su prueba de regresión actualmente falla:
   espera datos IDAC0 x50 que ya no están en el conjunto activo (`KeyError:
   (0, 50, 1)`).

Por lo tanto no se usaron los resultados cerrados para cambiar una ganancia,
un riel, una constante de tiempo ni una condición inicial. El orden general
pedido permanece **MEDIDO** en campaña, pero no está explicado
predictivamente por este ajuste.

## Medición que falta

**DEDUCIDO.** Hace falta A--B--A--B--A de IDAC2 a PGAout x16, x24 y x32,
con un escalón que no sature SUM ni LP, y muestreo suficientemente rápido
(<=0,5 s durante los primeros 30 s) para separar PGAout de la dinámica LP.
También hace falta IDAC3 en esos pares para identificar su margen real. Esa
medición identifica la transferencia que produjo el error retenido; no es
una medición de x16/x16 para forzar un veredicto.

## Variante OPA_SUM

No evaluada: la condición «si y sólo si pasa» no se cumplió. Declarar una
mejora de x16/x16 con el modelo actual sería usar una salida cerrada
codificada y no una predicción; tampoco puede verificarse que IDAC3 quede
lejos del riel.

Recomendación: **no cambiar el aprendizaje; medir IDAC2→SUM/LP e IDAC3 por PGAout antes de volver a evaluar OPA_SUM.**
