# Investigación de la cadena analógica - 2026-09-26

## Método y alcance

No se abrió COM8, no se ejecutó software de puerto serie ni se grabó firmware.
**MEDIDO** designa resultados de placa; **SIMULADO**, el host `lab/sim`; y
**DEDUCIDO**, una consecuencia de topología/valores. Las visitas `FALLA` y
`APRENDIENDO` sirven para localizar taps fuera de rango, no para ajustar
pendientes.

## P1. Referencia de PGAgain

**MEDIDO — evidencia externa aportada por el dueño (captura).** `IDAC0 × R0`
entra en `PGAm_ref`, no en la referencia de PGAgain.

**DEDUCIDO — consecuencia de esa topología.** Con
`Vout=Vref+(Vin-Vref)G` y PGAm=PGAp=2: `V_m=2 INn-Vref_m` y
`V_p=2 INp-V_m=2(INp-INn)+Vref_m`. La álgebra propuesta es correcta: el INA
tiene ganancia diferencial 2 y transporta `Vref_m` con ganancia +1. PGAgain
tiene referencia fija `ref2V5`; por ello `dSEo/dVref_m=G`.

**DEDUCIDO — autoridad nominal.** Con I_FS=31.875 uA, 255 códigos y R0=15 k,
`dVref_m/dcode0=1.875 mV`; así `dSEo/dcode0=+1.875G mV/código`. La rama
directa del sumador es -27/6.8=-3.9706: `dOPA_SUM/dcode0=-7.441G mV/código`,
-29.76 mV a x4 y -372.06 mV a x50. No es `1-G`: esa derivada suponía la
topología errónea donde IDAC0 movía el Vref de PGAgain.

**MEDIDO.** Las cuatro visitas PASA x50/x1 de
`campana_techo/resultados.jsonl` terminan con IDAC0=11,12,13,14; IDAC1=9,8,6,8;
SEo=-15.0,-13.3,-9.2,-6.0 mV y OPA_SUM=+6.2,-3.5,-10.8,-18.7 mV. No son un
barrido aislado, por lo que no estiman pendiente.

**DEDUCIDO — inconsistencia aparente.** Una lectura literal de 15 k proyecta
por IDAC0 solo 1.03--1.31 V en SEo y -4.09--5.21 V en OPA_SUM.
Sin conocer offsets y cancelaciones simultáneas, esto no refuta 15 k: es una
inconsistencia aparente que exige un escalón aislado.

**DEDUCIDO — explicaciones y prueba discriminante.**

| Hipótesis | Predice | Evaluación / dato decisivo |
|---|---|---|
| R0 físico distinto | Las pendientes de IDAC0 escalan con R0. Atribuir literalmente cada final sin offset/cancelación da R0≈69--218 ohm desde SEo y ≈12--54 ohm desde OPA_SUM. | Plausible: `psoc_hw.h` documenta el precedente LP 1 k vs 10 k. No hay valor único. R0=680 aún da 4.25 mV/código SEo x50 y -16.87 mV/código OPA. Confirmar midiendo R0 desenergizada o un escalón aislado. |
| Telemetría no es código crudo | Habría escala/offset entre reporte y registro IDAC. | No decidido por `psoc_nv.c`: sólo prueba serialización EEPROM como magnitud + máscara, no el valor publicado ni el registro físico. Capturar comando, `idac_final`, máscara y `IDAC*_Data`; igualdad descarta discrepancia en ese trayecto, no una anterior. |
| I_FS distinto de 31.875 uA | La pendiente se escala por I_FS real/31.875. | Posible sólo como discrepancia de configuración/canal; la campaña no decide. Medir corriente o LSB sobre R0. |
| Atenuación hacia PGAm_ref | `dSEo/dcode0=aG·LSB`, con a<1. | Posible: la captura prueba el destino funcional, no ausencia de divisor/carga. Medir R0 y PGAm_ref durante escalón; su razón da a. |
| Ganancia PGAgain efectiva/configurada distinta | La pendiente IDAC0 escala con el G eléctrico, no necesariamente con el G informado. | Posible si hay build/configuración/tap de ganancia distinto. Inyectar un escalón conocido a la entrada y medir `ΔSEo/ΔVp` para confrontar G. |
| Escala/unidad ADC incorrecta | Los cinco taps pueden conservar el orden de nodos pero reportar pendiente/offset en mV erróneos. | Distinta de una permuta de tap. Aplicar una tensión DC trazable a cada canal ADC o comparar simultáneamente con DMM. |
| Taps distintos de los supuestos | El escalón puede estar en el nodo físico pero no en el ADC reportado. | Posible. Excitar IDAC0 aislado y contrastar los cinco ADC con DMM/sonda de SEo y OPA_SUM. |

No se puede elegir entre hipótesis con cuatro puntos de control acoplado. La
medición decisiva es A-B-A-B-A de IDAC0, con IDAC1--3 fijos y PI congelado, a
x4 y x50, registrando cinco taps, código/máscara escritos y PGAm_ref externo.
**Protocolo registrado:** A y B difieren +4 códigos desde un punto interior;
360 s por meseta, o hasta que cada tap cambie <1 LSB ADC en 10 muestras
consecutivas; guardar mediana y rango de las últimas 10 muestras, temperatura
y rieles. Repetir A-B-A-B-A en ese orden y abortar una meseta si cualquier tap
sale de su ventana válida; no usar un tramo saturado para estimar pendiente.

## P2. Vernier diferencial

**DEDUCIDO.** La inspección física en `debug_analogico/HALLAZGOS_ANALOGICO.md`
dice que RV1 no existe: hay 680 ohm fijo. Reconstruye BPo--SUMm=7.42--7.43 k.
Así las ganancias son `-27/6.8=-3.9706` (directa) y
`-27/7.434=-3.6319` (BP). Los 51 k hallados son R2/R3 del geófono, no del
sumador. Es una contradicción documental real con TopDesign (`RV1=2k,31.7%`)
y debe prevalecer la inspección de la placa.

**MEDIDO.** IDAC1 -> OPA_SUM/SUM fue -5.24 mV/código, e IDAC1 -> LP
+17.79 mV/código (LP/SUM=-3.40) a x4/x16.

**DEDUCIDO — topología corregida.** IDAC0 llega por la rama directa después
de PGAgain: `a0=-3.9706·G·LSB0`; IDAC1 llega por BP sin PGAgain:
`a1=-3.6319·LSB1`. Si ambos RSET=15 k e I_FS=31.875 uA,
`a0/a1=1.0933G`: 4.37 a x4 y 54.7 a x50. No existe el vernier propuesto de
autoridades similares salvo aproximadamente a x1 (razón 1.09). A x4 puede
existir un vernier matricial, pero requiere varios códigos IDAC1 por cada
IDAC0 y tiene rango limitado; a x50 está mal condicionado y no es práctico
con códigos enteros. Si R0 fuese 680 ohm, la razón sería 0.0496G: 0.20 a x4,
1.19 a x24 y 2.48 a x50; la coincidencia ideal cae en G≈20.2. Por eso x24,
no x50, es el régimen disponible más cercano. La conclusión ``x50 no práctico''
es condicional a R0=15 k. Esto es
DEDUCIDO, no una recomendación de firmware: primero hay que medir la matriz y
la resistencia física.

**Firmware.** `control_runtime.inc` no implementa un vernier diferencial
calibrado. El aprendizaje mueve ambos lentos correlacionados desde
`CP_SLOW0/1_SLOPE_UV` (cerca de líneas 1148--1149); sólo en el refinamiento
final usa incidentalmente `n0 += sign; n1 -= sign` (1180--1181). Haría falta
medir la matriz IDAC0/1 -> SEo/OPA_SUM por ganancia, ortogonalizar vectores,
limitar/anti-windup, respetar la cola lenta y probar host y placa.

## PREDICCIONES REGISTRADAS

**DEDUCIDO — antes de medir.** Incrementos por `+1` código firmado, con PI
congelado, otros IDAC fijos y espera DC. Si la polaridad física está invertida,
se invierte cada fila completa, no las relaciones entre taps. `—` es cero
nominal, no una lectura literalmente nula: se contrasta contra el rango basal
registrado en el protocolo; `ND`, no deducible sin inventar la transferencia. R0=680 sólo cambia
IDAC0; R1 sigue en 15 k. IDAC0 usa PGAout=x1; IDAC2, PGAgain=x1.

| Ensayo | R0 | ΔSEo mV | ΔBPo mV | ΔOPA_SUM mV | ΔSUM mV | ΔLP mV |
|---|---:|---:|---:|---:|---:|---:|
| IDAC0, PGAgain x4 | 15 k | +7.500 | — | -29.76 | -29.76* | ND |
| IDAC0, PGAgain x4 | 680 | +0.340 | — | -1.349 | -1.349* | ND |
| IDAC0, PGAgain x50 | 15 k | +93.750 | — | -372.06 | -372.06* | ND |
| IDAC0, PGAgain x50 | 680 | +4.250 | — | -16.87 | -16.87* | ND |
| IDAC1, PGAgain x4 | 15 k / 680 | — | ±1.875† | ∓6.810 | ∓6.810* | ND |
| IDAC1, PGAgain x50 | 15 k / 680 | — | ±1.875† | ∓6.810 | ∓6.810* | ND |
| IDAC2, PGAout x4 | 15 k / 680 | — | — | +5.484 | +21.94‡ | ND |
| IDAC2, PGAout x24 | 15 k / 680 | — | — | +5.484 | +131.63‡ | ND |
| IDAC3, PGAout x24 | 15 k / 680 | — | — | — | — | ND (§) |

* `SUM=OPA_SUM` presupone PGAout x1; con otro PGAout, `ΔSUM=Gout·ΔOPA_SUM`
alrededor de su Vref. No se presupone transferencia DC del LP.

† Es el escalón del nodo de referencia BP si BPo es ese nodo/una transferencia
unitaria. La autoridad segura a OPA_SUM es `-27/7.434×1.875=-6.810` mV/código.
Si BPo no da 1.875 mV, investigar tap/atenuación BP, R1, I_FS, código físico y
configuración ADC; este resultado no selecciona una causa única.

‡ Usa `(1+27/6.8+27/7.434)×0.6375=5.484` mV/código antes de PGAout. Si
OPA_SUM no vale eso o SUM no escala ×6 de x4 a x24, se refuta ubicación o
ganancia supuesta; LP requiere la función DC del MFB.

§ **DEDUCIDO:** IDAC3 mueve su referencia 1.250 mV/código con R3=10 k, pero
referencia→LP es ND; esta fila no discrimina R0=15 k de 680. **MEDIDO** en P4:
+0.45 mV/código aproximadamente, sin escala con PGAout. Ese antecedente no es
una predicción ni criterio de aceptación de la nueva medida; se registra aparte
para detectar una incompatibilidad de configuración/tap.

**Criterio de decisión registrado.** Bajo código→corriente, I_FS, taps y
linealidad ya verificados, IDAC0 separa los dos modelos nominales por 22.06 y
debe escalar x50/x4=12.5. La pendiente IDAC0 sola no identifica R0: R0,
I_FS, atenuación y escala de código son multiplicativos. Medir R0 desenergizada
identifica R0; corriente-vs-código separa I_FS/código; ΔPGAm_ref/(I·R0) prueba
atenuación; DMM frente a ADC prueba el tap. IDAC1 debe ser igual a x4/x50 e
IDAC2 igual en OPA_SUM y ×6 en SUM entre x4/x24, también bajo esas condiciones.

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

**DEDUCIDO — hipótesis, no selección causal.** Vos máximo del PGA es 10 mV y
la deriva hasta 30 uV/C; un offset referido a entrada se proyecta aproximadamente
G·Vos. Sólo 2--5 mV efectivos dan 64--250 mV a G=32--50, como SEo observado.
Offset/deriva amplificado antes de BP es compatible, pero no queda seleccionado
frente a saturación, ganancia efectiva, tap/configuración o atenuación: no hay
escalón aislado. Si se confirma pendiente IDAC0 alta escalada por PGAgain, su
rango puede exceder el útil mientras la resolución resulta inservible; falta
medir la transferencia para repartir cuantización y offset.

Medición necesaria: A-B-A-B-A separados de IDAC0 e IDAC1, a x4/x16 y x48/x2,
taps SEo/BPo/OPA_SUM/SUM. Aplicar el **Protocolo registrado** de P1 (Δ=+4,
criterio DC, últimas 10 muestras, temperatura/rieles y abortar saturación) y
registrar voltajes absolutos frente a VDDA y VSSA, no sólo Vref.

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
congelado, usando el **Protocolo registrado** de P1 y lectura de vuelta. Recién entonces actualizar
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

**DEDUCIDO.** No recomendar cambio todavía. Usar 1--14 de 255 códigos muestra
margen, no el mecanismo limitante. Reducir R mejora resolución pero reduce
rango; no arregla Vos, saturación, cola lenta ni un vernier no implementado.
Si P1 confirma una pendiente efectiva IDAC0 alta y cuantización es el
limitante, R0 para ~7.4 mV/código a x50 sería del orden de 300 ohm, pero deja
sólo ~47 mV de recorrido: no es una receta ni una compra autorizada. R1 no se
empareja automáticamente con un R0 bajo; ambos se dimensionan por
offset/deriva medidos y la matriz de autoridad, no por el 5% de una campaña.

## Plan de acción priorizado

### 1. Software sin riesgo físico

1. Corregir documentos/telemetría que presenten IDAC3=6.68; conservar
   +450 uV/código medido. Verificar por búsqueda y pruebas host.
2. No cambiar signo ni módulo de `CP_COARSE_SLOPE_UV`; el simulador revela el
   riesgo del descargue, no calibra la placa. Verificar tras la medición IDAC2.
3. Preparar telemetría y representación matricial común/diferencial inactiva.
   Éxito: pruebas host idénticas al comportamiento actual al deshabilitarla.

### 2. Medir primero

1. IDAC0 -> SEo/OPA_SUM a x4 y x50: confronta las predicciones registradas,
   autoridad y resolución; x1 sólo sería un ensayo adicional.
2. IDAC2 -> OPA_SUM/LP a PGAout x24: decide `CP_COARSE_SLOPE_UV` y bumpless.
3. Taps absolutos y escalones lentos x4/x16, x48/x2: decide Vos/saturación
   frente a resolución.

Éxito común: pendiente repetible A-B-A-B-A, taps lejos de rieles y predicción
del intercambio de códigos dentro de HOLD.

### 3. Hardware

1. Cambiar R0 sólo si se confirma una pendiente efectiva IDAC0 alta y
   cuantización, no Vos/saturación, es el limitante; verificar rango
   bidireccional en peor caso y paso menor que
   ventana útil.
2. Cambiar R1 sólo si la matriz confirma que el diferencial estable resuelve
   un problema real; verificar mejora repetible sin perder rango ni agravar
   la cola BP.
