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

## Pendiente

- **FTM:** el responder del maestro rechaza todas las configuraciones (`FTM_STATUS_CONF_REJECTED`), tanto con el flag puesto en caliente como reiniciando el WiFi.
  - El prototipo que si mide (ftm-test) corre ESP-IDF 5.5; aca es Arduino 2.0.17 (IDF 4.4).
  - Probablemente requiere migrar a Arduino 3 (IDF 5). Hay que decidirlo.
  - La distancia y la sincronizacion por FTM quedan sin probar.
- **Nodo 3:** reprogramarlo (firmware viejo, sin simulador).
