# Informe de firmas y limpieza — SIM_S3_q

Deconvolución conjunta: 95.76 % de varianza HF explicada fuera de muestra.

| Fuente | EV drop-one | SNR bootstrap | Sig. | Recomendado | HF explicada | 1–100 después/antes | 10–50 después/antes | 10–50 después/base | Error señal |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| SD_IO | 4.131 % | 245.54 | sí | interp | 36.42 % | 0.5547 | 0.6354 | nan | 0.1402 |
| SD_SYNC | 0.002 % | 12.24 | sí | interp | 1.47 % | 1.0012 | 1.0004 | nan | 0.0454 |
| RADIO_TX | 66.109 % | 674.31 | sí | interp | 73.21 % | 1.0099 | 0.9955 | nan | 0.0366 |
| I2C | 20.809 % | 438.81 | sí | interp | 27.58 % | 0.9986 | 0.9881 | nan | 0.0614 |
| AP_BEACON | 1.785 % | 102.41 | sí | interp | 4.39 % | 0.9982 | 0.9990 | nan | 0.0137 |
| MASTER_RX | -0.001 % | 3.52 | sí | none | 0.00 % | 1.0000 | 1.0000 | nan | 0.0000 |

Offsets: sin=92.32 %, todos=95.76 %, seleccionados=SD_IO.
Estimación: HP 150 Hz=95.76 %; sin HP=41.13 %.
PyWavelets/SWT: evaluado.
Cadena web: offset → notch de línea → I2C → SD → TX → beacon/RX → FIR LP 200 Hz (101 taps).

---
Proveniencia: Codex, ejecución directa sin delegados.
