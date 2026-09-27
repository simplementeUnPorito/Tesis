# Barridos del lazo host (2026-09-26)

## Alcance

Esto es **simulación**, no medición de placa. Se compiló `control_config.c` para host mediante `lab/sim/simulador_lazo.py`. No se abrió COM8, no se ejecutó ningún script de puerto y no se grabó firmware.

Se usaron sin modificarlos: IDAC3->LPo = +450 uV/código; IDAC1->SUMo = -5240 uV/código; LPo/SUMo = -3,40; IDAC2->SUMo = +9850 uV/código; por lo tanto IDAC2->LPo total = -33490 uV/código; tau lento/LP = 40/25 s. En `Planta`, `c_coarse` es un camino directo adicional a `a_lp*SUMo`; se fijó a cero para no contar dos veces la inversión y dejar el efecto total de IDAC2 en -33490 uV/código. Salvo indicación, las muestras son cada 3 s. `hold=1` significa que la histéresis congeló el firmware.

## Hallazgo 1 — `CP_COARSE_SLOPE_UV=-150000` es inconsistente y rompe el descargue bumpless

**Barrido.** Planta anterior, `IDAC3=+245`, `IDAC2=0`, LPo inicial +20 mV (dentro de HOLD). Se comparó fábrica contra -33490.

| `CP_COARSE_SLOPE_UV` | Compensación calculada por -1 IDAC2 | IDAC3 tras descargar | LPo a 6 s | LPo a 27 s |
|---:|---:|---:|---:|---:|
| -150000 (fábrica) | -333 códigos (limitado por rango) | -88 | +20,0 mV | -46,1 mV |
| -33490 (planta) | -74 códigos | +171 | +20,0 mV | +20,1 mV |

Para un movimiento IDAC2=-1, LP cambia +33,490 mV. La compensación necesaria es `-33490/450=-74,4` códigos de IDAC3. Fábrica pide -333,3: desde +245 deja IDAC3=-88 y la compensación física queda `+33,490 - 333*0,450 = -116,4 mV`. En simulación sale de HOLD y vuelve a actuar.

**Significado.** Éste es el único valor de fábrica directamente incompatible con las pendientes físicas entregadas: su módulo es 4,48 veces demasiado alto. `CP_FINE_SLOPE_UV=+450` sí coincide. El signo negativo de grueso coincide con el efecto total deducido; no hay sustento para cambiar sólo el signo.

**Confirmación en placa.** Con PI congelado, medir escalones A-B-A-B-A de IDAC2 y LPo, con espera para ambos tau y lectura del código aplicado. Confirmar además que no exista un camino directo IDAC2->LPo omitido por la deducción.

## Hallazgo 2 — pasos: ninguno cruza la ventana por sí solo; el descargue mal compensado sí puede hacerlo

**Barrido.** Conversión de pasos de fábrica usando las pendientes dadas. El rescate duplica 25 a 50 y se limita a 64 antes de bisección.

| Parámetro | Códigos/acción | Movimiento LPo | ¿cruza 194 mV de ventana completa? |
|---|---:|---:|---|
| `CP_FINE_STEP=1` | 1 IDAC3 | +0,450 mV | No |
| `CP_RESCUE_STEP=25` inicial | 25 IDAC3 | +11,25 mV | No |
| rescate expandido | hasta 64 IDAC3 | hasta +28,8 mV | No |
| `CP_COARSE_STEP=1` | 1 IDAC2 | -33,49 mV | No |

**Significado.** No aparece incompatibilidad física directa en esos tres tamaños. Pero con la pendiente gruesa de fábrica el contramovimiento del Hallazgo 1 genera físicamente ~116 mV: más que el semiancho válido de 97 mV, aunque IDAC2 aislado sólo mueva 33,49 mV. Por tanto el riesgo está en la pareja grueso/vernier, no en `CP_COARSE_STEP=1` aislado.

**Confirmación en placa.** Medir transitorio y valor final de 1 código IDAC2 y de 25/50/64 códigos IDAC3; luego comprobar que un descargue 1 código IDAC2 / ~74 IDAC3 permanezca dentro de HOLD.

## Hallazgo 3 — `pi.slope_uv` subestima porque observa antes de asentar

**Barrido.** Planta de +450 uV/código exactos, LPo inicial +35 mV, sin guarda SUMo; se variaron `CP_PERIOD_MS` y tau LP. Se informa el último `pi.slope_uv` del firmware. Entra pronto a HOLD y deja de observar, por lo que no hay convergencia asintótica asegurada a 450.

| `CP_PERIOD_MS` | tau LP=10 s | tau LP=25 s | tau LP=40 s | tau LP=80 s |
|---:|---:|---:|---:|---:|
| 1 s | 142 | 100 | 118 | 105 |
| 3 s (fábrica) | 185 | **149** | 114 | 107 |
| 6 s | 314 | 171 | 163 | 116 |
| 10 s | 284 | 247 | 177 | 140 |
| 20 s | 389 | 359 | 284 | 177 |

Valores en uV/código. Traza nominal (3 s/25 s): 3 s LPo=35,0, IDAC3=-32; 6 s 33,4/-57; 9 s 30,7/-97/slope=108; 12 s 26,2/-137/slope=111; 15 s 20,2/-137/slope=149 y HOLD.

**Significado.** En simulación, con `CP_PERIOD_MS=3 s` y tau LP=25 s, mide ~149 frente a 450 reales. El sesgo empeora al disminuir período/tau: 1/25 dio 100 y 3/80 dio 107. Períodos mayores lo reducen en este barrido, pero no monótonamente de forma garantizada: la cuantización, rescate y entrada a HOLD cambian las muestras. No se debe calibrar una constante a partir de esta tabla.

**Confirmación en placa.** Registrar LPo tras un escalón de IDAC3 hasta asentamiento y comparar la pendiente reportada con una pendiente A-B-A-B-A de régimen para varios períodos.

## Hallazgo 4 — barrido de PI: no osciló en el modelo nominal, pero no prueba robustez

**Barrido.** LPo inicial +35 mV, sin guarda SUMo, tau LP=25 s, período 3 s; se cruzaron `CP_TAU_MS` y Kp (`0, 1/4, 1, 2, 4`). Filas representativas:

| `CP_TAU_MS` | Kp | mínimo/máximo LPo | LPo final | primer HOLD |
|---:|---:|---:|---:|---:|
| 3 s | 0 | -19,0 / +35,0 mV | -18,1 mV | 12 s |
| 3 s | 4 | -16,3 / +35,0 mV | -15,4 mV | 12 s |
| **9 s fábrica** | **1/4 fábrica** | **-26,7 / +35,0 mV** | **-25,8 mV** | **15 s** |
| 18 s | 4 | -10,0 / +35,0 mV | -1,4 mV | 15 s |
| 30 s | 4 | +6,2 / +35,0 mV | +6,2 mV | 18 s |
| 60 s | 1/4 | +7,1 / +35,0 mV | +7,1 mV | 27 s |

**Significado.** En simulación, fábrica no tiene oscilación sostenida ni arrastre en esta condición: cruza una vez a -26,7 mV y HOLD lo congela (sólo 1,7 mV fuera de HOLD). El barrido no concluye que sea óptimo ni robusto: la histéresis lo corta en 12--27 s y los errores mayores de DEADBAND usan bisección, no PI. No se infiere estabilidad ante ruido, retardo adicional o deriva real.

**Confirmación en placa.** Inyectar escalones pequeños que queden entre HOLD y DEADBAND, registrar IDAC3/LPo por tick y medir sobrepaso, establecimiento y ciclos límite con ruido real.

## Hallazgo 5 — la guarda SUMo tiene no-convergencias simuladas pese a autoridad disponible

**Barrido.** LPo inicial +90 mV (válido, fuera de HOLD), barrido de SUMo inicial y `CP_COARSE_SLOPE_UV` de fábrica. `off_lp` sólo se ajustó para preservar LPo inicial. Cada celda: `SUMo, LPo, IDAC3, IDAC2` a 60/300/900 s.

| SUMo inicial | 60 s | 300 s | 900 s | estado 900 s |
|---:|---|---|---|---|
| -70 mV | -60,+47,-25,+2 | -50,-42,-145,+2 | -50,-41,-143,+2 | HOLD |
| -100 mV | -90,+47,0,+2 | -58,-51,+97,+4 | -51,-33,+98,+5 | HOLD |
| -160 mV | -150,+47,0,+2 | -99,-82,+175,+7 | -60,**-185**,+222,+10 | sin HOLD |
| +100 mV | +90,+84,-175,-2 | +60,**+148**,-255,-4 | +58,**+195**,-122,-4 | sin HOLD |
| +160 mV | +150,+84,-175,-2 | +99,**+196**,-255,-7 | +59,**+375**,-222,-10 | sin HOLD |

Extendidas a 3600 s: +100 terminó LPo=+164,5 mV, IDAC3=+78, IDAC2=-4; -160 terminó -164,4 mV, IDAC3=+255, IDAC2=+11. Ambos conservan mucho rango IDAC2 (+/-255); el +100 tampoco agotó IDAC3. Repetir +100 con `CP_COARSE_SLOPE_UV=-33490` no lo resolvió: terminó +99,5 mV, IDAC3=-255, IDAC2=-3.

**Significado.** En simulación hay combinaciones sin convergencia aunque sobra rango. No es atribuible sólo a la pendiente gruesa errada, porque persiste con -33490. El mecanismo es la interacción de guarda (prioriza un IDAC2 cada `CP_COARSE_MS=45 s`), acople lento y rescate de IDAC3 cuando LPo sale de válido. Es una patología simulada de arquitectura/control; no un hecho de placa.

**Confirmación en placa.** En una campaña posterior a la medición actual, preparar SUMo +100/-160 mV y LPo válido ~+90 mV; registrar LPo, SUMo, IDAC2 e IDAC3 más de una hora. Confirmar primero signo y cola de un código IDAC2. Si se reproduce, medir una variante donde IDAC3 pueda corregir LPo válido durante la guarda SUMo.

## Prioridad

1. Medir directamente IDAC2->SUMo y IDAC2->LPo y, si confirma -33,49 mV/código, corregir `CP_COARSE_SLOPE_UV`: es la única incompatibilidad directa y hoy invalida bumpless.
2. Verificar y rediseñar la interacción guarda SUMo--IDAC2--rescate IDAC3: la simulación tiene no-convergencias con autoridad disponible y corregir sólo la pendiente no las eliminó.
3. Hacer que el estimador observe un escalón asentado, o evitar que su estimación parcial gobierne el PI: 3 s/25 s dio 149 frente a 450 uV/código.
4. Sólo después retunar `CP_TAU_MS`/Kp en transitorios medidos; el modelo nominal no osciló, pero no demuestra robustez.
