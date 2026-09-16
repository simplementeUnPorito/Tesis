# Endurance de autocalibración en dos fases — 2026-09-10

Fuente: `lab\calibracion_nueva\dos_fases_endurance_guarded_15x_20260909.json`.

## Resultado global

- Duración observada: 30.7 min.
- Campañas completas: 14/15 (93.3%; IC95% Wilson 70.2%..98.8%).
- Posiciones planificadas: 150; intentadas: 142. Las restantes no se ejecutaron después del aborto seguro de la campaña.
- Fase 1: 15/15 PASS; 62.31 ± 0.70 s.
- Cambios intentados: 141/142 PASS (99.3%; IC95% Wilson 96.1%..99.9%).
- Campaña completa: 124.25 ± 4.97 s; p95 130.86 s; máximo 131.50 s.

## Desglose por ganancia

| PGAout | PASS/intentos | IC95% | tiempo medio ± DE (s) | p95 (s) | LPo medio ± DE vs Vref (mV) | todos los taps |
|---:|---:|---:|---:|---:|---:|---:|
| x1 | 29/29 | 88.3%..100.0% | 6.19 ± 1.88 | 8.99 | 2084.1 ± 0.6 | 15/29 |
| x2 | 14/15 | 70.2%..98.8% | 5.99 ± 1.67 | 8.92 | 2290.7 ± 62.3 | 12/14 |
| x4 | 14/14 | 78.5%..100.0% | 6.60 ± 1.87 | 8.97 | 2292.4 ± 28.7 | 0/14 |
| x8 | 14/14 | 78.5%..100.0% | 6.63 ± 1.90 | 8.96 | 2178.8 ± 0.6 | 0/14 |
| x16 | 14/14 | 78.5%..100.0% | 5.98 ± 1.81 | 8.87 | 2129.1 ± 14.3 | 0/14 |
| x24 | 14/14 | 78.5%..100.0% | 6.53 ± 1.92 | 8.96 | 2139.9 ± 0.5 | 0/14 |
| x32 | 14/14 | 78.5%..100.0% | 6.57 ± 2.03 | 8.97 | 2122.0 ± 0.4 | 0/14 |
| x48 | 14/14 | 78.5%..100.0% | 5.52 ± 1.47 | 8.93 | 2140.2 ± 5.2 | 0/14 |
| x50 | 14/14 | 78.5%..100.0% | 5.75 ± 1.72 | 8.94 | 2139.0 ± 1.2 | 0/14 |

## Seguridad y hallazgo

- Abortos protegidos: 1.
- Reverificaciones extraordinarias: 2.
- Recuperaciones neutras de fase 2: 0.
- Reintentos de escritura IDAC recuperados: 10.
- Eventos de búsqueda amplia/rieles: **0**.
- El aborto observado ocurrió después de tres verificaciones inválidas. Se restauró la ganancia previa sin barrer rieles.
- El resultado demuestra contención segura, pero no demuestra 100% de disponibilidad prolongada de todas las ganancias.
