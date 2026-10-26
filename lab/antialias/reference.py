"""Reference designs and metrics for the PSoC MASW anti-alias study."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy import signal

FS = 2000.0
FACTORS = (2, 3, 4, 5, 6, 8, 10, 13, 16)
ATTEN_DB = 90.0
PASS_RATIO = 0.8
STOP_RATIO = 1.2
PSOC_FIR_TAPS = 127
PSOC_FIR_CUTOFF_HZ = 200.0
PSOC_FIR_ATTEN_DB = 60.0


def i0_series(x: float) -> float:
    term = 1.0
    total = 1.0
    y = x * x * 0.25
    k = 1
    while True:
        term *= y / (k * k)
        total += term
        k += 1
        if not (term > total * 1.0e-16 and k < 100):
            return total


def round_away(x: float) -> int:
    return math.floor(x + 0.5) if x >= 0.0 else math.ceil(x - 0.5)


def tap_count(factor: int, attenuation_db: float = ATTEN_DB) -> int:
    width = (STOP_RATIO - PASS_RATIO) / factor
    estimate = (attenuation_db - 8.0) / (2.285 * math.pi * width) + 1.0
    taps = math.ceil(estimate)
    return taps if taps & 1 else taps + 1


def kaiser_q23(factor: int) -> np.ndarray:
    taps = tap_count(factor)
    beta = 0.1102 * (ATTEN_DB - 8.7)
    denom = i0_series(beta)
    middle = (taps - 1) // 2
    cutoff = 1.0 / factor
    work: list[float] = []
    for i in range(taps):
        m = float(i - middle)
        ideal = cutoff if m == 0.0 else math.sin(math.pi * cutoff * m) / (math.pi * m)
        ratio = 2.0 * i / (taps - 1) - 1.0
        window = i0_series(beta * math.sqrt(max(0.0, 1.0 - ratio * ratio))) / denom
        work.append(ideal * window)
    norm = sum(work)
    q = np.array([round_away(value / norm * (1 << 23)) for value in work], dtype=np.int32)
    residual = (1 << 23) - int(np.sum(q, dtype=np.int64))
    q[middle] = np.int32(int(q[middle]) + residual)
    return q


def kaiser_float(factor: int) -> np.ndarray:
    return kaiser_q23(factor).astype(float) / float(1 << 23)


def acquisition_fir_q23(fs_hz: float) -> np.ndarray:
    """FIR de adquisición de 127 taps para el bloque Filter de 128 taps.

    El tap 128 se agrega como cero al serializar. Así el FIR útil conserva
    simetría impar y un retardo de grupo entero de 63 muestras.
    """
    beta = 0.1102 * (PSOC_FIR_ATTEN_DB - 8.7)
    coefficients = signal.firwin(
        PSOC_FIR_TAPS,
        PSOC_FIR_CUTOFF_HZ,
        window=("kaiser", beta),
        fs=float(fs_hz),
        scale=True,
    )
    q23 = np.rint(coefficients * (1 << 23)).astype(np.int64)
    q23[PSOC_FIR_TAPS // 2] += (1 << 23) - int(q23.sum())
    if np.any(q23 < -(1 << 23)) or np.any(q23 >= (1 << 23)):
        raise ValueError("los coeficientes no entran en Q1.23")
    return q23


def moving_average(factor: int) -> np.ndarray:
    return np.ones(factor) / factor


def cic(factor: int, order: int = 3) -> np.ndarray:
    h = np.ones(1)
    stage = np.ones(factor) / factor
    for _ in range(order):
        h = np.convolve(h, stage)
    return h


def cic_compensated(factor: int) -> np.ndarray:
    """Three-stage CIC plus a 31-tap pre-decimation droop compensator.

    This deliberately gives the compensator the best possible anti-alias
    placement; applying it after decimation cannot repair aliases.
    """
    base = cic(factor)
    grid = np.linspace(0.0, PASS_RATIO / factor, 64)
    _, response = signal.freqz(base, worN=grid * np.pi)
    gain = np.minimum(3.0, 1.0 / np.maximum(np.abs(response), 1.0e-4))
    freq = np.r_[grid, STOP_RATIO / factor, 1.0]
    desired = np.r_[gain, 0.0, 0.0]
    comp = signal.firwin2(31, freq, desired)
    comp /= np.sum(comp)
    return np.convolve(base, comp)


def iir_sos(kind: str, factor: int) -> np.ndarray:
    wp = PASS_RATIO / factor
    ws = STOP_RATIO / factor
    if kind == "butter":
        return signal.iirdesign(wp, ws, 0.10, 62.0, ftype="butter", output="sos")
    if kind == "ellip":
        return signal.iirdesign(wp, ws, 0.10, 62.0, ftype="ellip", output="sos")
    if kind == "bessel":
        # Give every order its best chance: choose Wn so loss at wp is 0.1 dB,
        # then test ws. Bessel's gentle transition generally needs many stages.
        from scipy.optimize import brentq
        last = None
        target = 10 ** (-0.10 / 20)
        for order in range(2, 31):
            def edge_error(wn: float) -> float:
                trial = signal.bessel(order, wn, btype="low", norm="mag", output="sos")
                return abs(signal.sosfreqz(trial, worN=np.array([wp * np.pi]))[1][0]) - target
            try:
                wn = brentq(edge_error, wp * 0.05, min(0.999, wp * 5.0))
            except ValueError:
                continue
            last = signal.bessel(order, wn, btype="low", norm="mag", output="sos")
            stop_gain = abs(signal.sosfreqz(last, worN=np.array([ws * np.pi]))[1][0])
            if stop_gain <= 10 ** (-60 / 20):
                return last
        assert last is not None
        return last
    raise ValueError(kind)


@dataclass
class Metrics:
    ripple_db: float
    ripple_1_100_db: float
    alias_rejection_db: float
    group_delay_span_ms: float
    step_overshoot_pct: float
    negative_impulse_pct: float


def metrics(system: np.ndarray, factor: int, sos: bool = False) -> Metrics:
    w = np.linspace(0.0, np.pi, 131073)
    if sos:
        _, h = signal.sosfreqz(system, worN=w)
    else:
        _, h = signal.freqz(system, worN=w)
        b, a = np.asarray(system), np.array([1.0])
    f = w * FS / (2 * np.pi)
    pass_hz = PASS_RATIO * FS / (2 * factor)
    stop_hz = STOP_RATIO * FS / (2 * factor)
    p = f <= pass_hz
    field = (f >= 1.0) & (f <= min(100.0, pass_hz))
    stop = f >= stop_hz
    mag_db = 20 * np.log10(np.maximum(np.abs(h), 1e-15))
    ripple = float(np.ptp(mag_db[p]))
    ripple_field = float(np.ptp(mag_db[field])) if np.count_nonzero(field) > 1 else float("nan")
    rejection = float(-np.max(mag_db[stop]))
    phase = np.unwrap(np.angle(h))
    gd = -np.gradient(phase, w) / FS * 1000.0
    gd_band = gd[field & (np.abs(h) > 1e-5)]
    gd_span = float(np.ptp(gd_band)) if gd_band.size else float("nan")
    excitation = np.r_[1.0, np.zeros(4095)]
    impulse = signal.sosfilt(system, excitation) if sos else signal.lfilter(b, a, excitation)
    step = np.cumsum(impulse)
    final = float(np.sum(impulse))
    overshoot = max(0.0, (float(np.max(step)) - final) / abs(final) * 100.0)
    negative = float(np.sum(np.abs(impulse[impulse < 0])) / np.sum(np.abs(impulse)) * 100.0)
    return Metrics(ripple, ripple_field, rejection, gd_span, overshoot, negative)


def designs(factor: int):
    linear = kaiser_float(factor)
    minimum = signal.minimum_phase(linear, method="homomorphic", half=False)
    return {
        "promedio": (moving_average(factor), False),
        "FIR Kaiser lineal/polifase": (linear, False),
        "CIC3": (cic(factor), False),
        "CIC3+comp31": (cic_compensated(factor), False),
        "Butterworth": (iir_sos("butter", factor), True),
        "Bessel": (iir_sos("bessel", factor), True),
        "eliptico": (iir_sos("ellip", factor), True),
        "FIR fase minima": (minimum, False),
    }


def print_summary() -> None:
    for factor in FACTORS:
        print(f"N={factor} fs_out={FS/factor:.3f} Hz taps={tap_count(factor)}")
        for name, (system, is_sos) in designs(factor).items():
            m = metrics(system, factor, is_sos)
            print(f"  {name:25s} ripple={m.ripple_db:7.3f} dB "
                  f"alias={m.alias_rejection_db:7.2f} dB "
                  f"gdspan={m.group_delay_span_ms:8.4f} ms "
                  f"over={m.step_overshoot_pct:6.2f}%")


if __name__ == "__main__":
    print_summary()
