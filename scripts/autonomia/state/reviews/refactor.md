VERDICT: PASS

Resumen para el commit: refactor(server): http.server -> FastAPI + estáticos, con las rutas, el CORS y el worker en hilo intactos (gate 15/15).

---

## Qué verifiqué (no por lo que diga nadie)

**Gate, corrido por mí dos veces: 15/15.**
`gate_20260725_005419.log` — los 6 `base.*` pasan **sin haber sido editados**
(`git status` no muestra `smoke_test.py` modificado; los checks `refactor.*` ya
estaban commiteados en `c62160f`).

**Los checks nuevos pueden fallar de verdad.** Los rompí a mano, uno por uno, con
backup y restauración:

| Mutación | Resultado |
|---|---|
| `allow_credentials=True` en `api.py` | FAIL `refactor.cors_en_post` **y** FAIL `base.cors_preflight` (`Access-Control-Allow-Origin='http://192.168.4.1'` — el eco del origen, exactamente la trampa que el spec anticipaba) |
| `cat.pop("node_count")` en `dataset_summary` | FAIL `refactor.contrato_dataset` (`falta la clave 'node_count'`) |
| `<style>` inline en `index.html` | FAIL `refactor.index_sin_logica` |
| `/api/jobs` pasado a `async def` con `time.sleep(3)` | FAIL `refactor.worker_no_bloquea` (`/api/jobs tardó 3.0s`) |

Todo restaurado: los md5 de `api.py`, `routers/dataset.py`, `routers/ingest.py`
e `index.html` vuelven a coincidir con los de antes de mutar, y
`git status --porcelain` queda igual que al empezar (` M server/app.py`,
`?? server/api.py`, `?? server/routers/`, `?? server/static/`). Ninguna mutación
colgada.

**Los requisitos de §1 sobrevivieron:**
- CORS en `/ingest`: `CORSMiddleware` con `allow_credentials=False`,
  `allow_headers=["Content-Type","X-Geo-Filename"]`, `max_age=86400`. Verificado
  en preflight y en la respuesta del POST real con `Origin`.
- Respuesta antes de preprocesar: `submit_zip` encola y vuelve;
  `base.ingest_responde_rapido` en 0.0 s.
- Worker en hilo aparte: `pipeline.py` intacto (no aparece en el diff), el POST
  va por `run_in_threadpool`, y `/api/dataset` y `/api/jobs` son `def` sync, así
  que Starlette las manda al threadpool.
- `python -m server --port N --raw-root R --data-root D`: el gate arranca así y
  el log del servidor muestra las 3 líneas de arranque intactas. Defaults sin
  tocar (`parents[4]`, `data/server`, `data/raw`).

**§0.4 reuso**: `dataset_summary` es la mudanza literal de `_dataset_summary`,
comentarios incluidos, con `scan_catalog` + `frd.discover_dataset` +
`frd.load_annotations` y el `except FileNotFoundError`. No hay ninguna fórmula
copiada ni `discover_dataset` usado solo (el orden catálogo→picks se respeta, §5.5).

**`C:\Github\Tesis\data`**: intacto. `git status --porcelain` en el repo de datos
sale vacío antes y después. Los sandbox del gate van a `tempfile.mkdtemp`.

**Código muerto / a medio portear**: no encontré. `app.py` queda sólo con
`main()`, sin `Handler`/`INDEX_HTML`/`MAX_UPLOAD` (migró a `ingest.py`) y con el
docstring actualizado. `picks.py` y `masw.py` son esqueletos declarados como
tales. `plot.js` tiene una implementación mínima real, no un stub vacío.
Las tabs sin portear dicen "pendiente de porteo", no muestran pantalla en blanco.

## Observaciones (no bloquean; para tener en cuenta en §3.1)

1. `api.py` agrega un middleware `_TitleCaseHeaders` que no estaba en el spec:
   re-castea los headers salientes a Title-Case porque el gate hace
   `dict(headers).get("Access-Control-Allow-Origin")` (case-sensitive) y
   Starlette emite todo en minúsculas. Es correcto por HTTP (RFC 7230), está
   documentado y era la alternativa a editar un check `base.*`, que está
   prohibido. Pero es código de producción con forma de dependencia del gate:
   si algún día se permite tocar `smoke_test.py`, conviene pasar el gate a
   lookup case-insensitive y borrar el middleware.
2. `refactor.worker_no_bloquea` es más flojo de lo que parece: no cronometra los
   POST, sólo el `/health` y el `/api/jobs` posteriores. Probé una mutación que
   bloquea el event loop 3 s por cada ingesta (el check tardó 9.1 s en vez de
   0.1 s) y **pasó igual**, porque el bloqueo se consume durante los POST. Sí
   caza el bloqueo persistente (mutación 4). Al agregar los endpoints de §3.1
   conviene sumarle un assert de duración sobre los propios POST.
3. Tab `Borrado`: sólo tiene el botón de "sin martillo"; el borrado por carpeta
   quedó en la tabla de `Capturas` (con un texto que lo aclara). El spec §2.8
   los pedía a los dos en `Borrado`. No es una pérdida de función —los dos
   botones existen y hacen lo mismo que hoy— pero queda pendiente para la
   ventana dedicada de §4.
4. `capturas.js` expone `window.borrarCarpeta` como global (lo pide el
   `onclick=` heredado del index viejo) y no la limpia al desmontar la tab.
   Cuando §3.1 reescriba esa tabla, conviene pasar a `addEventListener`.
5. Rutas inexistentes ahora devuelven el 404 JSON de FastAPI
   (`{"detail":"Not Found"}`) en vez de `no existe\n` en texto plano. Nadie
   consume eso —la SPA sólo postea `/ingest`— pero es el único cambio de forma
   de respuesta que encontré.
