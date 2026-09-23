# PI permanente del firmware: oscilacion, ticks y modo estable (2026-09-16)

Continuacion de la sesion codex `01a0a622` (firmware unificado, ver
`VALIDACION_FIRMWARE_UNIFICADO_2026-09-16.md`). Placa geo-01, PGA x4 (codigo 2),
PGAout x24 (codigo 5), perfil lento aprendido IDAC0/IDAC1 = (+4, +4).
Proyecto: `src/firmware/psoc/AcondicionamientoAnalogico.cydsn`.
Ley vigente del lazo: `CONTROL_UNIFICADO.md`, seccion "Ley del lazo rapido (v4)".

## Unidades

Todas las tensiones de este documento estan en el **dominio del ADC de
control** (`ctl_dc`, mV relativos a la referencia de 1 V del banco), que es lo
unico que observa el lazo. No son tensiones fisicas del tap. Comparando con el
osciloscopio la relacion es del orden de x20 (LPo +112 mV de banco con el tap
en riel), pero no se midio con precision.

## Sintoma reportado

"El PI oscila mucho, tarda en converger, tiene saltitos bobos, trata de
microoptimizar y se queda moviendo eternamente". Captura:
`data/Osciloscopio Calibracion/Calibracion_16_09/Calibracion_16_09_15_17.csv`.

## Diagnostico (firmware v3 de codex)

Registro de 10 min sin tocar nada: `pi_firmware_2026-09-16/log1_antes_codex_v3.txt`.

1. **La rama PI nunca se ejecutaba.** `DEADBAND_UV` = 100 mV y la ventana
   valida de LPo es -95..+98 mV: toda lectura valida caia dentro de la banda.
   Solo actuaba el rescate de 80 codigos de IDAC3, que cruza la ventana entera.
2. **IDAC2 perseguia ruido.** `SUM_BAND_UV` = 5 mV contra un ruido de lectura
   de SUMo de +-6 mV, y esa rama tenia prioridad sobre LPo. En el log IDAC2
   recorre -3, -4, -5, -4, -5, -4... cada ~45 s; cada codigo tira LPo
   ~-150 mV y el rescate de IDAC3 (0 <-> 80) le responde. Ciclo limite.
3. **Pendientes en otra escala.** Config: IDAC3 7 mV/codigo, IDAC2 -1400
   mV/codigo (valores fisicos de los scripts de banco). Medido en `ctl_dc`:

| actuador | efecto sobre LPo | fuente |
|---|---|---|
| IDAC3 | ~+0,19..0,25 mV/codigo; todo su recorrido +-64 mV | lazo cerrado: -149 codigos -> -28 mV (log2) |
| IDAC2 | ~-80 mV inmediato, ~-150 mV asentado | log1, pasos -5->-4 y -4->-3 |
| SUMo por codigo de IDAC2 | ~+10 mV, enterrado en ruido | log1 |

   Consecuencia estructural: **un codigo de IDAC2 es mayor que todo el
   recorrido de IDAC3**. El vernier grueso/fino no cierra.
4. **Perturbaciones digitales en la cadena analogica.** Captura 15:17: cada
   1,02 s SUMo cae ~0,45 V y LPo va al riel ~90 ms, con recuperacion de ~0,4 s.

## La telemetria golpea la cadena (probado)

Se agrego al firmware una traza de las ultimas 127 lecturas crudas de LPo
(~20 ms cada una) que se vuelca con `ctl get 255` (`lab/ctl_trace.py`).

- `traza1_reporte_1s.txt`: golpes +47/-54 mV en t=46361 y 47367 ms, 15-20 ms
  despues de cada inicio de reporte (cadencia 1000 ms), cola de ~0,5 s.
- `traza2_reporte_20s.txt`: con `REPORT_MS`=20000 el golpe aparece solo tras
  el reporte (t=67529, reporte en 67489) y desaparece la cadencia de 1 s.

El reporte eran 72 tramas de 11 bytes por I2C (PSoC maestro, 400 kHz,
bloqueante). El ping de 1 s del PSoC NO produjo golpes visibles.

- `traza3_pozos_2s.txt`: ademas hay pozos de 40 ms y ~-30 mV cada ~2,0 s,
  ~0,5-0,7 s antes de cada barrido. Origen no identificado.

## Cambios (v4 + modo estable)

Todos en `control_config.c/.h` (logica pura, probada en PC) y
`control_runtime.inc` (medicion, barrido, telemetria):

- **Histeresis**: congela con |LPo| <= 6 mV (`HOLD_UV`), despierta fuera de
  +-20 mV (`DEADBAND_UV`). Mientras congelado no integra nada.
- **Guarda de SUMo**: IDAC2 solo si SUMo en riel o fuera de +-60 mV, un
  codigo cada 45 s (`COARSE_MS`).
- **Rescate de LPo en riel**: IDAC3 por signo de a 100 codigos cada 10 s; en
  tope, IDAC2 un codigo con contramovimiento de IDAC3.
- **Descarga a IDAC2** solo si IDAC3 >= 240, el error lo empuja mas afuera y
  el error predicho despues es menor. Sin la prediccion, LPo en el hueco entre
  dos codigos de IDAC2 hacia bailar a IDAC2 (simulado).
- **Medicion**: mediana de 5 promedios por canal; se descartan las lecturas de
  los 800 ms siguientes a cualquier trama de telemetria (`QUIET_MS`).
- **Modo estable** (tras 60 s congelado, `SETTLED_MS`): despierta solo con 3
  lecturas seguidas (`WAKE_COUNT`) fuera de +-35 mV (`SETTLED_BAND_UV`); un
  riel despierta siempre. Barrido de 1 s a 20 s, reporte de 5 s a 30 s.
- **Bandera de banda** = veredicto del lazo (congelado), ya no umbral crudo:
  antes titilaba con cada lectura mala y cada cambio emitia una trama I2C.
- Reporte periodico sin las 36 palabras de configuracion (van cada 30
  reportes, en `ctl report`, en `apply` y en el snapshot de captura).
- **Perfil**: retocar el lazo rapido ya no invalida IDAC0/IDAC1. EEPROM v3 se
  migra al arrancar (se conserva el perfil, el lazo rapido toma valores de
  fabrica). Imagen nueva: `CONTROL_NV_VERSION` 4; las tramas de telemetria
  siguen en version 3 (el ESP no se reflasheo).

Parametros nuevos al final de la tabla (indices 36-44): `HOLD_UV`, `FINE_MID`,
`COARSE_MS`, `QUIET_MS`, `SETTLED_MS`, `SETTLED_BAND_UV`, `WAKE_COUNT`,
`SCAN_SETTLED_MS`, `REPORT_SETTLED_MS`. Se cambian con `ctl set N V` +
`ctl apply` (+ `ctl save` para persistir).

## Verificacion

Host: `gcc -std=c99 -Wall -Wextra -Werror tests/control_test.c
AcondicionamientoAnalogico.cydsn/control_config.c -lm` (desde
`src/firmware/psoc`). Incluye una planta simulada (IDAC3 local rapido, IDAC2
con cola lenta de 35 s, ruido, pozos cada 2 s, deriva 5 mV/min, rieles) con
pendientes de IDAC3 0,18 / 0,25 / 0,50 mV/codigo. Con 0,12 mV/codigo IDAC3 ya
no puentea el hueco de IDAC2 y el lazo vuelve a mover IDAC2 12-17 veces en
30 min: limite fisico, no de sintonia.

Placa (Release grabado con `program_psoc.ps1`):

| log | firmware | resultado |
|---|---|---|
| log2 | v4 histeresis, pendiente 1,5 | converge lento (~5 min, pendiente 7x sobrestimada); luego 8 movimientos en 10 min, IDAC2 1 |
| log3 | v4 + mediana + pendiente 0,25 | valido a 22 s, en banda a 30 s, ultimo movimiento a 178 s, 12 min quieto, 153/155 lecturas en +-20 mV |
| log4 | modo estable | en banda a 80 s, ultimo movimiento 141 s, estable ~200 s, 9 min sin mover nada; reporte 30 s, barrido ~20 s; LPo deriva -10 -> -24 mV dentro de +-35 |

Captura 16:34 (`Calibracion_16_09_16_34.csv`, firmware log3): ningun tick era
del PI. Quedaban: espiga de 4 ms cada 2,0 s en SUMo (+2,2 V) y LPo (-1,5 V)
coincidente con el barrido; LPo +1,5 V 40 ms y cola 0,3 s cada 5 s
coincidente con el reporte; una muestra de +0,5 V en LPo cada 0,5 s sin
explicar. El modo estable fue la respuesta a esa captura; **falta confirmarlo
en osciloscopio**.

## Pendientes

1. Confirmar en osciloscopio que en modo estable los ticks pasan a 20 s y 30 s.
2. Origen del tick de 0,5 s en LPo y de los pozos de 2 s vistos por el ADC.
3. **Vernier roto**: IDAC3 (+-64 mV) no cubre un codigo de IDAC2 (~150 mV).
   Opcion solo firmware: IDAC3 en rango 255 uA con limite de codigos por
   compliance (nodo 10 k contra Vref; ver
   `COMPLIANCE_DE_LOS_IDAC_Y_MARGEN_DE_IDAC3_2026-09-13.md`). No probado.
4. **Captura**: `psoc_arm()` emite el snapshot completo por I2C justo antes de
   muestrear; por lo medido puede ensuciar el primer medio segundo capturado.
5. Nada de esto esta commiteado (submodulo `src/firmware/psoc`).

## Herramientas

- `lab/ctl_log.py`: registro de telemetria en columnas (no resetea el ESP).
- `lab/ctl_trace.py`: traza cruda de LPo desde el PSoC.
- `lab/monitor_control.ps1`: monitor de codex (`-StartLearning`, `-Command`,
  `-ResetEsp` para rehacer el saludo PSoC-ESP tras reflashear el PSoC).
