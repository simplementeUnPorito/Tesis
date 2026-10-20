# Piso de ruido con entrada en corto

Rieles ADC inferidos: -131072 a 131071 cuentas (18 bits). Conversión: 19.92 µV/cuenta.

| tap | PGA | PGAout | usadas | saturadas | media [cuentas] | std [µV] | RMS AC [µV] | p2p AC [µV] |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 4 | 4 | 0 | 5.181e+04 | 149.1 | 38.02 | 458.2 |
| 0 | 1 | 4 | 4 | 0 | 5.175e+04 | 45.47 | 43.66 | 502.6 |
| 0 | 2 | 4 | 4 | 0 | 5.171e+04 | 80.39 | 75.99 | 879.5 |
| 0 | 3 | 4 | 8 | 0 | 5.174e+04 | 461.1 | 150.9 | 1705 |
| 1 | 3 | 4 | 4 | 0 | 5.183e+04 | 197.1 | 196.8 | 1903 |
| 2 | 3 | 4 | 4 | 0 | 5.188e+04 | 65.39 | 62.74 | 697.2 |
| 3 | 3 | 4 | 4 | 0 | 5.199e+04 | 1228 | 1202 | 1.448e+04 |
| 4 | 0 | 4 | 4 | 0 | 5.441e+04 | 4350 | 3054 | 2.654e+04 |
| 4 | 1 | 4 | 4 | 0 | 5.158e+04 | 1.107e+04 | 3430 | 2.71e+04 |
| 4 | 2 | 4 | 4 | 0 | 5.149e+04 | 3976 | 3491 | 2.652e+04 |
| 4 | 3 | 0 | 4 | 0 | 5.121e+04 | 2353 | 224 | 3020 |
| 4 | 3 | 2 | 4 | 0 | 5.432e+04 | 3104 | 891.4 | 9400 |
| 4 | 3 | 4 | 24 | 0 | 5.15e+04 | 2.887e+04 | 5548 | 8.67e+04 |

La media y la desviación estándar usan todas las muestras crudas del grupo. RMS, p2p y Welch usan cada captura después de quitarle su propia media.

---
Generado por Codex (GPT-5), sin delegados.
