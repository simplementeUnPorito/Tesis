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

## Convenciones que costaron caro

- **Unidades**: los scripts Python de banco hablan en mV físicos del tap
  (vía `escala_banco.py`); el firmware de control en `ctl_dc` (dominio del ADC,
  ~x20 más chico). No mezclar pendientes entre ambos.
- **Un riel puede caer dentro de la ventana válida**: la saturación se prueba
  porque el tap no responde a su actuador, no por el valor.
- **Esperar varias τ** (τ del pasabanda ~30–45 s) antes de medir una pendiente o
  afirmar histéresis.
- Los documentos marcados SUPERADO / NO USAR se conservan como historia.
