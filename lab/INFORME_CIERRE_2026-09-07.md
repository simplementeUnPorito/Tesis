# Cierre de EXP4c/EXP4d — 7 de septiembre de 2026

## Estado entregado

La adquisición iniciada el 6 de septiembre se detuvo a pedido de Elías el 7 de
septiembre a las 08:01. Quedó cerrada en 22,055 h, sin procesos de adquisición
ni vigilantes en segundo plano. El informe PDF y todas sus cifras se regeneran
desde los JSON guardados.

## Resultado medido

- Configuración: PGA ×50, PGAout ×1, calibración hecha por el firmware una sola
  vez; no hubo recalibración durante la corrida.
- Archivo: `lab/planta/deriva_20260906_0954.json`.
- Ventana: 2026-09-06 09:57:49 a 2026-09-07 08:01:07.
- 1.257 instantes; 1.245 lecturas válidas del tap LP.
- LP: inició a −14 mV de Vref, terminó a +75 mV y recorrió una banda total de
  245 mV (−144 a +101 mV).
- Resumen lineal de esta ventana: +7,7 mV/h, 171 mV acumulados, con 24 mV RMS de
  vagabundeo alrededor de la recta. No se extrapola este ajuste hasta el riel.
- La banda equivale a 7,2 veces los 34 mV que consigue la calibración. Un trim
  fijo no sostiene el punto durante un turno; la recalibración automática queda
  justificada por medición.
- EXP4d: 250 bloques válidos de ruido; mediana RMS 381 µV de banco y mediana de
  50 Hz igual a 0 µV. La mediana no crece entre mitades. Hubo seis excitaciones
  por encima del doble de la mediana, hasta 8.010 µV; se conservan en los datos
  y se tratan como eventos ambientales, no como piso de la cadena.

## Calidad y límites

- Hay 58 taps nulos entre 5.028 lecturas (1,15 %): ch0=13, ch1=20, ch2=13,
  ch3=12. También faltan 2 de 252 bloques de ruido previstos. Los nulos se
  excluyen y no se interpolan.
- El campo histórico `lecturas_fallidas=0` era incompleto: no contaba respuestas
  vacías. `exp_deriva.py` quedó corregido para contarlas en corridas futuras.
- La temperatura exterior modelada por Open-Meteo varió entre 8,1 y 17,7 °C y
  tiene correlación contemporánea `r=-0,86` con el LP. Es sólo un proxy
  meteorológico: no reemplaza un sensor en el banco ni prueba causalidad térmica.

## Reproducibilidad

- SHA-256 de `deriva_20260906_0954.json`:
  `25645512F544517C3BE84045D2F87C4110ED2C6D17186DB24F6D0B0CF062486D`.
- SHA-256 de `temperatura_exterior_20260906_20260907.json`:
  `59E0F9C61AB29638F6ABFC442D15D8721D08D00582917ED9287B9238140CF75C`.
- Análisis: `cd src/interfaces/python; python analizar_deriva.py`.
- Regeneración: `python descargar_temperatura_deriva.py`, luego
  `python figuras_semana.py`.
- PDF: `cd docs/informe_semana_2026-09-06; ./compilar.ps1` o dos ejecuciones de
  `lualatex -interaction=nonstopmode -halt-on-error informe.tex`.

## Pendiente físico

Para separar deriva térmica de otros mecanismos hace falta repetir la prueba
con un sensor de temperatura junto a la placa. El resto de los pendientes de
hardware continúa en `lab/PLAN_RESISTENCIAS_LUNES.md`.
