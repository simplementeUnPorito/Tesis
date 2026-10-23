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

## Validación en vivo (2026-10-23, capturas nuevas VIVO_VALIDACION, powerbank, sin lazo de masa)

Mismo código de la web (`noise_clean.js`) con `firmas.json` de GEO_I2C_A, cadena offset → I2C → SD → TX → beacon/RX:

| Captura | Ruido >150 Hz | Banda 10–50 Hz | Error sobre seno 20 Hz inyectado |
|---|---:|---:|---:|
| async_sd r1 | −20,9 % | ×1,0000 | 1,1 % (corrimiento de offset) |
| async_sd r2 | −21,2 % | ×1,0000 | 1,4 % |
| rt_sd r1 | −40,5 % | ×1,0006 | 1,1 % |
| rt_sd r2 | −40,1 % | ×1,0002 | 1,7 % |

Conclusión: las firmas generalizan a capturas nuevas y la limpieza saca el ruido digital de alta frecuencia sin tocar la banda útil. En batería ese ruido queda arriba de 150 Hz: el FIR de la web ya lo elimina de la banda útil.
