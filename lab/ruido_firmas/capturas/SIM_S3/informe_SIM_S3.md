# Informe de firmas y limpieza — SIM_S3

Deconvolución conjunta: 95.41 % de varianza HF explicada fuera de muestra.

| Fuente | EV drop-one | SNR bootstrap | Sig. | Recomendado | HF explicada | 1–100 después/antes | 10–50 después/antes | 10–50 después/base | Error señal |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| SD_IO | 4.038 % | 113.44 | sí | interp | -154.18 % | 0.9629 | 0.9526 | nan | 0.1523 |
| SD_SYNC | -0.000 % | 6.79 | sí | none | 0.00 % | 1.0000 | 1.0000 | nan | 0.0000 |
| RADIO_TX | 66.673 % | 732.02 | sí | interp | -269.93 % | 0.9787 | 0.9782 | nan | 0.0345 |
| I2C | 20.739 % | 325.44 | sí | interp | -470.23 % | 0.9609 | 0.9605 | nan | 0.0614 |
| AP_BEACON | 1.800 % | 86.75 | sí | interp | -41.61 % | 0.9974 | 0.9974 | nan | 0.0133 |
| MASTER_RX | -0.001 % | 4.83 | sí | none | 0.00 % | 1.0000 | 1.0000 | nan | 0.0000 |

Offsets: sin=91.99 %, todos=95.40 %, seleccionados=SD_IO.
Estimación: HP 150 Hz=95.41 %; sin HP=-0.04 %.
PyWavelets/SWT: evaluado.
Cadena web: offset → notch de línea → I2C → SD → TX → beacon/RX → FIR LP 200 Hz (101 taps).

---
Proveniencia: Codex, ejecución directa sin delegados.
