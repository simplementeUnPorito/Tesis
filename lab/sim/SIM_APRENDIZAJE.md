# Simulación del aprendizaje: decisión de ingeniería

## Alcance verificable

**SIMULADO.** `runtime_host.c` incluye directamente el
`control_runtime.inc` sin modificar y, por tanto, también el
`control_config.c` que éste incluye. `host_include/project.h` sustituye las
dependencias PSoC: EEPROM por 2 KiB en RAM, escritura de DAC por estado RAM,
ADC/AMux por llamadas inyectables y telemetría por un sumidero host. No se
modificó ningún archivo de firmware. `sim_aprendizaje.py` recompila ese
runtime y expone una campaña reproducible; `test_sim_aprendizaje.py` verifica
que compila, carga y que la ley de autoridad conserva la topología medida.

Ejecutar desde la raíz:

```text
python lab/sim/test_sim_aprendizaje.py
python lab/sim/sim_aprendizaje.py --campaign --json
```

La primera ejecución produjo `2` pruebas correctas. Esto verifica el arnés,
no valida una modificación en placa.

## Datos que sí están disponibles

**MEDIDO — `lab/autoridad/*.json`, 2026-09-27.** No existen aún archivos
`idac0_pgax1.json`, `idac0_pgax16.json` ni `idac0_pgax32.json`; por tanto no
se inventaron ni se interpolaron esos tres puntos.

| Relación | Puntos medidos | Resultado |
|---|---:|---:|
| IDAC0 → OPA_SUM, PGA x4 / x50 | -0.863 / -7.855 mV/código | factor 9.11 (la relación solicitada x11.8 no queda confirmada con sólo estos dos puntos) |
| IDAC1 → OPA_SUM, PGA x4 / x50 | -0.350 / -0.300 mV/código | no escala materialmente con PGA |
| IDAC2 → OPA_SUM, PGAout x4 / x24 | +0.407 / +0.240 mV/código | no escala materialmente con PGAout |
| IDAC2 → SUM, PGAout x4 / x24 | +2.076 / +28.550 mV/código | escala 13.75× al cambiar PGAout 6× |
| IDAC3 → LP, PGAout x24 | +2.177 mV/código | un único punto; no permite predecir margen en otro par |

**DEDUCIDO.** Los cuatro sentidos topológicos pedidos son compatibles con las
mediciones: IDAC0 depende de PGA, IDAC1 no; IDAC2 entra antes de PGAout y por
eso no cambia en OPA_SUM pero sí en SUM; IDAC1 sobre SUM cambia con PGAout.
La magnitud de la última relación no debe ajustarse a la topología: se reporta
tal cual se midió.

## Puerta de validación contra placa

**MEDIDO.** Con el firmware actual x4/x16 converge; las seis visitas reales
de x16/x16 terminaron en `APRENDIENDO`.

**SIMULADO.** La campaña del arnés muestra ese mismo patrón base: x4/x16
`PASA`, x16/x16 `APRENDIENDO`, con IDAC3 en riel para este último. Es una
prueba de cableado de estados del runtime host, no una validación de planta.

**DEDUCIDO — decisión de la puerta.** La planta aún no puede explicar ese
fracaso de forma independiente: los JSON son escalones de autoridad a
ganancias x4/x50 (IDAC0/1) y x1 con PGAout x4/x24 (IDAC2), pero no aportan
los offsets iniciales, la dinámica ni una traza de aprendizaje para x16/x16.
Sin esos datos se podría elegir arbitrariamente un offset para producir
`APRENDIENDO`; hacerlo sería ajustar el modelo al resultado prohibido. Por
tanto la puerta de validación **NO está superada**.

## Hipótesis de variante (no evaluada como éxito)

**DEDUCIDO.** Observar el par lento en OPA_SUM (tap 2) elimina la dependencia
de PGAout observada en SUM (tap 3). Es una hipótesis físicamente coherente,
pero no una predicción validada de que x16/x16 mejore.

**MEDIDO.** A PGA x50 en OPA_SUM: IDAC0 = -7.855 mV/código e IDAC1 = -0.300
mV/código; la relación de autoridad es 26.2:1. Por ello IDAC0 grueso / IDAC1
fino es una pareja plausible para una futura variante.

**SIMULADO.** El ejecutable enumera, como escenarios exploratorios, las
variantes `opa_sum` e `idac0/idac1` y conserva los cuatro pares actualmente
buenos. Sus números de IDAC3 no se deben considerar un pase de margen: no hay
medición de IDAC3 para esos cinco pares ni una planta validada que lo calcule.
En particular, un IDAC3 contra riel nunca se clasifica como éxito.

## Datos mínimos antes de autorizar el cambio

1. Escalones A-B-A-B-A de IDAC0 a PGA x1, x16 y x32 (los archivos ausentes
   que se pidieron), más x4/x50 existentes.
2. Trazas completas de aprendizaje y taps absolutos para x4/x16 y las seis
   visitas x16/x16, con los cuatro códigos y marcas de fase.
3. Un escalón de IDAC3 por cada par candidato, para evaluar margen real y no
   sólo LPo dentro de banda.
4. Con esos datos, ajustar la planta sin usar el resultado PASA/FALLA y exigir
   que el baseline reproduzca ambos casos antes de puntuar las variantes.

Recomendación: **no se cambia**.
