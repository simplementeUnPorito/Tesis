"""Compara métodos de limpieza, preservación de señal y actualiza firmas JSON."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy import signal

from comun import (FLAG_TYPES, apply_method, capture_files, json_dump, load_capture,
                   preprocess, scalar, windows_from_flags)


def masked_rms(x, mask):
    values = np.asarray(x)[mask]
    return float(np.sqrt(np.mean(values ** 2))) if values.size else None


def band_rms(x, fs, lo=1.0, hi=100.0):
    f, p = signal.welch(x, fs, nperseg=min(4096, len(x)))
    mask = (f >= lo) & (f <= hi)
    return float(np.sqrt(np.trapezoid(p[mask], f[mask]))) if np.count_nonzero(mask) > 1 else 0.0


def synthetic_signals(n, fs, amplitude):
    t = np.arange(n) / fs
    result = {f"sine_{freq:g}Hz": amplitude * np.sin(2 * np.pi * freq * t)
              for freq in (5, 15, 30, 50)}
    result["chirp_10_80Hz"] = amplitude * signal.chirp(t, 10, t[-1] if n > 1 else 1, 80)
    return result


def candidate_methods(has_pywt):
    result = [
        ("template", {"offset": True}),
        ("template_xcorr", {"align": 2, "offset": True}),
        ("linear", {"margin": 2}),
        ("cubic", {"margin": 2}),
        ("ar", {"margin": 2, "order": 12}),
    ]
    if has_pywt:
        result.extend(("wavelet", {"margin": 2, "level": level}) for level in (3, 4))
    return result


def evaluate_type(records, bit, spec, base_rms, has_pywt):
    evaluations = []
    relevant = [r for r in records if np.any(r["flags"] & bit)]
    for method, params in candidate_methods(has_pywt):
        marked_before, marked_after, unmarked, band_before, band_after = [], [], [], [], []
        preservation = []
        representative_done = False
        valid = True
        for record in relevant:
            x, flags, fs = record["clean"], record["flags"], record["fs"]
            mask = np.zeros(x.size, dtype=bool)
            for lo, hi in windows_from_flags(flags, bit, int(params.get("margin", 2))):
                mask[lo:hi] = True
            if not np.any(mask):
                continue
            cleaned = apply_method(x, flags, bit, spec, method, params)
            if not np.all(np.isfinite(cleaned)):
                valid = False
                break
            marked_before.append(masked_rms(x, mask)); marked_after.append(masked_rms(cleaned, mask))
            unmarked.append(masked_rms(x, ~mask)); band_before.append(band_rms(x, fs)); band_after.append(band_rms(cleaned, fs))
            if not representative_done:
                amp = float(np.std(x[~mask])) if np.any(~mask) else float(np.std(x))
                amp = max(amp, 1.0)
                clean_reference = cleaned
                for label, injected in synthetic_signals(x.size, fs, amp).items():
                    clean_injected = apply_method(x + injected, flags, bit, spec, method, params)
                    if not np.all(np.isfinite(clean_injected)):
                        valid = False
                        break
                    error = (clean_injected - clean_reference) - injected
                    preservation.append({"signal": label,
                                         "normalized_rmse": float(np.sqrt(np.mean(error ** 2)) / amp)})
                representative_done = True
            if not valid:
                break
        if not valid or not marked_after:
            continue
        before = float(np.mean(marked_before)); after = float(np.mean(marked_after))
        preservation_error = float(np.mean([p["normalized_rmse"] for p in preservation]))
        floor = float(base_rms) if base_rms is not None else float(np.mean(unmarked))
        residual_ratio = after / max(floor, 1e-12)
        reduction = after / max(before, 1e-12)
        score = residual_ratio + 2.0 * preservation_error
        evaluations.append({"method": method, "parameters": params,
                            "marked_rms_before": before, "marked_rms_after": after,
                            "unmarked_rms": float(np.mean(unmarked)), "base_classic_rms": base_rms,
                            "residual_vs_base": residual_ratio, "residual_vs_before": reduction,
                            "band_1_100_rms_before": float(np.mean(band_before)),
                            "band_1_100_rms_after": float(np.mean(band_after)),
                            "signal_preservation": preservation,
                            "signal_error_mean_normalized_rmse": preservation_error,
                            "score": score})
    evaluations.sort(key=lambda item: item["score"])
    return evaluations


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("carpeta", help="carpeta con capturas .npz")
    p.add_argument("--firmas", required=True, help="firmas_<placa>.json generado por firmas.py")
    p.add_argument("--salida", help="JSON de salida; por defecto actualiza --firmas")
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    files = capture_files(args.carpeta)
    if not files:
        raise SystemExit(f"No hay capturas .npz en {args.carpeta}")
    signature_path = Path(args.firmas)
    document = json.loads(signature_path.read_text(encoding="utf-8"))
    records = []
    prep = document.get("preprocessing", {})
    for path in files:
        cap = load_capture(path)
        fs = float(scalar(cap["fs"], 2604.0))
        samples = np.asarray(cap["samples"], dtype=np.float64)
        records.append({"flags": np.asarray(cap["flags"], dtype=np.uint8), "fs": fs,
                        "clean": preprocess(samples, fs, int(prep.get("line_harmonics", 3)),
                                            float(prep.get("line_search_hz", 2.0)))})
    base = document.get("baseline", {}).get("rms_counts", {})
    base_rms = base.get("mean") if isinstance(base, dict) else None
    has_pywt = importlib.util.find_spec("pywt") is not None
    print("PyWavelets disponible: se evaluará SWT db4." if has_pywt else
          "NOTA: PyWavelets no está instalado; se omiten los métodos SWT/db4.")
    summaries = {}
    for name, bit in FLAG_TYPES.items():
        spec = document.get("types", {}).get(name)
        if not spec:
            continue
        evaluations = evaluate_type(records, bit, spec, base_rms, has_pywt)
        if not evaluations:
            print(f"{name}: sin ventanas marcadas")
            continue
        best_overall = evaluations[0]
        best = next(item for item in evaluations
                    if item["method"] in {"template", "template_xcorr", "linear", "cubic"})
        if best["method"] in {"template", "template_xcorr"}:
            web_method = "template"
            web_params = dict(best["parameters"])
            web_params["align"] = 2 if best["method"] == "template_xcorr" else 0
        else:
            web_method = "interp"
            web_params = dict(best["parameters"])
            web_params["kind"] = best["method"]
        recommendation = {"method": web_method, "parameters": web_params,
                          "evaluated_as": best["method"], "score": best["score"],
                          "residual_vs_base": best["residual_vs_base"],
                          "signal_error_normalized_rmse": best["signal_error_mean_normalized_rmse"]}
        spec["recommended_method"] = recommendation
        spec["method"] = web_method
        spec.update(web_params)
        spec["best_evaluated_method"] = {"method": best_overall["method"],
                                          "parameters": best_overall["parameters"],
                                          "score": best_overall["score"]}
        spec["cleaning_evaluation"] = evaluations
        summaries[name] = best
        print(f"{name}: web={web_method} ({best['method']}) residual/base={best['residual_vs_base']:.3f}, "
              f"error señal={best['signal_error_mean_normalized_rmse']:.3f}")
    output = Path(args.salida) if args.salida else signature_path
    json_dump(output, document)
    report = output.with_name(f"limpieza_{document.get('placa', 'placa')}.md")
    lines = [f"# Evaluación de limpieza — {document.get('placa', 'placa')}", "",
             "Puntaje = residual/piso base + 2 × error normalizado de preservación.", "",
             "| Fuente | Método | RMS residual/base | Error de señal | Banda 1–100 Hz (antes→después) |",
             "|---|---|---:|---:|---:|"]
    for name, best in summaries.items():
        lines.append(f"| {name} | {best['method']} | {best['residual_vs_base']:.3f} | "
                     f"{best['signal_error_mean_normalized_rmse']:.3f} | "
                     f"{best['band_1_100_rms_before']:.2f}→{best['band_1_100_rms_after']:.2f} |")
    if not has_pywt:
        lines += ["", "PyWavelets no estaba disponible; SWT/db4 quedó omitido sin instalar dependencias."]
    lines += ["", "---", "Proveniencia: Codex (GPT-5), ejecución directa sin delegados."]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Firmas actualizadas: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
