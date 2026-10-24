"""OTA de un esclavo a traves del maestro (http://192.168.4.1/ota/*).

Cada imagen lleva su NODE_ID compilado: se graba de a un nodo con su .bin.

  python lab/s3/ota.py --node 2 --bin C:/piobuild/slaveS3/slaveS3_2/firmware.bin
  python lab/s3/ota.py --node 2 --env slaveS3_2      (usa el build de pio)
"""
import argparse
import json
import sys
import time
import urllib.request
import uuid

BASE = 'http://192.168.4.1'
STATES = ['inactivo', 'asociandose', 'descargando', 'verificando', 'reiniciando',
          'sin confirmar', 'confirmado', 'fallo']


def http(method, path, body=None, headers=None, timeout=60):
    req = urllib.request.Request(BASE + path, data=body, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode('utf-8', 'replace')


def upload(path):
    data = open(path, 'rb').read()
    b = uuid.uuid4().hex
    body = (f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="slave.bin"\r\n'
            'Content-Type: application/octet-stream\r\n\r\n').encode() + data + f'\r\n--{b}--\r\n'.encode()
    t = time.time()
    st, txt = http('POST', '/ota/upload', body,
                   {'Content-Type': f'multipart/form-data; boundary={b}'}, timeout=180)
    print(f'subida {len(data)} B en {time.time() - t:.1f} s -> {st} {txt[:200]}')
    return st == 200


def status():
    return json.loads(http('GET', '/ota/status', timeout=10)[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--node', type=int, required=True)
    ap.add_argument('--bin')
    ap.add_argument('--env')
    ap.add_argument('--timeout', type=float, default=300)
    a = ap.parse_args()
    path = a.bin or f'C:/piobuild/slaveS3/{a.env}/firmware.bin'
    if not upload(path):
        sys.exit(2)
    print('imagen:', status().get('image'))
    print('start ->', http('POST', f'/ota/start?node={a.node}', b'')[1][:200])
    t0 = time.time()
    last = None
    while time.time() - t0 < a.timeout:
        time.sleep(2)
        try:
            s = status()
        except Exception as e:
            print('status error', e)
            continue
        nd = next((n for n in s.get('nodes', []) if n.get('node') == a.node), None)
        txt = json.dumps(nd)
        if txt != last:
            st = nd.get('state') if nd else None
            nombre = STATES[st] if isinstance(st, int) and st < len(STATES) else st
            print(f'{time.time() - t0:6.1f} s  {nombre}  {txt}')
            last = txt
        if nd and nd.get('state') in (6, 7):
            sys.exit(0 if nd['state'] == 6 else 1)
    print('timeout')
    sys.exit(3)


if __name__ == '__main__':
    main()
