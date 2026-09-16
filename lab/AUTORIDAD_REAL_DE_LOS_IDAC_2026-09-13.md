# La autoridad real de los cuatro IDAC, y de dónde sale el techo de ganancia

Fecha: 2026-09-13. Reemplaza a todo lo que se dijo antes sobre la autoridad de
IDAC3, incluido el informe del 2026-09-12 por la tarde, que estaba mal.

## Los números vienen del firmware, no de una medición mía

Las resistencias de conversión corriente-tensión están declaradas en
`psoc_hw.h`, y el rango de cada IDAC en `calibration.c`. No hacía falta medirlas.

| etapa | referencia | R | rango | por código | excursión total |
|---|---|---|---|---|---|
| 0 | Vref_PGA | 15 kΩ | 32 µA | 0,125 µA | 478 mV |
| 1 | Vref_BP | 15 kΩ | 32 µA | 0,125 µA | 478 mV |
| 2 | Vref_ADDER | 1,5 kΩ | **255 µA** | 1 µA | 382 mV |
| 3 | Vref_LP | 10 kΩ | 32 µA | 0,125 µA | 319 mV |

La etapa 2 es la única en el rango de 255 µA. Eso explica por qué su paso sobre
el sumador es de unos 12 mV cuando el de las otras es de 2 a 3: no es que tenga
una resistencia grande, es que tiene ocho veces más corriente por código.

## La hipótesis del compliance queda descartada, con números

El datasheet del IDAC8 pide 1,0 V de headroom: la salida no puede pasar de
VDDA − 1,0 V drenando ni bajar de VSSA + 1,0 V entregando. Con VDDA = 4,826 V y
los nodos de referencia en VDDA/2 = 2,413 V, la ventana permitida es
**2,413 ± 1,413 V**.

La excursión más grande que puede pedir cualquiera de los cuatro actuadores son
los 478 mV de las etapas 0 y 1. Sobra un factor de tres. **Ningún IDAC de esta
placa sale de compliance en ningún código**, así que no es esa la causa de que
IDAC3 no mueva LPo.

## La autoridad de IDAC3, medida hoy con LPo dentro de la ventana

Ésta es la medición que faltaba desde el principio, y la que corrige a todas las
anteriores. Se hizo con PGA en x1 y PGAout en x1, que es donde la cadena entra
más cómoda, y **sólo después de comprobar que LPo estaba dentro de la ventana**,
que es la condición que ninguna medición previa había cumplido. El barrido es
ABBA de cuatro bloques para que la deriva no se confunda con la respuesta.

| bloque | mV por código |
|---|---|
| 0 | 6,33 |
| 1 | 6,71 |
| 2 | 6,82 |
| 3 | 6,88 |
| **medio** | **6,68** |

El modelo predice 7,53 mV por código: 0,125 µA por código sobre 10 kΩ, por la
ganancia de 6 del pasabajos desde su pin positivo. Lo medido es el 89 % de eso,
que para una cadena con tolerancias de resistencia y un ±3,5 % de error de
ganancia del propio IDAC es un acuerdo bueno.

**La autoridad total de IDAC3 son ±1,70 V sobre LPo**, y no depende de la
ganancia de PGAout porque entra después de ella. Es un actuador de recorrido
completo, no un trim.

## Por qué la curva que guarda el firmware da once veces menos

`calibration.c` guarda una curva de dieciséis puntos de Vref_LP contra el tap
del pasabajos, medida en la placa el 2026-09-03, en cuentas del ADC. Convertida
a milivolts con los 19,9157 µV por cuenta:

| código IDAC3 | LPo |
|---|---|
| −255 | −266 mV |
| −128 | −115 mV |
| 0 | 0 |
| +128 | +71 mV |
| +255 | +127 mV |

Cerca de cero da **0,58 mV por código** y una excursión completa de **393 mV**,
marcadamente asimétrica. Eso es once veces menos que lo medido hoy, y la
diferencia no está en la resistencia: el cambio de 6,68 kΩ a 10 kΩ explicaría
un factor 1,5, no un factor 11.

Lo que la explica es la condición en que se tomó cada una. La curva del
firmware se levantó con LPo contra su riel, donde la etapa comprime y cualquier
actuador parece débil. El propio comentario que la acompaña dice que la
pendiente cambia por un factor 2,6 entre una mitad y la otra, que es la firma de
una saturación, no de un actuador no lineal.

**Consecuencia para el firmware:** `g_cal_geo_lp_delta_counts` en
`calibration.c` subestima la autoridad de IDAC3 en un orden de magnitud, y el PI
que la usa para calcular su ganancia de cuerda va a pedir movimientos diez veces
más grandes de los necesarios. Hay que volver a levantar esa curva con la etapa
dentro de la ventana antes de confiar en la calibración de a bordo.

## El techo de ganancia: la resolución ya no es el cuello de botella

La bisección de IDAC2 deja a LPo, en el peor caso, a medio paso de IDAC2 del
cero. Ese paso, visto en LPo, vale 12 mV × 9,07 × G/4. Para que IDAC3 pueda
taparlo, sus 1.704 mV de recorrido tienen que alcanzar:

| PGAout | paso de IDAC2 en LPo | ¿lo tapa IDAC3? |
|---|---|---|
| x1 | 27 mV | sí |
| x4 | 109 mV | sí |
| x8 | 219 mV | sí |
| x16 | 437 mV | sí |
| x24 | 656 mV | sí |
| x32 | 874 mV | sí |
| x50 | 1.367 mV | sí, con poco margen |

Con la resistencia de 10 kΩ puesta, **la resolución deja de ser el límite en
todo el rango de ganancias**. El límite que quede tiene que venir de otro lado:
de que la cadena aguas arriba se clave antes, no de que falte fineza. Eso es lo
que mide la escalera de ganancias, y es una pregunta empírica.

Esto también anula la recomendación de cambiar la resistencia a 33 kΩ que
figuraba en la primera versión de este documento: los 10 kΩ que ya están puestos
alcanzan.
