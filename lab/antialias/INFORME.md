# Antialias antes de la decimación por software del PSoC

Reemplaza la media móvil de N muestras (`aa_decim.h`, incluido desde `main.c`).

**Diseño:** sinc con ventana Kaiser, 60 dB, fase lineal. Banda útil hasta
0,8 × Nyquist nuevo (0,4/N ciclos/muestra). Rechaza todo lo que se pliega sobre
esa banda al decimar: desde fs_nueva − 0,8 × Nyquist nuevo (0,6/N). El largo es
L ≈ 18·N + 1 taps, impar, con tope de 511. Los coeficientes se calculan en el PSoC
cuando cambia N, en flotante por software. La ISR hace el producto en q15 con
acumulador de 64 bits, una salida cada N entradas. El retardo es constante,
(L−1)/2 muestras de entrada, e igual en todos los nodos: no altera la fase
relativa entre geófonos que usa MASW.

**Medido sobre los coeficientes que genera el código del PSoC** (compilado en la
PC con `host/aa_host.c`):

| N | L | Ganancia DC | Rizo 0–0,8 Ny | Peor alias | Media móvil (antes) | Rizo 1–100 Hz |
|---|---:|---:|---:|---:|---:|---:|
| 2 | 37 | 1,000000 | 0,020 dB | −57,5 dB | −4,6 dB | 0,005 dB |
| 3 | 55 | 1,000000 | 0,019 dB | −58,6 dB | −5,4 dB | 0,006 dB |
| 4 | 73 | 1,000000 | 0,020 dB | −58,9 dB | −5,6 dB | 0,007 dB |
| 5 | 93 | 1,000000 | 0,015 dB | −61,6 dB | −5,7 dB | 0,007 dB |
| 6 | 111 | 1,000000 | 0,016 dB | −58,7 dB | −5,8 dB | 0,010 dB |
| 8 | 147 | 1,000000 | 0,014 dB | −56,9 dB | −5,9 dB | 0,012 dB |
| 10 | 183 | 1,000000 | 0,015 dB | −58,4 dB | −5,9 dB | 0,015 dB |
| 13 | 237 | 1,000000 | 0,017 dB | −56,8 dB | −5,9 dB | 0,017 dB |
| 16 | 291 | 1,000000 | 0,016 dB | −57,2 dB | −5,9 dB | 0,016 dB |
| 20 | 363 | 1,000000 | 0,018 dB | −57,5 dB | −5,9 dB | 0,018 dB |
| 28 | 509 | 1,000000 | 0,018 dB | −58,4 dB | −5,9 dB | 0,018 dB |

La media móvil dejaba pasar a −5/−6 dB lo que se pliega sobre la banda útil:
no protegía contra aliasing. Con N mayor que 28 se alcanza el tope de 511 taps y
la atenuación baja.

**Costo:** L productos de 64 bits por salida, por ejemplo 183 para N=10 cada
3,8 ms. Es menos del 1 % del Cortex-M3.

**Pendiente en placa:** medir el tiempo de la ISR con N=28 y comparar una
captura decimada contra la misma decimada offline.
