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
