# Investigación de la cadena analógica - 2026-09-26

## Método y alcance

No se abrió COM8, no se ejecutó software de puerto serie ni se grabó firmware.
**MEDIDO** designa resultados de placa; **SIMULADO**, el host `lab/sim`; y
**DEDUCIDO**, una consecuencia de topología/valores. Las visitas `FALLA` y
`APRENDIENDO` sirven para localizar taps fuera de rango, no para ajustar
pendientes.

## P1. Referencia de PGAgain

**DEDUCIDO - evidencia decisiva.** El datasheet local instalado de PSoC
Creator 4.4, `PGA_v2_0/PGA_v2_0.pdf`, indica: `Vout = Vref + (Vin - Vref) ×
Gain`. La [hoja pública de Infineon](https://www.infineon.com/assets/row/public/documents/cross-divisions/396/infineon-component-programmable-gain-amplifier-pga-v2.0-software-module-datasheets-en.pdf)
confirma esa ecuación y Vref externo. Es (a), no (b): con Vin fijo,
`dVout/dVref = 1-G`.

**DEDUCIDO - build/TopDesign.** `Generated_Source/PSoC5/PGAgain.h` define
`PGAgain_VREF_MODE=0`, es decir `GNDVREF_DI` (VSS interno deshabilitado), y
`PGAgain.c` lo carga en CR2 como PGA no inversor. Es fuerte evidencia de Vref
externo en la instancia, no de que el nodo físico que mueve IDAC0 llegue sin
otra transformación a ese Vref.

Con R0=15 k, un código da 1.875 mV. R6=6.8 k y R8=27 k dan
`A_SE=-27/6.8=-3.9706`; luego, si IDAC0 llega a Vref de PGAgain,
`dOPA_SUM/dcode0=-3.9706(1-G)1.875 mV`. Vale cero a x1 y +364.9 mV/código a
x50. El PGA también limita Vin-Vref a VDDA/G, de modo que no hay margen para
presumir linealidad a ganancia alta.

**MEDIDO - contradicción abierta.** Las cuatro visitas `PASA` x50/x1 usan
IDAC0=11--14 e IDAC1=6--9, con SEo=-15 a -6 mV y OPA_SUM=-18.7 a +6.2 mV.
Con (a), sólo IDAC0 implicaría +4.0 a +5.1 V en OPA_SUM; no cabe entre rieles
ni aparece en los taps. Es inválido tomar esos códigos como confirmación de
(a): puede haber convención de código/polaridad, nodo distinto o discrepancia
entre build y la placa. La documentación favorece (a), pero la transferencia
efectiva de placa aún no está demostrada.

**Decisión de compra:** no cambiar R0 todavía. Medir, con PI congelado,
IDAC1--3 fijos, A-B-A-B-A de IDAC0 (±2 o ±4 códigos), 360 s/meseta y lectura
de vuelta, SEo y OPA_SUM, a PGAgain x1 y x50/PGAout x1. (a) predice SEo=0 a
x1 y -91.875 mV/código a x50; (b), +1.875 mV/código en ambos.

## P2. Vernier diferencial

**DEDUCIDO.** La inspección física en `debug_analogico/HALLAZGOS_ANALOGICO.md`
dice que RV1 no existe: hay 680 ohm fijo. Reconstruye BPo--SUMm=7.42--7.43 k.
Así las ganancias son `-27/6.8=-3.9706` (directa) y
`-27/7.434=-3.6319` (BP). Los 51 k hallados son R2/R3 del geófono, no del
sumador. Es una contradicción documental real con TopDesign (`RV1=2k,31.7%`)
y debe prevalecer la inspección de la placa.

**MEDIDO.** IDAC1 -> OPA_SUM/SUM fue -5.24 mV/código, e IDAC1 -> LP
+17.79 mV/código (LP/SUM=-3.40) a x4/x16.

**Conclusión.** La cuenta propuesta (-14.3 mV común, -0.64 mV opuesto,
factor 22) exige dos autoridades lentas iguales. Es incompatible con (a):
IDAC0 es 0 a x1 y crece como G-1; a x50 sería ~365 mV/código teóricos, no
~7.4. Aun si (b) resultara en placa, la pendiente medida IDAC1 es -5.24, no
-7.4: falta medir IDAC0 antes de formar el vector diferencial.

**Firmware.** `control_runtime.inc` no implementa un vernier diferencial
calibrado. El aprendizaje mueve ambos lentos correlacionados desde
`CP_SLOW0/1_SLOPE_UV` (cerca de líneas 1148--1149); sólo en el refinamiento
final usa incidentalmente `n0 += sign; n1 -= sign` (1180--1181). Haría falta
medir la matriz IDAC0/1 -> SEo/OPA_SUM por ganancia, ortogonalizar vectores,
limitar/anti-windup, respetar la cola lenta y probar host y placa.

## P3. Falla del PGA alto

**MEDIDO.** Alta ganancia en PGAgain (x50/x1, x32/x2, x48/x2, x16/x8) logra
1 PASA/24; en PGAout (x4/x16, x4/x24, x4/x32, x8/x16), 13 PASA/26. En fallas
de PGA alto OPA_SUM ya queda fuera: x32/x2 frío SEo=-84.2, BPo=-27.3,
OPA_SUM=+92.0, SUM=+90.4, LP=-282.5 mV; x32/x2 desde x1 da
SEo=+71.3, BPo=+8.3, OPA_SUM=-244.9, SUM=-239.0, LP=+130.7 mV. x48/x2 repite
el patrón (-120.6/-27.4/+92.1/+90.6/-282.6 y +121.3/+4.1/-245.6/-239.7/+130).
No es sólo LP/IDAC3: el problema ya existe antes de PGAout. x16/x8 frío tiene
OPA_SUM=+11.1 pero SUM=+104.9 y LP=-268.9 mV, mostrando además que PGAout
puede saturar posteriormente.

**DEDUCIDO.** Vos máximo del PGA es 10 mV y la deriva hasta 30 uV/C; un
offset referido a entrada se proyecta aproximadamente G·Vos. Sólo 2--5 mV
efectivos dan 64--250 mV a G=32--50, como SEo observado. El mecanismo más
compatible es offset/deriva amplificado antes de que BP, desacoplado en DC,
pueda seguirlo. Con (a) IDAC0 tiene exceso de rango pero resolución
inutilizable; no hay evidencia de falta primaria de autoridad. Falta medir
su transferencia efectiva para cerrar el reparto entre cuantización y offset.

Medición necesaria: A-B-A-B-A separados de IDAC0 e IDAC1, a x4/x16 y x48/x2,
taps SEo/BPo/OPA_SUM/SUM, 360 s. Registrar voltajes absolutos frente a VDDA y
VSSA (no sólo desviación de Vref) para demostrar saturación de SEo.

## P4. `CP_COARSE_SLOPE_UV`

**DEDUCIDO.** IDAC2 y 5.1 k dan 0.6375 mV/código en Vref_ADDER. La ganancia
de referencia del sumador inversor incluye ambos caminos:
`1+27/6.8+27/7.434=8.6025`, o +5.484 mV/código en OPA_SUM. Después PGAout y
el MFB invierten; por tanto el signo esperado en LP es negativo si no hay
camino adicional. El valor -150 mV/código exige una ganancia adicional grande
y no sale de estos valores.

**SIMULADO.** `BARRIDOS_CODEX.md` adopta +9.85 mV/código a OPA_SUM y
-33.49 mV/código total a LP; con -150000, bumpless pide 333 códigos IDAC3 en
vez de ~74 y patea LP ~-116 mV. Demuestra sensibilidad del algoritmo, no mide
IDAC2. `HALLAZGOS_SIM.md` retracta correctamente el signo inferido de fotos.

**Veredicto:** -150000 es incompatible con topología nominal, pero no debe
cambiarse aún por -33490. Medir IDAC2 -> OPA_SUM y -> LP a PGAout x24, PI
congelado, A-B-A-B-A, 360 s y lectura de vuelta. Recién entonces actualizar
pendiente y comprobar en host y placa un intercambio 1 IDAC2/IDAC3 dentro de
HOLD.

### IDAC3: 6.68 versus 0.45 mV/código

**MEDIDO.** La campaña rigurosa da +0.45 mV/código (0.49 a PGAout x16, 0.41
a x1): no escala con PGAout, por lo que IDAC3 entra después de él.

**DEDUCIDO.** R3=10 k mueve su referencia 1.25 mV/código. El comentario de
`psoc_hw.h` supuso erróneamente ganancia MFB=5.3 desde referencia; una
inyección de referencia no tiene por qué atravesar la transferencia de señal.
El cociente medido 0.45/1.25=0.36 es compatible con rechazo parcial de modo
común del MFB. El 6.68 pre-bug queda refutado por A-B-A-B-A y no debe volver
al firmware.

## P5. R0/R1

No recomendar cambio todavía. Usar 1--14 de 255 códigos muestra margen, no
el mecanismo limitante. Reducir R mejora resolución pero reduce rango; no
arregla Vos, saturación, cola lenta ni un vernier no implementado. Si P1
confirma (a) y cuantización es realmente el limitante, R0 para ~7.4
mV/código a x50 sería del orden de 300 ohm, pero deja sólo ~47 mV de recorrido:
no es una receta ni una compra autorizada. R1 no se empareja con R0 bajo (a).
Si confirmara (b), dimensionar ambos por offset/deriva medidos y matriz de
autoridad, no por el 5% de una campaña.

## Plan de acción priorizado

### 1. Software sin riesgo físico

1. Corregir documentos/telemetría que presenten IDAC3=6.68; conservar
   +450 uV/código medido. Verificar por búsqueda y pruebas host.
2. No cambiar signo ni módulo de `CP_COARSE_SLOPE_UV`; el simulador revela el
   riesgo del descargue, no calibra la placa. Verificar tras la medición IDAC2.
3. Preparar telemetría y representación matricial común/diferencial inactiva.
   Éxito: pruebas host idénticas al comportamiento actual al deshabilitarla.

### 2. Medir primero

1. IDAC0 -> SEo/OPA_SUM a x1 y x50: decide (a)/(b), autoridad y resolución.
2. IDAC2 -> OPA_SUM/LP a PGAout x24: decide `CP_COARSE_SLOPE_UV` y bumpless.
3. Taps absolutos y escalones lentos x4/x16, x48/x2: decide Vos/saturación
   frente a resolución.

Éxito común: pendiente repetible A-B-A-B-A, taps lejos de rieles y predicción
del intercambio de códigos dentro de HOLD.

### 3. Hardware

1. Cambiar R0 sólo si se confirma (a) y cuantización, no Vos/saturación, es
   el limitante; verificar rango bidireccional en peor caso y paso menor que
   ventana útil.
2. Cambiar R1 sólo si la matriz confirma que el diferencial estable resuelve
   un problema real; verificar mejora repetible sin perder rango ni agravar
   la cola BP.
