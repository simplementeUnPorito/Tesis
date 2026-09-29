# lab/ — bitácora de banco de la cadena analógica GEO

Informes, handoffs y datos crudos del trabajo de autocalibración y control de
la cadena de acondicionamiento (PGA → pasabanda → sumador → PGAout → pasabajos)
entre el 2026-09-04 y el 2026-09-16. Los documentos se escribieron en caliente:
**varios quedaron superados o contienen conclusiones retractadas**. Este índice
dice cuál es estado y cuál es historia.

## Leer primero (estado al 2026-09-16)

| documento | qué fija |
|---|---|
| `PI_FIRMWARE_TICKS_Y_MODO_ESTABLE_2026-09-16.md` | PI permanente del firmware: por qué oscilaba, telemetría I2C que golpea LPo, modo estable, pendientes en dominio `ctl_dc`. Pendientes abiertos. |
| `VALIDACION_FIRMWARE_UNIFICADO_2026-09-16.md` | Proyecto PSoC único + ESP `slave2`: qué se compiló, grabó y probó. |
| `../src/firmware/psoc/AcondicionamientoAnalogico.cydsn/CONTROL_UNIFICADO.md` | Secuencia de operación, comandos `ctl`, ley del lazo rápido. |
| `RESULTADO_GANANCIA_2026-09-14.md` | Ganancia conjunta sostenida (PGA x4 · PGAout x24 = 96) y dónde está el techo. |
| `ARQUITECTURA_CALIBRACION_CAMPO.md` | Arquitectura propuesta para campo (aprender una vez, identidad de placa, trazabilidad). |

## Cronología

### 2026-09-04 / 05 — primeras mediciones
- `PREGUNTAS_PARA_ELIAS.md` — decisiones abiertas al cierre del 04; medido en `docs/MEDICIONES_2026-09-04.md`.
- `HANDOFF_GOAL_2026-09-05.md` — estado del goal de fin de semana; ver `docs/MEDICIONES_2026-09-05.md`.

### 2026-09-06 / 07 — resistencias y AMux
- `INFORME_CIERRE_2026-09-07.md` — cierre de la adquisición EXP4c/EXP4d (22 h).
- `PLAN_RESISTENCIAS_LUNES.md` — plan de cambio de R; resultado: solo R14 a 3,9 kΩ.
- `INFORME_R14_3K9_2026-09-07.md` — validación de R14 = 3,9 kΩ a PGA x50 / PGAout x1.
- `REGISTRO_AMUX_6CH_Y_RESISTENCIAS_2026-09-07.md` — AMux de seis canales (sexto = capacitor).

### 2026-09-08 / 10 — autocalibración a lazo abierto (Python)
- `INFORME_AUTOCALIBRACION_2026-09-08.md` — **SUPERADO**: el capacitor del AMux alteraba los nodos.
- `HANDOFF_AUTOCALIBRACION_AUTORITATIVO_2026-09-09.md` — IDAC2 e IDAC3 siguen en 10 kΩ (historia).
- `RUNBOOK_POST_CAMBIO_IDAC2_5K1.md` — **NO USAR**: cambio a 5,1 kΩ nunca instalado.
- `RESULTADOS_AUTOCALIBRACION_DOS_FASES_2026-09-09.md` — método de dos fases.
- `DIAGNOSTICO_AUTORIDAD_Y_CENTRADO_2026-09-10.md` — superado por el handoff de la tarde.
- `HANDOFF_AUTOCALIBRACION_2026-09-10_TARDE.md` — handoff autoritativo de ese día.
- `RESULTADOS_ENDURANCE_DOS_FASES_2026-09-10.md`, `RESULTADOS_ENDURANCE_RECOVERY_DOS_FASES_2026-09-10.md`, `REPUNTUACION_ENDURANCE_2026-09-10.md` — endurance (14/15 y 10/10) y su re-puntuación por rieles.
- `RESULTADOS_ARRANQUE_FRIO_2026-09-10.md` — 16/16 arranques en frío (datos en `arranque_frio/`).
- `RESULTADOS_MAPA_SUMADOR_2026-09-10.md` — mapa parcial del sumador.
- `RESULTADOS_NOCTURNOS_CONSOLIDADOS_2026-09-10.md` — 70 min de pruebas nocturnas.
- `REVISION_CONSTANTES_2026-09-10.md` — auditoría de constantes de `autocalibracion_dos_fases.py`.

### 2026-09-11 / 13 — acople, lazo cerrado, PGAout
- `HANDOFF_AUTOCALIBRACION_2026-09-11.md` — sesión del 11 (datos en `calibracion_nueva/`).
- `CONCLUSIONES_PARCIALES_2026-09-11.md` — PGAout carga al sumador; la carga crece con la ganancia.
- `LAZO_CERRADO_PI_2026-09-12.md` — regulador PI en cascada con vernier (`regulador_pi.py`).
- `HALLAZGOS_2026-09-12_TARDE.md` — la "histéresis" de IDAC3 era rezago: **retractada**.
- `RESUMEN_NOCHE_2026-09-13.md` — índice de la noche 12→13; compliance descartado.
- `RESULTADOS_CENTRADO_POR_BISECCION_2026-09-13.md` — bisección de signo en vez de PI.
- `AUTORIDAD_REAL_DE_LOS_IDAC_2026-09-13.md` — autoridad real de los cuatro IDAC (reemplaza lo anterior).
- `COMPLIANCE_DE_LOS_IDAC_Y_MARGEN_DE_IDAC3_2026-09-13.md` — por qué IDAC3 parecía no tener autoridad.
- `PORTE_A_FIRMWARE_BISECCION_2026-09-13.md` — cómo llevar la bisección a firmware.
- `LA_CADENA_DIVERGE_SOLA_A_GANANCIA_100_2026-09-13.md` — a ganancia 100 diverge sin lazo.
- `PGAOUT_TIENE_REFERENCIA_PROPIA_2026-09-13.md` — el punto fijo de PGAout no es cero: error de consigna.

### 2026-09-14 / 16 — ganancia, firmware unificado, PI permanente
- `RESULTADO_GANANCIA_2026-09-14.md`
- `VALIDACION_FIRMWARE_UNIFICADO_2026-09-16.md`
- `PI_FIRMWARE_TICKS_Y_MODO_ESTABLE_2026-09-16.md`

## Datos y herramientas

| ruta | contenido |
|---|---|
| `pi_firmware_2026-09-16/` | logs de telemetría (v3 → modo estable) y trazas crudas de LPo |
| `calibracion_nueva/` | corridas de autocalibración 08–11/09 (json/csv/log) |
| `arranque_frio/` | campaña de arranque en frío del 10/09 |
| `calibracion/` | calibración del 04/09 |
| `planta/` | campañas por combinación PGA/PGAout (05/09) y diagnósticos de calibración (`cal_*.json`, `analisis/`) |
| `lunes/` | sesión de resistencias del 07/09: línea base, autoridad por etapa y tap, encadenado |
| `server_root/` | raíz de datos de prueba del servidor (`raw/`, `processed/`, `server/`) del 03/09 |
| `geo_node2_ws_20260903_1715.*` | captura WebSocket del nodo 2 (int24le + json) |
| `banco_pi.py` | banco del lazo PI: devuelve VEREDICTOS, no logs (`arranque`, `ganancias`, `convergencia`, `estado`) |
| `diag_par.py` | foto completa de un par de ganancias: los cinco taps, sus banderas de validez y los cuatro IDAC a CSV |
| `analiza_pasos.py` | saca pendiente y tiempo de establecimiento de cada actuador a partir de un CSV de `diag_par.py` |
| `ctl_log.py` | registro en columnas de la telemetría `ctl` (no resetea el ESP) |
| `ctl_trace.py` | traza cruda de LPo desde el PSoC (`ctl get 255`) |
| `monitor_control.ps1` | monitor de codex; `-StartLearning`, `-Command`, `-ResetEsp` |
| `barrido_total.py` | barrido reanudable de las 81 combinaciones PGA/PGAout; recuperación del PSoC mediante el ESP |
| `barrido_total.sh` | servicio liviano para Linux por SSH (`start/status/log/stop`), sin PSoC Creator ni PowerShell |
| `finalizar_deriva_24h.ps1`, `reanudar_goal.ps1`, `PARAR_REANUDACION` | automatización de goals largos (watchdog/reanudación) |

## Barrido desatendido en Linux

La placa debe tener cargados el firmware ESP32 con `psocreset` y el firmware
PSoC con la ISR de `esp_reset`. Después de clonar o actualizar el repositorio:

```bash
git submodule update --init --recursive
chmod +x lab/barrido_total.sh
./lab/barrido_total.sh start 3 240
./lab/barrido_total.sh status
./lab/barrido_total.sh log
```

El lanzador busca primero `/dev/serial/by-id/`, crea un entorno virtual e
instala `pyserial`. Si hay más de un adaptador, seleccione el correcto con
`BARRIDO_PORT=/dev/serial/by-id/...`. La sesión sigue al cerrar SSH mediante
`nohup`; después de un reinicio del servidor basta ejecutar nuevamente
`./lab/barrido_total.sh start`, que reanuda desde `resultados.jsonl`.

## Memoria de puntos de trabajo (2026-09-24)

El firmware guarda, para **cada uno de los 81 pares de ganancia**, el punto de
trabajo que le funcionó (los cuatro códigos de IDAC). Al volver a ese par
arranca ahí en vez de buscarlo a ciegas. Antes la tabla tenía **ocho** lugares
con rotación circular, así que nueve de cada diez pares perdían su punto antes
de que se los volviera a visitar.

**Por qué importa**, medido sobre las 191 visitas de las campañas del 22 y 23:

| | nota A | nota B | nota C | nota D | no quieto |
|---|---:|---:|---:|---:|---:|
| sin aprendizaje (restauró un punto) | **2,0 s** | **2,0 s** | 85 s | 48 s | 271 s |
| con aprendizaje (buscó a ciegas) | 57 s | 229 s | 216 s | 455 s | 959 s |

Lo que aterriza rápido es lo que aterriza bien. No hay que elegir entre
velocidad y estabilidad: son el mismo caso.

### La invariante: el lazo nunca se abre

El punto guardado es una **condición inicial**, nunca un reemplazo del control.
`control_on_gain_change()` abre la ventana de forzado **antes** de restaurar, así
que el punto entra con el PI corrigiendo a fondo. Ningún nivel de política
congela el lazo, y siguen intactos los mecanismos que absorben lo no modelado
(recentrado lento, despertar del modo estable, watchdogs de SUMo y LPo). Un
punto que no reproduce se degrada y termina invalidado: **la medición le gana al
modelo, nunca al revés.**

Eso no se asume, se prueba, y la prueba es bloqueante:

```powershell
python lab\prueba_lazo_cerrado.py --port COM8
```

Perturba el punto con un escalón de IDAC y verifica que el lazo vuelva solo.
Si falla, la memoria de puntos rompió el control: **no soltar la campaña.**

### Política de selección

`ctl punto policy <n>` la cambia **en caliente**, sin `apply` (un apply
reiniciaría el lazo en medio de un experimento):

| n | nivel | de dónde sale la condición inicial |
|---|---|---|
| 0 | OFF | como antes — es el **brazo de control** del experimento |
| 1 | UNICO | el punto validado de la EEPROM |
| 2 | VECINO | el candidato de contexto más parecido (pool de RAM) |
| 3 | INTERPOLADO | recta entre dos candidatos asentados; **nunca extrapola** |

El contexto es el **estado físico medido** (SUMo al entrar + códigos del par
lento), que es el proxy de la carga del acople de 680 µF — no "de qué par
venís", que serían 81² casos y se sobreajustaría al orden del barrido.

### Comandos nuevos por USB

```
ctl punto <par> <c0> <c1> <c2> <c3>   siembra un punto (par = pga_cod*9 + pgaout_cod)
ctl puntos                            vuelca la tabla entera
ctl punto dump <par>                  vuelca un par
ctl punto clear [par]                 borra uno, o todos
ctl punto policy <0..3>               cambia la política en caliente
```

### Levantar el experimento

```powershell
# 1. generar la semilla desde lo ya medido (no toca el banco)
python lab\semilla_puntos.py
python lab\semilla_puntos.py --comandos | Select-Object -First 5

# 2. compuerta: el lazo sigue cerrado
python lab\prueba_lazo_cerrado.py --port COM8

# 3. sembrar y medir las tres condiciones contra el brazo de control
python lab\experimento_semilla.py --port COM8 --sembrar --reanudar
```

Se detiene sin perder nada con Ctrl-C, con SIGTERM, o creando `.run/STOP`
dentro del directorio de salida. `--reanudar` saltea las combinaciones
`(par, condición, brazo, vuelta)` que ya están en `resultados.jsonl`.

### Qué mide, y en qué orden de prioridad

1. **Cobertura** — cuántos pares quedan estables.
2. **Reproducibilidad** — que pase en las **tres** condiciones de entrada
   (frío tras `psocreset`, viniendo de x1/x1, viniendo de x32/x32).
3. **Velocidad** — `t_estable` por origen del punto.
4. **Nota** — cuánto rango libre quedó.

Y en toda visita, el **residuo de corrección** = códigos finales − semilla.
Residuo → 0 significa que la semilla acertó; su dependencia con el contexto es
la superficie de corrección que van a consumir las campañas siguientes; y el
mismo par en días distintos mide la deriva térmica sin instrumental extra.

### Cobertura real de la semilla

**42 de 81 pares** tienen un punto de nota A/B respaldado por al menos 15
muestras válidas de LPo, y **31 de esos tienen margen de actuador**. Los otros
11 sólo tienen puntos con IDAC3 pasado 200: están en banda pero sin autoridad
para corregir, y sembrarlos propagaría la fragilidad.

**PGA x16 y x24 son 0 de 9.** No es "a más ganancia peor" — x32 es 8 de 9. La
causa está medida: a x24 un solo código de IDAC0 mueve SUMo 365 mV contra una
ventana de 195 mV, o sea que **el actuador es más grueso que el blanco** y la
búsqueda a ciegas no puede resolverlo por más tiempo que se le dé.

### Trampa que costó 39 semillas falsas

`LPo_pp_final_mV` se calcula sobre las últimas 15 muestras **válidas**. Si la
visita tuvo una sola, el pico a pico da **0,0 mV** y parece quietud perfecta
cuando es ausencia de dato. Hay 21 visitas así en el histórico, con LPo medible
entre el 0,7 % y el 1,7 % del tiempo. Por eso toda nota exige ahora
`muestras_validas_LPo >= 15` (`MUESTRAS_VALIDAS_MIN`): la ventana del pico a
pico tiene que estar llena para que el número signifique algo.

## Ruido de la SD y de la radio (rutinas listas, medición pendiente)

Se corre **una vez congeladas las ganancias estables y sin tocar nada más**: si
el punto de operación cambia entre dos medidas, la diferencia no se le puede
atribuir a la SD.

El firmware ya sabía parte de la respuesta — en `main.cpp` está escrito que el
drenaje de la SD "escribe un sector cada 57,6 ms durante el muestreo y cada
escritura mete una espiga en la señal". Lo que falta medir es **cuánto, con qué
forma espectral, y si depende de la ganancia**.

### El camino de datos era la radio

Las muestras sólo salían del nodo por ESP-NOW, así que no se podía medir con la
radio callada: leer los datos ya la encendía. Por eso se agregó `dumpusb`, que
vuelca la captura que quedó en RAM por USB **después** de terminada. La captura
tiene que ser limpia; la lectura puede ser sucia porque ocurre después.

La campaña reproducible por omisión compara BASE contra radio. La SD real sólo
se puede medir con una captura mayor que la RAM del PSoC y `sdcap`; `sdstress`
queda como diagnóstico sintético y se etiqueta explícitamente SDSTRESS para no
confundir ambas cosas.

```
dumpusb [desde] [hasta]       vuelca la captura en RAM por USB
sdstress <ms> <periodo_ms>    diagnóstico sintético de escrituras (no SD real)
rftest <ms> <periodo_ms> <bytes>   trafico ESP-NOW en paralelo
```

### Correr

```powershell
python lab\experimento_ruido.py --port COM8 --pares 2,4 2,5 --repeticiones 3
python lab\experimento_ruido.py --port COM8 --condiciones BASE RF
python lab\analisis_ruido.py lab\ruido_<fecha>
```

Las condiciones pedidas se recorren de ida y vuelta; con el modo predeterminado
el orden es **BASE / RF / RF / BASE**. Esto evita medir todas las BASE y luego
todas las RF, que mezclaría la diferencia con la deriva de τ≈30-44 s. Para una
prueba eléctrica sintética puede pedirse `--condiciones BASE SDSTRESS`, pero ese
resultado no se presenta como almacenamiento real del PSoC.

### Tres cosas que el análisis separa a propósito

**Ruido y muestras perdidas no son lo mismo.** Si la SD le roba DMA o CPU al
PSoC el daño son lotes faltantes, no ruido, y no se arregla con blindaje. Se
informa aparte, contando huecos de `seq`.

**La dependencia con la ganancia dice DÓNDE se acopla.** Si el delta referido a
la entrada no cambia con la ganancia, el ruido entra antes del PGA; si baja al
subir la ganancia, entra después. Eso vale mucho más que "sí depende".

**La comparación dentro de la misma captura es la que detecta las espigas.** El
firmware marca las muestras que caen durante una escritura de SD
(`SAMPLE_FLAG_SD_WRITE`, `sync_protocol.h:106`), así que se comparan contra las
no marcadas **sin deriva de por medio**. Verificado con datos sintéticos: una
interferencia impulsiva que en el RMS de 10-50 Hz apenas mueve la aguja (1,01×)
aparece como 5,2× en esta comparación, porque reparte su energía por todo el
espectro y casi nada cae en la banda útil. Mirando sólo el RMS de banda se
concluiría que la SD no molesta.

### El piso de ruido absoluto queda escrito, sin correr

`--piso` exige la entrada terminada o en corto: con el geófono conectado se
mide el movimiento del suelo más el instrumento. Es una intervención física, y
el script se niega a correr sin `--entrada-terminada`. Para el **delta** —
cuánto agregan la SD y la radio — no hace falta: el par intercalado cancela lo
que haga el geófono.

## Convenciones que costaron caro

- **Unidades**: los scripts Python de banco hablan en mV físicos del tap
  (vía `escala_banco.py`); el firmware de control en `ctl_dc` (dominio del ADC,
  ~x20 más chico). No mezclar pendientes entre ambos.
- **Un riel puede caer dentro de la ventana válida**: la saturación se prueba
  porque el tap no responde a su actuador, no por el valor.
- **Esperar varias τ** (τ del pasabanda ~30–45 s) antes de medir una pendiente o
  afirmar histéresis.
- Los documentos marcados SUPERADO / NO USAR se conservan como historia.
- **Un pico a pico de 0,0 mV no es quietud**: con una sola muestra valida
  `max-min` da cero. Exigir la ventana llena antes de creerle.
