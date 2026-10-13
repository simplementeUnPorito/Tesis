# FTM_SYNC: LED/GPIO sincronizados con temporizador disciplinado por FTM (5 × ESP32-S3)

Experimento para ver en el osciloscopio cinco placas ESP32-S3 (1 referencia + 4 seguidores) generando el mismo pulso al mismo tiempo, usando la biblioteca existente **FTS / Fine Time Sync** (<https://github.com/abbbe/fts>, GPL-3.0). No se inventó ninguna correspondencia reloj-MAC → `esp_timer`: todo el sincronismo lo hace el código de upstream.

> **Estado de verificación (2026-10-05):** configuración, scripts y lógica verificados de forma **estática** (`scripts\Test-FtmSyncConfig.ps1`, todo en verde). **No se compiló** (en esta PC no hay ESP-IDF instalado: no existe `idf.py` ni `IDF_PATH`; no se instaló nada) y **no se midió nada en hardware**. No se promete ningún valor de nanosegundos.

## 1. Arduino IDE vs ESP-IDF (importante)

| | Qué es | Arduino IDE |
|---|---|---|
| `..\FTM\` (ejemplos oficiales FTM_Initiator / FTM_Responder) | Medición de **distancia** por RTT | **Sí funcionan con Arduino IDE.** Siguen intactos y separados. |
| `FTM_SYNC\` (este experimento) | **Temporizador disciplinado** (FTS) | **No es compatible con Arduino. Requiere ESP-IDF nativo.** |

Por qué: upstream usa `esp_wifi_internal_get_mac_clock_time()` (API privada de ESP-IDF, `esp_private/wifi.h`), el periférico MCPWM por registros HAL (`mcpwm_ll_*`), ISR en IRAM y componentes ESP-IDF propios (`dtr`, `crm`, `dtc`, `ftm`). El propio autor escribe «The code uses native ESP-IDF» y deja el port a Arduino como asunto abierto (issue #2 de su repositorio). Por eso aquí **no hay port a Arduino**: tener Arduino IDE instalado no sirve para este experimento. Los sketches de distancia no sincronizan relojes (miden RTT) y por eso no sirven para esto.

## 2. Qué hay en esta carpeta

```
FTM_SYNC/
  LEEME.md                    <- esta guía
  UPSTREAM_MANIFEST.json      <- procedencia: repo, commit, SHA-256 de cada archivo, exclusiones
  upstream/                   <- snapshot PRISTINO de abbbe/fts (80 archivos, sin .git, LICENSE intacta)
  profiles/                   <- perfiles locales (sdkconfig.defaults propios) y mapa de nodos
  config/experiment.example.psd1   <- copiar a experiment.local.psd1 y editar
  scripts/                    <- Build-Firmware, Flash-Node, Monitor-Node, Test-FtmSyncConfig
  PLACA_YD_ESP32S3.md, platformio/   <- NO son de este trabajo (ver nota abajo)
```

> **Aviso:** `PLACA_YD_ESP32S3.md` y la carpeta `platformio/` (variante PlatformIO + ESP-IDF con envs master/slave1-4) aparecieron en esta carpeta mientras se preparaba este paquete, creados por otro flujo de trabajo. **Este paquete no los revisó, no los usa y no los modificó**; las instrucciones de este LEEME y de `scripts/` corresponden únicamente a ESP-IDF nativo con `idf.py`. Conviene decidir cuál de las dos rutas se mantiene para no mezclar configuraciones.

* **Procedencia:** `https://github.com/abbbe/fts`, rama `main`, commit fijado `5d6ea2bfcd516473a98f8aebe7daf690eec21b31` (2026-01-04), bajado el 2026-10-05. Archivos de `upstream/` verificados byte a byte contra los blobs git de ese commit; SHA-256 en `UPSTREAM_MANIFEST.json`.
* **Archivos de upstream modificados: ninguno** (`modifiedUpstreamFiles: []`). El build copia `upstream/` a una carpeta de trabajo (`work\fts`, ignorada por git) para que `managed_components/` y `dependencies.lock` no lo ensucien. `.gitattributes` marca `upstream/**` como `-text` para que git en Windows no convierta saltos de línea.
* **Excluido del snapshot** (290 MB, 130 archivos; detalle en el manifiesto): `fts-platform/` (plataforma Docker/Grafana/MQTT, 9 MB), `docs/**/*.png|odp|pdf|pptx` (presentaciones e imágenes), `docs/misc/mac_timer_align_analysis/` (logs y notebook, 21 MB), `Untitled*.ipynb`, y `CLAUDE.md` (instrucciones dirigidas a un modelo; excluido a propósito). Se conservaron el código, los Kconfig, los `sdkconfig.defaults*`, `bin/`, `jtag/` y los textos en `docs/**/*.md`.
* **Licencia:** GPL-3.0. Si se redistribuye este paquete, mantener `upstream/LICENSE`.

## 3. Versión de ESP-IDF: v5.5.1

Fijada a **ESP-IDF v5.5.1**, con este fundamento (revisado en upstream y en las fuentes de ESP-IDF):

* `components/clock/clock.c` y `ftm.c` llaman a `esp_wifi_internal_get_mac_clock_time()`. Esa función **no existe en ESP-IDF v5.4.2** y **sí existe en v5.5, v5.5.1 y v5.5.2** (verificado en `esp_private/wifi.h` de cada tag).
* El único ESP-IDF que el autor nombra es «v5.5.1» (`docs/posts/20251222-performance-stress-testing.md`: «Recent ESP IDF v5.5.1 give access to local MAC clock»).
* El único requisito explícito de versión en el repo es `idf: ">=5.0"` en `components/usb_uplink/idf_component.yml`, que no es el límite real.

Otras 5.5.x (5.5.2 en adelante) tienen la API pero no fueron probadas aquí; los scripts avisan si detectan una distinta de 5.5.1 y se niegan con versiones que no sean 5.5.x. Upstream no declara una versión de IDF probada en su README: v5.5.1 es **la mejor evidencia disponible, no una garantía**.

**Instalación (la hace usted; este paquete no instala nada):** instalador de ESP-IDF para Windows de Espressif, eligiendo la versión v5.5.1 y el chip ESP32-S3 (guía oficial: *ESP-IDF Get Started → Windows Installer*). Luego usar el acceso directo «ESP-IDF 5.5 PowerShell», o poner en `IdfPath` de la config la carpeta que contiene `export.ps1`.

Requisitos extra del build (todos de upstream, sin tocar):
* **Red al compilar la primera vez:** `components/usb_uplink` declara la dependencia `espressif/esp_tinyusb ^1.0.0` y `main/idf_component.yml` toma `cmd_system`, `cmd_nvs`, `cmd_wifi` de `$IDF_PATH/examples/system/console/advanced/components` (vienen con una instalación normal de ESP-IDF). `usb_uplink` se compila siempre, aunque en este montaje no se use USB.
* Rutas largas de Windows: si el build falla por longitud de ruta, poner `WorkRoot` en una carpeta corta (p. ej. `C:\fw`).

## 4. Mapa de perfiles de firmware y nodos

5 placas, **2 imágenes distintas**. Con MQTT apagado, lo único que upstream diferencia por nodo (`CONFIG_FTS_MQTT_DEVICE_ID`) no se usa, así que F1..F4 llevan **el mismo binario**; la identidad F1..F4 es una etiqueta física (cinta en la placa y en la sonda) más su puerto COM.

| Nodo | Perfil | Rol upstream | Defaults (en orden) | Quién es |
|---|---|---|---|---|
| REF | `ref` | `FTS_ROLE_MASTER` | `fts_common` + `fts_ref` + consola + generado | Crea el AP `FTM_SYNC_TESIS`, FTM responder, emite sync UDP cada 500 ms, pulso de referencia |
| F1 | `follower` | `FTS_ROLE_SLAVE` | `fts_common` + `fts_follower` + consola + generado | Seguidor |
| F2 | `follower` | idem | idem | Seguidor |
| F3 | `follower` | idem | idem | Seguidor |
| F4 | `follower` | idem | idem | Seguidor |

* **Modo de red:** `FTS_MODE_INTERNAL_AP` (FTM por Wi-Fi hacia el AP del maestro; canal 1 por defecto). Se descartó el modo por defecto de upstream (`sdkconfig.defaults`: USB-NCM + MQTT contra `192.168.129.206`) porque exige un host Linux y un broker.
* **Máximo de seguidores en el AP:** confirmado en `components/ftm/ftm.c`, `ftm_master_ap_init()`: `.max_connection = 4` y `.ftm_responder = true`. Cuatro seguidores es **exactamente** el máximo: no queda margen, un quinto seguidor no podría asociarse. **No hizo falta modificar upstream.** (Que 4 iniciadores FTM simultáneos funcionen bien contra un solo respondedor **no está verificado aquí**; el README de upstream muestra maestro + 2 esclavos.)
* Los archivos `sdkconfig.defaults.fts_*` de upstream (master, master2/3, slave1-6) llevan pines de LED de **sus** placas (XIAO GPIO21, Waveshare GPIO41, WS2812 en GPIO48) y MQTT; **no se usan**.

## 5. Qué sale por cada pin (leído del código)

| Salida | Pin (config) | Cómo se genera | Para qué sirve |
|---|---|---|---|
| **Pulso de referencia** | `PulseGpio`, provisional **GPIO7** | **Hardware MCPWM** (`dtr_mcpwm.c`): sube en el evento TEZ del temporizador y baja en la comparación. **2 kHz** (periodo 500 µs), **5 %** (≈25 µs en alto) según `dtr.h` | **Osciloscopio.** Mismo pin en las 5 placas |
| **LED visible** | `LedGpio` (sin valor por defecto; desactivado) | `gpio_set_level()` **por software** desde la ISR del temporizador (`fts_callback`), sólo al cambiar de estado. **Activo en bajo**; encendido el primer 20 % de un ciclo de **1,25 s** (2500 periodos × 500 µs) | Parpadeo **visual**. No usar para medir ns |

* **GPIO7** es el pin por defecto de upstream (`Kconfig.projbuild`: `default 7`; `fts_main.c`: `GPIO_NUM_7`; README: «solder pin headers … GND and GPIO7»). Aquí es **provisional**: hay que **confirmar el pinout de la placa antes de conectar nada** (§6).
* Nota de documentación de upstream: el texto de ayuda del Kconfig dice «2.5kHz 20% duty» y el comentario de `fts_main.c` dice «2.5kHz»/«1Hz»; los valores reales están en `dtr.h` (2 kHz, 5 %) y en el cálculo de `fts_callback` (1,25 s). Prevalece el código.
* **Un LED en el pin del pulso casi no parpadea:** a 2 kHz con 5 % se ve como un brillo tenue constante. El parpadeo visible es el del LED aparte (`LedGpio`, distinto de `PulseGpio`; los scripts lo rechazan si coinciden).
* **LED RGB integrado: no se asume que sea un LED simple.** Un WS2812 necesita su propio protocolo; upstream lo soporta con la opción `FTS_LED_WS2812` (`components/ws2812`, codificador RMT) y lo actualiza desde una **tarea** avisada por la ISR, no con un `gpio_set_level()` directo. En la config: `LedType = 'ws2812'` (por defecto `'gpio'` = LED simple activo en bajo) y `LedGpio` con el pin del RGB. Con ese tipo el parpadeo es sólo visual y **no sirve para medir nanosegundos**. El LED queda **desactivado** por defecto, y un seguidor sin LED igualmente emite el pulso.
* Los pulsos de un seguidor permanecen **forzados a nivel bajo hasta la primera alineación** (`mcpwm_generator_set_force_level` en `dtr_mcpwm.c`, liberado en `dtr.c` en el primer periodo alineado). La opción de upstream `FTS_PULSE_BEFORE_ALIGN` figura en el Kconfig pero **ninguna parte del código la usa** (revisado con `grep`), así que no cambia nada.

## 6. Hardware: confirmar antes de conectar

Aún no está confirmado el modelo de placa ni el pin del LED. Hay una nota previa en `PLACA_YD_ESP32S3.md` (escrita por otro flujo de trabajo, no por este): las placas serían EGBO ESP32-S3 **N16R8** con inscripción leída «V1120 YO-ESP32-S3 2022-V1.3», probablemente **YD-ESP32-S3**, cuyo README del fabricante (<https://github.com/vcc-gnd/YD-ESP32-S3>) documenta WS2812 en GPIO48, GPIO7 disponible, USB nativo en GPIO19/20 y un segundo puerto con CH343P. **Es una identificación provisional; no se verificó contra la placa física.** Con 8 MB de PSRAM octal, los GPIO33-37 quedan ocupados (GPIO7 y GPIO48 no figuran entre ellos). Antes de soldar o conectar:

1. Anotar el modelo exacto de las 5 placas en `BoardModel` y abrir **su hoja de pines**.
2. Verificar que `PulseGpio` (7) está accesible en el header y **no** es: strapping (0, 3, 45, 46), USB nativo (19, 20), SPI flash/PSRAM (26-32; 33-37 con PSRAM octal), UART0 (43, 44) si la consola es `uart0`. `Test-FtmSyncConfig.ps1` avisa de estos casos, pero **no sabe qué placa tiene**; la verificación es suya.
3. Elegir un pin libre y accesible para el LED externo (si se usa) y ponerlo en `LedGpio` con `LedEnabled = $true`.
4. Sólo entonces poner `BoardPinoutConfirmed = $true`. Hasta ese momento `Flash-Node.ps1` se niega a flashear (la compilación sí se permite).

Conexiones (lógica de 3,3 V, las cinco con el mismo esquema):

* **GND común** entre las cinco placas y la masa de las sondas. Un solo cable de GND por placa hacia un bus común, sondas con su pinza a ese bus.
* **Sonda de osciloscopio:** punta en `PulseGpio`, pinza en GND. **No** conectar a 5 V ni a 3V3 por error: el pin es una salida de 3,3 V. Compensar la sonda en ×10.
* **LED opcional (activo en bajo):** 3V3 → resistencia (330 Ω–1 kΩ) → ánodo del LED; cátodo → `LedGpio`. El pin **hunde** la corriente cuando el LED debe encender. Una resistencia por LED.
* **Bucles de masa:** upstream advierte que es fácil crear uno al usar osciloscopio o analizador USB baratos junto con las placas y que puede degradar FTM; probar con baterías o portátiles a batería si aparece ruido.
* Cada placa se alimenta por USB (también sirve para flashear y monitorear).

## 7. Preparación y flasheo

En PowerShell, dentro de `FTM_SYNC\scripts` (con ESP-IDF v5.5.1 ya instalado y activo):

```powershell
Copy-Item ..\config\experiment.example.psd1 ..\config\experiment.local.psd1
# editar experiment.local.psd1: modelo de placa, PulseGpio, LED, consola, puertos COM, IdfPath
.\Test-FtmSyncConfig.ps1                 # verificación estática; debe terminar en verde
.\Build-Firmware.ps1 -Profile all        # compila ref y follower (primera vez: baja componentes)
# Con BoardPinoutConfirmed = $true:
.\Flash-Node.ps1 -Node REF               # una placa a la vez: conectar sólo esa por USB
.\Flash-Node.ps1 -Node F1                # ... F2, F3, F4 con la imagen follower
.\Monitor-Node.ps1 -Node REF             # un monitor por terminal; Ctrl+] sale
```

* `Build-Firmware.ps1 -DryRun` / `Flash-Node.ps1 -DryRun` sólo imprimen las órdenes `idf.py`.
* Orden de defaults pasado a `SDKCONFIG_DEFAULTS`: común, rol, consola, generado (pines, LED, Wi-Fi). El `sdkconfig` del build se regenera en cada compilación para que los cambios de config apliquen.
* Consola: por defecto `usb-serial-jtag` (puerto USB nativo). Si su placa expone el puerto «UART» (CP210x/CH340) y es el que usa, cambiar a `uart0`. Si el monitor queda mudo, probar el otro modo o el otro conector USB.
* Cada placa debe identificarse con su COM: al conectar una por vez, anotar qué puerto aparece en el Administrador de dispositivos. Los COM pueden reasignarse al reconectar.

## 8. Orden de arranque y comportamiento de enganche (según el código fuente)

**Orden:** 1) arrancar **REF primero**; en su consola esperar `Master AP: SSID='FTM_SYNC_TESIS', Channel=1`. 2) Arrancar F1..F4 **como máximo ~2 minutos después** de REF (README de upstream, issue #1: si el seguidor arranca más tarde aparece un error de fase fijo de cientos de µs). 3) Verlos enganchar (no hay una sola señal de «lock»; ver abajo).

**Señales en el log de cada seguidor**, en este orden: `FIRST SYNC: MAC=… channel=… run_id=…` (recibió el sync UDP del maestro) → `FTM #n: 64/64 entries …` (sesión FTM; una por segundo, `FTM_PERIOD_MS`) → `Regression: samples=…, R²=…, std=… ns` → `Alignment request …` / `Alignment feedback: period_ticks=… cycle=…`. Upstream recomienda mirar que cada sesión aporte casi todas las muestras (`+63` de 64); con pocas, «su resultado variará».

**Qué significa «enganchado» en el código (inferido de la lectura, no medido):**
* El modelo del reloj se considera válido cuando la regresión da R² > 0,999 con al menos 32 muestras (`crm.c`: `CRM_R_SQUARED_THRESHOLD`, `MIN_REGRESSION_SAMPLES = 64/2`). Con eso el seguidor pide su primera alineación y recién entonces su pulso deja de estar forzado a bajo.
* **Cada** sesión FTM posterior vuelve a alinear (a menos que se active `FTS_TEST_ALIGN_ONCE`, desactivado aquí): es disciplina continua, con corrección de periodo en pasos de 1/65536 de tick de 25 ns.
* **No hay indicador de «lock perdido»**: no existe un estado ni salida que lo señale al exterior.

**Limitaciones de reenganche (del código):**
* **Si el maestro se reinicia**, cada seguidor detecta otro `run_id` y llama `abort()` (reinicia). Tras reiniciar REF hay que esperar a que los seguidores se reinicien y reenganchen; la regla de los 2 minutos vuelve a aplicar. Es el diseño actual (la ruta de resincronización suave está comentada en `ftm.c`).
* **Si un seguidor pierde el Wi-Fi**, pausa las sesiones FTM y reintenta `esp_wifi_connect()`; **no hay modelo de espera (holdover)**: su temporizador sigue libre con el último periodo corregido, así que deriva a la tasa ppm del cristal, y al volver el enlace se realinea con la siguiente regresión. Que ese retorno funcione bien en la práctica **no se verificó**.
* **Cambios de canal del AP:** el seguidor se reconecta al canal anunciado; el canal fijo (1) evita el caso.
* **Reinicio de un seguidor:** pierde todo el estado (en RAM) y empieza de nuevo; su pulso queda forzado a bajo hasta realinear.
* **Reinicios por `abort()`** en el código ante condiciones anómalas: periodo calculado fuera de [1, 65535] ticks, timeout de 1 s esperando el evento TEZ, reporte FTM con más entradas de las previstas. En el monitor, un reinicio inesperado de un seguidor casi seguro es uno de estos o el reinicio del maestro.
* **Rollover del reloj MAC (cada ≈71,6 min):** el código lo desenrolla (`clock.c`, vigilante horario), pero una medición que cruce ese punto no fue probada aquí. Si la sesión de medición supera ~72 min, anotar qué ocurre al cruzarlo.
* **Error de fase fijo por placa:** upstream documenta unos pocos µs entre maestro y esclavo (el maestro inicializa Wi-Fi distinto) y entre esclavos no debería haber una diferencia significativa; se corrige a mano con `DTR_COMPENSATION_NS` (en `upstream/components/dtr/include/dtr.h`, valor actual −200). **No se modificó.** Si se decide ajustarlo, hacerlo como parche **documentado y separado**, nunca editando silenciosamente `upstream/` (registrar en `modifiedUpstreamFiles` del manifiesto).

## 9. Pruebas con osciloscopio

Canales: CH1 = **referencia de comparación**, CH2 = **la placa bajo prueba**. Ambas puntas ×10, **mismo GND**. Disparo en **flanco de subida de CH1**, nivel ≈ 1,5 V, acoplamiento DC. Escala sugerida inicial: 50 µs/div y subir el detalle (≤1 µs/div, o menos) alrededor del flanco; persistencia o 100+ adquisiciones para ver la dispersión.

**Prueba A: referencia contra cada seguidor (4 mediciones):** CH1 = REF, CH2 = F1; luego F2, F3, F4.
**Prueba B: seguidor contra seguidor:** CH1 = F1 y CH2 = F2; F1–F3; F1–F4; F2–F3; F2–F4; F3–F4 (6 pares). Upstream sostiene que entre esclavos no debe quedar un desfase fijo significativo; es una hipótesis a comprobar, no un resultado.

Para cada par registrar, con el mismo disparo y tras permitir que los seguidores lleven un tiempo enganchados (anotar cuánto):

* **Offset (delta de flanco de subida):** diferencia media entre los flancos de subida de CH1 y CH2 (cursores o medida «Delay» de flanco a flanco, subida→subida, al 50 % del nivel). Con signo; es el **error de fase fijo**.
* **Jitter:** dispersión (desviación estándar y pico a pico) de ese delta en N ≥ 100 capturas, **separada del offset**. Si el osciloscopio lo permite, histograma de la medida de delay con estadísticas.
* **Controles:** (1) pares REF–REF con la misma señal a CH1 y CH2 por dos sondas para conocer el piso del instrumento (cable/sondas); (2) intercambiar las sondas entre CH1 y CH2 para separar el sesgo de canal del desfase real; (3) mismas longitudes de cable y mismo tipo de sonda.
* Anotar: fecha, modelo de placa, versión de ESP-IDF, commit de upstream (en `UPSTREAM_MANIFEST.json`), tiempo desde el arranque, valor de `Regression: … std=…` y RSSI del seguidor al momento de cada medida, y distancia entre placas.
* No esperar ni afirmar un valor de nanosegundos antes de medirlo. El autor de upstream declara una dispersión menor a 100 ns en su montaje; **aquí no está verificado**. Un osciloscopio con la base de tiempo gruesa no resolverá algo tan fino: usar la escala de tiempo mínima que permita ver un flanco de 25 µs de ancho con claridad.
* La ISR del LED y el flanco MCPWM no son la misma cosa: **medir sólo el pulso del pin `PulseGpio`.**

## 10. Qué queda sin verificar

* Compilación (no hay ESP-IDF en esta PC); en especial la combinación de `sdkconfig` local (modo AP, TinyUSB NCM sin inicializar, consola USB-Serial/JTAG) frente a la de upstream, y la descarga de `esp_tinyusb`.
* Que cuatro seguidores a la vez sostengan FTM contra un solo AP.
* Cualquier medición en hardware, y cualquier cifra de offset o jitter.
* Pines utilizables de la placa real (modelo sin confirmar) y el comportamiento de GPIO7 en ella.
* Comportamiento tras pérdida y recuperación del enlace, y el cruce de ≈71,6 min.
