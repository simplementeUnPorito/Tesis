# Handoff: ruido de la SD y de la radio (estado al 2026-10-21, 16:30)

Punto de partida para retomar el trabajo con el contexto necesario. Detalle en
las bitácoras citadas; este archivo dice dónde está todo, qué quedó a medias y
qué se decidió.

## Dónde está

| Qué | Dónde |
|---|---|
| Rama | `exp/ruido-wifi` en el repo padre, `src/firmware/psoc` y `src/firmware/esp32` (todas con push; los submódulos en rama, no en detached HEAD) |
| Bitácora SD | `lab/RUIDO_SD_2026-10-19.md` |
| Bitácora radio | `lab/RUIDO_RF_2026-10-20.md` (W1…W13, radiosil, validación de campo) |
| Firmas y resta | `lab/FIRMAS_RUIDO.md`, `lab/firmas_ruido.py`, firmas en `lab/firmas/` |
| Cómo medir (herramientas y comandos) | `lab/MEDIR_RUIDO.md` |
| Radio durante la captura (firmware) | `lab/RADIO_DURANTE_CAPTURA.md` |
| Datos de banco | `lab/ruido_sd_20261019/`, `lab/ruido_rf_20261020/` (ignorados por git salvo resúmenes) y crudos en Tesis-datos `raw/laboratorio/ruido_{sd_20261019,rf_20261020}` (LFS, con push) |
| Campaña completa pausada | `lab/ruido_rf_20261021_campana/` (estado en `campana_estado.json`) |
| Informe para compartir | https://claude.ai/artifact/81PNs9NcPyHX2MQXpJGXPu (Claude Docs, privado: compartir a mano) |

## Estado del banco

- PSoC (KitProg) con el firmware de `exp/ruido-wifi` (sdprobe modo 7 = ping I2C).
- ESP esclavo en **COM8** (`pio run -e slave2`) con `rftest … [b]`, `rfrx`,
  `txpower`, `radio off|on` y **`radiosil on <ms>` / `radiosil off`**
  (desactivado por defecto; no se guarda en NVS).
- ESP maestro en **COM6** con el comando binario `0xC1` (ráfagas de prueba).
- Ambos a potencia máxima (84 qdBm pedidos, el chip da 78 = 19,5 dBm).
- Entrada en corto; PSoC, esclavo y maestro por USB de la PC.
- microSD del PSoC **dañada** (no responde ni en el lector de la PC): sin ella
  no se pueden repetir los experimentos de SD (`--plan sd`, `sdprobe` 4-5).
- En `src/firmware/psoc` quedan **sin commitear cambios del usuario**:
  TopDesign con LVTTL y artefactos de build (`.cysch/.cyfit/.rpt…`). No tocar
  a mano los `.cysch/.cyfit/.cyprj`.

## Qué se sabe (resumen)

**SD.** Ruido conducido por la corriente de la tarjeta en la masa común; la
referencia del PSoC sigue a la masa. Con el PSoC en un cargador aislado el
brote baja 5-9×. Su firma es repetible: **restarla saca ~90 % del exceso sin
distorsionar la señal** (`FIRMAS_RUIDO.md`).

**Radio (esclavo).**
- Una trama ESP-NOW mete 4× el ruido de una escritura SD; entra antes del PGA
  (constante referida a la entrada, ~1,5 mV), escala con la potencia (×6 de 2
  a 19,5 dBm), no con el largo ni el ACK. Conducido por el propio esclavo; lo
  inducido desde el maestro es mínimo (RX ×1,3; la baliza desaparece al
  apagar la radio del esclavo aunque el maestro siga emitiendo).
- **No se resta por software** (≤ 23 % y lo que ajusta más se come la señal).
- En campo el esclavo **no transmite durante el muestreo** (store-and-forward;
  HELLO/STATUS suspendidos) y el PSoC no habla por I2C durante la captura. Lo
  que sí llega es la **radio encendida en reposo** (baliza de 102,4 ms):
  **×2,5 en 5-50 Hz**. La baliza no es constante referida a la entrada (crece
  ×4 de PGA x1 a x16): parte entra después del PGA.
- **`radiosil on 500`**: apaga WiFi + ESP-NOW al entrar en SAMPLING y arranca
  el PSoC 500 ms después (campo: SYNC por `esp_timer`; banco: `delay` antes de
  `psoc.startNow`). Sin demora mete un transitorio de ~200 ms que lleva
  capturas al riel; 250 ms no alcanza; 500 sí. Banco: banda útil ×0,31.
  Campo (lo que recibe el maestro): **44/44 capturas completas, banda útil
  ×0,60 de media** (0,46-0,70), baliza ×0,17-0,30.
- Capturas largas: el esclavo recorta N a la RAM libre del ESP (384-448 lotes
  con 500 pedidos); no se pierden datos.

## Pendiente

1. **Terminar la campaña completa** (pausada en 15/21; faltan el resto de
   W11, W12c, W12e y W13 ×3, ~45 min). Mismo comando, retoma sola:
   ```
   python lab/campana_ruido.py correr --plan rf --raiz lab/ruido_rf_20261021_campana --port COM8 --maestro COM6 --nota "entrada en corto, PSoC por USB, ESP esclavo y maestro por USB, potencia max (78 qdBm); campana completa de validacion de la herramienta"
   ```
   Opcional: reintentar W5 (se colgó dos veces en la captura RX r23; el
   maestro seguía conectado) con `--solo W5_lpo_pgaout1 --rehacer`; ahora
   `ruido_sd.py` vuelca la pila si una captura pasa de 4 min y el puerto del
   maestro tiene `write_timeout`. Después:
   `python lab/comparar_campanas.py lab/ruido_rf_20261020 lab/ruido_rf_20261021_campana`
   (para la radio comparar el RMS en banda, no el p2p del brote promedio, que
   no se repite entre corridas).
2. **Decisiones del usuario:**
   - ¿`radiosil on 500` por defecto en todos los nodos? (cuesta 0,5 s entre
     START y muestreo; el golpe del martillo tiene que esperarlo).
   - ¿Tope fijo de lotes para capturas a RAM? (hoy el recorte varía con la
     fragmentación del heap).
3. **Banco (lo hace el usuario):** osciloscopio disparado por GPIO4 del
   esclavo durante una transmisión (W6, origen del escalón de 20 ms); PSoC en
   el cargador aislado mientras el esclavo transmite (W7a: si el brote cae
   5-9× como con la SD, es conducido por la masa compartida); antena del
   esclavo alejada o blindada (W7b); microSD nueva.
4. **Placa nueva:** aislar alimentación y masa digital (UCC33420 propuesto;
   ISO1640 + ISO7741 para comunicaciones; ver el informe). Con la placa:
   `campana_ruido.py --plan rf` (y `sd` con SD), `firmas_ruido.py extraer
   --todas`, `evaluar --todas`, `baliza`, y `comparar_campanas.py` contra
   `lab/ruido_rf_20261020`.

## Cosas que costaron caro (no repetir)

- Abrir el puerto del esclavo lo reinicia y resetea el PSoC: el lazo vuelve a
  aprender y el esclavo tarda ~50 s en unirse a la red (la prueba con el
  maestro ahora espera HELLO antes de ARM).
- `startwait` (banco) arranca el PSoC por UART, no por SYNC: lo que se haga en
  el camino del SYNC no actúa en el banco.
- No llamar `esp_wifi_stop`/`esp_now_deinit` desde el callback de recepción
  ESP-NOW: radiosil lo difiere al loop.
- En capturas con radio el promedio sincronizado necesita la muestra exacta de
  cada evento: se interpola entre los pings I2C del PSoC (sdprobe modo 7).
- El worker de Codex corta a ~5 min: darle tareas chicas con ubicación exacta
  (archivo:línea), sin exploración.
