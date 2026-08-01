SPEC_READY

# refactor — §1 Refactor a FastAPI + estáticos

Objetivo: reemplazar `http.server` por FastAPI + uvicorn con la estructura de
PORT_PLAN §1 (`api.py`, `routers/`, `static/`), **sin perder ni una sola de las
funciones que hoy andan**. Los routers `picks.py` y `masw.py` quedan como
esqueletos (router vacío, sin rutas) — eso es lo esperado en este ítem.

Regla mental para todo el ítem: *esto es una mudanza, no un rediseño*. Ninguna
ruta cambia de path, ni de método, ni de forma de respuesta, ni de códigos de
error. Cualquier "mejora" de API acá es una regresión encubierta: la SPA del
ESP32 (`src/firmware/esp32/Nodo comunicación/master/data/js/app.js`) ya postea
contra `/ingest` y está flasheada en el campo.

FastAPI 0.140.0 y uvicorn 0.51.0 ya están instalados (verificado). No agregar
dependencias.

---

## 1. Archivos a crear / editar (rutas absolutas)

### Crear

| Ruta | Contenido |
|---|---|
| `C:\Github\Tesis\src\interfaces\python\server\api.py` | `create_app(pipeline) -> FastAPI`: CORS, montaje de estáticos, `include_router` de los 5 routers, `app.state.pipeline`, dependencia `get_pipeline`. |
| `C:\Github\Tesis\src\interfaces\python\server\routers\__init__.py` | vacío (paquete). |
| `C:\Github\Tesis\src\interfaces\python\server\routers\ingest.py` | `POST /ingest` (port literal de `app.py:322` `_ingest`). |
| `C:\Github\Tesis\src\interfaces\python\server\routers\dataset.py` | `GET /api/dataset`, `GET /api/jobs`, `GET /health` + la función `dataset_summary()` (mudanza de `app.py:35`). |
| `C:\Github\Tesis\src\interfaces\python\server\routers\admin.py` | `POST /api/delete`, `POST /api/delete-sin-hammer`, `POST /api/requeue`. |
| `C:\Github\Tesis\src\interfaces\python\server\routers\picks.py` | esqueleto: `router = APIRouter()` y nada más. Docstring: "§3.1, todavía no". |
| `C:\Github\Tesis\src\interfaces\python\server\routers\masw.py` | ídem, para §3.5. |
| `C:\Github\Tesis\src\interfaces\python\server\static\index.html` | esqueleto con las tabs de §2; sin lógica adentro. |
| `C:\Github\Tesis\src\interfaces\python\server\static\css\app.css` | los estilos que hoy están en el `<style>` de `app.py:83-109`, más lo mínimo de tabs. |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\main.js` | router de tabs + estado global + el polling y el render que hoy están inline en `app.py:135-237`. |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\theme.js` | toggle claro/oscuro (`data-theme` en `:root` + `localStorage`). |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\plot.js` | módulo de dibujo reutilizable. En este ítem puede exportar sólo el andamio (p. ej. `export function drawSeries(canvas, series, opts)` con una implementación mínima de línea + ejes); §3.1 lo usa de verdad. **No puede ser un archivo vacío**: el gate pide que exista y tenga contenido. |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\tabs\capturas.js` | el dashboard actual (tabla de subidas + tabla de capturas). |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\tabs\borrado.js` | los dos botones de borrado que hoy viven en el index. |

### Editar

| Ruta | Qué |
|---|---|
| `C:\Github\Tesis\src\interfaces\python\server\app.py` | queda **sólo** con `main()` (argparse + construcción del `Pipeline` + `uvicorn.run`). Se borran `Handler`, `INDEX_HTML`, `MAX_UPLOAD`, `_dataset_summary` (migran a los routers). El docstring del módulo se actualiza: ya no es "sobre la biblioteca estándar a propósito". |
| `C:\Github\Tesis\src\interfaces\python\server\smoke_test.py` | agregar los checks `refactor.*` de la §4 de este spec. |

### No tocar

`pipeline.py`, `catalog.py`, `__init__.py`, `__main__.py`, y todo
`geophone_scope/`. Si aparece la necesidad de tocar `pipeline.py`, es señal de
que el port se está saliendo del ítem.

---

## 2. Cómo portar cada pieza (con el código a reusar)

El implementador no conoce el repo. Todo lo de abajo **ya existe**: hay que
llamarlo, no reescribirlo.

### 2.1 Arranque y flags — `app.py:362-392` (`main`)

`main()` se conserva casi tal cual. Lo único que cambia es el final:

* Se mantienen **exactamente** los mismos flags: `--port` (8000), `--host`
  (`0.0.0.0`), `--data-root`, `--raw-root`. El gate arranca con
  `python -m server --port N --raw-root R --data-root D` (`smoke_test.py:231`):
  si un flag cambia de nombre, el gate ni siquiera bootea y todo el ítem falla.
* Se mantiene el cálculo de defaults **idéntico**, incluyendo el comentario de
  `app.py:373` (`parents[4]` = raíz del superproyecto) y los `mkdir`. Ojo:
  `smoke_test.py:49` re-deriva `REPO` con el mismo `parents[4]` y lo dice en un
  comentario; si acá se mueve el archivo de lugar, se rompen los dos.
* Se conservan los tres `print` de arranque (`app.py:385-387`): el gate imprime
  el stdout del proceso cuando no bootea, y son lo único que se ve ahí.
* Reemplazo del final:

```python
pipeline = Pipeline(data_root, raw_root=raw_root)
app = create_app(pipeline)
uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
```

Pasar el **objeto** `app`, no el string `"server.api:app"`: con el string
uvicorn re-importa el módulo y construiría un `Pipeline` distinto (dos workers
sobre el mismo `jobs.json`). Por la misma razón, **no** definir un `app`
a nivel de módulo en `api.py`.

`KeyboardInterrupt` sigue atrapado como hoy. `__main__.py` y `__init__.py` no se
tocan: siguen importando `main` desde `.app`.

### 2.2 CORS — `app.py:246-253` (`_cors`)

Se reemplaza por `CORSMiddleware` con estos valores, que son los mismos que hoy
manda `_cors`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,          # ver trampa abajo
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Geo-Filename"],
    max_age=86400,
)
```

Tres trampas concretas acá, todas ya vistas o fáciles de pisar:

1. `allow_credentials=True` junto a `allow_origins=["*"]` hace que Starlette
   devuelva el origen **eco** en vez de `*`. `base.cors_preflight`
   (`smoke_test.py:173`) asserta `== "*"` y falla. Dejarlo en `False`.
2. `CORSMiddleware` sólo agrega las cabeceras cuando el request trae `Origin`.
   El handler viejo las mandaba siempre (`app.py:260`). Eso es aceptable —el
   navegador siempre manda `Origin` en cross-origin— pero el check
   `refactor.cors_en_post` manda `Origin` explícito justamente para verificarlo.
3. `X-Geo-Filename` es un header **no safelisted**: si falta en `allow_headers`,
   el preflight del POST real de la SPA falla aunque el gate pase. Va sí o sí.

### 2.3 `POST /ingest` — `app.py:322-356` (`_ingest`)

Port literal, misma semántica y mismos códigos:

| Condición | Código | Cuerpo (text/plain) |
|---|---|---|
| `Content-Length` no entero | 400 | `Content-Length inválido\n` |
| `length <= 0` | 400 | `cuerpo vacío\n` |
| `length > MAX_UPLOAD` (256 MiB, `app.py:32`) | 413 | `demasiado grande: {length} B\n` |
| bytes leídos ≠ `length` | 500 | `recibido incompleto: {n}/{length} B\n` |
| no empieza con `PK` | 415 | `no parece un ZIP\n` |
| ok | 200 | `OK {job_id} encolado ({n} B)\n` |

Forma sugerida:

```python
@router.post("/ingest")
async def ingest(request: Request, pipeline: Pipeline = Depends(get_pipeline)):
    body = await request.body()
    ...validaciones...
    name = (request.headers.get("X-Geo-Filename") or "captura.zip").strip()
    job = await run_in_threadpool(pipeline.submit_zip, body, name)
    print(f"[ingest] {request.client.host} -> {job.job_id} ({len(body)} B) encolado", flush=True)
    return PlainTextResponse(f"OK {job.job_id} encolado ({len(body)} B)\n")
```

* `pipeline.submit_zip` está en `pipeline.py:157`: guarda el ZIP, crea el `Job`,
  persiste y encola. **Devuelve enseguida** — ya cumple "responder antes de
  preprocesar"; no hay que agregar `BackgroundTasks` ni nada.
* Igual va envuelto en `run_in_threadpool` (`starlette.concurrency`) porque
  escribe hasta 256 MB a disco y eso sí bloquearía el event loop.
* El `print` de `app.py:352` se conserva: es el único rastro de una ingesta en
  la consola del campo. `request.client` puede ser `None` — usar
  `request.client.host if request.client else "?"`.
* **No** validar el ZIP ni tocar `Pipeline`: el worker de `pipeline.py:243`
  (`_run`) sigue siendo un hilo daemon propio, creado en `Pipeline.__init__`
  (`pipeline.py:103`). No moverlo a `asyncio`, no llamar a `_process` desde una
  ruta: `frd.auto_pick_shot` (`field_review_data.py:348`) carga señales enteras.

### 2.4 Rutas de lectura — `routers/dataset.py`

* `GET /health` → `PlainTextResponse("ok\n")`, 200. Es lo que sondea
  `start_server` (`smoke_test.py:242`) para decidir que el servidor arrancó.
* `GET /api/jobs` → `{"jobs": pipeline.jobs()}`. `Pipeline.jobs` está en
  `pipeline.py:145` y ya devuelve dicts ordenados por fecha. No re-serializar.
* `GET /api/dataset` → mudanza tal cual de `_dataset_summary` (`app.py:35-77`).
  **Copiar la función completa, comentarios incluidos**, sólo cambiándole el
  nombre a `dataset_summary`. Usa:
  * `scan_catalog` — `catalog.py:82`
  * `frd.discover_dataset` — `field_review_data.py:184`
  * `frd.load_annotations` — `field_review_data.py:394`
  * `frd.default_annotations_path` — `field_review_data.py:1577`
  * el `except FileNotFoundError: pass` de `app.py:68` (dataset vacío en
    sandbox). Sin eso, el modo `sandbox` del gate revienta.

  Las claves del JSON son contrato: `raw_root`, `folders`, `capture_count`,
  `node_count`, `shot_count`, `reviewed_count`, y por captura `capture`,
  `order`, `fs`, `nodes`, `has_hammer`, `has_geo`, `pickable`, `pick`.
  `base.dataset_completo` y `base.dataset_no_descarta` (`smoke_test.py:134,146`)
  leen varias de esas y `refactor.contrato_dataset` las verifica todas.

**Estas dos rutas se definen con `def`, no `async def`.** `scan_catalog` +
`discover_dataset` sobre 210 capturas hacen I/O de disco por segundos; una
corrutina bloquearía el event loop y colgaría `/health` y `/ingest` al mismo
tiempo. Con `def`, Starlette las corre en el threadpool solo. Es la misma razón
por la que el worker vive en un hilo (§1 del plan).

### 2.5 Rutas de escritura — `routers/admin.py`

Port literal de `app.py:296-318`, **manteniendo los query params** (la forma
`?folder=&zip=1`, no un body JSON):

* `POST /api/delete?folder=<name>&zip=0|1` → `pipeline.delete_folder(folder,
  with_zip=...)` (`pipeline.py:192`). Devuelve el dict tal cual, con status 200
  si `res["ok"]` y **400 si no** (`app.py:303`). Con FastAPI: `JSONResponse(res,
  status_code=200 if res.get("ok") else 400)`.
* `POST /api/delete-sin-hammer?zip=0|1` → itera
  `folders_without_hammer(pipeline.raw_root)` (`catalog.py:67`) llamando a
  `delete_folder`, y responde `{"ok": True, "deleted": [...], "errors": [...]}`.
* `POST /api/requeue?job_id=<id>` → `pipeline.requeue(job_id)`
  (`pipeline.py:178`); 200 `reencolado\n` / 404 `no existe\n`, **texto plano**,
  como `app.py:318`.
* Las tres son `def` sync (borran archivos, tocan disco).
* `delete_folder` ya trae la validación de path traversal (`pipeline.py:201-206`)
  y la política de conservar el ZIP y marcar el job como `borrado` en vez de
  eliminarlo (`pipeline.py:219-226`). **No duplicar ni relajar eso**: es la regla
  dura 7 / §0.3 del plan.

### 2.6 Inyección del Pipeline

```python
def create_app(pipeline: Pipeline) -> FastAPI:
    app = FastAPI(title="Servidor de datos Geophone", version="1")
    app.state.pipeline = pipeline
    ...
def get_pipeline(request: Request) -> Pipeline:
    return request.app.state.pipeline
```

`get_pipeline` vive en `api.py` y los routers lo importan. Nada de globals ni de
atributos de clase como el `Handler.pipeline` de hoy (`app.py:243`).

**Dejar `/openapi.json` y `/docs` habilitados** (o sea: no pasar
`openapi_url=None`). `refactor.stack_fastapi` los usa como prueba de que el
servidor ya no es `http.server`.

### 2.7 Estáticos

```python
STATIC = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=STATIC), name="static")

@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html", headers={"Cache-Control": "no-store"})
```

* Montar en `/static`, **no en `/`**. Un `app.mount("/", StaticFiles(...))`
  captura todo lo que se registre después y es una fuente clásica de 404
  fantasma en las rutas `/api/*`.
* `/index.html` se mantiene porque el handler viejo lo aceptaba (`app.py:281`).
* `Cache-Control: no-store` en `/` y en las respuestas `/api/*` — hoy lo pone
  `_send` (`app.py:259`) para todo. Sin eso, el navegador del campo muestra un
  dataset viejo y parece que el servidor no ingesta. Ponerlo con un middleware
  chico o header por ruta, a gusto.

### 2.8 El front

`index.html` es **esqueleto**: markup de tabs, `<link rel="stylesheet"
href="/static/css/app.css">` y `<script type="module" src="/static/js/main.js">`.
Cero `<style>`, cero `<script>` inline, cero `fetch(`. Todo el JS que hoy está
entre `app.py:135` y `app.py:237` se muda a los módulos.

Tabs (nombres **literales**, de PORT_PLAN §2):

`Capturas` · `Filtros` · `Agrupamiento` · `Enfase` · `Promedios / arrivals` ·
`Waterfall` · `MASW` · `Borrado`

Sólo `Capturas` y `Borrado` tienen contenido en este ítem; las demás muestran un
placeholder honesto ("pendiente de porteo", no una pantalla en blanco).

Paridad funcional obligatoria (es lo que hoy anda y no se puede perder):

* Tab `Capturas`: tabla de Subidas (`renderJobs`, `app.py:151`) + tabla de
  capturas por carpeta (`renderDataset`, `app.py:172`), con el badge de conteos,
  el `🔨/📈` por rol, el estado `completa` / `sin martillo` / `sin geófono`, el
  trigger y el `validado`. Polling cada 3 s (`app.py:236`), y el `catch` que
  **no borra lo ya dibujado** cuando falla el fetch (`app.py:146`) — en el campo
  la conexión se cae y no se quiere una pantalla vacía.
* Tab `Borrado`: el botón por carpeta (`borrarCarpeta`, `app.py:216`) y el de
  "Borrar las capturas sin martillo" (`app.py:223`), con los mismos `confirm()`
  que **listan qué se va a borrar** y aclaran que el ZIP se conserva.
* Los `fetch` pasan a rutas absolutas (`/api/jobs`, `/api/dataset`, …): hoy son
  relativas y con el index servido desde `/` seguirían andando, pero absolutas
  es lo correcto.

`theme.js`: `document.documentElement.dataset.theme = 'light'|'dark'`,
persistido en `localStorage`, con `matchMedia('(prefers-color-scheme: dark)')`
como valor inicial, y un botón que alterna. El patrón está en
`src\firmware\esp32\Nodo comunicación\master\data\js\app.js:2387-2421`
(`applyTheme` / `initTheme` / el listener de `btn-theme`). Ojo: ahí el toggle es
`body.classList.toggle('light')`; el plan pide `data-theme` en `:root`, así que
se copia la **estructura** (leer `localStorage` → aplicar → persistir en el
click, con `try/catch` porque `localStorage` puede estar deshabilitado), no la
línea. El CSS usa `:root[data-theme="dark"] { … }` y `prefers-color-scheme` sólo
como default cuando no hay atributo.

---

## 3. Criterio de aceptación observable

1. `cd C:\Github\Tesis\src\interfaces\python && python -m server --port 8000`
   arranca, imprime las mismas 3 líneas y sirve la web en `http://127.0.0.1:8000`.
2. Los 6 checks `base.*` siguen pasando **sin editarlos**. Si alguno hubo que
   tocarlo para que pase, el refactor rompió un contrato: revertir, no editar el
   check.
3. `GET /` devuelve un HTML que carga CSS y JS desde `/static/`, y en el
   navegador se ve lo mismo que hoy (subidas + capturas + los dos borrados),
   ahora dentro de tabs.
4. `POST /ingest` de un ZIP real sigue devolviendo `OK <job_id> encolado` en
   menos de un segundo y la carpeta aparece en `/api/dataset` cuando el worker
   termina.
5. Gate verde:
   ```
   cd "C:\Github\Tesis\src\interfaces\python" && python "C:\Github\Tesis\src\interfaces\python\server\smoke_test.py" --only base --only refactor --require refactor --json "C:\Github\Tesis\scripts\autonomia\state\gate\refactor.json"
   ```

---

## 4. Checks a agregar al gate

Van en `C:\Github\Tesis\src\interfaces\python\server\smoke_test.py`, con el
decorador `@check(...)` (`smoke_test.py:113`). Usar `ctx.get` / `ctx.post` /
`ctx.json_get` (`smoke_test.py:66-99`); no importar nada de `server.*` — el gate
habla sólo HTTP a propósito (`smoke_test.py` docstring, punto 1).

Siete de los ocho **fallan contra el `app.py` actual** (probalo si dudás: son
checks de verdad, no adornos). El octavo, `refactor.contrato_dataset`, pasa hoy
a propósito: es el que detecta que el port perdió una clave del JSON, o sea que
sólo puede fallar *después* de romper algo.

| id | modo | qué asserta | por qué falla hoy |
|---|---|---|---|
| `refactor.stack_fastapi` | read | `GET /openapi.json` → 200, JSON con `"paths"`, y ese dict contiene `/ingest` y `/api/dataset` | `http.server` devuelve 404 |
| `refactor.estaticos` | read | `GET /static/css/app.css` → 200, `len > 200`; `/static/js/main.js`, `/static/js/theme.js`, `/static/js/plot.js` → 200 y `len > 100` cada uno; el content-type de `app.css` contiene `css` | hoy no existe `/static` |
| `refactor.index_sin_logica` | read | `GET /` → 200 y el cuerpo decodificado **contiene** `/static/js/main.js` y `/static/css/app.css`, y **no contiene** `fetch(` ni `setInterval(` ni `<style` | hoy todo eso está inline |
| `refactor.tabs_presentes` | read | el cuerpo de `GET /` contiene los 8 nombres literales: `Capturas`, `Filtros`, `Agrupamiento`, `Enfase`, `Promedios / arrivals`, `Waterfall`, `MASW`, `Borrado` | hoy sólo existe "Capturas" |
| `refactor.contrato_dataset` | read | `GET /api/dataset` trae las 6 claves de nivel raíz; alguna carpeta con capturas; y la primera captura trae `capture`, `nodes`, `has_hammer`, `has_geo`, `pickable` y la clave `pick` presente (puede ser `null`) | pasa hoy — **por eso el assert de raw_root de abajo va en el mismo check o en `refactor.raw_root_del_flag`** |
| `refactor.raw_root_del_flag` | read | `Path(json["raw_root"]).resolve() == ctx.raw_root.resolve()` | prueba que `--raw-root` se respeta post-refactor (trampa §5.1). Comparar con `Path(...).resolve()`, no strings: en Windows difieren por mayúsculas y separadores |
| `refactor.cors_en_post` | sandbox | POST a `/ingest` de un ZIP mínimo **con header `Origin: http://192.168.4.1`** → status 200/202 y la **respuesta** trae `Access-Control-Allow-Origin: *` | detecta el `allow_credentials=True` que hace eco del origen, y el caso "CORS sólo en el preflight" |
| `refactor.worker_no_bloquea` | sandbox | postear 3 ZIPs mínimos seguidos; inmediatamente después, `GET /health` y `GET /api/jobs`; assert que ambos vuelven en `< 2.0 s` y que `/api/jobs` lista ≥ 3 trabajos | falla si alguien mueve el procesado al event loop o al request |

Detalles para que no se peleen con la infraestructura del gate:

* Los ZIPs de prueba se arman en memoria como en `_ingest_rapido`
  (`smoke_test.py:186-193`): `zipfile.ZipFile(io.BytesIO(), "w")` +
  `zf.writestr("smoke/README.txt", ...)`. **Nunca** un archivo de `data/`.
* Todo lo que postea va en `mode="sandbox"`: en ese modo el gate levanta un
  servidor con `raw_root` y `data_root` temporales (`smoke_test.py:296-299`) y
  los borra al final. Un check que escriba en modo `read` estaría escribiendo
  sobre `data/raw` real → regla dura 2.
* `refactor.contrato_dataset` y `refactor.raw_root_del_flag` van en `read`:
  necesitan el dataset real.
* No cambiar `MIN_CAPTURES` / `MIN_NODES` (`smoke_test.py:55`) ni ningún check
  `base.*`.

---

## 5. Trampas del §5 del plan que aplican acá

1. **§5.1 — el proceso viejo no toma los cambios.** Después de refactorizar hay
   que matar cualquier `python -m server` que haya quedado corriendo antes de
   probar; si no, se prueba el binario viejo y el resultado no significa nada.
   El gate arranca su propio proceso en un puerto libre
   (`smoke_test.py:200-248`), así que ahí no aplica — aplica a las pruebas a
   mano.
2. **§5.2 — CORS.** Es la trampa central del ítem. El síntoma es "servidor
   inalcanzable" en la SPA y el error real sólo aparece en la consola del
   navegador. Ver §2.2: `allow_credentials=False` y `X-Geo-Filename` en
   `allow_headers`.
3. **§5.5 — `discover_dataset` descarta capturas sin par hammer+geo.** El
   catálogo lo hace `scan_catalog` (`catalog.py:82`) y los picks se superponen
   encima. Al mudar `_dataset_summary` **no** invertir ese orden ni "simplificar"
   usando sólo `discover_dataset`: el catálogo pasaría de 210 capturas a las que
   tengan martillo, y `base.dataset_completo` lo caza.
4. **§5.6 — Windows/OneDrive + LFS.** Todo lo que escriba el gate va a
   `tempfile.mkdtemp`. No escribir en `C:\Github\Tesis\data` bajo ningún
   concepto, ni siquiera un archivo de prueba que después se borra.
5. **§0.3 — nada se borra solo.** El port de `/api/delete*` no puede agregar
   ningún borrado automático, ni "limpiar" carpetas incompletas al arrancar.
   El ZIP se conserva salvo `zip=1`.
6. **§0.4 — reusar, no reimplementar.** Si en algún momento aparece la
   necesidad de re-implementar el descubrimiento, el picking o el formato de
   anotaciones dentro de un router: está mal. Todo eso ya está en
   `field_review_data.py` y en `pipeline.py`.

---

## 6. Fuera de alcance (no hacerlo en este ítem)

* Cualquier endpoint de §3 (`/api/signal`, `/api/pick`, MASW). `picks.py` y
  `masw.py` quedan vacíos.
* La ventana de borrado de §4 con banderas y subgrupos. Acá sólo se mudan los
  dos botones que ya existen.
* Modelos Pydantic para las respuestas: las rutas devuelven los dicts tal cual
  para no alterar el contrato JSON. Tipar puede venir después, con el contrato
  ya cubierto por checks.
