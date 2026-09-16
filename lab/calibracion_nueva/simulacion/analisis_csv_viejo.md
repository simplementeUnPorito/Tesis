# Resultados del mapa parcial del sumador — 2026-09-10

Fuente: `C:/Github/Tesis/lab/calibracion_nueva/mapear_alcance_sumador_20260910_122631.csv`. Las filas CSV citadas cuentan el encabezado como fila 1. Los valores eléctricos de los ajustes son desviaciones físicas respecto de Vref, tomadas de `real_mv_vs_vref`; los límites y la detección de clavado provienen de `escala_banco.py`.

## 1. Qué se corrió y hasta dónde

| Magnitud | Resultado |
| --- | --- |
| Configuración | PGA x50; PGAout x1; ADC ±2,5 V; IDAC0=+19; IDAC3=0 |
| Filas de canal | 345 |
| Capturas completas de cinco canales | 69 de 69 registradas |
| Celdas de malla gruesa | 35 de 126 planeadas (27,8 %) |
| Bloques IDAC1 completos | 5 de 18 |
| Capturas adicionales | 5 de referencia y 29 del tramo fino |
| Pasadas con filas | 1 |
| Tiempo hasta la última fila | t_s=998,919 s (16 min 38,9 s) |
| Intervalo cubierto por filas | 788,927 s (13 min 8,9 s) |

La corrida fue cortada a propósito y no es una campaña completa. La última fila persistida es la 346: pasada 1, IDAC1=+0, IDAC2=+255, fase `fino`, ch4, t_s=998,919 s.
El JSON adyacente quedó con `estado=malla` y `resumen=None`; esto sólo se usa para describir el corte.

## 2. Mapa de validez

Leyenda por canal: **V** = válido y vivo; **C** = válido pero clavado; **F** = fuera de rango; **F\*** = fuera de rango y además clavado; **—** = celda no medida. Cada celda se escribe como `2estado/3estado/4estado`.

**Pasada 1.**
| IDAC1 \ IDAC2 | -255 | -128 | -64 | +0 | +64 | +128 | +255 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -255 | 2V/3V/4C | 2V/3V/4C | 2V/3V/4V | 2V/3V/4V | 2V/3V/4F | 2V/3V/4F* | 2V/3V/4F* |
| -192 | 2V/3V/4C | 2V/3V/4C | 2V/3V/4V | 2V/3V/4V | 2V/3V/4F | 2V/3V/4F* | 2V/3V/4F* |
| -128 | 2F/3F/4C | 2V/3V/4C | 2V/3V/4V | 2V/3V/4V | 2V/3V/4V | 2V/3V/4F* | 2V/3V/4F* |
| -64 | 2F/3F/4C | 2F/3F/4C | 2V/3V/4C | 2V/3V/4V | 2V/3V/4V | 2V/3V/4F | 2V/3V/4F* |
| +0 | 2F/3F/4C | 2F/3F/4C | 2F/3F/4C | 2V/3V/4C | 2V/3V/4V | 2V/3V/4V | 2V/3V/4F* |
| +64 | — | — | — | — | — | — | — |
| +128 | — | — | — | — | — | — | — |
| +192 | — | — | — | — | — | — | — |
| +255 | — | — | — | — | — | — | — |

**Pasada 2:** no hay filas de malla en el CSV.

## 3. La diagonal de soluciones

Se buscó, por pasada e IDAC1, el menor `abs(real_mv_vs_vref)` de ch4 entre capturas `malla` y `fino` donde ch4 es válido y no está clavado. No se incluyó la captura `referencia`.
| Pasada | IDAC1 | IDAC2 óptimo | Fase | Error ch4 (mV) | Error ch2 (mV) | Filas CSV ch4/ch2 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | -255 | -56 | fino | +172,3 | -13,9 | 76/74 |
| 1 | -192 | -8 | fino | -92,1 | -257,7 | 121/119 |
| 1 | -128 | +0 | malla | +26,4 | -556,7 | 176/174 |
| 1 | -64 | +64 | malla | -623,9 | -686,6 | 256/254 |
| 1 | +0 | +64 | malla | +683,2 | -1249,6 | 316/314 |

Ajuste lineal de los códigos óptimos:

| Pasada | N | Pendiente ΔIDAC2/ΔIDAC1 | Ordenada (códigos) | RMS (códigos) | R² |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | +0,4889 | +75,28 | 13,00 | 0,9201 |

Pasada 1: no cumple el criterio descriptivo R² ≥ 0,95; la pendiente observada es +0,4889 códigos de IDAC2 por código de IDAC1.
El umbral R² ≥ 0,95 es sólo un criterio descriptivo del conjunto observado; no prueba la relación fuera del sector medido.

## 4. Pendientes locales

| Pasada | IDAC1 | ch2 mV/código | Signo ch2 | RMS ch2 (mV); N | Filas ch2 | ch4 mV/código | Signo ch4 | RMS ch4 (mV); N | Filas ch4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | -255 | +6,805 | positivo | 2,21; N=7 | 44, 49, 54, 59, 64, 69, 74 | -63,483 | negativo | 23,87; N=7 | 46, 51, 56, 61, 66, 71, 76 |
| 1 | -192 | +6,390 | positivo | 2,90; N=7 | 119, 124, 129, 134, 139, 144, 149 | -56,477 | negativo | 20,67; N=7 | 121, 126, 131, 136, 141, 146, 151 |
| 1 | -128 | +1,555 | positivo | 5,75; N=7 | 194, 199, 204, 209, 214, 219, 224 | no se puede | — | 0 | — |
| 1 | -64 | -5,069 | negativo | 11,51; N=4 | 269, 274, 279, 284 | no se puede | — | 0 | — |
| 1 | +0 | -7,412 | negativo | 8,17; N=4 | 329, 334, 339, 344 | no se puede | — | 0 | — |

`no se puede` significa que quedaron menos de dos lecturas vivas del canal en ese tramo; las filas fuera de rango o clavadas no entraron en la recta.

Pendiente de BPo (ch1) contra IDAC1 en la malla:

| Pasada | Pendiente ch1 (mV/código) | RMS (mV) | N | Filas CSV |
| --- | --- | --- | --- | --- |
| 1 | +1,9834 | 15,34 | 35 | 8, 13, 18, 23, 28, 33, 38, 83, 88, 93, 98, 103, 108, 113, 158, 163, 168, 173, 178, 183, 188, 233, 238, 243, 248, 253, 258, 263, 293, 298, 303, 308, 313, 318, 323 |
El módulo de esta pendiente es el cambio de headroom de BPo por código de IDAC1; el signo indica hacia qué lado se desplaza.

## 5. Ajuste del modelo

Se ajustó `salida = A·IDAC2 + B·IDAC1 + C·ch0 + K`. El ajuste principal usa todas las fases registradas; se muestra además la malla gruesa sola para que la concentración de puntos finos no oculte el resultado del muestreo espaciado. La salida y ch0 están en mV físicos respecto de Vref. Para cada salida se exigió que esa salida y ch0 fueran válidos y vivos.
| Datos | Salida | N | A (mV/cód. IDAC2) | B (mV/cód. IDAC1) | C (mV/mV ch0) | K (mV) | RMS (mV) | A−9,56 | Filas de salida |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todas | ch2 | 63 | +5,1081 | -7,7852 | +3,8997 | -1588,8 | 103,11 | -4,4519 | 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 94, 99, 104, 109, 114, 119, 124, 129, 134, 139, 144, 149, 154, 164, 169, 174, 179, 184, 189, 194, 199, 204, 209, 214, 219, 224, 229, 244, 249, 254, 259, 264, 269, 274, 279, 284, 289, 309, 314, 319, 324, 329, 334, 339, 344 |
| todas | ch4 | 29 | -26,1743 | +11,3527 | +2,7291 | +1854,7 | 319,51 | -35,7343 | 6, 21, 26, 46, 51, 56, 61, 66, 71, 76, 81, 96, 101, 121, 126, 131, 136, 141, 146, 151, 156, 171, 176, 181, 231, 251, 256, 316, 321 |
| malla | ch2 | 29 | +4,8108 | -7,6844 | +7,7960 | -1460,9 | 129,55 | -4,7492 | 9, 14, 19, 24, 29, 34, 39, 84, 89, 94, 99, 104, 109, 114, 164, 169, 174, 179, 184, 189, 244, 249, 254, 259, 264, 309, 314, 319, 324 |
| malla | ch4 | 11 | -24,6255 | +11,7814 | -0,8004 | +1800,0 | 424,12 | -34,1855 | 21, 26, 96, 101, 171, 176, 181, 251, 256, 316, 321 |

En el ajuste principal de ch2, A cambia -4,4519 mV/código respecto de +9,56 mV/código. El RMS previo era 15,0 mV.
El residuo de ch2, 103,11 mV RMS, supera 15,0 mV. Es grande respecto del ajuste previo y señala que falta al menos un término o que la relación no es constante en el dominio observado.
El residuo de ch4, 319,51 mV RMS, supera 15,0 mV. Es grande respecto del ajuste previo y señala que falta al menos un término o que la relación no es constante en el dominio observado.

## 6. Ganancia de la etapa LP

La ganancia se estimó dentro de cada tramo fino, usando sólo pares ch2/ch4 vivos. El centrado por pasada/IDAC1 permite una ordenada distinta para cada tramo y evita confundir cambios de nivel entre bloques con la derivada local de la etapa.

Ganancias por tramo:

| Pasada | IDAC1 | N | Ganancia ch4/ch2 (mV/mV) | RMS ch4 (mV) | R² | Filas CSV ch2 | Filas CSV ch4 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | -255 | 7 | -9,3148 | 20,77 | 0,9956 | 44, 49, 54, 59, 64, 69, 74 | 46, 51, 56, 61, 66, 71, 76 |
| 1 | -192 | 7 | -8,7932 | 23,52 | 0,9928 | 119, 124, 129, 134, 139, 144, 149 | 121, 126, 131, 136, 141, 146, 151 |

Pendiente común con ordenada absorbida por tramo:

| Tramos | N | Ganancia ch4/ch2 (mV/mV) | RMS ch4 (mV) | R² dentro de tramos | Filas CSV ch2 | Filas CSV ch4 |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | 14 | -9,0699 | 23,74 | 0,9935 | 44, 49, 54, 59, 64, 69, 74, 119, 124, 129, 134, 139, 144, 149 | 46, 51, 56, 61, 66, 71, 76, 121, 126, 131, 136, 141, 146, 151 |

Localmente, cada +1 mV de ch2 corresponde a -9,0699 mV de ch4. Esto hace que el paso de IDAC2 llegue multiplicado en módulo a ch4. IDAC3 permaneció en cero, por lo que este archivo no contiene su pendiente: con este mapa solo no se puede decidir cuantitativamente si el trim final debe usar IDAC2 o IDAC3.

## 7. Límites físicos observados

Los extremos siguientes son lecturas de banco. `pp` también está en unidades del banco. Una lectura bajo 880,4 mV se conserva como evidencia de fuera de rango, no como tensión física.
| Canal | Mínimo (mV) | pp mín. (mV) | Estado | Fila/clave del mínimo | Máximo (mV) | pp máx. (mV) | Estado | Fila/clave del máximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ch0 PGAgain (SEo) | 999,259 | 2,593 | V | 82 (P1, malla, c1=-192, c2=-255) | 1001,987 | 4,310 | V | 342 (P1, fino, c1=+0, c2=+255) |
| ch1 BPo | 957,832 | 32,806 | V | 3 (P1, referencia, c1=-255, c2=+0) | 986,347 | 4,463 | V | 338 (P1, fino, c1=+0, c2=+253) |
| ch2 OPA_SUMo | 735,034 | 3,967 | F | 294 (P1, malla, c1=+0, c2=-255) | 1079,273 | 1,525 | V | 39 (P1, malla, c1=-255, c2=+255) |
| ch3 SUMo | 738,964 | 2,765 | F | 295 (P1, malla, c1=+0, c2=-255) | 1078,529 | 1,888 | V | 40 (P1, malla, c1=-255, c2=+255) |
| ch4 LPo | 731,830 | 0,286 | F* | 211 (P1, fino, c1=-128, c2=+128) | 1106,643 | 0,209 | C | 11 (P1, malla, c1=-255, c2=-255) |

Lecturas clavadas repetidas (`pp_banco_uv < 300`):

| Canal | Lado | N | Mínimo (mV) | Mediana (mV) | Máximo (mV) | Rango pp (mV) | Filas CSV |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ch4 LPo | bajo | 19 | 731,830 | 731,868 | 732,097 | 0,133–0,286 | 36, 41, 111, 116, 186, 191, 206, 211, 216, 221, 226, 266, 276, 281, 326, 331, 336, 341, 346 |
| ch4 LPo | alto | 14 | 1106,472 | 1106,491 | 1106,643 | 0,095–0,267 | 11, 16, 86, 91, 161, 166, 236, 241, 246, 291, 296, 301, 306, 311 |

El riel alto repetido aparece en ch4: N=14, mediana 1106,491 mV de banco. Está 16,209 mV de banco por debajo de `BANCO_MAX_VALIDO_MV`=1122,7 mV; por eso una lectura puede estar dentro de la ventana y, a la vez, clavada al riel de la etapa.

## 8. Qué queda sin contestar

- La segunda pasada no corrió: no hay pares ida/vuelta y no existe dato de histéresis. No se infiere histéresis ni ausencia de histéresis.

- La malla gruesa tiene 35 de 126 celdas. Los IDAC1 sin sus siete celdas no permiten extender las pendientes ni la diagonal fuera del sector observado.

- No se pudo obtener pendiente fina de ch4 en: P1/IDAC1=-128, P1/IDAC1=-64, P1/IDAC1=+0. En esos casos faltan al menos dos puntos válidos y vivos.

- IDAC3 quedó fijo en cero. Falta medir `ch4/IDAC3` con ch4 vivo para comparar autoridad y resolución con la ruta `IDAC2 → ch2 → ch4`; por eso no se asigna el trim final con este archivo.

- Los tramos finos se centraron alrededor del mejor ch2, no del mejor ch4. La diagonal de ch4 sólo identifica el mejor código entre los códigos efectivamente muestreados.

- El residuo del modelo de ch2 supera el del ajuste previo. Estos datos no identifican por sí solos cuál es el término faltante; hace falta otra variable o un modelo por regiones.

## Criterios de cálculo

- Conversión de diferencias: 1 mV de banco = 19,9157 mV físicos.

- Ventana válida: 880,4 a 1122,7 mV de banco; objetivo: 1001,5 mV de banco.

- Vivo = `ok=True`, `valido=True` y `clavado=False` en la misma fila.

- Las dispersiones informadas son RMS de los residuos respecto de la recta ajustada. Los mínimos cuadrados se resolvieron con ecuaciones normales, centrado y escalado de predictores, y eliminación gaussiana con pivoteo parcial; no se usaron NumPy ni pandas.
