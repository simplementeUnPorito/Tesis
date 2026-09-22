"""Invoca Codex solamente ante una alerta critica nueva del barrido.

El sondeo y la recuperacion normal no consumen tokens. Cada contenido distinto
de alert.json se entrega una sola vez a Codex y luego se archiva, aun si Codex
falla, para evitar bucles costosos.
"""
import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import time


STOP = False


def atomic_json(path, payload):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def now_text():
    return time.strftime('%Y-%m-%dT%H:%M:%S%z')


def stop_handler(_signum, _frame):
    global STOP
    STOP = True


def arguments(argv):
    p = argparse.ArgumentParser(description='Operador Codex por excepcion')
    p.add_argument('--repo', required=True)
    p.add_argument('--codex-bin', required=True)
    p.add_argument('--poll-s', type=int, default=15)
    p.add_argument('--timeout-s', type=int, default=1800)
    return p.parse_args(argv)


def read_last_hash(path):
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            value = json.load(fh)
        return value.get('last_hash')
    except (FileNotFoundError, OSError, ValueError, TypeError):
        return None


def main(argv=None):
    ns = arguments(argv if argv is not None else sys.argv[1:])
    repo = os.path.abspath(ns.repo)
    run_dir = os.path.join(repo, 'lab', 'barrido_total', '.run')
    alert_path = os.path.join(run_dir, 'alert.json')
    state_path = os.path.join(run_dir, 'codex_operator.json')
    result_path = os.path.join(run_dir, 'codex_last_result.txt')
    guide_path = os.path.join(repo, 'lab', 'CODEX_OPERADOR_BARRIDO.md')
    os.makedirs(run_dir, exist_ok=True)
    last_hash = read_last_hash(state_path)

    while not STOP:
        try:
            with open(alert_path, 'rb') as fh:
                alert_raw = fh.read(65536)
        except FileNotFoundError:
            time.sleep(ns.poll_s)
            continue
        except OSError as exc:
            atomic_json(state_path, {
                'status': 'watch_error', 'updated': now_text(),
                'error': str(exc), 'last_hash': last_hash,
            })
            time.sleep(ns.poll_s)
            continue

        alert_hash = hashlib.sha256(alert_raw).hexdigest()
        if alert_hash == last_hash:
            time.sleep(ns.poll_s)
            continue

        prompt = (
            'Actua como operario por excepcion del barrido de ganancias. '
            'Trabaja exclusivamente en %s. Lee primero %s y respeta sus '
            'limites. Hay una alerta critica nueva en '
            'lab/barrido_total/.run/alert.json. Diagnostica la causa usando '
            'health.json, resultados y journalctl --user cuando sea necesario. '
            'Aplica solo una recuperacion segura, reversible y dentro del '
            'procedimiento documentado. No cambies ningun pin, firmware, '
            'ganancia, criterio de prueba ni archivo ajeno. No hagas commit ni '
            'push. Si falta hardware o hace falta una decision humana, no '
            'improvises: dejalo explicado en tu respuesta final. Alerta:\n%s'
            % (repo, guide_path, alert_raw.decode('utf-8', errors='replace'))
        )
        atomic_json(state_path, {
            'status': 'invoking_codex', 'updated': now_text(),
            'alert_hash': alert_hash, 'last_hash': last_hash,
        })
        command = [
            ns.codex_bin, 'exec', '-C', repo, '--sandbox', 'workspace-write',
            '--ask-for-approval', 'never', '--color', 'never',
            '--output-last-message', result_path, '-',
        ]
        rc = None
        error = None
        try:
            completed = subprocess.run(
                command, input=prompt, text=True, stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE, timeout=ns.timeout_s, check=False,
            )
            rc = completed.returncode
            if rc != 0:
                error = (completed.stderr or '')[-4000:]
        except (OSError, subprocess.TimeoutExpired) as exc:
            error = str(exc)

        last_hash = alert_hash
        archive = os.path.join(
            run_dir, 'alert.handled-%s-%s.json'
            % (time.strftime('%Y%m%dT%H%M%S'), alert_hash[:12]))
        try:
            with open(alert_path, 'rb') as fh:
                current_hash = hashlib.sha256(fh.read(65536)).hexdigest()
            if current_hash == alert_hash:
                os.replace(alert_path, archive)
        except FileNotFoundError:
            pass
        atomic_json(state_path, {
            'status': 'handled' if rc == 0 else 'codex_error',
            'updated': now_text(), 'last_hash': last_hash,
            'returncode': rc, 'error': error, 'archived_alert': archive,
            'result': result_path,
        })
    return 0


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)
    raise SystemExit(main())
