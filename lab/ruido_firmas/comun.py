"""Utilidades compartidas para calibrar y aplicar firmas de interferencia."""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy import interpolate, linalg, signal

FS_DEFAULT = 2604.0
LINE_F0 = 50.0
LINE_HARMONICS = 3
LINE_SEARCH_HZ = 2.0

FLAG_TYPES = {
    "SD_IO": 0x01,
    "SD_SYNC": 0x02,
    "RADIO_TX": 0x04,
    "I2C": 0x08,
    "AP_BEACON": 0x10,
    "MASTER_RX": 0x20,
}


def remove_offset(samples):
    x = np.asarray(samples, dtype=np.float64)
    return x - np.median(x) if x.size else x.copy()


def _sinusoid_fit_score(x, fs, freq, mean):
    if not (0.0 < freq < fs / 2.0):
        return -np.inf
    n = np.arange(x.size, dtype=np.float64)
    phase = 2.0 * np.pi * freq * n / fs
    c, s = np.cos(phase), np.sin(phase)
    y = x - mean
    cc, ss, cs = np.dot(c, c), np.dot(s, s), np.dot(c, s)
    yc, ys = np.dot(y, c), np.dot(y, s)
    det = cc * ss - cs * cs
    if not det > 1e-12:
        return -np.inf
    return (ss * yc * yc - 2.0 * cs * yc * ys + cc * ys * ys) / det


def _line_frequency_score(x, fs, base_freq, n_harmonics, mean):
    scores = []
    for k in range(1, n_harmonics + 1):
        freq = k * base_freq
        if freq >= fs / 2.0:
            break
        score = _sinusoid_fit_score(x, fs, freq, mean)
        if np.isfinite(score):
            scores.append(score)
    return float(np.sum(scores)) if scores else -np.inf


def estimate_line_frequency(x, fs, f0=LINE_F0, search_hz=LINE_SEARCH_HZ,
                            n_harmonics=LINE_HARMONICS):
    """Puerto de estimateLineFrequency de la web (81 puntos + refinado de 21)."""
    x = np.asarray(x, dtype=np.float64)
    span = max(0.0, float(search_hz or 0.0))
    if not (span > 0 and x.size >= 8 and fs > 0 and f0 > 0):
        return float(f0)
    mean = float(np.mean(x))
    lo = max(0.1, f0 - span)
    hi = min(fs / 2.0 - 1e-6, f0 + span)
    if not hi > lo:
        return float(f0)
    coarse = np.linspace(lo, hi, 81)
    scores = [_line_frequency_score(x, fs, f, n_harmonics, mean) for f in coarse]
    best = float(coarse[int(np.argmax(scores))])
    best_score = max(scores)
    step = (hi - lo) / 80.0
    for f in np.linspace(max(lo, best - step), min(hi, best + step), 21):
        score = _line_frequency_score(x, fs, float(f), n_harmonics, mean)
        if score > best_score:
            best, best_score = float(f), score
    return best


def harmonic_notch(x, fs, f0=LINE_F0, n_harmonics=LINE_HARMONICS,
                   search_hz=LINE_SEARCH_HZ):
    """Puerto del harmonicNotch web: ajuste LS conjunto de cos/sen y resta."""
    original = np.asarray(x)
    y = np.asarray(x, dtype=np.float64)
    nh = int(n_harmonics or 0)
    if not y.size or nh <= 0 or not (fs > 0 and f0 > 0):
        return original
    line_f0 = estimate_line_frequency(y, fs, f0, search_hz, nh)
    n = np.arange(y.size, dtype=np.float64)
    cols = []
    for k in range(1, nh + 1):
        if k * line_f0 >= fs / 2.0:
            break
        phase = 2.0 * np.pi * k * line_f0 * n / fs
        cols.extend((np.cos(phase), np.sin(phase)))
    if not cols or y.size <= len(cols):
        return original
    h = np.column_stack(cols)
    gram = h.T @ h
    rhs = h.T @ y
    try:
        coef = linalg.solve(gram, rhs, assume_a="sym")
    except linalg.LinAlgError:
        return original
    if not np.all(np.isfinite(coef)):
        return original
    return y - h @ coef


def preprocess(samples, fs, n_harmonics=LINE_HARMONICS, search_hz=LINE_SEARCH_HZ):
    return harmonic_notch(remove_offset(samples), fs, LINE_F0, n_harmonics, search_hz)


def load_capture(path):
    path = Path(path)
    with np.load(path, allow_pickle=False) as z:
        result = {key: z[key] for key in z.files}
    for key in ("scenario", "timestamp", "placa"):
        if key in result and np.asarray(result[key]).ndim == 0:
            result[key] = str(np.asarray(result[key]).item())
    return result


def capture_files(folder):
    return sorted(Path(folder).glob("*.npz"))


def event_runs(flags, bit):
    active = (np.asarray(flags, dtype=np.uint8) & bit) != 0
    edges = np.diff(np.r_[False, active, False].astype(np.int8))
    starts = np.flatnonzero(edges == 1)
    ends = np.flatnonzero(edges == -1)
    return list(zip(starts.tolist(), ends.tolist()))


def exclusive_runs(flags, bit, pre, post):
    flags = np.asarray(flags, dtype=np.uint8)
    other_mask = 0xFF ^ bit
    selected = []
    for start, end in event_runs(flags, bit):
        lo, hi = max(0, start - pre), min(flags.size, start + post + 1)
        if start >= pre and start + post < flags.size and not np.any(flags[lo:hi] & other_mask):
            selected.append((start, end))
    return selected


def aligned_segments(x, events, pre, post, template=None, max_shift=3):
    x = np.asarray(x, dtype=np.float64)
    width = pre + post + 1
    rows, shifts = [], []
    for start, _ in events:
        best_shift = 0
        if template is not None:
            scores = []
            for shift in range(-max_shift, max_shift + 1):
                row = x[start + shift - pre:start + shift + post + 1]
                scores.append(np.dot(row, template) if row.size == width else -np.inf)
            best_shift = int(np.argmax(scores)) - max_shift
        row = x[start + best_shift - pre:start + best_shift + post + 1]
        if row.size == width:
            rows.append(row)
            shifts.append(best_shift)
    return np.asarray(rows, dtype=np.float64), np.asarray(shifts, dtype=np.int16)


def windows_from_flags(flags, bit, margin=2):
    n = len(flags)
    windows = []
    for start, end in event_runs(flags, bit):
        lo, hi = max(0, start - margin), min(n, end + margin)
        if windows and lo <= windows[-1][1]:
            windows[-1] = (windows[-1][0], max(windows[-1][1], hi))
        else:
            windows.append((lo, hi))
    return windows


def _template_array(spec, which="onset"):
    value = spec.get(f"{which}_template", spec.get(which, {}).get("template", []))
    return np.asarray(value, dtype=np.float64)


def subtract_templates(x, flags, bit, spec, align=0, include_offset=True):
    out = np.asarray(x, dtype=np.float64).copy()
    pre = int(spec.get("pre", 20))
    onset = _template_array(spec, "onset")
    offset = _template_array(spec, "offset") if include_offset else np.empty(0)
    for start, end in event_runs(flags, bit):
        for center, templ in ((start, onset), (end, offset)):
            if not templ.size:
                continue
            best_shift = 0
            if align:
                scores = []
                for shift in range(-align, align + 1):
                    lo = center + shift - pre
                    seg = out[lo:lo + templ.size]
                    scores.append(abs(np.dot(seg, templ)) if seg.size == templ.size else -np.inf)
                best_shift = int(np.argmax(scores)) - align
            lo = center + best_shift - pre
            hi = lo + templ.size
            if lo < 0 or hi > out.size:
                continue
            denom = float(np.dot(templ, templ))
            amp = float(np.dot(out[lo:hi], templ) / denom) if denom > 0 else 0.0
            out[lo:hi] -= np.clip(amp, 0.0, 2.0) * templ
    return out


def interpolate_windows(x, windows, kind="linear"):
    out = np.asarray(x, dtype=np.float64).copy()
    for lo, hi in windows:
        anchors = np.r_[np.arange(max(0, lo - 4), lo), np.arange(hi, min(out.size, hi + 4))]
        if anchors.size < (4 if kind == "cubic" else 2):
            continue
        targets = np.arange(lo, hi)
        use_kind = kind if kind != "cubic" or anchors.size >= 4 else "linear"
        fun = interpolate.interp1d(anchors, out[anchors], kind=use_kind, fill_value="extrapolate")
        out[targets] = fun(targets)
    return out


def ar_interpolate_windows(x, windows, order=12, context=80):
    out = np.asarray(x, dtype=np.float64).copy()
    for lo, hi in windows:
        left = out[max(0, lo - context):lo]
        right = out[hi:min(out.size, hi + context)][::-1]
        length = hi - lo
        preds = []
        for side in (left, right):
            if side.size <= order + 2:
                preds.append(None)
                continue
            corr = np.correlate(side - np.mean(side), side - np.mean(side), mode="full")[side.size - 1:]
            try:
                coef = linalg.solve_toeplitz((corr[:order], corr[:order]), corr[1:order + 1])
                hist = list(side[-order:])
                pred = []
                for _ in range(length):
                    value = float(np.dot(coef, hist[-order:][::-1]))
                    pred.append(value); hist.append(value)
                preds.append(np.asarray(pred))
            except (linalg.LinAlgError, ValueError):
                preds.append(None)
        if preds[0] is not None and preds[1] is not None:
            weight = np.linspace(1.0, 0.0, length, endpoint=True)
            out[lo:hi] = weight * preds[0] + (1.0 - weight) * preds[1][::-1]
        elif preds[0] is not None:
            out[lo:hi] = preds[0]
        elif preds[1] is not None:
            out[lo:hi] = preds[1][::-1]
    return out


def apply_method(x, flags, bit, spec, method=None, params=None):
    params = dict(params or {})
    method = method or spec.get("recommended_method", {}).get("method") or spec.get("method", "interp")
    if method == "template":
        return subtract_templates(x, flags, bit, spec, align=0, include_offset=params.get("offset", True))
    if method == "template_xcorr":
        return subtract_templates(x, flags, bit, spec, align=int(params.get("align", 2)),
                                  include_offset=params.get("offset", True))
    margin = int(params.get("margin", spec.get("margin", 2)))
    windows = windows_from_flags(flags, bit, margin)
    if method in ("linear", "interp"):
        return interpolate_windows(x, windows, "linear")
    if method == "cubic":
        return interpolate_windows(x, windows, "cubic")
    if method == "ar":
        return ar_interpolate_windows(x, windows, int(params.get("order", 12)))
    if method == "wavelet":
        try:
            import pywt
        except ImportError as exc:
            raise RuntimeError("PyWavelets no está instalado; método wavelet omitido") from exc
        out = np.asarray(x, dtype=np.float64).copy()
        level = int(params.get("level", 3))
        for lo, hi in windows:
            length = hi - lo
            block = 2 ** level
            stop = min(out.size, lo + int(math.ceil(length / block)) * block)
            seg = out[lo:stop]
            if seg.size < block or seg.size % block:
                continue
            coeffs = pywt.swt(seg, "db4", level=level)
            sigma = np.median(np.abs(coeffs[-1][1])) / 0.6745
            threshold = sigma * math.sqrt(2.0 * math.log(max(2, seg.size)))
            cleaned = [(ca, pywt.threshold(cd, threshold, mode="soft")) for ca, cd in coeffs]
            out[lo:stop] = pywt.iswt(cleaned, "db4")
        return out
    raise ValueError(f"Método desconocido: {method}")


def json_dump(path, value):
    def safe(item):
        if isinstance(item, dict):
            return {str(key): safe(val) for key, val in item.items()}
        if isinstance(item, (list, tuple)):
            return [safe(val) for val in item]
        if isinstance(item, (float, np.floating)):
            return float(item) if math.isfinite(float(item)) else None
        if isinstance(item, np.integer):
            return int(item)
        return item
    Path(path).write_text(json.dumps(safe(value), ensure_ascii=False, indent=2,
                                     allow_nan=False) + "\n", encoding="utf-8")


def scalar(value, default=None):
    arr = np.asarray(value)
    return arr.item() if arr.size == 1 else default

