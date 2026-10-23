"""Autotest sintético: aprende plantillas conocidas y verifica su limpieza."""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import numpy as np

import firmas
import limpieza
from comun import FLAG_TYPES, exclusive_runs, json_dump


def save_capture(folder, name, samples, flags, scenario, mode, fs, placa):
    np.savez_compressed(folder / f"{name}.npz", samples=np.rint(samples).astype(np.int32),
                        flags=flags.astype(np.uint8), fs=np.float64(fs), mode=np.int16(mode),
                        n_batches=np.int32(len(samples) // 30), scenario=np.str_(scenario),
                        timestamp=np.str_("2026-01-01T00:00:00-03:00"), placa=np.str_(placa))


def generate(folder):
    rng = np.random.default_rng(2929)
    fs, n, pre, post = 2604.0, 24000, 20, 120
    t = np.arange(n) / fs
    base = 7.0 * rng.normal(size=n) + 18.0 * np.sin(2 * np.pi * 50.4 * t)
    zeros = np.zeros(n, dtype=np.uint8)
    save_capture(folder, "base_01", base, zeros, "base_clasico", 0, fs, "sintetica")
    save_capture(folder, "base_02", 7.0 * rng.normal(size=n) + 18.0 * np.sin(2 * np.pi * 50.4 * t),
                 zeros, "base_clasico", 0, fs, "sintetica")

    expected = {}
    for repetition in range(2):
        x = 7.0 * rng.normal(size=n) + 18.0 * np.sin(2 * np.pi * 50.4 * t + repetition)
        flags = np.zeros(n, dtype=np.uint8)
        for type_index, (name, bit) in enumerate(FLAG_TYPES.items()):
            axis = np.arange(post + 1)
            pulse = (220.0 + 35.0 * type_index) * np.exp(-axis / (12.0 + type_index))
            pulse *= np.cos(2 * np.pi * (0.055 + 0.006 * type_index) * axis)
            full = np.r_[np.zeros(pre), pulse]
            expected[name] = full
            start0 = 500 + type_index * 3600
            for event_index in range(14):
                start = start0 + event_index * 230 + repetition * 3
                duration = 3 + event_index % 5
                flags[start:start + duration] |= bit
                gain = 0.8 + 0.4 * rng.random()
                x[start - pre:start + post + 1] += gain * full
        save_capture(folder, f"ruido_{repetition}", x, flags, "rt_sd", 6, fs, "sintetica")
    return expected


def correlation(a, b):
    a, b = np.asarray(a), np.asarray(b)
    a, b = a - np.mean(a), b - np.mean(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def test_dense_overlapping_deconvolution():
    """La regresion conjunta separa firmas que no tienen eventos exclusivos."""
    rng = np.random.default_rng(7319)
    fs, n, pre, length = 2604.0, 18000, 4, 32
    records = []
    truth = {}
    axis = np.arange(length, dtype=float) - pre
    for type_index, name in enumerate(FLAG_TYPES):
        envelope = np.exp(-np.maximum(axis, 0) / (8.0 + type_index))
        truth[name] = (1.0 + 0.18 * type_index) * envelope * np.cos(
            2 * np.pi * (0.085 + 0.011 * type_index) * axis + 0.31 * type_index)

    for capture_index in range(4):
        flags = np.zeros(n, dtype=np.uint8)
        schedules = {
            "I2C": np.arange(40 + capture_index, n - 40, 30),
            "RADIO_TX": np.sort(np.r_[np.arange(44, n - 40, 30), np.arange(58, n - 40, 30)]),
            "SD_IO": np.arange(51 + 2 * capture_index, n - 40, 47),
            "SD_SYNC": np.arange(73 + capture_index, n - 40, 113),
            "AP_BEACON": np.arange(91 + 3 * capture_index, n - 40, 173),
            "MASTER_RX": np.arange(67 + capture_index, n - 40, 61),
        }
        samples = 0.04 * rng.normal(size=n)
        for name, bit in FLAG_TYPES.items():
            for event_index, start in enumerate(schedules[name]):
                start = int(start + rng.integers(-1, 2))
                duration = 1 + (event_index + capture_index) % 5
                flags[start:start + duration] |= bit
                lo = start - pre
                samples[lo:lo + length] += truth[name]
        records.append({"samples": samples, "flags": flags, "fs": fs,
                        "scenario": "dense", "path": f"dense_{capture_index}"})

    if exclusive_runs(records[0]["flags"], FLAG_TYPES["RADIO_TX"], pre, length - pre - 1):
        raise AssertionError("el caso denso debe impedir el promedio de eventos exclusivos")
    learned = firmas.fit_joint_templates(records, pre, length, hp=None, damp=0.5)
    for name, expected in truth.items():
        recovered = learned[name]["onset"]
        corr = correlation(recovered, expected)
        if corr <= 0.95:
            raise AssertionError(f"{name}: deconvolucion densa corr={corr:.3f} <= 0.95")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--salida", help="conservar artefactos en esta carpeta; default: temporal")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    temporary = args.salida is None
    folder = Path(args.salida) if args.salida else Path(tempfile.mkdtemp(prefix="ruido_firmas_"))
    folder.mkdir(parents=True, exist_ok=True)
    try:
        test_dense_overlapping_deconvolution()
        expected = generate(folder)
        if firmas.main([str(folder), "--salida", str(folder), "--placa", "sintetica",
                        "--pre", "20", "--largo", "141", "--hp", "none",
                        "--bootstrap", "20"]):
            raise AssertionError("firmas.py devolvió error")
        signature_path = folder / "firmas_sintetica.json"
        document = json.loads(signature_path.read_text(encoding="utf-8"))
        correlations = {}
        for name, truth in expected.items():
            learned = document["types"][name]["onset"]
            correlations[name] = correlation(learned, truth)
            if correlations[name] < 0.85:
                raise AssertionError(f"{name}: correlación de plantilla {correlations[name]:.3f} < 0.85")
        if limpieza.main([str(folder), "--firmas", str(signature_path)]):
            raise AssertionError("limpieza.py devolvió error")
        cleaned = json.loads(signature_path.read_text(encoding="utf-8"))
        reductions = {}
        for name in FLAG_TYPES:
            evaluation = next(item for item in cleaned["types"][name]["cleaning_evaluation"]
                              if item["method"] == "template")
            reductions[name] = evaluation["residual_vs_before"]
            if reductions[name] >= 0.995:
                raise AssertionError(f"{name}: limpieza insuficiente ({reductions[name]:.3f})")
        result = {"ok": True, "template_correlations": correlations,
                  "best_residual_vs_before": reductions,
                  "artifacts": str(folder) if not temporary else "temporales eliminados"}
        print("AUTOTEST OK")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    finally:
        if temporary:
            shutil.rmtree(folder, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
