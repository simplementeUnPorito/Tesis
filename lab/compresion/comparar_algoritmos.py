"""Comparacion reproducible de codecs lossless para lotes de geofono.

Los largos informados son los bytes producidos por el codec (incluyen control,
parametros, muestras de arranque y flags), pero no la cabecera exterior de la
trama ESP-NOW. Cada variante se decodifica y compara contra la entrada.
"""
from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
BATCH = 30
S24_MIN, S24_MAX = -(1 << 23), (1 << 23) - 1


class BitWriter:
    def __init__(self):
        self.data = bytearray()
        self.acc = 0
        self.used = 0

    def bit(self, value: int) -> None:
        self.acc = (self.acc << 1) | (value & 1)
        self.used += 1
        if self.used == 8:
            self.data.append(self.acc)
            self.acc = self.used = 0

    def bits(self, value: int, count: int) -> None:
        for shift in range(count - 1, -1, -1):
            self.bit(value >> shift)

    def unary0(self, quotient: int) -> None:
        for _ in range(quotient):
            self.bit(0)
        self.bit(1)

    def finish(self) -> bytes:
        if self.used:
            self.data.append(self.acc << (8 - self.used))
            self.acc = self.used = 0
        return bytes(self.data)


class BitReader:
    def __init__(self, data: bytes | memoryview):
        self.data = data
        self.pos = 0

    def bit(self) -> int:
        if self.pos >= len(self.data) * 8:
            raise ValueError("bitstream truncado")
        value = (self.data[self.pos >> 3] >> (7 - (self.pos & 7))) & 1
        self.pos += 1
        return value

    def bits(self, count: int) -> int:
        value = 0
        for _ in range(count):
            value = (value << 1) | self.bit()
        return value

    def unary0(self) -> int:
        value = 0
        while self.bit() == 0:
            value += 1
            if value > (1 << 27):
                raise ValueError("unario invalido")
        return value


def load_batches(path: Path) -> tuple[np.ndarray, np.ndarray]:
    raw = np.frombuffer(path.read_bytes(), dtype=np.uint8)
    if raw.size % 150:
        raise ValueError(f"{path}: largo no multiplo de 150")
    records = raw.reshape(-1, 150)
    samples = records[:, :120].copy().view("<i4").reshape(-1, BATCH)
    flags = records[:, 120:].copy()
    if np.any(samples < S24_MIN) or np.any(samples > S24_MAX):
        raise ValueError(f"{path}: muestra fuera de signed-24")
    return samples, flags


def pack_s24(values) -> bytes:
    out = bytearray()
    for item in values:
        value = int(item) & 0xFFFFFF
        out += bytes((value & 255, value >> 8 & 255, value >> 16 & 255))
    return bytes(out)


def unpack_s24(data: bytes | memoryview, count: int) -> np.ndarray:
    out = np.empty(count, dtype=np.int32)
    for i in range(count):
        value = int(data[3*i]) | int(data[3*i+1]) << 8 | int(data[3*i+2]) << 16
        out[i] = value - (1 << 24) if value & (1 << 23) else value
    return out


def zigzag(value: int) -> int:
    return 2 * value if value >= 0 else -2 * value - 1


def unzigzag(value: int) -> int:
    return value >> 1 if not value & 1 else -((value >> 1) + 1)


FIXED_COEFFICIENTS = ((), (1,), (2, -1), (3, -3, 1))


def fixed_residuals(samples: np.ndarray, order: int) -> list[int]:
    coefficients = FIXED_COEFFICIENTS[order]
    return [zigzag(int(samples[i]) - sum(c * int(samples[i-j-1])
                                         for j, c in enumerate(coefficients)))
            for i in range(order, len(samples))]


def rice_bits(values: list[int], k: int) -> int:
    return sum((value >> k) + 1 + k for value in values)


def exact_k(values: list[int], limit: int = 31) -> tuple[int, int]:
    candidates = [(rice_bits(values, k), k) for k in range(limit + 1)]
    return min(candidates)


def estimated_k(values: list[int]) -> int:
    # Estimador usual para Rice: floor(log2(media)); no garantiza el minimo.
    mean = sum(values) / len(values) if values else 0
    return min(31, max(0, int(math.floor(math.log2(mean))) if mean >= 1 else 0))


def rice_pack(values: list[int], k: int) -> bytes:
    writer = BitWriter()
    for value in values:
        writer.unary0(value >> k)
        writer.bits(value, k)
    return writer.finish()


def rice_unpack(data: bytes | memoryview, k: int, count: int) -> list[int]:
    reader = BitReader(data)
    return [(reader.unary0() << k) | reader.bits(k) for _ in range(count)]


def encode_flags_current(flags: np.ndarray) -> tuple[int, bytes]:
    if not np.any(flags):
        return 0, b""
    out = bytearray()
    start = 0
    for i in range(1, len(flags) + 1):
        if i == len(flags) or flags[i] != flags[start]:
            out += bytes((int(flags[start]), i - start))
            start = i
    return 1, bytes(out)


def decode_flags_current(mode: int, data: bytes | memoryview, count: int) -> np.ndarray:
    if not mode:
        if len(data):
            raise ValueError("flags sobrantes")
        return np.zeros(count, dtype=np.uint8)
    out = []
    if len(data) % 2:
        raise ValueError("RLE impar")
    for value, run in zip(data[::2], data[1::2]):
        out.extend([value] * run)
    if len(out) != count:
        raise ValueError("RLE incompleto")
    return np.asarray(out, dtype=np.uint8)


def fixed_encode(samples: np.ndarray, flags: np.ndarray, *, orders=range(4),
                 estimate=False) -> tuple[bytes, dict]:
    flag_mode, flag_data = encode_flags_current(flags)
    best = None
    for order in orders:
        residuals = fixed_residuals(samples, order)
        if estimate:
            k = estimated_k(residuals)
            bits = rice_bits(residuals, k)
        else:
            bits, k = exact_k(residuals)
        candidate = (order * 3 + (bits + 7) // 8, order, k, residuals)
        if best is None or candidate[:3] < best[:3]:
            best = candidate
    _, order, k, residuals = best
    compressed = bytes(((flag_mode << 3) | order, k)) + pack_s24(samples[:order]) + rice_pack(residuals, k)
    raw = bytes((0x80 | flag_mode << 3,)) + pack_s24(samples)
    body = compressed if len(compressed) < len(raw) else raw
    return body + flag_data, {"order": order if body is compressed else "raw", "k": k}


def fixed_decode(packet: bytes, count: int = BATCH) -> tuple[np.ndarray, np.ndarray]:
    control = packet[0]
    raw, flag_mode = bool(control & 0x80), (control >> 3) & 1
    if raw:
        samples = unpack_s24(packet[1:], count)
        used = 1 + 3 * count
    else:
        order, k = control & 3, packet[1]
        samples = np.empty(count, dtype=np.int32)
        samples[:order] = unpack_s24(packet[2:], order)
        reader = BitReader(memoryview(packet)[2 + 3*order:])
        coefficients = FIXED_COEFFICIENTS[order]
        for i in range(order, count):
            u = (reader.unary0() << k) | reader.bits(k)
            prediction = sum(c * int(samples[i-j-1]) for j, c in enumerate(coefficients))
            samples[i] = prediction + unzigzag(u)
        used = 2 + 3*order + (reader.pos + 7) // 8
    return samples, decode_flags_current(flag_mode, memoryview(packet)[used:], count)


def partition_encode(samples: np.ndarray, flags: np.ndarray) -> tuple[bytes, dict]:
    flag_mode, flag_data = encode_flags_current(flags)
    residuals = fixed_residuals(samples, 1)
    parts = (residuals[:14], residuals[14:])
    choices = [exact_k(part) for part in parts]
    body = bytearray(((flag_mode << 3) | 1, choices[0][1], choices[1][1]))
    body += pack_s24(samples[:1])
    body += rice_pack(parts[0], choices[0][1])
    body += rice_pack(parts[1], choices[1][1])
    raw = bytes((0x80 | flag_mode << 3,)) + pack_s24(samples)
    result = bytes(body) if len(body) < len(raw) else raw
    return result + flag_data, {"k": [item[1] for item in choices]}


def partition_decode(packet: bytes) -> tuple[np.ndarray, np.ndarray]:
    control = packet[0]
    flag_mode = (control >> 3) & 1
    if control & 0x80:
        samples = unpack_s24(packet[1:], BATCH)
        used = 91
    else:
        samples = np.empty(BATCH, dtype=np.int32)
        samples[0] = unpack_s24(packet[3:], 1)[0]
        pos = 6
        for first, n, k in ((1, 14, packet[1]), (15, 15, packet[2])):
            reader = BitReader(memoryview(packet)[pos:])
            for i in range(first, first + n):
                u = (reader.unary0() << k) | reader.bits(k)
                samples[i] = int(samples[i-1]) + unzigzag(u)
            pos += (reader.pos + 7) // 8
        used = pos
    return samples, decode_flags_current(flag_mode, memoryview(packet)[used:], BATCH)


def gamma_pack(values: list[int]) -> bytes:
    writer = BitWriter()
    for value in values:
        number = value + 1
        width = number.bit_length()
        writer.bits(0, width - 1)
        writer.bits(number, width)
    return writer.finish()


def gamma_read(reader: BitReader) -> int:
    zeros = 0
    while reader.bit() == 0:
        zeros += 1
    return ((1 << zeros) | reader.bits(zeros)) - 1


def gamma_encode(samples: np.ndarray, flags: np.ndarray) -> tuple[bytes, dict]:
    flag_mode, flag_data = encode_flags_current(flags)
    residuals = fixed_residuals(samples, 1)
    body = bytes(((flag_mode << 3) | 1,)) + pack_s24(samples[:1]) + gamma_pack(residuals)
    raw = bytes((0x80 | flag_mode << 3,)) + pack_s24(samples)
    result = body if len(body) < len(raw) else raw
    return result + flag_data, {}


def gamma_decode(packet: bytes) -> tuple[np.ndarray, np.ndarray]:
    control = packet[0]
    flag_mode = (control >> 3) & 1
    if control & 0x80:
        samples, used = unpack_s24(packet[1:], BATCH), 91
    else:
        samples = np.empty(BATCH, dtype=np.int32)
        samples[0] = unpack_s24(packet[1:], 1)[0]
        reader = BitReader(memoryview(packet)[4:])
        for i in range(1, BATCH):
            samples[i] = int(samples[i-1]) + unzigzag(gamma_read(reader))
        used = 4 + (reader.pos + 7) // 8
    return samples, decode_flags_current(flag_mode, memoryview(packet)[used:], BATCH)


def exp_bits(values: list[int], p: int) -> int:
    return sum(2 * ((value >> p) + 1).bit_length() - 1 + p for value in values)


def exp_pack(values: list[int], p: int) -> bytes:
    writer = BitWriter()
    for value in values:
        q, r = value >> p, value & ((1 << p) - 1)
        number = q + 1
        width = number.bit_length()
        writer.bits(0, width - 1)
        writer.bits(number, width)
        writer.bits(r, p)
    return writer.finish()


def exp_encode(samples: np.ndarray, flags: np.ndarray) -> tuple[bytes, dict]:
    flag_mode, flag_data = encode_flags_current(flags)
    residuals = fixed_residuals(samples, 1)
    bits, p = min((exp_bits(residuals, p), p) for p in range(16))
    body = bytes(((flag_mode << 3) | 1, p)) + pack_s24(samples[:1]) + exp_pack(residuals, p)
    raw = bytes((0x80 | flag_mode << 3,)) + pack_s24(samples)
    result = body if len(body) < len(raw) else raw
    return result + flag_data, {"p": p, "bits": bits}


def exp_decode(packet: bytes) -> tuple[np.ndarray, np.ndarray]:
    control = packet[0]
    flag_mode = (control >> 3) & 1
    if control & 0x80:
        samples, used = unpack_s24(packet[1:], BATCH), 91
    else:
        p = packet[1]
        samples = np.empty(BATCH, dtype=np.int32)
        samples[0] = unpack_s24(packet[2:], 1)[0]
        reader = BitReader(memoryview(packet)[5:])
        for i in range(1, BATCH):
            q = gamma_read(reader)
            u = (q << p) | reader.bits(p)
            samples[i] = int(samples[i-1]) + unzigzag(u)
        used = 5 + (reader.pos + 7) // 8
    return samples, decode_flags_current(flag_mode, memoryview(packet)[used:], BATCH)


def rounded_q12(total: int) -> int:
    return (total + 2048) // 4096 if total >= 0 else -((-total + 2048) // 4096)


def lpc_coefficients(samples: np.ndarray, order: int) -> np.ndarray:
    target = samples[order:].astype(np.float64)
    design = np.column_stack([samples[order-j-1:-j-1 if j >= 0 else None]
                              for j in range(order)])
    coefficients, *_ = np.linalg.lstsq(design, target, rcond=None)
    return np.clip(np.rint(coefficients * 4096), -32768, 32767).astype(np.int16)


def lpc_residuals(samples: np.ndarray, coefficients: np.ndarray) -> list[int]:
    order = len(coefficients)
    return [zigzag(int(samples[i]) - rounded_q12(sum(int(coefficients[j]) * int(samples[i-j-1])
                                                     for j in range(order))))
            for i in range(order, len(samples))]


def lpc_encode(samples: np.ndarray, flags: np.ndarray) -> tuple[bytes, dict]:
    flag_mode, flag_data = encode_flags_current(flags)
    best = None
    for order in range(1, 5):
        coefficients = lpc_coefficients(samples, order)
        residuals = lpc_residuals(samples, coefficients)
        bits, k = exact_k(residuals)
        size = 2 + 2*order + 3*order + (bits + 7)//8
        candidate = (size, order, k, coefficients, residuals)
        if best is None or candidate[:3] < best[:3]:
            best = candidate
    _, order, k, coefficients, residuals = best
    coeff_bytes = np.asarray(coefficients, dtype="<i2").tobytes()
    body = bytes(((flag_mode << 3) | (order - 1), k)) + coeff_bytes + pack_s24(samples[:order]) + rice_pack(residuals, k)
    raw = bytes((0x80 | flag_mode << 3,)) + pack_s24(samples)
    result = body if len(body) < len(raw) else raw
    return result + flag_data, {"order": order, "k": k}


def lpc_decode(packet: bytes) -> tuple[np.ndarray, np.ndarray]:
    control = packet[0]
    flag_mode = (control >> 3) & 1
    if control & 0x80:
        samples, used = unpack_s24(packet[1:], BATCH), 91
    else:
        order, k = (control & 3) + 1, packet[1]
        coefficients = np.frombuffer(packet, dtype="<i2", count=order, offset=2)
        start = 2 + 2*order
        samples = np.empty(BATCH, dtype=np.int32)
        samples[:order] = unpack_s24(packet[start:], order)
        reader = BitReader(memoryview(packet)[start + 3*order:])
        for i in range(order, BATCH):
            prediction = rounded_q12(sum(int(coefficients[j]) * int(samples[i-j-1])
                                         for j in range(order)))
            u = (reader.unary0() << k) | reader.bits(k)
            samples[i] = prediction + unzigzag(u)
        used = start + 3*order + (reader.pos + 7)//8
    return samples, decode_flags_current(flag_mode, memoryview(packet)[used:], BATCH)


SCHEMES = {
    "actual_d1_rice_k_exacto": (lambda x, f: fixed_encode(x, f, orders=(1,)), fixed_decode),
    "fixed_0_3_mejor_rice": (fixed_encode, fixed_decode),
    "lpc_q12_1_4_mejor_rice": (lpc_encode, lpc_decode),
    "d1_rice_2_particiones": (partition_encode, partition_decode),
    "d1_rice_k_estimado": (lambda x, f: fixed_encode(x, f, orders=(1,), estimate=True), fixed_decode),
    "d1_elias_gamma": (gamma_encode, gamma_decode),
    "d1_exp_golomb_p_optimo": (exp_encode, exp_decode),
}


def summary(values) -> dict:
    data = np.asarray(values, dtype=np.float64)
    return {"mean": round(float(data.mean()), 6),
            "p99": round(float(np.percentile(data, 99, method="linear")), 6),
            "max": round(float(data.max()), 6)}


def flag_sizes(flags: np.ndarray) -> dict[str, int]:
    zero = not np.any(flags)
    _, rle = encode_flags_current(flags)
    return {
        "crudos_siempre": len(flags),
        "bit_cero_sino_crudos": 0 if zero else len(flags),
        "actual_bit_cero_sino_rle": len(rle),
        "bit_cero_adaptativo_rle_crudo": 0 if zero else min(len(rle), len(flags)),
    }


def superbatch_encode(samples: np.ndarray, flags: np.ndarray) -> bytes:
    flat_samples = samples.reshape(-1)
    flat_flags = flags.reshape(-1)
    return fixed_encode(flat_samples, flat_flags)[0]


def validate_file(path: Path) -> dict:
    samples, flags = load_batches(path)
    sizes = defaultdict(list)
    metadata = defaultdict(Counter)
    mismatches = Counter()
    flag_results = defaultdict(list)
    for batch, batch_flags in zip(samples, flags):
        for name, (encoder, decoder) in SCHEMES.items():
            packet, meta = encoder(batch, batch_flags)
            decoded, decoded_flags = decoder(packet)
            if not np.array_equal(decoded, batch) or not np.array_equal(decoded_flags, batch_flags):
                mismatches[name] += 1
            sizes[name].append(len(packet))
            for key, value in meta.items():
                metadata[f"{name}.{key}"][str(value)] += 1
        for name, value in flag_sizes(batch_flags).items():
            flag_results[name].append(value)

    superbatches = {}
    for group in (2, 3, 4):
        normalized = []
        bad = 0
        for start in range(0, len(samples), group):
            batch_group = samples[start:start+group]
            flag_group = flags[start:start+group]
            packet = superbatch_encode(batch_group, flag_group)
            decoded, decoded_flags = fixed_decode(packet, batch_group.size)
            if not np.array_equal(decoded, batch_group.reshape(-1)) or not np.array_equal(decoded_flags, flag_group.reshape(-1)):
                bad += 1
            normalized.extend([len(packet) / len(batch_group)] * len(batch_group))
        superbatches[str(group)] = summary(normalized) | {"mismatches": bad}

    return {
        "batches": len(samples),
        "schemes": {name: summary(values) | {"mismatches": mismatches[name]}
                    for name, values in sizes.items()},
        "superbatch_fixed_0_3": superbatches,
        "flags_payload_only": {name: summary(values) for name, values in flag_results.items()},
        "metadata_histograms": {name: dict(counter) for name, counter in metadata.items()},
    }


def main() -> None:
    results = {
        "date": "2026-10-24",
        "units": "codec bytes per 30-sample batch; outer transport header excluded",
        "datasets": {},
        "operations_estimate": {
            "actual_d1_rice_k_exacto": "29 restas+zigzag; 32x29 shifts/acumulaciones para k; ~29 codigos Rice",
            "fixed_0_3_mejor_rice": "~116 predicciones (hasta 3 MAC) + 4x32 barridos Rice; ~4-6k ops enteras",
            "lpc_q12_1_4_mejor_rice": "4 ajustes least-squares + prediccion Q12 + 4x32 Rice; miles de MAC y divisiones; claramente el mas caro",
            "d1_rice_2_particiones": "29 restas+zigzag; 2x32 barridos de 14/15; ~1.9k shifts/sumas",
            "d1_rice_k_estimado": "29 restas+zigzag + suma/media/log2 + un solo conteo; ~100 ops enteras",
            "d1_elias_gamma": "29 restas+zigzag+bit_length; ~100 ops enteras",
            "d1_exp_golomb_p_optimo": "29 restas+zigzag + 16x29 conteos; ~600 ops enteras",
        },
        "header_analysis": {
            "current_outer_assumed_bytes": 8,
            "fields": [
                {"field": "tipo/marcador", "current_bytes": 1, "minimal_bytes": 1, "note": "necesario para despachar el mensaje"},
                {"field": "secuencia", "current_bytes": 4, "minimal_bytes": 3, "note": "24 bits envuelven cada 53.6 h a 87 lotes/s"},
                {"field": "nodo", "current_bytes": 1, "minimal_bytes": 0, "note": "se puede inferir de la MAC ESP-NOW"},
                {"field": "largo", "current_bytes": 1, "minimal_bytes": 0, "note": "ya viene dado por el largo de la trama recibida"},
                {"field": "CRC aplicacion", "current_bytes": 1, "minimal_bytes": 0, "note": "opcional si alcanza el FCS y la autenticacion de ESP-NOW"},
                {"field": "control codec", "current_bytes": 1, "minimal_bytes": 1, "note": "escape, predictor y modo de flags"},
                {"field": "k Rice", "current_bytes": 1, "minimal_bytes": 1, "note": "sólo en modo comprimido; dos bytes con particiones"},
            ],
            "minimal_outer_bytes": 4,
        },
    }
    for filename in ("reales.bin", "martillo.bin"):
        print(f"Procesando {filename}...", flush=True)
        results["datasets"][filename] = validate_file(HERE / filename)

    real_schemes = results["datasets"]["reales.bin"]["schemes"]
    hammer_schemes = results["datasets"]["martillo.bin"]["schemes"]
    base_name = "actual_d1_rice_k_exacto"
    # Desempatar por martillo: no se acepta regresion en reales.
    best_name = min(real_schemes,
                    key=lambda name: (real_schemes[name]["mean"],
                                      hammer_schemes[name]["mean"]))
    gains = {}
    for dataset in results["datasets"]:
        schemes = results["datasets"][dataset]["schemes"]
        gains[dataset] = round(100 * (schemes[base_name]["mean"] - schemes[best_name]["mean"])
                               / schemes[base_name]["mean"], 6)
    results["decision"] = {
        "baseline": base_name,
        "best_independent": best_name,
        "gain_pct": gains,
        "threshold_pct_for_c_proposal": 10.0,
        "implement_c": bool(max(gains.values()) > 10.0),
        "c_proposal": "geo_codec2_propuesto.h",
    }
    output = HERE / "resultados_algoritmos.json"
    output.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results["decision"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
