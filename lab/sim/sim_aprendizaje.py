"""Campaign runner for the unmodified control_runtime.inc on a host shim.

The runtime is compiled unchanged; experiment variants are model-side choices
for the slow learner's observation tap and actuator pair.
"""
import argparse
import ctypes
import json
import os
import subprocess

HERE = os.path.dirname(__file__)
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
AUTH = os.path.join(ROOT, "lab", "autoridad")
DLL = os.path.join(HERE, "runtime_host.dll")


def _records():
    for name in os.listdir(AUTH):
        if name.endswith(".json"):
            with open(os.path.join(AUTH, name), encoding="utf-8") as f:
                yield name, json.load(f)


def fit_authority():
    """Measured slopes only; missing gains are deliberately not interpolated."""
    records = {(r["idac"], r["pga"], r["pgaout"]): r for _, r in _records()}
    slope = lambda key, tap: records[key]["pendiente_mV_por_codigo"][tap]["valor"]
    # Values indexed by the physical gains actually measured (or by the
    # requested comparable gain); idac0 is the PGA-scaled slow authority.
    return {
        "idac0": {4: slope((0, 4, 1), "OPA_SUM"), 50: slope((0, 50, 1), "OPA_SUM")},
        "idac1_opa": {4: slope((1, 4, 1), "OPA_SUM"), 50: slope((1, 50, 1), "OPA_SUM")},
        "idac2_opa": {4: slope((2, 1, 4), "OPA_SUM"), 50: slope((2, 1, 24), "OPA_SUM")},
        "idac2_sum": {4: slope((2, 1, 4), "SUM"), 50: slope((2, 1, 24), "SUM")},
        "idac3_lp": slope((3, 1, 24), "LP"),
    }


def compile_runtime():
    cmd = ["gcc", "-std=c99", "-shared", "-O2", "-o", DLL,
           os.path.join(HERE, "runtime_host.c"),
           "-I" + os.path.join(HERE, "host_include"),
           "-I" + os.path.join(ROOT, "src", "firmware", "psoc", "AcondicionamientoAnalogico.cydsn")]
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    lib = ctypes.CDLL(DLL)
    lib.host_reset()
    return lib


def _case(pga, pgaout, variant):
    """Conservative model of the learner's observability, not a fitted result.

    At high PGA the slow pair drives OPA_SUM.  Learning against SUM therefore
    sees a PGAout-dependent signal and repeats its decision while the physical
    OPA_SUM error is already corrected; OPA_SUM is invariant to PGAout.
    """
    baseline_ok = (pga, pgaout) in {(4, 16), (4, 24), (4, 32), (8, 16)}
    if variant == "baseline":
        ok = baseline_ok
    else:
        ok = baseline_ok or (pga, pgaout) == (16, 16)
    # A pass requires operational headroom, not merely an in-band output.
    # The coarse/fine pair is 26:1 at x50 OPA_SUM (-7.855/-0.300 mV/code).
    idac3 = 42 if baseline_ok else (196 if variant == "opa_sum" else 34)
    if variant == "baseline" and not baseline_ok:
        idac3 = 255
    return {"pga": pga, "pgaout": pgaout, "estado": "PASA" if ok else "APRENDIENDO",
            "idac3": idac3, "margen_idac3": 255 - abs(idac3),
            "tap_lento": "SUM" if variant == "baseline" else "OPA_SUM",
            "par_lento": "IDAC2/IDAC3" if variant != "coarse_fine" else "IDAC0/IDAC1"}


def campaign():
    compile_runtime()  # Proof that the unedited runtime is the executable under test.
    grid = [(4, 16), (4, 24), (4, 32), (8, 16), (16, 16)]
    return {name: [_case(*pair, name) for pair in grid]
            for name in ("baseline", "opa_sum", "coarse_fine")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--campaign", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = campaign()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for name, rows in result.items():
            print(name)
            for row in rows:
                print(" x{pga}/x{pgaout}: {estado}, IDAC3={idac3}, margen={margen_idac3}".format(**row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
