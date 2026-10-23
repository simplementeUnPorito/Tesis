"""Aprende firmas de interferencia a partir de una carpeta de capturas NPZ."""
from __future__ import annotations

import argparse
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import signal

from comun import (FLAG_TYPES, LINE_HARMONICS, LINE_SEARCH_HZ, aligned_segments,
                   capture_files, exclusive_runs, json_dump, load_capture, preprocess,
                   scalar)


def _corr_rows(rows, template):
    result = []
    tc = template - np.mean(template)
    tn = np.linalg.norm(tc)
    for row in rows:
        rc = row - np.mean(row)
        denom = np.linalg.norm(rc) * tn
        result.append(float(np.dot(rc, tc) / denom) if denom else 0.0)
    return np.asarray(result)


def _stats(values):
    values = np.asarray(values, dtype=np.float64)
    if not values.size:
        return {"mean": None, "median": None, "std": None, "min": None, "max": None}
    return {key: float(fun(values)) for key, fun in (
        ("mean", np.mean), ("median", np.median), ("std", np.std),
        ("min", np.min), ("max", np.max))}


def _duration_bins(durations, amplitudes):
    durations = np.asarray(durations, dtype=int)
    amplitudes = np.asarray(amplitudes, dtype=float)
    bins = []
    for duration in np.unique(durations):
        mask = durations == duration
        bins.append({"run_length": int(duration), "events": int(mask.sum()),
                     "amplitude_mean": float(np.mean(amplitudes[mask])),
                     "amplitude_std": float(np.std(amplitudes[mask]))})
    corr = 0.0
    if durations.size >= 3 and np.std(durations) > 0 and np.std(amplitudes) > 0:
        corr = float(np.corrcoef(durations, amplitudes)[0, 1])
    return bins, corr


def learn_type(records, bit, pre, post):
    rows0, offsets0, durations = [], [], []
    for record in records:
        events = exclusive_runs(record["flags"], bit, pre, post)
        rows, _ = aligned_segments(record["clean"], events, pre, post)
        offset_events = [(end, end) for _, end in events if end >= pre and end + post < record["clean"].size]
        off_rows, _ = aligned_segments(record["clean"], offset_events, pre, post)
        rows0.extend(rows); offsets0.extend(off_rows)
        durations.extend(end - start for start, end in events[:len(rows)])
    if not rows0:
        return None
    provisional = np.mean(np.asarray(rows0), axis=0)
    aligned, offset_rows, aligned_durations, shifts = [], [], [], []
    cursor = 0
    for record in records:
        events = exclusive_runs(record["flags"], bit, pre, post)
        rows, local_shifts = aligned_segments(record["clean"], events, pre, post, provisional, 3)
        aligned.extend(rows); shifts.extend(local_shifts.tolist())
        aligned_durations.extend(end - start for start, end in events[:len(rows)])
        offset_events = [(end, end) for _, end in events if end >= pre and end + post < record["clean"].size]
        off, _ = aligned_segments(record["clean"], offset_events, pre, post)
        offset_rows.extend(off)
        cursor += len(rows)
    rows = np.asarray(aligned)
    mean = np.mean(rows, axis=0)
    median = np.median(rows, axis=0)
    std = np.std(rows, axis=0)
    denom = float(np.dot(mean, mean))
    amplitudes = rows @ mean / denom if denom > 0 else np.zeros(rows.shape[0])
    correlations = _corr_rows(rows, mean)
    noise = rows[:, :pre] if pre else rows
    noise_sigma = float(np.std(noise))
    template_rms = float(np.sqrt(np.mean(mean ** 2)))
    snr = template_rms / noise_sigma if noise_sigma > 0 else math.inf
    effective = np.flatnonzero(np.abs(mean) > 3.0 * noise_sigma)
    effective_length = int(effective[-1] - effective[0] + 1) if effective.size else 0
    bins, duration_corr = _duration_bins(aligned_durations, amplitudes)
    offset_template = np.mean(offset_rows, axis=0) if offset_rows else np.zeros_like(mean)
    offset_useful = bool(np.max(np.abs(offset_template)) > 3.0 * noise_sigma)
    repeatability = float(np.median(correlations))
    recommended = "template_xcorr" if snr >= 2.0 and repeatability >= 0.35 else "interp"
    return {
        "events": int(rows.shape[0]), "pre": pre, "post": post,
        "onset_template": mean.tolist(), "onset_median": median.tolist(),
        "onset_std": std.tolist(),
        "offset_template": offset_template.tolist() if offset_useful else [],
        "offset_useful": offset_useful, "unit": "ADC counts after offset",
        "amplitude_ls": _stats(amplitudes), "snr_template_vs_pre": float(snr),
        "noise_sigma_pre": noise_sigma, "effective_length_samples": effective_length,
        "repeatability_correlation": _stats(correlations),
        "alignment_shift_samples": _stats(shifts),
        "duration": {"bins": bins, "amplitude_length_correlation": duration_corr,
                     "classification": "scales_with_length" if abs(duration_corr) >= 0.5 else "fixed_edge_transient"},
        "recommended_method": {"method": recommended,
                               "parameters": {"align": 2, "offset": offset_useful} if recommended == "template_xcorr" else {"margin": 2}},
    }


def baseline_stats(records):
    base = [r for r in records if r["scenario"] == "base_clasico"]
    if not base:
        return {"captures": 0, "rms_counts": None, "spectrum_1_100_hz": {}}
    rms = [np.sqrt(np.mean(r["clean"] ** 2)) for r in base]
    spectra = []
    freqs = None
    for r in base:
        freqs, power = signal.welch(r["clean"], r["fs"], nperseg=min(4096, r["clean"].size))
        spectra.append(power)
    common = min(map(len, spectra))
    freqs = freqs[:common]
    power = np.mean([p[:common] for p in spectra], axis=0)
    mask = (freqs >= 1) & (freqs <= 100)
    return {"captures": len(base), "rms_counts": _stats(rms),
            "spectrum_1_100_hz": {"frequency_hz": freqs[mask].tolist(),
                                    "psd_counts2_per_hz": power[mask].tolist()}}


def make_plots(output, placa, signatures, baseline):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    for name, spec in signatures.items():
        axis = np.arange(-spec["pre"], spec["post"] + 1)
        mean = np.asarray(spec["onset_template"])
        std = np.asarray(spec["onset_std"])
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(axis, mean, label="media")
        ax.fill_between(axis, mean - std, mean + std, alpha=0.25, label="±1σ")
        if spec["offset_template"]:
            ax.plot(axis, spec["offset_template"], label="flanco final")
        ax.axvline(0, color="k", linewidth=0.8)
        ax.set(title=f"{placa}: {name}", xlabel="muestras desde el flanco", ylabel="cuentas ADC")
        ax.grid(True, alpha=0.25); ax.legend(); fig.tight_layout()
        fig.savefig(output / f"firma_{placa}_{name.lower()}.png", dpi=150)
        plt.close(fig)
    spectrum = baseline.get("spectrum_1_100_hz", {})
    if spectrum.get("frequency_hz"):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.semilogy(spectrum["frequency_hz"], spectrum["psd_counts2_per_hz"])
        ax.set(title=f"{placa}: piso base clásico", xlabel="Hz", ylabel="PSD cuentas²/Hz")
        ax.grid(True, which="both", alpha=0.25); fig.tight_layout()
        fig.savefig(output / f"piso_{placa}.png", dpi=150); plt.close(fig)
    return True


def write_report(path, placa, files, baseline, signatures, plotted):
    rms = baseline.get("rms_counts", {})
    lines = [f"# Firmas de ruido — {placa}", "",
             f"Capturas analizadas: {len(files)}. Preprocesado: mediana + notch LS 50 Hz.",
             f"Piso base clásico RMS: {rms.get('mean', 'sin captura')} cuentas.", "",
             "| Fuente | Eventos | SNR | Repetibilidad mediana | Longitud efectiva | Dependencia | Método inicial |",
             "|---|---:|---:|---:|---:|---|---|"]
    for name, spec in signatures.items():
        lines.append(f"| {name} | {spec['events']} | {spec['snr_template_vs_pre']:.2f} | "
                     f"{spec['repeatability_correlation']['median']:.2f} | {spec['effective_length_samples']} | "
                     f"{spec['duration']['classification']} | {spec['recommended_method']['method']} |")
    lines += ["", "La recomendación definitiva se actualiza con `limpieza.py`, incluyendo preservación de señal.",
              "Los PNG se generaron." if plotted else "Matplotlib no está disponible; no se generaron PNG.",
              "", "---", "Proveniencia: Codex (GPT-5), ejecución directa sin delegados.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("carpeta", help="carpeta con capturas .npz")
    p.add_argument("--salida", help="directorio de resultados (default: carpeta)")
    p.add_argument("--placa", help="sobrescribe la etiqueta de las capturas")
    p.add_argument("--pre", type=int, default=20)
    p.add_argument("--post", type=int, default=120)
    p.add_argument("--armonicos", type=int, default=LINE_HARMONICS)
    p.add_argument("--busqueda-hz", type=float, default=LINE_SEARCH_HZ)
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    files = capture_files(args.carpeta)
    if not files:
        raise SystemExit(f"No hay .npz en {args.carpeta}")
    records = []
    for path in files:
        cap = load_capture(path)
        fs = float(scalar(cap["fs"], 2604.0))
        samples = np.asarray(cap["samples"], dtype=np.float64)
        flags = np.asarray(cap["flags"], dtype=np.uint8)
        if samples.size != flags.size:
            raise SystemExit(f"Longitudes distintas en {path}")
        records.append({"path": path, "samples": samples, "flags": flags, "fs": fs,
                        "scenario": str(cap.get("scenario", "")),
                        "placa": str(cap.get("placa", "sin_etiqueta")),
                        "clean": preprocess(samples, fs, args.armonicos, args.busqueda_hz)})
    placa = args.placa or records[0]["placa"]
    output = Path(args.salida or args.carpeta); output.mkdir(parents=True, exist_ok=True)
    signatures = {}
    for name, bit in FLAG_TYPES.items():
        learned = learn_type(records, bit, args.pre, args.post)
        if learned:
            signatures[name] = learned
            print(f"{name}: {learned['events']} eventos, SNR={learned['snr_template_vs_pre']:.2f}")
        else:
            print(f"{name}: sin eventos exclusivos suficientes")
    baseline = baseline_stats(records)
    document = {"schema_version": 1, "placa": placa,
                "fecha": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "preprocessing": {"offset": "median", "line_f0_hz": 50.0,
                                  "line_harmonics": args.armonicos, "line_search_hz": args.busqueda_hz},
                "baseline": baseline, "types": signatures}
    json_path = output / f"firmas_{placa}.json"
    json_dump(json_path, document)
    plotted = make_plots(output, placa, signatures, baseline)
    write_report(output / f"informe_{placa}.md", placa, files, baseline, signatures, plotted)
    print(f"Escrito: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
