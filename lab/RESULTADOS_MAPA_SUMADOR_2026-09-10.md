# Resultados del mapa parcial del sumador — 2026-09-10

Fuente: `C:/Github/Tesis/lab/calibracion_nueva/mapear_alcance_sumador_20260910_133605.csv`. Las filas CSV citadas cuentan el encabezado como fila 1. Los valores eléctricos de los ajustes son desviaciones físicas respecto de Vref, tomadas de `real_mv_vs_vref`; los límites y la detección de clavado provienen de `escala_banco.py`.

## 1. Qué se corrió y hasta dónde

| Magnitud | Resultado |
| --- | --- |
| Configuración | PGA x50; PGAout x1; ADC ±2,5 V; IDAC0=+15,+17,+19,+21,+23; IDAC3=0 |
| Filas de canal | 1696 |
| Capturas completas de cinco canales | 336 de 344 registradas |
| Celdas de malla gruesa | 126 de 126 planeadas (100,0 %) |
| Bloques IDAC1 completos | 18 de 18 |
| Capturas adicionales | 18 de referencia, 0 del tramo fino, 192 ABBA de IDAC2 y 8 ABBA de IDAC0 |
| Pasadas con filas | 0, 1, 2 |
| Tiempo hasta la última fila | t_s=3229,240 s (53 min 49,2 s) |
| Intervalo cubierto por filas | 3127,435 s (52 min 7,4 s) |

Las 126 celdas de la malla están presentes; el informe trata la corrida como completa.

## 2. Mapa de validez

Leyenda por canal: **V** = válido y vivo; **C** = válido pero clavado; **F** = fuera de rango; **F\*** = fuera de rango y además clavado; **—** = celda no medida. Cada celda se escribe como `2estado/3estado/4estado`.

**Pasada 1.**
| IDAC1 \ IDAC2 | -255 | -128 | -64 | +0 | +64 | +128 | +255 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -255 | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| -192 | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| -128 | 2F/3F/4F | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| -64 | 2F/3F/4V | 2F/3F/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| +0 | 2F/3F*/4C | 2F/3F/4V | 2F/3F/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| +64 | 2F*/3F*/4C | 2F/3F/4V | 2F/3F/4V | 2F/3F/4F | 2F/3F/4F* | 2V/3V/4F* | 2V/3V/4F* |
| +128 | 2F*/3F*/4C | 2F*/3F*/4C | 2F/3F/4V | 2F/3F/4V | 2F/3F/4F | 2F/3F/4F* | 2V/3V/4F |
| +192 | 2F*/3F*/4V | 2F*/3F*/4C | 2F*/3F*/4C | 2F/3F/4V | 2F/3F/4V | 2F/3F/4F | 2V/3V/4F* |
| +255 | 2F*/3F*/4V | 2F*/3F*/4V | 2F*/3F*/4C | 2F*/3F*/4V | 2F/3F*/4C | 2F/3F/4V | 2F/3F/4F* |

**Pasada 2.**
| IDAC1 \ IDAC2 | -255 | -128 | -64 | +0 | +64 | +128 | +255 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -255 | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| -192 | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| -128 | 2F/3F/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| -64 | 2F/3F/4V | 2F/3F/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| +0 | 2F/3F/4V | 2F/3F/4F | 2F/3F/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* | 2V/3V/4F* |
| +64 | 2F*/3F*/4C | 2F/3F/4V | 2F/3F/4F | 2F/3F/4F* | 2F/3F/4F* | 2V/3V/4F* | 2V/3V/4F* |
| +128 | 2F*/3F*/4V | 2F*/3F*/4C | 2F/3F/4V | 2F/3F/4V | 2F/3F/4F | 2F/3F/4F* | 2V/3V/4F* |
| +192 | 2F*/3F*/4V | 2F*/3F*/4V | 2F*/3F*/4C | 2F/3F/4V | 2F/3F/4V | 2F/3F/4F | 2V/3V/4F* |
| +255 | 2F*/3F*/4V | 2F*/3F*/4V | 2F*/3F*/4C | 2F*/3F*/4V | 2F/3F/4V | 2F/3F/4V | 2F/3F/4F* |

## 3. La diagonal de soluciones

Se buscó, por pasada e IDAC1, el menor `abs(real_mv_vs_vref)` de ch4 entre capturas `malla`, `fino` y `abba` donde ch4 es válido y no está clavado. No se incluyó la captura `referencia`.
| Pasada | IDAC1 | IDAC2 óptimo | Fase | Error ch4 (mV) | Error ch2 (mV) | Filas CSV ch4/ch2 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | +0 | no se puede | — | — | — | — |
| 1 | -255 | no se puede | — | — | — | — |
| 1 | -192 | no se puede | — | — | — | — |
| 1 | -128 | no se puede | — | — | — | — |
| 1 | -64 | -255 | malla | +65,5 | -4533,5 | 327/325 |
| 1 | +0 | -128 | malla | -1410,6 | -3937,5 | 432/430 |
| 1 | +64 | -64 | malla | -738,6 | -4254,3 | 537/535 |
| 1 | +128 | +0 | malla | -504,6 | -4432,0 | 642/640 |
| 1 | +192 | +64 | malla | -244,8 | -4656,9 | 747/745 |
| 1 | +255 | +128 | malla | +179,9 | -4953,2 | 852/850 |
| 2 | -255 | no se puede | — | — | — | — |
| 2 | -192 | no se puede | — | — | — | — |
| 2 | -128 | no se puede | — | — | — | — |
| 2 | -64 | -255 | malla | -1819,0 | -4319,6 | 1307/1305 |
| 2 | +0 | -255 | malla | +324,2 | -5342,2 | 1207/1205 |
| 2 | +64 | -128 | malla | -91,7 | -4900,0 | 1112/1110 |
| 2 | +128 | -64 | malla | +405,1 | -5207,3 | 1017/1015 |
| 2 | +192 | +64 | malla | -543,4 | -4617,0 | 927/925 |
| 2 | +255 | +128 | malla | -16,9 | -4873,1 | 892/890 |

Ajuste lineal de los códigos óptimos:

| Pasada | N | Pendiente ΔIDAC2/ΔIDAC1 | Ordenada (códigos) | RMS (códigos) | R² |
| --- | --- | --- | --- | --- | --- |
| 1 | 6 | +1,1433 | -152,07 | 17,62 | 0,9804 |
| 2 | 6 | +1,3136 | -210,89 | 27,46 | 0,9646 |

Pasada 1: es aproximadamente lineal en los puntos observados; la pendiente observada es +1,1433 códigos de IDAC2 por código de IDAC1.
Pasada 2: es aproximadamente lineal en los puntos observados; la pendiente observada es +1,3136 códigos de IDAC2 por código de IDAC1.
El umbral R² ≥ 0,95 es sólo un criterio descriptivo del conjunto observado; no prueba la relación fuera del sector medido.

## 4. Pendientes locales

| Pasada | IDAC1 | ch2 mV/código | Signo ch2 | RMS ch2 (mV); N | Filas ch2 | ch4 mV/código | Signo ch4 | RMS ch4 (mV); N | Filas ch4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

`no se puede` significa que quedaron menos de dos lecturas vivas del canal en ese tramo; las filas fuera de rango o clavadas no entraron en la recta.

Pendiente de BPo (ch1) contra IDAC1 en la malla:

| Pasada | Pendiente ch1 (mV/código) | RMS (mV) | N | Filas CSV |
| --- | --- | --- | --- | --- |
| 1 | +1,8833 | 18,87 | 63 | 24, 29, 34, 39, 44, 49, 54, 124, 129, 134, 139, 144, 149, 154, 224, 229, 234, 239, 244, 249, 254, 324, 329, 334, 339, 344, 349, 354, 424, 429, 434, 439, 444, 449, 454, 524, 529, 534, 539, 544, 549, 554, 624, 629, 634, 639, 644, 649, 654, 724, 729, 734, 739, 744, 749, 754, 824, 829, 834, 839, 844, 849, 854 |
| 2 | +1,8290 | 9,23 | 63 | 864, 869, 874, 879, 884, 889, 894, 904, 909, 914, 919, 924, 929, 934, 1004, 1009, 1014, 1019, 1024, 1029, 1034, 1104, 1109, 1114, 1119, 1124, 1129, 1134, 1204, 1209, 1214, 1219, 1224, 1229, 1234, 1304, 1309, 1314, 1319, 1324, 1329, 1334, 1404, 1409, 1414, 1419, 1424, 1429, 1434, 1504, 1509, 1514, 1519, 1524, 1529, 1534, 1604, 1609, 1614, 1619, 1624, 1629, 1634 |
El módulo de esta pendiente es el cambio de headroom de BPo por código de IDAC1; el signo indica hacia qué lado se desplaza.

## 5. Coeficientes físicos obtenidos con ABBA

Brazo `abba_idac0`; pendientes físicas por delta:

| Delta | d(ch0)/d(IDAC0) (mV/cód.) | d(ch2)/d(IDAC0) (mV/cód.) | a por delta | Estado | Filas CSV |
| --- | --- | --- | --- | --- | --- |
| 2 | +49,7146 | -6,4577 | -0,12989 | limpia | 2, 3, 4, 5, 6, 7, 8, 9 |
| 4 | +49,6673 | -5,9585 | -0,11997 | limpia | 10, 11, 12, 13, 14, 15, 16, 17 |

Medianas limpias: d(ch0)/d(IDAC0)=+49,6909 mV/código, d(ch2)/d(IDAC0)=-6,2081 mV/código; a=-0,12493.

Pendientes `abba` de IDAC2 por delta:

| Pasada | IDAC1 | Delta | d(ch2)/d(IDAC2) (mV/cód.) | Estado ch2 | d(ch4)/d(IDAC2) (mV/cód.) | Estado ch4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | -255 | 8 | +4,8432 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -255 | 4 | +5,0561 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -255 | 2 | +2,9923 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -192 | 8 | +5,1283 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -192 | 4 | +3,5139 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -192 | 2 | +2,5193 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -128 | 8 | +5,1992 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -128 | 4 | +4,0827 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -128 | 2 | +4,3665 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -64 | 8 | +5,0928 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -64 | 4 | +4,0118 | limpia | — | faltan cuatro lecturas válidas |
| 1 | -64 | 2 | +1,8995 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +0 | 8 | +5,0685 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +0 | 4 | +4,9378 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +0 | 2 | +6,5996 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +64 | 8 | +5,3418 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +64 | 4 | +6,6942 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +64 | 2 | +5,5092 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +128 | 8 | +9,2589 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +128 | 4 | +11,4665 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +128 | 2 | +15,2405 | limpia | — | faltan cuatro lecturas válidas |
| 1 | +192 | 8 | — | faltan cuatro lecturas válidas | — | faltan cuatro lecturas válidas |
| 1 | +192 | 4 | — | faltan cuatro lecturas válidas | — | faltan cuatro lecturas válidas |
| 1 | +192 | 2 | — | faltan cuatro lecturas válidas | — | faltan cuatro lecturas válidas |
| 2 | +192 | 8 | — | faltan cuatro lecturas válidas | — | faltan cuatro lecturas válidas |
| 2 | +192 | 4 | — | faltan cuatro lecturas válidas | — | faltan cuatro lecturas válidas |
| 2 | +192 | 2 | — | faltan cuatro lecturas válidas | — | faltan cuatro lecturas válidas |
| 2 | +128 | 8 | +10,6481 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +128 | 4 | +14,1962 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +128 | 2 | +10,3487 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +64 | 8 | +6,1726 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +64 | 4 | +4,6777 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +64 | 2 | +5,8403 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +0 | 8 | +4,8432 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +0 | 4 | +3,6570 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +0 | 2 | +6,6494 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -64 | 8 | +5,1407 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -64 | 4 | +3,8686 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -64 | 2 | +6,8386 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -128 | 8 | +4,8912 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -128 | 4 | +5,7930 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -128 | 2 | +7,1697 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -192 | 8 | +5,8882 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -192 | 4 | +4,1076 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -192 | 2 | +5,1258 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -255 | 8 | +5,7332 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -255 | 4 | +4,8905 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -255 | 2 | +5,2702 | limpia | — | faltan cuatro lecturas válidas |

Cuartetos excluidos por tener A1/B1/B2/A2 clavados: en `abba`, ch2=0 y ch4=0; en `abba_idac0`, ch0=0 y ch2=0. Se muestran para auditoría, pero sus pendientes no entran en las medianas limpias.

### Calidad del asentamiento

0 de 18 bloques de IDAC1 llegaron al techo sin verificar estabilidad: ninguno. Sus pendientes quedan marcadas y fuera del resumen limpio.

Derivadas locales de la malla usadas para b:

| Pasada | IDAC1 | d(ch1)/d(IDAC1) | d(ch2)/d(IDAC1) | b = d(ch2)/d(ch1) | Pares IDAC2 |
| --- | --- | --- | --- | --- | --- |
| 1 | -255 | +2,6652 | -9,1890 | -3,44775 | 7 |
| 1 | -192 | +2,2732 | -7,9636 | -3,50324 | 6 |
| 1 | -128 | +1,8489 | -6,8880 | -3,72549 | 5 |
| 1 | -64 | +1,8414 | -8,2383 | -4,47385 | 4 |
| 1 | +0 | +1,8192 | -8,6730 | -4,76753 | 2 |
| 1 | +64 | +1,8993 | -7,8524 | -4,13435 | 1 |
| 1 | +128 | +1,7983 | -11,9063 | -6,62078 | 1 |
| 1 | +192 | — | — | — | 0 |
| 2 | -255 | +1,9656 | -7,0849 | -3,60437 | 7 |
| 2 | -192 | +1,9187 | -6,7508 | -3,51837 | 6 |
| 2 | -128 | +1,8993 | -6,7603 | -3,55935 | 5 |
| 2 | -64 | +1,9675 | -8,2338 | -4,18485 | 4 |
| 2 | +0 | +1,8118 | -8,8169 | -4,86642 | 2 |
| 2 | +64 | +1,7510 | -7,9800 | -4,55731 | 1 |
| 2 | +128 | +1,7302 | -11,3127 | -6,53849 | 1 |
| 2 | +192 | — | — | — | 0 |

Medianas ABBA por bloque de IDAC1:

| Pasada | IDAC1 | ch2 limpia (mV/cód.) | ch4 limpia (mV/cód.) | ch2 sin filtro | ch4 sin filtro |
| --- | --- | --- | --- | --- | --- |
| 1 | -255 | +4,8432 | — | +4,8432 | — |
| 1 | -192 | +3,5139 | — | +3,5139 | — |
| 1 | -128 | +4,3665 | — | +4,3665 | — |
| 1 | -64 | +4,0118 | — | +4,0118 | — |
| 1 | +0 | +5,0685 | — | +5,0685 | — |
| 1 | +64 | +5,5092 | — | +5,5092 | — |
| 1 | +128 | +11,4665 | — | +11,4665 | — |
| 1 | +192 | — | — | — | — |
| 2 | -255 | +5,2702 | — | +5,2702 | — |
| 2 | -192 | +5,1258 | — | +5,1258 | — |
| 2 | -128 | +5,7930 | — | +5,7930 | — |
| 2 | -64 | +5,1407 | — | +5,1407 | — |
| 2 | +0 | +4,8432 | — | +4,8432 | — |
| 2 | +64 | +5,8403 | — | +5,8403 | — |
| 2 | +128 | +10,6481 | — | +10,6481 | — |
| 2 | +192 | — | — | — | — |

### Tabla final — sólo pendientes limpias

| Coeficiente | Significado | Mediana | Unidad | Dispersión entre bloques IDAC1 | N bloques |
| --- | --- | --- | --- | --- | --- |
| a | ganancia del sumador desde SEo | -0,12493 |  | no identificable: un solo brazo IDAC0 | 1 |
| b | ganancia del sumador desde BPo | -4,15960 |  | MAD 0,60409; -6,62078…-3,44775 | 14 |
| n = 1 + a + b | ganancia no inversora | -3,28453 |  | MAD 0,60409; -5,74572…-2,57269 | 14 |
| paso_nodo | d(ch2)/d(IDAC2) / n | -1,63818 | mV/código | MAD 0,29688; -2,15811…-1,11476 | 14 |
| R | paso_nodo / 0,125 µA | -13105,5 | Ω | MAD 2375,0; -17264,9…-8918,1 | 14 |
| K | media de ch2 − (n·v2 − a·s − b·p) | +665,78 | mV | MAD 1316,11; -4034,06…+2968,60 | 14 |

Cambian mucho entre bloques (rango mayor que 10 % de la mediana, y al menos 20 mV para K): b, n, paso, R, K. La región no es lineal y un único juego de coeficientes no vale.

Contraste con osciloscopio: R (limpia)=-13105,5 Ω; su módulo se compara con 3294,0 Ω (105 mV/255 códigos y 0,125 µA/código): diferencia +9811,5 Ω (+297,9 %).

## 6. Ajuste del modelo

Se ajustó `salida = A·IDAC2 + B·IDAC1 + C·ch0 + K`. El ajuste principal usa todas las fases registradas; se muestra además la malla gruesa sola para que la concentración de puntos finos no oculte el resultado del muestreo espaciado. La salida y ch0 están en mV físicos respecto de Vref. Para cada salida se exigió que esa salida y ch0 fueran válidos y vivos.
| Datos | Salida | N | A (mV/cód. IDAC2) | B (mV/cód. IDAC1) | C (mV/mV ch0) | K (mV) | RMS (mV) | A−9,56 | Filas de salida |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todas | ch2 | 256 | +4,9921 | -7,3940 | -0,0656 | -1665,1 | 284,71 | -4,5679 | 3, 5, 7, 9, 11, 13, 15, 17, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 230, 235, 240, 245, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 335, 340, 345, 350, 355, 360, 365, 370, 375, 380, 385, 390, 395, 400, 405, 410, 415, 420, 440, 445, 450, 455, 460, 465, 470, 475, 480, 485, 490, 495, 500, 505, 510, 515, 550, 555, 560, 565, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 655, 660, 665, 670, 675, 680, 685, 690, 695, 700, 705, 710, 715, 755, 765, 770, 935, 945, 950, 1035, 1040, 1045, 1050, 1055, 1060, 1065, 1070, 1075, 1080, 1085, 1090, 1095, 1130, 1135, 1140, 1145, 1150, 1155, 1160, 1165, 1170, 1175, 1180, 1185, 1190, 1195, 1200, 1220, 1225, 1230, 1235, 1240, 1245, 1250, 1255, 1260, 1265, 1270, 1275, 1280, 1285, 1290, 1295, 1300, 1315, 1320, 1325, 1330, 1335, 1340, 1345, 1350, 1355, 1360, 1365, 1370, 1375, 1380, 1385, 1390, 1395, 1400, 1410, 1415, 1420, 1425, 1430, 1435, 1440, 1445, 1450, 1455, 1460, 1465, 1470, 1475, 1480, 1485, 1490, 1495, 1500, 1505, 1510, 1515, 1520, 1525, 1530, 1535, 1540, 1545, 1550, 1555, 1560, 1565, 1570, 1575, 1580, 1585, 1590, 1595, 1600, 1605, 1610, 1615, 1620, 1625, 1630, 1635, 1640, 1645, 1650, 1655, 1660, 1665, 1670, 1675, 1680, 1685, 1690, 1695 |
| todas | ch4 | 33 | -2,0816 | +6,9297 | -15,5051 | -1193,6 | 586,21 | -11,6416 | 327, 432, 532, 537, 622, 637, 642, 722, 727, 742, 747, 822, 827, 832, 842, 852, 867, 872, 882, 887, 892, 902, 907, 912, 922, 927, 1002, 1007, 1017, 1022, 1112, 1207, 1307 |
| malla | ch2 | 66 | +5,4447 | -8,5150 | +6,2887 | -1872,4 | 170,19 | -4,1153 | 25, 30, 35, 40, 45, 50, 55, 125, 130, 135, 140, 145, 150, 155, 230, 235, 240, 245, 250, 255, 335, 340, 345, 350, 355, 440, 445, 450, 455, 550, 555, 655, 755, 935, 1035, 1130, 1135, 1220, 1225, 1230, 1235, 1315, 1320, 1325, 1330, 1335, 1410, 1415, 1420, 1425, 1430, 1435, 1505, 1510, 1515, 1520, 1525, 1530, 1535, 1605, 1610, 1615, 1620, 1625, 1630, 1635 |
| malla | ch4 | 28 | -1,4550 | +6,9703 | -27,2161 | -1219,9 | 524,05 | -11,0150 | 327, 432, 532, 537, 637, 642, 727, 742, 747, 827, 832, 842, 852, 867, 872, 882, 887, 892, 907, 912, 922, 927, 1007, 1017, 1022, 1112, 1207, 1307 |

En el ajuste principal de ch2, A cambia -4,5679 mV/código respecto de +9,56 mV/código. El RMS previo era 15,0 mV.
El residuo de ch2, 284,71 mV RMS, supera 15,0 mV. Es grande respecto del ajuste previo y señala que falta al menos un término o que la relación no es constante en el dominio observado.
El residuo de ch4, 586,21 mV RMS, supera 15,0 mV. Es grande respecto del ajuste previo y señala que falta al menos un término o que la relación no es constante en el dominio observado.

## 7. Ganancia de la etapa LP

No se puede calcular: ningún tramo fino tiene al menos dos pares ch2/ch4 válidos y vivos.

## 8. Límites físicos observados

Los extremos siguientes son lecturas de banco. `pp` también está en unidades del banco. Una lectura bajo 880,4 mV se conserva como evidencia de fuera de rango, no como tensión física.
| Canal | Mínimo (mV) | pp mín. (mV) | Estado | Fila/clave del mínimo | Máximo (mV) | pp máx. (mV) | Estado | Fila/clave del máximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ch0 PGAgain (SEo) | 990,924 | 11,672 | V | 10 (P0, abba_idac0, c1=+0, c2=+0) | 1011,390 | 14,553 | V | 14 (P0, abba_idac0, c1=+0, c2=+0) |
| ch1 BPo | 956,707 | 17,642 | V | 19 (P1, referencia, c1=-255, c2=+0) | 1010,494 | 17,089 | V | 829 (P1, malla, c1=+255, c2=-128) |
| ch2 OPA_SUMo | 731,945 | 0,171 | F* | 730 (P1, malla, c1=+192, c2=-128) | 1078,510 | 1,525 | V | 55 (P1, malla, c1=-255, c2=+255) |
| ch3 SUMo | 737,018 | 0,190 | F* | 1006 (P2, malla, c1=+128, c2=-255) | 1077,785 | 1,010 | V | 56 (P1, malla, c1=-255, c2=+255) |
| ch4 LPo | 731,773 | 0,228 | F* | 757 (P1, malla, c1=+192, c2=+255) | 1062,870 | 0,286 | C | 427 (P1, malla, c1=+0, c2=-255) |

Lecturas clavadas repetidas (`pp_banco_uv < 300`):

| Canal | Lado | N | Mínimo (mV) | Mediana (mV) | Máximo (mV) | Rango pp (mV) | Filas CSV |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ch2 OPA_SUMo | bajo | 22 | 731,945 | 732,040 | 732,154 | 0,171–0,267 | 525, 625, 630, 725, 730, 735, 820, 825, 830, 835, 840, 860, 865, 870, 875, 880, 905, 910, 915, 1005, 1010, 1105 |
| ch3 SUMo | bajo | 24 | 737,018 | 737,228 | 737,590 | 0,152–0,267 | 426, 526, 626, 631, 726, 731, 736, 821, 826, 831, 836, 841, 846, 861, 866, 871, 876, 881, 906, 911, 916, 1006, 1011, 1106 |
| ch4 LPo | bajo | 279 | 731,773 | 732,059 | 732,269 | 0,095–0,286 | 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77, 82, 87, 92, 97, 102, 107, 112, 117, 122, 127, 132, 137, 142, 147, 152, 157, 162, 167, 172, 177, 182, 187, 192, 197, 202, 207, 212, 217, 222, 232, 237, 242, 247, 252, 257, 262, 267, 272, 277, 282, 287, 292, 297, 302, 307, 312, 317, 322, 332, 337, 342, 347, 352, 357, 362, 367, 372, 377, 382, 387, 392, 397, 402, 407, 412, 417, 422, 437, 442, 447, 452, 457, 462, 467, 472, 477, 482, 487, 492, 497, 502, 507, 512, 517, 547, 552, 557, 562, 567, 572, 577, 582, 587, 592, 597, 602, 607, 612, 617, 652, 662, 667, 672, 677, 682, 687, 692, 697, 702, 707, 712, 717, 757, 762, 772, 777, 782, 787, 792, 797, 802, 807, 812, 817, 857, 897, 937, 942, 947, 952, 957, 962, 967, 972, 977, 982, 987, 992, 997, 1032, 1037, 1042, 1047, 1052, 1057, 1062, 1067, 1072, 1077, 1082, 1087, 1092, 1097, 1102, 1122, 1127, 1132, 1137, 1142, 1147, 1152, 1157, 1162, 1167, 1172, 1177, 1182, 1187, 1192, 1197, 1202, 1217, 1222, 1227, 1232, 1237, 1242, 1247, 1252, 1257, 1262, 1267, 1272, 1277, 1282, 1287, 1292, 1297, 1302, 1312, 1317, 1322, 1327, 1332, 1337, 1342, 1347, 1352, 1357, 1362, 1367, 1372, 1377, 1382, 1387, 1392, 1397, 1402, 1407, 1412, 1417, 1422, 1427, 1432, 1437, 1442, 1447, 1452, 1457, 1462, 1467, 1472, 1477, 1482, 1487, 1492, 1497, 1502, 1507, 1512, 1517, 1522, 1527, 1532, 1537, 1542, 1547, 1552, 1557, 1562, 1567, 1572, 1577, 1582, 1587, 1592, 1597, 1602, 1607, 1612, 1617, 1622, 1627, 1632, 1637, 1642, 1647, 1652, 1657, 1662, 1667, 1672, 1677, 1682, 1687, 1692, 1697 |
| ch4 LPo | alto | 13 | 1021,995 | 1038,570 | 1062,870 | 0,247–0,286 | 427, 527, 627, 632, 732, 737, 837, 847, 862, 877, 917, 1012, 1107 |

El riel alto repetido aparece en ch4: N=13, mediana 1038,570 mV de banco. Está 84,130 mV de banco por debajo de `BANCO_MAX_VALIDO_MV`=1122,7 mV; por eso una lectura puede estar dentro de la ventana y, a la vez, clavada al riel de la etapa.

## 9. Qué queda sin contestar

- Las dos pasadas de malla están presentes; hay pares ida/vuelta para describir histéresis dentro de las celdas que resultaron válidas.

- La malla gruesa tiene 126 de 126 celdas. Los IDAC1 sin sus siete celdas no permiten extender las pendientes ni la diagonal fuera del sector observado.

- No se pudo obtener pendiente fina de ch4 en: ninguno. En esos casos faltan al menos dos puntos válidos y vivos.

- IDAC3 quedó fijo en cero. Falta medir `ch4/IDAC3` con ch4 vivo para comparar autoridad y resolución con la ruta `IDAC2 → ch2 → ch4`; por eso no se asigna el trim final con este archivo.

- Los tramos rápidos (`fino` o `abba`) se centraron alrededor del mejor ch2, no del mejor ch4. La diagonal de ch4 sólo identifica el mejor código entre los códigos efectivamente muestreados.

- El residuo del modelo de ch2 supera el del ajuste previo. Estos datos no identifican por sí solos cuál es el término faltante; hace falta otra variable o un modelo por regiones.

## Criterios de cálculo

- Conversión de diferencias: 1 mV de banco = 19,9157 mV físicos.

- Ventana válida: 880,4 a 1122,7 mV de banco; objetivo: 1001,5 mV de banco.

- Vivo = `ok=True`, `valido=True` y `clavado=False` en la misma fila.

- Las dispersiones informadas son RMS de los residuos respecto de la recta ajustada. Los mínimos cuadrados se resolvieron con ecuaciones normales, centrado y escalado de predictores, y eliminación gaussiana con pivoteo parcial; no se usaron NumPy ni pandas.
