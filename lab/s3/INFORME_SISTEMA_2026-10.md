# Estado integral del sistema de adquisición — 26 de octubre de 2026

## Convenciones y siglas

- **ACK/NACK:** confirmación positiva/negativa.
- **ADC:** convertidor analógico-digital.
- **AP:** punto de acceso Wi-Fi.
- **API:** interfaz de programación de aplicaciones.
- **ARP:** protocolo de resolución de direcciones.
- **CSV:** valores separados por comas.
- **DMA:** acceso directo a memoria.
- **DSI:** interconexión digital del PSoC.
- **EOC:** fin de conversión del ADC.
- **FIR:** filtro de respuesta finita al impulso.
- **FTM:** medición fina de tiempo de Wi-Fi.
- **GPIO:** entrada/salida digital de propósito general.
- **HTTP:** protocolo de transferencia de hipertexto.
- **HT/AMPDU:** alta tasa y unidad de datos MAC agregada, modos de transmisión/agregación 802.11.
- **I2C:** bus serie interintegrado.
- **IDF:** framework de desarrollo IoT de Espressif.
- **IMO:** oscilador principal interno del PSoC.
- **JSON:** notación de objetos de JavaScript.
- **LMK:** clave maestra local de ESP-NOW.
- **LS:** mínimos cuadrados.
- **LVTTL:** lógica transistor-transistor de baja tensión.
- **lwIP:** implementación liviana de los protocolos de internet.
- **MAC:** control de acceso al medio; también identifica la dirección de radio.
- **MASW:** análisis multicanal de ondas superficiales.
- **MCPWM:** modulador de ancho de pulso para control de motores del ESP32.
- **mDNS:** sistema de nombres de dominio multidifusión.
- **OTA:** actualización de firmware por el aire.
- **PC:** computadora personal.
- **PHY:** capa física de radio.
- **PI:** controlador proporcional-integral.
- **PLL:** lazo enganchado en fase.
- **PSRAM:** memoria pseudoestática externa.
- **PSoC:** sistema programable en chip.
- **RAM:** memoria de acceso aleatorio.
- **RTO:** tiempo de espera de retransmisión.
- **SD:** tarjeta Secure Digital.
- **SOC:** inicio de conversión del ADC.
- **SPA:** aplicación web de una sola página.
- **STA:** estación Wi-Fi.
- **TCP/IP:** protocolos de control de transmisión e internet.
- **TX/RX:** transmisión/recepción.
- **UDB:** bloque digital universal del PSoC.
- **UART:** receptor-transmisor asíncrono universal.
- **USB:** bus serie universal.
- **ZIP:** contenedor comprimido de archivos.

Las tasas se expresan en hertz (Hz), los tiempos en segundos (s), milisegundos (ms), microsegundos (us) o nanosegundos (ns), y las derivas en partes por millón (ppm) o partes por mil millones (ppb). En las tablas, B significa bytes.

## 1. Resumen ejecutivo

El sistema completo quedó integrado alrededor de un maestro ESP32-S3 con Arduino 3.3.12 sobre Espressif IoT Development Framework (ESP-IDF) 5.5.5, esclavos ESP32-S3 asociados a un Programmable System-on-Chip (PSoC) 5LP y compatibilidad con esclavos ESP32 clásicos. El maestro mantiene un punto de acceso de software (SoftAP) denominado `GeoNetwork`, publica la aplicación web y el WebSocket, coordina las capturas por ESP-NOW y actúa como responder Fine Timing Measurement (FTM). El canal de radio operativo es el 1.

La configuración de campo elegida conserva FTM en el maestro. El defecto de transmisión de ESP-NOW de ESP-IDF 5.5, documentado como `esp-idf #19269`, se evitó en los envíos del maestro mediante tramas 802.11 raw construidas con el formato de ESP-NOW y transmitidas por `esp_wifi_80211_tx()`. La solución fue verificada en cinco corridas de 14 min con tres nodos, sin bloqueo de transmisión ni muerte del responder FTM. Las sesiones FTM se distribuyen en turnos exclusivos de 1 s dentro de una rueda de 8 s para no superponer iniciadores.

La sincronización del comienzo de captura dispone de tres caminos:

1. START programado con el modelo FTM, preferido cuando todos los nodos armados poseen un modelo vigente.
2. START anclado al instante de recepción de la trama, respaldo disponible en esclavos S3 con ESP-IDF 5.
3. START por ejecución inmediata del callback, camino legado de los esclavos clásicos.

Las dispersiones medidas entre nodos fueron de 152 us de mediana y 374 us de máximo para el broadcast legado, 5 us de mediana y 10 us de máximo para el anclaje a recepción, y entre 1 us y 7 us para START programado por FTM. Estas cifras miden la activación de SYNC en los ESP; todavía falta medir en placa la relación entre SYNC, los pulsos de Start of Conversion (SOC), la conversión del Analog-to-Digital Converter (ADC) y la primera muestra efectiva.

La cadena temporal nueva ya está implementada en firmware y software, pero no fue probada con el PSoC real. Cada esclavo S3 genera por hardware un pulso SOC nominal cada 500 us —2000 Hz— en el GPIO 1 y un reloj de 8 MHz, 50 % de ciclo útil, en el GPIO 2. El tren SOC se disciplina con la deriva estimada por FTM y se alinea al START. También se implementaron marcas periódicas muestra↔reloj del maestro, frecuencia de muestreo informada por nodo y ajuste muestra→tiempo en la aplicación de análisis. Para completar esta cadena, Elias debe modificar el proyecto en PSoC Creator: configurar el ADC Delta-Sigma en Single Sample de 18 bits con SOC por hardware, llevar el reloj externo de 8 MHz a un Phase-Locked Loop (PLL), pasar SOC al ADC solamente cuando SYNC esté alto y recompilar el proyecto con el antialias Q1.23.

La adquisición ofrece tres modos: asincrónico, tiempo real y descarga rápida. El almacenamiento seleccionable es RAM del PSoC, RAM compartida del camino en vivo o RAM más Secure Digital (SD). Los datos viajan en lotes de 30 muestras; se numeran, confirman y retransmiten. En tiempo real, el maestro confirma periódicamente, la web detecta huecos y solicita `FILL`, y el esclavo conserva datos para recuperarlos. El formato GeoZ reduce un lote maestro→web de alrededor de 270 B a unos 63 B sin pérdida.

La web muestra la señal cruda y una vista filtrada. Durante la captura aplica un Finite Impulse Response (FIR) causal y compensa visualmente su retardo de grupo; al cerrar, recalcula la captura con filtrado hacia adelante y hacia atrás (`filtfilt`). El rechazo de red y la limpieza guiada por marcas se aplican al cierre. El archivo ZIP exportado contiene señal cruda, metadatos, firmas de ruido y, con el firmware nuevo, `time_marks.csv` por nodo. El navegador puede subir el ZIP al servidor por Tailscale; el servidor valida, conserva y procesa la captura, y la aplicación Python ajusta una recta muestra→reloj maestro para alinear los canales.

El estado debe leerse en dos niveles claramente separados:

| Nivel | Estado al 26/10/2026 |
|---|---|
| Banco S3 sin PSoC ni SD reales | Probado de punta a punta en modos asincrónico, rápido y tiempo real; OTA, WebSocket, web, ZIP, servidor y aplicación verificados. |
| Radio del maestro ESP-IDF 5.5 | TX raw y FTM por turnos probados en cinco corridas de 14 min con tres nodos. |
| START entre ESP32 | Medido; FTM entre 1 us y 7 us, respaldo anclado 5/10 us de mediana/máximo. |
| SOC disciplinado, reloj de 8 MHz y marcas temporales | Implementados, compilados y probados en host; no probados en placa. |
| ADC Single Sample de 18 bits gobernado por SOC | Configuración pendiente en PSoC Creator; no probado. |
| Antialias Q1.23 de 90 dB nominales | Implementado y verificado contra modelos de host; pendiente de recompilar y medir en PSoC. |
| FIR de adquisición de 200 Hz | Implementado, coeficientes verificados; pendiente de validación física. |
| PSoC y SD reales, esclavos clásicos, más de 5–6 nodos | Pendiente de banco/campo. |

### 1.1. Consolidación de cambios del 23 al 26 de octubre

| Fecha | Cambios incorporados |
|---|---|
| 23/10 | Captura PSoC→ESP en RAM compartida, SD y tiempo real; descarga rápida; web de captura; modos/almacenes/sin límite; marcas de ruido por muestra; limpieza por firmas; motivo de reinicio en HELLO; recuperación del dueño WebSocket y eliminación de bloqueos del tiempo real. |
| 24/10 | Port completo a ESP32-S3; entornos por NODE_ID; OTA por el maestro; exportación de crudo+metadata; antialias Kaiser en PSoC; carga web de 128 taps Q1.23; modos FTM activo/pausado/radio apagada; compresión sin pérdida; simulación de PSoC/SD; registro remoto; exclusión de nodos no listos; reintentos de descarga; duración de 5 min y 14 min; firmas simuladas y prueba desde la web. |
| 25/10 | Migración S3 a ESP-IDF 5.5.5; FTM operativo; START programado; procesamiento fuera de callbacks; STOP unicast; FIR causal en vivo; vista móvil y firmas dentro del ZIP; diagnóstico de pánicos; START anclado a recepción; investigación del bloqueo TX; TX raw; FTM por turnos y vigía; reducción de ACK; prueba teléfono→ZIP→Tailscale→servidor→aplicación; purga de variantes experimentales y SD obsoleta; SOC disciplinado, reloj de 8 MHz, marcas temporales y frecuencia dinámica. |
| 26/10 | FIR común GEO/HAMMER; FIR de adquisición de 200 Hz; metadata de retardos; antialias Q1.23 de 90 dB nominales; fase de decimación 0, N, 2N; constante de latencia del ADC; matriz automatizada de banco y actualización de los tres submódulos en el superproyecto. |

## 2. Términos y arquitectura actual

### 2.1. Maestro ESP32-S3

El maestro de campo es el entorno `masterS3`, basado en Arduino 3.3.12 y ESP-IDF 5.5.5. La variante `masterS3_log` agrega el registro humano por UART0 para banco. Los entornos `masterS3_idf44` y `masterS3_idf44_log` quedan como respaldo sin FTM funcional.

Sus responsabilidades son:

- levantar `GeoNetwork` como SoftAP en el canal 1;
- servir la aplicación web desde LittleFS y el WebSocket en `/ws`;
- descubrir y mantener hasta ocho esclavos;
- enviar ARM, PRESTART, consultas de HOT_WAIT, START, STOP, pedidos de lotes, confirmaciones y OTA;
- recibir datos, marcas de ruido, marcas temporales, estados y registros remotos;
- responder sesiones FTM y emitir una baliza de reloj MAC a 2 Hz;
- reenviar los datos al navegador o a la interfaz USB/MATLAB;
- conservar la cola de enlace y la configuración del servidor.

El maestro usa modo Wi-Fi AP+STA, pero la captura no necesita una asociación STA. La aplicación permite guardar solamente la URL del servidor: el navegador del teléfono realiza la subida. Esto evita que el maestro haga escaneos STA durante la adquisición.

Toda transmisión ESP-NOW originada en el maestro usa actualmente `esp_wifi_80211_tx()` con una action frame compatible con ESP-NOW v2, tasa de 1 Mbps y un único elemento de información para los payloads vigentes. Los peers no están cifrados; el camino raw no sirve para ESP-NOW con Local Master Key (LMK) y bit Protected.

### 2.2. Esclavos ESP32-S3 con PSoC 5LP

El firmware S3 deriva del firmware común del esclavo y se regenera mediante `tools/sync_s3.py`. En la configuración actual de banco existen los entornos `slaveS3_2`, `slaveS3_3` y `slaveS3_4`. `SIM_SIN_HW=1` reemplaza el PSoC real por un simulador y la SD por almacenamiento simulado; debe desactivarse para la placa física. `REMOTE_LOG_ENABLE=1` replica el registro y el resumen de coredump al maestro.

En placa, el S3 se comunica con el PSoC por I2C y UART, mantiene la PSRAM para el anillo de captura, administra una SD local opcional del modo en vivo y controla:

- GPIO 7: SYNC hacia el PSoC;
- GPIO 1: SOC periódico de 500 us;
- GPIO 2: reloj continuo de 8 MHz para el PSoC;
- GPIO 16: solicitud de reset del PSoC;
- GPIO 8/9: I2C;
- GPIO 17/18: UART.

El reloj SOC usa MCPWM a 160 MHz, resolución de 6,25 ns y pulso nominal de 3 us. El período se disciplina suavemente con la deriva del modelo FTM y un lazo PI. Al armar un START se estira un único período para ubicar el siguiente borde sobre el origen temporal de la captura; después se retoma el período disciplinado. Si el modelo deja de estar vigente, se conserva la última deriva conocida y se registra `hueco=1`.

### 2.3. Esclavos ESP32 clásicos

Los esclavos WROOM clásicos siguen soportados sobre ESP-IDF 4.4. No implementan FTM ni activan por defecto el módulo nuevo de SOC/reloj externo. Reciben el START por broadcast y activan SYNC cuando se procesa la trama, por lo que su dispersión corresponde al camino legado. Si participa un clásico, no todos los nodos pueden programar START por FTM y la captura usa el respaldo compatible.

Los clásicos deben regrabarse con el firmware actual porque el filtro de MAC fue ampliado para aceptar la diferencia entre la MAC STA y la MAC AP localmente administrada del maestro S3.

### 2.4. PSoC 5LP y cadena analógica

El PSoC unifica las variantes GEO y HAMMER. Recibe configuración y órdenes del ESP, adquiere el ADC, puede seleccionar señal cruda o salida del bloque FIR, decima con antialias y entrega lotes de 30 muestras.

La RAM interna admite hasta 512 lotes por bloque del camino clásico. El modo en vivo usa un anillo y transfiere mientras se adquiere. La lógica `superMaquina` mantiene estados IDLE, ARMED, SAMPLING, DONE y ERROR, controla solicitudes de DMA y utiliza SYNC para pasar de armado a muestreo.

La topología física nueva todavía debe completarse en PSoC Creator. El comportamiento requerido es que los pulsos SOC externos alcancen el ADC solamente mientras SYNC esté alto, mediante lógica DSI/UDB sin intervención de la unidad central de procesamiento. El ADC debe quedar en Single Sample, 18 bits y Hardware SOC, con reloj no mayor que 3,027 MHz y una tasa de conversión cercana a 2400 muestras/s para aceptar un pulso cada 500 us.

El GPIO 2 del ESP debe alimentar un pin digital del PSoC. Desde allí se lleva por DSI a un PLL configurado como 8 MHz / 4 × 12 = 24 MHz de bus, igual al bus vigente. Esto reemplaza la dependencia de frecuencia del IMO, especificado en ±1 %, para la base de tiempo de la adquisición.

### 2.5. WebSocket, web móvil, servidor y aplicación de análisis

La web es una Single-Page Application (SPA) servida por el maestro. Usa un único dueño del WebSocket, se recupera de reconexiones, permite ARM/START/STOP, configuración por nodo, filtros, decimación, modos de captura, almacenamiento, OTA y exportación.

El diseño móvil dispone las pestañas en grilla, expande los campos al ancho de pantalla y mantiene START/STOP fijos. El protocolo web puede recibir lotes clásicos de 6 B o lotes GeoZ comprimidos, activados con `ZWEB`.

El ZIP vigente responde al contrato `geophone_scope_web_zip_v4`. Contiene señal cruda y metadatos; las derivaciones filtradas se reconstruyen. Incluye `noise_signatures.json` y, con las marcas nuevas, un `time_marks.csv` por nodo. El servidor FastAPI acepta `/ingest`, valida estructura, límites, duplicados, archivos declarados y columnas, conserva el ZIP y procesa en segundo plano. Puede exponerse por Tailscale; la prueba integrada utilizó `http://100.105.239.49:8000/ingest`.

La aplicación Python carga los canales, las firmas y las marcas temporales. Ajusta por LS una relación entre índice de muestra y reloj MAC del maestro, contempla el wrap de 32 bits y alinea varios canales por interpolación sobre una grilla común. Los ZIP antiguos sin marcas continúan siendo válidos y usan la frecuencia heredada como respaldo.

## 3. Flujo de una captura de punta a punta

### 3.1. Configuración y ARM

La web o el cliente de banco selecciona:

- modo: asincrónico, tiempo real o descarga rápida;
- almacén: 0 para RAM del PSoC, 1 para RAM compartida y 2 para RAM+SD;
- cantidad de lotes o captura sin límite;
- factor de decimación N;
- modo de sincronismo: FTM activo, FTM pausado o radio apagada;
- fuente ADC cruda o salida FIR del PSoC;
- FIR de navegador, rechazo de red y limpieza por firmas.

El maestro envía ARM a los nodos. En los S3, ARM y PRESTART se encolan desde el callback de recepción y se ejecutan en `loop()`, fuera de la tarea Wi-Fi. Cada esclavo configura el PSoC, prepara buffers y responde. Un nodo que falla o informa que no está listo se excluye de la máscara de la captura; no aborta a los demás.

### 3.2. PRESTART y HOT_WAIT

START no se emite de inmediato. El maestro entra en PRESTART, ordena a cada esclavo preparar el número de lotes y el modo, espera el asentamiento y consulta HOT_WAIT. El `HOTWAIT_ACK` incluye un motivo de rechazo. En modo vivo, el esclavo reintenta una vez la secuencia SD, modo vivo y cantidad de lotes antes de declararse no listo.

Solamente los nodos que confirman HOT_WAIT integran la máscara efectiva. Las balizas periódicas se coordinan con esta fase y el tráfico secundario se reduce en las ventanas críticas.

### 3.3. Selección del START

Si todos los nodos armados informan modelo FTM válido, el maestro toma su reloj MAC, elige un instante aproximadamente 400 ms en el futuro, lo alinea con la grilla nominal de muestreo y lo incluye en `CMD_START`. Cada esclavo convierte ese instante maestro a su reloj local y programa la subida de SYNC.

Si no puede usarse FTM, un esclavo S3 toma el timestamp de recepción que ESP-IDF 5 entrega en `rx_ctrl->timestamp` y programa SYNC para recepción + 20 ms. Como todos parten del timestamp de hardware de la misma trama, se elimina la mayor parte de la dispersión del scheduling del callback.

El clásico carece de ese camino y sube SYNC al procesar el broadcast. La metadata registra `ftm_scheduled` o `broadcast_start`; además, cada marca de START distingue FTM, anclaje a recepción o broadcast legado.

### 3.4. SOC, ADC y muestreo

En el diseño objetivo de placa, el S3 entrega un pulso SOC cada 500 us. La lógica del PSoC deja pasar esos pulsos al ADC únicamente mientras SYNC está alto. El ADC Single Sample de 18 bits inicia una conversión por pulso. La latencia calculada SOC→EOC es 413,737 us, basada en 1271 ciclos a 3,072 MHz; debe confirmarse con osciloscopio porque el reloj definitivo pedido no debe superar 3,027 MHz y la referencia temporal efectiva depende de la configuración real del componente.

El bloque FIR de adquisición puede entregar una versión pasabajos de 200 Hz. Después se aplica el FIR antialias de decimación. Para N > 1 solamente sobreviven las entradas 0, N, 2N, ... desde cada START. La primera llamada al decimador produce salida; esta corrección evita el desplazamiento anterior de fase.

La frecuencia exacta se informa en milihertz. En el modo SOC nominal, N=1 corresponde a 2000,000 Hz; con decimación, la salida es 2000/N. Los firmwares y ZIP antiguos mantienen 2604 Hz como respaldo de compatibilidad.

### 3.5. Transferencia PSoC→ESP y modos de almacenamiento

Cada lote contiene 30 muestras de 24 bits. El camino clásico guarda la ventana crítica en RAM del PSoC y vuelca después. El camino en vivo usa transferencia continua hacia el ESP y un anillo en RAM/PSRAM. El modo con SD agrega persistencia para recuperar o sostener capturas largas.

Los modos operativos son:

| Modo | Adquisición | Entrega al maestro |
|---|---|---|
| Asincrónico | Se completa la captura local antes del volcado. | El maestro pide cada lote con `REQ_BATCH`; puede pedir GeoZ comprimido. |
| Tiempo real | PSoC→ESP y ESP→maestro avanzan durante la captura. | Se envían lotes secuenciales; el maestro confirma por `STREAM_ACK` cada 8 lotes o 50 ms, con RTO de 150 ms. |
| Descarga rápida | Captura local seguida de ráfaga controlada. | Las mitades o tramas del lote esperan el callback de envío anterior para no saturar la cola. |

En tiempo real sin límite, STOP cierra la adquisición. El esclavo envía `STREAM_END`; si el maestro no lo recibe, repite STOP por unicast cada 300 ms a los nodos pendientes.

### 3.6. Confirmación, huecos y retransmisión

Los lotes llevan número de secuencia. El receptor detecta saltos y conserva huecos como `NaN` hasta recuperarlos. La web y `captura_ws.py` solicitan `FILL` con nodo, secuencia inicial y cantidad. El esclavo reenvía desde su almacenamiento. La corrida de descarte deliberado de 1 de cada 7 lotes recuperó 85 lotes y terminó con 18 000/18 000 muestras por nodo.

Los ACK del tiempo real se difieren a `loop()` si la cola Wi-Fi está llena. Los pedidos clásicos se reintentan a los 2 ms cuando la API informa falta de memoria. El relay web acumula datos y no vacía por cada cabecera o marca; solamente el control urgente se transmite de inmediato.

### 3.7. Marcas de ruido y marcas temporales

Las marcas de ruido se asocian a muestras y distinguen I2C, SD_IO, SD_SYNC, RADIO_TX, AP_BEACON y MASTER_RX. Las firmas aprendidas permiten identificar e interpolar segmentos contaminados. En el banco simulado con señal realista, las plantillas de I2C, SD_IO, RADIO_TX y AP_BEACON alcanzaron correlación 1,000, relación de amplitud 1,00 y desfase 0.

Las marcas temporales nuevas vinculan:

- token de captura;
- índice de muestra;
- reloj MAC del maestro;
- incertidumbre;
- tipo de ancla;
- validez del modelo.

El esclavo S3 mantiene un anillo de 2048 marcas. Durante silencio de radio las retiene; después las drena. Cada marca se transmite dos veces y la web deduplica por `(token, sample)`. No existe ACK individual para estas marcas.

### 3.8. Filtrado web, cierre y exportación

Durante la captura, el navegador aplica un FIR causal muestra a muestra sobre la vista y compensa su retardo de grupo en el eje. No aplica todavía notch ni limpieza por marcas. Al finalizar se ejecuta, en orden:

1. remoción de offset;
2. rechazo armónico de red;
3. limpieza de interferencias marcadas;
4. FIR con `filtfilt`, de fase cero.

Para capturas demasiado largas, el reprocesado completo puede limitarse a la ventana de visualización; se registra la advertencia correspondiente. La señal cruda se conserva siempre.

El ZIP exporta metadatos de frecuencia, N, perfil FIR, coeficientes Q1.23 cuando corresponden, fase de decimación, retardos de grupo, método de START, firmas y archivos de marcas. El navegador sube ese mismo ZIP al servidor configurado.

### 3.9. Servidor y ajuste temporal en Python

El servidor valida el contrato, guarda el ZIP y extrae la captura sin descartar `time_marks.csv`. La aplicación ajusta por LS:

`tiempo_maestro = a + b × muestra`

La pendiente entrega la frecuencia efectiva y el intercepto ubica el origen absoluto. La corrección común de latencia del ADC se resta del origen absoluto, no de la separación relativa entre canales. Después, los canales se interpolan sobre una grilla común para análisis de ondas superficiales multicanal (MASW).

## 4. Sincronización y base de tiempo

### 4.1. Modelo de reloj FTM

El maestro emite `CMD_TIME_BEACON` a 2 Hz con su reloj MAC. Cada esclavo mantiene una estimación gruesa y una recta sobre las últimas 16 sesiones FTM válidas. Se necesitan al menos cuatro sesiones para ajustar. El modelo se considera vigente durante 20 s.

Cada nodo posee un turno `node_id mod 8`: una ventana de 1 s cada 8 s. La sesión se inicia durante los primeros 300 ms de su turno. De esta forma no hay sesiones simultáneas sobre las tres plazas del responder.

El modelo se usa para:

- convertir un START futuro del reloj maestro al tiempo local del ESP;
- convertir anclas locales a reloj maestro;
- estimar deriva en ppb;
- disciplinar el período SOC;
- cuantificar el residuo temporal.

### 4.2. START medido

Resultados con tres nodos y diez START por método:

| Método | Mediana medida | Máximo medido | Interpretación |
|---|---:|---:|---|
| Broadcast legado, SYNC al ejecutar callback | 152 us | 374 us | Depende del scheduling de cada esclavo. |
| Broadcast anclado a recepción | 5 us | 10 us | Usa timestamp MAC local y timer; no requiere FTM del maestro. |
| Programado por FTM | 5 us | 7 us en la comparación; 1–5 us en los soaks finales | Preferido; todos programan el mismo instante maestro. |

Se observó un atraso común cercano a 15 us en las primeras pruebas FTM. Al ser común, no degradó la dispersión entre nodos, pero su origen no quedó explicado.

A 2604 Hz, una muestra dura 384 us. El broadcast legado ya quedaba dentro de una muestra, pero 374 us equivalen a aproximadamente 6,7° a 50 Hz. Un error de 10 us equivale a aproximadamente 0,2° a 50 Hz.

### 4.3. SOC disciplinado y reloj externo

**Implementado, calculado y no probado en placa:**

- MCPWM genera 2000 Hz nominales, pulso de 3 us y resolución de 6,25 ns.
- El período incorpora deriva FTM, acumulación fraccional de ticks y corrección PI de fase.
- La fase se define respecto de `T0 + k × período` y contempla wrap del reloj MAC de 71,6 min.
- GPIO 2 entrega 8 MHz desde el inicio de `setup()`, antes de liberar el PSoC.
- La frecuencia exacta y la frecuencia nativa viajan en HELLO y en metadata.

**Pendiente de implementación/confirmación física en PSoC Creator:**

- entrada LVTTL de SOC desde GPIO 1;
- entrada LVTTL de reloj desde GPIO 2;
- PLL 8 MHz / 4 × 12 = 24 MHz;
- ADC Single Sample, 18 bits y Hardware SOC;
- compuerta hardware SOC∧SYNC;
- SOC→EOC real y primera muestra efectiva.

### 4.4. Marcas como respaldo temporal

Las marcas periódicas permiten reconstruir la relación muestra→maestro aun cuando se acumule deriva. Las marcas START FTM, START RX y START broadcast declaran el origen. Si existe modelo FTM, la incertidumbre se propaga; si se pierde, el SOC conserva la última deriva y queda indicado el hueco.

El respaldo anclado a recepción evita depender del responder FTM para el inicio, pero no corrige por sí solo la deriva durante una captura larga. Las marcas periódicas y el reloj disciplinado son los elementos que agregan seguimiento temporal sostenido; ambos están pendientes de prueba física.

### 4.5. Medición obligatoria con osciloscopio

Se debe medir, sin confundir implementación con resultado:

1. 8 MHz estables y 50 % de ciclo útil en GPIO 2.
2. Período de 500 us y ancho cercano a 3 us en GPIO 1.
3. Relación SYNC→primer SOC aceptado.
4. SOC→EOC, con valor esperado cercano a 414 us.
5. Primera muestra válida después de START y fase 0, N, 2N del decimador.
6. Pulsos SOC de dos esclavos contra el marcador del maestro, durante varios minutos.
7. Deriva y residuo con FTM activo, pausado y radio apagada.

## 5. Filtros y retardos

### 5.1. FIR de adquisición de 200 Hz

Para frecuencia de entrada de 2000 Hz se incorporó un FIR Kaiser lineal de 127 taps útiles más un cero de relleno para las 128 palabras Q1.23 del bloque Filter del PSoC. La suma de los taps útiles es exactamente `2^23`, por lo que la ganancia en continua es uno.

| Métrica calculada sobre Q1.23 | Resultado |
|---|---:|
| Taps útiles | 127 |
| Retardo de grupo | 63 muestras = 31,5 ms |
| Ripple 0–50 Hz | 0,001233 dB |
| Ripple 0–150 Hz | 0,006973 dB |
| Rechazo desde 250 Hz | 66,491 dB |

La web selecciona este perfil cuando el nodo informa alrededor de 2000 Hz. Para 2604 Hz conserva el perfil de fábrica legado. La opción “Mismo FIR para martillo y geófonos” está activada por defecto y persiste en el navegador. Si se desactiva, se advierte que filtros distintos desplazan los tiempos de arribo.

### 5.2. Antialias Kaiser Q1.23

El antialias previo a decimación reemplazó la media móvil. Usa Kaiser, objetivo nominal de 90 dB, banda pasante hasta 0,8 veces el Nyquist de salida y rechazo desde 1,2 veces ese Nyquist. Los coeficientes se calculan al cambiar N, se cuantizan en Q1.23 y el producto se acumula en 64 bits.

La versión anterior Q15 exhibía un piso de cuantización: para N=16 caía a unos 64,6 dB. Q1.23 elimina esa limitación práctica. El máximo de 511 taps cumple el objetivo de diseño hasta N=17; desde N=18 el largo se recorta y la metadata indica que el objetivo no está garantizado.

| N | Taps | Retardo | Ripple 0–50 Hz | Rechazo desde 1,2 Nyquist de salida |
|---:|---:|---:|---:|---:|
| 2 | 59 | 14,5 ms | 0,000049 dB | 89,672 dB |
| 3 | 87 | 21,5 ms | 0,000135 dB | 89,479 dB |
| 4 | 117 | 29,0 ms | 0,000116 dB | 89,330 dB |
| 5 | 145 | 36,0 ms | 0,000162 dB | 89,059 dB |
| 6 | 173 | 43,0 ms | 0,000199 dB | 89,531 dB |
| 8 | 231 | 57,5 ms | 0,000231 dB | 89,323 dB |
| 10 | 287 | 71,5 ms | 0,000259 dB | 89,906 dB |
| 13 | 373 | 93,0 ms | 0,000319 dB | 90,145 dB |
| 16 | 459 | 114,5 ms | 0,000500 dB | 89,836 dB |

El test del header exacto del PSoC, con aproximaciones locales de seno y Bessel en `float`, midió 89,526 dB para N=16. Esta cifra es de host, no de placa.

El perfil web del FIR de adquisición conserva `stopband_attenuation_db: 60` como especificación nominal, mientras la respuesta calculada de sus coeficientes cuantizados es 66,491 dB desde 250 Hz. No son dos mediciones físicas distintas.

### 5.3. Cascada y retardos

El retardo total causal del camino filtrado en PSoC suma 63 muestras del FIR de adquisición y `(L-1)/2` muestras del antialias. No incluye la latencia del ADC.

| N | Retardo FIR total | Tiempo a 2000 Hz | Ripple de cascada 0–50 Hz | Rechazo de cascada |
|---:|---:|---:|---:|---:|
| 2 | 92 muestras | 46,0 ms | 0,001235 dB | 171,058 dB |
| 3 | 106 muestras | 53,0 ms | 0,001346 dB | 166,139 dB |
| 4 | 121 muestras | 60,5 ms | 0,001216 dB | 163,722 dB |
| 5 | 135 muestras | 67,5 ms | 0,001080 dB | 153,028 dB |
| 6 | 149 muestras | 74,5 ms | 0,001315 dB | 96,595 dB |
| 8 | 178 muestras | 89,0 ms | 0,001181 dB | 89,325 dB |
| 10 | 206 muestras | 103,0 ms | 0,001245 dB | 89,906 dB |
| 13 | 249 muestras | 124,5 ms | 0,001444 dB | 90,145 dB |
| 16 | 292 muestras | 146,0 ms | 0,001507 dB | 89,837 dB |

Para N=2 y N=3, la métrica hasta 0,8 Nyquist de salida incluye frecuencias por encima de la banda útil del FIR de 200 Hz; la gran variación allí es atenuación intencional, no ripple sísmico.

La constante de análisis `ADC_SOC_LATENCY_S = 1271 / 3,072e6 = 413,737 us` se resta del origen absoluto. Para una señal filtrada se debe sumar `(taps-1)/(2×Fs)`. Esta corrección es común a todos los nodos y no altera por sí sola la alineación relativa.

### 5.4. Fase de decimación

La fase se reinicia en cada captura. La primera entrada después del START es la muestra 0 y se conserva; para N=4 sobreviven 0, 4, 8, 12, ... Un test host verifica esa secuencia. En metadata quedan `first_retained_input_sample`, retardo en muestras de entrada/salida y retardo en segundos.

## 6. Problemas encontrados, evidencia y solución

### 6.1. Filtro de MAC incompatible con el AP del S3

**Problema:** el esclavo descartaba todo lo recibido del maestro S3.

**Causa:** la MAC del AP S3 activa el bit de administración local —por ejemplo `e2:` frente a `e0:`— y el filtro anterior solamente toleraba diferencia en el último byte.

**Solución:** se aceptan ambas formas de la MAC del maestro. Los clásicos deben recibir este firmware.

### 6.2. OTA revertida a los 180 s

**Problema:** la actualización volvía a la imagen anterior.

**Causa:** el esclavo esperaba tráfico del maestro para confirmar, pero en reposo no recibía nada.

**Solución:** el maestro responde a todo nodo que informa “sin confirmar”. En el banco simulado, 1,1 MB se transfirieron en unos 7 s y se confirmaron en unos 4 s.

### 6.3. Nodo no listo abortaba la captura completa

**Problema:** un nodo salteado en HOT_WAIT enviaba rechazo o NACK tardío y tiraba la captura de los demás.

**Solución:** el nodo fallido se elimina de la máscara efectiva; la captura sigue con los confirmados.

### 6.4. Descarga clásica lenta por `ESPNOW_NO_MEM`

**Problema:** se perdía aproximadamente un pedido de cada dos y 300 lotes × 2 nodos tardaban cerca de 100 s.

**Causa:** el tráfico TCP del WebSocket ocupaba la cola TX Wi-Fi.

**Solución:** `REQ_BATCH` se reintenta a los 2 ms. El mismo caso bajó a 11–16 s.

### 6.5. Confirmaciones de tiempo real perdidas

**Problema:** el esclavo frenaba por falta de ACK.

**Causa:** la confirmación se intentaba con la cola Wi-Fi llena.

**Solución:** `STREAM_ACK` se reintenta desde `loop()`. La cadencia vigente es cada 8 lotes o 50 ms, con RTO de 150 ms.

### 6.6. Relay WebSocket fragmentado

**Problema:** el maestro enviaba mensajes de 22 B promedio porque vaciaba el buffer con cada cabecera y cada marca.

**Solución:** solamente los paquetes de control salen de inmediato. Junto con el arreglo de ACK, una captura de 600 lotes pasó de 37 s a 7,5 s.

### 6.7. Descarga rápida con 23 % de pérdida

**Causa:** las dos mitades del lote se enviaban consecutivamente sin esperar confirmación del driver.

**Solución:** cada parte espera el callback de envío de la anterior. El resultado fue cero rellenos.

### 6.8. Esclavo ocupado después de una captura

**Problema:** OTA se rechazaba porque el nodo quedaba ocupado hasta el ARM siguiente.

**Solución:** `ota.py` manda ARM+STOP antes de ofrecer la imagen.

### 6.9. Reescaneo de canales y pérdida del ARM

**Problema:** después de 45 s sin ESP-NOW, algunos esclavos reescaneaban canales y quedaban sordos durante la captura siguiente.

**Solución:** las balizas del AP cuentan como señal de vida. Se obtuvieron 0 fallas en 3 intentos con 60 s de reposo.

### 6.10. HOT_WAIT fallaba después de `SET_RECLEN`

**Problema:** un nodo quedó afuera desde la web real con motivo 2.

**Solución:** el esclavo reintenta una vez la secuencia SD, modo vivo y cantidad de lotes, y registra el paso fallido.

### 6.11. Trabajo pesado dentro del callback Wi-Fi

**Problema:** el maestro perdía el AP, HTTP, WebSocket o responder FTM.

**Causa:** se pedía el reporte FTM y se volcaban lotes dentro de callbacks/secciones críticas.

**Solución:** `esp_wifi_ftm_get_report()` y el volcado de lotes se trasladaron a `loop()`. Los callbacks validan y encolan.

### 6.12. Pánico de esclavos al recibir ARM

**Problema:** nodos 3 y 4 sufrían `LoadProhibited` en `live::sendBatch`.

**Causa:** ARM se atendía en el callback ESP-NOW y liberaba el anillo mientras `loop()` retransmitía una sesión anterior.

**Solución:** ARM y PRESTART se difieren a `loop()`. El coredump de arranque se informa por radio a los 20 s, 40 s y 60 s.

### 6.13. STOP broadcast perdido

**Problema:** un nodo siguió transmitiendo después de STOP.

**Solución:** el maestro repite STOP por unicast cada 300 ms hasta recibir `STREAM_END` de todos los nodos de tiempo real.

### 6.14. TX maestro trabado en ESP-IDF 5.5, issue #19269

**Síntoma medido:** entre 1 min y 13 min el maestro dejaba de transmitir todo; desaparecían ARP, HTTP y WebSocket, FTM fallaba y `esp_now_send()` devolvía `NO_MEM` sin callbacks, aunque la recepción continuaba.

**Evidencia:** 9 de 11 corridas de 14 min fallaron en ESP-IDF 5.5 con distintas variantes; 0 de 2 fallaron en ESP-IDF 4.4. Se descartaron memoria, FTM, HT/AMPDU, escaneo STA y lock de lwIP.

**Causa verificada en binarios:** `esp_now_send()` inserta en `s_tx_cacheq` sin `g_wifi_global_lock`, mientras el consumidor extrae bajo ese lock. La intercalación puede desconectar el nuevo nodo de la lista.

**Solución vigente:** el maestro construye la action frame ESP-NOW sin cifrar y llama a `esp_wifi_80211_tx()`, que usa la misma cola con el lock global tomado. Se mantiene detector `[TXSTALL]`, un frame en vuelo y callbacks; se eliminó el reinit automático experimental.

**Limitación:** raw no soporta peers cifrados. El retorno del camino raw tampoco garantiza por sí mismo que `pp_post()` haya producido callback, por lo que el watchdog sigue siendo necesario.

### 6.15. Reinitialización Wi-Fi y mDNS

**Resultado experimental:** `esp_wifi_stop/start` no destrabó el TX. Apagar Wi-Fi y reconstruir AP, ESP-NOW y peers sí lo hizo en 100–600 ms, pero la PC tardó 67–115 s en reasociar y se perdieron 15–25 kB de heap por ciclo. Un intento llamó `MDNS.end()` después del deinit y produjo `LoadStoreError`.

**Decisión:** se corrigió el orden de mDNS, pero la recuperación automática completa fue eliminada durante la purga. No es apta para campo. La prevención es TX raw.

### 6.16. Responder FTM con plazas huérfanas

**Síntoma:** los nodos pasaban a `NO_RESPONSE` permanente, uno por uno.

**Causa verificada/inferida:** el blob posee tres plazas. La liberación por timer publica un evento; si falla la reserva o `pp_post()`, no reintenta y la plaza puede quedar ocupada. Una request de la misma MAC se ignora sin respuesta.

**Solución vigente:** turnos exclusivos de 1 s cada 8 s y vigía. Tres `NO_RESPONSE` seguidos de un nodo programan un reinicio Wi-Fi entre capturas, donde `wifi_softap_stop()` limpia las plazas.

### 6.17. IMO del PSoC y deriva entre nodos

**Problema:** la frecuencia de muestreo dependía del IMO del PSoC, especificado en ±1 %. El START sincronizaba el origen, pero no impedía deriva posterior.

**Solución implementada, no probada:** reloj de 8 MHz del ESP hacia PLL de 24 MHz, SOC disciplinado a 2000 Hz y marcas periódicas. La efectividad depende de completar el cableado y PSoC Creator.

### 6.18. Q15 frente a Q1.23

**Problema:** Q15 impedía sostener 90 dB en filtros largos; N=16 quedaba cerca de 64,6 dB.

**Solución:** coeficientes `int32` Q1.23, suma `2^23`, acumulador de 64 bits y redondeo simétrico. La RAM de coeficientes sube de 1022 B a 2044 B; el historial ocupa otros 2044 B. La cota conservadora del acumulador queda por debajo de `2^55`, con margen aproximado de 256,5 veces frente a `INT64_MAX`.

### 6.19. Fase incorrecta del decimador

**Problema:** la fase previa no garantizaba conservar la muestra 0 después de START.

**Solución:** reinicio por captura y salida en la primera entrada; quedan 0, N, 2N, ...

### 6.20. Limpieza por firmas sobre una señal simulada demasiado grande

**Problema:** con señal simulada de ±400 000 cuentas y marcas I2C en 23 % de las muestras, la interpolación agregaba más error de alta frecuencia que el que quitaba.

**Solución:** se repitió con amplitud representativa de geófono quieto, 2000 + 1000 cuentas. La limpieza explicó 73 % de alta frecuencia para RADIO_TX, 36 % para SD_IO, 28 % para I2C y 4 % para AP_BEACON, con errores de señal de 0,037; 0,140; 0,061 y 0,014, respectivamente.

### 6.21. Código experimental y almacenamiento obsoleto

Se eliminaron variantes experimentales de lock TCP/IP, AP en segundo plano, desactivación de baliza/FTM, reinicio automático, estadísticas Wi-Fi, diagnóstico `[SYNCBC]` y la antigua `sd_storage.*` sin llamadores. Se conservaron la SD física del PSoC, la SD vigente de `live_capture`, FTM, START RX, TX raw, coredump, STOP unicast, OTA, registro remoto y simulador.

### 6.22. Campos heredados incoherentes en la metadata de decimación

**Problema corregido en el código:** `applyNodeDecimation()` ya publica de forma consistente `first_retained_input_sample: 0`, `first_surviving_input_index: 0` y `coefficient_format: Q1.23`; la referencia de verificación apunta a `coefficients_2000hz_q23.csv`.

**Resultado:** la metadata del ZIP coincide con `aa_decim.h`: la fase se reinicia en cada captura y la primera llamada a `aa_push()` emite, por lo que sobreviven las muestras 0, N, 2N, ...

## 7. Pruebas y resultados

### 7.1. Banco simulado de dos nodos

| Prueba medida | Resultado por nodo |
|---|---|
| Asincrónico RAM, 300 lotes | 9000/9000; 11 s. Hubo un cero aislado del nodo 4 que no se repitió en tres intentos. |
| Asincrónico SD, 300 lotes | 9000/9000; 13 s. |
| Descarga rápida, 300 lotes | 9000/9000; 6 s; 0 rellenos. |
| Tiempo real, 600 lotes | 18 000/18 000; 7,5 s. |
| Tiempo real SD, 600 lotes | 18 000/18 000; 7,5 s. |
| Tiempo real, descarte 1/7 | 18 000/18 000; 85 lotes recuperados por FILL. |
| Tiempo real sin límite | STOP a 15 s; 1290 lotes; sin huecos. |
| FTM pausado, asincrónico | 9000/9000; 12 s. |
| Radio apagada, asincrónico | 9000/9000; 12,5 s. |

### 7.2. Duración

| Configuración medida | Duración | Resultado |
|---|---:|---|
| 2 nodos, N=1, 2604 Hz | 5 min | 26 030 lotes por nodo; atraso cercano a 15 lotes; vaciado 1 s. |
| 2 nodos, N=1, 2604 Hz | 14 min | 72 908 lotes por nodo; atraso 11–29 lotes; vaciado 1 s. |
| 3 nodos, ESP-IDF 5.5, `esp_now_send()` | 11 × 14 min | 9 bloqueos TX. |
| 3 nodos, TX raw sin turnos | 3 × 14 min | 0 bloqueos TX; responder FTM murió en la primera; START FTM en 2 de 4 intentos. |
| 3 nodos, TX raw + turnos | 5 × 14 min | 0 bloqueos TX; 0 muertes FTM; START FTM en 5 de 5; todos los lotes recuperados. |

Los JSON de las cinco corridas finales contienen aproximadamente 72 853–72 856 lotes por nodo. Durante una sesión FTM, el nodo no transmite datos y la vista puede quedar 1–3 s atrasada —habitualmente 90–280 lotes— sin pérdida final. Una corrida acumuló un atraso transitorio mucho mayor en un nodo y lo drenó después de STOP; por eso la matriz debe controlar tanto integridad final como atraso máximo.

### 7.3. Web, teléfono, ZIP y servidor

Se probaron desde Chrome tres capturas con lotes comprimidos:

| Captura | Muestras recibidas | Esperadas |
|---|---:|---:|
| Tiempo real, 5 s | 26 040 | 434 × 30 × 2 |
| Asincrónica, 3 s | 15 660 | 261 × 30 × 2 |
| Rápida, 3 s | 15 660 | 261 × 30 × 2 |

La prueba de teléfono emulado usó 412 × 915 px. La captura de punta a punta produjo 3 nodos × 261 lotes = 23 490 muestras, ZIP de 2,9 MB, subida por Tailscale y procesamiento exitoso. La aplicación cargó 7830 muestras por canal, sin huecos. No armó dataset por disparos porque los tres simulaban GEO y faltaba HAMMER.

El FIR pasabajos de 10 Hz y 101 taps avanzó en vivo junto con la traza cruda; el desplazamiento visual quedó compensado. Al cerrar se reemplazó por `filtfilt`.

### 7.4. Firmas de ruido

Con señal simulada realista, I2C, SD_IO, RADIO_TX y AP_BEACON alcanzaron correlación 1,000, amplitud 1,00 y desfase 0 respecto de la verdad inyectada. Las fuentes sin artefacto inyectado quedaron en picos de 72 cuentas para SD_SYNC y 16 para MASTER_RX.

### 7.5. Verificación de software de la capa nueva

Resultados ejecutados antes de este informe:

- `tools/sync_s3.py`: correcto e idempotente.
- Protocolos maestro/esclavo: SHA-256 idénticos.
- Sintaxis JavaScript: 18 archivos correctos.
- Python del submódulo: 142 pruebas aprobadas, 3 omitidas y 92 subpruebas aprobadas en la corrida de marcas.
- Antialias: pruebas Python/C y header real aprobados; 459 taps para N=16, fase correcta y comparación bit a bit.
- Matriz S3: 10 pruebas unitarias aprobadas; `--dry-run` listó 14 pruebas normales sin tocar hardware.
- Compilación PlatformIO: maestro S3, maestro con log, esclavos S3 2/3/4, respaldo IDF 4.4 y firmwares clásicos correctos.
- Aplicación Python, pruebas específicas de latencia/marcas: 11 aprobadas.

Estas verificaciones prueban compilación, protocolo y modelos de host. No prueban el ADC, el cableado, el timing del PSoC ni el ruido real de placa.

### 7.6. Matriz pendiente en placa

La matriz automatizada incluye:

| Grupo | Casos | Criterio principal |
|---|---|---|
| Estado | `estado` | HTTP 200, HELLO y modelo FTM de todos los nodos. |
| Asincrónico | `async_0..2` | 200 lotes, tres almacenes, sin faltantes/NaN. |
| Tiempo real | `rt_0..2` | 600 lotes, tres almacenes, sin faltantes/NaN. |
| Rápida | `rapida_1` | 200 lotes completos. |
| Sin límite | `rt_sinlimite` | 30 s, lotes iguales y sin huecos. |
| Pérdida deliberada | `droptest` | 600 lotes completos después de FILL. |
| Sincronismo | `sync_0..2` | FTM, FTM pausado y radio apagada; dispersión registrada. |
| OTA | `ota` | Reinicio, HELLO y modelo FTM recuperado. |
| Duración | `duracion` | Total ±1 %, atraso, drenaje y ausencia de incidentes. |
| Salud | `salud` | Sin TXSTALL, FTM muerto, reinicios, pánicos ni coredump nuevo. |

## 8. Pendientes y decisiones

### 8.1. Obligatorios antes de declarar la cadena temporal validada

1. Completar PSoC Creator: pines LVTTL, DSI, PLL, ADC y compuerta SOC∧SYNC.
2. Recompilar `AcondicionamientoAnalogico.cydsn` y revisar RAM, flash y timing con `aa_decim.h` Q1.23.
3. Grabar el PSoC real y desactivar `SIM_SIN_HW` en los esclavos.
4. Medir 8 MHz, SOC, SYNC, EOC, primera muestra y comparación entre nodos.
5. Ejecutar la matriz completa con PSoC y SD reales.

### 8.2. Capacidad de radio

La estimación por tiempo de aire, no medida con más de tres placas, asigna aproximadamente 9–10 % del canal por nodo a N=1 y 1 Mbps. Se estiman 5–6 nodos sostenibles. Para 8 GEO + HAMMER se debe decidir entre:

- N≥2;
- elevar la tasa PHY de ESP-NOW a 6–11 Mbps y medir alcance;
- escalonar o reducir telemetría secundaria.

No debe presentarse esta capacidad como validada hasta probar más de 5–6 nodos.

### 8.3. Campo

- Regrabar y ensayar esclavos clásicos.
- Calibrar distancia FTM con cinta en al menos tres distancias por nodo.
- Repetir firmas de ruido por placa con power bank y sin USB.
- Comprobar alcance, pérdida, latencia y backlog con la geometría real.
- Confirmar que todos los nodos exporten el mismo N, FIR y fase.

### 8.4. Decisiones abiertas

- Desactivar `SIM_SIN_HW` para placa real; se recomienda conservar `REMOTE_LOG_ENABLE`.
- Mantener maestro ESP-IDF 5.5 como principal y ESP-IDF 4.4 como respaldo.
- Decidir la política para más de 5–6 nodos.
- Decidir si el simulador y el registro remoto quedan habilitados en las imágenes de campo.

## 9. Uso operativo

### 9.1. Preparación del banco

La PC se conecta por Wi-Fi a `GeoNetwork`; puede conservar internet por Ethernet. El maestro S3 de banco usa COM14 y `masterS3_log`. No debe abrirse simultáneamente el puerto desde MATLAB y `log_maestro.py`.

```powershell
python lab/s3/log_maestro.py COM14 --reset
python lab/s3/maestro_ws.py
```

### 9.2. Capturas por WebSocket

```powershell
# Asincrónica, RAM compartida, 200 lotes
python lab/s3/captura_ws.py --modo async --almacen 1 --n 200 --nodos 2,3,4 --zweb

# Tiempo real, 600 lotes
python lab/s3/captura_ws.py --modo rt --almacen 1 --n 600 --nodos 2,3,4 --zweb

# Tiempo real sin límite; STOP a los 30 s
python lab/s3/captura_ws.py --modo rt --almacen 1 --n 0 --stop-s 30 --nodos 2,3,4 --zweb

# Descarga rápida
python lab/s3/captura_ws.py --modo rapida --almacen 1 --n 200 --nodos 2,3,4 --zweb
```

`--almacen 0/1/2` selecciona RAM PSoC, RAM compartida o RAM+SD. `--sync 0/1/2` selecciona FTM activo, FTM pausado o radio apagada. Las salidas quedan en `lab/s3/capturas/<marca>/`.

### 9.3. Matriz

```powershell
# Revisar el plan sin conectarse
python lab/s3/matriz_pruebas.py --dry-run

# Matriz normal
python lab/s3/matriz_pruebas.py --nodos 2,3,4 --log lab/s3/maestro.log

# Matriz completa con OTA y 14 min
python lab/s3/matriz_pruebas.py --con-ota --con-duracion --duracion-s 840

# Casos puntuales
python lab/s3/matriz_pruebas.py --solo estado,sync_0,salud
```

Cada caso produce JSON; al final se generan `resumen.json` y `resumen.md` bajo `lab/s3/matriz/<marca>/`. Un fallo hace que el proceso termine con código distinto de cero.

### 9.4. OTA

```powershell
python lab/s3/ota.py --node 2 --env slaveS3_2
python lab/s3/ota.py --node 3 --env slaveS3_3
python lab/s3/ota.py --node 4 --env slaveS3_4
```

Para grabar el maestro de campo por USB:

```powershell
cd "src/firmware/esp32/Nodo comunicación/masterS3"
pio run -e masterS3 -t upload --upload-port COM14
pio run -e masterS3 -t uploadfs --upload-port COM14
```

### 9.5. PSoC

Después de modificar y compilar en PSoC Creator:

```powershell
cd src/firmware/psoc
.\program_psoc.ps1 -SkipBuild
```

`-SkipBuild` programa los artefactos existentes; solamente debe usarse después de confirmar que corresponden al esquema y fuente recién compilados.

### 9.6. FTM y duración

```powershell
python lab/s3/ftm_registro.py --nodo 2 --declarada 5.0 --s 30 --ajustar
python lab/s3/prueba_duracion.py --n 1 --s 840 --nodos 2,3,4 --almacen 1 --sync 0
```

En PowerShell/Python, los argumentos numéricos normalmente requieren punto decimal aunque el informe use coma decimal; para evitar ambigüedad operativa, puede ser necesario escribir `5.0` en el comando.

### 9.7. Servidor y aplicación

```powershell
cd src/interfaces/python
python -m pip install -r server/requirements-core.txt
python -m server
```

El servidor escucha en `0.0.0.0:8000`. Variables relevantes:

- `TESIS_DATA_ROOT`: raíz común con `raw/`, `processed/` y `server/`;
- `TESIS_RAW_ROOT`, `TESIS_PROCESSED_ROOT`, `TESIS_SERVER_DATA_ROOT`: overrides independientes;
- `TESIS_HOST`, `TESIS_PORT`;
- `TESIS_READ_ONLY=1`;
- `TESIS_MAX_UPLOAD_BYTES`, `TESIS_MAX_ZIP_FILES`, `TESIS_MAX_UNCOMPRESSED_BYTES`, `TESIS_MAX_COMPRESSION_RATIO`.

Para la aplicación de escritorio:

```powershell
cd src/interfaces/python/geophone_scope
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

### 9.8. Estado de referencia revisado

- Superproyecto: `29c82da5`.
- Firmware ESP32: `7f21610`.
- Firmware PSoC: `e8d6474`.
- Interfaz Python: `2d07248`.
- Rama de firmware ESP32: `feat/tiempo-real`.
- Caché web: `field-study-50`.

No se realizó grabación de placas ni prueba por COM durante la preparación de este estado integral.

---

Proveniencia: IA principal Codex (modelo no reportado); delegados: ninguno; fallbacks: búsqueda PowerShell porque `rg` no estaba disponible.
