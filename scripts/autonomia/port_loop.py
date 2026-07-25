#!/usr/bin/env python3
"""Loop autónomo del porteo del PORT_PLAN, con contexto limpio por fase.

Idea central: **el "clear" sale gratis con procesos separados.** Cada fase lanza
un ``claude -p`` nuevo, que arranca con contexto virgen, hace UNA cosa, deja el
resultado en disco y muere. El loop no depende de que ningún modelo recuerde
nada: todo el estado vive en ``state/port_state.json`` y en los .md de spec y
review. Se puede matar y relanzar en cualquier momento sin perder el hilo.

Fases por ítem (tres procesos, tres contextos limpios)
-----------------------------------------------------
1. ``spec``   (opus)   lee el PORT_PLAN y el repo, escribe el spec del ítem con
                       criterio de aceptación y qué checks agregar al gate.
2. ``impl``   (sonnet) implementa contra el spec y deja el gate verde.
3. ``review`` (opus)   revisa el diff contra el spec y dictamina PASS/FAIL.

Escalera de escalado (Fable es carta de emergencia, no default)
--------------------------------------------------------------
intento 1 sonnet -> intento 2 sonnet + feedback del review -> intento 3 **fable**.
También se salta directo a Fable si el advisor o el reviewer escriben
``NEEDS_FABLE`` (o sea: alguien con más contexto dijo "esto necesita más
cabeza"). Cada escalado queda logueado; si el intento con Fable falla, el ítem
queda ``blocked``, se anota en DUDAS_LUNES.md y el loop **para**: arrastrar un
refactor torcido a los ítems siguientes es peor que no avanzar.

Límites de uso
--------------
Si la CLI reporta límite de tokens/rate limit, el loop **espera lo que haga
falta** y reintenta la misma fase (son idempotentes: el estado está en disco).
Si el mensaje trae el epoch de reseteo, espera hasta ahí; si no, backoff
15m/30m/60m. No hay tope de reintentos por límite — sí lo hay por error real.

Uso
---
    python port_loop.py --status         # ¿por dónde anda?
    python port_loop.py --dry-run        # qué haría, sin gastar un token
    python port_loop.py                  # correr (esto es lo que queda de fondo)
    python port_loop.py --reset-item refactor
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PY_ROOT = REPO / "src" / "interfaces" / "python"
SERVER = PY_ROOT / "server"
PLAN = SERVER / "PORT_PLAN.md"
GATE = SERVER / "smoke_test.py"

STATE_DIR = HERE / "state"
STATE_FILE = STATE_DIR / "port_state.json"
STATUS_FILE = STATE_DIR / "status.json"
LOG_FILE = STATE_DIR / "loop.log"
PROMPTS = STATE_DIR / "prompts"
SPECS = STATE_DIR / "specs"
REVIEWS = STATE_DIR / "reviews"
GATE_OUT = STATE_DIR / "gate"
RAW_OUT = STATE_DIR / "raw"
# En el repo raíz a propósito, NO en docs/: docs es un submódulo y commitear el
# gitlink desde acá dejaría el puntero mirando un commit que no tiene el archivo.
DUDAS = REPO / "DUDAS_LUNES.md"

CLAUDE = shutil.which("claude") or "claude"

MODEL_WORKER = "sonnet"
MODEL_ADVISOR = "opus"
MODEL_HEAVY = "fable"        # carta de emergencia

PHASE_TIMEOUT_S = {"spec": 2400, "impl": 5400, "review": 2400}
MAX_ATTEMPTS = 3             # 3ro es Fable
LIMIT_BACKOFF_S = [900, 1800, 3600]

# ── Detección de límites de uso ───────────────────────────────────────────────
LIMIT_EPOCH = re.compile(r"limit reached\|(\d{9,13})", re.I)
LIMIT_GENERIC = re.compile(
    r"(usage limit|session limit|rate.?limit|rate_limit|\b429\b|too many requests"
    r"|overloaded|quota|limit will reset|resets? \d|upgrade to increase)", re.I)
# "You've hit your session limit · resets 3:00am" / "resets at 3pm (America/Asuncion)".
# Esperar hasta esa hora es mucho mejor que un backoff a ciegas: con backoff se
# despierta cada 15 min a chocarse con la misma pared.
LIMIT_CLOCK = re.compile(
    r"resets?\s*(?:at\s*)?(\d{1,2})(?::(\d{2}))?\s*([ap])\.?m\.?"
    r"|resets?\s*(?:at\s*)?(\d{1,2}):(\d{2})", re.I)
# Una hora de reloj puede estar hasta 24 h adelante (mensaje a las 00:20 que dice
# "resets 11pm"), así que el tope tiene que dar lugar a eso. Lo que acota el daño
# de un parseo malo no es este número sino SLEEP_CHUNK_S: nunca se duerme más de
# eso de una vez, y al despertar se vuelve a preguntar.
MAX_LIMIT_WAIT_S = 25 * 3600
SLEEP_CHUNK_S = 6 * 3600
FATAL_AUTH = re.compile(
    r"(invalid api key|authentication_error|not logged in|please run /login"
    r"|credit balance is too low)", re.I)


# ── Ítems en alcance: PORT_PLAN §1 + §3.1, y para ─────────────────────────────
@dataclass
class Item:
    iid: str
    title: str
    plan_ref: str
    goal: str
    gate_prefix: str
    extra: str = ""


ITEMS: list[Item] = [
    Item(
        iid="refactor",
        title="§1 Refactor a FastAPI + estáticos",
        plan_ref="§1 (y §0 decisiones 1-5, §5 trampas)",
        goal=(
            "Pasar el servidor de http.server a FastAPI con la estructura de §1 "
            "(api.py, routers/ingest|dataset|picks|masw|admin, static/ con "
            "index.html + css/app.css + js/main.js|theme.js|plot.js|tabs/). Los "
            "routers de picks/masw pueden quedar como esqueletos vacíos: lo que "
            "NO puede quedar a medias es que todo lo que hoy funciona siga "
            "funcionando idéntico."
        ),
        gate_prefix="refactor",
        extra=(
            "Requisitos que NO se pueden perder (§1):\n"
            "- POST /ingest con las MISMAS cabeceras CORS (Access-Control-Allow-*). "
            "Sin CORS la SPA del ESP32 aborta en el preflight y en el campo se ve "
            "como 'servidor inalcanzable'. Ya pasó.\n"
            "- El POST se responde ANTES de preprocesar. El operador no espera.\n"
            "- El worker sigue en hilo aparte (Pipeline), NO en el event loop: "
            "auto_pick_shot carga señales enteras y bloquearía el servidor.\n"
            "- `python -m server --port N --raw-root R --data-root D` tiene que "
            "seguir arrancando con esos mismos flags: el gate los usa.\n"
            "- Los defaults de raw_root/data_root no cambian."
        ),
    ),
    Item(
        iid="tabs_tema",
        title="§2 Tabs de navegación + toggle de tema",
        plan_ref="§2",
        goal=(
            "Esqueleto de las 7 tabs con los nombres EXACTOS de la app "
            "(Capturas, Filtros, Agrupamiento, Enfase, 'Promedios / arrivals', "
            "Waterfall, MASW con subtabs '1. Dispersion', '2. Inversion', "
            "'3. Perfil Vs') más la tab nueva 'Borrado', y el toggle manual de "
            "tema claro/oscuro. Las tabs sin portear muestran un placeholder "
            "honesto que diga qué falta, no una pantalla vacía."
        ),
        gate_prefix="tabs",
        extra=(
            "El toggle de tema se copia del patrón que ya existe en la SPA del "
            "maestro: `master/data/js/app.js` initTheme() — data-theme en :root + "
            "localStorage, con prefers-color-scheme como valor inicial. Copiar ese "
            "patrón, no inventar otro.\n"
            "Ruta: src/firmware/esp32/'Nodo comunicación'/master/data/js/app.js"
        ),
    ),
    Item(
        iid="capturas_signal",
        title="§3.1 GET /api/signal con decimado min/max",
        plan_ref="§3.1",
        goal=(
            "Endpoint GET /api/signal?shot_id=&kind=raw|filt&max_points= que "
            "devuelva la serie decimada lista para dibujar, y el dibujo de "
            "hammer + geo en la tab Capturas con el trigger marcado."
        ),
        gate_prefix="capturas.signal",
        extra=(
            "Decimar EN EL SERVIDOR con min/max por píxel: una captura de 60 s a "
            "2604 Hz son ~156k muestras por canal; mandarlas crudas al navegador "
            "es inútil, y un decimado que promedia o saltea se come los picos, "
            "que es justo lo que hay que ver.\n"
            "Reusar frd.load_signal / frd.detect_hammer_trigger / "
            "frd.auto_pick_shot. Polaridad FIJA: geo no invertido, hammer "
            "invertido — load_signal(apply_invert=True) ya lo hace, no "
            "re-implementarlo.\n"
            "Para catalogar usar catalog.py, NO discover_dataset (descarta las "
            "capturas sin par hammer+geo, §5.5)."
        ),
    ),
    Item(
        iid="capturas_pick",
        title="§3.1 Pick editable (POST /api/pick) + geo_flip",
        plan_ref="§3.1 y §0 decisión 2, §6",
        goal=(
            "Arrastrar el marcador de trigger y guardarlo: POST /api/pick con "
            "arrival_s, accepted, reviewed=true, geo_flip. Es el mínimo para que "
            "un humano valide de verdad, que es lo único que el preprocesado no "
            "puede hacer."
        ),
        gate_prefix="capturas.pick",
        extra=(
            "Escribir con frd.save_annotations() en "
            "procesados/field_review_annotations.json. NO inventar un formato "
            "paralelo: la app PyQt y la web tienen que convivir toda la "
            "transición, y el criterio de 'listo' (§6) es que la app vea el "
            "cambio y al revés.\n"
            "geo_flip por captura: el geófono conectado al revés graba en "
            "contrafase y destruye el promedio y el waterfall.\n"
            "El check del gate tiene que verificar el ida y vuelta REAL: escribir "
            "un pick por HTTP y volver a leerlo con frd.load_annotations, en un "
            "sandbox temporal — NUNCA sobre data/raw."
        ),
    ),
]

RULES = f"""\
REGLAS DURAS (valen para todas las fases; romper una es peor que no avanzar):

1. NO tocar hardware. No reflashear el PSoC ni ningún ESP: la rama del PSoC está
   sin terminar. No correr pio/platformio, ni ppcli, ni nada que programe.
2. NO escribir ni borrar nada dentro de {REPO / 'data'}. Es el dataset real, está
   bajo LFS y es irreemplazable. Todo lo que escriba tiene que ir a directorios
   temporales.
3. NO hacer git push. NO cambiar de rama. NO tocar submódulos con
   `submodule deinit` ni `--force`. Commitea el loop, no vos.
4. NO editar archivos de proyecto de PSoC Creator (.cyprj/.cydwr/.cysch/.cyfit).
5. Reusar, no reimplementar: field_review_data.py (frd), signal_proc.py y
   masw_*.py NO tienen Qt y se importan tal cual. Si te da ganas de copiar una
   fórmula, es señal de que hay que exponer la función que ya existe.
6. Una sola fuente de datos: raw_root es el mismo árbol que lee la app PyQt.
   La web no tiene datos propios.
7. Nada se borra solo: ni por incompleto, ni por viejo, ni por cuota.
8. Si algo no se puede resolver sin decidir algo que no te corresponde, NO lo
   inventes: anotalo en {DUDAS} (creá el archivo si no existe, con una entrada
   por duda: qué, por qué te frenó, y qué opciones ves) y seguí con el resto.
"""


# ── Estado ────────────────────────────────────────────────────────────────────
def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(msg: str) -> None:
    line = f"[{now()}] {msg}"
    print(line, flush=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


LOCK_FILE = STATE_DIR / "loop.lock"


def acquire_lock() -> bool:
    """Un solo loop a la vez.

    Pasó de verdad: dos procesos arrancaron en el mismo segundo y quedaron los
    dos implementando el MISMO ítem, editando los mismos archivos. Un candado con
    el PID lo evita; si el PID guardado ya no existe, el candado está huérfano y
    se toma.
    """
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    if LOCK_FILE.is_file():
        try:
            old = int(LOCK_FILE.read_text(encoding="utf-8").split()[0])
        except (ValueError, IndexError):
            old = -1
        if old > 0 and pid_alive(old):
            print(f"ya hay un loop corriendo (pid {old}). Si estás seguro de que "
                  f"no, borrá {LOCK_FILE}", file=sys.stderr)
            return False
        log(f"candado huérfano de pid {old}; lo tomo")
    LOCK_FILE.write_text(f"{os.getpid()} {now()}\n", encoding="utf-8")
    return True


def pid_alive(pid: int) -> bool:
    done = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                          capture_output=True, text=True)
    return str(pid) in (done.stdout or "")


def release_lock() -> None:
    if LOCK_FILE.is_file():
        try:
            if int(LOCK_FILE.read_text(encoding="utf-8").split()[0]) == os.getpid():
                LOCK_FILE.unlink()
        except (ValueError, IndexError, OSError):
            pass


def load_state() -> dict:
    if STATE_FILE.is_file():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    state = {
        "created": now(),
        "scope": "PORT_PLAN §1 + §3.1 (después para y espera revisión humana)",
        "cost_usd": 0.0,
        "items": {i.iid: {"status": "pending", "attempts": 0, "phase": None,
                          "model": None, "history": []} for i in ITEMS},
    }
    save_state(state)
    return state


def save_state(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(STATE_FILE)


def set_status(**kw) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    data = {"updated": now(), "pid": os.getpid()}
    if STATUS_FILE.is_file():
        try:
            data.update(json.loads(STATUS_FILE.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass
    data.update(kw)
    data["updated"] = now()
    tmp = STATUS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(STATUS_FILE)


# ── Prompts ───────────────────────────────────────────────────────────────────
def write_prompt(item: Item, phase: str, model: str, attempt: int,
                 feedback: str = "") -> Path:
    PROMPTS.mkdir(parents=True, exist_ok=True)
    spec_path = SPECS / f"{item.iid}.md"
    review_path = REVIEWS / f"{item.iid}.md"
    gate_json = GATE_OUT / f"{item.iid}.json"
    # --require: el ítem no puede pasar apoyándose sólo en los checks base.
    gate_cmd = (f'python "{GATE}" --only base --only {item.gate_prefix} '
                f'--require {item.gate_prefix} --json "{gate_json}"')

    common = f"""\
Trabajás en el repo {REPO} (rama cambios-red). El plan maestro es {PLAN} — leelo
ANTES de hacer nada; es la fuente de verdad y está escrito para que no dependas
de ninguna conversación previa.

Ítem en curso: [{item.iid}] {item.title}
Referencia del plan: {item.plan_ref}
Objetivo: {item.goal}

{item.extra}

Gate objetivo (criterio de "anda", ejecutable):
    cd "{PY_ROOT}" && {gate_cmd}
El gate está en {GATE} y arranca el servidor por HTTP, así que NO depende de la
implementación interna. Los checks nuevos se agregan ahí con el decorador
@check("{item.gate_prefix}.<nombre>", "<qué prueba>", mode="read"|"sandbox").

{RULES}
"""

    if phase == "spec":
        body = f"""\
Sos el ADVISOR. NO implementás: escribís el spec que va a ejecutar otro modelo
con contexto limpio, que no vio nada de esto.

{common}

Tarea:
1. Leé el PORT_PLAN completo y el código que este ítem toca (al menos
   {SERVER}/app.py, pipeline.py, catalog.py, y lo que el ítem necesite de
   {PY_ROOT}/geophone_scope).
2. Escribí el spec en {spec_path} con esta estructura:
   - Primera línea EXACTA: `SPEC_READY` (o `NEEDS_FABLE` si de verdad este ítem
     necesita un modelo más fuerte para razonarse; úsalo sólo si lo justificás en
     el spec, no por costumbre).
   - Qué archivos crear/editar, con rutas absolutas.
   - Las funciones existentes que hay que REUSAR, con archivo:línea. Este punto
     es el que más valor tiene: el implementador no conoce el repo.
   - Criterio de aceptación observable, y los checks concretos a agregar al gate
     (id, modo read/sandbox, qué asertan). Los checks tienen que poder fallar:
     un check que siempre pasa no es un check.
   - Trampas del §5 del plan que aplican a este ítem.
3. NO modifiques ningún archivo del servidor en esta fase. Sólo escribís el spec
   (y, si hace falta, {DUDAS}).

Tu salida de texto no la lee nadie: lo que importa es el archivo.
"""
    elif phase == "impl":
        fb = ""
        if feedback:
            fb = f"""
ATENCIÓN — este es el intento {attempt}. El intento anterior fue RECHAZADO en la
revisión. Feedback que tenés que resolver (no lo ignores, no lo discutas, no
reescribas desde cero lo que ya andaba):

{feedback}
"""
        body = f"""\
Sos el IMPLEMENTADOR. Ejecutás el spec que ya está escrito.

{common}

Spec a ejecutar: {spec_path} — leelo primero y seguilo. Si el spec se contradice
con el PORT_PLAN, gana el PORT_PLAN y lo anotás en {DUDAS}.
{fb}
Tarea:
1. Implementá el ítem según el spec.
2. Agregá al gate ({GATE}) los checks que el spec pide, con el prefijo
   `{item.gate_prefix}.`.
3. Corré el gate y dejalo VERDE:
       cd "{PY_ROOT}" && {gate_cmd}
   Iterá hasta que pase. Si un check no pasa por una razón legítima (algo que el
   plan no previó), NO lo borres ni lo debilites para que pase: dejalo fallando y
   anotá en {DUDAS} por qué. Un gate verde falso es el peor resultado posible.
4. NO commitees: del commit se encarga el loop.
5. Si el servidor viejo quedó corriendo con otro raw_root, reiniciálo (trampa
   §5.1 del plan: mostraba 1 captura en vez de 210).

Terminá cuando el gate esté verde. Tu último mensaje tiene que decir, en una
línea, el resultado del gate (N/M checks OK).
"""
    else:  # review
        body = f"""\
Sos el REVISOR. No implementás; dictaminás. Sé escéptico: tu trabajo es encontrar
lo que el implementador rompió o simuló, no felicitarlo.

{common}

Spec que había que cumplir: {spec_path}

Tarea:
1. Mirá el diff real:
       cd "{PY_ROOT}" && git --no-pager diff --stat && git --no-pager diff
   (y `git status --porcelain` para los archivos nuevos, que no salen en el diff).
2. Verificá con tus propios ojos, no por lo que diga nadie:
   - ¿Se cumple el criterio de aceptación del spec?
   - ¿Los checks nuevos del gate PUEDEN fallar, o están escritos para pasar
     siempre? Rompé mentalmente el código y comprobá que el check lo detectaría.
   - ¿Sobrevivieron CORS en /ingest, la respuesta antes de preprocesar y el
     worker en hilo aparte? (§1)
   - ¿Se reusaron frd/signal_proc en vez de copiar fórmulas? (§0.4)
   - ¿Se tocó algo dentro de {REPO / 'data'}? Eso es motivo de FAIL inmediato.
   - ¿Quedó código muerto, o un archivo a medio portear que dice que anda?
3. Corré el gate vos mismo:
       cd "{PY_ROOT}" && {gate_cmd}
4. Escribí el veredicto en {review_path}:
   - Primera línea EXACTA, una de: `VERDICT: PASS` / `VERDICT: FAIL` /
     `VERDICT: NEEDS_FABLE` (esta última si el ítem necesita un modelo más
     fuerte, no si el implementador simplemente se equivocó).
   - Si es FAIL: lista numerada y accionable de qué arreglar. Ese texto se le pasa
     literal al próximo intento, así que escribilo para alguien sin contexto.
   - Si es PASS: una línea de resumen para el mensaje de commit.
"""
    path = PROMPTS / f"{item.iid}.{phase}.{attempt}.md"
    path.write_text(body, encoding="utf-8")
    return path


# ── Ejecución de claude con espera por límites ────────────────────────────────
def clean_env() -> dict:
    env = dict(os.environ)
    # Sin esto la CLI hija puede creerse anidada en esta sesión.
    for key in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SSE_PORT"):
        env.pop(key, None)
    return env


def parse_reset_ts(blob: str) -> tuple[float, str] | None:
    """Saca de qué hora habla el mensaje de límite. Devuelve (timestamp, motivo).

    Dos formatos, en orden de confiabilidad: el epoch que a veces trae la CLI, y
    la hora de reloj del mensaje de sesión ("resets 3:00am"). La hora de reloj se
    interpreta en la zona local de la máquina y, si ya pasó, se toma la próxima
    vuelta del reloj.
    """
    m = LIMIT_EPOCH.search(blob)
    if m:
        epoch = float(m.group(1))
        if epoch > 1e12:
            epoch /= 1000
        if 0 < epoch - time.time() <= MAX_LIMIT_WAIT_S:
            return epoch, "epoch informado por la CLI"

    m = LIMIT_CLOCK.search(blob)
    if not m:
        return None
    if m.group(1):
        hour, minute, half = int(m.group(1)), int(m.group(2) or 0), m.group(3).lower()
        if half == "p" and hour != 12:
            hour += 12
        if half == "a" and hour == 12:
            hour = 0
    else:
        hour, minute = int(m.group(4)), int(m.group(5))
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return None
    now_local = datetime.now()
    target = now_local.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now_local:
        target += timedelta(days=1)
    ts = target.timestamp()
    if ts - time.time() > MAX_LIMIT_WAIT_S:
        return None
    return ts, f"reseteo anunciado a las {target.strftime('%H:%M')}"


def sleep_until(ts: float, why: str) -> None:
    """Duerme hasta ``ts``, en tramos, publicando el latido en status.json.

    Nunca duerme más de SLEEP_CHUNK_S de una sola vez: si la hora parseada
    estuviera mal, al despertar se reintenta y se vuelve a leer el mensaje real
    en vez de quedarse dormido un día entero.
    """
    ts = min(ts, time.time() + SLEEP_CHUNK_S)
    hora = datetime.fromtimestamp(ts)
    log(f"límite de uso: espero hasta {hora.strftime('%d/%m %H:%M')} "
        f"({(ts - time.time()) / 60:.0f} min) — {why}")
    while True:
        left = ts - time.time()
        if left <= 0:
            log("límite: despierto y reintento la misma fase")
            return
        set_status(state="waiting_limit",
                   wait_until=hora.isoformat(timespec="seconds"), wait_reason=why)
        time.sleep(min(left, 300))


def run_claude(prompt_path: Path, model: str, phase: str, item: Item,
               attempt: int, state: dict, artifact: Path | None = None) -> dict:
    """Lanza una fase. Reintenta indefinidamente si el bloqueo es por límite.

    ``artifact`` es el entregable de la fase (el .md de spec o de review). Si el
    proceso muere por límite pero el archivo ya está escrito, la fase se da por
    hecha: rehacerla sería pagar dos veces el mismo trabajo.
    """
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    cmd = [CLAUDE, "-p", f"Leé {prompt_path} y hacé exactamente lo que dice.",
           "--model", model, "--dangerously-skip-permissions",
           "--output-format", "json", "--add-dir", str(REPO)]
    limit_hits = 0
    while True:
        set_status(state="running", item=item.iid, phase=phase, model=model,
                   attempt=attempt, wait_until=None, wait_reason=None,
                   prompt=str(prompt_path))
        log(f"[{item.iid}/{phase}] intento {attempt} con {model}")
        started = time.time()
        try:
            done = subprocess.run(cmd, cwd=str(REPO), env=clean_env(),
                                  capture_output=True, text=True,
                                  timeout=PHASE_TIMEOUT_S[phase])
            out, err, rc = done.stdout, done.stderr, done.returncode
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout or ""
            err = f"TIMEOUT tras {PHASE_TIMEOUT_S[phase]}s"
            rc = 124
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        if isinstance(err, bytes):
            err = err.decode("utf-8", "replace")

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        (RAW_OUT / f"{item.iid}.{phase}.{attempt}.{stamp}.json").write_text(
            (out or "") + ("\n--- stderr ---\n" + err if err else ""), encoding="utf-8")

        payload: dict = {}
        try:
            payload = json.loads(out)
        except (json.JSONDecodeError, TypeError):
            pass
        cost = float(payload.get("total_cost_usd") or 0.0)
        state["cost_usd"] = round(state.get("cost_usd", 0.0) + cost, 4)
        save_state(state)
        set_status(cost_usd=state["cost_usd"])

        blob = f"{out}\n{err}"
        is_error = bool(payload.get("is_error")) or rc != 0
        # La CLI marca el límite de forma estructurada; es más confiable que el
        # texto. Caso real medido: api_error_status=429 con
        # result="You've hit your session limit · resets 11:20pm (America/Asuncion)".
        es_limite = payload.get("api_error_status") == 429 or bool(LIMIT_GENERIC.search(blob))

        if FATAL_AUTH.search(blob):
            log("FATAL: problema de autenticación/crédito. El loop para; "
                "hace falta un humano.")
            return {"ok": False, "fatal": True, "text": blob[-2000:]}

        if is_error and es_limite:
            # Un límite NO es un intento fallido: no gasta intento ni escala de
            # modelo. Pero si la fase ya había dejado su entregable antes de
            # chocarse con el límite, se acepta en vez de pagarla de nuevo.
            if artifact is not None and artifact.is_file() and artifact.stat().st_size > 0:
                log(f"[{item.iid}/{phase}] llegó el límite DESPUÉS de escribir "
                    f"{artifact.name}; lo tomo como hecho y sigo")
                return {"ok": True, "fatal": False, "text": "(entregable ya escrito)"}
            reset = parse_reset_ts(blob)
            if reset:
                sleep_until(reset[0] + 90, reset[1])
            else:
                wait = LIMIT_BACKOFF_S[min(limit_hits, len(LIMIT_BACKOFF_S) - 1)]
                sleep_until(time.time() + wait,
                            f"backoff {wait // 60} min (el mensaje no dijo la hora)")
            limit_hits += 1
            continue                       # misma fase, sin gastar un intento

        elapsed = time.time() - started
        log(f"[{item.iid}/{phase}] terminó en {elapsed / 60:.1f} min "
            f"(rc={rc}, error={is_error}, costo acumulado ${state['cost_usd']:.2f})")
        return {"ok": not is_error, "fatal": False,
                "text": (payload.get("result") or blob)[-4000:]}


# ── Gate y git ────────────────────────────────────────────────────────────────
def run_gate(item: Item) -> tuple[bool, str]:
    GATE_OUT.mkdir(parents=True, exist_ok=True)
    out_json = GATE_OUT / f"{item.iid}.json"
    cmd = [sys.executable, str(GATE), "--only", "base",
           "--only", item.gate_prefix, "--require", item.gate_prefix,
           "--json", str(out_json)]
    try:
        done = subprocess.run(cmd, cwd=str(PY_ROOT), capture_output=True,
                              text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return False, "el gate no terminó en 30 min"
    tail = (done.stdout or "")[-1500:] + (done.stderr or "")[-500:]
    return done.returncode == 0, tail


def git(args: list[str], cwd: Path) -> tuple[int, str]:
    done = subprocess.run(["git"] + args, cwd=str(cwd), capture_output=True, text=True)
    return done.returncode, (done.stdout or "") + (done.stderr or "")


def commit_item(item: Item, summary: str) -> str:
    """Commitea en el submódulo y sube el gitlink en el superproyecto.

    Sin push, por decisión explícita. Se verifica que el submódulo NO esté en
    detached HEAD: commitear ahí deja el trabajo colgado de ningún branch.
    """
    rc, branch = git(["rev-parse", "--abbrev-ref", "HEAD"], PY_ROOT)
    branch = branch.strip()
    if rc != 0 or branch == "HEAD":
        return f"NO COMMITEADO: el submódulo está en detached HEAD ({branch!r})"
    msg = f"port: {item.title}\n\n{summary.strip()[:600]}\n\nÍtem {item.iid} del PORT_PLAN; gate verde."
    git(["add", "-A"], PY_ROOT)
    rc, out = git(["commit", "-m", msg], PY_ROOT)
    if rc != 0 and "nothing to commit" not in out:
        return f"commit del submódulo falló: {out[-300:]}"
    sub_sha = git(["rev-parse", "--short", "HEAD"], PY_ROOT)[1].strip()
    git(["add", "src/interfaces/python", "scripts/autonomia", "DUDAS_LUNES.md"], REPO)
    git(["commit", "-m", f"port: {item.title} (submódulo {sub_sha})"], REPO)
    return f"commiteado en {branch} ({sub_sha})"


def append_dudas(text: str) -> None:
    DUDAS.parent.mkdir(parents=True, exist_ok=True)
    header = "" if DUDAS.is_file() else (
        "# Dudas y bloqueos del porteo automático\n\n"
        "Escrito por el loop y por los modelos que corrieron sin supervisión.\n"
        "Se lee el lunes, en orden.\n")
    with DUDAS.open("a", encoding="utf-8") as fh:
        if header:
            fh.write(header)
        fh.write(f"\n## {now()}\n\n{text}\n")


def first_line_verdict(path: Path) -> str:
    if not path.is_file():
        return "MISSING"
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line:
            up = line.upper()
            if "NEEDS_FABLE" in up:
                return "NEEDS_FABLE"
            if "PASS" in up:
                return "PASS"
            if "FAIL" in up:
                return "FAIL"
            if "SPEC_READY" in up:
                return "SPEC_READY"
            return up[:40]
    return "EMPTY"


# ── Loop ──────────────────────────────────────────────────────────────────────
def model_for_attempt(attempt: int, forced_fable: bool) -> str:
    if forced_fable or attempt >= MAX_ATTEMPTS:
        return MODEL_HEAVY
    return MODEL_WORKER


def do_item(item: Item, state: dict) -> bool:
    entry = state["items"][item.iid]
    SPECS.mkdir(parents=True, exist_ok=True)
    REVIEWS.mkdir(parents=True, exist_ok=True)
    forced_fable = False

    # ── spec (advisor) ────────────────────────────────────────────────────────
    spec_path = SPECS / f"{item.iid}.md"
    if not spec_path.is_file():
        entry["phase"] = "spec"
        save_state(state)
        res = run_claude(write_prompt(item, "spec", MODEL_ADVISOR, 1),
                         MODEL_ADVISOR, "spec", item, 1, state, artifact=spec_path)
        if res.get("fatal"):
            return False
        verdict = first_line_verdict(spec_path)
        entry["history"].append({"phase": "spec", "model": MODEL_ADVISOR,
                                 "verdict": verdict, "at": now()})
        if verdict == "MISSING":
            log(f"[{item.iid}] el advisor no escribió el spec; reintento con {MODEL_HEAVY}")
            res = run_claude(write_prompt(item, "spec", MODEL_HEAVY, 2),
                             MODEL_HEAVY, "spec", item, 2, state, artifact=spec_path)
            if res.get("fatal") or not spec_path.is_file():
                entry["status"] = "blocked"
                save_state(state)
                append_dudas(f"**[{item.iid}] {item.title}** — no se pudo ni "
                             f"escribir el spec. Ver {RAW_OUT}.")
                return False
            verdict = first_line_verdict(spec_path)
        if verdict == "NEEDS_FABLE":
            forced_fable = True
            log(f"[{item.iid}] el advisor pidió Fable para implementar")

    # ── impl + review, con escalado ───────────────────────────────────────────
    feedback = ""
    while entry["attempts"] < MAX_ATTEMPTS:
        entry["attempts"] += 1
        attempt = entry["attempts"]
        model = model_for_attempt(attempt, forced_fable)
        if model == MODEL_HEAVY:
            log(f"[{item.iid}] ESCALADO A FABLE (intento {attempt})")
        entry["phase"], entry["model"], entry["status"] = "impl", model, "running"
        save_state(state)

        res = run_claude(write_prompt(item, "impl", model, attempt, feedback),
                         model, "impl", item, attempt, state)
        if res.get("fatal"):
            return False

        gate_ok, gate_tail = run_gate(item)
        log(f"[{item.iid}] gate {'VERDE' if gate_ok else 'ROJO'} tras intento {attempt}")
        entry["history"].append({"phase": "impl", "model": model, "attempt": attempt,
                                 "gate_ok": gate_ok, "at": now()})
        save_state(state)

        if not gate_ok:
            feedback = ("El gate quedó ROJO. Salida del gate:\n\n" + gate_tail +
                        "\n\nArreglá lo que falla sin debilitar los checks.")
            continue

        entry["phase"] = "review"
        save_state(state)
        review_path = REVIEWS / f"{item.iid}.md"
        if review_path.is_file():
            review_path.unlink()
        res = run_claude(write_prompt(item, "review", MODEL_ADVISOR, attempt),
                         MODEL_ADVISOR, "review", item, attempt, state,
                         artifact=review_path)
        if res.get("fatal"):
            return False
        verdict = first_line_verdict(review_path)
        review_text = (review_path.read_text(encoding="utf-8", errors="replace")
                       if review_path.is_file() else "(sin archivo de review)")
        entry["history"].append({"phase": "review", "model": MODEL_ADVISOR,
                                 "attempt": attempt, "verdict": verdict, "at": now()})
        log(f"[{item.iid}] veredicto: {verdict}")

        if verdict == "PASS":
            entry["status"] = "done"
            entry["phase"] = None
            note = commit_item(item, review_text)
            entry["commit"] = note
            log(f"[{item.iid}] {note}")
            save_state(state)
            return True
        if verdict == "NEEDS_FABLE":
            forced_fable = True
        feedback = review_text
        save_state(state)

    entry["status"] = "blocked"
    entry["phase"] = None
    save_state(state)
    append_dudas(
        f"**[{item.iid}] {item.title}** — BLOQUEADO tras {MAX_ATTEMPTS} intentos "
        f"(el último con {MODEL_HEAVY}).\n\n"
        f"- Spec: `{SPECS / (item.iid + '.md')}`\n"
        f"- Última revisión: `{REVIEWS / (item.iid + '.md')}`\n"
        f"- Transcripciones: `{RAW_OUT}`\n\n"
        f"Último feedback del revisor:\n\n```\n{feedback[:2000]}\n```\n\n"
        f"El loop paró acá a propósito: arrastrar esto a los ítems siguientes "
        f"era peor que no avanzar.")
    return False


def print_status() -> int:
    if not STATE_FILE.is_file():
        print("todavía no arrancó (no hay port_state.json)")
        return 1
    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    st = json.loads(STATUS_FILE.read_text(encoding="utf-8")) if STATUS_FILE.is_file() else {}
    print(f"=== PORT LOOP — {now()} ===")
    print(f"alcance : {state.get('scope')}")
    print(f"costo   : ${state.get('cost_usd', 0):.2f} acumulados")
    print(f"estado  : {st.get('state')}  item={st.get('item')} fase={st.get('phase')} "
          f"modelo={st.get('model')} intento={st.get('attempt')}")
    if st.get("state") == "waiting_limit":
        print(f"          ESPERANDO LÍMITE hasta {st.get('wait_until')} "
              f"({st.get('wait_reason')})")
    print(f"latido  : {st.get('updated')}  pid={st.get('pid')}")
    print("\nítems:")
    for item in ITEMS:
        e = state["items"][item.iid]
        mark = {"done": "OK  ", "blocked": "STOP", "running": ">>  ",
                "pending": "... "}.get(e["status"], "?   ")
        print(f"  {mark} {item.iid:16s} {e['status']:8s} intentos={e['attempts']} "
              f"{e.get('commit', '')}")
    fables = [h for item in ITEMS for h in state["items"][item.iid]["history"]
              if h.get("model") == MODEL_HEAVY]
    if fables:
        print(f"\nescalados a Fable: {len(fables)}")
    if DUDAS.is_file():
        print(f"\ndudas anotadas para el lunes: {DUDAS}")
    if LOG_FILE.is_file():
        print("\n--- últimas 12 líneas del log ---")
        for line in LOG_FILE.read_text(encoding="utf-8",
                                       errors="replace").splitlines()[-12:]:
            print("  " + line)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--reset-item", help="volver un ítem a pending y borrar su spec")
    ap.add_argument("--only-item", help="correr sólo este ítem")
    args = ap.parse_args()

    if args.status:
        return print_status()

    state = load_state()

    if args.reset_item:
        iid = args.reset_item
        if iid not in state["items"]:
            print(f"ítem desconocido {iid}", file=sys.stderr)
            return 2
        state["items"][iid] = {"status": "pending", "attempts": 0, "phase": None,
                               "model": None, "history": []}
        for p in (SPECS / f"{iid}.md", REVIEWS / f"{iid}.md"):
            if p.is_file():
                p.unlink()
        save_state(state)
        print(f"{iid} reseteado")
        return 0

    todo = [i for i in ITEMS if state["items"][i.iid]["status"] not in ("done",)]
    if args.only_item:
        todo = [i for i in todo if i.iid == args.only_item]

    if args.dry_run:
        print(f"repo      : {REPO}")
        print(f"claude    : {CLAUDE}")
        print(f"gate      : {GATE}")
        print(f"modelos   : advisor={MODEL_ADVISOR} worker={MODEL_WORKER} "
              f"emergencia={MODEL_HEAVY} (sólo por escalado)")
        print(f"estado    : {STATE_FILE}")
        print(f"dudas     : {DUDAS}")
        print("\nfases por ítem: spec(opus) -> impl(sonnet) -> review(opus), "
              "con commit al PASS")
        print("\npendientes:")
        for i in todo:
            print(f"  - {i.iid:16s} {i.title}   gate: base + {i.gate_prefix}")
        if not todo:
            print("  (nada: todo done)")
        return 0

    if not todo:
        log("nada pendiente: todos los ítems del alcance están done")
        set_status(state="done", item=None, phase=None)
        return 0

    if not acquire_lock():
        return 3

    try:
        return run_all(todo, state)
    finally:
        release_lock()


def run_all(todo: list[Item], state: dict) -> int:
    log(f"=== arranca el loop; pendientes: {[i.iid for i in todo]} ===")
    set_status(state="running")
    for item in todo:
        ok = do_item(item, state)
        if not ok:
            log(f"=== el loop PARA en [{item.iid}] — hace falta un humano ===")
            set_status(state="blocked", item=item.iid)
            return 1
    log("=== alcance completo: §1 + §3.1 portados y commiteados ===")
    set_status(state="done", item=None, phase=None)
    append_dudas(
        "**Alcance completo.** §1 (refactor FastAPI) y §3.1 (Capturas con pick "
        "editable) quedaron con gate verde y commiteados sin push. Lo que sigue "
        "según el plan: §3.2 Filtros/Enfase, §3.3 Agrupamiento/Promedios, "
        "§3.4 Waterfall, §3.5 MASW, §4 ventana de Borrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
