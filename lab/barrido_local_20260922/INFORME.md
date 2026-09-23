# Barrido exhaustivo de ganancias

Generado el 2026-09-23 08:33. 81 visitas medidas sobre 81 pares distintos: 38 PASA (47 %), 25 FALLA, 18 que seguian APRENDIENDO al vencerse el tiempo, 0 INVALIDA.


**APRENDIENDO no es un fallo**: el nodo no habia terminado de buscar su punto cuando se acabo el tiempo asignado. Un aprendizaje en frio a ganancia alta puede tardar 600-800 s. Informarlo como fallo seria medir la ventana del banco y no el nodo.

Horas de banco acumuladas: 11.6.


**Criterio.** `estable` es el instante desde el cual LPo ya no vuelve a salir de la ventana de +-97 mV. El "primer cruce" que declara el firmware puede ser un rescate cruzando de un riel al otro, y como numero de convergencia miente.


Cada par arranca donde lo dejo el anterior, asi que el tiempo depende del camino: por eso se repite el barrido y se informa el LPo de partida.


## Todos los pares

| PGA | PGAout | ganancia | visitas | PASA | estable mediana | estable peor | LPo final | I0 | I1 | I2 | I3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| x1 | x1 | **1** | 1 | 1 | 2 s | 2 s | -24.7 mV | 7 | 7 | 1 | -89 |
| x1 | x2 | **2** | 1 | 1 | 2 s | 2 s | -3.1 mV | 7 | 7 | 1 | -89 |
| x2 | x1 | **2** | 1 | 1 | 2 s | 2 s | -20.4 mV | 0 | 0 | 0 | 0 |
| x1 | x4 | **4** | 1 | 1 | 2 s | 2 s | 36.2 mV | 7 | 7 | 1 | -96 |
| x2 | x2 | **4** | 1 | 1 | 2 s | 2 s | -30.3 mV | 0 | 0 | 0 | 0 |
| x4 | x1 | **4** | 1 | 1 | 2 s | 2 s | -42.6 mV | 0 | 0 | 0 | 0 |
| x1 | x8 | **8** | 1 | 1 | 58 s | 58 s | 40.7 mV | 7 | 7 | 2 | -255 |
| x2 | x4 | **8** | 1 | 1 | 148 s | 148 s | -61.0 mV | 0 | 0 | 7 | 253 |
| x4 | x2 | **8** | 1 | 1 | 56 s | 56 s | -40.9 mV | 0 | 0 | 0 | 197 |
| x8 | x1 | **8** | 1 | 1 | 94 s | 94 s | -46.5 mV | 0 | 0 | -9 | 97 |
| x1 | x16 | **16** | 1 | 1 | 81 s | 81 s | 10.2 mV | 7 | 7 | 6 | -241 |
| x2 | x8 | **16** | 1 | 1 | 188 s | 188 s | -58.4 mV | 0 | 0 | 2 | 240 |
| x4 | x4 | **16** | 1 | 1 | 229 s | 229 s | -40.9 mV | 1 | 1 | -3 | 252 |
| x8 | x2 | **16** | 1 | 1 | 290 s | 290 s | 58.5 mV | 7 | 5 | -13 | 251 |
| x16 | x1 | **16** | 1 | 1 | 94 s | 94 s | 55.1 mV | 20 | 13 | -6 | -255 |
| x1 | x24 | **24** | 1 | 1 | 2 s | 2 s | -8.5 mV | 7 | 7 | 7 | -231 |
| x24 | x1 | **24** | 1 | 1 | 158 s | 158 s | -57.8 mV | 12 | 6 | -10 | -170 |
| x1 | x32 | **32** | 1 | 1 | 2 s | 2 s | 21.3 mV | 7 | 7 | 7 | -231 |
| x2 | x16 | **32** | 1 | 1 | 34 s | 34 s | -7.2 mV | 0 | 0 | -1 | 245 |
| x4 | x8 | **32** | 1 | 1 | 214 s | 214 s | -29.6 mV | 2 | 1 | -6 | 249 |
| x8 | x4 | **32** | 1 | 1 | 62 s | 62 s | 44.1 mV | 7 | 5 | -13 | -69 |
| x16 | x2 | **32** | 1 | 0 | — | — | 57.4 mV | 7 | 5 | -6 | -255 |
| x32 | x1 | **32** | 1 | 1 | 173 s | 173 s | -9.0 mV | 12 | 6 | 0 | -1 |
| x1 | x48 | **48** | 1 | 1 | 77 s | 77 s | -60.1 mV | 7 | 7 | 8 | -161 |
| x2 | x24 | **48** | 1 | 1 | 2 s | 2 s | 17.9 mV | 0 | 0 | -2 | 235 |
| x24 | x2 | **48** | 1 | 0 | — | — | 15.1 mV | 12 | 6 | -17 | 65 |
| x48 | x1 | **48** | 1 | 1 | 719 s | 719 s | -32.7 mV | 11 | 7 | -3 | 132 |
| x1 | x50 | **50** | 1 | 1 | 2 s | 2 s | -47.6 mV | 7 | 7 | 8 | -150 |
| x50 | x1 | **50** | 1 | 1 | 925 s | 925 s | -58.0 mV | 12 | 7 | -1 | -43 |
| x2 | x32 | **64** | 1 | 1 | 2 s | 2 s | 1.4 mV | 0 | 0 | -2 | 235 |
| x4 | x16 | **64** | 1 | 1 | 19 s | 19 s | -53.0 mV | 2 | 1 | -7 | 244 |
| x8 | x8 | **64** | 1 | 1 | 73 s | 73 s | 52.8 mV | 7 | 5 | -12 | -252 |
| x16 | x4 | **64** | 1 | 0 | — | — | -14.6 mV | 9 | 8 | 0 | 0 |
| x32 | x2 | **64** | 1 | 0 | — | — | -91.6 mV | 13 | 7 | -15 | 255 |
| x2 | x48 | **96** | 1 | 1 | 2 s | 2 s | -18.1 mV | 0 | 0 | -2 | 238 |
| x4 | x24 | **96** | 1 | 1 | 2 s | 2 s | -30.1 mV | 2 | 1 | -8 | 237 |
| x24 | x4 | **96** | 1 | 0 | — | — | — mV | 12 | 6 | -9 | -127 |
| x48 | x2 | **96** | 1 | 0 | — | — | -32.5 mV | 26 | 14 | -10 | 255 |
| x2 | x50 | **100** | 1 | 1 | 2 s | 2 s | -47.3 mV | 0 | 0 | -2 | 245 |
| x50 | x2 | **100** | 1 | 0 | — | — | — mV | 13 | 7 | -17 | 255 |
| x4 | x32 | **128** | 1 | 1 | 2 s | 2 s | 65.2 mV | 2 | 1 | -9 | 222 |
| x8 | x16 | **128** | 1 | 1 | 17 s | 17 s | 26.2 mV | 7 | 5 | -10 | -255 |
| x16 | x8 | **128** | 1 | 0 | — | — | -25.8 mV | 10 | 9 | 0 | 0 |
| x32 | x4 | **128** | 1 | 0 | — | — | -29.8 mV | 12 | 6 | -2 | 253 |
| x4 | x48 | **192** | 1 | 1 | 2 s | 2 s | 56.1 mV | 2 | 1 | -9 | 156 |
| x8 | x24 | **192** | 1 | 1 | 2 s | 2 s | 19.3 mV | 7 | 5 | -9 | -249 |
| x24 | x8 | **192** | 1 | 0 | — | — | -10.5 mV | 12 | 6 | -8 | -113 |
| x48 | x4 | **192** | 1 | 0 | — | — | — mV | 26 | 14 | -9 | 221 |
| x4 | x50 | **200** | 1 | 1 | 2 s | 2 s | 46.3 mV | 2 | 1 | -9 | 83 |
| x50 | x4 | **200** | 1 | 0 | — | — | — mV | 12 | 7 | -4 | 253 |
| x8 | x32 | **256** | 1 | 0 | — | — | -94.3 mV | 7 | 5 | -8 | -216 |
| x16 | x16 | **256** | 1 | 0 | — | — | 26.7 mV | 9 | 8 | 0 | 0 |
| x32 | x8 | **256** | 1 | 0 | — | — | -47.0 mV | 12 | 6 | -2 | 127 |
| x8 | x48 | **384** | 1 | 0 | — | — | 93.6 mV | 7 | 5 | -10 | 215 |
| x16 | x24 | **384** | 1 | 0 | — | — | 1.0 mV | 8 | 7 | 0 | 0 |
| x24 | x16 | **384** | 1 | 0 | — | — | 51.7 mV | 12 | 6 | -6 | -143 |
| x48 | x8 | **384** | 1 | 0 | — | — | 58.3 mV | 26 | 14 | -7 | -129 |
| x8 | x50 | **400** | 1 | 0 | — | — | 28.9 mV | 15 | 15 | 0 | 0 |
| x50 | x8 | **400** | 1 | 0 | — | — | — mV | 12 | 7 | -4 | 191 |
| x16 | x32 | **512** | 1 | 0 | — | — | -20.1 mV | 9 | 8 | 0 | 0 |
| x32 | x16 | **512** | 1 | 0 | — | — | 55.9 mV | 12 | 6 | -1 | 137 |
| x24 | x24 | **576** | 1 | 0 | — | — | -67.8 mV | 12 | 6 | -1 | -255 |
| x16 | x48 | **768** | 1 | 0 | — | — | 23.7 mV | 7 | 5 | -10 | -235 |
| x24 | x32 | **768** | 1 | 0 | — | — | 21.6 mV | 12 | 6 | -2 | -247 |
| x32 | x24 | **768** | 1 | 0 | — | — | -87.8 mV | 12 | 6 | -2 | 119 |
| x48 | x16 | **768** | 1 | 0 | — | — | -19.1 mV | 26 | 14 | -2 | -255 |
| x16 | x50 | **800** | 1 | 0 | — | — | 22.9 mV | 7 | 5 | -10 | -233 |
| x50 | x16 | **800** | 1 | 0 | — | — | — mV | 0 | 0 | 0 | 0 |
| x32 | x32 | **1024** | 1 | 0 | — | — | — mV | 0 | 0 | 0 | 0 |
| x24 | x48 | **1152** | 1 | 0 | — | — | — mV | 0 | 0 | 0 | 0 |
| x48 | x24 | **1152** | 1 | 0 | — | — | — mV | 0 | 0 | 0 | 0 |
| x24 | x50 | **1200** | 1 | 0 | — | — | -33.5 mV | 3 | 3 | 0 | 0 |
| x50 | x24 | **1200** | 1 | 0 | — | — | — mV | 1 | 1 | 0 | 0 |
| x32 | x48 | **1536** | 1 | 0 | — | — | — mV | 3 | 3 | 0 | 0 |
| x48 | x32 | **1536** | 1 | 0 | — | — | -93.5 mV | 1 | 1 | 0 | 0 |
| x32 | x50 | **1600** | 1 | 0 | — | — | — mV | 12 | 6 | -3 | 121 |
| x50 | x32 | **1600** | 1 | 0 | — | — | -34.4 mV | 12 | 7 | -4 | 197 |
| x48 | x48 | **2304** | 1 | 0 | — | — | — mV | 26 | 14 | 0 | -249 |
| x48 | x50 | **2400** | 1 | 0 | — | — | -12.7 mV | 26 | 14 | 3 | -233 |
| x50 | x48 | **2400** | 1 | 0 | — | — | — mV | 12 | 7 | -3 | -57 |
| x50 | x50 | **2500** | 1 | 0 | — | — | — mV | 0 | 0 | 0 | 0 |

## Recomendados

Pares que pasaron **todas** sus visitas, con LPo final dentro de +-60 mV (banda del modo estable) y mediana de estabilizacion por debajo de 60 s. Ordenados por ganancia.

| PGA | PGAout | ganancia | estable mediana | LPo final | visitas |
|---|---|---|---|---|---|
| x4 | x50 | **200** | 2 s | 46.3 mV | 1/1 |
| x4 | x48 | **192** | 2 s | 56.1 mV | 1/1 |
| x8 | x24 | **192** | 2 s | 19.3 mV | 1/1 |
| x8 | x16 | **128** | 17 s | 26.2 mV | 1/1 |
| x2 | x50 | **100** | 2 s | -47.3 mV | 1/1 |
| x2 | x48 | **96** | 2 s | -18.1 mV | 1/1 |
| x4 | x24 | **96** | 2 s | -30.1 mV | 1/1 |
| x2 | x32 | **64** | 2 s | 1.4 mV | 1/1 |
| x4 | x16 | **64** | 19 s | -53.0 mV | 1/1 |
| x1 | x50 | **50** | 2 s | -47.6 mV | 1/1 |
| x2 | x24 | **48** | 2 s | 17.9 mV | 1/1 |
| x1 | x32 | **32** | 2 s | 21.3 mV | 1/1 |
| x2 | x16 | **32** | 34 s | -7.2 mV | 1/1 |
| x1 | x24 | **24** | 2 s | -8.5 mV | 1/1 |
| x1 | x8 | **8** | 58 s | 40.7 mV | 1/1 |
| x4 | x2 | **8** | 56 s | -40.9 mV | 1/1 |
| x1 | x4 | **4** | 2 s | 36.2 mV | 1/1 |
| x2 | x2 | **4** | 2 s | -30.3 mV | 1/1 |
| x4 | x1 | **4** | 2 s | -42.6 mV | 1/1 |
| x1 | x2 | **2** | 2 s | -3.1 mV | 1/1 |
| x2 | x1 | **2** | 2 s | -20.4 mV | 1/1 |
| x1 | x1 | **1** | 2 s | -24.7 mV | 1/1 |

## Pares con al menos un fallo

| PGA | PGAout | ganancia | PASA/visitas | aprendizajes | LPo final | SUM valido | nota |
|---|---|---|---|---|---|---|---|
| x16 | x2 | 32 | 0/1 | 0 | 57.4 mV | 1.7 % | nunca declaro banda |
| x24 | x4 | 96 | 0/1 | 0 | None mV | 0.9 % | nunca declaro banda |
| x48 | x2 | 96 | 0/1 | 0 | -32.5 mV | 100.0 % | nunca declaro banda |
| x32 | x4 | 128 | 0/1 | 0 | -29.8 mV | 6.9 % | nunca declaro banda |
| x24 | x8 | 192 | 0/1 | 1 | -10.5 mV | 5.7 % | entro y se fue |
| x48 | x4 | 192 | 0/1 | 1 | None mV | 3.3 % | entro y se fue |
| x50 | x4 | 200 | 0/1 | 0 | None mV | 2.6 % | entro y se fue |
| x8 | x32 | 256 | 0/1 | 0 | -94.3 mV | 100.0 % | entro y se fue |
| x32 | x8 | 256 | 0/1 | 1 | -47.0 mV | 2.2 % | nunca declaro banda |
| x8 | x48 | 384 | 0/1 | 0 | 93.6 mV | 100.0 % | entro y se fue |
| x24 | x16 | 384 | 0/1 | 1 | 51.7 mV | 10.2 % | entro y se fue |
| x48 | x8 | 384 | 0/1 | 1 | 58.3 mV | 2.2 % | nunca declaro banda |
| x50 | x8 | 400 | 0/1 | 1 | None mV | 0.4 % | entro y se fue |
| x32 | x16 | 512 | 0/1 | 1 | 55.9 mV | 7.0 % | entro y se fue |
| x24 | x24 | 576 | 0/1 | 1 | -67.8 mV | 3.3 % | nunca declaro banda |
| x16 | x48 | 768 | 0/1 | 0 | 23.7 mV | 5.8 % | entro y se fue |
| x24 | x32 | 768 | 0/1 | 1 | 21.6 mV | 4.1 % | entro y se fue |
| x32 | x24 | 768 | 0/1 | 1 | -87.8 mV | 0.9 % | entro y se fue |
| x48 | x16 | 768 | 0/1 | 1 | -19.1 mV | 2.4 % | entro y se fue |
| x16 | x50 | 800 | 0/1 | 1 | 22.9 mV | 4.6 % | entro y se fue |
| x32 | x50 | 1600 | 0/1 | 0 | None mV | 0.9 % | nunca declaro banda |
| x50 | x32 | 1600 | 0/1 | 0 | -34.4 mV | 2.9 % | entro y se fue |
| x48 | x48 | 2304 | 0/1 | 0 | None mV | 0.6 % | nunca declaro banda |
| x48 | x50 | 2400 | 0/1 | 1 | -12.7 mV | 1.1 % | entro y se fue |
| x50 | x48 | 2400 | 0/1 | 1 | None mV | 0.4 % | nunca declaro banda |

## Parametros del controlador

Los que definen el lazo, tal como los reporto el firmware en la ultima visita de cada par. Las pendientes de IDAC2 y del par lento las escala el firmware con la ganancia de PGAout, asi que cambian de par en par.

| PGA | PGAout | FINE_SLOPE_UV | COARSE_SLOPE_UV | SLOW0_SLOPE_UV | SLOW1_SLOPE_UV | OPA_TARGET_UV | RESCUE_STEP | RESCUE_MS | COARSE_MS | FINE_MID | HOLD_UV | DEADBAND_UV | SUM_BAND_UV | SLOW_TAU_MS |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| x1 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x1 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x1 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x2 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x2 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x4 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x4 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x8 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x8 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x16 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x16 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x24 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x24 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x32 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x32 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x48 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x48 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |
| x50 | x50 | 15000 | -150000 | 600 | 400 | 0 | 2 | 60000 | 45000 | 240 | 25000 | 45000 | 60000 | 43700 |

## Detalle por par


### x1 / x1 — ganancia 1

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -26.6 | -24.7 | 1.1 | 7 | 7 | 1 | -89 | 0 | REGULANDO 31s |

Taps en la ultima visita: SEo -8.2 mV (100.0 % valido), BP -7.8 mV (100.0 % valido), OPAs -11.5 mV (100.0 % valido), SUM -11.6 mV (100.0 % valido), LP -24.7 mV (100.0 % valido).

### x1 / x2 — ganancia 2

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -24.7 | -3.1 | 22.0 | 7 | 7 | 1 | -89 | 0 | REGULANDO 31s |

Taps en la ultima visita: SEo -7.2 mV (100.0 % valido), BP -7.0 mV (100.0 % valido), OPAs -10.6 mV (100.0 % valido), SUM -14.8 mV (100.0 % valido), LP -3.1 mV (100.0 % valido).

### x2 / x1 — ganancia 2

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -47.6 | -20.4 | 5.3 | 0 | 0 | 0 | 0 | 1 | APRENDIENDO 31s, REGULANDO 2s |

Taps en la ultima visita: SEo -9.4 mV (100.0 % valido), BP -8.5 mV (100.0 % valido), OPAs -6.1 mV (100.0 % valido), SUM -6.2 mV (100.0 % valido), LP -20.4 mV (100.0 % valido).

### x1 / x4 — ganancia 4

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -3.1 | 36.2 | 2.8 | 7 | 7 | 1 | -96 | 0 | REGULANDO 31s |

Taps en la ultima visita: SEo -7.3 mV (100.0 % valido), BP -7.0 mV (100.0 % valido), OPAs -10.7 mV (100.0 % valido), SUM -23.4 mV (100.0 % valido), LP 36.2 mV (100.0 % valido).

### x2 / x2 — ganancia 4

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -20.4 | -30.3 | 9.9 | 0 | 0 | 0 | 0 | 0 | APRENDIENDO 31s |

Taps en la ultima visita: SEo -10.3 mV (100.0 % valido), BP -9.5 mV (100.0 % valido), OPAs -6.6 mV (100.0 % valido), SUM -5.4 mV (100.0 % valido), LP -30.3 mV (100.0 % valido).

### x4 / x1 — ganancia 4

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -47.3 | -42.6 | 18.8 | 0 | 0 | 0 | 0 | 1 | APRENDIENDO 29s, REGULANDO 2s |

Taps en la ultima visita: SEo -10.9 mV (100.0 % valido), BP -8.0 mV (100.0 % valido), OPAs -2.1 mV (100.0 % valido), SUM -2.3 mV (100.0 % valido), LP -42.6 mV (100.0 % valido).

### x1 / x8 — ganancia 8

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 58 s | 85 s | 36.2 | 40.7 | 26.1 | 7 | 7 | 2 | -255 | 0 | REGULANDO 102s |

Taps en la ultima visita: SEo -7.5 mV (100.0 % valido), BP -7.2 mV (100.0 % valido), OPAs -10.3 mV (100.0 % valido), SUM -36.0 mV (100.0 % valido), LP 40.7 mV (49.0 % valido).

### x2 / x4 — ganancia 8

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 148 s | 208 s | -30.3 | -61.0 | 2.6 | 0 | 0 | 7 | 253 | 0 | APRENDIENDO 208s |

Taps en la ultima visita: SEo -11.9 mV (100.0 % valido), BP -11.1 mV (100.0 % valido), OPAs -3.2 mV (100.0 % valido), SUM 14.7 mV (100.0 % valido), LP -61.0 mV (37.0 % valido).

### x4 / x2 — ganancia 8

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 56 s | 69 s | -42.6 | -40.9 | 2.4 | 0 | 0 | 0 | 197 | 0 | REGULANDO 100s |

Taps en la ultima visita: SEo -15.0 mV (100.0 % valido), BP -12.0 mV (100.0 % valido), OPAs -1.2 mV (100.0 % valido), SUM 7.6 mV (100.0 % valido), LP -40.9 mV (45.8 % valido).

### x8 / x1 — ganancia 8

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 94 s | 127 s | 46.3 | -46.5 | 4.3 | 0 | 0 | -9 | 97 | 0 | APRENDIENDO 121s, REGULANDO 6s |

Correccion medida del modelo del par lento: **0.27x**.

Taps en la ultima visita: SEo -13.8 mV (100.0 % valido), BP -8.3 mV (100.0 % valido), OPAs 5.5 mV (100.0 % valido), SUM 5.4 mV (100.0 % valido), LP -46.5 mV (27.9 % valido).

### x1 / x16 — ganancia 16

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 81 s | 154 s | 40.7 | 10.2 | 4.4 | 7 | 7 | 6 | -241 | 0 | REGULANDO 182s |

Taps en la ultima visita: SEo -8.3 mV (100.0 % valido), BP -8.0 mV (100.0 % valido), OPAs -8.6 mV (100.0 % valido), SUM -29.0 mV (100.0 % valido), LP 10.2 mV (65.1 % valido).

### x2 / x8 — ganancia 16

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 188 s | 242 s | -61.0 | -58.4 | 4.9 | 0 | 0 | 2 | 240 | 0 | APRENDIENDO 210s, REGULANDO 31s |

Taps en la ultima visita: SEo -10.8 mV (100.0 % valido), BP -10.0 mV (100.0 % valido), OPAs -5.5 mV (100.0 % valido), SUM 14.8 mV (100.0 % valido), LP -58.4 mV (23.3 % valido).

### x4 / x4 — ganancia 16

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 229 s | 250 s | -40.9 | -40.9 | 8.9 | 1 | 1 | -3 | 252 | 1 | APRENDIENDO 110s, REGULANDO 148s |

Taps en la ultima visita: SEo -13.4 mV (100.0 % valido), BP -10.9 mV (100.0 % valido), OPAs -3.6 mV (100.0 % valido), SUM 12.8 mV (100.0 % valido), LP -40.9 mV (13.7 % valido).

### x8 / x2 — ganancia 16

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 290 s | 302 s | -46.5 | 58.5 | 26.3 | 7 | 5 | -13 | 251 | 1 | APRENDIENDO 175s, REGULANDO 193s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -11.9 mV (100.0 % valido), BP -9.8 mV (100.0 % valido), OPAs -6.9 mV (100.0 % valido), SUM -5.2 mV (100.0 % valido), LP 58.5 mV (22.2 % valido).

### x16 / x1 — ganancia 16

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 94 s | 2 s | None | 55.1 | 17.5 | 20 | 13 | -6 | -255 | 0 | APRENDIENDO 122s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -1.9 mV (100.0 % valido), BP -8.5 mV (100.0 % valido), OPAs -41.6 mV (100.0 % valido), SUM -41.2 mV (98.3 % valido), LP 55.1 mV (67.8 % valido).

### x1 / x24 — ganancia 24

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | 10.2 | -8.5 | 18.0 | 7 | 7 | 7 | -231 | 0 | REGULANDO 31s |

Taps en la ultima visita: SEo -8.3 mV (100.0 % valido), BP -8.1 mV (100.0 % valido), OPAs -8.0 mV (100.0 % valido), SUM -24.0 mV (100.0 % valido), LP -8.5 mV (100.0 % valido).

### x24 / x1 — ganancia 24

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 158 s | 118 s | None | -57.8 | 28.3 | 12 | 6 | -10 | -170 | 1 | APRENDIENDO 183s, REGULANDO 4s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -10.3 mV (100.0 % valido), BP -8.3 mV (100.0 % valido), OPAs -12.5 mV (100.0 % valido), SUM -12.6 mV (97.8 % valido), LP -57.8 mV (30.0 % valido).

### x1 / x32 — ganancia 32

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -8.5 | 21.3 | 9.2 | 7 | 7 | 7 | -231 | 0 | REGULANDO 33s |

Taps en la ultima visita: SEo -8.4 mV (100.0 % valido), BP -8.1 mV (100.0 % valido), OPAs -8.1 mV (100.0 % valido), SUM -30.9 mV (100.0 % valido), LP 21.3 mV (100.0 % valido).

### x2 / x16 — ganancia 32

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 34 s | 77 s | -58.4 | -7.2 | 5.2 | 0 | 0 | -1 | 245 | 0 | REGULANDO 106s |

Taps en la ultima visita: SEo -10.2 mV (100.0 % valido), BP -9.4 mV (100.0 % valido), OPAs -7.0 mV (100.0 % valido), SUM 7.4 mV (100.0 % valido), LP -7.2 mV (74.5 % valido).

### x4 / x8 — ganancia 32

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 214 s | 231 s | -40.9 | -29.6 | 20.3 | 2 | 1 | -6 | 249 | 1 | APRENDIENDO 146s, REGULANDO 106s |

Correccion medida del modelo del par lento: **0.27x**.

Taps en la ultima visita: SEo -11.9 mV (100.0 % valido), BP -9.9 mV (100.0 % valido), OPAs -5.9 mV (100.0 % valido), SUM 11.5 mV (100.0 % valido), LP -29.6 mV (17.4 % valido).

### x8 / x4 — ganancia 32

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 62 s | 102 s | 58.5 | 44.1 | 21.6 | 7 | 5 | -13 | -69 | 0 | REGULANDO 118s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -9.4 mV (100.0 % valido), BP -7.3 mV (100.0 % valido), OPAs -10.7 mV (100.0 % valido), SUM -22.9 mV (100.0 % valido), LP 44.1 mV (75.4 % valido).

### x16 / x2 — ganancia 32

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | 55.1 | 57.4 | 0.0 | 7 | 5 | -6 | -255 | 0 | APRENDIENDO 217s, REGULANDO 25s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo 26.6 mV (100.0 % valido), BP 13.9 mV (100.0 % valido), OPAs -134.7 mV (8.7 % valido), SUM -239.0 mV (1.7 % valido), LP 131.4 mV (1.7 % valido).

### x32 / x1 — ganancia 32

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 173 s | 58 s | None | -9.0 | 26.8 | 12 | 6 | 0 | -1 | 0 | APRENDIENDO 192s, REGULANDO 35s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -10.5 mV (100.0 % valido), BP -7.6 mV (100.0 % valido), OPAs -8.7 mV (82.4 % valido), SUM -8.8 mV (82.4 % valido), LP -9.0 mV (31.5 % valido).

### x1 / x48 — ganancia 48

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 77 s | 154 s | 21.3 | -60.1 | 27.0 | 7 | 7 | 8 | -161 | 0 | REGULANDO 156s |

Taps en la ultima visita: SEo -8.7 mV (100.0 % valido), BP -8.4 mV (100.0 % valido), OPAs -7.8 mV (100.0 % valido), SUM -12.9 mV (100.0 % valido), LP -60.1 mV (77.3 % valido).

### x2 / x24 — ganancia 48

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 4 s | -7.2 | 17.9 | 7.6 | 0 | 0 | -2 | 235 | 0 | REGULANDO 37s |

Taps en la ultima visita: SEo -10.2 mV (100.0 % valido), BP -9.4 mV (100.0 % valido), OPAs -7.6 mV (100.0 % valido), SUM 2.3 mV (100.0 % valido), LP 17.9 mV (100.0 % valido).

### x24 / x2 — ganancia 48

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 2 s | -57.8 | 15.1 | 99.8 | 12 | 6 | -17 | 65 | 1 | APRENDIENDO 800s, REGULANDO 160s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -60.7 mV (100.0 % valido), BP -26.8 mV (100.0 % valido), OPAs 79.6 mV (83.7 % valido), SUM 91.2 mV (74.8 % valido), LP -282.5 mV (3.5 % valido).

### x48 / x1 — ganancia 48

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 719 s | 73 s | None | -32.7 | 1.5 | 11 | 7 | -3 | 132 | 1 | APRENDIENDO 744s, REGULANDO 4s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo -13.0 mV (100.0 % valido), BP -6.9 mV (99.2 % valido), OPAs 5.7 mV (49.2 % valido), SUM 5.8 mV (48.6 % valido), LP -32.7 mV (8.9 % valido).

### x1 / x50 — ganancia 50

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -60.1 | -47.6 | 10.0 | 7 | 7 | 8 | -150 | 0 | REGULANDO 30s |

Taps en la ultima visita: SEo -8.7 mV (100.0 % valido), BP -8.4 mV (100.0 % valido), OPAs -7.8 mV (100.0 % valido), SUM -13.5 mV (100.0 % valido), LP -47.6 mV (100.0 % valido).

### x50 / x1 — ganancia 50

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 925 s | 21 s | None | -58.0 | 2.8 | 12 | 7 | -1 | -43 | 1 | APRENDIENDO 936s, REGULANDO 18s |

Objetivo de SUMo bisecado: **-8.3 mV**.

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo -10.0 mV (100.0 % valido), BP -6.8 mV (100.0 % valido), OPAs -3.5 mV (82.7 % valido), SUM -3.5 mV (82.7 % valido), LP -58.0 mV (6.6 % valido).

### x2 / x32 — ganancia 64

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | 17.9 | 1.4 | 18.2 | 0 | 0 | -2 | 235 | 0 | REGULANDO 31s |

Taps en la ultima visita: SEo -10.2 mV (100.0 % valido), BP -9.5 mV (100.0 % valido), OPAs -7.6 mV (100.0 % valido), SUM 3.9 mV (100.0 % valido), LP 1.4 mV (100.0 % valido).

### x4 / x16 — ganancia 64

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 19 s | 50 s | -29.6 | -53.0 | 18.4 | 2 | 1 | -7 | 244 | 0 | REGULANDO 52s |

Correccion medida del modelo del par lento: **0.27x**.

Taps en la ultima visita: SEo -11.5 mV (100.0 % valido), BP -9.4 mV (100.0 % valido), OPAs -6.7 mV (100.0 % valido), SUM 14.0 mV (100.0 % valido), LP -53.0 mV (76.0 % valido).

### x8 / x8 — ganancia 64

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 73 s | 131 s | 44.1 | 52.8 | 6.6 | 7 | 5 | -12 | -252 | 0 | REGULANDO 131s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -9.2 mV (100.0 % valido), BP -7.3 mV (100.0 % valido), OPAs -10.6 mV (100.0 % valido), SUM -39.2 mV (100.0 % valido), LP 52.8 mV (46.0 % valido).

### x16 / x4 — ganancia 64

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 83 s | None | -14.6 | 132.5 | 9 | 8 | 0 | 0 | 1 | APRENDIENDO 899s, REGULANDO 62s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo 8.8 mV (100.0 % valido), BP 1.9 mV (100.0 % valido), OPAs -39.5 mV (98.7 % valido), SUM -248.5 mV (26.5 % valido), LP 121.6 mV (4.8 % valido).

### x32 / x2 — ganancia 64

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 2 s | -9.0 | -91.6 | 71.1 | 13 | 7 | -15 | 255 | 1 | APRENDIENDO 755s, REGULANDO 206s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -76.7 mV (95.2 % valido), BP -25.8 mV (100.0 % valido), OPAs 92.9 mV (100.0 % valido), SUM 91.5 mV (100.0 % valido), LP -281.9 mV (4.4 % valido).

### x2 / x48 — ganancia 96

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | 1.4 | -18.1 | 13.7 | 0 | 0 | -2 | 238 | 0 | REGULANDO 31s |

Taps en la ultima visita: SEo -10.6 mV (100.0 % valido), BP -9.9 mV (100.0 % valido), OPAs -7.9 mV (100.0 % valido), SUM 8.4 mV (100.0 % valido), LP -18.1 mV (100.0 % valido).

### x4 / x24 — ganancia 96

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -53.0 | -30.1 | 15.3 | 2 | 1 | -8 | 237 | 0 | REGULANDO 31s |

Correccion medida del modelo del par lento: **0.27x**.

Taps en la ultima visita: SEo -11.6 mV (100.0 % valido), BP -9.7 mV (100.0 % valido), OPAs -7.4 mV (100.0 % valido), SUM 9.0 mV (100.0 % valido), LP -30.1 mV (100.0 % valido).

### x24 / x4 — ganancia 96

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | None | None | 12 | 6 | -9 | -127 | 0 | APRENDIENDO 408s, REGULANDO 73s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -34.4 mV (100.0 % valido), BP -18.6 mV (100.0 % valido), OPAs 39.9 mV (100.0 % valido), SUM 100.7 mV (0.9 % valido), LP -273.1 mV (0.0 % valido).

### x48 / x2 — ganancia 96

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | -32.7 | -32.5 | 0.0 | 26 | 14 | -10 | 255 | 0 | APRENDIENDO 456s, REGULANDO 25s |

Objetivo de SUMo bisecado: **-9.5 mV**.

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo -54.2 mV (63.9 % valido), BP -26.2 mV (100.0 % valido), OPAs 59.9 mV (100.0 % valido), SUM 91.3 mV (100.0 % valido), LP -281.9 mV (0.9 % valido).

### x2 / x50 — ganancia 100

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 2 s | -18.1 | -47.3 | 27.9 | 0 | 0 | -2 | 245 | 0 | REGULANDO 30s |

Taps en la ultima visita: SEo -10.6 mV (100.0 % valido), BP -9.8 mV (100.0 % valido), OPAs -7.9 mV (100.0 % valido), SUM 9.4 mV (100.0 % valido), LP -47.3 mV (100.0 % valido).

### x50 / x2 — ganancia 100

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | -58.0 | None | None | 13 | 7 | -17 | 255 | 1 | APRENDIENDO 769s, REGULANDO 192s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo -118.4 mV (2.6 % valido), BP -26.0 mV (100.0 % valido), OPAs 93.3 mV (100.0 % valido), SUM 91.9 mV (100.0 % valido), LP -281.4 mV (0.0 % valido).

### x4 / x32 — ganancia 128

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 21 s | -30.1 | 65.2 | 18.0 | 2 | 1 | -9 | 222 | 0 | REGULANDO 62s |

Correccion medida del modelo del par lento: **0.27x**.

Taps en la ultima visita: SEo -11.1 mV (100.0 % valido), BP -9.3 mV (100.0 % valido), OPAs -7.8 mV (100.0 % valido), SUM -6.8 mV (100.0 % valido), LP 65.2 mV (100.0 % valido).

### x8 / x16 — ganancia 128

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 17 s | 35 s | 52.8 | 26.2 | 30.0 | 7 | 5 | -10 | -255 | 0 | REGULANDO 62s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -10.7 mV (100.0 % valido), BP -8.2 mV (100.0 % valido), OPAs -8.8 mV (100.0 % valido), SUM -32.6 mV (100.0 % valido), LP 26.2 mV (86.2 % valido).

### x16 / x8 — ganancia 128

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 89 s | None | -25.8 | 137.5 | 10 | 9 | 0 | 0 | 1 | APRENDIENDO 829s, REGULANDO 131s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -21.5 mV (100.0 % valido), BP -12.5 mV (100.0 % valido), OPAs 10.2 mV (100.0 % valido), SUM 105.6 mV (27.5 % valido), LP -268.6 mV (5.8 % valido).

### x32 / x4 — ganancia 128

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | -29.8 | 0.0 | 12 | 6 | -2 | 253 | 0 | APRENDIENDO 452s, REGULANDO 30s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo 19.6 mV (100.0 % valido), BP 2.2 mV (100.0 % valido), OPAs -151.2 mV (36.8 % valido), SUM -248.3 mV (6.9 % valido), LP 121.6 mV (1.3 % valido).

### x4 / x48 — ganancia 192

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 67 s | 65.2 | 56.1 | 24.7 | 2 | 1 | -9 | 156 | 0 | REGULANDO 67s |

Correccion medida del modelo del par lento: **0.27x**.

Taps en la ultima visita: SEo -11.0 mV (100.0 % valido), BP -9.1 mV (100.0 % valido), OPAs -7.8 mV (100.0 % valido), SUM -8.6 mV (100.0 % valido), LP 56.1 mV (100.0 % valido).

### x8 / x24 — ganancia 192

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 4 s | 26.2 | 19.3 | 8.9 | 7 | 5 | -9 | -249 | 0 | REGULANDO 38s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -10.5 mV (100.0 % valido), BP -8.3 mV (100.0 % valido), OPAs -8.3 mV (100.0 % valido), SUM -32.8 mV (100.0 % valido), LP 19.3 mV (100.0 % valido).

### x24 / x8 — ganancia 192

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 830 s | None | -10.5 | 0.0 | 12 | 6 | -8 | -113 | 1 | APRENDIENDO 841s, REGULANDO 120s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo 1.9 mV (100.0 % valido), BP -4.3 mV (100.0 % valido), OPAs -39.8 mV (72.3 % valido), SUM -253.3 mV (5.7 % valido), LP 116.6 mV (0.9 % valido).

### x48 / x4 — ganancia 192

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 222 s | None | None | None | 26 | 14 | -9 | 221 | 1 | APRENDIENDO 766s, REGULANDO 196s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo -8.9 mV (28.5 % valido), BP -35.0 mV (99.6 % valido), OPAs 9.3 mV (12.0 % valido), SUM 76.5 mV (3.3 % valido), LP -270.1 mV (0.0 % valido).

### x4 / x50 — ganancia 200

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | PASA | 2 s | 15 s | 56.1 | 46.3 | 8.8 | 2 | 1 | -9 | 83 | 0 | REGULANDO 31s |

Correccion medida del modelo del par lento: **0.27x**.

Taps en la ultima visita: SEo -10.9 mV (100.0 % valido), BP -9.2 mV (100.0 % valido), OPAs -7.8 mV (100.0 % valido), SUM -13.2 mV (100.0 % valido), LP 46.3 mV (100.0 % valido).

### x50 / x4 — ganancia 200

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 162 s | None | None | None | 12 | 7 | -4 | 253 | 0 | APRENDIENDO 435s, REGULANDO 46s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo 29.9 mV (99.6 % valido), BP -2.7 mV (97.8 % valido), OPAs -224.0 mV (26.5 % valido), SUM -248.2 mV (2.6 % valido), LP 121.5 mV (0.0 % valido).

### x8 / x32 — ganancia 256

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 4 s | 19.3 | -94.3 | 158.9 | 7 | 5 | -8 | -216 | 0 | REGULANDO 241s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -11.1 mV (100.0 % valido), BP -8.7 mV (100.0 % valido), OPAs -7.8 mV (100.0 % valido), SUM -11.9 mV (100.0 % valido), LP -180.3 mV (12.1 % valido).

### x16 / x16 — ganancia 256

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 316 s | None | 26.7 | 47.6 | 9 | 8 | 0 | 0 | 1 | APRENDIENDO 848s, REGULANDO 113s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -7.6 mV (100.0 % valido), BP -4.4 mV (100.0 % valido), OPAs -12.8 mV (100.0 % valido), SUM -218.7 mV (15.2 % valido), LP 113.8 mV (2.0 % valido).

### x32 / x8 — ganancia 256

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | -47.0 | 141.8 | 12 | 6 | -2 | 127 | 1 | APRENDIENDO 790s, REGULANDO 173s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -24.6 mV (95.0 % valido), BP -11.7 mV (100.0 % valido), OPAs 25.3 mV (60.7 % valido), SUM 105.8 mV (2.2 % valido), LP -268.1 mV (0.9 % valido).

### x8 / x48 — ganancia 384

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 77 s | None | 93.6 | 158.9 | 7 | 5 | -10 | 215 | 0 | REGULANDO 242s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -10.6 mV (100.0 % valido), BP -8.6 mV (100.0 % valido), OPAs -7.8 mV (100.0 % valido), SUM -30.7 mV (100.0 % valido), LP 112.3 mV (50.4 % valido).

### x16 / x24 — ganancia 384

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 10 s | None | 1.0 | 69.1 | 8 | 7 | 0 | 0 | 1 | APRENDIENDO 872s, REGULANDO 90s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -9.2 mV (100.0 % valido), BP -4.4 mV (100.0 % valido), OPAs -9.7 mV (99.3 % valido), SUM -182.8 mV (5.6 % valido), LP 114.2 mV (0.9 % valido).

### x24 / x16 — ganancia 384

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 262 s | None | 51.7 | 0.0 | 12 | 6 | -6 | -143 | 1 | APRENDIENDO 918s, REGULANDO 44s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -3.6 mV (100.0 % valido), BP -6.6 mV (100.0 % valido), OPAs -23.8 mV (94.8 % valido), SUM -255.7 mV (10.2 % valido), LP 114.2 mV (1.1 % valido).

### x48 / x8 — ganancia 384

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | 58.3 | 0.0 | 26 | 14 | -7 | -129 | 1 | APRENDIENDO 810s, REGULANDO 150s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo 41.8 mV (94.8 % valido), BP -37.8 mV (98.9 % valido), OPAs -158.0 mV (30.8 % valido), SUM -253.1 mV (2.2 % valido), LP 116.5 mV (0.7 % valido).

### x8 / x50 — ganancia 400

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 565 s | None | 28.9 | 0.0 | 15 | 15 | 0 | 0 | 1 | APRENDIENDO 814s, REGULANDO 148s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -3.2 mV (100.0 % valido), BP -5.9 mV (100.0 % valido), OPAs -18.8 mV (100.0 % valido), SUM -255.0 mV (10.9 % valido), LP 114.8 mV (0.7 % valido).

### x50 / x8 — ganancia 400

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 87 s | None | None | None | 12 | 7 | -4 | 191 | 1 | APRENDIENDO 793s, REGULANDO 169s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo -31.5 mV (94.1 % valido), BP -11.1 mV (98.9 % valido), OPAs 44.8 mV (35.4 % valido), SUM 105.8 mV (0.4 % valido), LP -267.9 mV (0.0 % valido).

### x16 / x32 — ganancia 512

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 327 s | None | -20.1 | 124.9 | 9 | 8 | 0 | 0 | 1 | APRENDIENDO 802s, REGULANDO 159s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -7.0 mV (100.0 % valido), BP -4.8 mV (100.0 % valido), OPAs -12.0 mV (100.0 % valido), SUM -255.6 mV (7.8 % valido), LP 114.1 mV (2.2 % valido).

### x32 / x16 — ganancia 512

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 252 s | None | 55.9 | 52.3 | 12 | 6 | -1 | 137 | 1 | APRENDIENDO 871s, REGULANDO 90s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -3.2 mV (100.0 % valido), BP -5.7 mV (100.0 % valido), OPAs -23.4 mV (91.5 % valido), SUM -255.3 mV (7.0 % valido), LP 114.3 mV (3.1 % valido).

### x24 / x24 — ganancia 576

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | -67.8 | 0.0 | 12 | 6 | -1 | -255 | 1 | APRENDIENDO 808s, REGULANDO 152s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -2.5 mV (100.0 % valido), BP -6.3 mV (100.0 % valido), OPAs -24.1 mV (78.3 % valido), SUM -254.8 mV (3.3 % valido), LP 114.9 mV (0.7 % valido).

### x16 / x48 — ganancia 768

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 62 s | None | 23.7 | 50.9 | 7 | 5 | -10 | -235 | 0 | APRENDIENDO 543s, REGULANDO 179s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -20.5 mV (100.0 % valido), BP -11.0 mV (100.0 % valido), OPAs 10.8 mV (100.0 % valido), SUM 107.0 mV (5.8 % valido), LP -267.2 mV (1.4 % valido).

### x24 / x32 — ganancia 768

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 383 s | None | 21.6 | 0.0 | 12 | 6 | -2 | -247 | 1 | APRENDIENDO 858s, REGULANDO 102s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -16.7 mV (100.0 % valido), BP -10.3 mV (100.0 % valido), OPAs 3.7 mV (94.8 % valido), SUM 107.8 mV (4.1 % valido), LP -266.2 mV (0.7 % valido).

### x32 / x24 — ganancia 768

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 62 s | None | -87.8 | 104.2 | 12 | 6 | -2 | 119 | 1 | APRENDIENDO 789s, REGULANDO 172s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -19.8 mV (100.0 % valido), BP -11.3 mV (100.0 % valido), OPAs 13.4 mV (66.1 % valido), SUM 107.1 mV (0.9 % valido), LP -266.9 mV (1.3 % valido).

### x48 / x16 — ganancia 768

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 877 s | None | -19.1 | 0.0 | 26 | 14 | -2 | -255 | 1 | APRENDIENDO 808s, REGULANDO 152s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo 31.0 mV (93.7 % valido), BP -13.7 mV (98.9 % valido), OPAs -261.4 mV (36.2 % valido), SUM -255.5 mV (2.4 % valido), LP 113.9 mV (0.4 % valido).

### x16 / x50 — ganancia 800

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 376 s | None | 22.9 | 0.0 | 7 | 5 | -10 | -233 | 1 | APRENDIENDO 826s, REGULANDO 135s |

Correccion medida del modelo del par lento: **0.55x**.

Taps en la ultima visita: SEo -20.2 mV (100.0 % valido), BP -9.6 mV (100.0 % valido), OPAs 5.4 mV (100.0 % valido), SUM 107.1 mV (4.6 % valido), LP -267.1 mV (0.7 % valido).

### x50 / x16 — ganancia 800

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | None | None | 0 | 0 | 0 | 0 | 2 | APRENDIENDO 824s, REGULANDO 137s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo -52.9 mV (94.3 % valido), BP 9.3 mV (98.9 % valido), OPAs 68.4 mV (47.8 % valido), SUM 108.7 mV (2.4 % valido), LP -265.0 mV (0.0 % valido).

### x32 / x32 — ganancia 1024

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | None | None | 0 | 0 | 0 | 0 | 1 | APRENDIENDO 839s, REGULANDO 121s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -37.3 mV (100.0 % valido), BP -3.5 mV (100.0 % valido), OPAs 62.8 mV (69.3 % valido), SUM 108.2 mV (0.9 % valido), LP -265.8 mV (0.0 % valido).

### x24 / x48 — ganancia 1152

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | None | None | 0 | 0 | 0 | 0 | 2 | APRENDIENDO 861s, REGULANDO 102s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -32.4 mV (100.0 % valido), BP -6.1 mV (100.0 % valido), OPAs 49.4 mV (78.0 % valido), SUM 107.2 mV (1.3 % valido), LP -266.8 mV (0.0 % valido).

### x48 / x24 — ganancia 1152

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | 64 s | None | None | None | 0 | 0 | 0 | 0 | 2 | APRENDIENDO 837s, REGULANDO 123s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo -58.9 mV (94.8 % valido), BP 22.8 mV (99.3 % valido), OPAs 23.8 mV (33.8 % valido), SUM 107.6 mV (0.9 % valido), LP -266.2 mV (0.0 % valido).

### x24 / x50 — ganancia 1200

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | -33.5 | 133.6 | 3 | 3 | 0 | 0 | 1 | APRENDIENDO 869s, REGULANDO 92s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -29.1 mV (100.0 % valido), BP -12.6 mV (100.0 % valido), OPAs 56.5 mV (79.6 % valido), SUM 107.3 mV (1.1 % valido), LP -266.7 mV (1.8 % valido).

### x50 / x24 — ganancia 1200

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | None | None | 1 | 1 | 0 | 0 | 1 | APRENDIENDO 839s, REGULANDO 121s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo -58.9 mV (93.7 % valido), BP -9.7 mV (99.3 % valido), OPAs 108.9 mV (40.2 % valido), SUM 107.6 mV (0.0 % valido), LP -266.2 mV (0.0 % valido).

### x32 / x48 — ganancia 1536

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | None | None | 3 | 3 | 0 | 0 | 1 | APRENDIENDO 844s, REGULANDO 117s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -36.3 mV (100.0 % valido), BP -13.0 mV (100.0 % valido), OPAs 82.8 mV (66.6 % valido), SUM 107.4 mV (0.0 % valido), LP -266.4 mV (0.0 % valido).

### x48 / x32 — ganancia 1536

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | -93.5 | 0.0 | 1 | 1 | 0 | 0 | 1 | APRENDIENDO 871s, REGULANDO 89s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo -50.7 mV (93.7 % valido), BP -5.2 mV (99.3 % valido), OPAs 107.1 mV (40.2 % valido), SUM 108.3 mV (2.4 % valido), LP -265.7 mV (0.4 % valido).

### x32 / x50 — ganancia 1600

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | None | None | 12 | 6 | -3 | 121 | 0 | APRENDIENDO 678s, REGULANDO 44s |

Correccion medida del modelo del par lento: **1.28x**.

Taps en la ultima visita: SEo -20.2 mV (100.0 % valido), BP -9.1 mV (100.0 % valido), OPAs 9.0 mV (55.4 % valido), SUM 107.3 mV (0.9 % valido), LP -266.6 mV (0.0 % valido).

### x50 / x32 — ganancia 1600

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 417 s | None | -34.4 | 0.0 | 12 | 7 | -4 | 197 | 0 | APRENDIENDO 708s, REGULANDO 14s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo 0.0 mV (92.5 % valido), BP -6.0 mV (99.4 % valido), OPAs -32.8 mV (37.9 % valido), SUM -255.4 mV (2.9 % valido), LP 114.2 mV (0.9 % valido).

### x48 / x48 — ganancia 2304

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | None | None | 26 | 14 | 0 | -249 | 0 | APRENDIENDO 696s, REGULANDO 25s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo 33.9 mV (92.5 % valido), BP -33.1 mV (99.1 % valido), OPAs -123.3 mV (36.8 % valido), SUM -254.7 mV (0.6 % valido), LP 114.8 mV (0.0 % valido).

### x48 / x50 — ganancia 2400

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | 304 s | None | -12.7 | 0.0 | 26 | 14 | 3 | -233 | 1 | APRENDIENDO 796s, REGULANDO 166s |

Correccion medida del modelo del par lento: **1.16x**.

Taps en la ultima visita: SEo 35.5 mV (94.3 % valido), BP -6.8 mV (100.0 % valido), OPAs -260.7 mV (32.1 % valido), SUM -254.9 mV (1.1 % valido), LP 114.6 mV (0.7 % valido).

### x50 / x48 — ganancia 2400

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | FALLA | — | — | None | None | None | 12 | 7 | -3 | -57 | 1 | APRENDIENDO 798s, REGULANDO 162s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo -24.8 mV (94.1 % valido), BP -9.4 mV (99.6 % valido), OPAs 26.2 mV (45.9 % valido), SUM 107.4 mV (0.4 % valido), LP -266.4 mV (0.0 % valido).

### x50 / x50 — ganancia 2500

| vuelta | veredicto | estable | 1er cruce | LPo ini | LPo fin | pp | I0 | I1 | I2 | I3 | aprendizajes | tiempo por estado |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | APRENDIENDO | — | — | None | None | None | 0 | 0 | 0 | 0 | 2 | APRENDIENDO 797s, REGULANDO 164s |

Correccion medida del modelo del par lento: **2.67x**.

Taps en la ultima visita: SEo -58.7 mV (94.1 % valido), BP 9.4 mV (98.9 % valido), OPAs 74.7 mV (46.6 % valido), SUM 107.6 mV (0.0 % valido), LP -266.3 mV (0.0 % valido).
