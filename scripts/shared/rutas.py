"""Rutas comunes para artefactos generados por el superproyecto.

Convencion: todo resultado interno o intermedio se escribe en ``outputs/``;
solo los entregables de tesis versionables se escriben en ``docs/``. Ningun
generador debe dejar resultados junto a su codigo fuente.
"""

from __future__ import annotations

from pathlib import Path


def _ancestros(inicio: Path):
    inicio = inicio.resolve()
    yield inicio
    yield from inicio.parents


def _buscar_marcador(inicios: list[Path], marcador: str) -> Path | None:
    vistos: set[Path] = set()
    for inicio in inicios:
        for carpeta in _ancestros(inicio):
            if carpeta in vistos:
                continue
            vistos.add(carpeta)
            if (carpeta / marcador).exists():
                return carpeta
    return None


def dir_salida(*partes: str | Path, entregable: bool = False) -> Path:
    """Crea y devuelve la carpeta donde debe escribir un generador.

    Busca hacia arriba la raiz del superproyecto, identificada por
    ``.gitmodules``. Devuelve ``<raiz>/outputs/<partes>`` para resultados de
    trabajo o ``<raiz>/docs/<partes>`` para entregables. Si el submodulo fue
    clonado por separado, usa el ``outputs/`` (o ``docs/``) de ese repositorio
    local. En ese modo aislado todos los resultados caen en ``outputs/``,
    incluso si se pidio ``entregable=True``.
    """

    inicios = [Path.cwd(), Path(__file__).resolve().parent]
    raiz = _buscar_marcador(inicios, ".gitmodules")
    aislado = raiz is None
    if aislado:
        raiz = _buscar_marcador(inicios, ".git") or Path.cwd().resolve()

    carpeta = raiz / ("docs" if entregable and not aislado else "outputs")
    carpeta = carpeta.joinpath(*(Path(parte) for parte in partes))
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta
