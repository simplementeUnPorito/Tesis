# Investigación: responder FTM que deja de contestar

Fecha: 2026-10-25. No se modificó el firmware, no se grabaron placas y no se accedió a COM14.

## Conclusión ejecutiva

**VERIFICADO:** el responder FTM de este `libnet80211.a` dispone de **tres sesiones simultáneas**. Cada sesión queda asociada a una MAC iniciadora. Una nueva request inicial de una MAC que ya tiene sesión se descarta **sin respuesta**. La liberación normal depende principalmente de un timer de sesión: su callback no libera directamente, sino que reserva/postea un evento a la tarea Wi-Fi; si la reserva o `pp_post()` falla, retorna sin reintentar y el slot sigue ocupado. Una request explícita de terminación o `wifi_softap_stop()` también lo libera.

**SUPUESTO con evidencia fuerte:** durante la carga real se perdió una limpieza por cada iniciador. Quedaron tres slots huérfanos, uno para S3, S2 y S4. Desde ese momento, cada request inicial de esas mismas MAC fue ignorada y los iniciadores reportaron `FTM_STATUS_NO_RESPONSE` (3). Esto explica mejor el patrón que un `busy` global: S3 murió primero y S2/S4 siguieron funcionando hasta perder sus propios slots.

No hay API pública para vaciar las sesiones FTM del responder sin bajar el SoftAP. Cambiar `ftm_responder` con `esp_wifi_set_config(WIFI_IF_AP, ...)` **no limpia los slots**. `esp_wifi_ftm_resp_set_offset()` tampoco. La recuperación pública confiable sigue siendo parar/iniciar Wi-Fi —o quitar/reponer AP— con la consecuente desconexión del teléfono.

## Alcance y evidencia

Binario principal: `libnet80211.a`, SHA-256 `ACF1AF8D20976E3C4792094B7EB67C5CE1DC47EA92124E572B8603EC08DB23E3`, Arduino-ESP32 3.3.12 / IDF 5.5.5. Herramienta: GNU `xtensa-esp-elf-objdump` 2.43.1. Los offsets mencionados son internos a objetos relocatables.

También se contrastaron los objetos FTM de IDF 5.5.6 y `esp32-wifi-lib` master (`ec08f0c`, 2026-10-22): mantienen `ftm_resp_ctx` de 12 bytes y las rutinas de lookup/add de tres entradas. Los objetos no son idénticos; esta comparación no demuestra que todos los detalles internos sean iguales.

En `maestro.log`:

- S3 tuvo éxito a las 10:50:36 con `ses=918` y pasó a `ev=3` a las 10:50:38; el contador no volvió a avanzar.
- S2 tuvo éxito a las 10:52:46 con `ses=1073` y pasó a `ev=3` a las 10:52:48.
- S4 tuvo éxito a las 10:52:47 con `ses=1011` y pasó a `ev=3` a las 10:52:49.
- A las 11:10 los tres seguían en `ev=3` con los mismos contadores.
- Antes del colapso, S2 tuvo `NO_VALID_MSMT` (5) a las 10:49:46, 10:50:00 y 10:50:36, pero se recuperó de cada uno.

El dato corrige una imprecisión del resumen inicial: S2 y S4 no fallaron con dos minutos de diferencia entre sí, sino con un segundo de diferencia; S3 sí antecedió a ambos por unos 130 segundos.

## 1. Internos del responder

### VERIFICADO

**Capacidad:** `ftm_resp_ctx` ocupa `0x0c` bytes: tres punteros de 32 bits. `ftm_get_resp_session_for_peer`, `ftm_get_resp_session_by_cookie` y `ftm_add_resp_session` recorren exactamente tres posiciones. `ftm_resp_get_burst_slot` compone una máscara con el byte de estado de esas tres sesiones y elige uno de tres bits. Por lo tanto, hay **tres slots de responder**.

**Alta:** `ftm_create_responder_session` reserva 120 bytes, asigna parámetros, intenta insertar en esos tres slots y genera un cookie aleatorio. Si no hay lugar, la initial response sale con rechazo; no se crea una cuarta sesión.

**Liberación:** `ftm_free_resp_session`:

1. desarma y destruye dos timers de la sesión;
2. invalida el cookie;
3. pone en `NULL` su entrada dentro de `ftm_resp_ctx`;
4. libera los 120 bytes.

Se llega a esa función por estas rutas:

- `ieee80211_ftm_sess_timeout_process(cookie)`, luego del timer de sesión;
- una action FTM sin FTM Parameters cuyo campo de continuación/terminación vale cero;
- `ftm_responder_cleanup()`, que recorre los tres slots. En el binario inspeccionado, su único caller externo es `wifi_softap_stop()`.

El último measurement TX no libera directamente la sesión. `public_send_action_ftm_resp` rearma el timer de sesión con el tiempo programado más un margen de 500 ms. Por lo tanto, incluso una sesión exitosa termina dependiendo de que se procese ese timeout o llegue una terminación del peer.

**Falla persistente posible:** `ftm_session_timeout` solamente llama `ieee80211_timer_process(7, 22, cookie)`. Esta última función toma el lock Wi-Fi, intenta reservar un objeto de evento de 8 bytes y llama `pp_post()`. Si falla la reserva o el post, libera lo que corresponda, registra error y retorna; no hay retry ni barrido por antigüedad al recibir requests nuevas. Consumido el timer one-shot, el slot puede quedar ocupado indefinidamente, hasta una terminación válida o un `wifi_softap_stop()`.

**Request repetida:** `public_recv_action_ftm_req` busca primero una sesión por MAC. Si la trama es una request inicial —contiene FTM Parameters— y ya existe una sesión para esa MAC, sale sin enviar respuesta. Esto se ve en el iniciador exactamente como `NO_RESPONSE`, no como `CONF_REJECTED`.

No encontré otro latch global de “responder busy”. El estado global relevante es la tabla de tres punteros, más parámetros globales como el offset FTM. Existe además una regla especial de admisión para ASAP, pero no explica el caso actual configurado con `burst_period=2`.

### SUPUESTO

La carga combinada —aproximadamente 290 tramas ESP-NOW/s, WebSocket y FTM de tres nodos— pudo agotar temporalmente el pool/event queue usado por `ieee80211_timer_process`. Perder un único post de limpieza por peer basta para reproducir la progresión observada. El desensamblado demuestra que la ventana existe; el log actual no demuestra que `pp_post()` haya fallado porque no contiene el log interno de Wi-Fi ni una captura de `ftm_resp_ctx`.

Con tres slots huérfanos, una cuarta MAC nueva debería recibir rechazo de configuración/capacidad, mientras las tres MAC ya registradas seguirían siendo ignoradas. Esa es una prueba discriminante útil para la próxima reproducción.

## 2. Lado esclavo

### VERIFICADO

`ftm_slave.cpp` usa inicialmente 16 frames y `burst_period=2` (200 ms). `s_periodMs` vale 1000 ms por defecto, aunque el log operativo muestra reportes aproximadamente cada 2 s. Las alternativas `{32, 0, 64, 24}` sólo se prueban ante `CONF_REJECTED`; después del primer éxito la configuración queda bloqueada.

El flujo es:

- procesa primero cualquier evento FTM pendiente y pone `s_busy=false`;
- si continúa busy por más de 4000 ms, llama `esp_wifi_ftm_end_session()`, restaura promiscuo y publica un timeout local;
- si está permitido y venció el período, deshabilita promiscuo, inicia FTM y marca busy sólo si la API devolvió `ESP_OK`.

La condición de pausa durante captura es correcta: sólo permite FTM en `SYNCMODE_FTM_ACTIVE`. Además, si `allowed` cambia a falso con una sesión en curso, la rama busy sigue corriendo y eventualmente ejecuta el watchdog; no abandona silenciosamente la sesión.

En el blob iniciador:

- `ftm_initiator_session_end()` y `ftm_initiator_session_abort()` limpian el contexto local y publican el reporte; **no envían terminación al responder**.
- `esp_wifi_ftm_end_session()` llega a `ftm_initiator_end_session_local()`. Sólo en un estado activo concreto arma una request FTM de terminación; en otros estados aborta localmente.
- Si esa trama de terminación se pierde, el responder debe recuperarse por su timer.
- Una vez que el SDK ya publicó `NO_RESPONSE` y destruyó el contexto local, llamar después a `esp_wifi_ftm_end_session()` no tiene una sesión activa desde la cual mandar terminación.

Por eso el watchdog de 4 s no parece causar este incidente: el timeout interno que produce `ev=3` ocurre antes y deja `s_busy=false`. Tampoco puede reparar el slot remoto después del evento.

### SUPUESTO / mejora posible

Un reset, pérdida de radio o aborto del esclavo durante una sesión aumenta la dependencia del timeout remoto, pero no debería colgar al responder si ese timer se procesa. El problema no es que el esclavo omita una llamada obligatoria después de cada éxito: la API pública ya destruyó el contexto cuando entrega el evento exitoso y no ofrece una terminación tardía confiable.

No existe un parámetro `min_delta` en este código. Si se refiere al filtro/modelo de sincronización, ajustarlo no cambia la vida de los slots FTM. Los controles relevantes acá son `s_periodMs`, coordinación entre nodos, `frm_count`, `burst_period` y la pausa durante captura.

## 3. Reset sin cortar el SoftAP

### VERIFICADO

`esp_wifi_set_config(WIFI_IF_AP, ...)` despacha a `wifi_softap_set_config`. En esta versión, el byte `wifi_ap_config_t::ftm_responder` está en offset 116; la rutina lo copia/persiste, pero no referencia `ftm_responder_cleanup`, `ieee80211_ftm_attach/detach`, `wifi_softap_stop` ni `wifi_softap_start`. Apagar y prender el flag en caliente puede cambiar la admisión/capability futura, pero **no vacía `ftm_resp_ctx`**. Coincide con la observación ya documentada en `apEnableFtmResponder()`: el flag quedaba guardado, pero sin restart no activaba correctamente el responder en ese arranque.

`esp_wifi_ftm_resp_set_offset()` sólo convierte/guarda el offset de timestamps (`g_t1_offset_psec`); no toca sesiones.

`ftm_responder_cleanup()` existe como símbolo privado y limpia los tres slots, pero está pensado para ejecutarse dentro del teardown del SoftAP. No toma por sí mismo una exclusión que vuelva segura una llamada arbitraria desde la aplicación. Invocarlo mientras timers/callbacks Wi-Fi conservan punteros puede causar use-after-free o doble free.

No encontré una API pública ni un evento privado estable que programe “reset FTM responder” dentro de la tarea Wi-Fi. Cambiar temporalmente el modo a STA también termina bajando el AP y desconecta al teléfono.

### SUPUESTO / opción experimental

Una action FTM de terminación correctamente formada, enviada desde cada MAC esclava, debería entrar por la ruta verificada que libera su slot sin bajar el AP. La API pública no permite hacerlo una vez finalizado el contexto local; requeriría construir/injectar management frames o enganchar un estado interno. Puede servir como experimento diagnóstico, pero es frágil frente al ABI/protocolo y no lo recomiendo como recuperación de producción sin sniffer y pruebas de estrés.

## 4. Antecedentes de Espressif

### VERIFICADO

- [ESP-IDF #7702](https://github.com/espressif/esp-idf/issues/7702) reprodujo en ESP32-S2/IDF 4.3.1 sesiones repetidas que terminaban permanentemente en `CONF_REJECTED`, incluso a una cada 5 s; sólo resetear el AP recuperaba. Hubo reportes equivalentes en C3.
- [esp32-wifi-lib #26](https://github.com/espressif/esp32-wifi-lib/issues/26) registra el mismo defecto.
- Espressif lo corrigió con [commit `c3d971c52e34`](https://github.com/espressif/esp-idf/commit/c3d971c52e34ff7d6954a83e72155eabdc7e84cd): el mensaje oficial dice que agrega un session timer de limpieza al responder, aumenta el timeout del iniciador y corrige ASAP/start delta. Espressif indicó que quedaría disponible en IDF 4.3.2; el reportante confirmó la resolución.
- [ESP-IDF #7753](https://github.com/espressif/esp-idf/issues/7753) era otro wedge de 4.3.1 por cálculo de start time; el mismo commit cambió el cuelgue por un aborto recuperable. Un comentario post-fix todavía observó el delta absurdo, pero la siguiente sesión volvió a funcionar.

El binario 5.5.5 actual **ya contiene** el timer agregado por aquel arreglo. Por eso el incidente presente no es simplemente “falta el fix de 2021”: es compatible con una pérdida del evento que ejecuta ese timer, o con otro defecto de estado. No encontré un issue público de Espressif que reproduzca exactamente ESP32-S3/IDF 5.5.5, tres iniciadores, alta carga y `NO_RESPONSE` permanente.

### SUPUESTO

El antecedente refuerza que las sesiones huérfanas han sido una clase real de bug del blob, pero no prueba que el defecto de 2021 haya regresado. Tampoco hay evidencia pública de que actualizar de 5.5.5 a 5.5.6 o a master corrija este caso; la estructura crítica de tres slots sigue presente.

## 5. Recomendación ordenada

1. **Serializar y escalonar FTM entre esclavos.** Dar ventanas exclusivas por nodo y evitar que tres sesiones de 200 ms se solapen. Empezaría con una sesión global cada 2 s, rotando S2/S3/S4 —cada nodo mediría cada 6 s— y luego bajaría el intervalo sólo si un soak largo sigue limpio. Riesgo: menor tasa de actualización del modelo; beneficio: reduce sesiones concurrentes y presión sobre eventos.

2. **Mantener 16 frames; no probar 32/64 bajo carga.** Es el mínimo explícitamente usado/aceptado por este firmware. `burst_period=0` (ASAP) acorta ocupación, pero el blob tiene arbitraje especial para ASAP y puede aumentar `CONF_REJECTED` si hay concurrencia. Probarlo únicamente después de serializar, A/B contra período 2. Riesgo: cambio de timing y calidad de medición.

3. **Aplicar backoff/circuit breaker por peer.** Tras 2–3 `NO_RESPONSE` consecutivos, dejar de reintentar ese esclavo durante 30–60 s y reportar el estado al maestro. No libera un slot ya huérfano, pero evita tráfico inútil y mayor presión. Los `NO_VALID_MSMT` aislados deben contarse aparte: el log muestra que eran recuperables.

4. **Crear ventanas de baja carga para FTM.** Si la sincronización lo tolera, medir antes de capturar o intercalar ventanas breves sin ráfagas ESP-NOW/WebSocket. Pausar FTM durante toda la captura es la prevención más fuerte, pero obliga a revisar la caducidad actual del modelo y sacrifica corrección online.

5. **Agregar un watchdog maestro y recuperación programada.** Detectar contador de sesiones congelado más `NO_RESPONSE` consecutivo de los tres peers. En el siguiente límite seguro de captura, ejecutar `esp_wifi_stop()/start()` y reconstruir ESP-NOW/AP/WebSocket según el flujo ya conocido. Esto sí llama `wifi_softap_stop()` y `ftm_responder_cleanup()`. Riesgo: desconexión/reconexión del teléfono y pérdida transitoria de datos; no hace falta un deinit completo sólo para limpiar FTM.

6. **Ensayo diagnóstico en la próxima reproducción:** antes del restart, intentar FTM desde una cuarta MAC. Rechazo inmediato a la cuarta más silencio para las tres originales apoyaría “tres slots huérfanos”. Activar logs Wi-Fi suficientes para buscar fallo de alloc/`pp_post`, y registrar heap/pools en el instante de cada muerte.

7. **No usar como recovery de producción** el toggle `ftm_responder`, `esp_wifi_ftm_resp_set_offset()` ni una llamada directa a `ftm_responder_cleanup()`: los dos primeros no limpian y la tercera viola ABI/concurrencia. Una terminación FTM raw por peer merece un prototipo separado sólo si evitar toda desconexión del teléfono justifica ese riesgo.

8. **No asumir que una actualización lo arregla.** Repetir el soak real al cambiar blob. El criterio mínimo es que, bajo saturación, los timers puedan reintentarse o exista un barrido de sesiones vencidas; conservar tres slots no es por sí mismo un defecto.

## Dictamen

La explicación más parsimoniosa es **agotamiento progresivo de los tres slots por pérdida de los eventos de cleanup**, no un único busy global. Está verificada la capacidad de tres, la política de ignorar una request inicial de una MAC ya presente y la ruta sin retry ante fallo de post; queda por verificar en vivo que ese fallo ocurrió. La mitigación de menor riesgo es serializar/ralentizar FTM y reservar el stop/start para un watchdog en un límite seguro. Hoy no hay reset público, barato y confiable que conserve el SoftAP conectado.

---

IA principal: Codex, modelo no reportado  
Delegados: ninguno (`ORCHESTRATOR_DEPTH=1`)  
Fallbacks: `rg` no estaba instalado; se usó PowerShell. La herramienta web no devolvió contenido para estas páginas; se consultó la API pública de GitHub y se contrastó con binarios locales.
