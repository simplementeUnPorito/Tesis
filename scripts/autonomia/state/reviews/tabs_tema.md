VERDICT: PASS

feat(web): 8 tabs con los nombres exactos de la app + 3 subtabs de MASW, placeholders que dicen qué falta y de qué § del plan, y toggle de tema sin fogonazo (theme-boot.js) — 6 checks `tabs.*` nuevos, 12/12 mutaciones detectadas

---

## Qué verifiqué (2026-07-25)

**Gate del ítem** — `--only base --only tabs --require tabs`: **13/13 PASS**, exit 0.
Log: `state/gate/gate_20260725_010536.log`.

**No rompió el ítem anterior** — `--only refactor`: **8/8 PASS**, exit 0. En
particular `refactor.index_sin_logica` (no entró `fetch(`, `setInterval(` ni
`<style` en `index.html`) y `refactor.tabs_presentes`.

**Los checks nuevos PUEDEN fallar.** No me lo creí: muté el código y corrí el
gate 12 veces (backup fuera del repo, restaurado después de cada una). **Las 12
mutaciones fueron detectadas**, con el mensaje correcto y apuntando al panel/
archivo culpable:

| mutación | check que la cazó |
|---|---|
| `Waterfall` → `Waterfalll` en el botón | `tabs.nombres_y_orden` ("orden roto: 'Waterfall' debería ir antes que 'MASW'") |
| borrar `Falta:` del placeholder de enfase | `tabs.placeholders_honestos` (nombra `panel-enfase`) |
| borrar el `§` del placeholder de waterfall | `tabs.placeholders_honestos` |
| borrar la subtab `2. Inversion` | `tabs.masw_subtabs` |
| generar las subtabs desde JS (sacarlas del HTML) | `tabs.masw_subtabs` |
| botón `data-tab` extra sin su `<section>` | `tabs.nombres_y_orden` + `tabs.panel_por_tab` |
| renombrar `id="panel-enfase"` (panel huérfano) | `tabs.panel_por_tab` + `tabs.placeholders_honestos` |
| mover `theme-boot.js` al final del `<body>` | `tabs.tema_sin_flash` |
| `theme-boot.js` con `defer` | `tabs.tema_sin_flash` |
| cambiar la clave en `theme-boot.js` y no en `theme.js` | `tabs.tema_sin_flash` |
| quitar la regla `[data-theme="dark"]` del CSS | `tabs.tema_toggle` |
| renombrar `id="btn-theme"` | `tabs.tema_toggle` |

El detalle que más fácil se escribía para-pasar-siempre —
`tabs.nombres_y_orden` — está bien hecho: usa bordes de letra
(`(?<![A-Za-z])…(?![A-Za-z])`) en vez de `in`, así que `Waterfalll` no matchea
como `Waterfall`, y el orden se rompe igual porque el `<h2>` del panel queda
después del botón `MASW`. No es un check decorativo.

**Reglas duras**: nada tocado dentro de `C:\Github\Tesis\data` (el repo de datos
da `git status --porcelain` vacío; el gate usa `%TEMP%\smoke_sandbox_*`). Ni
hardware, ni `pio`, ni push, ni submódulos, ni `.cyprj`. Matar procesos: sólo por
PID exacto de lo que arranqué yo.

**Sin mutaciones colgadas** (regla 11). `git status --porcelain` del submódulo
queda exactamente en los 5 modificados + 2 nuevos del ítem, sin ningún `.bak`:

```
 M server/smoke_test.py       ?? server/static/js/tabs/masw.js
 M server/static/css/app.css  ?? server/static/js/theme-boot.js
 M server/static/index.html
 M server/static/js/main.js
 M server/static/js/theme.js
```

**§1 sobrevivió**: el diff no toca `api.py`, `app.py`, `pipeline.py`, `catalog.py`
ni `routers/**` — o sea el orden de `add_middleware` sigue intacto. Confirmado por
gate: `base.cors_preflight`, `refactor.cors_en_post`,
`base.ingest_responde_rapido` (respuesta antes de preprocesar) y
`refactor.worker_no_bloquea` (hilo aparte) los cuatro en PASS.

**§0.4 reusar, no reimplementar**: el ítem es front estático + checks; no hay una
sola fórmula copiada. Y los nombres de función que citan los placeholders
**existen de verdad** (los verifiqué uno por uno en
`geophone_scope/field_review_data.py`): `load_filter_settings:486`,
`save_filter_settings:505`, `apply_bandpass_filter:906`,
`load_alignment_offsets:521`, `save_alignment_offsets:545`,
`load_average_arrivals:443`, `save_average_arrivals:464`; `masw_dispersion.py` y
`masw_backends.py` también están. Un placeholder que promete una función
inexistente es peor que uno vacío, y no es el caso. La duda del §3.2 con los
nombres viejos del plan (`dcRemove`/`filtFilt`/`hilbertEnvelope`, que no existen)
quedó escrita en `docs/proyecto/DUDAS_LUNES.md` #7 sin decidirla, que es lo correcto.

**Nada a medio portear que diga que anda**: `theme.js` mantiene el patrón de
`master/data/js/app.js` (`localStorage` con try/catch, próximo estado calculado
desde el DOM), sin inventar un tercer estado "auto"; el `aria-pressed`/`title` se
actualiza en `applyTheme()`, así arranca correcto en el primer render y no sólo al
clickear. `masw.js` está calcado de `activateTab` y devuelve su función de
desmontaje, que `main.js:29` sí usa. `capturas.js`, `borrado.js` y `plot.js` no
fueron tocados.

**Un hueco del gate que tapé a mano**: ningún check pide `tabs/masw.js`, y un 404
ahí rompería el grafo de módulos ES completo (ninguna tab andaría) sin que el gate
se enterase. Levanté el servidor y los pedí: `masw.js` 200 (802 B),
`theme-boot.js` 200 (466 B), `main.js` 200, `capturas.js` 200.

## Notas para el que siga (no bloquean, no arreglar ahora)

1. `tabs.placeholders_honestos` cuenta los ≥ 120 caracteres sobre el bloque
   entero, tags y `<h2>` incluidos (~50 caracteres de arranque). Es lo que pedía
   el spec §6, y con `Falta:` + `§` obligatorios alcanza; pero si algún día un
   placeholder queda flaco, el umbral solo no lo va a cazar.
2. `.placeholder` (`app.css:111`) es byte por byte igual a `.empty`
   (`app.css:136`), que sigue en uso en `capturas.js`. Dos nombres para la misma
   regla; unificar cuando se toque el CSS, no antes (§9 del spec prohíbe rediseñar
   acá).
3. Queda pendiente lo único que el gate no puede ver, y está bien que no lo vea:
   la validación humana de §7 — que el click cambie de panel/subpanel y que tras
   `F5` no haya fogonazo. El gate habla HTTP, no ejecuta JS, y el spec
   explícitamente prohíbe fingir esa cobertura con un check estructural.
