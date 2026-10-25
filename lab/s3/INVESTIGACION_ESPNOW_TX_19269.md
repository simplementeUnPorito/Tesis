# Investigación ESP-NOW / cola TX en ESP32-S3, IDF 5.5.5

Fecha: 2026-10-25. No se modificó el firmware ni se accedió a COM14.

## Conclusión ejecutiva

Está **verificado en los binarios instalados** que el camino de `esp_now_send()` inserta en `s_tx_cacheq` sin `g_wifi_global_lock`, mientras el consumidor `ieee80211_output_process()` retira la cabeza bajo ese lock. La inserción es una operación de lista enlazada de varios pasos y puede perder un nodo si se intercala con la extracción del último nodo.

También está **verificado** que `esp_wifi_80211_tx()` termina en la misma `ieee80211_post_hmac_tx()` y la misma `s_tx_cacheq`, pero mantiene `g_wifi_global_lock` desde antes de reservar/describir el buffer hasta después de la inserción. Por lo tanto, armar la action frame ESP-NOW sin cifrar y enviarla con `esp_wifi_80211_tx()` **esquiva específicamente la carrera observada**.

No es una garantía absoluta contra todo wedge del driver: el pool de buffers y `pp_post()` siguen siendo compartidos; además, el binario ignora el retorno de `ieee80211_post_hmac_tx()` en el camino raw. Hay que usar callback TX, un solo frame en vuelo y watchdog.

## Alcance y artefactos

Binarios analizados, todos con revisión embebida `b9f67df`:

| Archivo | SHA-256 |
|---|---|
| `libnet80211.a` | `ACF1AF8D20976E3C4792094B7EB67C5CE1DC47EA92124E572B8603EC08DB23E3` |
| `libespnow.a` | `49A1542162166CA6AB161F4FDE03C66B3FDF43D30D760098C77634A5B0E0B925` |
| `libpp.a` | `F0ADB57A8377F4C18909B58BC261F842FDB5EC15F1C5FE53C98A8328FD299A1D` |
| `libcore.a` | `880414563990CAFFF3EB825382CE01341DDD1E6505EA0FCADCC3AD3CF700BFDE` |

Herramienta: GNU `xtensa-esp-elf-objdump` 2.43.1. Las direcciones citadas son offsets relocatables dentro de la sección del objeto, no direcciones finales de runtime.

## VERIFICADO: ruta ESP-NOW y carrera

Ruta de símbolos:

```text
libespnow.a:espnow.o       esp_now_send +0xca/+0x126 -> mt_send
libespnow.a:manatick.o     mt_send +0xe7             -> ieee80211_send_action_vendor_spec
libnet80211.a:...vendor.o  ...send_action... +0x24   -> construct_action_vendor_spec
                           ...send_action... +0x2e   -> ieee80211_post_hmac_tx
libnet80211.a:...output.o  ieee80211_post_hmac_tx    -> s_tx_cacheq + pp_post(5)
```

En `ieee80211_construct_action_vendor_spec`, `g_wifi_global_lock` se toma alrededor de la búsqueda del peer y la construcción (`+0x9d` carga el lock, llamada de lock en `+0xad`; unlock en `+0x34d..+0x35d`). La función retorna y recién después `ieee80211_send_action_vendor_spec +0x2e` llama a `ieee80211_post_hmac_tx`. No hay adquisición del lock entre ambas llamadas.

La inserción sin lock está en `.wifiextrairam.2`:

```text
ieee80211_post_hmac_tx +0x38  carga &s_tx_cacheq
                         3b   nodo->next = NULL
                         3d   carga queue->tail
                         41   *queue->tail = nodo
                         48   queue->tail = &nodo->next
                         4b   pp_post(evento 5)
```

El consumidor, `.wifi0iram.8:ieee80211_output_process`, toma `g_wifi_global_lock` en `+0x93..+0x9e`, retira la cabeza en `+0xa4..+0xaa`, y si quedó vacía repone el tail en `+0xaf`; libera el lock en `+0xb1..+0xbb`.

La secuencia peligrosa es compatible con la hipótesis del issue: productor lee el tail viejo; consumidor retira el último nodo y reinicia head/tail; productor escribe a través del tail viejo y deja el nuevo nodo desconectado. Ese buffer no llega a `ppTxPkt`, no genera callback y queda retenido.

## VERIFICADO: `esp_wifi_80211_tx()` usa la cola, pero correctamente bloqueada

`libnet80211.a:ieee80211_output.o`, `.text.esp_wifi_80211_tx`:

```text
+0x3f  ieee80211_raw_frame_sanity_check
+0x4f  carga g_wifi_global_lock
+0x54..+0x59  lock()
+0x62  ic_ebuf_alloc(buffer, len, 1)
+0xb3  ic_get_80211_tx_rate(ifx)
+0x117 ieee80211_post_hmac_tx(eb)
+0x11d..+0x127 unlock()
```

Resultado: pasa por `ieee80211_post_hmac_tx`/`s_tx_cacheq`, pero la inserción queda serializada con el consumidor. También serializa múltiples emisores raw entre sí. Respecto de **esta carrera concreta**, el camino es seguro.

Dos salvedades binarias:

- Si `ic_ebuf_alloc` falla, este objeto retorna `0x101` (`ESP_ERR_NO_MEM`), aunque el header documenta `ESP_ERR_WIFI_NO_MEM`.
- El retorno de `ieee80211_post_hmac_tx()` no se copia al valor devuelto: después de llamarla, se libera el lock y se retorna el resultado anterior (`ESP_OK`). Si `pp_post()` falla, raw puede devolver OK sin garantía de callback. La inserción ya ocurrió, así que otro evento podría igualmente drenar el nodo.

La configuración instalada usa, según variante, buffers TX estáticos/cache (`8`/`16`) o dinámicos (`32`). No hay un límite separado visible de `s_tx_cacheq`: el límite práctico es el pool de `esf_buf` más la cola de eventos de `ppTask`.

## VERIFICADO: formato exacto que arma esta versión

Para payload de hasta 250 bytes, el buffer pasado a `esp_wifi_80211_tx()` debe ser:

```text
Offset  Tamaño  Contenido
0       2       Frame Control = D0 00 (Management / Action, ToDS=0, FromDS=0)
2       2       Duration = 00 00
4       6       addr1 = MAC destino
10      6       addr2 = MAC propia de la interfaz elegida
16      6       addr3 = FF FF FF FF FF FF
22      2       Sequence Control = 00 00 si en_sys_seq=true
24      1       Category = 7F
25      3       OUI exterior = 18 FE 34
28      4       Random value (32 bits; variar en cada trama)
32      1       Element ID = DD
33      1       Length = payload_len + 5
34      3       OUI del IE = 18 FE 34
37      1       Type = 04
38      1       Reserved/More/Version = 02 para último IE
39      N       Payload ESP-NOW original
```

Longitud entregada a raw: `39 + N`; no se incluye FCS, que agrega el hardware.

Evidencia:

- `ieee80211_construct_action_vendor_spec +0x1a9`: escribe `0x00d0`; `+0x1af`: duration 0.
- `+0x1b4..+0x1c1`: copia destino a `addr1`; `+0x1c4..+0x1cd`: MAC obtenida por `wifi_get_macaddr(ifx)` a `addr2`; `+0x1d0..+0x1db`: copia `ieee80211_ethbroadcast` a `addr3`.
- `ieee80211_add_action_vendor_spec_esp +0x0f..+0x18`: category 127; rodata `18 fe 34`; `+0x30..+0x50`: random de `ic_get_random`, evitando repetir el anterior.
- `ieee80211_add_ie_vendor_esp_now`: ID `0xdd`, largo `N+5`, OUI `g_espnow_user_oui`, type 4, byte final `0x02`.
- `g_espnow_user_oui` inicial = `18 fe 34`; `g_mt_version` = `2`.

Para payloads mayores a 250 se concatenan IEs de hasta 250 bytes. En todos menos el último, el byte Reserved/More/Version es `0x12`; en el último es `0x02`. La fórmula es:

```text
24 + 8 + sum(7 + chunk_len), con chunk_len <= 250
```

El límite público raw es 1500 bytes. Por eso el máximo payload ESP-NOW v2 reproducible es **1426 bytes** (seis IEs), no los 1470 admitidos por `esp_now_send()` interno.

No usar `esp_now_set_user_oui()` si se desea compatibilidad exacta; si ya se usa, el OUI interior debe coincidir con el configurado en receptores.

### Direcciones por interfaz

No dependen de asociación:

| Peer/interfaz | addr1 | addr2 | addr3 |
|---|---|---|---|
| `WIFI_IF_STA`, STA no asociada | destino | MAC STA del maestro | broadcast |
| `WIFI_IF_AP` | destino | MAC SoftAP del maestro | broadcast |

En `WIFI_AP_STA`, para imitar los peers actuales `WIFI_IF_STA`, usar la MAC STA en `addr2` y llamar `esp_wifi_80211_tx(WIFI_IF_STA, ..., true)`. El filtro de los esclavos por MAC de origen seguirá viendo esa MAC.

## VERIFICADO: recepción por `esp_now_register_recv_cb()`

La recepción no distingue si el transmisor llamó a `esp_now_send()` o a raw. `ieee80211_recv_action_vendor_esp_now` valida:

- OUI exterior `18:fe:34` (`+0x39..+0x48`);
- cada IE `0xdd`, longitud válida y OUI interior (`+0x90..+0xc2`);
- type `4` (`+0xc5..+0xc8`);
- concatena los cuerpos de múltiples IEs y llama al callback registrado (`+0x121..+0x13e`).

La info entregada al callback se arma con destino desde cabecera `+4` y origen desde cabecera `+10`. Por eso los esclavos IDF 5.5, STA no asociada, canal 1, aceptarán la trama manual sin cambios si está sin cifrar, tiene el formato anterior y `addr2` es la MAC STA esperada.

### Limitación crítica: cifrado

`esp_wifi_80211_tx()` no permite frames cifrados. `ieee80211_raw_frame_sanity_check +0xf3..+0xf6` rechaza el bit Protected, con el texto embebido `invalid frame control, unsupport crypto frame`. No se puede reemplazar por raw un peer ESP-NOW con LMK/encrypt=true usando la API pública. El camino propuesto sirve únicamente para peers sin cifrar.

## VERIFICADO: restricciones y comportamiento de raw TX

- Tipos admitidos: beacon, probe request/response, action y data non-QoS. Action (`D0 00`) está admitida.
- Longitud: 24 a 1500 bytes.
- Interfaz: en APSTA acepta `WIFI_IF_STA` o `WIFI_IF_AP`, siempre que esa interfaz esté iniciada. STA no asociada es válida.
- Usar `en_sys_seq=true`: funciona sin asociación y es obligatorio si más adelante la interfaz queda conectada. El driver sobrescribe Sequence Control.
- La MAC `addr2` debe coincidir con la MAC de la interfaz elegida.
- Tasa: raw llama `ic_get_80211_tx_rate(ifx)`, no `ic_get_espnow_rate()`. Se puede fijar antes de `esp_wifi_start()` con `esp_wifi_config_80211_tx_rate(ifx, WIFI_PHY_RATE_1M_L)` o la API completa `esp_wifi_config_80211_tx()`. Configurar STA y AP por separado si se usan ambas. La tasa ESP-NOW por-peer no aplica al camino raw.
- Callback: existe `esp_wifi_register_80211_tx_cb()`. El callback corre en la tarea Wi-Fi y recibe `des_addr`, `src_addr`, `ifidx`, puntero al frame, tasa y `WIFI_SEND_SUCCESS/FAIL`. El binario guarda un único callback global; registrar otro lo reemplaza.
- El buffer de entrada se copia en `ic_ebuf_alloc`; puede reutilizarse al retornar la llamada.
- Raw no admite el bit Protected, QoS ni varios bits de control/retry/fragmentación puestos manualmente.

## ACK y reintentos: VERIFICADO vs. INFERIDO

**Verificado:** la action frame unicast conserva dirección individual y llega a `ppTxPkt`; la callback raw expone `tx_status`. La documentación de ESP-NOW define success como recepción a nivel MAC, y el driver usa la misma capa PP/LMAC.

**Inferido con alta confianza:** una action unicast raw pide ACK 802.11 y usa los reintentos MAC normales; una dirección broadcast no recibe ACK. No encontré una API pública para fijar el retry count raw. El número exacto de reintentos no queda demostrable desde `libnet80211.a`; reside en `libpp`/LMAC cerrado. Validarlo con sniffer y callback antes de sustituir producción.

## Versiones posteriores y estado upstream

### VERIFICADO

- [Issue #19269](https://github.com/espressif/esp-idf/issues/19269) sigue abierto, asignado y sin respuesta técnica de Espressif al 2026-10-25. No tiene PR ni milestone.
- [Issue #18682](https://github.com/espressif/esp-idf/issues/18682) sigue abierto como bug. Espressif pidió pruebas sobre LR/heap y luego separó el caso de un-frame-en-vuelo a otro ticket; no publicó un fix ni workaround oficial.
- ESP-IDF [v5.5.6](https://github.com/espressif/esp-idf/releases/tag/v5.5.6) salió el 2026-10-16. Sus notas no listan un fix ESP-NOW/TX queue.
- El tag IDF v5.5.6 apunta `components/esp_wifi/lib` al commit público `61bbece9...` de `esp32-wifi-lib`, revisión interna `c6dceae`. Desensamblé ese `libnet80211.a`: `ieee80211_send_action_vendor_spec` sigue llamando a `ieee80211_post_hmac_tx` fuera del lock y `ieee80211_post_hmac_tx` sigue idéntico.
- También desensamblé `esp32-wifi-lib` master público al commit `ec08f0c` del 2026-10-22, revisión interna `5bb751d`: el camino roto sigue idéntico. Por lo tanto, ni 5.5.6 ni el master disponible cuatro días después contienen este arreglo.
- Arduino-ESP32 estable más nuevo es [3.3.12 / IDF 5.5.5](https://github.com/espressif/arduino-esp32/releases/tag/3.3.12). Existe 4.0.0-RC1 / IDF 6.1, pero #18682 contiene una reproducción nativa en 6.1-dev con un solo frame en vuelo; no es una actualización de bajo riesgo ni evidencia de arreglo.
- Pioarduino `55.03.312[-1]` empaqueta Arduino 3.3.12/IDF 5.5.5. No hay una estable posterior con un `libnet80211` corregido identificable al corte.

### SUPUESTO / no probado

- Un futuro binario puede corregirlo sin mencionarlo explícitamente en release notes. La prueba decisiva es desensamblar `ieee80211_send_action_vendor_spec` y verificar lock alrededor de `ieee80211_post_hmac_tx`, no solamente mirar el número de versión.
- Los cambios recientes de FTM/off-channel en master no corrigen esta cola: el desensamblado lo descarta para los artefactos revisados.

## Otras mitigaciones

### VERIFICADO como insuficiente o no equivalente

- Lock de lwIP: no es `g_wifi_global_lock`; no serializa al consumidor ni a productores internos del AP.
- Una sola tarea emisora: elimina concurrencia entre llamadas de aplicación, no la concurrencia con `ppTask`/SoftAP.
- Llamar desde callback Wi-Fi o contexto del consumidor: puede evitar que ese mismo `ppTask` consuma simultáneamente, pero no excluye productores de otro core. Además el callback es de alta prioridad y no debe hacer trabajo pesado. No es una solución verificable.
- Suspender la tarea Wi-Fi: impide el drenaje, no cubre otros productores y usa internals no soportados. Riesgo alto de deadlock/wedge.
- Suspender scheduler/deshabilitar interrupciones en un core: no excluye el otro core.
- `esp_wifi_stop/start`: el pool/cola relevante sobrevive; coincide con el binario y con las reproducciones.

### SUPUESTO razonable

- Tomar directamente `g_wifi_global_lock` desde la aplicación podría cerrar la carrera, pero depende de símbolos/tipos privados y ABI propietario. No lo recomiendo frente a `esp_wifi_80211_tx()`, que ya hace exactamente eso por una API pública.
- Afinar todo al mismo core reduce ventanas, pero no ofrece exclusión mutua y no debe considerarse fix.

## Recomendación ordenada

1. **Prototipo A/B con raw, sólo para peers sin cifrar.** Implementar una función que arme exactamente un IE para payloads `<=250`, `addr2=MAC STA`, `addr3=broadcast`, random nuevo, y llame `esp_wifi_80211_tx(WIFI_IF_STA, frame, len, true)`. Registrar `esp_wifi_register_80211_tx_cb`. Mantener un solo frame raw en vuelo y una FIFO fuera del callback. Riesgo: **medio**; usa API pública y evita la carrera, pero cambia de camino TX y no tiene cifrado.

2. **Prueba de compatibilidad antes del soak.** Con sniffer, comprobar: recepción en `esp_now_register_recv_cb`, MAC origen, payload exacto, tasa, ACK/retries unicast, callback success/fail y broadcast. Probar unicast y broadcast separadamente. Riesgo: **bajo**.

3. **Soak bajo la carga real AP + WebSocket + FTM.** Contar `raw_submit_ok`, callbacks, timeouts, status y máximo en vuelo. Hacer al menos el tiempo/volumen que produjo 9/11 fallas. Un timeout debe detener nuevos envíos y disparar diagnóstico/recovery, no liberar el latch y seguir llenando el pool. Riesgo: **bajo**.

4. **Fijar explícitamente la tasa raw antes de start.** Si se busca equivalencia con ESP-NOW default, usar 1 Mbps long preamble en `WIFI_IF_STA`; confirmar al aire. Riesgo: **bajo**, con costo de airtime alto ya conocido.

5. **Conservar full deinit/init como recuperación secundaria**, con umbral de callbacks perdidos o fallos de alloc consecutivos. Mejorar la secuencia para no acumular heap y aceptar la demora de reconexión. Si el heap no vuelve o la reinit falla, reinicio controlado. Riesgo operativo: **medio/alto**.

6. **Si hay peers cifrados, no usar raw para ellos.** Mantener IDF 4.4 donde ya fue estable, separar tráfico crítico, o esperar/probar un binario de Espressif cuyo desensamblado muestre el lock. Riesgo de migrar a 5.5.6/6.1 esperando un fix: **alto**, porque el defecto sigue presente en los binarios comprobados.

7. **No invertir tiempo en callbacks/contexto/core como supuesto fix.** Pueden bajar frecuencia, no cierran la exclusión mutua demostrada.

## Criterio para aceptar un futuro fix upstream

Aceptar sólo si se cumple al menos uno:

- `ieee80211_send_action_vendor_spec` mantiene `g_wifi_global_lock` durante `ieee80211_post_hmac_tx`; o
- `ieee80211_post_hmac_tx` internamente toma ese lock para todos sus callers; o
- `s_tx_cacheq` cambia a una primitiva atómica/cola thread-safe demostrable.

Después, repetir el soak: la presencia del lock corrige la carrera estructural, pero no prueba por sí sola que no haya otro problema de PP/LMAC.

---

IA principal: Codex, modelo no reportado  
Delegados: ninguno (`ORCHESTRATOR_DEPTH=1`)  
Fallbacks: `rg` no estaba instalado; se usó búsqueda PowerShell. Web dinámica de release notes no expuso contenido, por lo que se contrastaron tags, submódulos y binarios.
