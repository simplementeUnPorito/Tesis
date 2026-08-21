"""Verifica que todas las interfaces históricas puedan levantarse sin un ESP32.

Cada versión se sirve en un puerto efímero mediante la misma aplicación FastAPI que
se usa para las capturas. Se comprueban la página principal, las rutas REST simuladas
y un intercambio WebSocket. El script no modifica los archivos históricos.
"""

from __future__ import annotations

import asyncio
import base64
import json
import os
import socket
import struct
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from serve_demo import available_versions, start_demo_server


def request_text(url: str, data: dict[str, str] | None = None) -> tuple[str, int]:
    """Realiza una solicitud HTTP pequeña sin agregar dependencias al proyecto."""

    encoded = None if data is None else urlencode(data).encode("utf-8")
    request = Request(url, data=encoded)
    try:
        with urlopen(request, timeout=5) as response:
            body = response.read()
    except HTTPError as error:
        raise RuntimeError(f"{url} devolvió HTTP {error.code}") from error
    return body.decode("utf-8"), len(body)


def receive_exact(connection: socket.socket, count: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < count:
        chunk = connection.recv(count - len(chunks))
        if not chunk:
            raise RuntimeError("El WebSocket se cerró antes de completar la trama")
        chunks.extend(chunk)
    return bytes(chunks)


def receive_ws_frame(connection: socket.socket) -> tuple[int, bytes]:
    first, second = receive_exact(connection, 2)
    opcode = first & 0x0F
    length = second & 0x7F
    if length == 126:
        length = struct.unpack("!H", receive_exact(connection, 2))[0]
    elif length == 127:
        length = struct.unpack("!Q", receive_exact(connection, 8))[0]
    mask = receive_exact(connection, 4) if second & 0x80 else None
    payload = bytearray(receive_exact(connection, length))
    if mask:
        for index in range(length):
            payload[index] ^= mask[index % 4]
    return opcode, bytes(payload)


def receive_ws_text(connection: socket.socket) -> str:
    """Devuelve la próxima trama textual, ignorando muestras binarias demo."""

    for _ in range(24):
        opcode, payload = receive_ws_frame(connection)
        if opcode == 0x1:
            return payload.decode("utf-8")
        if opcode == 0x8:
            raise RuntimeError("El WebSocket se cerró antes de la trama textual")
    raise RuntimeError("No llegó una trama textual tras 24 tramas WebSocket")


def send_ws_text(connection: socket.socket, text: str) -> None:
    payload = text.encode("utf-8")
    mask = os.urandom(4)
    if len(payload) < 126:
        header = bytes((0x81, 0x80 | len(payload)))
    elif len(payload) < 65536:
        header = bytes((0x81, 0x80 | 126)) + struct.pack("!H", len(payload))
    else:
        header = bytes((0x81, 0x80 | 127)) + struct.pack("!Q", len(payload))
    masked = bytes(value ^ mask[index % 4] for index, value in enumerate(payload))
    connection.sendall(header + mask + masked)


def websocket_exchange(port: int) -> tuple[dict[str, object], dict[str, object]]:
    key = base64.b64encode(os.urandom(16)).decode("ascii")
    request = (
        "GET /ws HTTP/1.1\r\n"
        f"Host: 127.0.0.1:{port}\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n\r\n"
    ).encode("ascii")

    with socket.create_connection(("127.0.0.1", port), timeout=5) as connection:
        connection.sendall(request)
        response = bytearray()
        while b"\r\n\r\n" not in response:
            response.extend(connection.recv(1))
        header, _ = bytes(response).split(b"\r\n\r\n", 1)
        if b" 101 " not in header.split(b"\r\n", 1)[0]:
            raise RuntimeError(f"Falló la negociación WebSocket: {header[:160]!r}")
        initial = json.loads(receive_ws_text(connection))
        send_ws_text(connection, '{"command":"status"}')
        acknowledgement = json.loads(receive_ws_text(connection))
    return initial, acknowledgement


async def verify_version(web_root) -> dict[str, object]:
    server = await start_demo_server(web_root, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]

    base = f"http://127.0.0.1:{port}"
    try:
        page_text, page_bytes = await asyncio.to_thread(request_text, f"{base}/")
        if "<html" not in page_text.lower():
            raise RuntimeError("La ruta / no devolvió un documento HTML")

        status_text, _ = await asyncio.to_thread(
            request_text, f"{base}/enlace/status"
        )
        scan_text, _ = await asyncio.to_thread(request_text, f"{base}/enlace/scan")
        configured_text, _ = await asyncio.to_thread(
            request_text,
            f"{base}/enlace/config",
            {
                "ssid": "Verificacion-2G",
                "pass": "demostracion",
                "server_url": "http://100.64.0.10:8000/ingest",
            },
        )

        initial, acknowledgement = await asyncio.to_thread(websocket_exchange, port)

        return {
            "version": web_root.name,
            "html_bytes": page_bytes,
            "rest": "demo=1" in status_text
            and "Verificacion-2G" in configured_text,
            "scan_networks": len([line for line in scan_text.splitlines() if line]),
            "websocket": initial.get("demo") is True
            and acknowledgement.get("type") == "demo_ack",
        }
    finally:
        server.close()
        await server.wait_closed()


async def main() -> None:
    results = []
    for version in available_versions():
        results.append(await verify_version(version))

    print("Versión                              HTML      REST  WS  Redes")
    print("-" * 72)
    for result in results:
        print(
            f"{result['version']:<36}"
            f"{result['html_bytes']:>7} B   "
            f"{'OK' if result['rest'] else 'FALLO':<5} "
            f"{'OK' if result['websocket'] else 'FALLO':<5} "
            f"{result['scan_networks']}"
        )

    if not all(result["rest"] and result["websocket"] for result in results):
        raise SystemExit(1)
    print(f"\nResultado: {len(results)} de {len(results)} versiones operativas sin hardware.")


if __name__ == "__main__":
    asyncio.run(main())
