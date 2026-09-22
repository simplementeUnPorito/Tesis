#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
CODEX_BIN="${CODEX_BIN:-$HOME/.local/bin/codex}"
USER_UNITS="$HOME/.config/systemd/user"

[[ -x "$CODEX_BIN" ]] || { echo "No existe Codex en $CODEX_BIN" >&2; exit 2; }
"$SCRIPT_DIR/barrido_total.sh" setup
mkdir -p "$USER_UNITS" "$SCRIPT_DIR/barrido_total/.run"

for template in "$SCRIPT_DIR"/systemd/*.service.in; do
    target="$USER_UNITS/$(basename "${template%.in}")"
    sed -e "s|@REPO@|$REPO_DIR|g" -e "s|@CODEX@|$CODEX_BIN|g" \
        "$template" >"$target"
done

systemctl --user daemon-reload
systemctl --user enable codex-remote-control.service \
    barrido-total.service barrido-codex-operator.service
echo "Servicios instalados. Inicie con:"
echo "  systemctl --user start codex-remote-control.service barrido-total.service barrido-codex-operator.service"
