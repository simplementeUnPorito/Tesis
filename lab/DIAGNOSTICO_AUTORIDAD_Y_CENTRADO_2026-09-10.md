# Diagnóstico de autoridad y centrado — 2026-09-10

## Conclusión ejecutiva

El problema actual no es un único LSB mal elegido:

1. **IDAC2 e IDAC3 están físicamente en 10 kΩ.** La premisa inicial de que
   IDAC2 había sido cambiado a 5,1 kΩ era incorrecta y queda anulada.
2. **IDAC2 está sin margen por desplazamiento del punto de operación.** En el
   ABBA estacionario de 30 s, aun en código 254, `OPA_SUMo` queda en mediana
   943,05 mV de banco: −1,164 V respecto de Vref. La pendiente medida es
   9,56 mV físicos/código de mediana, con DE 1,97 mV/código. Harían falta unos
   122 códigos adicionales si todo lo demás permaneciera fijo.
3. **IDAC3 no está desconectado ni simplemente tiene un paso grande.** Con la
   entrada actual de la etapa LP, la salida no presenta una región lineal útil:
   permanece cerca de 4,49 V o cae fuera del rango del ADC por abajo. Al subir
   desde el riel bajo conmuta entre códigos +16 y +24; al bajar desde el riel
   alto empieza a caer entre −32 y −40. La histéresis observada es de unos
   48–64 códigos y a −40 la conmutación tarda aproximadamente 6 s.
4. **El software oculta el fallo.** El camino histórico declara PASS cuando
   PGAgain, BPo y LPo son físicamente legibles; no minimiza el error de LPo y no
   exige que OPA_SUMo/SUMo sean válidos. Por eso reutiliza `[19,140,254,83]` en
   todas las ganancias aunque LPo quede +2,08 V respecto de Vref y ch2/ch3 se
   saturen desde x4.
5. **Centrar correctamente BPo agrava la falta de margen de OPAsum.** Un ABBA
   de 45 s midió IDAC1→BPo = +2,188 mV/código e IDAC1→OPA_SUMo =
   −17,05 mV/código. Cambiar IDAC1 de 140 a 188 centra BPo, pero lleva OPA_SUMo
   de aproximadamente −1,1 V a aproximadamente −1,9 V, aun con IDAC2=254.

## Ensayo local repetido

Configuración: PGA x50, PGAout x1, punto `[19,140,254,83]`, sin escritura de
EEPROM. Se descargó previamente la fase 2 y se ejecutaron tres ciclos ABBA por
actuador. Al finalizar se restauró x1 y el punto operativo.

| actuador | intervalo | tap | pendiente física mediana | DE |
|---|---:|---|---:|---:|
| IDAC2, ABBA 5 s | 238→254 | OPA_SUMo | +10,54 mV/código | 0,78 mV/código |
| IDAC2, ABBA 30 s | 238→254 | OPA_SUMo | +9,56 mV/código | 1,97 mV/código |
| IDAC2, ABBA 30 s | 238→254 | SUMo | +9,39 mV/código | 1,84 mV/código |
| IDAC3 | 67→99 | LPo | 0,00 mV/código | 0,011 mV/código |

El cero local de IDAC3 no significa que el actuador no funcione: ambos códigos
67 y 99 están en la meseta alta de LPo. El barrido amplio posterior confirmó
que los códigos negativos llevan la salida a la meseta baja.

En el ABBA largo, los 18 puntos de IDAC2=254 dejaron OPA_SUMo entre 942,17 y
944,46 mV de banco, con mediana 943,05 mV. Eso equivale a −1,164 V respecto de
Vref. En IDAC2=238 la mediana fue 935,37 mV (−1,317 V). La diferencia local es
9,56 mV/código, pero el primer tramo dio sólo 4,96 mV/código: la memoria sigue
siendo material incluso con mesetas de 30 s.

## Barridos de IDAC3

- Dos recorridos amplios confirmaron la misma polaridad y los dos estados:
  código 0 puede conservar el estado previo; −128/−255 llevan LPo abajo y
  +83/+128/+255 lo llevan arriba.
- En el recorrido dirigido −128→+96→−128, la transición ascendente ocurrió
  entre +16 y +32; una repetición desde abajo mostró que +24 ya conmuta arriba.
- En el recorrido descendente, −32 dejó una lectura transitoria alta
  (1087,95 mV de banco) y −48 ya estaba fuera de rango por abajo. Mantener −40
  produjo una lectura alta inicial y la conmutación al riel bajo unos 6 s más
  tarde; permaneció abajo durante el resto de la ventana.
- Por tanto, reducir el tamaño de paso de IDAC3 no corrige por sí solo el
  comportamiento rail-to-rail: primero hay que llevar SUM/entrada LP a una
  región donde el lazo LP tenga solución lineal.

## Decisión de hardware

**No existe un único valor de resistencia de IDAC2 que resuelva bien todas las
ganancias con el cero actual.** La prueba de Fase 1 confirmó que centrar BPo no
libera IDAC2: aumenta el déficit de OPAsum hasta aproximadamente 1,9 V. Con la
pendiente local actual, el código equivalente necesario sería ~454. Una
solución exclusivamente resistiva requeriría del orden de **18 kΩ** en IDAC2.

Eso daría alcance en x1, pero empeoraría la resolución aguas abajo: el paso
medido actual de 9,56 mV/código antes de PGAout se vuelve aproximadamente
478 mV/código en x50; escalado a 18 kΩ sería aproximadamente **0,86 V/código**.
Por tanto, aumentar R arreglaría alcance a baja ganancia a costa de una malla
muy gruesa a alta ganancia.

La solución preferida es **corregir el cero DC de OPAsum** para que IDAC2 use
una pequeña fracción de ±255 después de centrar BPo. Alternativas estructurales
son volver a inyectar la corrección después de PGAout o disponer de autoridad
conmutable según la ganancia. Cambiar 10 kΩ por otro valor fijo sin corregir el
cero sólo mueve el compromiso alcance/resolución.

**No cambiar IDAC3 todavía.** Primero hay que sacar SUM/entrada LP de la zona
saturada; recién allí se puede medir su paso lineal y decidir si 10 kΩ ofrece la
resolución final adecuada.

Después de resolver IDAC2, IDAC3 debe volver a caracterizarse en una región no
saturada. El antecedente con R14=3,9 kΩ midió 2,692 mV/código y buena cobertura,
pero pertenecía a otra distribución de autoridad; no justifica cambiarlo ahora
sin ese ensayo posterior.

## Cambio mínimo de software necesario

- Fase 1: minimizar solamente PGAgain/BPo y terminar rápido.
- Fase 2: no aceptar el historial sólo porque LPo esté dentro de los rieles.
  Debe minimizar `abs(LPo−Vref)` y exigir margen antirriel.
- Antes de actuar con IDAC3, exigir que OPA_SUMo/SUMo sean válidos y que IDAC2
  no esté limitado en ±255. Si IDAC2 está limitado, informar `sin autoridad` en
  vez de declarar PASS.
- Estimar pendientes con ABBA y ventanas repetidas; no con barridos monotónicos
  cortos que mezclan respuesta con deriva.

## Evidencia primaria

- `calibracion_nueva/autoridad_local_actual_20260910_082627.csv`
- `calibracion_nueva/autoridad_local_actual_20260910_082627.csv.json`
- `calibracion_nueva/autoridad_local_actual_20260910_085138.csv`
- `calibracion_nueva/autoridad_local_actual_20260910_085138.csv.json`
- `calibracion_nueva/autoridad_local_actual_20260910_090727.csv`
- `calibracion_nueva/autoridad_local_actual_20260910_090727.csv.json`
- `calibracion_nueva/idac3_rango_actual_20260910_083620.csv`
- `calibracion_nueva/idac3_rango_actual_20260910_084048.csv`
- `calibracion_nueva/idac3_rango_actual_20260910_084332.csv`

Los runners usados quedan en:

- `src/interfaces/python/diagnosticar_autoridad_actual.py`
- `src/interfaces/python/diagnosticar_idac3_rango_actual.py`
