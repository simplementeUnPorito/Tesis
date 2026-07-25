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
