# Banco S3 sin hardware (2026-10-24)

**Montaje:** maestro ESP32-S3 grabado por USB (COM14, puente CH343) y esclavos ESP32-S3 sin placa, actualizados por OTA a traves del maestro. Los esclavos no tienen PSoC ni SD: `sim_psoc` responde el protocolo real del PSoC por el mismo parser I2C, y `sim_sd` usa LittleFS como SD. Todo el codigo de simulacion esta detras de `SIM_SIN_HW` y solo se activa en `slaveS3`.

La PC queda en GeoNetwork por WiFi y con internet por cable.

**Nodos:**
- Nodos 2 y 4: con el simulador.
- Nodo 3: aparece a veces con firmware viejo sin PSoC. Queda afuera de las capturas sin tirarlas.

## Herramientas (`lab/s3`)

| Script | Uso |
|---|---|
| `maestro_ws.py` | Cliente WebSocket igual a la web; `estado` lista nodos y textos |
| `captura_ws.py` | Captura de punta a punta: lotes por `seq`, huecos NaN, FILL como la web, DROPTEST, marcas |
| `ota.py` | OTA de un nodo por el maestro (sube, ofrece, sigue el estado) |
| `log_maestro.py` | Log humano del maestro por la UART0 (`masterS3_log`); incluye el log remoto de los esclavos (`[Sn>]`) |
| `ftm_registro.py` | Reportes FTM y calibracion de distancia contra cinta |
| `a_kit_firmas.py` | Pasa capturas al formato de `lab/ruido_firmas` |
| `verificar_firmas.py` | Compara las firmas estimadas con la verdad del simulador |

## Fallas encontradas y corregidas

1. **El esclavo descartaba todo lo del maestro S3.**
   - **Causa:** el S3 arma la MAC de su AP prendiendo el bit de administrada localmente (`e2:..` contra `e0:..`), y el filtro solo toleraba una diferencia en el ultimo byte.
   - **Arreglo:** el filtro acepta las dos formas.
2. **La OTA volvia a la imagen anterior a los 180 s.**
   - **Causa:** el esclavo confirma cuando oye al maestro, y en reposo el maestro no le manda nada.
   - **Arreglo:** el maestro contesta a todo nodo que informa "sin confirmar".
   - **Resultado:** 1,1 MB en ~7 s, confirmada en ~4 s.
3. **Un nodo salteado en HOT_WAIT tiraba la captura de los demas**, porque su rechazo de START y sus NACK tardios abortaban todo. Ahora queda fuera de la mascara de la captura.
4. **La descarga clasica perdia un pedido de cada dos.**
   - **Causa:** `esp_now_send` devolvia `ESPNOW_NO_MEM`, con la cola de TX del WiFi ocupada por el TCP del WebSocket.
   - **Arreglo:** el REQ_BATCH se reintenta a los 2 ms.
   - **Resultado:** 300 lotes x 2 nodos pasaron de 100 s a 11-16 s.
5. **Las confirmaciones del tiempo real fallaban por la misma cola llena** y el esclavo frenaba por falta de confirmacion. Ahora el STREAM_ACK se reintenta desde `loop()`.
6. **El relay a la web vaciaba el buffer con cada cabecera de lote y cada marca:** mensajes de 22 B en promedio. Ahora solo los paquetes de control salen al instante.
   - **Resultado conjunto de 5 y 6:** tiempo real de 600 lotes, de 37 s a 7,5 s, que es lo que dura la captura.
7. **Descarga rapida con 23 % de lotes perdidos.**
   - **Causa:** las dos mitades del lote salian pegadas.
   - **Arreglo:** cada una espera el aviso de envio de la anterior.
   - **Resultado:** 0 rellenos.
8. **Ocupado despues de una captura en vivo:** el esclavo quedaba "ocupado" hasta el proximo ARM y la OTA se rechazaba. `ota.py` manda ARM + STOP antes de ofrecer.
9. **Diagnostico remoto:** el log del esclavo se replica al maestro por ESP-NOW (`remote_log.h`). El HOTWAIT_ACK lleva el motivo del NACK.

## Resultados (2 esclavos simulados, 2026-10-24 20:30)

| Modo | Tiempo total | Resultado por nodo |
|---|---:|---|
| Asincronico RAM, 300 lotes | 11 s | 9000/9000 (una vez el nodo 4 dio 0; no se repitio en 3 intentos) |
| Asincronico SD, 300 | 13 s | 9000/9000 |
| Descarga rapida, 300 | 6 s | 9000/9000, 0 rellenos |
| Tiempo real, 600 | 7,5 s | 18000/18000 |
| Tiempo real SD, 600 | 7,5 s | 18000/18000 |
| Tiempo real con 1 de cada 7 lotes descartado (DROPTEST) | 7,5 s | 18000/18000, 85 recuperados con FILL |
| Tiempo real sin limite, STOP a los 15 s | 15,5 s | 1290 lotes, sin huecos |
| FTM pausado (asincronico) | 12 s | 9000/9000 |
| Radio apagada (asincronico) | 12,5 s | 9000/9000 |

**Integridad:** la senal simulada es determinista. En la corrida con DROPTEST las muestras sin artefacto son identicas a las de una corrida limpia (diferencia 0), asi que los lotes recuperados caen en su lugar.

## Firmas de ruido

Son 8 capturas en tiempo real con SD (`lab/ruido_firmas/capturas/SIM_S3`). Las plantillas estimadas con `firmas.py` (pasa-altos de 150 Hz) sobre los datos que recorrieron toda la cadena coinciden con la verdad inyectada:

| Fuente | Correlacion | Amplitud est./verdad | Desfase |
|---|---:|---:|---:|
| I2C | 0,960 | 1,00 | 0 |
| SD_IO | 1,000 | 1,00 | 0 |
| RADIO_TX | 1,000 | 1,00 | 0 |
| AP_BEACON | 1,000 | 0,99 | 0 |

Las fuentes sin artefacto inyectado dan picos chicos: SD_SYNC 184 cuentas y MASTER_RX 38, contra miles de las otras.

**Limpieza:** con la senal simulada original (+-400 000 cuentas) no se puede evaluar, porque la interpolacion sobre marcas tan densas (I2C en el 23 % de las muestras) mete mas error de alta frecuencia que el que saca. El simulador paso a una amplitud de geofono quieto (2000 + 1000 cuentas) para repetir la evaluacion.

## Fallas corregidas despues del primer informe

10. **Los esclavos reescaneaban canales** tras 45 s sin ESP-NOW del maestro y quedaban sordos unos segundos: se perdia el ARM/PRESTART de la captura siguiente y faltaba un nodo entero, de forma intermitente. Ahora las balizas del AP del maestro cuentan como senal de vida. Resultado: 0/3 fallas con 60 s de reposo antes de cada captura.
11. **Compresion maestro -> web:** registro 0x57 con el lote GeoZ (opt-in `ZWEB`). Bajo de ~270 a 63 B por lote. El USB/MATLAB sigue con paquetes de 6 bytes.
12. **Descarga clasica comprimida:** un MsgDataZ por lote en vez de dos MsgData de 167 B (bit0 de `REQ_BATCH.flags`).

## Firmas con senal realista (2000 + 1000 cuentas)

Son 8 capturas en tiempo real con SD y lotes comprimidos a la web (`capturas/SIM_S3_q`).

**Plantillas contra la verdad:** correlacion 1,000 y amplitud 1,00 en I2C, SD_IO, RADIO_TX y AP_BEACON, con desfase 0. SD_SYNC y MASTER_RX quedan en 72 y 16 cuentas.

**Limpieza** (`limpieza.py`):

| Fuente | Metodo | Alta frecuencia explicada | Error de senal |
|---|---|---:|---:|
| RADIO_TX | interp | 73 % | 0,037 |
| SD_IO | interp | 36 % | 0,140 |
| I2C | interp | 28 % | 0,061 |
| AP_BEACON | interp | 4 % | 0,014 |
| MASTER_RX | ninguno | 0 % | 0 |

Elige interpolar y no restar la plantilla: la plantilla se aprende con pasa-altos de 150 Hz y no tiene la parte lenta de los artefactos largos (rampa de la SD, escalon de la baliza).

## Prueba desde la web real (Chrome, field-study-42)

Tres capturas lanzadas con los botones de la pagina (ARM + START), con lotes comprimidos a la web:

| Captura | Muestras | Esperadas |
|---|---:|---:|
| Tiempo real, 5 s | 26 040 | 434 lotes x 30 x 2 nodos |
| Asincronica, 3 s | 15 660 | 261 x 30 x 2 |
| Descarga rapida, 3 s | 15 660 | 261 x 30 x 2 |

En una primera corrida un nodo quedo afuera con `motivo=2` (en vivo, el PSoC simulado no confirmo despues del `SET_RECLEN` de la web). Ahora el esclavo reintenta una vez la secuencia SD + modo en vivo + SETN antes de abortar, y registra que paso fallo.

## Cuanto dura el tiempo real

Prueba con `prueba_duracion.py`, 2 nodos, N=1 (2604 Hz, 87 lotes/s por nodo), sin limite:

| Duracion | Lotes por nodo | Atraso | Crecimiento del atraso | Vaciado tras STOP |
|---:|---:|---|---:|---:|
| 5 min | 26 030 | ~15 lotes (0,17 s) | -0,01 lotes/s | 1 s |
| 14 min | 72 908 | 11-29 lotes (0,1-0,3 s) | -0,004 / +0,025 lotes/s | 1 s |

**Conclusion:** a tasa completa el tiempo real se sostiene indefinidamente con 2 nodos, sin decimar.

**Estimacion por tiempo de aire** (no medida, hay solo 2 placas): cada nodo a N=1 ocupa ~9-10 % del canal a 1 Mbps.
- Entran ~5-6 nodos a N=1.
- Con 8 GEO + HAMMER conviene N>=2, o subir la tasa PHY de ESP-NOW (6-11 Mbps), que reduce el aire ~6 veces a costa de alcance.

## Evaluacion de Arduino 3 / IDF 5 por FTM (2026-10-24 noche)

Hay entornos nuevos `masterS3_idf5`, `masterS3_idf5_log` y `slaveS3_idf5`, con pioarduino 53.03.13. El codigo compila igual en los dos SDK, con guardas `ESP_ARDUINO_VERSION_MAJOR >= 3` en tres puntos:
- el callback de recepcion de ESP-NOW (`esp_now_recv_info_t`);
- mbedtls 3 (sin el sufijo `_ret`);
- el reporte FTM, que se pide con `esp_wifi_ftm_get_report` / `use_get_report_api`.

Tamano: RAM igual (46 %); flash +180 KB en el esclavo.

Probado en placa:
- El maestro IDF 5 funciona: web, WebSocket, ESP-NOW y OTA.
- La OTA cruzada funciona: un esclavo paso de IDF 4.4 a IDF 5 por radio y confirmo la imagen.

FTM sigue sin medir:

| Maestro | Esclavo | Resultado |
|---|---|---|
| IDF 4.4 | IDF 4.4 | `CONF_REJECTED` |
| IDF 5 | IDF 4.4 | `CONF_REJECTED` |
| IDF 5 | IDF 5 | `NO_RESPONSE` |

Probado sin exito:
- responder habilitado y reinicio del WiFi antes de ESP-NOW;
- 5 combinaciones de tramas y periodo;
- modo promiscuo apagado durante la sesion;
- HT20 en el AP y en la STA.

**Siguiente paso sugerido:** grabar por USB el firmware de `ftm-test` (IDF 5.5) en un maestro y un esclavo para confirmar que estas placas miden FTM. Despues comparar la configuracion WiFi completa (modo, auth, `max_connection`, AP oculto) contra la nuestra.

El banco quedo otra vez en IDF 4.4 (`masterS3_log`, `slaveS3_2`/`slaveS3_4`) y se verifico con un tiempo real de 600 lotes completo.

## IDF 5.5, FTM y START programado (2026-10-25)

El banco corre ahora Arduino 3.3.12 / ESP-IDF 5.5.5 (pioarduino 55.03.312) en `masterS3*` y `slaveS3*`. Los entornos IDF 4.4 quedan como respaldo (`*_idf44`).

**FTM mide** en los tres nodos. Hizo falta:
- pedir el reporte con `esp_wifi_ftm_get_report` fuera de la seccion critica (adentro: reinicios por INT_WDT);
- sacar el volcado de lotes del callback de ESP-NOW del maestro a `loop()`: con el trabajo pesado en la tarea WiFi el maestro perdia el lado AP (HTTP, WebSocket y responder FTM).

**START programado por FTM:**
- El maestro manda una baliza de su reloj MAC (2 Hz, `CMD_TIME_BEACON`).
- Cada esclavo ajusta una recta reloj local / reloj del maestro con las ultimas 16 sesiones FTM.
- Si todos los nodos armados tienen modelo valido, el START lleva un instante del reloj del maestro 400 ms en el futuro. Cada esclavo sube SYNC en ese instante.
- **Dispersion entre nodos medida: 0-9 us.** Hay ~15 us de atraso comun a todos (sin explicar, no afecta la sincronia entre nodos).
- La web registra en los metadatos `start_method` = `ftm_scheduled` o `broadcast_start`.

**STOP perdido:** el nodo 2 perdio una vez el STOP broadcast y siguio transmitiendo. El maestro ahora repite el STOP por unicast cada 300 ms a los nodos de tiempo real que no mandaron STREAM_END.

**Panico de los esclavos (nodos 3 y 4):**
- Causa, por coredump: el ARM se atendia en el callback de ESP-NOW (tarea WiFi) y liberaba el anillo de `live_capture` mientras `loop()` retransmitia de el (`LoadProhibited` en `live::sendBatch`). Pasaba con un esclavo retransmitiendo una sesion vieja (por ejemplo tras reiniciar el maestro) cuando llegaba el ARM de la captura siguiente.
- Arreglo: ARM y PRESTART se encolan y se atienden en `loop()`.
- Los esclavos no tienen USB, asi que ahora informan el coredump del ultimo panico por el log remoto a los 20, 40 y 60 s del arranque. Los ELF grabados se guardan en `lab/s3/elf_20261025/` para decodificar con `xtensa-esp-elf-addr2line`.

**Tiempo real en IDF 5.5: el maestro deja de transmitir (esp-idf #19269)**

Sintoma: en tiempo real, a los 1-13 min, el maestro deja de transmitir todo. Se cae el AP (sin ARP ni HTTP; la PC queda en "authenticating"), se corta el WebSocket, las respuestas FTM fallan en todos los esclavos y `esp_now_send` devuelve `NO_MEM` sin fin, sin ningun aviso de envio. La recepcion sigue andando. El detector `[TXSTALL]` (maestro con log) lo marca cuando hay envios pendientes y no vuelve ningun aviso en 5 s.

| Maestro (3 nodos, N=1, 14 min) | Corridas | Con cuelgue |
|---|---:|---:|
| IDF 5.5, cualquier variante (FTM activo o pausado, sin baliza, sin responder, AP 11b/g, lock de lwIP) | 11 | 9 |
| IDF 4.4, mismo codigo (`masterS3_idf44_log`) | 2 | 0 |

Descartado midiendo:
- memoria (157 kB interna, 150 kB DMA en el cuelgue);
- FTM (responder, sesiones y baliza);
- HT/AMPDU (AP en 11b/g);
- escaneo de la STA (canal 1, STA sin SSID);
- tomar el core de lwIP alrededor de `esp_now_send`.

**Causa: [esp-idf #19269](https://github.com/espressif/esp-idf/issues/19269)** (Arduino 3.3.12 / IDF 5.5.5, APSTA). ESP-NOW inserta en la cola de TX del WiFi sin `g_wifi_global_lock`; si choca con una trama del SoftAP, la cola queda inalcanzable. Sin respuesta de Espressif ni arreglo. Nosotros lo disparamos mucho mas seguido que el reporte porque mandamos ~30 STREAM_ACK/s.

**Recuperacion probada, no sirve para campo:**
- `esp_wifi_stop/start` no lo destraba.
- `WiFi.mode(WIFI_OFF)` + volver a levantar AP, ESP-NOW y peers si (100-600 ms; `wifiFullReinit`). Pero:
  - la PC tardo 67-115 s en reasociarse y el maestro abandono la captura (13 900 de 72 900 lotes);
  - cada re-init pierde 15-25 kB de heap (180 -> 71 kB en 8 recuperaciones).
- Un primer intento llamaba `MDNS.end()` despues del deinit: panico `LoadStoreError` (corregido).

IDF 5.4 (pioarduino 54.03.21) no trae `esp_wifi_internal_get_mac_clock_time`, de la que dependen la baliza y el START programado.

**START anclado a la recepcion (la sincronia sin FTM)**

La dispersion del START por broadcast no viene del aire (todos reciben la misma trama a la vez) sino de cuando corre el callback en cada esclavo. Con IDF 5, `esp_now_recv_info_t` trae `rx_ctrl->timestamp` (reloj MAC local): el esclavo sube SYNC en recepcion + 20 ms con el mismo timer que el START programado. Medido con el modelo FTM como referencia (`dispersion_start.py`), 3 nodos, 10 STARTs por metodo:

| START | Mediana | Max |
|---|---:|---:|
| Broadcast, SYNC al procesar el paquete (esclavos clasicos) | 152 us | 374 us |
| Programado por FTM (necesita maestro IDF 5.5) | 5 us | 7 us |
| **Broadcast anclado a la recepcion (esclavos S3)** | **5 us** | **10 us** |

Una muestra a 2604 Hz dura 384 us: el broadcast comun ya era submuestra, pero a 50 Hz sus 374 us son 6,7 grados de fase; el anclado deja 0,2 grados.

Como el anclado no necesita el responder FTM del maestro, el maestro puede volver a **IDF 4.4** (sin #19269). Se pierde solo la estimacion de distancia por FTM, que era indicativa. La deriva de los relojes del ESP durante la captura no importa: la frecuencia de muestreo la fija el IMO del PSoC (+-1 %), cada nodo por su cuenta.

**Web (field-study-44):**
- Durante la captura la traza filtrada se calcula con un FIR causal, compensando su retardo de grupo; al cerrar se reemplaza por filtfilt sobre la captura completa. El notch y la limpieza de marcas solo se aplican al cerrar.
- CSS para telefono.
- `noise_signatures.json` va en el ZIP y el servidor lo usa para limpiar las marcas.

## Prueba de punta a punta con el telefono emulado (2026-10-25, maestro IDF 4.4, web field-study-47)

La app corrio en un iframe de 412 x 915 px (la ventana de Chrome no se pudo achicar).
- **Vista de telefono:** pestanas en grilla, campos a todo el ancho, START/STOP fijos abajo.
- **Enlace:** ahora se puede guardar solo la URL del servidor, sin red para el maestro. Antes exigia un SSID y eso hacia que el maestro intentara la STA (escaneos). La subida la hace el navegador.
- **Captura -> ZIP -> servidor por Tailscale** (`http://100.105.239.49:8000/ingest`): 3 nodos x 261 lotes = 23 490 muestras. Subido (2,9 MB) y procesado ("listo", 1 captura, 3 nodos). La metadata trae `slave_sync_anchor` y `noise_signatures.json`.
- **App de analisis:** carga los 3 canales (7830 muestras cada uno, sin huecos, con las firmas). Arma el dataset por disparos, asi que sin un nodo HAMMER no lo muestra (los 3 esclavos del banco simulan GEO). Ahora lee la sincronia de la metadata raiz del ZIP.
- **Filtro en vivo, medido en el canvas** (FIR pasabajos de 10 Hz, 101 taps, tiempo real): durante la captura la traza filtrada avanza junto con la cruda (52 -> 178 px en 8 s, mismos bordes), asi que el retardo de grupo queda compensado. Al cerrar se reemplaza por filtfilt.

## Pendiente

- **Maestro en IDF 4.4** (`masterS3_idf44` / `_idf44_log`) para campo; IDF 5.5 solo para medir distancia por FTM fuera del tiempo real, hasta que Espressif arregle #19269.
- **Prueba de punta a punta** captura -> web -> ZIP -> servidor por Tailscale, con el telefono emulado en Chrome.
