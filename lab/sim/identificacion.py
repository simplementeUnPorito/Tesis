"""Offline, reproducible identification of the frozen-loop A-B-A-B-A traces.

This intentionally has no serial, firmware-programming, or COM-port code.
The three named files are held out before every fit.
"""
import json
import math
import os
import statistics

HERE = os.path.dirname(__file__)
AUTH = os.path.normpath(os.path.join(HERE, "..", "autoridad"))
CAMPAIGN = os.path.normpath(os.path.join(HERE, "..", "campana_techo", "resultados.jsonl"))
TAPS = ("SEo", "BPo", "OPA_SUM", "SUM", "LP")
HOLDOUT = ("idac0_pgax16.json", "paso4_idac1.json", "paso6_idac2.json")


def _load(name):
    with open(os.path.join(AUTH, name), encoding="utf-8") as source:
        return json.load(source)


def _tail(segment, tap):
    values = [sample["taps"][tap] / 1000.0 for sample in segment["serie"][-12:]
              if sample["taps"][tap] is not None]
    return statistics.median(values)


def _centres(record):
    parts = {part["nombre"]: part for part in record["tramos"]}
    return {tap: {
        "a": (_tail(parts["A1"], tap) + _tail(parts["A2"], tap)) / 2.0,
        "b": (_tail(parts["B1"], tap) + _tail(parts["B2"], tap)) / 2.0,
        "dc": parts["B1"]["codigo"] - parts["A1"]["codigo"],
    } for tap in range(5)}


def _slope(record, tap):
    point = record["pendiente_mV_por_codigo"][TAPS[tap]]
    return None if point["saturado"] else point["valor"]


def _power_gain(points, gain):
    """Fit |k|=a*gain**b in log space; sign is fixed by the measurements."""
    xs = [math.log(p[0]) for p in points]
    ys = [math.log(abs(p[1])) for p in points]
    xbar, ybar = statistics.mean(xs), statistics.mean(ys)
    den = sum((x - xbar) ** 2 for x in xs)
    b = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / den
    a = math.exp(ybar - b * xbar)
    return math.copysign(a * gain ** b, points[0][1])


def _limits(records):
    # Physical clipping bounds are read from the independent closed-loop
    # campaign, never tuned to a held-out open-loop error.  Its field names
    # differ only for the two historical aliases below.
    aliases = ("SEo", "BP", "OPAs", "SUM", "LP")
    values = [[] for _ in TAPS]
    with open(CAMPAIGN, encoding="utf-8") as source:
        for line in source:
            row = json.loads(line)
            for tap, alias in enumerate(aliases):
                values[tap].extend((row["taps"][alias]["min_mV"],
                                    row["taps"][alias]["max_mV"]))
    return [(min(series), max(series)) for series in values]


def _clip(value, limits):
    return max(limits[0], min(limits[1], value))


def identify():
    names = sorted(name for name in os.listdir(AUTH) if name.endswith(".json"))
    records = {name: _load(name) for name in names}
    train = {name: record for name, record in records.items() if name not in HOLDOUT}
    limits = _limits(list(records.values()))

    # Identified only from non-saturated slopes.  IDAC0's SEo/BPo paths are
    # fitted versus PGA; the downstream IDAC0 paths are deliberately absent:
    # all usable new high-PGA steps hit their rails, so a gain is not observed.
    idac0 = [record for record in train.values() if record["idac"] == 0]
    k0 = {}
    for tap in (0, 1):
        points = [(record["pga"], _slope(record, tap)) for record in idac0
                  if _slope(record, tap) is not None]
        k0[tap] = _power_gain(points, 16) if len(points) >= 2 else None

    r1 = train["paso3_idac1.json"]
    r2 = train["paso5_idac2.json"]
    out = {}
    for name in HOLDOUT:
        record, centres = records[name], _centres(records[name])
        row = {"idac": record["idac"], "pga": record["pga"],
               "pgaout": record["pgaout"], "taps": []}
        for tap in range(5):
            base, actual, dc = centres[tap]["a"], centres[tap]["b"], centres[tap]["dc"]
            predicted = None
            if record["idac"] == 0:
                gain = k0.get(tap)
                if gain is not None:
                    predicted = _clip(base + gain * dc, limits[tap])
            elif record["idac"] == 1:
                gain = _slope(r1, tap)
                if gain is not None:
                    predicted = _clip(base + gain * dc, limits[tap])
            elif record["idac"] == 2:
                gain = _slope(r2, tap)
                if gain is not None:
                    # IDAC2 is upstream of PGAout for SUM/LP, but not OPA_SUM.
                    scale = record["pgaout"] / r2["pgaout"] if tap in (3, 4) else 1.0
                    predicted = _clip(base + gain * scale * dc, limits[tap])
            row["taps"].append({"tap": TAPS[tap], "actual_mV": actual,
                                "predicted_mV": predicted,
                                "error_mV": None if predicted is None else predicted - actual})
        out[name] = row
    return {"holdout": out, "limits_mV": dict(zip(TAPS, limits)),
            "idac0_predicted_slope_mV_code": {TAPS[t]: k for t, k in k0.items()}}


if __name__ == "__main__":
    print(json.dumps(identify(), indent=2, ensure_ascii=False))
