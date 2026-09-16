# Resultados de arranque en frío — 2026-09-10

## Alcance y estado

- Intentos completados: 16 de 16.
- Duración acumulada de los intentos: 3227,1 s (0,90 h).
- Fin de campaña: se completaron los intentos planeados.
- Datos por intento: `lab\arranque_frio\ARRANQUE_FRIO_20260910_210856_SIMULADO.csv`.
- Evidencia estructurada: `lab\arranque_frio\ARRANQUE_FRIO_20260910_210856_SIMULADO.json`.
- Ejecución simulada: no se abrió COM8 ni se llamó a KitProg.

## Tasa de éxito

La tasa global fue 16/16 (100,0 %), con intervalo de Wilson al 95 % de 80,6 %–100,0 %.

| Ganancia | Éxitos/intentos | Tasa | Wilson 95 % |
|---:|---:|---:|---:|
| x24 | 2/16 | 12,5 % | 3,5 %–36,0 % |
| x16 | 2/16 | 12,5 % | 3,5 %–36,0 % |
| x32 | 2/16 | 12,5 % | 3,5 %–36,0 % |
| x50 | 2/16 | 12,5 % | 3,5 %–36,0 % |
| x8 | 2/16 | 12,5 % | 3,5 %–36,0 % |
| x4 | 2/16 | 12,5 % | 3,5 %–36,0 % |
| x2 | 2/16 | 12,5 % | 3,5 %–36,0 % |
| x1 | 2/16 | 12,5 % | 3,5 %–36,0 % |

## Tiempos

| Tramo | n | Media (s) | Desvío (s) | p95 (s) | Máximo (s) |
|---|---:|---:|---:|---:|---:|
| total | 16 | 201,7 | 42,9 | 260,2 | 274,3 |
| calibracion | 16 | 140,6 | 43,0 | 198,9 | 213,2 |
| fase1 | 16 | 108,9 | 36,4 | 163,7 | 171,3 |
| fase2 | 16 | 31,7 | 10,7 | 48,9 | 53,7 |

## Error de LPo logrado

Se informa la mediana y el rango intercuartílico (RIC); no se compara con un umbral.

| Ganancia | n | Mediana (mV) | RIC (mV) |
|---:|---:|---:|---:|
| x24 | 2 | 5,9 | 35,4 |
| x16 | 2 | 40,4 | 95,9 |
| x32 | 2 | 10,5 | 127,5 |
| x50 | 2 | -50,4 | 56,4 |
| x8 | 2 | -81,1 | 44,3 |
| x4 | 2 | 54,4 | 24,4 |
| x2 | 2 | -17,0 | 18,1 |
| x1 | 2 | 146,9 | 1,4 |

## Puntaje

El puntaje de un intento es el menor margen de cualquiera de sus taps respecto de la guarda de 250 mV. Un tap con pico a pico menor que 300 µV se trata como clavado y recibe signo negativo.

Hubo 0 intentos con puntaje negativo de 16 con puntaje calculable.

| Mínimo (mV) | Q1 (mV) | Mediana (mV) | Q3 (mV) | Máximo (mV) |
|---:|---:|---:|---:|---:|
| 1519,5 | 1616,4 | 1645,9 | 1679,7 | 1766,9 |

## Movimientos de actuadores

No se cuentan la perturbación previa ni la vuelta deliberada a cero; sólo movimientos decididos por el calibrador.

| Actuador | Movimientos | Motivos (cantidad) |
|---|---:|---|
| IDAC0 | 4 | mínimo movimiento para margen ch0 (4) |
| IDAC1 | 3 | mínimo movimiento para margen ch1 (3) |
| IDAC2 | 29 | x16: lazo cerrado (resolucion_medio_paso) (2); x1: lazo cerrado (resolucion_medio_paso) (1); x24: lazo cerrado (resolucion_medio_paso) (2); x2: lazo cerrado (resolucion_medio_paso) (2); x32: lazo cerrado (resolucion_medio_paso) (1); x4: lazo cerrado (resolucion_medio_paso) (2); x8: lazo cerrado (resolucion_medio_paso) (1) |
| IDAC3 | 21 | x16: lazo cerrado (resolucion_medio_paso) (1); x1: lazo cerrado (resolucion_medio_paso) (2); x24: lazo cerrado (resolucion_medio_paso) (1); x2: lazo cerrado (resolucion_medio_paso) (2); x4: lazo cerrado (resolucion_medio_paso) (2); x50: lazo cerrado (resolucion_medio_paso) (1); x8: lazo cerrado (resolucion_medio_paso) (1) |

## Comparación de perturbaciones

| Modo | Intentos | Tasa de éxito | Calibración media (s) | Total medio (s) |
|---|---:|---:|---:|---:|
| aleatorio | 8 | 100,0 % | 107,5 | 168,6 |
| golpe | 8 | 100,0 % | 173,7 | 234,8 |

Frente al modo aleatorio, el modo golpe cambió el tiempo medio de calibración en 66,2 s y la tasa de éxito en 0,0 puntos porcentuales. Esa diferencia cuantifica el costo observado de dejar la cadena contra un riel antes de calibrar.

## Limitaciones

- `ToggleReset` resetea el PSoC, pero no corta la alimentación. El electrolítico de 680 µF conserva carga; por lo tanto, esto no es un ciclo de alimentación real y no prueba la rampa de la fuente.
- La perturbación de IDAC reproduce un estado analógico desplazado, no todas las condiciones posibles de un arranque de campo.
- Los datos corresponden a un solo nodo. No cuantifican dispersión entre placas.
- Cada agregado de este informe se obtiene de las filas del CSV citado al comienzo; las evidencias crudas por intento figuran en su columna `evidencia_json`.
