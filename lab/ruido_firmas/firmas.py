"""Estima firmas superpuestas mediante regresion FIR conjunta (deconvolucion)."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import signal, sparse
from scipy.sparse.linalg import lsqr

from comun import (FLAG_TYPES, LINE_HARMONICS, LINE_SEARCH_HZ, aligned_segments,
                   capture_files, event_runs, exclusive_runs, json_dump, load_capture,
                   preprocess, scalar)

VARIABLE_RUN_TYPES = {"SD_IO", "RADIO_TX", "I2C"}


def _hp_value(text):
    if text is None or str(text).strip().lower() in {"none", "ninguno", "off", "0"}:
        return None
    value = float(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("--hp debe ser > 0 o 'none'")
    return value


def estimation_signal(record, hp):
    x = np.asarray(record.get("clean", record["samples"]), dtype=np.float64)
    if hp is None:
        return x
    fs = float(record.get("fs", 2604.0))
    if not 0 < hp < fs / 2:
        raise ValueError(f"hp={hp} fuera de (0, Nyquist={fs / 2:g})")
    sos = signal.butter(4, hp, "highpass", fs=fs, output="sos")
    return signal.sosfiltfilt(sos, x)


def parameter_layout(length, offset_types=()):
    layout = []
    for name in FLAG_TYPES:
        layout.append((name, "onset", slice(len(layout) * length, (len(layout) + 1) * length)))
    for name in FLAG_TYPES:
        if name in offset_types:
            layout.append((name, "offset", slice(len(layout) * length, (len(layout) + 1) * length)))
    return layout


def build_design(flags, pre, length, offset_types=()):
    flags = np.asarray(flags, dtype=np.uint8)
    layout = parameter_layout(length, offset_types)
    columns = {(name, edge): section.start for name, edge, section in layout}
    rows, cols = [], []
    for name, bit in FLAG_TYPES.items():
        for start, end in event_runs(flags, bit):
            centers = [("onset", start)]
            if name in offset_types:
                centers.append(("offset", end))
            for edge, center in centers:
                base = columns[(name, edge)]
                lo = center - pre
                first = max(0, -lo)
                last = min(length, flags.size - lo)
                if last <= first:
                    continue
                rows.extend(range(lo + first, lo + last))
                cols.extend(range(base + first, base + last))
    values = np.ones(len(rows), dtype=np.float64)
    return sparse.csr_matrix((values, (rows, cols)), shape=(flags.size, len(layout) * length)), layout


def _prepared(records, pre, length, hp, offset_types):
    result = []
    for record in records:
        y = estimation_signal(record, hp)
        x, layout = build_design(record["flags"], pre, length, offset_types)
        result.append((x, y, layout))
    return result


def _fit_prepared(prepared, indices, damp):
    if not indices:
        raise ValueError("no hay capturas para ajustar")
    x = sparse.vstack([prepared[i][0] for i in indices], format="csr")
    y = np.concatenate([prepared[i][1] for i in indices])
    return lsqr(x, y, damp=damp, atol=1e-7, btol=1e-7, iter_lim=1200)[0]


def fit_joint_templates(records, pre, length, hp=150.0, damp=0.5, offset_types=(), indices=None):
    """Ajusta una plantilla FIR por marca; API reutilizada por autotest/limpieza."""
    prepared = _prepared(records, pre, length, hp, set(offset_types))
    selected = list(range(len(records))) if indices is None else list(indices)
    coef = _fit_prepared(prepared, selected, damp)
    templates = {name: {"onset": np.zeros(length), "offset": None} for name in FLAG_TYPES}
    for name, edge, section in prepared[0][2]:
        templates[name][edge] = coef[section].copy()
    return templates


def cross_validate(records, pre, length, hp, damp, offset_types=()):
    """Even/odd por captura, nunca por evento; informa aporte drop-one-type."""
    prepared = _prepared(records, pre, length, hp, set(offset_types))
    folds = [(list(range(0, len(records), 2)), list(range(1, len(records), 2))),
             (list(range(1, len(records), 2)), list(range(0, len(records), 2)))]
    all_y, all_residual = [], []
    drop_residuals = {name: [] for name in FLAG_TYPES}
    fold_scores = []
    layout = prepared[0][2]
    sections = {name: [section for item, _, section in layout if item == name]
                for name in FLAG_TYPES}
    for train, test in folds:
        if not train or not test:
            continue
        coef = _fit_prepared(prepared, train, damp)
        fold_y, fold_res = [], []
        for index in test:
            x, y, _ = prepared[index]
            prediction = x @ coef
            residual = y - prediction
            all_y.append(y); all_residual.append(residual)
            fold_y.append(y); fold_res.append(residual)
            for name in FLAG_TYPES:
                type_prediction = np.zeros_like(y)
                for section in sections[name]:
                    type_prediction += x[:, section] @ coef[section]
                drop_residuals[name].append(residual + type_prediction)
        fy, fr = np.concatenate(fold_y), np.concatenate(fold_res)
        fold_scores.append(100.0 * (1.0 - np.var(fr) / max(np.var(fy), 1e-18)))
    y = np.concatenate(all_y)
    residual = np.concatenate(all_residual)
    total_var = max(np.var(y), 1e-18)
    overall = 100.0 * (1.0 - np.var(residual) / total_var)
    by_type = {}
    for name in FLAG_TYPES:
        without = np.concatenate(drop_residuals[name])
        by_type[name] = 100.0 * (np.var(without) - np.var(residual)) / total_var
    return {"explained_pct": float(overall), "fold_explained_pct": fold_scores,
            "drop_one_type_pct": by_type}


def bootstrap_templates(records, pre, length, hp, damp, offset_types, repetitions=100, seed=2929):
    prepared = _prepared(records, pre, length, hp, set(offset_types))
    layout = prepared[0][2]
    rng = np.random.default_rng(seed)
    draws = []
    for _ in range(repetitions):
        indices = rng.integers(0, len(records), size=len(records)).tolist()
        draws.append(_fit_prepared(prepared, indices, damp))
    draws = np.asarray(draws)
    result = {name: {"onset": None, "offset": None} for name in FLAG_TYPES}
    for name, edge, section in layout:
        values = draws[:, section]
        result[name][edge] = {"low": np.percentile(values, 2.5, axis=0),
                              "high": np.percentile(values, 97.5, axis=0),
                              "std": np.std(values, axis=0)}
    return result


def exclusive_diagnostic(records, bit, pre, length):
    post = length - pre - 1
    rows = []
    for record in records:
        events = exclusive_runs(record["flags"], bit, pre, post)
        segments, _ = aligned_segments(estimation_signal(record, record.get("hp")), events, pre, post)
        rows.extend(segments)
    if not rows:
        return {"events": 0, "mean": None}
    return {"events": len(rows), "mean": np.mean(np.asarray(rows), axis=0).tolist()}


def _stats(values):
    values = np.asarray(values, dtype=np.float64)
    if not values.size:
        return {"mean": None, "median": None, "std": None, "min": None, "max": None}
    return {key: float(fun(values)) for key, fun in (("mean", np.mean), ("median", np.median),
                                                      ("std", np.std), ("min", np.min), ("max", np.max))}


def baseline_stats(records):
    base = [r for r in records if r["scenario"] == "base_clasico"]
    if not base:
        return {"captures": 0, "first_difference_rms_counts": None, "bands": {}}
    diff_rms = [np.sqrt(np.mean(np.diff(r["clean"]) ** 2)) for r in base]
    bands = {}
    for lo, hi in ((1, 100), (10, 50)):
        powers = []
        for r in base:
            f, p = signal.welch(r["clean"], r["fs"], nperseg=min(4096, r["clean"].size))
            mask = (f >= lo) & (f <= hi)
            powers.append(float(np.trapezoid(p[mask], f[mask])))
        bands[f"{lo}_{hi}_hz_power"] = _stats(powers)
    return {"captures": len(base), "first_difference_rms_counts": _stats(diff_rms), "bands": bands}


def make_plots(output, placa, signatures):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    for name, spec in signatures.items():
        axis = np.arange(spec["largo"]) - spec["pre"]
        mean = np.asarray(spec["onset"])
        low = np.asarray(spec["bootstrap_ci"]["onset_low"])
        high = np.asarray(spec["bootstrap_ci"]["onset_high"])
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(axis, mean, label="plantilla conjunta")
        ax.fill_between(axis, low, high, alpha=0.25, label="IC bootstrap 95 %")
        if spec["offset"] is not None:
            ax.plot(axis, spec["offset"], label="flanco final")
        ax.axhline(0, color="0.5", linewidth=0.7); ax.axvline(0, color="k", linewidth=0.8)
        ax.set(title=f"{placa}: {name}", xlabel="muestras desde el flanco", ylabel="cuentas ADC")
        ax.grid(True, alpha=0.25); ax.legend(); fig.tight_layout()
        fig.savefig(output / f"firma_{placa}_{name.lower()}.png", dpi=150)
        plt.close(fig)
    return True


def write_report(path, placa, files, document, plotted):
    cv = document["cross_validation"]
    lines = [f"# Firmas de ruido — {placa}", "",
             f"Capturas: {len(files)}; FIR: pre={document['estimation']['pre']}, "
             f"L={document['estimation']['largo']}, damp={document['estimation']['damp']}.",
             f"Varianza HF explicada fuera de muestra: {cv['explained_pct']:.2f} %.", "",
             "| Fuente | Eventos | Explicada drop-one | Pico (cuentas) | SNR bootstrap | Significativa | Método |",
             "|---|---:|---:|---:|---:|---|---|"]
    for name, spec in document["types"].items():
        lines.append(f"| {name} | {spec['events']} | {spec['explained_pct']:.3f} % | "
                     f"{max(abs(v) for v in spec['onset']):.3f} | {spec['template_snr']:.2f} | "
                     f"{'sí' if spec['significant'] else 'no'} | {spec['method']} |")
    offsets = document["offset_comparison"]
    hp = document["hp_comparison"]
    lines += ["", f"Sin offsets: {offsets['without_offsets_pct']:.2f} %; con offsets candidatos: "
              f"{offsets['all_offsets_pct']:.2f} %; seleccionados: {', '.join(offsets['selected']) or 'ninguno'}.",
              f"HP 150 Hz: {hp['150_hz_pct']:.2f} %; sin HP: {hp['none_pct']:.2f} %.",
              "El promedio exclusivo se conserva en `exclusive_diagnostic`, pero no gobierna las firmas.",
              "Los PNG se generaron." if plotted else "No se generaron PNG.", "", "---",
              "Proveniencia: Codex, ejecución directa sin delegados.", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("carpeta", help="carpeta con capturas .npz")
    p.add_argument("--salida", help="directorio de resultados (default: carpeta)")
    p.add_argument("--placa", help="sobrescribe la etiqueta de las capturas")
    p.add_argument("--pre", type=int, default=4)
    p.add_argument("--largo", type=int, default=32)
    p.add_argument("--hp", type=_hp_value, default=150.0,
                   help="corte pasa-altos solo para estimación; 'none' lo desactiva")
    p.add_argument("--damp", type=float, default=0.5)
    p.add_argument("--bootstrap", type=int, default=100)
    p.add_argument("--armonicos", type=int, default=LINE_HARMONICS)
    p.add_argument("--busqueda-hz", type=float, default=LINE_SEARCH_HZ)
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if args.pre < 0 or args.largo <= args.pre or args.damp < 0 or args.bootstrap < 20:
        raise SystemExit("requiere pre>=0, largo>pre, damp>=0 y bootstrap>=20")
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
                        "clean": preprocess(samples, fs, args.armonicos, args.busqueda_hz),
                        "hp": args.hp})
    active = [r for r in records if np.any(r["flags"])]
    if len(active) < 2:
        raise SystemExit("Se necesitan al menos dos capturas con marcas")
    placa = args.placa or records[0]["placa"]
    output = Path(args.salida or args.carpeta); output.mkdir(parents=True, exist_ok=True)

    cv_none_offset = cross_validate(active, args.pre, args.largo, args.hp, args.damp)
    cv_all_offset = cross_validate(active, args.pre, args.largo, args.hp, args.damp, VARIABLE_RUN_TYPES)
    selected_offsets = []
    for name in sorted(VARIABLE_RUN_TYPES):
        trial = cross_validate(active, args.pre, args.largo, args.hp, args.damp, {name})
        if trial["explained_pct"] > cv_none_offset["explained_pct"]:
            selected_offsets.append(name)
    final_cv = cross_validate(active, args.pre, args.largo, args.hp, args.damp, selected_offsets)
    hp150 = cross_validate(active, args.pre, args.largo, 150.0, args.damp, selected_offsets)
    hpnone = cross_validate(active, args.pre, args.largo, None, args.damp, selected_offsets)
    templates = fit_joint_templates(active, args.pre, args.largo, args.hp, args.damp, selected_offsets)
    bootstrap = bootstrap_templates(active, args.pre, args.largo, args.hp, args.damp,
                                    selected_offsets, args.bootstrap)

    signatures = {}
    for name, bit in FLAG_TYPES.items():
        onset = templates[name]["onset"]
        onset_ci = bootstrap[name]["onset"]
        significant_samples = (onset_ci["low"] > 0) | (onset_ci["high"] < 0)
        significant = bool(np.any(significant_samples))
        offset = templates[name]["offset"]
        offset_ci = bootstrap[name]["offset"]
        diagnostic = exclusive_diagnostic(active, bit, args.pre, args.largo)
        events = sum(len(event_runs(r["flags"], bit)) for r in active)
        bootstrap_snr = float(np.max(np.abs(onset) / np.maximum(onset_ci["std"], 1e-12)))
        spec = {"method": "template" if significant else "none",
                "pre": args.pre, "largo": args.largo,
                "onset": onset.tolist(), "offset": offset.tolist() if offset is not None else None,
                "units": "counts", "significant": significant,
                "explained_pct": float(final_cv["drop_one_type_pct"][name]), "events": events,
                "template_snr": bootstrap_snr,
                "bootstrap_ci": {
                    "onset_low": onset_ci["low"].tolist(), "onset_high": onset_ci["high"].tolist(),
                    "onset_std": onset_ci["std"].tolist(),
                    "offset_low": offset_ci["low"].tolist() if offset_ci else None,
                    "offset_high": offset_ci["high"].tolist() if offset_ci else None,
                    "offset_std": offset_ci["std"].tolist() if offset_ci else None},
                "exclusive_diagnostic": diagnostic}
        signatures[name] = spec
        print(f"{name}: EV={spec['explained_pct']:.3f} %, pico={np.max(np.abs(onset)):.3f}, "
              f"significativa={'sí' if significant else 'no'}")

    baseline = baseline_stats(records)
    document = {"schema_version": 2, "placa": placa,
                "fecha": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
                "preprocessing": {"offset": "median", "line_f0_hz": 50.0,
                                  "line_harmonics": args.armonicos, "line_search_hz": args.busqueda_hz},
                "estimation": {"method": "joint_fir_deconvolution", "pre": args.pre,
                               "largo": args.largo, "hp_hz": args.hp, "damp": args.damp,
                               "bootstrap_repetitions": args.bootstrap},
                "cross_validation": final_cv,
                "offset_comparison": {"without_offsets_pct": cv_none_offset["explained_pct"],
                                      "all_offsets_pct": cv_all_offset["explained_pct"],
                                      "selected": selected_offsets},
                "hp_comparison": {"150_hz_pct": hp150["explained_pct"],
                                  "none_pct": hpnone["explained_pct"]},
                "baseline": baseline, "types": signatures}
    json_path = output / f"firmas_{placa}.json"
    json_dump(json_path, document)
    plotted = make_plots(output, placa, signatures)
    write_report(output / f"informe_{placa}.md", placa, files, document, plotted)
    print(f"Escrito: {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
