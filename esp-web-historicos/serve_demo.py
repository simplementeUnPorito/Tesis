"""Levanta una versión histórica de la SPA del maestro sin hardware ESP32.

El emulador implementa con la biblioteca estándar de Python las rutas que espera la
página embebida (/ws y /enlace/*). No requiere FastAPI, Uvicorn ni un ESP conectado,
y no modifica los archivos históricos.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import json
import math
import mimetypes
import struct
from html import escape
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit


ROOT = Path(__file__).resolve().parent
CAPTURE_ROOT = (
    ROOT.parent
    / "docs"
    / "Primera Presentación"
    / "latex-nueva-estructura"
    / "figuras"
    / "interfaces"
    / "esp_historico"
)
WEBSOCKET_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


def available_versions() -> list[Path]:
    return sorted(
        path
        for path in ROOT.iterdir()
        if path.is_dir() and (path / "index.html").exists()
    )


def resolve_version(requested: str | None) -> Path:
    versions = available_versions()
    if not versions:
        raise SystemExit("No se encontraron versiones históricas con index.html")
    if requested is None:
        return versions[-1]
    exact = ROOT / requested
    if exact in versions:
        return exact
    matches = [path for path in versions if requested.lower() in path.name.lower()]
    if len(matches) == 1:
        return matches[0]
    choices = "\n  - ".join(path.name for path in versions)
    raise SystemExit(f"Versión ambigua o inexistente. Disponibles:\n  - {choices}")


def load_real_capture(capture_dir: Path) -> dict:
    """Carga una captura real de campo para alimentar la interfaz sin hardware.

    Espera el layout exportado por la propia SPA:
        <captura>/metadata.json
        <captura>/hammer_s1/raw_f32le.bin
        <captura>/geo1_s2/raw_f32le.bin
    Las muestras se guardan en volts (float32 LE) y se convierten a cuentas del
    ADC con el mismo factor que usa la UI (131072/2.5 = 52428.8 cuentas/V).
    """
    capture_dir = capture_dir.resolve()
    meta_path = capture_dir / "metadata.json"
    if not meta_path.is_file():
        raise SystemExit(f"No se encontró metadata.json en {capture_dir}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    fs = int(round(float(meta.get("fs", 2604))))
    counts_per_volt = float(meta.get("adc_counts_per_volt") or (131072 / 2.5))

    def read_signal(subdir: str):
        raw = capture_dir / subdir / "raw_f32le.bin"
        if not raw.is_file():
            return None
        data = raw.read_bytes()
        return [
            int(round(value * counts_per_volt))
            for (value,) in struct.iter_unpack("<f", data)
        ]

    nodes = []
    # hw_class: 0 = geófono, 1 = martillo (igual que reporta el PSoC)
    for subdir in sorted(p.name for p in capture_dir.iterdir() if p.is_dir()):
        if subdir.startswith("geo"):
            samples = read_signal(subdir)
            if samples:
                nodes.append({"hw_class": 0, "name": subdir, "samples": samples})
    for subdir in sorted(p.name for p in capture_dir.iterdir() if p.is_dir()):
        if subdir.startswith("hammer"):
            samples = read_signal(subdir)
            if samples:
                nodes.append({"hw_class": 1, "name": subdir, "samples": samples})
    if not nodes:
        raise SystemExit(f"No se encontraron señales raw_f32le.bin en {capture_dir}")

    # La captura de campo ya dura lo mismo que la ventana visible de la interfaz,
    # así que se emite completa: se ven el golpe del martillo y el arribo del geófono
    # en su posición temporal real, sin recortar ni realinear.
    start = 0

    for index, node in enumerate(nodes, start=1):
        node["node"] = index
    return {
        "fs": fs,
        "nodes": nodes,
        "start": start,
        "name": capture_dir.name,
        "length": min(len(n["samples"]) for n in nodes),
    }


class DemoApplication:
    """Servidor HTTP y WebSocket mínimo para una versión de la interfaz."""

    def __init__(self, web_root: Path, capture: dict | None = None):
        self.web_root = web_root.resolve()
        self.capture = capture
        self.sample_index = capture["start"] if capture else 0
        self.state = {
            "ssid": "Tesis-Campo-2G",
            "server_url": "http://100.64.0.10:8000/ingest",
            "auth_next": False,
        }

    def status_text(self) -> str:
        return "\n".join(
            (
                "phase=captura",
                "sta=up",
                f"ssid={self.state['ssid']}",
                "ip=192.168.1.86",
                "channel=1",
                "queue_files=9",
                "queue_bytes=1482752",
                "fs_free=127401984",
                f"server_url={self.state['server_url']}",
                "last_error=",
                "demo=1",
            )
        )

    def gallery_html(self) -> bytes:
        cards = []
        if CAPTURE_ROOT.is_dir():
            for image_path in sorted(CAPTURE_ROOT.rglob("*.png")):
                relative = image_path.relative_to(CAPTURE_ROOT).as_posix()
                cards.append(
                    '<figure><img loading="lazy" src="/demo/capture/'
                    + escape(relative, quote=True)
                    + '"><figcaption>'
                    + escape(relative)
                    + "</figcaption></figure>"
                )
        html = """<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>QA capturas ESP</title><style>
body{margin:16px;background:#111;color:#eee;font:13px system-ui,sans-serif}
h1{font-size:22px}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
figure{margin:0;padding:8px;background:#1c1c1c;border:1px solid #444;border-radius:6px}
img{display:block;width:100%;height:160px;object-fit:contain;background:#090909}
figcaption{margin-top:6px;overflow-wrap:anywhere;color:#ddd}
</style></head><body><h1>Capturas históricas ESP</h1><div class="grid">"""
        html += "".join(cards) + "</div></body></html>"
        return html.encode("utf-8")

    async def serve_capture(self, path: str, writer: asyncio.StreamWriter) -> None:
        relative = unquote(path.removeprefix("/demo/capture/")).lstrip("/")
        candidate = (CAPTURE_ROOT / relative).resolve()
        try:
            candidate.relative_to(CAPTURE_ROOT.resolve())
        except ValueError:
            await self.send_http(writer, "403 Forbidden", b"forbidden\n")
            return
        if not candidate.is_file():
            await self.send_http(writer, "404 Not Found", b"not found\n")
            return
        await self.send_http(writer, "200 OK", candidate.read_bytes(), "image/png")

    @staticmethod
    def demo_packet(node: int, ptype: int, b2: int, b1: int, b0: int) -> bytes:
        return bytes((0x56, node & 0xFF, ptype & 0xFF, b2 & 0xFF, b1 & 0xFF, b0 & 0xFF))

    @classmethod
    def demo_value_packet(cls, node: int, value: int) -> bytes:
        value &= 0xFFFFFF
        return cls.demo_packet(node, 0x00, value >> 16, value >> 8, value)

    def demo_initial_packets(self) -> bytes:
        if self.capture:
            fs = self.capture["fs"]
            layout = [(n["node"], n["hw_class"]) for n in self.capture["nodes"]]
        else:
            fs = 2604
            layout = [(1, 0), (2, 0), (3, 1)]
        packets = [
            self.demo_packet(0xFF, 0xFD, 1, 1, 0),  # maestro: ESP-NOW OK, canal 1
            self.demo_packet(0xFF, 0x01, 0, 0, 0),  # maestro IDLE
            self.demo_packet(0xFF, 0xFE, len(layout), 0, 0),
        ]
        for node, hw_class in layout:
            packets.extend(
                (
                    self.demo_packet(node, 0xFD, 0x05, (fs >> 8) & 0xFF, fs & 0xFF),
                    self.demo_packet(node, 0xFD, 0x06, hw_class, 0),
                    self.demo_packet(node, 0xFD, 0x07, 1 if hw_class == 0 else 0, 0),
                    self.demo_packet(node, 0x01, 8 if hw_class == 0 else 2, 128, 0),
                )
            )
        return b"".join(packets)

    def demo_signal_packets(self, samples: int = 96) -> bytes:
        if self.capture:
            return self.real_signal_packets(samples)
        packets: list[bytes] = []
        fs = 2604.0
        for offset in range(samples):
            n = self.sample_index + offset
            t = n / fs
            pulse_phase = (n % 5200) / fs
            pulse = math.exp(-10.0 * pulse_phase) * math.sin(2.0 * math.pi * 24.0 * pulse_phase)
            line = 0.18 * math.sin(2.0 * math.pi * 50.0 * t)
            slow = 0.35 * math.sin(2.0 * math.pi * 7.0 * t)
            values = (
                int(185000 * (pulse + line + slow)),
                int(145000 * (0.82 * pulse + 0.12 * math.sin(2.0 * math.pi * 34.0 * t + 0.8))),
                int(220000 * math.exp(-22.0 * pulse_phase) * math.sin(2.0 * math.pi * 85.0 * pulse_phase)),
            )
            for node, value in enumerate(values, start=1):
                packets.append(self.demo_value_packet(node, value))
        self.sample_index += samples
        return b"".join(packets)

    def real_signal_packets(self, samples: int) -> bytes:
        """Emite muestras de una captura real, intercaladas por nodo."""
        packets: list[bytes] = []
        total = self.capture["length"]
        nodes = self.capture["nodes"]
        for offset in range(samples):
            index = self.sample_index + offset
            if index >= total:
                break
            for node in nodes:
                packets.append(
                    self.demo_value_packet(node["node"], node["samples"][index])
                )
        self.sample_index = min(self.sample_index + samples, total)
        return b"".join(packets)

    async def send_http(
        self,
        writer: asyncio.StreamWriter,
        status: str,
        body: bytes,
        content_type: str = "text/plain; charset=utf-8",
    ) -> None:
        writer.write(
            (
                f"HTTP/1.1 {status}\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"Content-Type: {content_type}\r\n"
                "Cache-Control: no-store\r\n"
                "Connection: close\r\n\r\n"
            ).encode("ascii")
            + body
        )
        await writer.drain()

    async def serve_static(
        self, path: str, writer: asyncio.StreamWriter
    ) -> None:
        relative = "index.html" if path == "/" else unquote(path).lstrip("/")
        candidate = (self.web_root / relative).resolve()
        try:
            candidate.relative_to(self.web_root)
        except ValueError:
            await self.send_http(writer, "403 Forbidden", b"forbidden\n")
            return
        if not candidate.is_file():
            await self.send_http(writer, "404 Not Found", b"not found\n")
            return
        body = candidate.read_bytes()
        # La versión final fuerza geo-obtain.local cuando detecta una IP. Eso es
        # correcto en campo, pero impide documentarla sin la placa ni mDNS. El
        # emulador habilita una excepción sólo en la respuesta HTTP y únicamente
        # cuando la página se abrió con ?demo=1; el snapshot histórico no se toca.
        if candidate.as_posix().endswith("/js/enlace.js"):
            source = body.decode("utf-8")
            source = source.replace(
                "if (!h || h === 'geo-obtain.local' || h === 'geo-obtain') return;",
                "if (new URLSearchParams(location.search).has('demo') || "
                "!h || h === 'geo-obtain.local' || h === 'geo-obtain') return;",
            )
            body = source.encode("utf-8")
        mime = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        if mime.startswith("text/"):
            mime += "; charset=utf-8"
        await self.send_http(writer, "200 OK", body, mime)

    async def handle_websocket(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        headers: dict[str, str],
    ) -> None:
        key = headers.get("sec-websocket-key", "")
        if not key:
            await self.send_http(writer, "400 Bad Request", b"missing key\n")
            return
        accept = base64.b64encode(
            hashlib.sha1((key + WEBSOCKET_GUID).encode("ascii")).digest()
        ).decode("ascii")
        writer.write(
            (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept}\r\n\r\n"
            ).encode("ascii")
        )
        await writer.drain()

        link_state = json.dumps(
            {
                "type": "link",
                "demo": True,
                "master_rssi": -42,
                "slaves": [
                    {"node": 1, "rssi": -48},
                    {"node": 2, "rssi": -53},
                    {"node": 3, "rssi": -57},
                ],
            }
        )
        await self.send_ws_frame(writer, 0x1, link_state.encode("utf-8"))
        if self.state.pop("auth_next", False):
            await self.send_ws_frame(
                writer, 0x1, json.dumps({"type": "auth_required"}).encode("utf-8")
            )
        await self.send_ws_frame(writer, 0x2, self.demo_initial_packets())
        if self.capture:
            # Lotes sucesivos hasta agotar la captura real.
            while self.sample_index < self.capture["length"]:
                await self.send_ws_frame(writer, 0x2, self.demo_signal_packets(720))
        else:
            await self.send_ws_frame(writer, 0x2, self.demo_signal_packets(720))

        while not reader.at_eof():
            try:
                opcode, payload = await asyncio.wait_for(
                    self.receive_ws_frame(reader), timeout=3
                )
            except asyncio.TimeoutError:
                continue
            except (asyncio.IncompleteReadError, ConnectionError):
                break
            if opcode == 0x8:
                await self.send_ws_frame(writer, 0x8, payload)
                break
            if opcode == 0x9:
                await self.send_ws_frame(writer, 0xA, payload)
                continue
            if opcode == 0x1:
                message = payload.decode("utf-8", errors="replace")
                acknowledgement = json.dumps(
                    {"type": "demo_ack", "received": message[:160]}
                ).encode("utf-8")
                await self.send_ws_frame(writer, 0x1, acknowledgement)
                # Un comando de la UI suele cambiar ganancia, filtro o modo de
                # captura. Enviar otro bloque después del ACK permite ver el
                # efecto sin mantener un streaming que haga crecer el log.
                if self.capture:
                    self.sample_index = self.capture["start"]
                    while self.sample_index < self.capture["length"]:
                        await self.send_ws_frame(
                            writer, 0x2, self.demo_signal_packets(720)
                        )
                else:
                    await self.send_ws_frame(writer, 0x2, self.demo_signal_packets(720))

    @staticmethod
    async def receive_ws_frame(
        reader: asyncio.StreamReader,
    ) -> tuple[int, bytes]:
        first, second = await reader.readexactly(2)
        opcode = first & 0x0F
        length = second & 0x7F
        if length == 126:
            length = struct.unpack("!H", await reader.readexactly(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", await reader.readexactly(8))[0]
        mask = await reader.readexactly(4) if second & 0x80 else None
        payload = bytearray(await reader.readexactly(length))
        if mask:
            for index in range(length):
                payload[index] ^= mask[index % 4]
        return opcode, bytes(payload)

    @staticmethod
    async def send_ws_frame(
        writer: asyncio.StreamWriter, opcode: int, payload: bytes
    ) -> None:
        if len(payload) < 126:
            header = bytes((0x80 | opcode, len(payload)))
        elif len(payload) < 65536:
            header = bytes((0x80 | opcode, 126)) + struct.pack("!H", len(payload))
        else:
            header = bytes((0x80 | opcode, 127)) + struct.pack("!Q", len(payload))
        writer.write(header + payload)
        await writer.drain()

    async def handle(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        try:
            request_line = (await reader.readline()).decode("iso-8859-1").strip()
            if not request_line:
                return
            method, target, _ = request_line.split(" ", 2)
            headers: dict[str, str] = {}
            while True:
                line = await reader.readline()
                if line in (b"\r\n", b"\n", b""):
                    break
                name, value = line.decode("iso-8859-1").split(":", 1)
                headers[name.lower().strip()] = value.strip()

            path = urlsplit(target).path
            if (
                path == "/ws"
                and headers.get("upgrade", "").lower() == "websocket"
            ):
                await self.handle_websocket(reader, writer, headers)
                return

            content_length = int(headers.get("content-length", "0"))
            body = await reader.readexactly(content_length) if content_length else b""

            if method == "GET" and path == "/enlace/status":
                await self.send_http(writer, "200 OK", self.status_text().encode())
            elif method == "GET" and path == "/demo/auth":
                self.state["auth_next"] = True
                await self.send_http(writer, "200 OK", b"auth_required_on_next_ws\n")
            elif method == "GET" and path == "/demo/gallery":
                await self.send_http(
                    writer,
                    "200 OK",
                    self.gallery_html(),
                    "text/html; charset=utf-8",
                )
            elif method == "GET" and path.startswith("/demo/capture/"):
                await self.serve_capture(path, writer)
            elif method == "GET" and path == "/enlace/scan":
                await self.send_http(
                    writer,
                    "200 OK",
                    b"1 -39 Tesis-Campo-2G\n6 -67 Laboratorio\n11 -74 Hotspot-2.4G\n",
                )
            elif method == "POST" and path == "/enlace/config":
                form = parse_qs(body.decode("utf-8"), keep_blank_values=True)
                ssid = form.get("ssid", [""])[0]
                if ssid:
                    self.state["ssid"] = ssid
                self.state["server_url"] = form.get("server_url", [""])[0]
                await self.send_http(writer, "200 OK", self.status_text().encode())
            elif method == "POST" and path == "/ingest":
                filename = headers.get("x-geo-filename", "captura.zip")
                response = json.dumps(
                    {"ok": True, "filename": filename, "bytes": len(body), "demo": True}
                ).encode("utf-8")
                await self.send_http(
                    writer, "200 OK", response, "application/json; charset=utf-8"
                )
            elif method == "GET" and path == "/ws-reset":
                await self.send_http(writer, "200 OK", b"ok\n")
            elif method == "GET":
                await self.serve_static(path, writer)
            else:
                await self.send_http(
                    writer, "405 Method Not Allowed", b"method not allowed\n"
                )
        except (ValueError, UnicodeError, asyncio.IncompleteReadError):
            if not writer.is_closing():
                await self.send_http(writer, "400 Bad Request", b"bad request\n")
        finally:
            if not writer.is_closing():
                writer.close()
                await writer.wait_closed()


async def start_demo_server(
    web_root: Path, host: str, port: int, capture: dict | None = None
) -> asyncio.AbstractServer:
    application = DemoApplication(web_root, capture)
    return await asyncio.start_server(application.handle, host, port)


async def run(
    web_root: Path, host: str, port: int, capture: dict | None = None
) -> None:
    server = await start_demo_server(web_root, host, port, capture)
    address = server.sockets[0].getsockname()
    print(f"Versión: {web_root.name}")
    if capture:
        print(
            f"Datos reales: {capture['name']} "
            f"(fs={capture['fs']} Hz, {len(capture['nodes'])} nodos)"
        )
    print(f"Abrir: http://{address[0]}:{address[1]}/")
    async with server:
        await server.serve_forever()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Servidor de demostración para las interfaces web históricas del ESP32"
    )
    parser.add_argument(
        "--version",
        help="Nombre completo o fragmento único; por defecto se usa la más reciente",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument("--list", action="store_true", help="Lista versiones y termina")
    parser.add_argument(
        "--datos",
        help="Directorio de una captura real exportada; sustituye la señal sintética",
    )
    args = parser.parse_args()

    if args.list:
        for version in available_versions():
            print(version.name)
        return

    capture = load_real_capture(Path(args.datos)) if args.datos else None
    asyncio.run(run(resolve_version(args.version), args.host, args.port, capture))


if __name__ == "__main__":
    main()
