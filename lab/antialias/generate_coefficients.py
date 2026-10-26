"""Genera coeficientes Q1.23 antialias para una frecuencia nativa dada."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from reference import FACTORS, acquisition_fir_q23, kaiser_q23


def write_decimation_table(path: Path, fs_hz: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("fs_input_hz", "decimation", "fs_output_hz", "tap", "q23"))
        for factor in FACTORS:
            coefficients = kaiser_q23(factor)
            for tap, value in enumerate(coefficients):
                writer.writerow((f"{fs_hz:.9f}", factor,
                                 f"{fs_hz / factor:.9f}", tap, int(value)))


def write_psoc_fir(path: Path, fs_hz: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    coefficients = acquisition_fir_q23(fs_hz)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(("fs_input_hz", "cutoff_hz", "tap", "q23"))
        for tap, value in enumerate(coefficients):
            writer.writerow((f"{fs_hz:.9f}", "200.000000000", tap, int(value)))
        writer.writerow((f"{fs_hz:.9f}", "200.000000000", len(coefficients), 0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fs", type=float, required=True, help="Fs nativa en Hz")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--psoc-fir-output", type=Path,
                        help="CSV Q1.23 del FIR de adquisición del bloque Filter")
    args = parser.parse_args()

    write_decimation_table(args.output, args.fs)
    if args.psoc_fir_output is not None:
        write_psoc_fir(args.psoc_fir_output, args.fs)


if __name__ == "__main__":
    main()
