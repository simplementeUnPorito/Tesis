"""Resume el piso de ruido con la entrada en corto.

Uso desde la raiz del repositorio::

    python lab/piso_ruido_corto.py
    python lab/piso_ruido_corto.py --raiz lab/ruido_sd_20261019 \
        --salida lab/ruido_sd_20261019/piso_ruido
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib
import numpy as np
from scipy.signal import welch

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# ruido_sd ya selecciona el decodificador comun de los volcados. Importarlo
# evita mantener una segunda implementacion del formato binario de las muestras.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lab import ruido_sd  # noqa: E402


UV_POR_CUENTA = 19.92
NPERSEG = 1024
ADC_BITS = 18
RIEL_INFERIOR = -(2 ** (ADC_BITS - 1))
RIEL_SUPERIOR = 2 ** (ADC_BITS - 1) - 1
MARGEN_RIEL = 2000
# Riel medido de LPo: con PGA x16 o PGAout x24 la salida queda clavada aca y el
# brote de la SD no la mueve (E3, sin respuesta). No coincide con el riel del
# ADC, por eso se declara aparte.
RIEL_LPO_MEDIDO = 38300


@dataclass
class Captura:
    ruta: Path
    grupo: tuple[int, int, int]
    fs: float
    muestras: np.ndarray
    media: float
    p2p: float
    razones_saturacion: tuple[str, ...]

    @property
    def saturada(self) -> bool:
        return bool(self.razones_saturacion)


def _leer_captura(ruta: Path) -> Captura | None:
    with ruta.open(encoding="utf-8") as fh:
        documento = json.loads(fh.readline())

    meta = documento.get("meta", {})
    nota = str(meta.get("nota", ""))
    if meta.get("cond") != "BASE" or "entrada en corto" not in nota.casefold():
        return None

    faltantes = [clave for clave in ("tap", "pga", "pgaout") if meta.get(clave) is None]
    if faltantes:
        raise ValueError(f"{ruta}: faltan metadatos {', '.join(faltantes)}")
    grupo = tuple(int(meta[clave]) for clave in ("tap", "pga", "pgaout"))

    cabecera = documento.get("cabecera", {})
    try:
        fs = float(cabecera["fs"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{ruta}: fs ausente o invalido en la cabecera") from exc
    if not np.isfinite(fs) or fs <= 0:
        raise ValueError(f"{ruta}: fs debe ser positivo, recibido {fs!r}")

    # La decodificacion queda centralizada en el codigo ya usado por ruido_sd.
    _, _, muestras, _, _ = ruido_sd.ar.cargar(str(ruta))
    if muestras.size == 0:
        raise ValueError(f"{ruta}: el volcado no contiene muestras")
    muestras = np.asarray(muestras, dtype=np.float64).copy()
    # Mismo saneamiento que ruido_sd._medir: la muestra 0 y las posiciones de
    # marca traen un artefacto de codificacion (+2^16/+2^17) aislado.
    centro = muestras[1:-1]
    aisladas = np.flatnonzero(
        (np.abs(centro - muestras[:-2]) > ruido_sd.MARCA_UMBRAL) &
        (np.abs(centro - muestras[2:]) > ruido_sd.MARCA_UMBRAL)) + 1
    muestras[aisladas] = 0.5 * (muestras[aisladas - 1] + muestras[aisladas + 1])
    if muestras.size > 1 and abs(muestras[0] - muestras[1]) > ruido_sd.MARCA_UMBRAL:
        muestras[0] = muestras[1]
    media = float(np.mean(muestras))
    p2p = float(np.ptp(muestras))

    razones = []
    if p2p < 5:
        razones.append(f"p2p={p2p:g} < 5 cuentas")
    distancia_inferior = abs(media - RIEL_INFERIOR)
    distancia_superior = abs(RIEL_SUPERIOR - media)
    if min(distancia_inferior, distancia_superior) < MARGEN_RIEL:
        riel = RIEL_INFERIOR if distancia_inferior < distancia_superior else RIEL_SUPERIOR
        razones.append(
            f"media={media:.3f}, a {min(distancia_inferior, distancia_superior):.3f} "
            f"cuentas del riel {riel}"
        )
    motivo = ruido_sd.no_utilizable(muestras)
    if motivo:
        razones.append(motivo)
    return Captura(ruta, grupo, fs, muestras, media, p2p, tuple(razones))


def _esta_dentro(ruta: Path, directorio: Path) -> bool:
    try:
        ruta.resolve().relative_to(directorio.resolve())
        return True
    except ValueError:
        return False


def _descubrir(raiz: Path, salida: Path) -> list[Captura]:
    capturas = []
    for ruta in sorted(raiz.glob("*/*.txt")):
        if _esta_dentro(ruta, salida):
            continue
        captura = _leer_captura(ruta)
        if captura is not None:
            capturas.append(captura)
    return capturas


def _resumir_grupo(
    grupo: tuple[int, int, int], capturas: list[Captura]
) -> tuple[dict[str, object], tuple[np.ndarray, np.ndarray] | None]:
    validas = [captura for captura in capturas if not captura.saturada]
    saturadas = [captura for captura in capturas if captura.saturada]
    fila: dict[str, object] = {
        "tap": grupo[0],
        "pga": grupo[1],
        "pgaout": grupo[2],
        "capturas_usadas": len(validas),
        "capturas_saturadas": len(saturadas),
        "muestras_usadas": sum(c.muestras.size for c in validas),
    }
    if not validas:
        fila.update(
            {
                "fs_hz": "",
                "media_cuentas": "",
                "media_uV": "",
                "std_cuentas": "",
                "std_uV": "",
                "rms_ac_cuentas": "",
                "rms_ac_uV": "",
                "p2p_cuentas": "",
                "p2p_uV": "",
            }
        )
        return fila, None

    frecuencias = {captura.fs for captura in validas}
    if len(frecuencias) != 1:
        detalle = ", ".join(f"{c.ruta.name}={c.fs:g}" for c in validas)
        raise ValueError(f"fs incompatibles en el grupo {grupo}: {detalle}")
    fs = frecuencias.pop()
    cortas = [c.ruta.name for c in validas if c.muestras.size < NPERSEG]
    if cortas:
        raise ValueError(
            f"capturas con menos de {NPERSEG} muestras en el grupo {grupo}: "
            + ", ".join(cortas)
        )

    crudas = np.concatenate([captura.muestras for captura in validas])
    centradas = [captura.muestras - captura.media for captura in validas]
    ac = np.concatenate(centradas)
    media = float(np.mean(crudas))
    std = float(np.std(crudas, ddof=1)) if crudas.size > 1 else 0.0
    rms_ac = float(np.sqrt(np.mean(ac**2)))
    p2p = float(np.max(ac) - np.min(ac))
    fila.update(
        {
            "fs_hz": fs,
            "media_cuentas": media,
            "media_uV": media * UV_POR_CUENTA,
            "std_cuentas": std,
            "std_uV": std * UV_POR_CUENTA,
            "rms_ac_cuentas": rms_ac,
            "rms_ac_uV": rms_ac * UV_POR_CUENTA,
            "p2p_cuentas": p2p,
            "p2p_uV": p2p * UV_POR_CUENTA,
        }
    )

    psd = []
    frecuencia = None
    for muestras in centradas:
        frecuencia, densidad = welch(muestras, fs=fs, nperseg=NPERSEG)
        psd.append(densidad)
    return fila, (frecuencia, np.mean(np.stack(psd), axis=0))


def _guardar_csv(salida: Path, filas: list[dict[str, object]]) -> None:
    columnas = [
        "tap",
        "pga",
        "pgaout",
        "fs_hz",
        "capturas_usadas",
        "capturas_saturadas",
        "muestras_usadas",
        "media_cuentas",
        "media_uV",
        "std_cuentas",
        "std_uV",
        "rms_ac_cuentas",
        "rms_ac_uV",
        "p2p_cuentas",
        "p2p_uV",
    ]
    with (salida / "piso.csv").open("w", newline="", encoding="utf-8") as fh:
        escritor = csv.DictWriter(fh, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(filas)


def _numero(fila: dict[str, object], clave: str) -> str:
    valor = fila[clave]
    return "—" if valor == "" else f"{float(valor):.4g}"


def _guardar_markdown(salida: Path, filas: list[dict[str, object]]) -> None:
    lineas = [
        "# Piso de ruido con entrada en corto",
        "",
        (
            f"Rieles ADC inferidos: {RIEL_INFERIOR} a {RIEL_SUPERIOR} cuentas "
            f"({ADC_BITS} bits). Conversión: {UV_POR_CUENTA:g} µV/cuenta."
        ),
        "",
        "| tap | PGA | PGAout | usadas | saturadas | media [cuentas] | std [µV] | RMS AC [µV] | p2p AC [µV] |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for fila in filas:
        lineas.append(
            "| {tap} | {pga} | {pgaout} | {capturas_usadas} | "
            "{capturas_saturadas} | {media} | {std} | {rms} | {p2p} |".format(
                **fila,
                media=_numero(fila, "media_cuentas"),
                std=_numero(fila, "std_uV"),
                rms=_numero(fila, "rms_ac_uV"),
                p2p=_numero(fila, "p2p_uV"),
            )
        )
    lineas.extend(
        [
            "",
            "La media y la desviación estándar usan todas las muestras crudas del grupo. "
            "RMS, p2p y Welch usan cada captura después de quitarle su propia media.",
            "",
            "---",
            "Generado por Codex (GPT-5), sin delegados.",
            "",
        ]
    )
    (salida / "piso.md").write_text("\n".join(lineas), encoding="utf-8")


def _guardar_indice(salida: Path, raiz: Path, grupos: dict[tuple[int, int, int], list[Captura]]) -> None:
    lineas = [
        "Archivos seleccionados: cond == BASE y nota contiene 'entrada en corto'",
        f"Rieles de saturacion: [{RIEL_INFERIOR}, {RIEL_SUPERIOR}], margen {MARGEN_RIEL}",
        "",
    ]
    for grupo, capturas in grupos.items():
        lineas.append(f"tap={grupo[0]}, pga={grupo[1]}, pgaout={grupo[2]}")
        validas = [c for c in capturas if not c.saturada]
        saturadas = [c for c in capturas if c.saturada]
        lineas.append(f"  USADAS ({len(validas)}):")
        lineas.extend(f"    {c.ruta.relative_to(raiz).as_posix()}" for c in validas)
        lineas.append(f"  SATURADAS, EXCLUIDAS ({len(saturadas)}):")
        lineas.extend(
            "    {ruta} -- {razones}".format(
                ruta=c.ruta.relative_to(raiz).as_posix(),
                razones="; ".join(c.razones_saturacion),
            )
            for c in saturadas
        )
        lineas.append("")
    (salida / "indice.txt").write_text("\n".join(lineas), encoding="utf-8")


def _guardar_psd(
    salida: Path,
    espectros: dict[tuple[int, int, int], tuple[np.ndarray, np.ndarray]],
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5.2))
    for grupo, (frecuencia, densidad) in espectros.items():
        seleccion = frecuencia > 0
        asd_uv = np.sqrt(densidad[seleccion]) * UV_POR_CUENTA
        ax.plot(
            frecuencia[seleccion],
            asd_uv,
            linewidth=1.1,
            label=f"tap {grupo[0]}, PGA {grupo[1]}, out {grupo[2]}",
        )
    ax.set_yscale("log")
    ax.set_xlabel("Frecuencia [Hz]")
    ax.set_ylabel("Densidad espectral [µV/√Hz]")
    ax.set_title(f"Piso de ruido por grupo — Welch nperseg={NPERSEG}")
    ax.grid(True, which="both", alpha=0.25)
    if espectros:
        ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(salida / "psd_por_tap.png", dpi=160)
    plt.close(fig)


def ejecutar(raiz: Path, salida: Path) -> int:
    if not raiz.is_dir():
        raise FileNotFoundError(f"no existe el directorio de entrada: {raiz}")
    capturas = _descubrir(raiz, salida)
    if not capturas:
        raise ValueError("no hay capturas BASE con la nota 'entrada en corto'")

    grupos: dict[tuple[int, int, int], list[Captura]] = {}
    for captura in capturas:
        grupos.setdefault(captura.grupo, []).append(captura)
    grupos = dict(sorted(grupos.items()))

    filas = []
    espectros = {}
    for grupo, miembros in grupos.items():
        fila, espectro = _resumir_grupo(grupo, miembros)
        filas.append(fila)
        if espectro is not None:
            espectros[grupo] = espectro

    salida.mkdir(parents=True, exist_ok=True)
    _guardar_csv(salida, filas)
    _guardar_markdown(salida, filas)
    _guardar_indice(salida, raiz, grupos)
    _guardar_psd(salida, espectros)

    usadas = sum(int(fila["capturas_usadas"]) for fila in filas)
    saturadas = sum(int(fila["capturas_saturadas"]) for fila in filas)
    print(
        f"{len(capturas)} seleccionadas: {usadas} usadas, {saturadas} saturadas; "
        f"{len(grupos)} grupos"
    )
    print(f"salida: {salida}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raiz", default="lab/ruido_sd_20261019")
    parser.add_argument("--salida")
    args = parser.parse_args(argv)
    raiz = Path(args.raiz)
    salida = Path(args.salida) if args.salida else raiz / "piso_ruido"
    return ejecutar(raiz, salida)


if __name__ == "__main__":
    raise SystemExit(main())
