# Endurance de autocalibración en dos fases — 2026-09-10

Fuente: `lab\calibracion_nueva\dos_fases_endurance_recovery_10x_20260910.json`.

## Resultado global

- Duración observada: 20.3 min.
- Campañas completas: 10/10 (100.0%; IC95% Wilson 72.2%..100.0%).
- Posiciones planificadas e intentadas: 100/100.
- Fase 1: 10/10 PASS; 62.53 ± 0.85 s.
- Cambios intentados: 100/100 PASS (100.0%; IC95% Wilson 96.3%..100.0%).
- Campaña completa: 121.78 ± 1.93 s; p95 124.32 s; máximo 124.81 s.

## Desglose por ganancia

| PGAout | PASS/intentos | IC95% | tiempo medio ± DE (s) | p95 (s) | LPo medio ± DE vs Vref (mV) | todos los taps |
|---:|---:|---:|---:|---:|---:|---:|
| x1 | 20/20 | 83.9%..100.0% | 5.59 ± 1.51 | 8.94 | 2084.5 ± 0.5 | 10/20 |
| x2 | 10/10 | 72.2%..100.0% | 5.45 ± 1.36 | 7.95 | 2220.3 ± 89.4 | 9/10 |
| x4 | 10/10 | 72.2%..100.0% | 5.27 ± 1.28 | 7.11 | 2279.1 ± 18.6 | 0/10 |
| x8 | 10/10 | 72.2%..100.0% | 5.86 ± 1.70 | 8.86 | 2189.7 ± 33.6 | 0/10 |
| x16 | 10/10 | 72.2%..100.0% | 7.48 ± 1.70 | 8.99 | 2131.0 ± 16.5 | 0/10 |
| x24 | 10/10 | 72.2%..100.0% | 5.68 ± 1.70 | 8.91 | 2140.1 ± 0.5 | 0/10 |
| x32 | 10/10 | 72.2%..100.0% | 5.27 ± 1.30 | 7.13 | 2122.0 ± 0.7 | 0/10 |
| x48 | 10/10 | 72.2%..100.0% | 6.27 ± 1.92 | 8.95 | 2141.8 ± 0.6 | 0/10 |
| x50 | 10/10 | 72.2%..100.0% | 6.66 ± 2.00 | 9.01 | 2139.1 ± 0.8 | 0/10 |

## Seguridad y hallazgo

- Abortos protegidos: 0.
- Reverificaciones extraordinarias: 0.
- Recuperaciones neutras de fase 2: 0.
- Reintentos de escritura IDAC recuperados: 10.
- Eventos de búsqueda amplia/rieles: **0**.
- No hubo fallos funcionales ni fue necesario activar la recuperación excepcional en esta tanda.
