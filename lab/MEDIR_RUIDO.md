# Cómo medir el ruido que meten la SD y la radio

Guía para repetir las mediciones de octubre de 2026 con una placa nueva. Todo
corre desde la PC con el ESP esclavo por USB (y el maestro para recepción); el
PSoC mide con su propio ADC a través del MUX. Bitácoras de referencia:
`RUIDO_SD_2026-10-19.md` (SD) y `RUIDO_RF_2026-10-20.md` (radio).

## Firmware necesario

| Equipo | Rama mínima | Qué aporta |
|---|---|---|
| PSoC | `exp/ruido-wifi` | `sdprobe` (0xAD): modos 0-5 (CS, bus, escritura real) y **modo 7 = ping por I2C** en cada k·150 muestras |
| ESP esclavo | `exp/ruido-wifi` (`SLAVE_LAB_TOOLS_ENABLE`) | comandos de banco (tabla de abajo) |
| ESP maestro | `exp/ruido-wifi` | comando binario `0xC1` (ráfaga ESP-NOW en difusión) |

## Comandos del esclavo (consola USB, 115200)

| Comando | Para qué |
|---|---|
| `view <tap>` | elige el tap que digitaliza la captura: 0 SEo, 1 BP, 2 sumador, 3 SUMo, 4 LPo |
| `pga <c>` / `pgaout <c>` | ganancias (códigos 0-8 = x1..x50) |
| `sdprobe <ms> 58 <modo> [div] [slew]` | arma la sonda del PSoC; `sdprobe 0` desarma |
| `rftest <ms> <periodo> <bytes> [b]` | transmite ESP-NOW; **periodo 0 = en cada ping del PSoC**; con `b` transmite a `FF:FF:FF:FF:FF:FF` sin ACK ni reintentos; informa `#RFTEST t` y `#PING t` (micros) |
| `rfrx <ms>` | registra la llegada de las ráfagas del maestro (`#RFRX t`) |
| `txpower <dBm>` | potencia máxima (2-21; el ESP32 la limita a 19,5 dBm) |
| `radio off` / `radio on` | apaga y prende WiFi + ESP-NOW sin reiniciar (no resetea el PSoC) |
| `radiosil on` / `radiosil off` | silencio de radio automático durante el muestreo (desactivado por defecto) |
| `espsd <ms> <cada_lotes>` | SD conectada al ESP (HSPI: SCK 14, MOSI 13, MISO 32, CS 25) |
| `sddiag`..`sddiag9` | diagnóstico de bajo nivel de esa SD |
| `sdinfo` | reinicializa la SD del PSoC (hacerlo antes de usar `sdprobe` 4-5) |

El pulso de disparo para el osciloscopio sale por **GPIO4** del esclavo en cada
transmisión de `rftest` (~200 µs).

## Medir: `lab/ruido_sd.py correr`

```
python lab/ruido_sd.py correr --port COM8 [--maestro COM6] --raiz <carpeta> \
    --exp <nombre> --cond <C1> <C2> ... --rep 3 --pga 3 --pgaout 4 --tap 4 --nota "<condiciones físicas>"
```

Condiciones disponibles:

| Condición | Qué hace | Marcas |
|---|---|---|
| `BASE` | captura sin estresor (control) | posiciones fijas k·150 |
| `P<modo>[D<div>][S<slew>]`, `REAL` | sonda de la SD del PSoC | k·150 |
| `PING` | solo los pings I2C del PSoC (control de los demás) | k·150 |
| `RF<bytes>[P<dBm>][T<ms>][B]` | transmisión ESP-NOW; sin `T`, en cada ping; `T` fija periodo de 1-10000 ms; `B` usa difusión sin ACK ni reintentos | muestra exacta (interpolada entre pings) |
| `RX` | ráfagas del maestro (requiere `--maestro`) | muestra exacta |
| `OFF` | captura con la radio apagada | k·150 |
| `SIL` | `radiosil on`: el firmware calla la radio al entrar en SAMPLING y la prende al salir (modo de campo propuesto) | k·150 |
| `ESD` | SD en el ESP escribiendo | lotes (aproximado) |

El script espera que el lazo converja después de fijar la ganancia, verifica
antes de cada captura que no esté aprendiendo, alterna las condiciones en
orden ABBA y guarda cada volcado con su metadato.

## Campaña completa con un comando: `lab/campana_ruido.py`

```
python lab/campana_ruido.py correr --plan rf --raiz lab/ruido_rf_<fecha> --port COM8 --maestro COM6 --nota "<placa, alimentación>"
python lab/campana_ruido.py correr --plan sd --raiz lab/ruido_sd_<fecha> --port COM8
python lab/campana_ruido.py resumir --raiz <carpeta>      # escribe campana.md
```

Los planes `rf` (W1, W1b, W3b, W4b/W5, W5 por tap, W9 ganancia) y `sd` vienen
embebidos; `--plan archivo.json` acepta uno propio y `--solo W5,W9` filtra
pasos. Cada paso llama a `ruido_sd.py correr` y después a `resumir` y
`espectro_condiciones.py`. Si la placa no escribe nada en 6 min
(`--silencio-min`) se mata el paso, se espera que el puerto reaparezca y se
reintenta una vez; los pasos con RX se saltean si falta el maestro. El estado
queda en `campana_estado.json`, así que repetir el comando reanuda.

Figuras de la radio: `python lab/figuras_informe_rf.py --raiz <carpeta>`.

## Analizar

| Script | Qué da |
|---|---|
| `ruido_sd.py resumir <dir>` | brote promedio sincronizado por condición: p2p, energía, gráfico `bursts_conjunto.png`; descarta capturas que tocan un riel |
| `espectro_condiciones.py <dir>` | RMS y PSD por condición, líneas espectrales (baliza 9,77 Hz, 17,36 Hz...) para efectos sin evento |
| `sustraer_brote_rf.py <dir>` | si restar la plantilla del brote (posiciones conocidas) limpia la medición; RMS y PSD 5-50 Hz antes y después |
| `figuras_informe_rf.py` | figuras de la radio: potencia, taps, ganancia, formas, uso real, difusión |
| `piso_ruido_corto.py` | piso de ruido con la entrada en corto |
| `ganancia_ruido_sd.py` | dependencia con la ganancia (dónde entra el ruido) |
| `osc_ruido_sd.py <csv>` | capturas del TDS 2004B alineadas con el disparo |
| `figuras_informe_sd.py` | figuras matriciales del informe |
| `presupuesto_consumo_psoc.py [factor]` | consumo del lado analógico para dimensionar el DC-DC aislado |

## Reglas que costaron caro

- Entrada en corto y ganancias fijas; tras cambiar ganancia, esperar
  convergencia (el script lo hace). Una captura que toca un riel no vale.
- Si una condición satura (transmisión WiFi a ganancia x8·x16), medir en un tap
  anterior o con PGAout x1, no subir el umbral.
- Abrir el puerto del esclavo lo reinicia y resetea el PSoC: el lazo vuelve a
  aprender. `sdinfo` hace falta otra vez antes de usar la SD del PSoC.
- Con la fuente de laboratorio, unir su GND con el de la placa (referencia del
  SPI) y verificar polaridad con la salida apagada.
