# Dudas y bloqueos del porteo automático

Escrito por el loop (`scripts/autonomia/port_loop.py`) y por los modelos que
corrieron sin supervisión. Se lee el lunes, en orden. Las entradas nuevas se
agregan al final con su fecha.

---

## 2026-07-24 — sembrado a mano antes de largar el loop

### 1. El canal del maestro cambió de 1 a 7 (esclavos ESP-NOW)

El maestro quedó asociado a `Flia. Martinez` (IP `192.168.100.219`) y su radio se
movió al canal del router: **canal 7**. El AP `GeoNetwork` sigue vivo en
192.168.4.1 porque corre `WIFI_AP_STA`, pero **los esclavos ESP-NOW tienen que
adoptar el canal nuevo** (el esclavo escanea el SSID del maestro y adopta su
canal, `link_mode.h:612`). No lo pude verificar: no probé una captura con
esclavos en esta sesión.

**Para el lunes**: encender un esclavo y confirmar que aparece en el maestro con
el canal 7. Si el router salta de canal solo (muy común en 2.4 GHz), esto se va a
repetir; habría que decidir si vale fijar el canal en el router.

### 2. `/enlace/scan` se auto-bloquea y tira al cliente del AP

Dos cosas distintas, las dos reales:

- El escaneo **desconecta a la PC del AP** (una sola radio: para escanear la saca
  del canal). Se ve como `WinError 10053/10060` y parece un problema de red. No lo
  es. `link_config.py` ya lo tolera reconectando.
- Con un SSID guardado que no existe, `linkScanPoll` (`link_mode.h:719`) entra en
  **livelock**: `scanComplete()` devuelve FAILED porque el `WiFi.begin()` de
  reintento está en curso, y el handler arranca otro escaneo, para siempre. El
  endpoint contesta 202 indefinidamente y nunca lista una red.

**Duda que no me corresponde decidir**: arreglarlo pide tocar firmware del
maestro (por ejemplo, no re-disparar el escaneo si hay un intento de STA en
curso, o suspender el retry de STA mientras se escanea). No lo toqué porque
reflashear el maestro corta el WiFi y vos no estabas para reconectar. Queda
anotado como fix chico y bien delimitado.

Mientras tanto no molesta: la verificación buena del SSID no es el escaneo, es
que la STA se asocie (`sta=up` + IP), y eso es lo que `link_config.py` exige.

### 3. Hardware que NO se tocó, a propósito

- **PSoC**: no se programó nada. La rama está sin terminar. `device_reset.py psoc`
  sólo hace `ToggleReset` por KitProg (no programa), y no lo ejecuté en esta
  sesión: sin un esclavo hablándole no hay forma de verificar que el reset salió
  bien, y un reset a ciegas dispara una auto-calibración de varios minutos.
- **Esclavo (COM12)**: no reseteado. Resetear el esclavo puede colgar el PSoC, y
  ahí sí haría falta el ToggleReset encadenado (`--and-psoc`).
- **Maestro (COM8)**: reseteado y verificado (arranca, el AP vuelve, `/health`
  responde). La cola del enlace sobrevivió: 1 archivo, 26684 B.

**Para el lunes**: probar `python scripts/autonomia/device_reset.py psoc
--wait-autocal` con el esclavo conectado, que es la única forma de ver si el PSoC
volvió sano (`psoc=1`, `IDLE`).

### 4. El servidor sigue siendo `http.server`, no FastAPI

Es el ítem `refactor` del loop (PORT_PLAN §1). Si el loop quedó bloqueado ahí,
esta es la razón por la que nada más avanzó: el loop **para** en el primer ítem
bloqueado en vez de arrastrar un refactor torcido a los siguientes.

### 5. Cómo leer el log si el loop pasó la noche esperando

La primera corrida se chocó con el límite de sesión a los 4 minutos
(`api_error_status=429`, *"You've hit your session limit · resets 11:20pm"*), ya
con el spec del refactor escrito y **$1.71 gastados**. El loop ahora:

- espera hasta la hora que anuncia el mensaje (no un backoff a ciegas), en tramos
  de 6 h como máximo para poder re-leer el mensaje real al despertar;
- no cuenta el límite como intento fallido ni escala de modelo por eso;
- si la fase ya había dejado su entregable antes del corte, la da por hecha en vez
  de pagarla de nuevo (fue exactamente lo que pasó con ese spec).

Así que en el log es **normal** ver horas de `límite de uso: espero hasta …`
seguidas de la misma fase retomando. No es un cuelgue.

**Cota real de esta corrida**: el techo no es el plan, es la cuota. El ítem
`refactor` solo costó $1.71 sólo en escribir su spec con Opus. Si el lunes ves
pocos ítems hechos, mirá `costo` en `--status` antes de sospechar del loop.

### 6. Cosas que el loop no puede validar y vos sí

El gate verifica HTTP y datos reales, no percepción. Nada de esto está cubierto:

- que un pick arrastrado a mano **se vea** donde tiene que verse;
- que la app PyQt vea el cambio de la web y al revés (criterio §6 del plan) —
  el check `capturas.pick` verifica el ida y vuelta por `frd.load_annotations`
  en sandbox, que es lo más cerca que llega sin un humano;
- que la web responda bien con 200+ capturas en el waterfall (§3.4, fuera de
  alcance de esta corrida).

---

## 2026-07-25 — escribiendo el spec de `tabs_tema` (§2)

### 7. Los nombres de función del PORT_PLAN §3.2 no existen

El plan dice filtrar con `signal_proc.py`: `dcRemove`, `filtFilt`,
`harmonicNotch`, `hilbertEnvelope`. **Ninguno de esos cuatro existe en el repo**
(son nombres estilo MATLAB; el código Python es snake_case). Lo que hay:

- `geophone_scope/signal_proc.py:367` `dc_remove`, `:235` `harmonic_notch`,
  `:37` `fir_filter` — el camino del **scope en vivo**.
- `geophone_scope/field_review_data.py:906` `apply_bandpass_filter` y `:873`
  `design_bandpass_filter` (Butterworth SOS + `sosfiltfilt`, fase cero) — el
  camino que **realmente usa el tab Filtros de la app PyQt**
  (`field_review_app.py:1970`).
- `hilbertEnvelope` no tiene equivalente: no encontré ningún cálculo de envolvente
  de Hilbert en `field_review_*`.

**Por qué me frenó**: para §2 no bloquea nada (sólo escribí placeholders, y ahí
cité los nombres reales). Bloquea al ítem §3.2 `Filtros`, que va a arrancar
buscando funciones que no están.

**Opciones que veo**:

1. Corregir §3.2 del plan para que diga `frd.apply_bandpass_filter` — es lo que
   da paridad con la app, que es el criterio del §6 del plan. Es lo que yo haría.
2. Portar además el DC/notch de `signal_proc` como opciones extra del tab web.
   Es funcionalidad que la app de review **no** tiene, así que sería
   funcionalidad nueva, no porteo — y el plan dice explícitamente que esto es una
   mudanza.
3. Si `hilbertEnvelope` era un pedido real y no un recuerdo de otra herramienta,
   hay que decidir si entra como feature nueva. No lo asumí.

No elegí ninguna: cambiar el alcance del §3.2 no me corresponde.

---

## 2026-07-25 — escribiendo el spec de `capturas_signal` (§3.1, parte 1)

### 8. El sandbox del gate escribe en el archivo de picks REAL

`frd._procesados_dir_for` (`field_review_data.py:63-69`) resuelve la carpeta de
salida por **`raw_root.name`**, no por la ruta completa. El sandbox del gate crea
su raw en `<tmp>\raw` (`server/smoke_test.py:597-599`), así que `name == "raw"`,
igual que `data\raw`. Consecuencia:

`default_annotations_path(<tmp>\raw)` == `default_annotations_path(data\raw)` ==
`C:\Github\Tesis\data\processed\raw\field_review_annotations.json`

Hoy no hizo daño porque `reviewed_count == 0` y el ZIP que ingesta el gate no
tiene par hammer+geo (sin shots, `Pipeline._process` no llama a
`save_annotations`). **Pero el día que tengas picks validados a mano, un check de
sandbox que ingeste una captura completa te los borra todos, sin aviso.** Es lo
que el §0.3 del plan ("nada se borra solo") prohíbe explícitamente.

**Por qué me frenó**: no bloquea el ítem §3.1-parte-1 (lo escribí de sólo
lectura, y los fixtures del gate se escriben directo en el raw temporal en vez de
pasar por `/ingest`). **Sí bloquea al ítem de `POST /api/pick`**, que escribe
anotaciones por diseño.

**Opciones que veo**:

1. Pasarle `TESIS_DATA_ROOT=<tmp>` en el `env` del `subprocess.Popen` de
   `start_server` (`smoke_test.py:516`) **sólo en modo sandbox**.
   `frd._discover_data_root` (`field_review_data.py:30-42`) ya respeta esa
   variable, así que todo `data/processed` del sandbox cae en el temporal y el
   modo `read` sigue viendo las anotaciones reales. Es lo que yo haría: una línea
   y no toca la capa de datos.
2. Que `_procesados_dir_for` use algo único por dataset (hash de la ruta
   absoluta, o la ruta completa espejada). Es más correcto de fondo —dos datasets
   llamados `raw` en distintos discos hoy comparten anotaciones **también en la
   app PyQt**— pero cambia dónde vive todo lo ya generado y habría que migrar
   `data/processed/*`. No lo decido yo.
3. Hacer una copia de seguridad del JSON de picks antes de cada corrida del gate.
   Es un parche, no un arreglo.

### 9. `catalog.pickable` y `discover_dataset` no coinciden (186 vs 194)

Medido hoy contra `data\raw`: el catálogo marca **186** capturas `pickable` en
`Canchiga`, y `discover_dataset` encuentra **194** disparos en esa misma carpeta.
Al revés también pasa: las 9 capturas de `Canchita` son `pickable: true` y
**ninguna** tiene `shot_id` (quedaron afuera por el dedup por firma de señal).

La causa es que hay **dos detecciones de rol distintas**:

- `catalog.py:104` lee sólo `node["role"]`;
- `frd._node_role` (`field_review_data.py:1754`) mira además
  `type`/`hw_type`/`name`/`data_dir`/`raw_file`.

**Por qué me frenó**: para este ítem lo esquivé (la web habilita el dibujo por
`pick.shot_id`, no por `pickable`, y está escrito en el spec). Pero significa que
la columna "Estado" de la tabla de Capturas **le miente al usuario en 8
capturas**: dice "sin martillo" en capturas que sí tienen martillo.

**Opciones que veo**:

1. Que `catalog.py` importe y use `frd._node_role`. Es una función privada de
   `frd`, y el §0 del plan dice no relajar ese contrato… pero acá no lo relaja:
   lo unifica. Es lo que yo haría.
2. Copiar la lógica de roles en `catalog.py`. Queda una tercera copia que se va a
   desincronizar: en contra del §0.4 del plan.
3. Exponer `node_role()` público en `field_review_data.py` y que los dos lo usen.
   Es lo más limpio, pero toca `geophone_scope`, que es código compartido con la
   app PyQt, y eso no lo decido yo.

Aparte, `/api/dataset` **no dice por qué** una captura no tiene `shot_id`
(¿sin martillo? ¿duplicada?). La web hoy lo explica con un texto genérico. Si
querés que diga "duplicada de X", hay que exponer `duplicate_of`
(`FieldShot.duplicate_of`, `field_review_data.py:105`) en el contrato de
`/api/dataset` — es un agregado, no rompe `refactor.contrato_dataset`, pero es
alcance nuevo.

#### RESUELTA (2026-07-25, respondida por Elías)

La premisa de la duda era equivocada: **las cuatro funciones existen**. Los nombres
están en camelCase porque vienen del **SPA del maestro**, que las tiene
implementadas en JavaScript (`master/data/js/signal_proc.js` las exporta todas:
`dcRemove:224`, `filtFilt:195`, `harmonicNotch`, `hilbertEnvelope:284`). También
hay versiones en Python y en MATLAB. O sea: no hay nada que inventar ni ningún
alcance que cambiar, y `hilbertEnvelope` tampoco es una feature nueva.

Qué hace cada una, ya escrito en el §3.2 del PORT_PLAN (que es lo que leen todas
las fases del loop, a diferencia de este archivo, que sólo se escribe):

- `dcRemove`: quita la continua.
- `filtFilt`: pasabanda Butterworth de **fase cero** — no corre los tiempos de
  arribo, que es justo lo que no se puede romper para el picking.
- `harmonicNotch`: cancela ruido de línea estimando **por RMS** las senoidales en
  los armónicos de la frecuencia de línea y restándolas. El maestro es donde está
  mejor explicado (`app.js:1298`, LS de armónicos sobre la ventana completa).
- `hilbertEnvelope`: envolvente por transformada de Hilbert.

Más el orden de la cadena, que no estaba escrito en ninguna parte del plan y sí
importa: **FIR → DC → notch**, con el notch último y sobre la ventana completa.

La instrucción para el loop quedó como "buscá la implementación que te convenga y
llamala, no la reescribas", sin atarlo a un nombre ni a un archivo.
