#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
RUN_DIR="${BARRIDO_RUN_DIR:-$SCRIPT_DIR/barrido_total/.run}"
VENV_DIR="${BARRIDO_VENV:-$REPO_DIR/.venv-barrido}"
PID_FILE="$RUN_DIR/pid"
LOG_FILE="$RUN_DIR/barrido.log"

is_running() {
    [[ -f "$PID_FILE" ]] || return 1
    local pid
    pid="$(<"$PID_FILE")"
    [[ "$pid" =~ ^[0-9]+$ ]] && kill -0 "$pid" 2>/dev/null
}

setup() {
    command -v python3 >/dev/null || { echo "Falta python3" >&2; exit 2; }
    if [[ ! -x "$VENV_DIR/bin/python" ]]; then
        python3 -m venv "$VENV_DIR"
    fi
    "$VENV_DIR/bin/python" -m pip install -q -r "$SCRIPT_DIR/requirements-barrido.txt"
    mkdir -p "$RUN_DIR"
}

start() {
    setup
    if is_running; then
        echo "Ya esta corriendo (PID $(<"$PID_FILE"))."
        exit 0
    fi
    local port repetitions window
    port="${BARRIDO_PORT:-auto}"
    repetitions="${1:-3}"
    window="${2:-240}"
    rm -f "$RUN_DIR/alert.json"
    nohup "$VENV_DIR/bin/python" -u "$SCRIPT_DIR/barrido_supervisor.py" \
        "$repetitions" "$window" --port "$port" \
        --output "$SCRIPT_DIR/barrido_total" --pid-file "$PID_FILE" \
        >>"$LOG_FILE" 2>&1 &
    echo "$!" >"$PID_FILE"
    sleep 1
    if ! is_running; then
        echo "El barrido no arranco; revise $LOG_FILE" >&2
        tail -n 30 "$LOG_FILE" >&2 || true
        exit 1
    fi
    echo "Barrido iniciado: PID $(<"$PID_FILE"), puerto $port"
    echo "Log: $LOG_FILE"
}

status() {
    if is_running; then
        echo "RUNNING PID $(<"$PID_FILE")"
        tail -n 5 "$LOG_FILE" 2>/dev/null || true
    else
        echo "STOPPED"
        [[ -f "$LOG_FILE" ]] && tail -n 10 "$LOG_FILE" || true
        return 1
    fi
}

operator_status() {
    local alert="$RUN_DIR/alert.json"
    local health="$RUN_DIR/health.json"
    if [[ -s "$alert" ]]; then
        printf 'ALERT '
        tr -d '\n' <"$alert"
        printf '\n'
        return 2
    fi
    if is_running; then
        printf 'OK '
        [[ -s "$health" ]] && tr -d '\n' <"$health" || printf '{"status":"starting"}'
        printf '\n'
        return 0
    fi
    if [[ -s "$health" ]] && grep -q '"status": "complete"' "$health"; then
        printf 'COMPLETE '
        tr -d '\n' <"$health"
        printf '\n'
        return 0
    fi
    printf 'ALERT {"severity":"critical","kind":"supervisor_not_running","message":"El supervisor no esta corriendo y el barrido no figura completo."}\n'
    return 2
}

stop() {
    if ! is_running; then
        echo "No esta corriendo."
        return 0
    fi
    local pid
    pid="$(<"$PID_FILE")"
    kill -TERM "$pid"
    for _ in {1..20}; do
        kill -0 "$pid" 2>/dev/null || { rm -f "$PID_FILE"; echo "Detenido."; return; }
        sleep 0.5
    done
    echo "No termino tras 10 s; PID $pid sigue vivo." >&2
    return 1
}

case "${1:-}" in
    setup) setup ;;
    start) shift; start "$@" ;;
    status) status ;;
    operator) operator_status ;;
    log) setup; touch "$LOG_FILE"; tail -F "$LOG_FILE" ;;
    stop) stop ;;
    restart) shift; stop; start "$@" ;;
    *) echo "Uso: $0 {setup|start [vueltas] [ventana_s]|status|operator|log|stop|restart}" >&2; exit 2 ;;
esac
