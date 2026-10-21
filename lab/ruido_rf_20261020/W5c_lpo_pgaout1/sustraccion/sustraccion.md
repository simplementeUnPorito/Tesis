# Sustraccion del brote RF

Ventana: -5 ms a +40 ms. RMS en uV sin media; potencia Welch (fs=2604 Hz, nperseg=2048) integrada entre 5 y 50 Hz en uV^2.
Capturas descartadas por riel: 0. Capturas sin marcas omitidas: 0.
Las capturas PING sin marcas se usan solo como referencia; a/b/c son identicos al original.

| condicion | n | RMS orig | RMS a global LOO | RMS b propia | RMS c ajustada | orig/ref | a/ref | b/ref | c/ref | PSD orig | PSD a | PSD b | PSD c |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| PING | 12 | 266.5 | 266.5 | 266.5 | 266.5 | 1.00 | 1.00 | 1.00 | 1.00 | 7627.9 | 7627.9 | 7627.9 | 7627.9 |
| RF10 | 6 | 8691.8 | 8185.0 | 8035.6 | 7788.5 | 32.61 | 30.71 | 30.15 | 29.22 | 26422049.9 | 18738429.3 | 17708679.5 | 14063455.7 |
| RF240 | 6 | 9930.9 | 9453.4 | 9127.9 | 8967.7 | 37.26 | 35.47 | 34.25 | 33.65 | 25797921.2 | 18302684.5 | 15185826.2 | 13835254.9 |
| RF240T29 | 6 | 10520.4 | 10545.7 | 10496.5 | 10274.1 | 39.47 | 39.57 | 39.38 | 38.55 | 32668241.4 | 32706717.8 | 32595683.3 | 30881806.9 |
| RF240T58 | 6 | 10191.9 | 9560.1 | 9430.4 | 9139.2 | 38.24 | 35.87 | 35.38 | 34.29 | 33466507.3 | 24645415.2 | 23427564.8 | 19468573.6 |

---
Generado por `lab/sustraer_brote_rf.py`.
