"""banco.py - UN solo programa para correr el banco toda la noche.

Antes esto eran tres procesos sueltos -el experimento, el registrador de
temperatura y el operador- que habia que lanzar y matar por separado, con sus
tres PIDs y sus tres logs. Se perdia uno y nadie se enteraba: el registrador
de temperatura murio en silencio la primera noche y el dato termico quedo en
una sola fila.

Aca es un proceso con tres hilos:

    principal    el experimento (dueno exclusivo del puerto serie)
    temperatura  una fila cada N minutos al CSV de la campana
    vigilante    si el experimento deja de escribir visitas, llama a codex

Si el proceso muere, muere entero y se nota. Si un hilo secundario falla, lo
dice y el experimento sigue: la temperatura es un extra, no un requisito.

Uso:

    python lab/banco.py --port COM8 --vueltas 4
    python lab/banco.py --port COM8 --vueltas 4 --reanudar

Se detiene sin perder nada con Ctrl-C o creando `.run/STOP` en la carpeta de
salida.
"""
import argparse
import os
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lab import experimento_semilla as exp    # noqa: E402
from lab import temperatura_ambiente as temp  # noqa: E402

CODEX = os.path.expandvars(
    r'%USERPROFILE%\.codex\plugins\.plugin-appserver\codex.exe')

# Techo de lo que puede tardar UNA visita: ventana de 240 s con prorroga hasta
# 960 s, mas la preparacion (reset y arranque, o asentamiento del contexto).
# Pasarlo no es lentitud, es un cuelgue.
LIMITE_ESTANCADO_S = 1500


def _log(msg):
    print('%s  %s' % (time.strftime('%H:%M:%S'), msg), flush=True)


# ------------------------------------------------------------- temperatura

def _hilo_temperatura(salida, cada_min, parar):
    """El nodo no tiene sensor propio; se usa el aire del lugar como proxy de
    la deriva lenta.  Es un extra: si falla, se dice y se sigue midiendo."""
    ruta = os.path.join(salida, 'temperatura.csv')
    nuevo = not os.path.exists(ruta)
    fallos = 0
    while not parar.is_set():
        try:
            t, grados, hum = temp.actual()
            with open(ruta, 'a', encoding='utf-8') as fh:
                if nuevo:
                    fh.write('utc,local,temp_C,humedad_pct\n')
                    nuevo = False
                fh.write('%s,%s,%s,%s\n'
                         % (t, time.strftime('%Y-%m-%dT%H:%M:%S'), grados, hum))
            fallos = 0
        except Exception as e:
            fallos += 1
            if fallos in (1, 10):        # avisa al primero y al decimo, no cada vez
                _log('[temp] sin dato (%r); se reintenta' % e)
        parar.wait(cada_min * 60)


# -------------------------------------------------------------- vigilante

def _visitas(crudo):
    if not os.path.exists(crudo):
        return 0
    with open(crudo, encoding='utf-8') as fh:
        return sum(1 for ln in fh if ln.strip())


def _llamar_codex(salida, motivo):
    prompt = (
        'Sos el operario de un banco de medicion que corre solo de noche.\n'
        'El programa es lab/banco.py sobre el puerto COM8, salida en %s.\n\n'
        'FALLO: %s\n\n'
        '1. Diagnostica leyendo esa carpeta y el jsonl de resultados.\n'
        '2. Aplica SOLO recuperaciones seguras: cebar la adquisicion con\n'
        '   startwait, o psocreset por GPIO19 si el PSoC quedo mudo.\n'
        '3. NO cambies pines, NO reflashees, NO borres resultados, NO toques\n'
        '   la tabla de puntos ni la politica.\n'
        '4. Terminá con RESUELTO o con NO_RESUELTO y el motivo.\n' % (salida, motivo))
    try:
        r = subprocess.run(
            [CODEX, 'exec', '--dangerously-bypass-approvals-and-sandbox',
             '-C', os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
             prompt],
            capture_output=True, text=True, timeout=1800)
        return (r.stdout or '') + (r.stderr or '')
    except Exception as e:
        return 'codex no pudo ejecutarse: %r' % e


def _hilo_vigilante(salida, parar):
    """No revisa por reloj: reacciona a que el progreso se detenga."""
    crudo = os.path.join(salida, 'resultados.jsonl')
    n, t_ultimo, intentos = _visitas(crudo), time.time(), 0
    while not parar.wait(30):
        actual = _visitas(crudo)
        if actual != n:
            n, t_ultimo, intentos = actual, time.time(), 0
            continue
        if time.time() - t_ultimo <= LIMITE_ESTANCADO_S:
            continue
        intentos += 1
        motivo = ('no se escribe una visita desde hace %d s (el techo de una '
                  'visita es %d s)' % (time.time() - t_ultimo, LIMITE_ESTANCADO_S))
        _log('[vigia] %s -> codex (intento %d)' % (motivo, intentos))
        r = _llamar_codex(salida, motivo)
        ok = 'RESUELTO' in r and 'NO_RESUELTO' not in r
        _log('[vigia] codex dice %s' % ('RESUELTO' if ok else 'NO_RESUELTO'))
        if ok and intentos < 3:
            t_ultimo = time.time()
            continue
        with open(os.path.join(salida, 'ALERTA_HUMANO.txt'), 'w',
                  encoding='utf-8') as fh:
            fh.write('motivo: %s\nintentos: %d\n\n%s\n' % (motivo, intentos, r[-4000:]))
        _log('[vigia] ESCALAMIENTO_HUMANO: ni el programa ni codex pudieron')
        return


# ------------------------------------------------------------------ arranque

def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--port')
    ap.add_argument('--output', default=exp.SALIDA_POR_OMISION)
    ap.add_argument('--politica', type=int, default=2)
    ap.add_argument('--vueltas', type=int, default=4)
    ap.add_argument('--ventana', type=int, default=240)
    ap.add_argument('--reanudar', action='store_true')
    ap.add_argument('--huerfanos', action='store_true')
    ap.add_argument('--sembrar', action='store_true')
    ap.add_argument('--pares', nargs='+')
    ap.add_argument('--temp-cada', type=int, default=10,
                    help='minutos entre lecturas de temperatura (0 = sin temp)')
    ap.add_argument('--sin-vigia', action='store_true',
                    help='no llamar a codex ante un estancamiento')
    a = ap.parse_args(argv)

    os.makedirs(os.path.join(a.output, '.run'), exist_ok=True)
    parar = threading.Event()
    hilos = []
    if a.temp_cada > 0:
        hilos.append(threading.Thread(target=_hilo_temperatura,
                                      args=(a.output, a.temp_cada, parar),
                                      daemon=True))
    if not a.sin_vigia:
        hilos.append(threading.Thread(target=_hilo_vigilante,
                                      args=(a.output, parar), daemon=True))
    for h in hilos:
        h.start()
    _log('banco arriba: experimento + %d hilo(s) de apoyo' % len(hilos))

    argv_exp = ['--politica', str(a.politica), '--vueltas', str(a.vueltas),
                '--ventana', str(a.ventana), '--output', a.output]
    if a.port:
        argv_exp += ['--port', a.port]
    if a.pares:
        argv_exp += ['--pares'] + list(a.pares)
    for bandera, nombre in ((a.reanudar, '--reanudar'),
                            (a.huerfanos, '--huerfanos'),
                            (a.sembrar, '--sembrar')):
        if bandera:
            argv_exp.append(nombre)
    try:
        return exp.main(argv_exp)
    finally:
        parar.set()
        _log('banco abajo')


if __name__ == '__main__':
    raise SystemExit(main())
