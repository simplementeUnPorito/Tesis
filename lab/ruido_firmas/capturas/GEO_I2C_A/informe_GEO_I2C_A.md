# Informe de firmas y limpieza — GEO_I2C_A

Deconvolución conjunta: 22.65 % de varianza HF explicada fuera de muestra.

| Fuente | EV drop-one | SNR bootstrap | Sig. | Recomendado | HF explicada | 1–100 después/antes | 10–50 después/antes | 10–50 después/base | Error señal |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| SD_IO | -0.021 % | 5.64 | sí | none | 0.00 % | 1.0000 | 1.0000 | 0.3673 | 0.0000 |
| SD_SYNC | -0.019 % | 5.72 | sí | none | 0.00 % | 1.0000 | 1.0000 | 0.3673 | 0.0000 |
| RADIO_TX | 9.971 % | 10.02 | sí | template | 16.54 % | 0.9954 | 1.0004 | 0.2225 | 0.0000 |
| I2C | 13.458 % | 104.07 | sí | template | 12.57 % | 0.9975 | 1.0000 | 0.4091 | 0.0000 |
| AP_BEACON | 0.010 % | 5.13 | sí | template | 0.11 % | 1.0000 | 1.0000 | 0.4091 | 0.0000 |
| MASTER_RX | 0.153 % | 9.05 | sí | template | -0.15 % | 1.0000 | 1.0000 | 0.2224 | 0.0000 |

Offsets: sin=20.18 %, todos=22.61 %, seleccionados=RADIO_TX.
Estimación: HP 150 Hz=22.65 %; sin HP=14.50 %.
PyWavelets/SWT: evaluado.
Cadena web: offset → notch de línea → I2C → SD → TX → beacon/RX → FIR LP 200 Hz (101 taps).

---
Proveniencia: Codex, ejecución directa sin delegados.
