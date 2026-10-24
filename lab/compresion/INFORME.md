# Compresión sin pérdida de lotes en tiempo real

**Objetivo:** mandar menos bytes por radio sin perder información. Cada lote se
codifica solo, para que uno perdido o retransmitido se decodifique sin los demás.

**Medido sobre 25 capturas reales** (26 640 lotes de 30 muestras, `estudio.py`):

| Esquema | Bytes/lote | Relación |
|---|---:|---:|
| Actual (`MsgData32`, 2 tramas de 15 × 10 B) | 334 | 1× |
| Solo los campos útiles (24 bits + marcas) | 123 | 2,7× |
| zlib nivel 9 (referencia, no apto para ESP32) | 66 | 5,1× |
| **Diferencia de 1.er orden + Rice con k por lote** (`geo_codec.h`) | **24,2** | **13,8×** |

Con golpes de martillo sintéticos (60 impulsos de 0,5 a 4 millones de cuentas,
decaimiento de 150 ms, sobre ruido real): media de 40,7 B y máximo de 97 B. Ese
máximo es el escape a crudo; el formato acota el largo a 152 B, así que siempre
entra en una sola trama ESP-NOW.

**Ida y vuelta exacta:** 0 lotes con diferencias en los 36 640 probados (reales y
martillo). El código probado es el mismo que corre en el firmware
(`codec_test.c` incluye `geo_codec.h` del esclavo).

**Por qué no hay pérdida de rigor:** los campos que se dejan de mandar no
aportan información.
- `raw_lo/raw_hi` son los 16 bits bajos del mismo valor.
- `alog*` siempre valen 0.
- `gain` es constante en la captura y ya viaja en el HELLO.
- El tiempo por lote no lo usa el maestro en tiempo real.

Se conservan el valor de 24 bits y las marcas de ruido de cada muestra.

**Formato:** ver la cabecera de `geo_codec.h`. Una trama `MsgDataZ`
(`0xBE`) por lote, con largo variable (8 + datos) y CRC. Se usa en tiempo real y
en la descarga rápida. El camino clásico lote por lote no cambia.

**Efecto esperado:** una trama de ~32 B por lote en lugar de dos de 167 B. Baja
el tiempo de aire, la marca de ruido de transmisión (TX) y las tramas a
retransmitir.

## Comparación ampliada (2026-10-24)

Se recorrieron los 26.640 lotes de `reales.bin` y los 10.000 de
`martillo.bin`. Los valores son bytes del códec por lote, sin la cabecera
exterior de 8 B. Todas las variantes hicieron ida y vuelta exacta en todos los
lotes (0 diferencias). En LPC se contaron los coeficientes Q12 de 16 bits.

| Esquema independiente | Reales media / P99 / máx. (B) | Martillo media / P99 / máx. (B) | Costo aproximado por lote |
|---|---:|---:|---|
| Actual: D1 + Rice, `k` exacto | **24,16 / 36 / 45** | 40,73 / 85 / 97 | 29 diferencias + 32×29 conteos Rice |
| FLAC fijo 0–3, mejor por lote | **24,16 / 36 / 45** | **31,91 / 65 / 80** | 4 predictores + 4×32 barridos; ~4–6 mil ops enteras |
| LPC Q12 1–4 | 26,16 / 38 / 47 | 31,49 / 56 / 82 | 4 ajustes LS, MAC y divisiones; el más caro |
| D1 + Rice, 2 particiones de 15 | 25,54 / 37 / 46 | 41,96 / 86 / 98 | 2×32 barridos Rice |
| D1 + Rice, `k` estimado | 24,22 / 36 / 45 | 40,79 / 85 / 97 | ~100 ops enteras |
| D1 + Elias-gamma | 24,71 / 37 / 46 | 52,65 / 105 / 113 | ~100 ops enteras |
| D1 + Exp-Golomb, parámetro óptimo | 25,26 / 37 / 46 | 42,13 / 89 / 102 | 16×29 conteos |

El `geo_codec.h` actual ya busca `k` de manera exhaustiva: no usa una
estimación. Reemplazarlo por el estimador ahorra CPU, pero cuesta 0,06 B/lote y
no mejora las colas. Las dos particiones tampoco amortizan su segundo `k` en
sólo 30 muestras. LPC ayuda en impactos, pero pierde 2 B/lote reales y suma los
bytes de coeficientes y bastante cómputo.

La selección FLAC eligió orden 1 en los 26.640 lotes reales. En martillo eligió
orden 1 en 5.427 lotes, orden 2 en 138 y orden 3 en 4.435. Por eso empata al
códec actual en reales y gana 8,83 B/lote (21,7 %) durante impactos.

### Superbatches (predictor continuo, menor granularidad)

| Lotes por trama | Reales media / P99 / máx. (B/lote) | Martillo media / P99 / máx. (B/lote) |
|---:|---:|---:|
| 2 | 21,65 / 31,00 / 36,50 | 28,81 / 63,00 / 74,50 |
| 3 | 20,81 / 29,33 / 33,00 | 27,87 / 62,67 / 71,00 |
| 4 | 20,39 / 28,50 / 31,75 | 27,44 / 63,00 / 69,50 |

Agrupar cuatro ahorra 3,77 B/lote reales frente al lote independiente, pero una
pérdida o retransmisión afecta 120 muestras y agrega 34,6 ms de latencia. No lo
recomiendo para el camino en tiempo real; sí puede servir para descarga masiva.

### Flags

| Codificación (payload solamente) | Reales media / P99 / máx. (B) | Martillo media / P99 / máx. (B) |
|---|---:|---:|
| 30 bytes crudos | 30,00 / 30 / 30 | 30,00 / 30 / 30 |
| 1 bit «todos cero», si no crudos | 26,42 / 30 / 30 | 22,76 / 30 / 30 |
| Actual: 1 bit «todos cero», si no RLE | **7,78 / 18 / 28** | **5,18 / 16 / 24** |
| RLE/crudo adaptativo | **7,78 / 18 / 28** | **5,18 / 16 / 24** |

El RLE actual nunca superó los 30 bytes en estos archivos; el modo crudo
adaptativo no cambia los resultados. Aunque los ceros dominan, hay flags no
cero en 23.462 lotes reales, así que un simple «todos cero» + crudo desperdicia
18,64 B/lote frente al RLE.

### Cabecera y recomendación

La cabecera exterior actual de 8 B puede desglosarse como tipo/marcador (1),
secuencia (4), nodo (1), largo (1) y CRC de aplicación (1). El control del códec
(1) y `k` (1; dos con particiones) están dentro del payload. Una cabecera mínima
razonable es tipo (1) + secuencia modular de 24 bits (3): envuelve cada 53,6 h a
87 lotes/s. El nodo puede inferirse de la MAC, el largo ya lo entrega ESP-NOW y
el CRC de aplicación puede omitirse si el FCS/autenticación del enlace cubre el
modelo de fallas. Si se necesita persistencia sin ese enlace, conviene conservar
el CRC. La longitud del payload queda implícita en el largo de trama.

**Recomendación:** pasar a FLAC fijo 0–3 por lote con `k` exacto. No reduce el
tráfico de ruido real medido, pero tampoco lo aumenta, conserva independencia y
reduce 21,7 % el payload de impactos. Con la misma cabecera exterior pasa de
48,73 a 39,91 B/lote en martillo (18,1 % menos bytes de trama): a 87 lotes/s
son 768 B/s menos y unos 6,14 ms/s menos de serialización a 1 Mbit/s, sin contar
el preámbulo fijo. En reales queda en 32,16 B/lote, sin cambio de airtime. La
propuesta `geo_codec2_propuesto.h` usa menos de 1 KiB de pila, no tiene tablas
grandes y compiló con GCC sin warnings; el test C dio 0 diferencias en ambos
archivos. Antes de llevarla al firmware mediría el tiempo en el ESP32-S3: si los
cuatro barridos exceden el presupuesto, mantendría D1 actual, que ya es óptimo
para las capturas reales.

Resultados completos y reproducibles: `comparar_algoritmos.py` y
`resultados_algoritmos.json`.

_Proveniencia: análisis y artefactos generados por Codex; verificación Python y C local._
