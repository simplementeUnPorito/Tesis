SPEC_READY

# capturas_signal — §3.1 (parte 1) `GET /api/signal` con decimado min/max + dibujo de hammer y geo

Objetivo: que un humano pueda **ver** una captura desde la web —martillo arriba,
geófono abajo, el trigger marcado— con la serie decimada **en el servidor** por
min/max, sin perder picos y sin mandar 10.800 muestras crudas por canal al
navegador.

**Alcance exacto de este ítem** (§3.1 del plan es más grande que esto):

| Del §3.1 | ¿Entra? |
|---|---|
| `GET /api/signal?shot_id=&kind=&max_points=` con decimado min/max | **sí** |
| Dibujar hammer + geo con el trigger marcado | **sí** |
| Polaridad fija (geo no invertido, hammer invertido) | **sí** (viene de `load_signal`) |
| `geo_flip` como *preview* (sin guardar) | **sí**, por query param — ver §4.4 |
| Arrastrar el marcador y **guardar** / `POST /api/pick` / `frd.save_annotations` | **NO** — próximo ítem |

Este ítem es **de sólo lectura**. No escribe ni una anotación. La razón no es
pereza: escribir anotaciones desde el gate hoy pisaría el archivo real de picks
(ver §8.1, es la trampa más peligrosa que encontré). El ítem que agregue
`POST /api/pick` tiene que arreglar eso **antes** de escribir nada.

**Nada de dependencias nuevas, ni build step, ni CDN.** La web se sirve por
Tailscale a un campo sin internet. Canvas 2D + módulos ES nativos, como ya hace
`main.js`. En el servidor: numpy (ya está, lo usa `field_review_data`).

---

## 1. Datos reales: los números que importan (verificados hoy, no los re-averigües)

Corrí `discover_dataset` y `dataset_summary` contra `C:\Github\Tesis\data\raw`:

| Dato | Valor real | Consecuencia para este ítem |
|---|---|---|
| capturas catalogadas | 210 (`capture_count`), 415 nodos | el gate ya lo exige (`MIN_CAPTURES=200`) |
| disparos con par hammer+geo | **194** (`shot_count`) | sólo esos 194 tienen `shot_id` y se pueden dibujar |
| carpetas con disparos | **una sola**: `Canchiga` (194). `Canchita` (9 capturas) queda entera fuera por dedup de capturas | no asumas "una carpeta = un sitio" en la UI |
| fs presentes | 1020 Hz (122 disparos) y 2929 Hz (72) | no hay 2604 Hz en este dataset |
| muestras por canal | **entre 8551 y 10800** (8.5 s a 2929 Hz, 10.6 s a 1020 Hz) | ver el párrafo de abajo |
| capturas donde hammer y geo tienen distinto largo | 4 | cada canal se decima con **su** largo (§4.3) |
| disparos con `filt_f32le.bin` | 194 (todos) | `kind=filt` es probable en todos |
| `reviewed_count` | 0 | hoy **ningún** disparo tiene anotación humana |
| `discover_dataset(data/raw)` | **1.2 s** (356 MB de `.bin`, hashea todos) | no va en el event loop (§4.6) |

**Corrección al plan, importante**: PORT_PLAN §3.1 habla de "60 s a 2604 Hz =
~156 k muestras". **En el dataset actual el máximo es 10.800 muestras** (~43 kB
por canal). El decimado sigue haciendo falta —10.800 puntos en un canvas de
~900 px es 12× más de lo dibujable, y el JSON crudo con 6 dígitos son ~200 kB
por canal— pero **no dimensiones los checks contra 156 k**: un assert
`samples > 100000` fallaría siempre. La cota que sí vale: `samples > max_points`
con `max_points=500`.

---

## 2. Archivos a crear / editar (rutas absolutas)

### Crear

| Ruta | Contenido |
|---|---|
| `C:\Github\Tesis\src\interfaces\python\server\signal_view.py` | La lógica pura: `decimate_minmax()` y `build_signal_payload()`. Sin FastAPI, sin `Request`. Es donde vive el min/max y el redondeo. |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\tabs\capturas_signal.js` | El visor: dos canvases (hammer/geo), controles (`raw`/`filt`, invertir geo), y el fetch a `/api/signal`. Exporta `mountViewer(host)` que devuelve `{ show(shotId, meta), destroy() }`. Se mantiene aparte de `capturas.js` para no volver a tocar `renderJobs`/`renderDataset`, que ya andan. |

### Editar

| Ruta | Qué |
|---|---|
| `...\server\routers\dataset.py` | agregar la ruta `GET /api/signal`. **Ahí y no en `picks.py`**: PORT_PLAN §1 asigna a `dataset.py` "catálogo, capturas, **señales**" y a `picks.py` "anotaciones (leer/escribir)". `picks.py` queda intacto para el ítem que viene. |
| `...\server\static\js\plot.js` | agregar `drawMinMax(canvas, ch, opts)` y `drawVLine(...)`. **No borrar `drawSeries`** (`plot.js:4`): el check `refactor.estaticos` sólo pide que el archivo exista y pese >100 B, pero borrar una export que otro ítem puede estar por usar no aporta nada. |
| `...\server\static\js\tabs\capturas.js` | (a) columna con un botón `ver` **sólo** cuando `c.pick && c.pick.shot_id`; (b) montar el visor de `capturas_signal.js` arriba de la tabla; (c) que el `setInterval` de 3 s (`capturas.js:62`) **no** vuelva a pedir la señal (§5.3). |
| `...\server\static\css\app.css` | `.viewer`, `canvas.plot`, `.plot-label`, `.viewer-meta`. Reusar las variables que ya están (`--panel-bg`, `--panel-border`, `--th-fg`, `--td-border`); **no** hardcodear colores de fondo/texto nuevos o se rompe el tema oscuro. Los colores de traza sí son literales (§6.3). |
| `...\server\smoke_test.py` | los 12 checks `capturas.signal.*` de §7, en una sección nueva `# ── Checks capturas/señal (§3.1: GET /api/signal + dibujo) ─` después de los `tabs.*`. |

### No tocar

`api.py` (en particular **el orden de `add_middleware`**, `api.py:69-89`: si
metés algo después de `_TitleCaseHeaders` deja de ser el más externo y
`base.cors_preflight` empieza a fallar por una razón que no tiene nada que ver),
`app.py`, `pipeline.py`, `catalog.py`, `routers/ingest.py`, `routers/admin.py`,
`routers/picks.py`, `routers/masw.py`, `static/index.html`,
`static/js/main.js`, `static/js/theme*.js`, `borrado.js`, `masw.js`, y **todo
`geophone_scope/`**.

`index.html` no se toca a propósito: `#panel-capturas` ya está vacío y lo llena
`capturas.js`. Si le agregás markup con `fetch(` / `setInterval(` / `<style`
rompés `refactor.index_sin_logica` (`smoke_test.py:244-253`).

---

## 3. Funciones existentes a REUSAR (esto es lo que no vas a encontrar solo)

Nada de esto se reimplementa. Si te da ganas de copiar una fórmula, es señal de
que hay que llamar a la que ya está (PORT_PLAN §0.4).

### Capa de datos (`C:\Github\Tesis\src\interfaces\python\geophone_scope\field_review_data.py`)

| Qué | Dónde | Notas |
|---|---|---|
| `discover_dataset(raw_root)` → `FieldDataset` | `:184` | 1.2 s en el dataset real. Devuelve `.shots`; **descarta** capturas sin par hammer+geo y las duplicadas (§5.5 del plan) |
| `FieldShot` (`shot_id`, `folder_name`, `capture_name`, `fs`, `distance_m`, `hammer`, `geo`) | `:92` | `shot_id` = `sha1(ruta relativa de la captura)[:16]`, se arma en `:1612` |
| `ChannelRef` (`role`, `pcb_id`, `raw_file`, `filt_file`, `fs`, `label`, `invert_signal`) | `:72` | `signal_file(prefer_filtered)` en `:84` decide qué archivo se lee y **cae al raw si no hay filt** |
| **`load_signal(channel, prefer_filtered, apply_invert=True)`** | `:324` | `np.fromfile('<f4')` + la negación de polaridad. **Llamalo con `apply_invert=True`** (default) |
| Convención de polaridad fija | `:1664-1673` (y `:1709` para el layout sin metadata) | `invert_signal` NO es "el archivo está invertido": es *la negación que hay que aplicar al cargar* para llegar a la convención **geo no invertido / hammer invertido**. Por eso el hammer sin marca en la metadata sale negado. **No lo re-implementes ni lo "corrijas"** |
| **`detect_hammer_trigger(signal, fs, search_window_s=None)`** → índice | `:367` | umbral robusto sobre la derivada suavizada; opera **sobre la señal del martillo** |
| **`auto_pick_shot(shot, prefer_filtered, search_window_s)`** → `PickAnnotation` | `:348` | envuelve a `detect_hammer_trigger` y devuelve `trigger_s`. Es lo que hay que usar para el trigger cuando no hay anotación |
| `PickAnnotation` (`trigger_s`, `arrival_s`, `accepted`, `reviewed`, `source`, **`geo_flip`**) | `:108`; qué significa `geo_flip`, `:118-123` | `geo_flip` se aplica **después** de la convención fija |
| `load_annotations(path)` | `:394` | sólo lee; devuelve `{}` si el archivo no existe |
| `default_annotations_path(raw_root)` | `:1577` | → `data/processed/<raw_root.name>/field_review_annotations.json`. **Ojo: hace `mkdir`** (`:63-69`). Ver §8.1 |
| `_zero_by_pretrigger(signal, trigger_idx, fs)` | `:1854` | resta la mediana de la ventana pre-trigger (−250 ms … −5 ms). Es **privada** pero existe; usala (`from field_review_data import _zero_by_pretrigger`) en vez de copiar las 6 líneas. El mismo cálculo está duplicado en `field_review_app.py:1789`, no agregues una tercera copia |
| `peak_to_peak(samples)` | `:334` | por si querés mostrar el p2p en el encabezado del visor. Opcional |

### La app PyQt, para copiar el comportamiento visual (`geophone_scope\field_review_app.py`)

| Qué hace la app | Dónde | Qué copiar |
|---|---|---|
| carga el par y aplica `geo_flip` | `_load_pair`, `:1056-1070` | el orden: `load_signal(apply_invert=True)` **y después** el flip por muestra |
| resta la línea de base | `_zeroed_pair`, `:1085-1089` | `trigger_idx = clip(round(trigger_s*fs), 0, n-1)` y el mismo `trigger_idx` para los dos canales |
| dibuja | `_refresh_plot`, `:1091-1138` | **eje del hammer absoluto** (`time = arange(n)/fs`), **eje del geo desplazado**: `geo_time = time - trigger_s` (`:1102`) |
| marca el trigger | `:1114-1134` | línea llena sobre el hammer en `trigger_s`; línea **punteada** sobre el geo en `0.0` |
| zoom inicial | `:1136-1137` | hammer `[trigger−0.15 , trigger+0.65]`, geo `[max(t0,−0.08) , min(tN, 1.1)]` |
| colores | `_plot_colors`, `:1510-1513` | claro: hammer `#cc5a00`, geo `#0066cc`; oscuro: hammer `#ffb86b`, geo `#69b7ff`. Trigger: `#e67e22` claro / `#ff9f43` oscuro (`:1119`) |

### Servidor (`C:\Github\Tesis\src\interfaces\python\server\`)

| Qué | Dónde |
|---|---|
| `dataset_summary(pipeline)` y el índice de picks por `(carpeta, captura)` | `routers/dataset.py:15`, el índice en `:30-47` — de ahí sale el `shot_id` que consume la UI |
| `get_pipeline` (DI) y `pipeline.raw_root` | `api.py:22`; `pipeline.py:93` |
| `frd` ya importado con el `sys.path` resuelto | `pipeline.py:30-34` — importá `from ..pipeline import frd` como hace `routers/dataset.py:8`. **No** vuelvas a manosear `sys.path` |
| ejemplo de trabajo bloqueante fuera del event loop | `routers/ingest.py:36` (`run_in_threadpool`) |
| registro de routers | `api.py:91-95` — `dataset.router` ya está incluido, no hay que tocar nada |

### Gate (`server\smoke_test.py`)

| Qué | Dónde |
|---|---|
| decorador `@check(cid, desc, mode)` — el registro se descubre solo | `:136-140` |
| `Ctx.get` / `post` / `json_get` (todo queda logueado con código y duración) | `:100-122` |
| `Ctx.sandbox` y `Ctx.raw_root` | `:76-79`; se arman en `main()`, `:596-607` |
| cotas del dataset real | `:59-60` |
| logs (uno por corrida + uno por servidor) | `:55`, `:592` — el propio gate imprime las rutas al terminar |

### Front (`server\static\`)

| Qué | Dónde |
|---|---|
| tabla del dataset que hay que ampliar con el botón `ver` | `js/tabs/capturas.js:87-129` (la fila, `:118-126`) |
| el `tick()` de 3 s | `js/tabs/capturas.js:29-40`, `:62` |
| andamio de dibujo | `js/plot.js:4` (`drawSeries`) |
| variables CSS de los dos temas | `css/app.css:1-30` |

---

## 4. El endpoint, contrato exacto

### 4.1 Firma

```
GET /api/signal?shot_id=<16 hex>&kind=raw|filt&max_points=<int>&geo_flip=0|1
```

- `shot_id` (obligatorio): el de `FieldShot.shot_id`, tal como lo publica
  `/api/dataset` en `capture.pick.shot_id`.
- `kind` (default `raw`): `raw` → `prefer_filtered=False`; `filt` →
  `prefer_filtered=True`. Cualquier otro valor → **400**.
  **`filt` es el `filt_f32le.bin` que grabó el nodo**, no el pasa-banda de §3.2
  del plan. Decilo en el `title`/tooltip del control para que nadie crea que ya
  está portado el tab Filtros.
- `max_points` (default `2000`): buckets pedidos. Se **clampea** a
  `[100, 20000]`, no se rechaza (un cliente que pide 1 no merece un 400, merece
  el mínimo). No numérico → dejá que FastAPI conteste 422; lo que no se acepta es
  un 500.
- `geo_flip` (opcional): ausente → se usa el `geo_flip` de la anotación.
  `0`/`1` → **override de preview**, sin escribir nada. Existe porque la app
  invierte la traza al toque con la tecla `X`
  (`field_review_app.py:1524`, `:1748`) y recién guarda después; y porque es la
  única forma de que el gate pruebe el flip sin escribir anotaciones (§8.1).

Códigos: `200` OK · `400` `kind` inválido · `404` `shot_id` inexistente (**no**
200 con canales vacíos, **no** 500) · `422` query mal tipada.

### 4.2 Respuesta

```json
{
  "shot_id": "f6d6d0954a6dd85a",
  "folder": "Canchiga",
  "capture": "023_actual",
  "distance_m": 48.0,
  "fs": 1020.0,
  "kind": "raw",
  "max_points": 2000,
  "trigger_s": 0.4137,
  "trigger_source": "annotation",
  "reviewed": false,
  "accepted": true,
  "geo_flip": false,
  "geo_flip_source": "annotation",
  "channels": {
    "hammer": {
      "role": "hammer", "pcb_id": "S1", "label": "Hammer",
      "file": "Canchiga/captures/023_actual/hammer_s1/raw_f32le.bin",
      "used_filtered": false,
      "invert_applied": true,
      "flip_applied": false,
      "samples": 10800,
      "duration_s": 10.588235,
      "stride": 6,
      "buckets": 1800,
      "bucket_dt": 0.00588235,
      "decimated": true,
      "y_min": -1.83, "y_max": 0.42,
      "min": [ ... 1800 números o null ... ],
      "max": [ ... 1800 ... ]
    },
    "geo": { "...igual...": null }
  }
}
```

Reglas del payload, todas chequeadas en §7:

1. **`min` y `max` tienen la misma longitud, y esa longitud es `buckets`.**
2. `buckets <= max_points` siempre.
3. `t` **no se manda**: el cliente lo deriva (`t_i = i * bucket_dt`). Mandar el
   eje triplica el JSON por nada; es una grilla uniforme.
4. `file` es relativo a `raw_root` con `/` (mismo criterio que
   `catalog.py:115`). Nunca una ruta absoluta del disco del servidor.
5. **Nada de `NaN` / `Infinity` en el JSON.** `json.dumps` los escribe como
   literales `NaN`, que **no son JSON válido** y hacen explotar `JSON.parse` en
   el navegador. Todo valor no finito va como `null` (bucket sin dato real).
   Esto no es teórico: la capa de datos usa NaN a propósito para "acá no hay
   muestra" (`frd.segment_nan_padded`, `field_review_data.py:1863`).
6. Redondeo: **6 dígitos significativos**, `float(f"{v:.6g}")`. No redondees a
   N decimales fijos: las amplitudes van de ~1e-3 a ~3 V y `round(v, 4)`
   aplasta las chicas a cero.
7. `trigger_source`: `"annotation"` si `load_annotations()` tiene el
   `shot_id`, `"auto"` si el trigger salió de `auto_pick_shot`. Hoy **todas** las
   respuestas van a decir `"auto"` (`reviewed_count == 0`).

### 4.3 El decimado min/max (el corazón del ítem)

En `signal_view.py`, función pura y testeable:

```python
def decimate_minmax(x: np.ndarray, max_points: int) -> tuple[np.ndarray, np.ndarray, int]:
    """Envolvente min/max por bucket. Devuelve (mins, maxs, stride).

    Por qué min/max y no un promedio ni un salteado: el primer arribo es un
    pico de pocas muestras. Promediar lo suaviza hasta hacerlo invisible y
    saltear se lo come cuando el pico cae entre dos muestras elegidas. Con
    min/max, cada píxel dibuja el rango real que hay abajo: la envolvente pasa
    exactamente por los extremos de la señal completa.
    """
```

Implementación pedida (vectorizada; nada de bucles sobre muestras):

```python
n = int(x.size)
stride = max(1, -(-n // max_points))        # ceil(n / max_points)
nb = -(-n // stride)                        # ceil(n / stride)  <= max_points
pad = nb * stride - n
if pad:
    x = np.concatenate([x, np.full(pad, np.nan, dtype=np.float32)])
m = x.reshape(nb, stride)
with warnings.catch_warnings():             # buckets all-NaN avisan y devuelven NaN
    warnings.simplefilter("ignore", RuntimeWarning)
    mins, maxs = np.nanmin(m, axis=1), np.nanmax(m, axis=1)
```

- `stride == 1` ⟹ `decimated: false` y `min == max` elemento a elemento (la
  serie cruda). Ese es el camino que usa el check de §7.2 como referencia.
- **Invariante que define "min/max está bien hecho"**:
  `max(maxs) == max(x_finito)` y `min(mins) == min(x_finito)`, exactamente
  (salvo el redondeo a 6 cifras). Un decimado que promedia o saltea **no**
  cumple esto, y eso es justo lo que chequea `capturas.signal.decimado_conserva_picos`.

Orden de operaciones (no lo cambies, cambia el resultado):

1. `load_signal(channel, prefer_filtered=(kind=="filt"), apply_invert=True)`
2. `geo` (sólo geo): si el flip efectivo está activo → `geo = -geo`
3. `trigger_idx = clip(round(trigger_s * fs), 0, n-1)`;
   `_zero_by_pretrigger(canal, trigger_idx, fs)` para **cada** canal, con el
   mismo `trigger_idx` (así lo hace `field_review_app.py:1085-1089`)
4. `decimate_minmax(...)` por canal
5. redondeo + no-finitos a `null`

**Cada canal se decima con su propio largo.** La app trunca los dos al mínimo
(`field_review_app.py:1061-1062`) porque después promedia; acá no: 4 disparos
tienen canales de largo distinto y recortar el geo para que empate con el hammer
esconde muestras reales, que es exactamente lo que el plan pide no hacer
("nunca esconder"). Por eso `samples` y `duration_s` son **por canal**.

### 4.4 `geo_flip`

`geo_flip` efectivo = el del query param si vino, si no el de la anotación, si no
`false`. Se aplica **sólo al geo**, **después** de `load_signal`, y se reporta
en `channels.geo.flip_applied` + el `geo_flip` / `geo_flip_source` de arriba.
Nunca al hammer. Este ítem **no lo persiste**.

### 4.5 De dónde sale el `shot_id`

`discover_dataset(pipeline.raw_root)` y buscar por `shot_id`. No hay índice y no
hace falta inventar uno: 194 shots, un `next(...)` sobre la lista.

Se puede cachear el resultado por `(raw_root, mtime)`, pero **no lo hagas en
este ítem**: `dataset_summary` (`routers/dataset.py:15-26`) recalcula por pedido
a propósito, y su comentario explica por qué (la app PyQt toca el volumen por
fuera y la web no puede mostrar un estado viejo). Un caché acá tiene que ser una
decisión consciente sobre invalidación, no un efecto colateral.

### 4.6 Fuera del event loop

`discover_dataset` son **1.2 s** y `np.fromfile` de dos archivos más el decimado
son otros ~50 ms. Si eso corre en el loop de asyncio, `/health` y toda la web se
frenan.

La forma más simple y correcta: **declarar el handler con `def`, no con
`async def`**. FastAPI corre los handlers síncronos en su threadpool
automáticamente. Si por algún motivo lo hacés `async`, entonces el trabajo va
adentro de `run_in_threadpool` (patrón ya usado en `routers/ingest.py:36`).
`capturas.signal.no_bloquea` (§7.8) falla si esto sale mal.

---

## 5. El front: qué se ve

### 5.1 Estructura

Arriba del `<section>` "Capturas" de `capturas.js:17-26`, un
`<section class="viewer">` con:

- encabezado: `carpeta / captura · <distancia> m · fs Hz · N muestras ·
  trigger 0.4137 s (auto)`;
- dos `<canvas class="plot">`: **hammer arriba, geo abajo** (mismo orden que la
  app), cada uno con su etiqueta;
- controles: radio/segmented `raw` | `filt`, checkbox **"Invertir geo (preview)"**
  → `geo_flip=1`, y un botón `recargar`;
- una línea honesta, con el mismo criterio que los placeholders de §2 del plan:
  `Sólo lectura: arrastrar el trigger y guardar el pick es el próximo paso
  (POST /api/pick, PORT_PLAN §3.1).`

En la tabla de `renderDataset` (`capturas.js:104-128`), una columna nueva al
final:

- `c.pick && c.pick.shot_id` → `<button data-shot="…">ver</button>`;
- si no → texto `—` con `title` explicando por qué: *"no hay disparo hammer+geo
  asociado (sin martillo, o captura duplicada — PORT_PLAN §5.5)"*.

**No uses `c.pickable` para habilitar el botón.** Medido hoy: el catálogo
declara 186 capturas `pickable` en `Canchiga` pero `discover_dataset` encuentra
**194** disparos ahí, porque `catalog.py:104` deduce el rol sólo de
`node["role"]` mientras `frd._node_role` (`field_review_data.py:1754`) mira
además `type`/`hw_type`/`name`/`data_dir`/`raw_file`. Y al revés: las 9 capturas
de `Canchita` son `pickable: true` y **no** tienen `shot_id` (quedaron fuera por
dedup). La única condición correcta para "esto se puede dibujar" es
**`pick.shot_id` presente**. (Queda anotado en `DUDAS_LUNES.md`: unificar las dos
detecciones de rol no es decisión de este ítem.)

Delegá el click en el contenedor de la tabla (`#dataset`) por `data-shot`, no con
`onclick=` inline ni un listener por fila: `renderDataset` reescribe el
`innerHTML` en cada tick de 3 s y se perderían.

### 5.2 Dibujo (`plot.js`)

```js
export function drawMinMax(canvas, ch, opts = {})   // envolvente min/max
export function drawVLine(canvas, xSec, opts = {})  // marca del trigger
```

- Un `moveTo`/`lineTo` **por bucket** entre `min[i]` y `max[i]`: es una columna
  de 1 px de alto real, y así el pico se ve. Bucket `null` → no se dibuja
  (`ctx.stroke()` del tramo anterior y seguir), no lo trates como 0.
- Escala vertical: `y_min`/`y_max` del canal, con un 5 % de aire. Si
  `y_max == y_min`, ancho 1 para no dividir por cero.
- Ventana horizontal, igual que la app (`field_review_app.py:1136-1137`):
  hammer `[max(0, trigger−0.15), min(dur, trigger+0.65)]`, geo
  `[max(−trigger, −0.08), min(dur−trigger, 1.1)]`. El eje del **geo va relativo
  al trigger** (`t − trigger_s`), como en `:1102`.
- Trigger: sobre el hammer línea llena en `trigger_s`; sobre el geo línea
  **punteada** (`setLineDash`) en `0`.
- Nitidez: `canvas.width = clientWidth * devicePixelRatio` (idem height) y
  `ctx.scale(dpr, dpr)`. Redibujar en `resize` con los datos que ya están (**sin
  refetch**).
- `max_points` que se pide = `Math.min(20000, Math.round(clientWidth * dpr))`.
  Un bucket por píxel físico: pedir más es tirar bytes.
- Colores: los de `_plot_colors` (§3) leyendo el tema actual
  (`document.documentElement.dataset.theme` + `matchMedia('(prefers-color-scheme: dark)')`,
  igual que `theme.js`). Los colores de traza sí van literales en el JS: son
  datos del gráfico, no chrome de la página.

### 5.3 Lo que el polling NO tiene que hacer

`capturas.js` refresca cada 3 s (`:62`). El visor **no** entra en ese ciclo:
`/api/signal` se pide sólo al elegir una captura, al cambiar `kind`, al tocar el
flip, o al apretar `recargar`. Pedir ~100 kB y 1.2 s de `discover_dataset` cada
3 s por tiempo indefinido es un bug de rendimiento servido en bandeja.

Aparte: cancelá el fetch en vuelo (`AbortController`) si el usuario clickea otra
captura, y devolvé el `destroy()` que limpia listeners — `main.js:22-25` llama al
retorno de `mount()` al cambiar de tab, y hoy `capturas.js:63` ya devuelve el
`clearInterval`.

---

## 6. Criterio de aceptación

### 6.1 Gate (es el criterio del ítem)

```
cd "C:\Github\Tesis\src\interfaces\python" && python "C:\Github\Tesis\src\interfaces\python\server\smoke_test.py" --only base --only capturas.signal --require capturas.signal --json "C:\Github\Tesis\scripts\autonomia\state\gate\capturas_signal.json"
```

Tiene que salir `0` con **todos** los checks en PASS. Y además, para no romper lo
anterior:

```
python "C:\Github\Tesis\src\interfaces\python\server\smoke_test.py" --only refactor --only tabs
```

### 6.2 Demostrar que los checks pueden fallar (regla 11 — hacelo de verdad)

1. Backup de `signal_view.py`.
2. Cambiá `decimate_minmax` por un salteado (`x[::stride]` para los dos arrays)
   → `capturas.signal.decimado_conserva_picos` **FAIL** (los picos ya no
   coinciden con la serie cruda).
3. Restaurá. Poné `apply_invert=False` en la carga del hammer →
   `capturas.signal.polaridad_fija` **FAIL**.
4. Restaurá. Sacá la conversión de no-finitos a `null` →
   `capturas.signal.nan_a_null` **FAIL** (y `sin_nan_en_json` también).
5. Restaurá, borrá los `.bak`, y mostrá con `git status --porcelain` que no quedó
   ninguna mutación colgada (el `.bak` tampoco tiene que aparecer).

### 6.3 A mano (el gate no ejecuta JS, y está bien que no finja que sí)

`cd src/interfaces/python && python -m server --port 8000`, abrir
`http://127.0.0.1:8000`:

- botón `ver` en una captura de `Canchiga` → se dibujan las dos trazas;
- el **martillo apunta para abajo** en el golpe (convención: hammer invertido) y
  la línea del trigger cae justo en el flanco;
- el geo arranca en `t = 0` en el trigger;
- `filt` cambia la traza; "Invertir geo" la espeja;
- cambiar de tema redibuja con los colores del tema (no queda una traza
  invisible sobre el fondo);
- las 9 capturas de `Canchita` muestran `—` con su explicación, no un botón roto.

---

## 7. Checks a agregar al gate

Todos con `@check("capturas.signal.<nombre>", "<qué prueba>", mode=...)` en
`smoke_test.py`. El registro se descubre solo (`:136-140`): no toques `main()`.

Dos helpers locales (no checks):

```python
def _first_shot(ctx: Ctx) -> tuple[str, dict]:
    """Primer (shot_id, captura) del dataset real que se pueda dibujar.

    Filtra por pick.shot_id y NO por pickable: son distintos (ver el spec §5.1).
    """
    data = ctx.json_get("/api/dataset")
    for folder in data.get("folders", []):
        for cap in folder.get("captures", []):
            pick = cap.get("pick") or {}
            if pick.get("shot_id"):
                return pick["shot_id"], cap
    raise AssertionError("ninguna captura de /api/dataset trae pick.shot_id: "
                         "sin eso la web no puede dibujar nada")


def _write_fixture(ctx: Ctx, folder: str, *, spike: float, with_nan: bool) -> str:
    """Escribe una captura sintética en el raw_root del SANDBOX y devuelve su shot_id.

    Cinturón de seguridad: nunca contra el dataset real (regla 2 del prompt).
    """
    assert ctx.sandbox and "smoke_sandbox" in str(ctx.raw_root), \
        f"_write_fixture sólo va en sandbox; raw_root={ctx.raw_root}"
    ...
```

El fixture, con el layout que realmente lee `frd`
(verificado contra `data/raw/Canchiga/captures/023_actual/metadata.json`):

```
<raw_root>/<folder>/captures/001_smoke/metadata.json
<raw_root>/<folder>/captures/001_smoke/hammer_s1/raw_f32le.bin
<raw_root>/<folder>/captures/001_smoke/geo1_s2/raw_f32le.bin
```

`metadata.json` mínimo que hace que `_discover_channels`
(`field_review_data.py:1641`) y `scan_catalog` (`catalog.py:100`) lo vean:

```json
{"order": 1, "fs": 1000,
 "nodes": [
   {"index": 1, "pcb_id": "S1", "role": "hammer", "type": "Hammer", "fs": 1000,
    "data_dir": "captures/001_smoke/hammer_s1",
    "raw_file": "captures/001_smoke/hammer_s1/raw_f32le.bin"},
   {"index": 2, "pcb_id": "S2", "role": "geo", "type": "Geo", "fs": 1000,
    "position_m": 4.0, "data_dir": "captures/001_smoke/geo1_s2",
    "raw_file": "captures/001_smoke/geo1_s2/raw_f32le.bin"}]}
```

Señal: 4000 muestras `float32` little-endian de ceros, con un pico
**positivo** `+spike` en la muestra 1000 (y unas 5 muestras alrededor, para que
`detect_hammer_trigger` lo tome) en **los dos** canales. `with_nan=True` mete
además `np.nan` en 3 muestras del geo, lejos del pico.

Tres avisos sobre el fixture, los tres son bugs si los ignorás:

- **Cada fixture tiene que tener contenido distinto** (variá `spike`): si dos
  carpetas quedan byte-idénticas, `discover_dataset` las marca duplicadas
  (`field_review_data.py:200-217`) y la segunda **no tiene shot**.
- Escribí sólo con `ctx.raw_root` del sandbox. El sandbox es un
  `tempfile.mkdtemp(prefix="smoke_sandbox_")` (`smoke_test.py:597`) y el
  `stop()` lo borra (`:497`).
- **No uses `/ingest` para meter el fixture.** Ver §8.1: el pipeline correría
  `auto_pick_shot` + `save_annotations` y eso escribe en
  `data/processed/raw/field_review_annotations.json`, que es el archivo de picks
  **del dataset real**. Escribir los archivos directo evita todo eso.

| # | id | modo | qué asserta | cómo se lo hace fallar |
|---|---|---|---|---|
| 1 | `capturas.signal.contrato` | read | `GET /api/signal?shot_id=…&max_points=500` → 200 y trae `shot_id, folder, capture, fs, kind, max_points, trigger_s, trigger_source, geo_flip, channels`; `channels` tiene `hammer` y `geo`; cada canal trae `role, pcb_id, file, used_filtered, invert_applied, flip_applied, samples, duration_s, stride, buckets, bucket_dt, decimated, y_min, y_max, min, max`; `fs > 0`, `samples > 0`, `len(min) == len(max) == buckets`, `buckets <= 500`, `decimated is True`, `bucket_dt > 0`, `file` relativo (sin `:` ni `\\`) | sacar una clave; mandar `t` en vez de `bucket_dt`; devolver `min` y `max` de largos distintos |
| 2 | `capturas.signal.decimado_conserva_picos` | read | Dos pedidos del mismo shot: `max_points=500` (decimado) y `max_points=100000` (crudo, `stride == 1`, `decimated is False`, `min == max` elemento a elemento). Para cada canal: `max(max_decimado) == max(max_crudo)` y `min(min_decimado) == min(min_crudo)` con `rel_tol=1e-5`. Además `buckets_decimado <= 500 < samples` y el **cuerpo** del decimado pesa < 60 kB | promediar por bucket, o saltear (`x[::stride]`): los extremos se achican y falla el primer assert |
| 3 | `capturas.signal.max_points_clamp` | read | `max_points=1` → 200 y `buckets >= 100`; `max_points=10**9` → 200 y `buckets <= 20000`; `max_points=abc` → 422 (**no** 500) | no clampear (un `reshape` con `stride` 0 explota en 500), o contestar 400 al 1 |
| 4 | `capturas.signal.sin_nan_en_json` | read | En el cuerpo crudo: `b"NaN" not in body`, `b"Infinity" not in body`; y `json.loads(body, parse_constant=...)` que **levanta** si aparece una constante no-JSON | devolver los `float(np.nan)` tal cual: `json.dumps` escribe `NaN` y `JSON.parse` del navegador tira `SyntaxError` |
| 5 | `capturas.signal.kind_filt` | read | `kind=filt` → 200, `used_filtered is True` en los dos canales y `file` termina en `filt_f32le.bin`; `kind=raw` → `used_filtered is False` y termina en `raw_f32le.bin`; `kind=xxx` → 400 | ignorar `kind` y devolver siempre el raw |
| 6 | `capturas.signal.shot_desconocido` | read | `shot_id=0000000000000000` → **404**; `shot_id` vacío → 400 o 422, nunca 200 ni 500 | dejar que el `next(...)` tire `StopIteration` → 500 |
| 7 | `capturas.signal.trigger_marcado` | read | `trigger_s` finito y `0 <= trigger_s <= duration_s` del hammer; `trigger_source in {"annotation","auto"}`; si `/api/dataset` traía `pick.trigger_s` no nulo → coinciden (`abs(dif) < 1e-9`) y `trigger_source == "annotation"`; si era nulo → `"auto"` | devolver `trigger_s: 0.0` fijo, o inventar el trigger en vez de usar `auto_pick_shot` / la anotación |
| 8 | `capturas.signal.no_bloquea` | read | 3 `GET /api/signal` en paralelo (`ThreadPoolExecutor`) y, mientras corren, `GET /health` en **< 2 s** y `GET /api/jobs` en < 2 s; los 3 terminan 200 | `async def` con numpy/`discover_dataset` adentro: el event loop queda tomado ~3.6 s y `/health` se encola detrás |
| 9 | `capturas.signal.ui_usa_endpoint` | read | `GET /static/js/tabs/capturas_signal.js` → 200 y contiene `/api/signal`, `max_points`, `geo_flip`; `GET /static/js/plot.js` contiene `export function drawMinMax`; `GET /static/js/tabs/capturas.js` contiene `capturas_signal.js` y `pick.shot_id` (o `shot_id`) | hacer el endpoint y no dibujar nada; o dejar el visor sin enganchar a la tabla |
| 10 | `capturas.signal.polaridad_fija` | sandbox | Fixture con pico **+1.0** en los dos canales. En la respuesta: hammer `min(min) <= -0.9` y `max(max) <= 0.1` (**quedó invertido**); geo `max(max) >= 0.9` y `min(min) >= -0.1` (**no** invertido); `channels.hammer.invert_applied is True`, `channels.geo.invert_applied is False`, `flip_applied is False` en los dos | `apply_invert=False`; invertir el geo; invertir los dos |
| 11 | `capturas.signal.nan_a_null` | sandbox | Fixture con NaN en el geo y `max_points` alto (`stride == 1`): el cuerpo no tiene `b"NaN"`, y `channels.geo.min` tiene **al menos un** `null`, y los buckets con dato siguen siendo números | convertir NaN a `0.0` (miente: dibuja una muestra que no existe) o dejarlo pasar como `NaN` |
| 12 | `capturas.signal.geo_flip_override` | sandbox | Mismo fixture que #10: sin `geo_flip` → `geo.max(max) >= 0.9`, `flip_applied is False`; con `geo_flip=1` → `geo.min(min) <= -0.9`, `max(max) <= 0.1`, `flip_applied is True`; y el **hammer no cambia** entre las dos respuestas | aplicar el flip al hammer también, o ignorar el query param |

Notas de implementación de los checks:

- Los mensajes de `assert` tienen que decir **qué** falló y **con qué números**
  (el estándar está en `smoke_test.py:161-164`): el que lee el log del gate no
  debería tener que abrir el código.
- Los checks 10-12 comparten el fixture: escribilo una vez por carpeta y reusá
  (`Canchiga` no, obviamente: nombres tipo `smoke_polaridad` y `smoke_nan`).
- **No** agregues un check de "el click dibuja": el gate habla HTTP y no ejecuta
  JS. #9 es estructural y se declara como tal; el resto es validación humana
  (§6.3). Fingir cobertura de comportamiento es peor que declarar el hueco.
- **Cobertura que este ítem NO tiene** (dejalo escrito, no lo tapes): que el
  `geo_flip` **de la anotación** se aplique. Se prueba el override por query,
  no el camino que lee `load_annotations`, porque para eso habría que escribir
  anotaciones y hoy eso es peligroso (§8.1). Lo cubre el ítem de `POST /api/pick`.

---

## 8. Trampas del §5 del plan que aplican acá

### 8.1 (nueva, y es la peor) El sandbox del gate **no** está aislado de las anotaciones reales

`frd._procesados_dir_for` (`field_review_data.py:63-69`) resuelve la carpeta de
salida por **`raw_root.name`**, no por la ruta completa. El sandbox del gate crea
su raw en `<tmp>/raw` (`smoke_test.py:597-599`), o sea `name == "raw"`… igual que
el `data/raw` real. Resultado:
`default_annotations_path(<tmp>/raw)` y `default_annotations_path(data/raw)`
apuntan **al mismo archivo**: `C:\Github\Tesis\data\processed\raw\field_review_annotations.json`.

Hoy no hace daño (`reviewed_count == 0` y este ítem no escribe). Pero si el gate
ingesta un ZIP con par hammer+geo, `Pipeline._process` (`pipeline.py:290-311`)
corre `auto_pick_shot` y **sobrescribe ese archivo** con los shots del dataset
temporal: se pierden todos los picks validados a mano del dataset real, sin
aviso. Es exactamente lo que la regla 2 del prompt y el §0.3 del plan prohíben.

Por eso este ítem: (a) es sólo lectura, (b) mete el fixture escribiendo archivos
en el raw del sandbox en vez de por `/ingest`. **No lo "optimices" usando
`/ingest`.**

El arreglo, para el ítem que escriba anotaciones: pasarle al servidor del
sandbox `TESIS_DATA_ROOT=<tmp>` en el `env` del `subprocess.Popen`
(`smoke_test.py:516`). `frd._discover_data_root` (`field_review_data.py:30-42`)
respeta esa variable, así que **todo** `data/processed` del sandbox cae en el
temporal. En modo `read` **no** se toca (ahí queremos ver las anotaciones
reales). Queda anotado en `DUDAS_LUNES.md`.

### 8.2 §5.1 — el proceso viejo no toma los cambios

La que más muerde. `.html/.css/.js` se sirven de disco y se recargan solos, pero
**el navegador cachea módulos ES**: si editaste `plot.js` y no ves el cambio,
`Ctrl+F5` antes de sospechar del código. Y todo lo que toques en Python
(`signal_view.py`, `routers/dataset.py`) **exige reiniciar el servidor**: no hay
`--reload`. Si un check falla con un mensaje que no tiene sentido, verificá
primero que no quedó un `python -m server` viejo escuchando (matá **el PID
exacto** que arrancaste vos, nunca por nombre — regla 9).

### 8.3 §5.5 — `discover_dataset` descarta capturas

Es el fundamento de todo §5.1 de este spec. `/api/signal` **necesita**
`discover_dataset` (el `shot_id` y el par hammer/geo salen de ahí), pero la
tabla que decide qué se puede dibujar es la del **catálogo**, y las dos no
coinciden: 210 capturas catalogadas, 194 dibujables. La regla es simple: catálogo
para listar, `shot_id` para dibujar, y cuando no hay `shot_id` **se dice por qué**
en vez de esconder la fila.

### 8.4 §5.4 — sin martillo no hay picking

`detect_hammer_trigger` mide el flanco **en la señal del martillo**. Sin hammer
no hay `trigger_s`, y sin `shot_id` no hay endpoint. No inventes un trigger para
esas capturas (ni `0.0`, que parece un dato): no tienen. Es geofísica, no un bug.

### 8.5 §5.2 — CORS

No toques el bloque de middlewares de `api.py:69-89`. Lo aclaro porque el visor
tienta a agregar headers (`Content-Encoding`, cache del JSON): cualquier
`add_middleware` nuevo queda **más externo** que `_TitleCaseHeaders` y
`base.cors_preflight` empieza a fallar por algo que no tiene nada que ver con lo
que estabas haciendo. Si querés comprimir, es `gzip` del cliente, no un
middleware.

### 8.6 §5.6 — Windows/OneDrive

Todo lo que escribe este ítem son `.py`/`.js`/`.css` dentro de `server/`. **Nada**
dentro de `C:\Github\Tesis\data` (regla 2): los fixtures del gate van al
temporal del sandbox. Y las rutas del payload van relativas con `/`
(`catalog.py:115`): un `C:\...` en el JSON filtra el disco del servidor a la web.

---

## 9. Fuera de alcance (no lo hagas aunque tiente)

- `POST /api/pick`, arrastrar el marcador, `frd.save_annotations`, `reviewed`,
  `accepted`, persistir `geo_flip`. **Es el ítem siguiente**, y necesita §8.1
  resuelto primero.
- El pasa-banda de §3.2 (`frd.apply_bandpass_filter`). `kind=filt` acá es el
  archivo que ya grabó el nodo, nada más.
- Cachear `discover_dataset` (§4.5), PNG server-side (eso es §3.4), zoom/pan
  interactivo, atajos de teclado de la app (`field_review_app.py:1515-1524`),
  overlays de promedios (`_plot_ok_average`, `_plot_folder_average`), y la zona
  de búsqueda auto (`search_window_s`).
- Rediseñar el CSS o cambiar la tabla de `renderDataset` más allá de la columna
  nueva.
