# Ganancia del ruido SD

Las métricas están en cuentas ADC. Cada valor se informa como media ± desvío muestral entre capturas P4 válidas; a cada P4 se le restó el promedio BASE del grupo y luego la media pre-marca (índices 0–19). La figura usa `|transfer|` porque el eje vertical es logarítmico; la tabla y los ajustes conservan su signo.

| tap | PGA (cód./gan.) | PGAout (cód./gan.) | n P4 | n BASE | transfer | busy | p2p | transfer/gan. | busy/gan. | p2p/gan. |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0/x1 | 4/x16 | 4 | 4 | -0.695369 ± 0.866816 | 5.83469 ± 0.395589 | 9.76531 ± 0.731166 | -0.695369 ± 0.866816 | 5.83469 ± 0.395589 | 9.76531 ± 0.731166 |
| 0 | 1/x2 | 4/x16 | 4 | 4 | 3.85214 ± 0.193765 | 13.6645 ± 0.233733 | 18.5663 ± 0.386275 | 1.92607 ± 0.0968824 | 6.83227 ± 0.116866 | 9.28316 ± 0.193138 |
| 0 | 2/x4 | 4/x16 | 4 | 4 | 10.3961 ± 0.589433 | 32.502 ± 0.535154 | 37.5969 ± 0.968618 | 2.59902 ± 0.147358 | 8.12551 ± 0.133788 | 9.39923 ± 0.242154 |
| 0 | 3/x8 | 4/x16 | 8 | 8 | 21.4021 ± 8.86736 | 61.9731 ± 24.638 | 66.3093 ± 26.0242 | 2.67526 ± 1.10842 | 7.74663 ± 3.07975 | 8.28866 ± 3.25302 |
| 4 | 0/x1 | 4/x16 | 4 | 4 | -658.778 ± 15.4624 | 1885.01 ± 42.5426 | 2090.01 ± 45.1842 | -41.1736 ± 0.966401 | 117.813 ± 2.65891 | 130.625 ± 2.82401 |
| 4 | 1/x2 | 4/x16 | 4 | 4 | -751.423 ± 105.729 | 2823.3 ± 902.22 | 3036.61 ± 904.007 | -23.482 ± 3.30403 | 88.2281 ± 28.1944 | 94.8941 ± 28.2502 |
| 4 | 2/x4 | 4/x16 | 4 | 4 | -758.71 ± 11.4557 | 2605.87 ± 80.5148 | 2811.72 ± 67.7146 | -11.8548 ± 0.178995 | 40.7167 ± 1.25804 | 43.9332 ± 1.05804 |
| 4 | 3/x8 | 0/x1 | 4 | 4 | -38.4638 ± 1.09652 | 151.201 ± 2.89943 | 198.913 ± 1.98684 | -4.80798 ± 0.137065 | 18.9002 ± 0.362428 | 24.8642 ± 0.248355 |
| 4 | 3/x8 | 2/x4 | 4 | 4 | -201.785 ± 2.12962 | 589.67 ± 12.2027 | 669.444 ± 9.86386 | -6.30578 ± 0.0665505 | 18.4272 ± 0.381334 | 20.9201 ± 0.308246 |
| 4 | 3/x8 | 4/x16 | 8 | 8 | -647.695 ± 297.519 | 2230.68 ± 891.897 | 2417.41 ± 946.979 | -5.06012 ± 2.32436 | 17.4272 ± 6.96795 | 18.886 ± 7.39827 |

## Ajustes lineales

Modelo: `y = a·G + b`. Criterio explícito (10%): con `S=max|a·G+b|` en los puntos observados, `b≈0` si `|b|≤0,1·S`; `a≈0` si `|a|·(Gmax−Gmin)≤0,1·S`.

### Tap 0 vs PGA

| métrica | a [cuentas/ganancia] | b [cuentas] | b/(aG+b), G=1 | b/(aG+b), G=8 |
|---|---:|---:|---:|---:|
| busy | 8.054 | -1.70894 | -0.269333 | -0.0272457 |
| transfer | 3.08622 | -2.83459 | -11.2651 | -0.129699 |

**Interpretación (una línea):** Tap 0 vs PGA: busy: entra en la entrada (referido a entrada aproximadamente constante); transfer: mezcla de términos de entrada y referencia/salida.

### Tap 4 vs PGAout, PGA fijo x8

| métrica | a [cuentas/ganancia] | b [cuentas] | b/(aG+b), G=1 | b/(aG+b), G=8 |
|---|---:|---:|---:|---:|
| busy | 138.094 | 23.8562 | 0.147306 | 0.0211377 |
| transfer | -39.6279 | -18.5858 | 0.319269 | 0.0553794 |

**Interpretación (una línea):** Tap 4 vs PGAout con PGA x8: busy: entra en la entrada (referido a entrada aproximadamente constante); transfer: entra en la entrada (referido a entrada aproximadamente constante).

Capturas descartadas por `_medir`: 0. Grupos omitidos por faltar BASE o P4 válidos: ninguno.

---
IA principal: Codex (modelo no reportado) · Delegados: ninguno · Fallbacks: ninguno
