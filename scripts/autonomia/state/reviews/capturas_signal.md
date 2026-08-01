VERDICT: PASS

Resumen para el commit: `GET /api/signal` con decimado min/max en el servidor
(`signal_view.py`) + visor de hammer/geo con el trigger marcado en la tab
Capturas; 12 checks `capturas.signal.*` nuevos, gate 19/19 y sin regresiones en
`refactor`/`tabs`.

---

## Qué verifiqué (revisor, no implementador)

### Gate, corrido por mí

```
python server/smoke_test.py --only base --only capturas.signal --require capturas.signal --json .../capturas_signal.json
→ [gate] 19/19 checks OK   (exit 0)

python server/smoke_test.py --only refactor --only tabs
→ [gate] 14/14 checks OK   (sin regresiones)
```

### Los checks PUEDEN fallar (regla 11 — los rompí yo, uno por uno)

No me creí los PASS: mutá el código, corrí el check, restauré. Los 6:

| Mutación | Check que la detectó | Mensaje real |
|---|---|---|
| `decimate_minmax` → salteado (`x[::stride]`) | `decimado_conserva_picos` | `hammer: max(max_decimado)=0.0331781 != max(max_crudo)=0.0354097` |
| `load_signal(apply_invert=False)` | `polaridad_fija` | `hammer: min=0.0, se esperaba <= -0.9 (invertido)` |
| Sacar la conversión de no-finitos a `null` | `nan_a_null` | `/api/signal -> 500` |
| NaN → `0.0` en vez de `null` (la mentira sutil) | `nan_a_null` | `geo.min no tiene ningún null` |
| `geo_flip` aplicado también al hammer | `geo_flip_override` | `el hammer cambió entre las dos respuestas` |
| `kind` ignorado (`prefer_filtered = False`) | `kind_filt` | `hammer: used_filtered=False con kind=filt` |
| handler `def` → `async def` | `no_bloquea` | `/health tardó 3.6s mientras /api/signal corría en paralelo` |

Ninguno está escrito para pasar siempre. El de `no_bloquea` en particular mide
de verdad: con `async def` el event loop queda tomado 3.6 s y se ve.

### Reglas duras

- **`data/` intacto**: `git status --porcelain` dentro de `C:\Github\Tesis\data`
  sale vacío y no hay ninguna carpeta `smoke_*` en `data\raw`. Los fixtures se
  escriben en el `raw_root` del sandbox (`tempfile.mkdtemp`) y `_write_fixture`
  tiene un `assert ctx.sandbox and "smoke_sandbox" in str(ctx.raw_root)` como
  cinturón. No se usó `/ingest` para meterlos, así que no se corrió
  `save_annotations` sobre el archivo de picks real (§8.1) — la trampa peor,
  esquivada bien.
- **Sólo lectura de verdad**: no hay `save_annotations` en el diff. `picks.py`
  intacto.
- **Sin mutaciones colgadas**: tras mis pruebas, `git --no-pager diff --stat`
  vuelve idéntico al original (5 archivos, 508 insertions(+), 6 deletions(-)),
  no hay `.bak` en el árbol y `git status --porcelain` (submódulo y raíz) coincide
  con el estado previo.
- **Archivos prohibidos**: `api.py` (y su orden de `add_middleware`),
  `index.html`, `main.js`, `theme*.js`, `pipeline.py`, `catalog.py`,
  `routers/{ingest,admin,picks,masw}.py` y todo `geophone_scope/` sin tocar.
  `plot.js` conserva `drawSeries`.
- **§1 sobrevivió**: `base.cors_preflight`, `refactor.cors_en_post`,
  `base.ingest_responde_rapido` y `refactor.worker_no_bloquea` en PASS.

### Reuso (§0.4), no reimplementación

`discover_dataset`, `load_signal(apply_invert=True)`, `auto_pick_shot`,
`load_annotations`, `default_annotations_path`, `_zero_by_pretrigger`,
`channel.signal_file()`. Verifiqué contra `field_review_data.py` que la
convención de polaridad **no** se re-implementó: `invert_applied` reporta
`channel.invert_signal` (que para el hammer sin marca en la metadata es
`not False == True`, `:1664-1673`) y la negación la hace `load_signal`. El orden
de operaciones del §4.3 está respetado, incluido el mismo `trigger_idx` para los
dos canales y **cada canal decimado con su propio largo** (no se truncan al
mínimo).

### Front

- El visor está en `capturas_signal.js` aparte; `renderJobs`/`renderDataset` no
  se reescribieron.
- El listener del botón `ver` está delegado en `#dataset`, y `renderDataset` hace
  `host.innerHTML = …` sobre ese mismo `#dataset` (no lo reemplaza), así que el
  listener sobrevive los ticks de 3 s. Correcto.
- El visor **no** entra en el `setInterval`: sólo se pide señal al elegir captura,
  cambiar `kind`, tocar el flip o apretar `recargar`. `AbortController` cancela el
  fetch en vuelo y `destroy()` limpia el listener de `resize`.
- Habilita por `pick.shot_id`, no por `c.pickable` — es lo correcto y está
  comentado con el motivo.
- Buckets `null` no se dibujan como 0: cada bucket es un `moveTo`/`lineTo`
  independiente y el `null` se saltea, así que no queda una línea falsa uniendo
  extremos.

### Dudas anotadas

`DUDAS_LUNES.md` tiene las dos que correspondían (§8.1 `_procesados_dir_for`
compartido por `raw_root.name`, y `catalog.pickable` 186 vs 194 disparos), con
opciones y sin decidir por el usuario.

---

## Nits (no bloquean, para quien siga)

1. `capturas.signal.sin_nan_en_json` **no puede fallar hoy**: lo comprobé —
   con la conversión a `null` sacada, ese check sigue en PASS porque el dataset
   real no trae NaN; lo que falla es `nan_a_null` (sandbox). O sea que la
   afirmación del spec §6.2 paso 4 ("y `sin_nan_en_json` también") es optimista.
   La cobertura existe, pero vive en el check de sandbox: no se apoye nadie en
   `sin_nan_en_json` como red para esto.
2. `<span class="sub">` en la celda `—` de la tabla: en `app.css` la regla es
   `p.sub` (`:57`), así que el span queda sin estilo. El `title` con la
   explicación sí funciona. Cosmético.
3. Quedaron algunos `style="…"` inline en `capturas_signal.js` (fila de
   controles, márgenes) en vez de clases; `app.css` ya tiene `.viewer`,
   `.viewer-meta`, `.plot-label` y `canvas.plot`. No rompe nada
   (`refactor.index_sin_logica` sólo mira `index.html`), pero es deuda menor.
4. `geo_flip_source` usa el vocabulario `annotation|default|override`, más
   amplio que el ejemplo del spec §4.2. Es más informativo y nadie lo chequea;
   dejarlo, pero que el ítem de `POST /api/pick` lo respete.
5. Falta la validación humana del §6.3 (el gate no ejecuta JS): martillo
   apuntando para abajo, trigger sobre el flanco, geo arrancando en `t=0`,
   `filt` cambiando la traza y el redibujo al cambiar de tema. El implementador
   lo declaró como hueco en vez de fingir cobertura, que es lo correcto, pero
   sigue pendiente de un par de ojos.
