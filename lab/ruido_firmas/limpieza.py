"""Evalua A-D contra deconvolucion E y actualiza el JSON de firmas."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
from scipy import signal

import firmas
from comun import FLAG_TYPES, apply_method, capture_files, json_dump, load_capture, preprocess, scalar

METHODS = [
    ("A_linear", "linear", {"margin": 2}),
    ("B_cubic", "cubic", {"margin": 2}),
    ("C_ar", "ar", {"margin": 2, "order": 12}),
    ("D_wavelet", "wavelet", {"margin": 2, "level": 3}),
    ("E_deconvolution", "template", {"offset": True}),
]


def band_power(x, fs, lo, hi):
    f, p = signal.welch(x, fs, nperseg=min(4096, len(x)))
    mask = (f >= lo) & (f <= hi)
    return float(np.trapezoid(p[mask], f[mask])) if np.count_nonzero(mask) > 1 else 0.0


def highpass(x, fs, cutoff=150.0):
    sos = signal.butter(4, cutoff, "highpass", fs=fs, output="sos")
    return signal.sosfiltfilt(sos, x)


def web_lowpass(x, fs):
    taps = signal.firwin(101, min(200.0, fs * 0.45), fs=fs)
    return signal.filtfilt(taps, [1.0], x)


def synthetic_signals(n, fs, amplitude):
    t = np.arange(n) / fs
    result = {f"sine_{freq:g}Hz": amplitude * np.sin(2 * np.pi * freq * t)
              for freq in (5, 15, 30, 50)}
    result["chirp_10_80Hz"] = amplitude * signal.chirp(t, 10, t[-1] if n > 1 else 1, 80)
    return result


def _template_spec(template, pre):
    return {"pre": pre, "onset": template["onset"].tolist(),
            "offset": template["offset"].tolist() if template["offset"] is not None else None,
            "method": "template"}


def oos_template_specs(records, document):
    estimation = document["estimation"]
    pre, length = int(estimation["pre"]), int(estimation["largo"])
    hp, damp = estimation.get("hp_hz"), float(estimation.get("damp", 0.5))
    offsets = set(document.get("offset_comparison", {}).get("selected", []))
    result = [{name: None for name in FLAG_TYPES} for _ in records]
    folds = [(list(range(0, len(records), 2)), list(range(1, len(records), 2))),
             (list(range(1, len(records), 2)), list(range(0, len(records), 2)))]
    for train, test in folds:
        if not train or not test:
            continue
        learned = firmas.fit_joint_templates(records, pre, length, hp, damp, offsets, train)
        for index in test:
            for name in FLAG_TYPES:
                result[index][name] = _template_spec(learned[name], pre)
    return result


def _apply(x, flags, bit, spec, method, params):
    return apply_method(x, flags, bit, spec, method, params)


def evaluate_type(records, name, bit, spec, oos_specs, base_powers, has_pywt):
    relevant = [(i, r) for i, r in enumerate(records) if np.any(r["flags"] & bit)]
    evaluations = []
    for label, method, params in METHODS:
        if method == "wavelet" and not has_pywt:
            continue
        before_hf, after_hf = [], []
        bands_before = {(1, 100): [], (10, 50): []}
        bands_after = {(1, 100): [], (10, 50): []}
        chain_before = {(1, 100): [], (10, 50): []}
        chain_after = {(1, 100): [], (10, 50): []}
        preservation = []
        representative_done = False
        valid = True
        for index, record in relevant:
            x, flags, fs = record["clean"], record["flags"], record["fs"]
            use_spec = oos_specs[index][name] if method == "template" else spec
            cleaned = _apply(x, flags, bit, use_spec, method, params)
            if not np.all(np.isfinite(cleaned)):
                valid = False
                break
            before_hf.append(highpass(x, fs)); after_hf.append(highpass(cleaned, fs))
            pre_fir, post_fir = web_lowpass(x, fs), web_lowpass(cleaned, fs)
            for band in bands_before:
                bands_before[band].append(band_power(x, fs, *band))
                bands_after[band].append(band_power(cleaned, fs, *band))
                chain_before[band].append(band_power(pre_fir, fs, *band))
                chain_after[band].append(band_power(post_fir, fs, *band))
            if not representative_done:
                amplitude = max(float(np.std(x)), 1.0)
                reference = cleaned
                for signal_name, injected in synthetic_signals(x.size, fs, amplitude).items():
                    with_signal = _apply(x + injected, flags, bit, use_spec, method, params)
                    component = with_signal - reference
                    denom = max(float(np.sqrt(np.mean(injected ** 2))), 1e-18)
                    preservation.append({"signal": signal_name,
                                         "normalized_rmse": float(np.sqrt(np.mean((component - injected) ** 2)) / denom)})
                representative_done = True
        if not valid or not before_hf:
            continue
        bh, ah = np.concatenate(before_hf), np.concatenate(after_hf)
        hf_ratio = float(np.var(ah) / max(np.var(bh), 1e-18))
        preservation_mean = float(np.mean([item["normalized_rmse"] for item in preservation]))
        bands = {}
        for band in bands_before:
            key = f"{band[0]}_{band[1]}_hz"
            before = float(np.mean(bands_before[band])); after = float(np.mean(bands_after[band]))
            cb = float(np.mean(chain_before[band])); ca = float(np.mean(chain_after[band]))
            base = float(base_powers.get(band, np.nan))
            bands[key] = {"before_power": before, "after_power": after,
                          "after_vs_before": after / max(before, 1e-18),
                          "before_vs_base": before / max(base, 1e-18),
                          "after_vs_base": after / max(base, 1e-18),
                          "web_chain_before_power": cb, "web_chain_after_power": ca,
                          "web_chain_after_vs_before": ca / max(cb, 1e-18)}
        # La señal útil vive en 1--100 Hz: una reducción HF no compensa
        # deformar un seno/chirp ni mover apreciablemente la banda 10--50 Hz.
        preservation_penalty = 8.0 * preservation_mean
        inband_penalty = abs(np.log(max(bands["10_50_hz"]["after_vs_before"], 1e-12)))
        base_penalty = 0.02 * abs(np.log(max(bands["10_50_hz"]["after_vs_base"], 1e-12)))
        score = hf_ratio + preservation_penalty + inband_penalty + base_penalty
        evaluations.append({"label": label, "method": method, "parameters": params,
                            "hf_residual_variance_ratio": hf_ratio,
                            "hf_explained_pct": 100.0 * (1.0 - hf_ratio),
                            "residual_vs_before": float(np.sqrt(max(hf_ratio, 0.0))),
                            "bands": bands, "signal_preservation": preservation,
                            "signal_error_mean_normalized_rmse": preservation_mean,
                            "score": float(score)})
    evaluations.sort(key=lambda item: item["score"])
    return evaluations


def base_band_powers(records):
    base = [r for r in records if r["scenario"] == "base_clasico"]
    return {band: float(np.mean([band_power(r["clean"], r["fs"], *band) for r in base]))
            for band in ((1, 100), (10, 50))} if base else {}


def none_summary(reference):
    result = json.loads(json.dumps(reference))
    result.update({"label": "none", "method": "none", "parameters": {},
                   "hf_residual_variance_ratio": 1.0, "hf_explained_pct": 0.0,
                   "residual_vs_before": 1.0,
                   "signal_error_mean_normalized_rmse": 0.0, "signal_preservation": [],
                   "score": 1.0})
    for band in result["bands"].values():
        band["after_power"] = band["before_power"]
        band["after_vs_before"] = 1.0
        band["after_vs_base"] = band["before_vs_base"]
        band["web_chain_after_power"] = band["web_chain_before_power"]
        band["web_chain_after_vs_before"] = 1.0
    return result


def whole_chain(records, document):
    result = {(1, 100): [[], []], (10, 50): [[], []]}
    for record in records:
        if not np.any(record["flags"]):
            continue
        x, flags, fs = record["clean"], record["flags"], record["fs"]
        cleaned = x.copy()
        for name in ("I2C", "SD_IO", "SD_SYNC", "RADIO_TX", "AP_BEACON", "MASTER_RX"):
            spec = document["types"][name]
            cleaned = apply_method(cleaned, flags, FLAG_TYPES[name], spec, spec.get("method"))
        before, after = web_lowpass(x, fs), web_lowpass(cleaned, fs)
        for band in result:
            result[band][0].append(band_power(before, fs, *band))
            result[band][1].append(band_power(after, fs, *band))
    return {f"{lo}_{hi}_hz": {"before_power": float(np.mean(values[0])),
                              "after_power": float(np.mean(values[1])),
                              "after_vs_before": float(np.mean(values[1]) / max(np.mean(values[0]), 1e-18))}
            for (lo, hi), values in result.items()}


def write_report(path, document, summaries, has_pywt):
    placa = document.get("placa", "placa")
    lines = [f"# Informe de firmas y limpieza — {placa}", "",
             f"Deconvolución conjunta: {document['cross_validation']['explained_pct']:.2f} % de varianza HF "
             "explicada fuera de muestra.", "",
             "| Fuente | EV drop-one | SNR bootstrap | Sig. | Recomendado | HF explicada | 1–100 después/antes | 10–50 después/antes | 10–50 después/base | Error señal |",
             "|---|---:|---:|---|---|---:|---:|---:|---:|---:|"]
    for name, best in summaries.items():
        spec = document["types"][name]
        bands = best["bands"]
        lines.append(f"| {name} | {spec['explained_pct']:.3f} % | {spec['template_snr']:.2f} | "
                     f"{'sí' if spec['significant'] else 'no'} | "
                     f"{spec['method']} | {best['hf_explained_pct']:.2f} % | "
                     f"{bands['1_100_hz']['after_vs_before']:.4f} | "
                     f"{bands['10_50_hz']['after_vs_before']:.4f} | "
                     f"{bands['10_50_hz']['after_vs_base']:.4f} | "
                     f"{best['signal_error_mean_normalized_rmse']:.4f} |")
    offsets = document["offset_comparison"]
    hp = document["hp_comparison"]
    lines += ["", f"Offsets: sin={offsets['without_offsets_pct']:.2f} %, todos="
              f"{offsets['all_offsets_pct']:.2f} %, seleccionados={', '.join(offsets['selected']) or 'ninguno'}.",
              f"Estimación: HP 150 Hz={hp['150_hz_pct']:.2f} %; sin HP={hp['none_pct']:.2f} %.",
              f"PyWavelets/SWT: {'evaluado' if has_pywt else 'no disponible'}.",
              "Cadena web: offset → notch de línea → I2C → SD → TX → beacon/RX → FIR LP 200 Hz (101 taps).",
              "", "---", "Proveniencia: Codex, ejecución directa sin delegados.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


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
        records.append({"path": path, "samples": samples,
                        "flags": np.asarray(cap["flags"], dtype=np.uint8), "fs": fs,
                        "scenario": str(cap.get("scenario", "")),
                        "clean": preprocess(samples, fs, int(prep.get("line_harmonics", 3)),
                                            float(prep.get("line_search_hz", 2.0)))})
    active = [r for r in records if np.any(r["flags"])]
    has_pywt = importlib.util.find_spec("pywt") is not None
    print("PyWavelets disponible: método D habilitado." if has_pywt else
          "PyWavelets no disponible: método D omitido.")
    oos_specs = oos_template_specs(active, document)
    base_powers = base_band_powers(records)
    summaries = {}
    for name, bit in FLAG_TYPES.items():
        spec = document["types"][name]
        evaluations = evaluate_type(active, name, bit, spec, oos_specs, base_powers, has_pywt)
        if not evaluations:
            continue
        deconv = next(item for item in evaluations if item["method"] == "template")
        web_candidates = [item for item in evaluations if item["method"] in {"template", "linear", "cubic"}]
        best = min(web_candidates, key=lambda item: item["score"])
        if not spec.get("significant", False) or spec.get("explained_pct", 0.0) <= 0:
            method, parameters = "none", {}
            chosen = none_summary(deconv)
        elif best["method"] == "template":
            method, parameters, chosen = "template", {"offset": spec.get("offset") is not None}, best
        else:
            method, parameters, chosen = "interp", {"kind": best["method"], "margin": 2}, best
        spec["method"] = method
        spec["recommended_method"] = {"method": method, "parameters": parameters,
                                      "evaluated_as": chosen["label"]}
        spec["cleaning_evaluation"] = evaluations
        spec["in_band_effect"] = chosen["bands"]
        spec["preservation_error"] = chosen["signal_error_mean_normalized_rmse"]
        summaries[name] = chosen
        print(f"{name}: {method} ({chosen['label']}), HF={chosen['hf_explained_pct']:.2f} %, "
              f"error señal={chosen['signal_error_mean_normalized_rmse']:.4f}")
    document["whole_web_chain"] = whole_chain(active, document)
    output = Path(args.salida) if args.salida else signature_path
    json_dump(output, document)
    write_report(output.with_name(f"informe_{document.get('placa', 'placa')}.md"),
                 document, summaries, has_pywt)
    print(f"Firmas actualizadas: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
