"""Supervisor sin IA para el barrido de ganancias.

Reinicia fallos transitorios con backoff, conserva la reanudacion del barrido y
solo crea ``alert.json`` cuando agota todas las recuperaciones automaticas.
Codex puede consultar ese archivo compacto sin leer el log completo.
"""
import argparse
import atexit
import collections
import glob
import json
import os
import signal
import subprocess
import sys
import time


STOP = False
CHILD = None


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
    if CHILD is not None and CHILD.poll() is None:
        CHILD.terminate()


def arguments(argv):
    p = argparse.ArgumentParser(description='Supervisor local del barrido')
    p.add_argument('repeticiones', nargs='?', type=int, default=3)
    p.add_argument('ventana_s', nargs='?', type=int, default=240)
    p.add_argument('--port', default='auto')
    p.add_argument('--output', required=True)
    p.add_argument('--max-restarts', type=int, default=8)
    p.add_argument('--pid-file', default=None,
                   help='archivo opcional con el PID del supervisor')
    p.add_argument('--stable-reset-s', type=int, default=900,
                   help='tras este tiempo vivo, un fallo vuelve a contar desde 1')
    return p.parse_args(argv)


def detect_port(requested):
    if requested and requested != 'auto':
        return requested if os.path.exists(requested) else None
    candidates = sorted(glob.glob('/dev/serial/by-id/*'))
    candidates += sorted(glob.glob('/dev/ttyUSB*'))
    candidates += sorted(glob.glob('/dev/ttyACM*'))
    return candidates[0] if candidates else None


def main(argv=None):
    global CHILD
    ns = arguments(argv if argv is not None else sys.argv[1:])
    output = os.path.abspath(ns.output)
    run_dir = os.path.join(output, '.run')
    health_path = os.path.join(run_dir, 'health.json')
    alert_path = os.path.join(run_dir, 'alert.json')
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          'barrido_total.py')
    os.makedirs(run_dir, exist_ok=True)
    if ns.pid_file:
        pid_file = os.path.abspath(ns.pid_file)
        os.makedirs(os.path.dirname(pid_file), exist_ok=True)
        with open(pid_file, 'w', encoding='ascii') as fh:
            fh.write('%d\n' % os.getpid())

        def remove_own_pid_file():
            try:
                with open(pid_file, 'r', encoding='ascii') as fh:
                    if fh.read().strip() == str(os.getpid()):
                        os.unlink(pid_file)
            except (FileNotFoundError, OSError):
                pass

        atexit.register(remove_own_pid_file)

    failures = 0
    backoffs = [15, 30, 60, 120, 300, 600]
    tail = collections.deque(maxlen=30)
    while not STOP:
        port = detect_port(ns.port)
        if port is None:
            atomic_json(health_path, {
                'status': 'waiting_for_device', 'updated': now_text(),
                'restart_count': failures, 'requested_port': ns.port,
            })
            time.sleep(10)
            continue
        command = [sys.executable, '-u', script,
                   str(ns.repeticiones), str(ns.ventana_s),
                   '--reanudar', '--reintentar-invalidas',
                   '--port', port, '--output', output]
        started = time.time()
        atomic_json(health_path, {
            'status': 'starting', 'updated': now_text(),
            'restart_count': failures, 'port': port,
        })
        CHILD = subprocess.Popen(command, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, text=True,
                                 encoding='utf-8', errors='replace', bufsize=1)
        atomic_json(health_path, {
            'status': 'running', 'updated': now_text(),
            'child_pid': CHILD.pid, 'restart_count': failures,
            'port': port, 'output': output,
        })
        assert CHILD.stdout is not None
        for line in CHILD.stdout:
            print(line, end='', flush=True)
            tail.append(line.rstrip())
        rc = CHILD.wait()
        lived = time.time() - started
        CHILD = None

        if STOP:
            atomic_json(health_path, {
                'status': 'stopped_by_operator', 'updated': now_text(),
                'restart_count': failures, 'last_returncode': rc,
            })
            return 0
        if rc == 0:
            atomic_json(health_path, {
                'status': 'complete', 'updated': now_text(),
                'restart_count': failures, 'last_returncode': rc,
            })
            return 0

        failures = 1 if lived >= ns.stable_reset_s else failures + 1
        if failures > ns.max_restarts:
            alert = {
                'severity': 'critical',
                'requires_codex': True,
                'kind': 'automatic_recovery_exhausted',
                'message': ('El barrido agoto %d reinicios automaticos; '
                            'requiere diagnostico del operario.'
                            % ns.max_restarts),
                'returncode': rc,
                'last_output': list(tail),
                'created': now_text(),
            }
            atomic_json(alert_path, alert)
            atomic_json(health_path, {
                'status': 'needs_operator', 'updated': now_text(),
                'restart_count': failures - 1, 'last_returncode': rc,
                'alert': alert_path,
            })
            print('ALERTA CRITICA: %s' % alert['message'], flush=True)
            return rc or 1

        delay = backoffs[min(failures - 1, len(backoffs) - 1)]
        atomic_json(health_path, {
            'status': 'recovering', 'updated': now_text(),
            'restart_count': failures, 'last_returncode': rc,
            'retry_in_s': delay,
        })
        print('recuperacion automatica %d/%d en %d s'
              % (failures, ns.max_restarts, delay), flush=True)
        deadline = time.time() + delay
        while not STOP and time.time() < deadline:
            time.sleep(min(1.0, deadline - time.time()))
    return 0


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)
    raise SystemExit(main())
