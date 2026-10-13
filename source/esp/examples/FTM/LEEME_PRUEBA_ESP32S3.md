# LEEME: prueba Wi-Fi FTM con dos ESP32-S3

Esta carpeta conserva una copia exacta de los ejemplos oficiales de Arduino-ESP32 para Wi-Fi Fine Timing Measurement (FTM), fijada al commit [`14095487f6628807ae92b22ff268f12ea51559ad`](https://github.com/espressif/arduino-esp32/commit/14095487f6628807ae92b22ff268f12ea51559ad). Los sketches están en `FTM_Responder/` y `FTM_Initiator/`; no fueron modificados. Los hashes y las URL de origen están en `MANIFEST.json`.

## Qué se necesita

- Dos placas ESP32-S3 compatibles, cada una con su cable USB de datos.
- Arduino IDE.
- El paquete de placas `esp32` de Espressif Systems.
- No hacen falta pines externos soldados ni conexiones entre placas para esta prueba inalámbrica: si ambas placas admiten alimentación, carga y consola por sus conectores USB integrados, basta conectarlas por USB al computador.

La compatibilidad concreta depende de la placa, su conector y su circuito USB. Algunas placas usan USB nativo; otras, un puente USB-UART; otras tienen más de un conector. La selección de puerto, el modo de carga, `USB CDC On Boot` y la posible necesidad de pulsar BOOT/RESET dependen del modelo. Consulte la documentación de su placa. Espressif documenta para ESP32-S3 con USB CDC `USB CDC On Boot -> Enabled` y `Upload Mode -> UART0 / Hardware CDC`, pero esas opciones no sustituyen la configuración específica de la placa.

## Instalar el soporte ESP32 en Arduino IDE

1. Abra **Archivo/Preferencias** (o **Arduino IDE/Settings**, según el sistema).
2. En **Additional Boards Manager URLs / URLs adicionales de gestor de placas**, agregue la URL estable oficial:

   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`

3. Abra **Tools/Herramientas > Board/Placa > Boards Manager/Gestor de placas**.
4. Busque e instale el paquete **esp32** de **Espressif Systems**.
5. Reinicie Arduino IDE si se lo solicita.
6. Para cada placa, elija en **Tools/Herramientas > Board/Placa** el modelo ESP32-S3 específico. Si su placa no aparece, use **ESP32S3 Dev Module** como alternativa genérica y configure correctamente flash, PSRAM y USB según el fabricante.
7. Seleccione el puerto USB/COM correspondiente.

Fuente oficial de instalación: [Arduino-ESP32 — Installing](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html). Referencia oficial de USB CDC: [USB CDC and DFU Flashing](https://docs.espressif.com/projects/arduino-esp32/en/latest/tutorials/cdc_dfu_flash.html).

## Cargar y probar

### 1. Responder: placa A

1. Abra `FTM_Responder/FTM_Responder.ino`.
2. Seleccione la placa y el puerto de la placa A.
3. Compile y cargue.
4. Abra el monitor serie a **115200 baud**.

El sketch crea un punto de acceso en el canal 1 con FTM habilitado mediante el último argumento `true` de:

`WiFi.softAP(WIFI_FTM_SSID, WIFI_FTM_PASS, 1, 0, 4, true);`

Debe aparecer `Starting SoftAP with FTM Responder support`.

### 2. Initiator: placa B

1. Abra `FTM_Initiator/FTM_Initiator.ino`.
2. Confirme que las credenciales sean idénticas a las del responder.
3. Seleccione la placa y el puerto de la placa B.
4. Compile y cargue.
5. Abra el monitor serie a **115200 baud**.

Los valores oficiales incluidos ya coinciden:

| Ajuste | Valor |
|---|---|
| SSID | `WiFi_FTM_Responder` |
| Contraseña | `ftm_responder` |
| `FTM_FRAME_COUNT` | `16` |
| `FTM_BURST_PERIOD` | `2` = 200 ms |

El initiator se conecta como estación al AP y solicita informes hasta que una sesión falla. En éxito imprime `Distance` en metros a partir de `dist_est` y `Return Time` en nanosegundos a partir de `rtt_est`. Tras un fallo, `setup()` termina y `loop()` solamente espera; reinicie la placa para volver a iniciar la secuencia.

## Compatibilidad y guardas reales del ejemplo

Los comentarios y README incluidos por upstream todavía enumeran ESP32-S2 y ESP32-C3, pero la documentación oficial actual de ESP-IDF confirma que ESP32-S3 admite FTM como **initiator en modo STA** y **responder en modo AP**: [ESP32-S3 — Fine Timing Measurement](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-guides/wifi-driver/security-and-roaming.html#fine-timing-measurement-ftm).

Los sketches `.ino` no incluyen una guarda de compilación de capacidad FTM, como `SOC_WIFI_FTM_SUPPORT`. Los archivos `ci.yml` sólo requieren `CONFIG_SOC_WIFI_SUPPORTED=y` o `CONFIG_ESP_HOSTED_ENABLED=y`, que no garantizan por sí solos soporte FTM. En el initiator, la única guarda `#if ESP_IDF_VERSION < ESP_IDF_VERSION_VAL(6, 0, 0)` decide si se libera `ftm_report_data`; es una diferencia de versión/propiedad de memoria, no una comprobación de capacidad FTM. Por eso debe seleccionar una placa/SoC compatible y no confiar en que el sketch rechace automáticamente cualquier destino incompatible.

## FTM RTT no es sincronización de relojes

Esta prueba mide **Wi-Fi Round Trip Time (RTT)** y usa ese tiempo de ida y vuelta para estimar distancia. No sincroniza los relojes de las dos placas. Los sketches oficiales no comparan frecuencia de osciladores, no calibran ni disciplinan un oscilador y no implementan un contador disciplinado. Si el objetivo posterior es sincronización de reloj o disciplina de frecuencia, hace falta otro protocolo y otra lógica de estimación/control.

La distancia RTT es una estimación y puede variar por interferencia RF, multitrayecto, orientación de antenas y falta de calibración. No se promete precisión ni rendimiento de hardware.

## Estado de validación

Se verificaron estructura, bytes y SHA-256 contra los blobs del commit fijado. **No se instaló software y no se realizó compilación, carga ni validación con hardware.**

---

> Proveniencia: guía generada por Codex el 2026-10-05 a partir de fuentes oficiales de Espressif; ejemplos descargados sin cambios desde `espressif/arduino-esp32` commit `14095487f6628807ae92b22ff268f12ea51559ad`. Validación limitada a inspección y hashes; sin prueba de compilación ni hardware.
