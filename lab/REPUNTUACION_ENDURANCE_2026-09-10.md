# Re-puntuación de endurance — 2026-09-10

## Criterio aplicado

Se recalcularon los eventos `gain_pass` y `gain_fail` desde `result.final`. El único criterio de señal es que ninguno de los cinco taps toque un riel: se compara `mean_bank_uv +/- pp_bank_uv/2` con la ventana de `escala_banco`, usando como límite alto efectivo el riel medido de 1106,1 mV banco por ser más restrictivo, y un margen de 100,0 mV físicos. Un tap con `pp_bank_uv < 300` también cuenta como riel. Un IDAC queda sin autoridad con |código| >= 255.

LPo se minimiza hacia 0,0 mV de error, pero su error no es una compuerta de aceptación.

El PASS anterior se reconstruyó como `valid` en ch0, ch1 y ch4.

## Resultado global

| Cambios registrados | PASS anterior | Sobreviven | Caen |
|---:|---:|---:|---:|
| 173 | 166 | 0 | 166 |

| Desglose de las caídas | Cambios |
|---|---:|
| La media ya toca riel | 166 |
| Caen sólo al considerar `media +/- pp/2` | 0 |
| Presentan al menos un tap clavado | 150 |
| Sin autoridad IDAC | 0 |

`Clavado` es una firma adicional y puede coincidir con una media en riel; por eso esa fila no se suma a las dos anteriores.

La excursión descubre además 1 tap en 1 cambio que ya caían porque otro tap tenía la media en riel; por eso no agrega una caída completa.

### Endurance recovery 10x

En `dos_fases_endurance_recovery_10x_20260910.json` hay 100 cambios, 100 PASS anteriores y 0 que sobreviven. Caen 100.

| Desglose de las caídas | Cambios |
|---|---:|
| La media ya toca riel | 100 |
| Caen sólo al considerar `media +/- pp/2` | 0 |
| Presentan al menos un tap clavado | 92 |
| Sin autoridad IDAC | 0 |

`Clavado` es una firma adicional y puede coincidir con una media en riel; por eso esa fila no se suma a las dos anteriores.

## Error de LPo logrado por ganancia (informativo)

El error de LPo se informa siempre, pero no cambia PASS/FAIL.

| Ganancia | Registrados | PASS anterior | Sobreviven | Caen | Error LPo mediano (mV físicos) | Rango de error LPo (mV físicos) |
|---:|---:|---:|---:|---:|---:|---:|
| x1 | 35 | 35 | 0 | 35 | 2084,5 | 2083,4 a 2085,3 |
| x2 | 26 | 19 | 0 | 19 | 2246,0 | 2056,8 a 2361,4 |
| x4 | 16 | 16 | 0 | 16 | 2285,1 | 2226,2 a 2327,6 |
| x8 | 16 | 16 | 0 | 16 | 2178,9 | 2178,3 a 2285,4 |
| x16 | 16 | 16 | 0 | 16 | 2125,7 | 2124,8 a 2177,9 |
| x24 | 16 | 16 | 0 | 16 | 2140,2 | 2139,2 a 2140,7 |
| x32 | 16 | 16 | 0 | 16 | 2122,1 | 2120,6 a 2122,9 |
| x48 | 16 | 16 | 0 | 16 | 2141,9 | 2141,1 a 2142,6 |
| x50 | 16 | 16 | 0 | 16 | 2138,8 | 2138,1 a 2140,3 |

## Resultado por campaña

| JSON | Campaña | Registrados | PASS anterior | Sobreviven | Motivo dominante de las caídas |
|---|---:|---:|---:|---:|---|
| `dos_fases_calibrate-gains_20260909_190358.json` | 1 | 2 | 1 | 0 | media toca riel: 1 |
| `dos_fases_calibrate-gains_20260909_191214.json` | 1 | 1 | 0 | 0 | — |
| `dos_fases_calibrate-gains_20260909_191451.json` | 1 | 1 | 0 | 0 | — |
| `dos_fases_calibrate-gains_20260909_191722.json` | 1 | 1 | 1 | 0 | media toca riel: 1 |
| `dos_fases_calibrate-gains_20260909_191914.json` | 1 | 2 | 2 | 0 | media toca riel: 2 |
| `dos_fases_calibrate-gains_20260909_192004.json` | 1 | 2 | 1 | 0 | media toca riel: 1 |
| `dos_fases_calibrate-gains_20260909_192338.json` | 1 | 2 | 2 | 0 | media toca riel: 2 |
| `dos_fases_calibrate-gains_20260909_192428.json` | 1 | 2 | 1 | 0 | media toca riel: 1 |
| `dos_fases_calibrate-gains_20260909_192712.json` | 1 | 2 | 1 | 0 | media toca riel: 1 |
| `dos_fases_calibrate-gains_20260909_193105.json` | 1 | 1 | 1 | 0 | media toca riel: 1 |
| `dos_fases_calibrate-gains_20260909_193232.json` | 1 | 2 | 1 | 0 | media toca riel: 1 |
| `dos_fases_calibrate-gains_20260909_224316.json` | 1 | 9 | 9 | 0 | media toca riel: 9 |
| `dos_fases_calibrate-gains_20260909_224651.json` | 1 | 9 | 9 | 0 | media toca riel: 9 |
| `dos_fases_calibrate-gains_20260909_224651.json` | 2 | 9 | 9 | 0 | media toca riel: 9 |
| `dos_fases_calibrate-gains_20260909_224651.json` | 3 | 9 | 9 | 0 | media toca riel: 9 |
| `dos_fases_calibrate-gains_20260909_224651.json` | 4 | 9 | 9 | 0 | media toca riel: 9 |
| `dos_fases_calibrate-gains_20260909_224651.json` | 5 | 9 | 9 | 0 | media toca riel: 9 |
| `dos_fases_calibrate-gains_20260909_225731.json` | 1 | 1 | 1 | 0 | media toca riel: 1 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 1 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 2 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 3 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 4 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 5 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 6 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 7 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 8 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 9 | 10 | 10 | 0 | media toca riel: 10 |
| `dos_fases_endurance_recovery_10x_20260910.json` | 10 | 10 | 10 | 0 | media toca riel: 10 |

## Archivos

| JSON | Estado |
|---|---|
| `dos_fases_calibrate-gains_20260909_190358.json` | procesado; 2 cambios |
| `dos_fases_calibrate-gains_20260909_190733.json` | sin eventos gain_pass/gain_fail |
| `dos_fases_calibrate-gains_20260909_190937.json` | sin eventos gain_pass/gain_fail |
| `dos_fases_calibrate-gains_20260909_191214.json` | procesado; 1 cambio |
| `dos_fases_calibrate-gains_20260909_191451.json` | procesado; 1 cambio |
| `dos_fases_calibrate-gains_20260909_191722.json` | procesado; 1 cambio |
| `dos_fases_calibrate-gains_20260909_191914.json` | procesado; 2 cambios |
| `dos_fases_calibrate-gains_20260909_192004.json` | procesado; 2 cambios |
| `dos_fases_calibrate-gains_20260909_192338.json` | procesado; 2 cambios |
| `dos_fases_calibrate-gains_20260909_192428.json` | procesado; 2 cambios |
| `dos_fases_calibrate-gains_20260909_192712.json` | procesado; 2 cambios |
| `dos_fases_calibrate-gains_20260909_193105.json` | procesado; 1 cambio |
| `dos_fases_calibrate-gains_20260909_193232.json` | procesado; 2 cambios |
| `dos_fases_calibrate-gains_20260909_224316.json` | procesado; 9 cambios |
| `dos_fases_calibrate-gains_20260909_224651.json` | procesado; 45 cambios |
| `dos_fases_calibrate-gains_20260909_225731.json` | procesado; 1 cambio |
| `dos_fases_endurance_recovery_10x_20260910.json` | procesado; 100 cambios |
