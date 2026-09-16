# Runbook histórico no ejecutado: propuesta IDAC2 a 5,1 kOhm

> **NO USAR COMO ESTADO ACTUAL.** El 2026-09-10 Elías confirmó que IDAC2 e
> IDAC3 permanecen físicamente en 10 kOhm. La cabecera anterior del handoff que
> daba por instalado 5,1 kOhm era incorrecta. Este archivo se conserva sólo
> como registro de la prueba que se había propuesto.

No ejecutar hasta que Elías confirme físicamente que **sólo** la resistencia
de IDAC2→Vref de OPAsum fue cambiada de 10 kOhm a 5,1 kOhm. Al corte del
2026-09-09 10:50 la placa quedó apagada, con la resistencia de 10 kOhm todavía
instalada; el último estado comandado antes de apagar fue PGAout x1 y los cuatro
IDAC en cero.

## Antes de energizar

1. Confirmar designador y medir la resistencia sin alimentación.
2. Inspeccionar puentes/soldadura y continuidad hacia Vref de OPAsum.
3. No modificar IDAC3 (10 kOhm) ni TopDesign.
4. Cambiar en código los metadatos de IDAC2 de 10.000 a 5.100 Ohm tanto en
   `testbench/core/checklist.py` como en `psoc_hw.h`; renombrar comentarios que
   todavía dicen PGAout, sin cambiar la asignación física.
5. Mantener los cuatro IDAC en 31,875 uA (0,125 uA/bit).

## Primera prueba: actuador aislado, PGAout x1

1. Fijar ADC ±2,5 V, PGA x50, PGAout x1 y los cuatro IDAC en cero.
2. Observar sin tocar durante al menos 2 minutos y registrar ch0..ch4 sin
   conectar AMuxCapacitor.
3. Si ch2 está en un riel, mover IDAC2 de a un código hacia la ventana. Medir
   ch2, ch3 y ch4 después de cada paso. Limitar la primera exploración a ±32.
4. Cuando ch2 sea válido, medir un patrón reversible ABBA alrededor del punto:
   `c, c+1, c, c-1, c`, con dwell suficiente y registro temporal.
5. Estimar pendiente local, histéresis y tiempo de asentamiento. No usar puntos
   saturados para una recta.
6. Restaurar cero si se cruza una guarda o falta comunicación reiteradamente.

Predicción teórica con R=5,1 kOhm y 0,125 uA/bit:

- referencia: 0,6375 mV/código;
- si la ganancia desde referencia a OPA_SUMo es ≈3: 1,91 mV/código en ch2;
- después de PGAout x24: ≈45,9 mV/código en SUMo;
- después de PGAout x50: ≈95,6 mV/código en SUMo.

Estas cifras son hipótesis de diseño; reemplazarlas por pendientes medidas sin
carga. IDAC3 seguirá resolviendo el residual de LPo.

## Cambio directo de ganancia

Sólo después de centrar ch2 en x1:

1. conservar IDAC0 e IDAC1;
2. verificar que el residual de ch2 es seguro al multiplicarlo por la ganancia;
3. conmutar directamente a la ganancia solicitada;
4. cerrar IDAC2 sobre ch2/ch3 y luego IDAC3 sobre ch4;
5. guardar un par IDAC2/IDAC3 distinto para cada ganancia sólo tras PASS;
6. si falla, restaurar el último par seguro e informar; la alternativa es
   ejecutar la calibración completa de arranque;
7. ensayar primero x24; sólo después de repetirlo probar x32/x48/x50.

## Criterio mínimo para declarar x24

- ninguna lectura usada por el controlador fuera de 880,4..1122,7 mV banco;
- PGAgain y BPo dentro de ±500 mV físicos de Vref;
- OPA_SUMo dentro de ±1 V, preferentemente mucho más cerca de cero;
- SUMo y LPo sin saturación durante toda la corrida;
- LPo final dentro de ±20 mV físicos durante una ventana ≥2*tau;
- convergencia desde cero, sin semillas; EEPROM sólo escrita después del PASS;
- al menos cinco reinicios independientes PASS y una prueba posterior a
  power-cycle;
- CSV/JSON con códigos, ganancias, tiempos, medias, pico-pico, tau estimada,
  Jacobiano/pendientes usados, guardas y causa explícita de cualquier aborto.

## Orden de implementación

1. Corregir simulador/unidades y hacer que un self-test fallido devuelva código
   de salida distinto de cero.
2. Añadir reintentos de lectura al diagnóstico de IDAC2.
3. Implementar rescate/bracket sin exigir que ch2 ya sea válido al arrancar.
4. Estimar tau sólo desde ch1 y usar una única ventana total de 2*tau para el
   tramo lento.
5. Newton local acotado + PI pequeño + verificación estacionaria.
6. Validar en Python/hardware.
7. Portar el método ganador a C autónomo y repetir la validación sin PC.
8. Recién entonces guardar EEPROM y declarar el objetivo cumplido.

## Ensayo opcional del capacitor auxiliar en plantas rápidas

Después de caracterizar sin carga, repetir los puntos locales de IDAC2/IDAC3
conectando `AMuxCapacitor` sólo en ch2/ch3/ch4. Aceptarlo únicamente si la media
no cambia dentro de la tolerancia, la pendiente coincide y no aparece memoria o
histéresis adicional. No usarlo en ch1 ni al estimar tau. Si baja pico-pico pero
desplaza la media, se descarta.
