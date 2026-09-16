# Resultados de autocalibración en dos fases — 2026-09-09

## Implementación validada

- Fase 1 se ejecuta una sola vez: acondiciona 30 s en neutro, aplica el punto
  histórico y espera 30 s. Código seleccionado por caracterización repetida:
  `IDAC0=19`, `IDAC1=140`.
- Fase 2 se ejecuta en cada cambio de PGAout. Reutiliza el par histórico
  `IDAC2=254`, `IDAC3=83`; si el punto ya es legible no explora ni visita rieles.
- Ganancias recorridas: `x1,x2,x4,x8,x16,x24,x32,x48,x50`.
- El criterio funcional es PGAgain, BPo y LPo dentro del rango físico del ADC.
  ch2/ch3 se registran siempre, pero no bloquean el uso de LPo.
- Techo de puesta en marcha: 180 s. EEPROM sólo se habilita después de PASS.

## Evidencia principal

Archivo: `calibracion_nueva/dos_fases_calibrate-gains_20260909_224651.json`

- 5 reinicios completos PASS.
- 45/45 cambios de ganancia PASS funcional.
- Fase 1: **62,62 ± 0,89 s** (media ± desviación estándar muestral;
  mínimo 61,99 s, máximo 63,91 s).
- Recorrido completo x1→x50: **117,81 ± 2,60 s** (mínimo 113,50 s,
  máximo 119,79 s).
- Cambio individual de ganancia: media 4,81 a 7,23 s según ganancia;
  máximo observado 8,96 s.
- Códigos reutilizados en las cinco campañas: `[19,140,254,83]`.

| PGAout | PASS | tiempo medio ± DE (s) | máximo (s) | LPo medio ± DE respecto Vref (mV) |
|---:|---:|---:|---:|---:|
| x1  | 5/5 | 6,46 ± 2,24 | 8,96 | +2084,3 ± 0,6 |
| x2  | 5/5 | 4,81 ± 0,02 | 4,83 | +2265,6 ± 19,6 |
| x4  | 5/5 | 6,46 ± 2,24 | 8,93 | +2284,8 ± 0,3 |
| x8  | 5/5 | 6,03 ± 1,83 | 8,94 | +2178,7 ± 0,5 |
| x16 | 5/5 | 6,45 ± 2,24 | 8,92 | +2125,3 ± 0,3 |
| x24 | 5/5 | 7,19 ± 2,16 | 8,95 | +2139,9 ± 0,3 |
| x32 | 5/5 | 7,23 ± 1,45 | 8,88 | +2121,8 ± 0,3 |
| x48 | 5/5 | 5,31 ± 0,85 | 6,78 | +2141,5 ± 0,4 |
| x50 | 5/5 | 5,21 ± 0,87 | 6,76 | +2138,7 ± 0,2 |

LPo permanece legible y estable, pero cerca del riel alto. No se impuso una
banda arbitraria en milivoltios. Las cinco señales fueron válidas en x1 y x2;
en x4..x50 ch2/ch3 quedan saturadas con la autoridad disponible, aunque LPo,
PGAgain y BPo permanecen legibles. Esto es una limitación física registrada,
no un PASS oculto de los taps internos.

## Selección de la semilla de fase 1

Archivos:

- `calibracion_nueva/dos_fases_characterize-x2_20260909_193700.json`
- `calibracion_nueva/dos_fases_characterize-x2_20260909_221909.json`
- `calibracion_nueva/dos_fases_characterize-x2_20260909_223231.json`

Se probaron vecinos de los mínimos discretos con tres reinicios por combinación.
`[19,140]` y `[19,120]` obtuvieron 3/3 PASS en x2; se eligió `[19,140]` por ser
el más cercano al mínimo estacionario de BPo. `[19,157]` sólo obtuvo 4/6 PASS
en dos bloques independientes.

## EEPROM

Archivo de evidencia:
`calibracion_nueva/dos_fases_calibrate-gains_20260909_225731.json`.

Después de los 45 PASS se volvió a ejecutar y verificar x1. El PSoC respondió
aceptación y escritura correctas para `[19,140,254,83]`. El historial reutilizable
también queda en `calibracion_nueva/autocal_history.json`.

Pendiente de validación separada: comprobar la restauración después de un
power-cycle real. No se realizó un corte físico de alimentación en esta sesión.

## Actualización de endurance — 2026-09-10

La afirmación anterior de que las cinco señales permanecían válidas en x1/x2
describe las cinco campañas iniciales, no la estabilidad interna prolongada.
Una tanda posterior de 15 campañas encontró deriva/memoria lenta en x2:

- fase 1: 15/15 PASS, 62,31 ± 0,70 s;
- campañas completas: 14/15;
- cambios intentados: 141/142 PASS;
- un x2 quedó inválido tras tres verificaciones;
- la guarda restauró x1 y evitó la búsqueda de extremos: 0 eventos de riel.

Ese hallazgo eliminó el comportamiento que barría extremos ante una lectura
transitoria. La versión final revalida, descarga IDAC2/IDAC3 en x1 durante 30 s
sólo como recuperación excepcional y, si todavía falla, restaura la ganancia
previa y aborta sin explorar.

Validación hardware de la versión final:

- 10/10 campañas completas;
- 100/100 cambios PASS, incluyendo diez retornos x50→x1;
- fase 1: 62,53 ± 0,85 s;
- recorrido completo: 121,78 ± 1,93 s, p95 124,32 s, máximo 124,81 s;
- cambios normales: máximo 9,01 s;
- 0 búsquedas amplias/rieles y 10 reintentos de escritura recuperados;
- 3/3 pruebas unitarias para reverificación, recuperación neutra y aborto seguro.

Los resultados completos e intervalos Wilson están en
`RESULTADOS_ENDURANCE_RECOVERY_DOS_FASES_2026-09-10.md`. La tanda que encontró
el fallo está preservada en `RESULTADOS_ENDURANCE_DOS_FASES_2026-09-10.md`.

La limitación interna es más amplia de lo que indicaban las cinco campañas
iniciales: en la tanda final todos los taps fueron válidos en 10/20 lecturas x1,
9/10 x2 y 0/10 desde x4. El PASS funcional sigue significando únicamente
PGAgain, BPo y LPo válidos; LPo continúa cerca del riel alto, no centrado.
