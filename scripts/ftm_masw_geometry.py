"""Calculadora analitica reproducible para geometria ESP32 FTM/MASW."""

from __future__ import annotations

import json
import math
from pathlib import Path

from shared.rutas import dir_salida


def _finite_nonnegative(**values: float) -> None:
    for name, value in values.items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and nonnegative")


def along_axis_interval(range_m: float, error_m: float, half_width_m: float,
                        height_difference_max_m: float = 0) -> tuple[float, float]:
    """Return the exact conservative interval for ordered slaves with |t| <= w."""
    _finite_nonnegative(range_m=range_m, error_m=error_m,
                        half_width_m=half_width_m,
                        height_difference_max_m=height_difference_max_m)
    shortest = max(0.0, range_m - error_m)
    lower_sq = max(0.0, shortest**2 - (2 * half_width_m) ** 2
                   - height_difference_max_m**2)
    return math.sqrt(lower_sq), range_m + error_m


def phase_error_deg(position_error_m: float, wavelength_m: float) -> float:
    """Convert position error to phase error in degrees."""
    _finite_nonnegative(position_error_m=position_error_m)
    if not math.isfinite(wavelength_m) or wavelength_m <= 0:
        raise ValueError("wavelength_m must be finite and strictly positive")
    return 360 * position_error_m / wavelength_m


def minimum_zero_failure_trials(coverage: float = 0.95,
                                confidence: float = 0.95) -> int:
    """Return the sample count for a zero-failure coverage demonstration."""
    if not all(math.isfinite(x) and 0 < x < 1 for x in (coverage, confidence)):
        raise ValueError("coverage and confidence must be finite and between zero and one")
    return math.ceil(math.log(1 - confidence) / math.log(coverage))


def build_results() -> dict[str, object]:
    """Build deterministic scenario data without writing files."""
    range_rows = [{"spacing_m": s, "half_width_m": w,
                   "worst_lateral_difference_m": 2 * w,
                   "range_excess_m": math.hypot(s, 2 * w) - s}
                  for w in (0.05, 0.1, 0.2, 0.3)
                  for s in (0.5, 1, 1.5, 2, 4)]
    phase_rows = [{"position_error_m": dx, "wavelength_m": wavelength,
                   "phase_error_deg": phase_error_deg(dx, wavelength)}
                  for dx in (0.1, 0.25, 0.5, 1)
                  for wavelength in (2, 5, 10, 20)]
    trials = [{"coverage": coverage, "confidence": 0.95,
               "minimum_trials": minimum_zero_failure_trials(coverage, 0.95)}
              for coverage in (0.9, 0.95, 0.99)]
    bounds = []
    for error in (0.25, 0.5, 1):
        lower, upper = along_axis_interval(2, error, 0.2)
        bounds.append({"range_m": 2, "error_m": error, "half_width_m": 0.2,
                       "height_difference_max_m": 0,
                       "along_axis_min_m": lower, "along_axis_max_m": upper})
    return {
        "metadata": {
            "scope": "All results are analytic examples; no measured performance.",
            "interval_assumptions": "Ordered slaves; each |t| <= half_width_m; bounded height difference.",
            "coverage_note": "Exact conservative geometric interval; no statistical coverage claim.",
        },
        "range_excess_scenarios": range_rows,
        "phase_error_scenarios": phase_rows,
        "zero_failure_trials": trials,
        "bound_examples": bounds,
    }


def _table(title: str, headers: tuple[str, ...], rows: list[dict],
           columns: tuple[tuple[str, str], ...]) -> list[str]:
    lines = [f"## {title}", "", "| " + " | ".join(headers) + " |",
             "|" + "|".join("---:" for _ in headers) + "|"]
    lines += ["| " + " | ".join(format(row[key], spec) for key, spec in columns) + " |"
              for row in rows]
    return lines + [""]


def _markdown(results: dict[str, object]) -> str:
    lines = ["# Geometria analitica ESP32 FTM/MASW", "",
             "Todos los resultados son ejemplos analiticos; no representan precision medida.",
             "El intervalo supone esclavos ordenados, |t| <= w y altura acotada; es una cota "
             "geometrica exacta y conservadora, sin afirmar cobertura estadistica.", ""]
    lines += _table("Exceso de rango por separacion lateral",
                    ("Espaciado (m)", "Semiancho w (m)", "Diferencia lateral maxima 2w (m)", "Exceso (m)"),
                    results["range_excess_scenarios"],
                    (("spacing_m", "g"), ("half_width_m", "g"),
                     ("worst_lateral_difference_m", "g"), ("range_excess_m", ".6f")))
    lines += _table("Error de fase", ("Error de posicion (m)", "Longitud de onda (m)", "Error (grados)"),
                    results["phase_error_scenarios"],
                    (("position_error_m", "g"), ("wavelength_m", "g"), ("phase_error_deg", ".3f")))
    lines += _table("Ensayos sin fallas", ("Cobertura", "Confianza", "Ensayos minimos"),
                    results["zero_failure_trials"],
                    (("coverage", ".2f"), ("confidence", ".2f"), ("minimum_trials", "d")))
    lines += _table("Ejemplos de cotas longitudinales",
                    ("Rango (m)", "Error (m)", "w (m)", "Altura max. (m)", "Min. (m)", "Max. (m)"),
                    results["bound_examples"],
                    (("range_m", "g"), ("error_m", "g"), ("half_width_m", "g"),
                     ("height_difference_max_m", "g"), ("along_axis_min_m", ".6f"),
                     ("along_axis_max_m", ".6f")))
    return "\n".join(lines)


def _plot(results: dict[str, object], path: Path) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for value in (0.05, 0.1, 0.2, 0.3):
        rows = [r for r in results["range_excess_scenarios"] if r["half_width_m"] == value]
        axes[0].plot([r["spacing_m"] for r in rows], [r["range_excess_m"] for r in rows],
                     marker="o", label=f"w={value:g} m")
    for value in (0.1, 0.25, 0.5, 1):
        rows = [r for r in results["phase_error_scenarios"] if r["position_error_m"] == value]
        axes[1].plot([r["wavelength_m"] for r in rows], [r["phase_error_deg"] for r in rows],
                     marker="o", label=f"dx={value:g} m")
    axes[0].set(xlabel="Espaciado longitudinal (m)", ylabel="Exceso de rango (m)")
    axes[0].set_title("Extremos de franja ±w; igual altura", fontsize=10)
    axes[1].set(xlabel="Longitud de onda (m)", ylabel="Error de fase (grados)")
    for axis in axes:
        axis.legend()
        axis.grid(alpha=0.3)
    figure.suptitle("Ejemplos analiticos; no precision medida")
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def main() -> None:
    output = dir_salida("ftm_masw")
    results = build_results()
    paths = (output / "ftm_masw_geometry.json", output / "ftm_masw_geometry.md",
             output / "ftm_masw_geometry.png")
    paths[0].write_text(json.dumps(results, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    paths[1].write_text(_markdown(results), encoding="utf-8")
    _plot(results, paths[2])
    print(*paths, sep="\n")


if __name__ == "__main__":
    main()
