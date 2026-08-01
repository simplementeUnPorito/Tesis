SPEC_READY

# tabs_tema — §2 Tabs de navegación + toggle de tema

Objetivo: dejar la navegación de la web **a paridad de nombres** con la app PyQt
(8 tabs + 3 subtabs de MASW), con placeholders que digan **qué falta y dónde está
escrito**, y el toggle manual de tema claro/oscuro andando y persistido.

Buena noticia y trampa a la vez: **el ítem §1 (refactor a FastAPI) ya dejó medio
hecho esto**. Las 8 tabs y el toggle ya existen. Este ítem NO es "crear las
tabs desde cero": es cerrar el delta. Si empezás reescribiendo `index.html`
entero vas a romper checks que hoy pasan (`refactor.*`). Leé §2 de este spec
antes de tocar nada.

**Nada de dependencias nuevas, ni build step, ni CDN.** La web se sirve por
Tailscale a un campo sin internet: todo tiene que estar en `static/`. Módulos ES
nativos (`<script type="module">`), que es lo que ya usa `main.js`.

---

## 1. Estado actual (verificado, no lo re-averigües)

| Pieza | Dónde | Estado |
|---|---|---|
| 8 botones de tab con los nombres exactos | `static/index.html:17-26` | **ya está** |
| 8 `<section id="panel-*">` | `static/index.html:28-49` | ya están, pero 6 tienen placeholder inútil |
| Router de tabs (click → activar panel + `mount()`) | `static/js/main.js:12-37` | ya está |
| Toggle de tema (`data-theme` + `localStorage`) | `static/js/theme.js` | ya está; falta anti-flash y estado accesible |
| Variables CSS de los dos temas | `static/css/app.css:1-30` | ya está |
| Tabs con contenido real | `capturas.js`, `borrado.js` | ya están; **no tocarlos** |
| Subtabs de MASW | — | **no existen: hay que hacerlas** |

Checks del gate que hoy pasan y que este ítem **no puede romper**:
`refactor.tabs_presentes` (los 8 literales en `/`),
`refactor.index_sin_logica` (sin `fetch(`, `setInterval(` ni `<style` inline en
`/`), `refactor.estaticos` (`main.js`, `theme.js`, `plot.js` > 100 B).

---

## 2. Archivos a crear / editar (rutas absolutas)

### Crear

| Ruta | Contenido |
|---|---|
| `C:\Github\Tesis\src\interfaces\python\server\static\js\theme-boot.js` | 5-10 líneas, **script clásico, no módulo**: lee `localStorage['geo-theme']` y escribe `document.documentElement.dataset.theme` **antes del primer paint**. Nada más. Ver §4. |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\tabs\masw.js` | Módulo de la tab MASW: sólo enruta las 3 subtabs (activar botón + mostrar subpanel). No dibuja nada: §3.5 del plan es otro ítem. Exporta `mount(root)` con la misma firma que `capturas.js` / `borrado.js`. |

### Editar

| Ruta | Qué |
|---|---|
| `C:\Github\Tesis\src\interfaces\python\server\static\index.html` | (a) `<script src="/static/js/theme-boot.js"></script>` en el `<head>`; (b) subtabs de MASW dentro de `#panel-masw`; (c) reescribir los 6 placeholders con el formato honesto de §5. **No mover ni renombrar** los 8 botones ni los `id="panel-*"`. |
| `C:\Github\Tesis\src\interfaces\python\server\static\css\app.css` | estilos de `.subtabs` / `.subtab-btn` (variante chica de `.tabs` / `.tab-btn`, ya definidos en `app.css:59-80`) y de `.placeholder`. Reusar las variables CSS que ya existen (`--panel-border`, `--th-fg`, …); no hardcodear colores nuevos, que rompe el tema oscuro. |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\main.js` | registrar `masw` en el mapa `TABS` (`main.js:5-8`). Nada más: el router de tabs ya sirve tal cual. |
| `C:\Github\Tesis\src\interfaces\python\server\static\js\theme.js` | exportar la constante del storage key, reflejar el estado en el botón (`aria-pressed` + `title`), y no duplicar la lectura inicial que ahora hace `theme-boot.js`. Ver §4. |
| `C:\Github\Tesis\src\interfaces\python\server\smoke_test.py` | agregar los 6 checks `tabs.*` de §6, en una sección nueva `# ── Checks tabs (§2 …)` después de los `refactor.*`. |

### No tocar

`api.py`, `app.py`, `pipeline.py`, `catalog.py`, `routers/**`, `capturas.js`,
`borrado.js`, `plot.js`, y todo `geophone_scope/`. Este ítem es **sólo front
estático + checks**. Si sentís que necesitás una ruta nueva del servidor, te
saliste del ítem: anotalo y seguí.

En particular **no toques el orden de `add_middleware` en `api.py:69-89`**: el
comentario de ahí no es decorativo, `_TitleCaseHeaders` tiene que quedar el más
externo o `base.cors_preflight` deja de pasar.

---

## 3. Los nombres exactos (copiar carácter por carácter)

Verificados contra la app PyQt, no contra el plan:

| Tab | Fuente | `data-tab` |
|---|---|---|
| `Capturas` | `geophone_scope/field_review_app.py:659` | `capturas` |
| `Filtros` | `field_review_app.py:710` | `filtros` |
| `Agrupamiento` | `field_review_app.py:711` | `agrupamiento` |
| `Enfase` | `field_review_app.py:712` | `enfase` |
| `Promedios / arrivals` | `field_review_app.py:713` | `promedios` |
| `Waterfall` | `field_review_app.py:714` | `waterfall` |
| `MASW` | `field_review_app.py:715` | `masw` |
| `Borrado` | PORT_PLAN §4 (no existe en la app) | `borrado` |

Subtabs de MASW (`field_review_app.py:4092-4094`):

| Subtab | `data-subtab` |
|---|---|
| `1. Dispersion` | `dispersion` |
| `2. Inversion` | `inversion` |
| `3. Perfil Vs` | `perfil` |

Detalles que parecen tontos y no lo son:

- `Promedios / arrivals` lleva **espacios alrededor de la barra**.
- `1. Dispersion` y `2. Inversion` van **sin tilde** (así están en la app; no las
  "corrijas": la paridad de nombres es el objetivo del ítem).
- El punto y el espacio después del número forman parte del literal.

Marcado de las subtabs (dentro de `#panel-masw`, en el HTML **estático**, no
generado por JS — ver §6, el gate sólo ve lo que devuelve `GET /`):

```html
<nav class="subtabs" id="masw-subtabs">
  <button class="subtab-btn active" data-subtab="dispersion">1. Dispersion</button>
  <button class="subtab-btn" data-subtab="inversion">2. Inversion</button>
  <button class="subtab-btn" data-subtab="perfil">3. Perfil Vs</button>
</nav>
<section id="subpanel-dispersion" class="subtab-panel">…</section>
<section id="subpanel-inversion" class="subtab-panel" hidden>…</section>
<section id="subpanel-perfil" class="subtab-panel" hidden>…</section>
```

`masw.js` sólo engancha el click sobre `#masw-subtabs` y hace el toggle de
`hidden` / `.active`, calcado de `activateTab` (`main.js:12-29`). No inventes un
router nuevo.

---

## 4. Tema: qué falta y de dónde se copia

El patrón de referencia es `initTheme()` / `applyTheme()` de la SPA del maestro:
`src/firmware/esp32/Nodo comunicación/master/data/js/app.js:2392-2419`
(`localStorage` con try/catch porque en modo privado tira, y el listener del
botón calculando el próximo estado desde el estado actual del DOM). Eso **ya está
portado** en `static/js/theme.js:30-43`, con `data-theme` en `:root` en vez de
una clase en `<body>`, como pide PORT_PLAN §2. No lo reescribas.

Falta:

1. **Flash de tema equivocado.** `main.js` es `type="module"` → se ejecuta
   diferido, después del primer paint. Si el usuario forzó *claro* en un sistema
   oscuro, ve un fogonazo oscuro en cada carga. Se arregla con
   `theme-boot.js`: script **clásico** (sin `type="module"`, sin `defer`) en el
   `<head>`, que aplica el tema guardado y nada más:

   ```js
   // Corre antes del primer paint: sin esto, main.js (type=module, diferido)
   // aplica el tema recién después de pintar y se ve un fogonazo del tema
   // contrario en cada carga.
   try {
     var t = localStorage.getItem('geo-theme');
     if (t) document.documentElement.dataset.theme = t;
   } catch (e) { /* localStorage deshabilitado: queda prefers-color-scheme */ }
   ```

   Sin valor guardado **no escribe nada**: el fallback es la media query de
   `app.css:20-30`, que ya hace lo correcto. No dupliques la detección de
   `prefers-color-scheme` acá.

2. **La clave del storage tiene que ser una sola.** Hoy `'geo-theme'` está
   hardcodeada en `theme.js:4`. `theme-boot.js` no puede importarla (es script
   clásico), así que queda duplicada a propósito: dejá en **los dos archivos** un
   comentario que diga que si cambia una, cambia la otra. El check
   `tabs.tema_sin_flash` verifica que el literal coincida.

3. **Estado visible del botón**: `#btn-theme` tiene que llevar
   `aria-pressed="true|false"` y un `title` que diga a qué cambia
   (p. ej. `"Cambiar a tema claro"`). Se actualiza en `applyTheme()`, no en el
   listener, así arranca correcto en el primer render.

Lo que **no** hay que hacer: un tercer estado "auto" en el toggle. El plan pide
claro/oscuro manual con `prefers-color-scheme` como valor inicial, nada más.

---

## 5. Placeholders honestos (el corazón del ítem)

Regla: un placeholder tiene que servirle a alguien que abre la web el lunes y se
pregunta *"¿esto está roto o todavía no está hecho?"*. **Formato obligatorio**,
tres partes, en este orden:

1. Un `<h2>` con el nombre exacto de la tab.
2. Una línea que empiece con `Falta:` y describa **la funcionalidad concreta**,
   nombrando las funciones que se van a reusar.
3. Una referencia al plan con el carácter `§` (p. ej. `PORT_PLAN §3.2`).

Prohibido: `"pendiente de porteo."` a secas (que es lo que hay hoy en
`index.html:31-47`), pantallas vacías, y "próximamente".

Contenido por panel — usá estos textos, ya están chequeados contra el código
real (los nombres de función son los que **existen**, ver la nota de §8):

- **`panel-filtros`** — `Falta: el pasa-banda Butterworth de fase cero (los
  mismos parámetros que la app, persistidos en el mismo archivo) sobre
  frd.load_filter_settings / save_filter_settings + frd.apply_bandpass_filter.
  PORT_PLAN §3.2.`
- **`panel-agrupamiento`** — `Falta: agrupar capturas por distancia y armar el
  promedio por carpeta. PORT_PLAN §3.3.`
- **`panel-enfase`** — `Falta: el enfase por carpeta (no por captura) con
  frd.load_alignment_offsets / save_alignment_offsets. PORT_PLAN §3.2.`
- **`panel-promedios`** — `Falta: promedios por carpeta con
  frd.load_average_arrivals / save_average_arrivals y el botón "Rechazar esta
  carpeta", que excluye del promedio sin invalidar las capturas. PORT_PLAN §3.3.`
- **`panel-waterfall`** — `Falta: la imagen de waterfall, la polaridad por punto
  (geo_flip), "Invertir traza" / "Auto polaridad" y la persistencia json+npz de
  la app. PORT_PLAN §3.4.`
- **`subpanel-dispersion`** — `Falta: la imagen f-v (masw_dispersion.py) y las
  regiones-polígono editables que dan N curvas por modo. PORT_PLAN §3.5.`
- **`subpanel-inversion`** — `Falta: correr los backends de masw_backends.py
  como trabajos del Pipeline (tardan minutos: no van en el request) y mostrar
  progreso. PORT_PLAN §3.5.`
- **`subpanel-perfil`** — `Falta: el perfil Vs resultante de la inversión, con
  curva editable. PORT_PLAN §3.5.`

`panel-masw` en sí **no** lleva placeholder propio: lleva las subtabs, y el
placeholder vive en cada subpanel.

`panel-capturas` y `panel-borrado` **no llevan placeholder**: ya tienen contenido
real montado por JS (`capturas.js`, `borrado.js`) y están vacíos en el HTML a
propósito. El check de §6 los excluye explícitamente.

---

## 6. Checks a agregar al gate

Van en `smoke_test.py`, con `@check("tabs.<nombre>", "<qué prueba>",
mode="read")`. Todos son de lectura: sólo hacen `GET` de HTML/CSS/JS estático, no
escriben nada. El registro se descubre solo (`smoke_test.py:135-139`); no hay que
tocar `main()`.

Un helper local (no un check) que van a usar varios:

```python
def _index_text(ctx: Ctx) -> str:
    code, body, _ = ctx.get("/")
    assert code == 200, f"/ -> {code}"
    return body.decode("utf-8", "replace")
```

| id | modo | qué asserta | cómo se lo hace fallar |
|---|---|---|---|
| `tabs.nombres_y_orden` | read | Los 8 literales de §3 aparecen en `/` **en ese orden** (posiciones `str.find` estrictamente crecientes) y hay exactamente 8 ocurrencias de `data-tab="` | renombrar `Waterfall` o intercambiar dos tabs |
| `tabs.masw_subtabs` | read | Los 3 literales `1. Dispersion`, `2. Inversion`, `3. Perfil Vs` están en `/`, con sus `data-subtab="dispersion|inversion|perfil"` y sus `id="subpanel-…"` | borrar una subtab, o generarla desde JS en vez de HTML |
| `tabs.panel_por_tab` | read | Para **cada** `data-tab="X"` extraído con regex de `/` existe un `id="panel-X"`, y viceversa (ningún panel huérfano) | agregar un botón sin su `<section>` |
| `tabs.placeholders_honestos` | read | Para cada uno de los 8 paneles pendientes (`filtros`, `agrupamiento`, `enfase`, `promedios`, `waterfall`, `subpanel-dispersion`, `subpanel-inversion`, `subpanel-perfil`): el bloque contiene `Falta:` **y** el carácter `§`, y tiene ≥ 120 caracteres | dejar el `"pendiente de porteo."` actual (hoy este check falla, que es el punto) |
| `tabs.tema_toggle` | read | `/` tiene `id="btn-theme"`; `/static/js/theme.js` contiene `localStorage`, `data-theme` y `prefers-color-scheme`; `/static/css/app.css` define **las dos** reglas `[data-theme="dark"]` y `[data-theme="light"]` | volver al tema sólo por media query (la regresión que §2 viene a arreglar) |
| `tabs.tema_sin_flash` | read | `/` referencia `/static/js/theme-boot.js` **antes de `</head>`** y esa etiqueta no tiene `type="module"` ni `defer`; el archivo responde 200; el literal de la clave (`geo-theme`) aparece igual en `theme-boot.js` y en `theme.js` | cambiar la clave en un archivo y no en el otro; o mover el script al final del `<body>` |

Notas de implementación de los checks:

- Para `tabs.placeholders_honestos`, extraé el bloque de cada panel con un regex
  no-greedy entre `id="panel-filtros"` y el `</section>` que lo cierra. Si un
  panel tiene `<section>` anidadas el regex simple se queda corto: en ese caso
  cortá desde `id="panel-X"` hasta el próximo `id="panel-` (o el fin del
  documento). Es lo bastante robusto para un HTML que escribimos nosotros y no
  mete un parser HTML como dependencia.
- El mensaje del `assert` tiene que decir **qué panel** falló y **qué le falta**,
  no `assert False`. Los mensajes de los checks existentes
  (`smoke_test.py:161-164`) son el estándar: el que lee el log no debería tener
  que abrir el código.
- No agregues un check de "el click cambia de tab": el gate habla HTTP, no
  ejecuta JS. Fingir cobertura de comportamiento con un check estructural es peor
  que declarar el hueco. Eso queda para la validación humana (§7).

---

## 7. Criterio de aceptación

Ejecutable (es el gate del ítem):

```
cd "C:\Github\Tesis\src\interfaces\python" && python "C:\Github\Tesis\src\interfaces\python\server\smoke_test.py" --only base --only tabs --require tabs --json "C:\Github\Tesis\scripts\autonomia\state\gate\tabs_tema.json"
```

Tiene que dar `0` con **todos** los checks en PASS. Antes de darlo por bueno,
corré también

```
python "C:\Github\Tesis\src\interfaces\python\server\smoke_test.py" --only refactor
```

para probar que no rompiste el ítem anterior (sobre todo
`refactor.index_sin_logica`: no metas `fetch(`, `setInterval(` ni `<style` en
`index.html`).

Prueba de que los checks pueden fallar (regla 11 del prompt, hacela de verdad):

1. `cp index.html index.html.bak`
2. Cambiá `Waterfall` por `Waterfalll` → `tabs.nombres_y_orden` FAIL.
3. Restaurá; borrá la palabra `Falta:` de un placeholder →
   `tabs.placeholders_honestos` FAIL.
4. Restaurá, borrá el `.bak`, y demostrá con `git status --porcelain` que no
   quedó ninguna mutación colgada (el `.bak` tampoco: no debe aparecer).

Observable a mano (no lo cubre el gate, y está bien que no lo cubra):
levantar `cd src/interfaces/python && python -m server --port 8000`, abrir
`http://127.0.0.1:8000`, y ver que (a) las 8 tabs cambian de panel, (b) las 3
subtabs de MASW cambian de subpanel, (c) el toggle 🌓 cambia el tema, (d) tras
`F5` el tema elegido sigue puesto **y no hay fogonazo** del tema contrario.

---

## 8. Trampas del §5 del plan que aplican acá

- **§5.1 — el proceso viejo no toma los cambios.** Es la que más te va a morder
  en este ítem. Los `.html`/`.css`/`.js` se sirven desde disco: se recargan
  solos. Pero `Cache-Control: no-store` lo pone el middleware
  (`api.py:78-82`) sólo para el servidor; **el navegador igual cachea módulos ES
  agresivamente**. Si editaste `theme.js` y no ves el cambio, recargá con
  `Ctrl+F5` antes de sospechar del código. Y si tocás Python (no deberías en este
  ítem), reiniciá el servidor.
- **§5.2 — CORS.** No toques el bloque de middlewares. Lo aclaro porque el
  toggle de tema tienta a agregar headers o middlewares "chiquitos": cualquier
  cosa insertada después de `_TitleCaseHeaders` lo saca de ser el más externo y
  `base.cors_preflight` empieza a fallar por una razón que no tiene nada que ver
  con lo que estabas haciendo.
- **§5.6 — Windows/OneDrive.** Todo lo que escribe este ítem vive dentro de
  `server/static/`. **Nada** dentro de `C:\Github\Tesis\data` (regla 2 del
  prompt): el gate ya usa directorios temporales y no hace falta que vos escribas
  ni un archivo ahí.
- Las trampas §5.4 y §5.5 (martillo/picking, `discover_dataset`) **no aplican**:
  este ítem no toca datos.

### Nota: los nombres de función del plan §3.2 están viejos

PORT_PLAN §3.2 dice de filtrar con `signal_proc.py`: `dcRemove`, `filtFilt`,
`harmonicNotch`, `hilbertEnvelope`. **Esos nombres no existen en el repo.** Lo
que existe:

- `geophone_scope/signal_proc.py:367` `dc_remove`, `:235` `harmonic_notch`,
  `:37` `fir_filter` — son las del scope en vivo.
- `geophone_scope/field_review_data.py:906` `apply_bandpass_filter` y `:873`
  `design_bandpass_filter` — **estas** son las que usa el tab Filtros de la app
  PyQt (`field_review_app.py:1970`), o sea las que corresponden para la paridad.
- No hay ninguna `hilbertEnvelope`.

Por eso los placeholders de §5 citan `frd.apply_bandpass_filter` y no los nombres
del plan. Queda anotado en `DUDAS_LUNES.md` porque decidir si el plan se corrige
o si además hay que portar el notch/DC de `signal_proc` no es una decisión del
implementador de este ítem.

---

## 9. Fuera de alcance (no lo hagas aunque tiente)

- Persistir la tab activa en `localStorage` o en el hash de la URL. No lo pide el
  plan y agrega un estado que después hay que sincronizar con el deep-link de
  §3.1.
- Empezar a portar cualquiera de las tabs con placeholder. Cada una es su propio
  ítem del loop, con su propio gate.
- Rediseñar el CSS. Reusá las variables que ya están; el objetivo es paridad de
  navegación, no un rediseño visual.
