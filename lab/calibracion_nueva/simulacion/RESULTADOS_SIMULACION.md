# Resultados del mapa parcial del sumador — 2026-09-10

Fuente: `C:/Github/Tesis/lab/calibracion_nueva/simulacion/mapear_alcance_sumador_20260910_133744.csv`. Las filas CSV citadas cuentan el encabezado como fila 1. Los valores eléctricos de los ajustes son desviaciones físicas respecto de Vref, tomadas de `real_mv_vs_vref`; los límites y la detección de clavado provienen de `escala_banco.py`.

## 1. Qué se corrió y hasta dónde

| Magnitud | Resultado |
| --- | --- |
| Configuración | PGA x50; PGAout x1; ADC ±2,5 V; IDAC0=+20,+22,+24,+26,+28; IDAC3=0 |
| Filas de canal | 1816 |
| Capturas completas de cinco canales | 360 de 368 registradas |
| Celdas de malla gruesa | 126 de 126 planeadas (100,0 %) |
| Bloques IDAC1 completos | 18 de 18 |
| Capturas adicionales | 18 de referencia, 0 del tramo fino, 216 ABBA de IDAC2 y 8 ABBA de IDAC0 |
| Pasadas con filas | 0, 1, 2 |
| Tiempo hasta la última fila | t_s=2429,800 s (40 min 29,8 s) |
| Intervalo cubierto por filas | 2340,020 s (39 min 0,0 s) |

Las 126 celdas de la malla están presentes; el informe trata la corrida como completa.

## 2. Mapa de validez

Leyenda por canal: **V** = válido y vivo; **C** = válido pero clavado; **F** = fuera de rango; **F\*** = fuera de rango y además clavado; **—** = celda no medida. Cada celda se escribe como `2estado/3estado/4estado`.

**Pasada 1.**
| IDAC1 \ IDAC2 | -255 | -128 | -64 | +0 | +64 | +128 | +255 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -255 | 2C/3C/4F* | 2C/3V/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* |
| -192 | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* |
| -128 | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2V/3C/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* |
| -64 | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3F*/4F* | 2F*/3F*/4F* |
| +0 | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* |
| +64 | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2V/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* |
| +128 | 2F*/3F*/4F* | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F |
| +192 | 2F*/3F*/4F* | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F | 2C/3C/4F* | 2C/3C/4F | 2F/3F*/4F* |
| +255 | 2F*/3F*/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F | 2C/3C/4F* | 2C/3C/4F* |

**Pasada 2.**
| IDAC1 \ IDAC2 | -255 | -128 | -64 | +0 | +64 | +128 | +255 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| -255 | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* |
| -192 | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* |
| -128 | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3V/4F | 2C/3C/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* |
| -64 | 2F*/3F*/4F* | 2C/3C/4F | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3F*/4F* | 2F*/3F*/4F* |
| +0 | 2F*/3F*/4F* | 2C/3C/4F* | 2V/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* |
| +64 | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* |
| +128 | 2F*/3F*/4F* | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* |
| +192 | 2F*/3F*/4F* | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2F*/3F*/4F* |
| +255 | 2F*/3F*/4F* | 2F*/3F*/4F* | 2F*/3F*/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* | 2C/3C/4F* |

## 3. La diagonal de soluciones

Se buscó, por pasada e IDAC1, el menor `abs(real_mv_vs_vref)` de ch4 entre capturas `malla`, `fino` y `abba` donde ch4 es válido y no está clavado. No se incluyó la captura `referencia`.
| Pasada | IDAC1 | IDAC2 óptimo | Fase | Error ch4 (mV) | Error ch2 (mV) | Filas CSV ch4/ch2 |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | +0 | no se puede | — | — | — | — |
| 1 | -255 | no se puede | — | — | — | — |
| 1 | -192 | no se puede | — | — | — | — |
| 1 | -128 | no se puede | — | — | — | — |
| 1 | -64 | no se puede | — | — | — | — |
| 1 | +0 | no se puede | — | — | — | — |
| 1 | +64 | no se puede | — | — | — | — |
| 1 | +128 | no se puede | — | — | — | — |
| 1 | +192 | no se puede | — | — | — | — |
| 1 | +255 | no se puede | — | — | — | — |
| 2 | -255 | no se puede | — | — | — | — |
| 2 | -192 | no se puede | — | — | — | — |
| 2 | -128 | no se puede | — | — | — | — |
| 2 | -64 | no se puede | — | — | — | — |
| 2 | +0 | no se puede | — | — | — | — |
| 2 | +64 | no se puede | — | — | — | — |
| 2 | +128 | no se puede | — | — | — | — |
| 2 | +192 | no se puede | — | — | — | — |
| 2 | +255 | no se puede | — | — | — | — |

Ajuste lineal de los códigos óptimos:

| Pasada | N | Pendiente ΔIDAC2/ΔIDAC1 | Ordenada (códigos) | RMS (códigos) | R² |
| --- | --- | --- | --- | --- | --- |

El umbral R² ≥ 0,95 es sólo un criterio descriptivo del conjunto observado; no prueba la relación fuera del sector medido.

## 4. Pendientes locales

| Pasada | IDAC1 | ch2 mV/código | Signo ch2 | RMS ch2 (mV); N | Filas ch2 | ch4 mV/código | Signo ch4 | RMS ch4 (mV); N | Filas ch4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

`no se puede` significa que quedaron menos de dos lecturas vivas del canal en ese tramo; las filas fuera de rango o clavadas no entraron en la recta.

Pendiente de BPo (ch1) contra IDAC1 en la malla:

| Pasada | Pendiente ch1 (mV/código) | RMS (mV) | N | Filas CSV |
| --- | --- | --- | --- | --- |
| 1 | — | — | 1 | 144 |
| 2 | — | — | 1 | 1549 |
El módulo de esta pendiente es el cambio de headroom de BPo por código de IDAC1; el signo indica hacia qué lado se desplaza.

## 5. Coeficientes físicos obtenidos con ABBA

Brazo `abba_idac0`; pendientes físicas por delta:

| Delta | d(ch0)/d(IDAC0) (mV/cód.) | d(ch2)/d(IDAC0) (mV/cód.) | a por delta | Estado | Filas CSV |
| --- | --- | --- | --- | --- | --- |
| 2 | +1,3767 | -9,7214 | -7,06148 | 4/4 posiciones clavadas | 2, 3, 4, 5, 6, 7, 8, 9 |
| 4 | +1,2671 | -9,4500 | -7,45776 | 4/4 posiciones clavadas | 10, 11, 12, 13, 14, 15, 16, 17 |

Medianas limpias: d(ch0)/d(IDAC0)=— mV/código, d(ch2)/d(IDAC0)=— mV/código; a=—.

Pendientes `abba` de IDAC2 por delta:

| Pasada | IDAC1 | Delta | d(ch2)/d(IDAC2) (mV/cód.) | Estado ch2 | d(ch4)/d(IDAC2) (mV/cód.) | Estado ch4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | -255 | 8 | +14,8459 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -255 | 4 | +14,6604 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -255 | 2 | +14,6206 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -192 | 8 | +14,7102 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -192 | 4 | +14,6343 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -192 | 2 | +14,7526 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -128 | 8 | +14,7880 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -128 | 4 | +14,5746 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -128 | 2 | +14,6032 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -64 | 8 | +14,7295 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -64 | 4 | +14,7177 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | -64 | 2 | +14,4563 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +0 | 8 | +14,7911 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +0 | 4 | +14,7090 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +0 | 2 | +14,7974 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +64 | 8 | +14,6567 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +64 | 4 | +14,6642 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +64 | 2 | +14,7550 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +128 | 8 | +14,7401 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +128 | 4 | +14,6169 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +128 | 2 | +14,8447 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +192 | 8 | +14,7644 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +192 | 4 | +14,7364 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +192 | 2 | +14,6380 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +255 | 8 | +14,7227 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +255 | 4 | +14,7476 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 1 | +255 | 2 | +14,8720 | limpia | — | faltan cuatro lecturas válidas |
| 2 | +255 | 8 | +14,7152 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +255 | 4 | +14,6953 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +255 | 2 | +14,6928 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +192 | 8 | +14,8042 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +192 | 4 | +14,7662 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +192 | 2 | +15,2206 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +128 | 8 | +14,7880 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +128 | 4 | +14,7476 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +128 | 2 | +14,6729 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +64 | 8 | +14,7463 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +64 | 4 | +14,6542 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +64 | 2 | +14,9119 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +0 | 8 | +14,6941 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +0 | 4 | +14,7028 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | +0 | 2 | +14,9293 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -64 | 8 | +14,7619 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -64 | 4 | +14,8484 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -64 | 2 | +15,0588 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -128 | 8 | +14,7961 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -128 | 4 | +14,7687 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -128 | 2 | +14,6953 | limpia | — | faltan cuatro lecturas válidas |
| 2 | -192 | 8 | +14,7874 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -192 | 4 | +14,7662 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -192 | 2 | +14,7451 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -255 | 8 | +14,6941 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -255 | 4 | +14,7389 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |
| 2 | -255 | 2 | +14,5907 | 4/4 posiciones clavadas | — | faltan cuatro lecturas válidas |

Cuartetos excluidos por tener A1/B1/B2/A2 clavados: en `abba`, ch2=51 y ch4=0; en `abba_idac0`, ch0=2 y ch2=2. Se muestran para auditoría, pero sus pendientes no entran en las medianas limpias.

### Calidad del asentamiento

0 de 18 bloques de IDAC1 llegaron al techo sin verificar estabilidad: ninguno. Sus pendientes quedan marcadas y fuera del resumen limpio.

Derivadas locales de la malla usadas para b:

| Pasada | IDAC1 | d(ch1)/d(IDAC1) | d(ch2)/d(IDAC1) | b = d(ch2)/d(ch1) | Pares IDAC2 |
| --- | --- | --- | --- | --- | --- |
| 1 | -255 | — | — | — | 0 |
| 1 | -192 | — | — | — | 0 |
| 1 | -128 | — | — | — | 0 |
| 1 | -64 | — | — | — | 0 |
| 1 | +0 | — | — | — | 0 |
| 1 | +64 | — | — | — | 0 |
| 1 | +128 | — | — | — | 0 |
| 1 | +192 | — | — | — | 0 |
| 1 | +255 | — | — | — | 0 |
| 2 | -255 | — | — | — | 0 |
| 2 | -192 | — | — | — | 0 |
| 2 | -128 | — | — | — | 0 |
| 2 | -64 | — | — | — | 0 |
| 2 | +0 | — | — | — | 0 |
| 2 | +64 | — | — | — | 0 |
| 2 | +128 | — | — | — | 0 |
| 2 | +192 | — | — | — | 0 |
| 2 | +255 | — | — | — | 0 |

Medianas ABBA por bloque de IDAC1:

| Pasada | IDAC1 | ch2 limpia (mV/cód.) | ch4 limpia (mV/cód.) | ch2 sin filtro | ch4 sin filtro |
| --- | --- | --- | --- | --- | --- |
| 1 | -255 | — | — | +14,6604 | — |
| 1 | -192 | — | — | +14,7102 | — |
| 1 | -128 | — | — | +14,6032 | — |
| 1 | -64 | — | — | +14,7177 | — |
| 1 | +0 | — | — | +14,7911 | — |
| 1 | +64 | — | — | +14,6642 | — |
| 1 | +128 | — | — | +14,7401 | — |
| 1 | +192 | — | — | +14,7364 | — |
| 1 | +255 | +14,8720 | — | +14,7476 | — |
| 2 | -255 | — | — | +14,6941 | — |
| 2 | -192 | — | — | +14,7662 | — |
| 2 | -128 | +14,6953 | — | +14,7687 | — |
| 2 | -64 | +15,0588 | — | +14,8484 | — |
| 2 | +0 | — | — | +14,7028 | — |
| 2 | +64 | — | — | +14,7463 | — |
| 2 | +128 | — | — | +14,7476 | — |
| 2 | +192 | — | — | +14,8042 | — |
| 2 | +255 | — | — | +14,6953 | — |

### Tabla final — sólo pendientes limpias

| Coeficiente | Significado | Mediana | Unidad | Dispersión entre bloques IDAC1 | N bloques |
| --- | --- | --- | --- | --- | --- |
| a | ganancia del sumador desde SEo | — |  | no identificable: un solo brazo IDAC0 | 0 |
| b | ganancia del sumador desde BPo | — |  | — | 0 |
| n = 1 + a + b | ganancia no inversora | — |  | — | 0 |
| paso_nodo | d(ch2)/d(IDAC2) / n | — | mV/código | — | 0 |
| R | paso_nodo / 0,125 µA | — | Ω | — | 0 |
| K | media de ch2 − (n·v2 − a·s − b·p) | — | mV | — | 0 |

### Cadena diagnóstica sin filtros

| Coeficiente | Significado | Mediana | Unidad | Dispersión entre bloques IDAC1 | N bloques |
| --- | --- | --- | --- | --- | --- |
| a | ganancia del sumador desde SEo | -7,25141 |  | no identificable: un solo brazo IDAC0 | 1 |
| b | ganancia del sumador desde BPo | -3,97843 |  | MAD 0,03252; -4,08436…-3,94105 | 18 |
| n = 1 + a + b | ganancia no inversora | -10,22985 |  | MAD 0,03252; -10,33577…-10,19246 | 18 |
| paso_nodo | d(ch2)/d(IDAC2) / n | -1,43688 | mV/código | MAD 0,00724; -1,45170…-1,42167 | 18 |
| R | paso_nodo / 0,125 µA | -11495,0 | Ω | MAD 58,0; -11613,6…-11373,4 | 18 |
| K | media de ch2 − (n·v2 − a·s − b·p) | -230,02 | mV | MAD 1832,30; -3872,12…+3484,74 | 18 |

Cambian mucho entre bloques (rango mayor que 10 % de la mediana, y al menos 20 mV para K): K. La región no es lineal y un único juego de coeficientes no vale.

Esta tabla sólo demuestra la cadena de cálculo: incluye cuartetos clavados o bloques sin asentamiento y no debe citarse como medición limpia.

Contraste con osciloscopio: R (diagnóstica sin filtros)=-11495,0 Ω; su módulo se compara con 3294,0 Ω (105 mV/255 códigos y 0,125 µA/código): diferencia +8201,0 Ω (+249,0 %).

## 6. Ajuste del modelo

Se ajustó `salida = A·IDAC2 + B·IDAC1 + C·ch0 + K`. El ajuste principal usa todas las fases registradas; se muestra además la malla gruesa sola para que la concentración de puntos finos no oculte el resultado del muestreo espaciado. La salida y ch0 están en mV físicos respecto de Vref. Para cada salida se exigió que esa salida y ch0 fueran válidos y vivos.
| Datos | Salida | N | A (mV/cód. IDAC2) | B (mV/cód. IDAC1) | C (mV/mV ch0) | K (mV) | RMS (mV) | A−9,56 | Filas de salida |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| todas | ch2 | 0 | — | — | — | — | — | — | — |
| todas | ch4 | 0 | — | — | — | — | — | — | — |
| malla | ch2 | 0 | — | — | — | — | — | — | — |
| malla | ch4 | 0 | — | — | — | — | — | — | — |

No se pudo ajustar ch2: menos de cuatro filas.
No se pudo ajustar ch4: menos de cuatro filas.

## 7. Ganancia de la etapa LP

No se puede calcular: ningún tramo fino tiene al menos dos pares ch2/ch4 válidos y vivos.

## 8. Límites físicos observados

Los extremos siguientes son lecturas de banco. `pp` también está en unidades del banco. Una lectura bajo 880,4 mV se conserva como evidencia de fuera de rango, no como tensión física.
| Canal | Mínimo (mV) | pp mín. (mV) | Estado | Fila/clave del mínimo | Máximo (mV) | pp máx. (mV) | Estado | Fila/clave del máximo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ch0 PGAgain (SEo) | 1001,965 | 0,280 | C | 16 (P0, abba_idac0, c1=+0, c2=+0) | 1002,529 | 0,244 | C | 14 (P0, abba_idac0, c1=+0, c2=+0) |
| ch1 BPo | 980,442 | 0,279 | C | 39 (P1, malla, c1=-255, c2=+0) | 1026,559 | 0,277 | C | 819 (P1, referencia, c1=+255, c2=+0) |
| ch2 OPA_SUMo | 875,000 | 0,255 | F* | 225 (P1, malla, c1=-128, c2=-255) | 1128,000 | 0,277 | F* | 45 (P1, malla, c1=-255, c2=+64) |
| ch3 SUMo | 875,000 | 0,253 | F* | 226 (P1, malla, c1=-128, c2=-255) | 1128,000 | 0,280 | F* | 46 (P1, malla, c1=-255, c2=+64) |
| ch4 LPo | 875,000 | 0,242 | F* | 22 (P1, referencia, c1=-255, c2=+0) | 875,104 | 0,275 | F* | 1767 (P2, abba, c1=-255, c2=-120) |

Lecturas clavadas repetidas (`pp_banco_uv < 300`):

| Canal | Lado | N | Mínimo (mV) | Mediana (mV) | Máximo (mV) | Rango pp (mV) | Filas CSV |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ch0 PGAgain (SEo) | alto | 357 | 1001,965 | 1002,232 | 1002,529 | 0,241–0,298 | 2, 4, 6, 8, 10, 12, 14, 16, 18, 23, 28, 33, 38, 43, 48, 53, 58, 63, 68, 73, 78, 83, 88, 93, 98, 103, 108, 113, 118, 123, 133, 138, 143, 148, 153, 158, 163, 168, 173, 178, 183, 188, 193, 198, 203, 208, 213, 223, 228, 233, 238, 243, 248, 253, 258, 263, 268, 273, 278, 283, 288, 293, 298, 303, 308, 313, 323, 328, 333, 338, 343, 348, 353, 363, 368, 373, 378, 383, 388, 393, 398, 403, 408, 413, 418, 423, 428, 433, 438, 443, 448, 453, 458, 463, 468, 473, 478, 483, 488, 493, 498, 503, 508, 513, 518, 523, 528, 533, 538, 543, 548, 553, 558, 563, 568, 573, 578, 583, 588, 593, 598, 603, 608, 613, 618, 623, 628, 633, 638, 643, 648, 653, 658, 663, 668, 673, 678, 683, 688, 693, 698, 703, 708, 713, 718, 723, 728, 738, 743, 748, 753, 758, 763, 768, 773, 778, 783, 788, 793, 798, 803, 808, 813, 818, 823, 828, 833, 838, 843, 848, 853, 858, 863, 868, 873, 878, 883, 888, 893, 898, 903, 908, 913, 918, 923, 928, 933, 938, 943, 948, 953, 958, 963, 968, 973, 978, 983, 988, 993, 998, 1003, 1008, 1013, 1018, 1023, 1028, 1033, 1038, 1043, 1048, 1053, 1058, 1063, 1068, 1073, 1078, 1083, 1088, 1093, 1098, 1103, 1108, 1113, 1118, 1123, 1128, 1133, 1138, 1143, 1148, 1153, 1158, 1163, 1168, 1173, 1188, 1193, 1198, 1203, 1208, 1213, 1218, 1223, 1228, 1233, 1238, 1243, 1248, 1253, 1258, 1263, 1268, 1273, 1278, 1283, 1288, 1293, 1298, 1303, 1308, 1313, 1318, 1323, 1328, 1333, 1338, 1343, 1348, 1353, 1358, 1363, 1368, 1378, 1383, 1388, 1393, 1398, 1403, 1408, 1418, 1423, 1428, 1433, 1438, 1443, 1448, 1453, 1458, 1468, 1473, 1478, 1483, 1488, 1493, 1498, 1503, 1508, 1513, 1518, 1523, 1528, 1533, 1538, 1543, 1548, 1553, 1558, 1563, 1568, 1573, 1578, 1583, 1588, 1593, 1598, 1603, 1608, 1613, 1618, 1623, 1628, 1633, 1638, 1643, 1648, 1653, 1663, 1668, 1673, 1678, 1683, 1688, 1693, 1698, 1703, 1708, 1713, 1718, 1723, 1728, 1733, 1738, 1743, 1748, 1753, 1758, 1763, 1768, 1773, 1778, 1783, 1788, 1793, 1798, 1803, 1808, 1813 |
| ch1 BPo | bajo | 157 | 980,442 | 991,896 | 997,824 | 0,241–0,295 | 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 94, 99, 104, 109, 114, 119, 124, 129, 134, 139, 149, 154, 159, 164, 169, 174, 179, 184, 189, 194, 199, 204, 209, 214, 219, 224, 229, 234, 239, 244, 249, 254, 259, 264, 269, 274, 279, 284, 289, 294, 299, 304, 309, 314, 319, 324, 329, 334, 339, 344, 349, 354, 359, 364, 369, 374, 379, 384, 389, 394, 399, 404, 409, 414, 1419, 1424, 1429, 1434, 1439, 1444, 1449, 1454, 1459, 1464, 1469, 1474, 1479, 1484, 1489, 1494, 1499, 1504, 1509, 1514, 1519, 1524, 1529, 1534, 1539, 1544, 1554, 1559, 1564, 1569, 1574, 1579, 1584, 1589, 1594, 1599, 1604, 1609, 1614, 1619, 1624, 1629, 1634, 1639, 1644, 1649, 1654, 1659, 1664, 1669, 1674, 1679, 1684, 1689, 1694, 1699, 1704, 1709, 1714, 1719, 1724, 1729, 1734, 1739, 1744, 1749, 1754, 1759, 1764, 1769, 1774, 1779, 1784, 1789, 1794, 1799, 1804, 1809, 1814 |
| ch1 BPo | alto | 198 | 1003,420 | 1015,038 | 1026,559 | 0,241–0,297 | 419, 424, 429, 434, 439, 444, 449, 454, 459, 464, 469, 474, 479, 484, 489, 494, 499, 504, 509, 514, 519, 524, 529, 534, 539, 544, 549, 554, 559, 564, 569, 574, 579, 584, 589, 594, 599, 604, 609, 614, 619, 624, 629, 634, 639, 644, 649, 654, 659, 664, 669, 674, 679, 684, 689, 694, 699, 704, 709, 714, 719, 724, 729, 734, 739, 744, 749, 754, 759, 764, 769, 774, 779, 784, 789, 794, 799, 804, 809, 814, 819, 824, 829, 834, 839, 844, 849, 854, 859, 864, 869, 874, 879, 884, 889, 894, 899, 904, 909, 914, 919, 924, 929, 934, 939, 944, 949, 954, 959, 964, 969, 974, 979, 984, 989, 994, 999, 1004, 1009, 1014, 1019, 1024, 1029, 1034, 1039, 1044, 1049, 1054, 1059, 1064, 1069, 1074, 1079, 1084, 1089, 1094, 1099, 1104, 1109, 1114, 1119, 1124, 1129, 1134, 1139, 1144, 1149, 1154, 1159, 1164, 1169, 1174, 1179, 1184, 1189, 1194, 1204, 1209, 1214, 1219, 1224, 1229, 1234, 1239, 1244, 1249, 1254, 1259, 1264, 1269, 1274, 1279, 1284, 1289, 1294, 1299, 1304, 1309, 1314, 1319, 1324, 1329, 1334, 1339, 1344, 1349, 1354, 1359, 1369, 1374, 1379, 1384, 1389, 1394, 1399, 1404, 1409, 1414 |
| ch2 OPA_SUMo | bajo | 186 | 875,000 | 979,428 | 1001,374 | 0,240–0,298 | 25, 30, 60, 75, 80, 95, 100, 115, 125, 130, 225, 230, 260, 275, 280, 295, 300, 315, 325, 330, 335, 360, 365, 370, 375, 380, 385, 390, 395, 400, 405, 410, 415, 425, 430, 435, 460, 475, 480, 495, 520, 525, 530, 535, 560, 565, 570, 575, 580, 585, 590, 595, 600, 605, 610, 615, 620, 625, 630, 635, 640, 660, 675, 720, 725, 730, 735, 740, 745, 760, 765, 770, 775, 780, 785, 790, 795, 800, 805, 810, 815, 820, 825, 830, 835, 840, 845, 920, 925, 930, 935, 940, 945, 960, 975, 1020, 1025, 1030, 1035, 1040, 1045, 1060, 1065, 1070, 1075, 1080, 1085, 1090, 1095, 1100, 1105, 1110, 1115, 1120, 1125, 1130, 1135, 1140, 1160, 1175, 1220, 1225, 1230, 1235, 1240, 1260, 1265, 1270, 1275, 1280, 1285, 1290, 1295, 1300, 1305, 1310, 1315, 1325, 1330, 1360, 1375, 1380, 1395, 1425, 1430, 1435, 1460, 1465, 1470, 1475, 1480, 1485, 1490, 1495, 1500, 1510, 1515, 1525, 1530, 1560, 1575, 1580, 1595, 1600, 1625, 1630, 1660, 1665, 1670, 1675, 1680, 1685, 1690, 1695, 1700, 1705, 1710, 1715, 1725, 1730, 1760, 1775, 1780, 1795, 1800, 1815 |
| ch2 OPA_SUMo | alto | 175 | 1001,533 | 1010,180 | 1128,000 | 0,244–0,296 | 3, 5, 7, 9, 11, 13, 15, 17, 20, 35, 40, 45, 50, 55, 65, 70, 85, 90, 105, 110, 120, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 215, 220, 235, 240, 250, 255, 265, 270, 285, 290, 305, 310, 320, 340, 345, 350, 355, 420, 440, 445, 450, 455, 465, 470, 485, 490, 500, 505, 510, 515, 545, 550, 555, 645, 650, 655, 665, 670, 680, 685, 690, 695, 700, 705, 710, 715, 750, 850, 855, 860, 865, 870, 875, 880, 885, 890, 895, 905, 910, 915, 950, 955, 965, 970, 980, 985, 990, 995, 1000, 1005, 1010, 1015, 1050, 1055, 1145, 1150, 1155, 1165, 1170, 1180, 1185, 1190, 1195, 1200, 1205, 1210, 1215, 1245, 1250, 1255, 1320, 1340, 1345, 1350, 1355, 1365, 1370, 1385, 1390, 1400, 1405, 1410, 1415, 1420, 1440, 1445, 1450, 1455, 1520, 1535, 1540, 1545, 1550, 1555, 1565, 1570, 1585, 1590, 1605, 1610, 1620, 1635, 1640, 1645, 1650, 1655, 1720, 1735, 1740, 1745, 1750, 1755, 1765, 1770, 1785, 1790, 1805, 1810 |
| ch3 SUMo | bajo | 173 | 875,000 | 980,204 | 1001,380 | 0,244–0,298 | 26, 61, 76, 81, 96, 101, 116, 126, 131, 226, 231, 261, 276, 281, 296, 326, 331, 336, 361, 366, 371, 376, 381, 386, 391, 396, 401, 406, 411, 416, 426, 431, 436, 461, 476, 521, 526, 531, 536, 541, 561, 566, 571, 576, 581, 586, 591, 596, 601, 606, 611, 616, 621, 626, 631, 636, 641, 721, 726, 731, 736, 741, 746, 761, 766, 771, 776, 781, 786, 791, 796, 801, 806, 811, 816, 821, 826, 831, 836, 841, 846, 921, 926, 931, 936, 941, 946, 1021, 1026, 1031, 1036, 1041, 1046, 1061, 1066, 1071, 1076, 1081, 1086, 1091, 1096, 1101, 1106, 1111, 1116, 1121, 1126, 1131, 1136, 1141, 1161, 1176, 1221, 1226, 1231, 1236, 1241, 1261, 1266, 1271, 1276, 1281, 1286, 1291, 1296, 1301, 1306, 1311, 1316, 1326, 1331, 1336, 1361, 1376, 1426, 1431, 1436, 1461, 1466, 1471, 1476, 1481, 1486, 1491, 1496, 1501, 1506, 1511, 1516, 1526, 1531, 1561, 1576, 1581, 1596, 1626, 1631, 1661, 1666, 1671, 1676, 1681, 1686, 1691, 1696, 1701, 1706, 1711, 1716, 1726, 1776, 1781, 1796 |
| ch3 SUMo | alto | 182 | 1001,845 | 1011,054 | 1128,000 | 0,240–0,298 | 21, 36, 41, 46, 51, 56, 66, 71, 86, 91, 106, 111, 121, 136, 141, 146, 151, 156, 161, 166, 171, 176, 181, 186, 191, 196, 201, 206, 211, 216, 221, 236, 241, 246, 251, 256, 266, 271, 286, 291, 301, 306, 311, 316, 321, 341, 346, 351, 356, 421, 441, 446, 451, 456, 466, 471, 481, 486, 491, 496, 501, 506, 511, 516, 546, 551, 556, 646, 651, 656, 661, 666, 671, 676, 681, 686, 691, 696, 701, 706, 711, 716, 751, 756, 851, 856, 861, 866, 871, 876, 881, 886, 896, 901, 906, 911, 916, 951, 956, 961, 966, 971, 976, 981, 986, 996, 1001, 1006, 1011, 1016, 1051, 1056, 1146, 1151, 1156, 1166, 1171, 1181, 1186, 1191, 1196, 1201, 1206, 1211, 1216, 1246, 1251, 1256, 1321, 1341, 1346, 1351, 1356, 1366, 1371, 1381, 1386, 1391, 1396, 1401, 1406, 1411, 1416, 1421, 1441, 1446, 1451, 1456, 1521, 1536, 1546, 1551, 1556, 1566, 1571, 1586, 1591, 1601, 1606, 1611, 1616, 1621, 1636, 1641, 1646, 1651, 1656, 1721, 1731, 1736, 1741, 1746, 1751, 1756, 1766, 1771, 1786, 1791, 1801, 1806, 1811, 1816 |
| ch4 LPo | bajo | 345 | 875,000 | 875,000 | 875,104 | 0,241–0,299 | 22, 27, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77, 82, 87, 92, 97, 102, 107, 112, 117, 122, 127, 132, 137, 142, 147, 152, 157, 162, 167, 172, 177, 182, 192, 197, 202, 207, 212, 217, 222, 227, 232, 237, 242, 247, 252, 257, 262, 267, 272, 277, 282, 287, 292, 297, 302, 307, 312, 317, 322, 327, 332, 337, 342, 347, 352, 357, 362, 367, 372, 377, 382, 387, 392, 397, 402, 407, 412, 422, 427, 432, 437, 442, 447, 452, 457, 462, 467, 472, 477, 482, 487, 492, 497, 502, 507, 512, 517, 522, 527, 532, 537, 542, 547, 552, 557, 562, 567, 572, 577, 582, 587, 592, 597, 602, 607, 612, 617, 622, 627, 632, 637, 642, 647, 652, 662, 667, 672, 677, 682, 687, 692, 697, 702, 707, 712, 717, 722, 727, 732, 737, 747, 757, 762, 767, 772, 777, 782, 787, 792, 797, 802, 807, 812, 822, 827, 832, 837, 842, 852, 857, 867, 872, 877, 882, 887, 892, 897, 902, 907, 912, 917, 922, 927, 932, 937, 942, 947, 952, 957, 962, 967, 972, 977, 987, 992, 997, 1002, 1007, 1012, 1017, 1022, 1027, 1032, 1037, 1042, 1047, 1052, 1057, 1062, 1067, 1072, 1077, 1082, 1087, 1092, 1097, 1102, 1107, 1112, 1117, 1122, 1127, 1132, 1137, 1142, 1147, 1152, 1157, 1162, 1167, 1172, 1177, 1182, 1187, 1192, 1197, 1202, 1207, 1212, 1217, 1222, 1227, 1232, 1237, 1242, 1247, 1252, 1257, 1262, 1267, 1272, 1277, 1282, 1287, 1292, 1297, 1307, 1312, 1317, 1322, 1327, 1332, 1337, 1342, 1347, 1352, 1357, 1362, 1367, 1372, 1377, 1382, 1387, 1392, 1402, 1407, 1417, 1422, 1427, 1437, 1442, 1447, 1452, 1457, 1462, 1467, 1472, 1477, 1482, 1487, 1492, 1497, 1502, 1507, 1512, 1517, 1522, 1527, 1532, 1537, 1547, 1552, 1557, 1562, 1567, 1572, 1577, 1582, 1587, 1592, 1597, 1602, 1607, 1612, 1617, 1622, 1627, 1632, 1637, 1642, 1647, 1652, 1657, 1662, 1667, 1672, 1682, 1687, 1692, 1697, 1702, 1707, 1712, 1717, 1722, 1727, 1732, 1737, 1742, 1747, 1752, 1757, 1762, 1767, 1772, 1777, 1782, 1787, 1792, 1797, 1802, 1807, 1812, 1817 |

El riel alto repetido aparece en ch0: N=357, mediana 1002,232 mV de banco. Está 120,468 mV de banco por debajo de `BANCO_MAX_VALIDO_MV`=1122,7 mV; por eso una lectura puede estar dentro de la ventana y, a la vez, clavada al riel de la etapa.

## 9. Qué queda sin contestar

- Las dos pasadas de malla están presentes; hay pares ida/vuelta para describir histéresis dentro de las celdas que resultaron válidas.

- La malla gruesa tiene 126 de 126 celdas. Los IDAC1 sin sus siete celdas no permiten extender las pendientes ni la diagonal fuera del sector observado.

- No se pudo obtener pendiente fina de ch4 en: ninguno. En esos casos faltan al menos dos puntos válidos y vivos.

- IDAC3 quedó fijo en cero. Falta medir `ch4/IDAC3` con ch4 vivo para comparar autoridad y resolución con la ruta `IDAC2 → ch2 → ch4`; por eso no se asigna el trim final con este archivo.

- Los tramos rápidos (`fino` o `abba`) se centraron alrededor del mejor ch2, no del mejor ch4. La diagonal de ch4 sólo identifica el mejor código entre los códigos efectivamente muestreados.

## Criterios de cálculo

- Conversión de diferencias: 1 mV de banco = 19,9157 mV físicos.

- Ventana válida: 880,4 a 1122,7 mV de banco; objetivo: 1001,5 mV de banco.

- Vivo = `ok=True`, `valido=True` y `clavado=False` en la misma fila.

- Las dispersiones informadas son RMS de los residuos respecto de la recta ajustada. Los mínimos cuadrados se resolvieron con ecuaciones normales, centrado y escalado de predictores, y eliminación gaussiana con pivoteo parcial; no se usaron NumPy ni pandas.
