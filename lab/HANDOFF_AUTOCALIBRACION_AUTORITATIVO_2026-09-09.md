# Handoff autoritativo: autocalibración analógica GEO

## Corrección física autoritativa — 2026-09-10 09:05

Elías corrigió el dato físico: **IDAC2 e IDAC3 permanecen ambos en 10 kOhm**.
El cambio propuesto de IDAC2 a 5,1 kOhm no se realizó. Esto reemplaza cualquier
cabecera o runbook posterior que lo diera por instalado. Se corrigieron los
metadatos de `psoc_hw.h` y `testbench/core/checklist.py` a 10 kOhm.

La medición estacionaria posterior, que no depende del valor declarado, dio
IDAC2→OPA_SUMo = 9,56 mV/código de mediana (DE 1,97 mV/código). En código 254,
OPA_SUMo queda en mediana 943,05 mV de banco, equivalente a −1,164 V respecto
de Vref. Un ABBA adicional de IDAC1 midió +2,188 mV/código sobre BPo y
−17,05 mV/código sobre OPA_SUMo: centrar BPo cerca de código 188 deja OPA_SUMo
aproximadamente −1,9 V aun con IDAC2=254. Una corrección sólo resistiva pediría
~18 kOhm, pero produciría un paso estimado de ~0,86 V/código después de PGAout
x50. La causa es estructural: cero DC desplazado más corrección situada antes
de la ganancia variable. Priorizar corregir el cero o mover/conmutar la
autoridad; no cambiar IDAC3 mientras SUM siga saturado.

## Estado vigente — 2026-09-10 00:27

> **ESTA ACTUALIZACIÓN REEMPLAZA EL ESTADO DE CORTE HISTÓRICO QUE SIGUE.**
> Esta sección contenía una premisa física incorrecta: el IDAC2 no fue cambiado
> a 5,1 kOhm. Rige la corrección autoritativa inmediatamente anterior.

- Implementación: `src/interfaces/python/autocalibracion_dos_fases.py`.
- Fase 1: `[IDAC0,IDAC1]=[19,140]`, una sola vez. En la última tanda:
  62,53 ± 0,85 s, máximo 64,01 s.
- Fase 2 normal: cambios x1→x50 en 4,80..9,01 s por ganancia.
- Validación final de la versión vigente: 10/10 campañas completas y 100/100
  cambios PASS, incluyendo retorno x50→x1 en cada campaña. Recorrido completo:
  121,78 ± 1,93 s, p95 124,32 s, máximo 124,81 s.
- Una tanda previa de 15 campañas descubrió deriva persistente en x2: 14/15
  completas, 141/142 cambios PASS. La guarda restauró x1 sin barrer rieles.
  Se añadió una descarga neutra excepcional de fase 2 antes del último intento.
- La versión final tiene 3/3 pruebas unitarias de recuperación y aborto seguro.
- Punto operativo reutilizado: `[19,140,254,83]`.
- EEPROM: escritura x1 aceptada después de reverificar las cinco señales.
- Alcance del PASS: PGAgain, BPo y LPo legibles. Los taps ch2/ch3 no son
  fiables tras el recorrido: en la tanda final fueron ambos válidos en 10/20
  mediciones x1, 9/10 x2 y 0/10 desde x4. No interpretar PASS como cinco taps.
- En las 10 campañas finales hubo 0 búsquedas amplias/rieles y 10 reintentos de
  escritura recuperados automáticamente.
- Pendiente real: comprobar restauración de EEPROM tras un power-cycle físico.
- Estadística final: `RESULTADOS_ENDURANCE_RECOVERY_DOS_FASES_2026-09-10.md`.
- Hallazgo y guarda previa: `RESULTADOS_ENDURANCE_DOS_FASES_2026-09-10.md`.
- Informe nocturno consolidado: `RESULTADOS_NOCTURNOS_CONSOLIDADOS_2026-09-10.md`.

## Estado de corte histórico — 2026-09-09 10:50

**Corte de información:** 2026-09-09 10:50 (America/Asuncion), después de
reprogramar la medición sin el capacitor auxiliar, interrumpir la última
identificación y dejar la placa apagada.

> **LEER PRIMERO EN UN CHAT NUEVO.** Ésta es la fuente única de continuidad.
> El hardware está apagado, IDAC2 todavía tiene 10 kOhm y el próximo paso
> físico aprobado es cambiar **únicamente IDAC2→Vref de OPAsum a 5,1 kOhm**.
> Después hay que seguir, sin improvisar, el runbook
> `RUNBOOK_POST_CAMBIO_IDAC2_5K1.md`. No ejecutar los informes viejos como si
> probaran x24: las mediciones anteriores a las 09:17 cargaban los nodos con el
> capacitor del AMux.

Este documento reemplaza como fuente de estado a
`INFORME_AUTOCALIBRACION_2026-09-08.md`. Ese informe describía correctamente
las corridas que se hicieron, pero su conclusión de “x24 validado” quedó
invalidada al descubrir que el comando DC conectaba el capacitor auxiliar en
paralelo con el nodo medido. No borrar los archivos viejos: son historia útil,
pero no evidencia de calibración de la planta sin carga.

## 1. Objetivo acordado

Dejar el PSoC capaz de autorregularse sin PC ni semillas precargadas:

- lazo cerrado, nunca una tabla abierta como solución final;
- estimar primero la constante de tiempo dominante usando BPo, canal 1;
- permitir como mínimo PGA x50 y PGAout x24 de manera fiable;
- intentar x32/x48/x50 sólo después de garantizar x24;
- salto tipo Newton/Jacobiano permitido para acercamiento, seguido por PI
  pequeño que cierre y verifique el residual;
- comparar secuencial y vectorial, pero conservar el método más seguro y
  repetible, no forzar el vectorial;
- guardar en EEPROM únicamente una calibración que haya convergido y haya sido
  verificada; una EEPROM previa puede acelerar un arranque futuro, pero no
  puede ser necesaria para que el algoritmo converja desde cero;
- registrar cada ensayo en CSV/JSON y probar el algoritmo final en hardware;
- no modificar TopDesign desde código. El TopDesign actualmente presente fue
  editado manualmente por Elías y debe preservarse.

Condición de laboratorio conocida: puede haber oscilación de red cercana a
50 Hz. No se debe confundir esa componente periódica con falta de convergencia
DC ni sobreadaptar el controlador para eliminarla; con el geófono enterrado se
espera que sea bastante menor. Aun así, el promedio y las guardas de riel deben
ser fiables con el ruido presente.

Estado al corte: **objetivo todavía no obtenido**. El siguiente cambio físico
acordado es IDAC2 de 10 kOhm a 5,1 kOhm. La placa ya fue neutralizada y apagada;
hasta confirmar el reemplazo no se deben cambiar los metadatos a 5,1 kOhm ni
reanudar pruebas energizadas.

## 2. Proyecto y equipo exactos

- Repositorio: `C:\Github\Tesis`.
- Proyecto PSoC que se debe usar:
  `src\firmware\psoc\AcondicionamientoAnalogicoTest\AcondicionamientoAnalogico.cydsn`.
- No confundirlo con la variante de campo de cinco canales. La variante vigente
  y mejor instrumentada es la de **seis canales**.
- Enlace de banco: ESP esclavo por `COM8`, 115200 baud. Abrir COM8 reinicia el
  ESP, no necesariamente el PSoC.
- Perfil observado: GEO, PSoC presente, enlace arriba.
- Binario PSoC programado el 2026-09-09 09:17:55
  (`CortexM3\ARM_GCC_541\Debug\AcondicionamientoAnalogico.hex`): SHA-256
  `C06F878CD1A52ED9B80B818E57A1327095AACC75BA9F6104587FCC577E998335`.
  El SHA-256 `EC1BB4D55D57DB4460F74F088D2C3AF69CB46D3AA2B007D48FE14C35EB6417FE`
  corresponde a `Generated_Source\PSoC5\config.hex`, no al archivo que leyó
  Programmer. Se deja la distinción para evitar comparar artefactos distintos.
- Log de programación:
  `C:\Users\elias\AppData\Local\Temp\psoc_program_geo_2604_20260909_091716.log`.
  Todas las filas programadas fueron verificadas y la sesión terminó OK.
- Rebuild final: exitoso, 71.064 bytes flash, 17.392 bytes SRAM, 286 filas.
- Advertencia pendiente del build: violación de setup CyBUS_CLK→CyBUS_CLK
  (`sta.M0019`, Warning-1366). No impidió compilar/programar, pero debe quedar
  visible y resolverse antes de declarar firmware de campaña definitivo.

## 3. Topología vigente

### AMux_ADC

| Canal | Nodo físico | Uso |
|---:|---|---|
| 0 | `PGAgain_mux` | salida del primer PGA; recordar: ch0 siempre es PGA |
| 1 | `BPo_mux` | salida del pasabanda; aquí se estima tau |
| 2 | `OPA_SUMo` | salida de OPAsum, antes de PGAout |
| 3 | `SUMo_mux` | salida de PGAout |
| 4 | `LPo_mux` | salida final del pasabajos/entrada útil del ADC |
| 5 | `AMuxCapacitor` | capacitor auxiliar; no es un tap de señal |

### Actuadores

| IDAC | Referencia actual | Resistencia al corte | Estado |
|---:|---|---:|---|
| 0 | `Vref_PGA` / PGAgain | 15 kOhm | vigente |
| 1 | `Vref_BP` / OPAbp | 15 kOhm | vigente |
| 2 | referencia de **OPAsum** | 10 kOhm | cambio a 5,1 kOhm aprobado, aún no realizado |
| 3 | `Vref_LP` | 10 kOhm | vigente, no cambiar por ahora |

PGAout quedó referenciado a 2,5 V fijos. IDAC2 **ya no** referencia PGAout:
entra en OPAsum y por eso afecta en cascada `OPA_SUMo`, `SUMo` y `LPo`.
IDAC3 actúa al final y sirve para el ajuste fino de LPo.

Los cuatro IDAC están configurados por C en el rango fino nativo
0–31,875 uA, 0,125 uA/código. La polaridad es externa, controlada por los bits
de `polarity_reg`, y el rango firmado expuesto es -255..+255. No usar 255 uA ni
2,04 mA. El orden implementado es polaridad primero y magnitud después para no
generar un pulso con signo viejo.

**Inconsistencia de metadatos pendiente:** `testbench/core/checklist.py` refleja
10 kOhm para IDAC2, pero `psoc_hw.h` todavía define
`PSOC_IDAC_PGAOUT_RSET_OHM 1500u`; el nombre también quedó heredado de la
topología anterior. Esa constante afecta cálculos/telemetría nominales, no la
resistencia física. Actualizarla a 5100 sólo después del cambio real.

## 4. Historia de hardware que no se debe confundir con el estado actual

1. La placa comenzó con cuatro resistencias de 15 kOhm.
2. Se ensayaron cambios en LP (incluido 3,9 kOhm) y combinaciones antiguas con
   33 kOhm/47 kOhm. Pertenecen a otra asignación de referencias.
3. En la topología donde IDAC2 entraba en Vref de PGAout se usó 1,5 kOhm. En
   PGAout x1 esa entrada tiene autoridad nula porque su ganancia es `1-G`.
4. Luego IDAC2 se trasladó a la referencia de OPAsum y PGAout se dejó a 2,5 V.
   Se instaló 10 kOhm en IDAC2 y 10 kOhm en LP.
5. Con la topología vigente se observó manualmente una calibración razonable
   alrededor de `[IDAC0, IDAC1, IDAC2, IDAC3] = [0, -110, -15, 200]` con las
   ganancias mostradas en la GUI. Es evidencia de que los cuatro actuadores
   responden, no una semilla autorizada para el algoritmo final.
6. El próximo cambio aprobado es **únicamente IDAC2: 10 kOhm → 5,1 kOhm**.
   Todavía no está instalado. IDAC3 queda en 10 kOhm y los cuatro IDAC quedan
   en el rango 0–31,875 uA (0,125 uA/bit).

Mediciones manuales de las referencias contra masa, útiles para comprobar
polaridad y autoridad eléctrica:

| Referencia | código +255 | código -255 | nota |
|---|---:|---:|---|
| Vref_PGA | 2,76 V | 2,14 V | responde en ambos sentidos |
| Vref_BP | 2,76–2,81 V | 1,91 V | responde; hubo variación temporal |
| antigua Vref_PGAout, R=1,5 kOhm | 2,40 V | 2,33 V | excursión pequeña |
| Vref_LP, R=10 kOhm | 2,73 V | 2,16 V | responde |
| IDAC2 ya en OPAsum, R=10 kOhm | 2,77 V | 2,13 V | responde |

## 5. Escala correcta del banco

`Lab.measure_dc()` informa una lectura interna del banco próxima a 1 V; no son
voltios físicos directos del tap. La recta medida con tester está en
`src/interfaces/python/escala_banco.py`:

```text
Vreal[mV] = 19,9157 * banco[mV] - 17533,5
```

- Objetivo Vref: 1001,5 mV de banco ≈ 2,415 V reales.
- Mínimo interpretable: 880,4 mV de banco ≈ 0 V.
- Máximo interpretable: 1122,7 mV de banco ≈ Vdda ≈ 4,826 V.
- Un cambio de 1 mV del banco representa ≈19,92 mV físicos.
- Valores fuera de 880,4..1122,7 pueden indicar saturación, pero su magnitud ya
  no se puede convertir a tensión real.

El código Python antiguo usaba objetivo 1.000.000 uV de banco y trataba límites
físicos como si fueran unidades del banco. `autocalibrar_seguro.py` fue
parcialmente corregido para usar `BANCO_VREF_MV`, `FACTOR` y la ventana válida.
La simulación interna todavía no fue reescalada: actualmente el self-test da
0/180 y, aunque el proceso devuelve exit code 0, **no es un PASS**.

## 6. Hallazgo que invalida las conclusiones anteriores

Hasta la reprogramación de las 09:17, el comando DC y el calibrador autónomo
seleccionaban el tap con:

```c
psoc_amux_select_exclusive(channel, 1u)
```

El segundo argumento conectaba también `AMuxCapacitor` en paralelo. En nodos de
alta impedancia esto no sólo filtró ruido: cambió el punto de operación, sacó
temporalmente nodos saturados del riel y generó una deriva artificial larga.
Así, varias corridas parecían converger a pocos mV aunque no estaban observando
la planta sin carga.

La comparación decisiva fue:

- comando DC con capacitor: OPA_SUM/SUM aparecían cerca de 920–1000 mV;
- comando AC sin capacitor, misma configuración: ch2 ≈732,0 mV y ch3 ≈737,9
  mV, ambos fuera del rango físico válido por abajo.

Cambios ya compilados y programados:

- `AcondicionamientoAnalogico.cydsn/calibration.c`: calibración selecciona cada
  tap con `with_cap=0`;
- `AcondicionamientoAnalogicoTest/.../psoc_selftest.h`: comando DC usa
  `with_cap=0`.

No volver a conectar ch5 durante una medición DC de control. El FIR digital de
128 taps sí puede usarse porque no carga el circuito.

## 7. Evidencia limpia posterior a la corrección

Con PGA x50, PGAout x1 y los cuatro IDAC en cero, inmediatamente después de
programar:

| Tap | lectura banco | interpretación |
|---|---:|---|
| ch0 PGAgain | 984,821 mV | válida |
| ch1 BPo | 985,641 mV | válida |
| ch2 OPA_SUMo | 731,964 mV | saturado/fuera de rango bajo |
| ch3 SUMo | 737,781 mV | saturado/fuera de rango bajo |
| ch4 LPo | 1106,586 mV | válida, alta |

Barrido mínimo IDAC2, x1, sin capacitor y restaurado a cero:

```text
codigo 0..8 : ch2 ≈732 mV (riel bajo; no hay pendiente medible allí)
codigo 9    : ch2 ≈771 mV (todavía inválido)
codigo 10   : ch2 ≈850 mV (todavía inválido)
codigo 11   : ch2 ≈928 mV (reentra en ventana válida)
```

En una repetición con historia distinta, código 10 produjo ch2≈1036 mV y
ch3≈1046 mV, mientras LPo terminó en el riel bajo; código 11 llevó ch2/ch3 cerca
del riel alto. Después de volver a cero, ch2 se observó primero ≈1056 mV y más
tarde ≈891 mV. Conclusión: IDAC2 funciona, pero 10 kOhm deja una transición
muy gruesa y la cadena muestra memoria/recuperación suficientemente grande como
para que un dwell de 0,5–10 s no defina un punto estacionario.

Archivo limpio creado tras la corrección:
`lab/calibracion_nueva/idac2_sin_carga_20260909_092616.csv`. Es corto porque una
respuesta serie faltante abortó la adquisición; aun así conserva el punto
obtenido. El runner `diagnosticar_idac2.py` ahora registra sólo ch2/ch3/ch4, usa
x1, limita IDAC2 a ±32 y restaura cero en `finally`; todavía hay que añadir
reintentos de lectura antes de usarlo para una corrida larga.

## 8. Qué datos anteriores siguen sirviendo

Los JSON/CSV anteriores a las 09:17 no sirven para declarar error DC final,
pendiente real ni tasa de éxito del autocalibrador. Sí conservan valor para:

- demostrar que UART, comandos de ganancia, escritura firmada de IDAC y logging
  funcionaban;
- reconstruir la secuencia de algoritmos ensayados;
- mostrar que hay dinámicas lentas y saturación;
- revisar bugs de identidad/respuesta tardía del protocolo.

No volver a presentar como válidos:

- “x24 pasó 6/6”; esos PASS midieron con el capacitor conectado;
- las semillas por ganancia del informe del 08/09;
- pendientes/Jacobianos calculados mezclando topologías, escalas de IDAC o el
  capacitor auxiliar;
- la conclusión de que IDAC2 carecía de autoridad rápida: estaba en un plateau
  saturado y la unidad física estaba mal interpretada.

## 9. Algoritmos ensayados y conclusión provisional

Se escribieron variantes PI secuencial, Jacobiano/Newton vectorial, Hadamard,
vectorial por bloques, híbrido Newton+PI y búsqueda local de plateau. No existe
aún una comparación cuantitativa válida entre ellas porque las corridas físicas
que las comparaban preceden al arreglo de medición.

Lo aprendido, independientemente de esos valores contaminados:

- Un Jacobiano medido cerca de saturación no extrapola; cambia con la ganancia
  y con la región de operación.
- Mezclar en una única identificación las plantas rápidas con BPo (polo lento)
  confunde deriva temporal con acople entre actuadores.
- El vectorial puede reducir iteraciones sólo dentro de una región lineal y con
  todos los taps observables. No es buen mecanismo de rescate desde un riel.
- Una búsqueda local/bracket por actuador es más segura para entrar en ventana;
  el salto Newton debe quedar dentro del bracket medido y ser verificado.
- El PI pequeño posterior es obligatorio: Newton sólo acerca, no certifica.
- PGAgain y BPo pueden tratarse como guardas si ya están dentro de ±500 mV; no
  conviene moverlos sólo para lograr cero si eso satura etapas posteriores.
- OPA_SUMo debe quedar dentro de ±1 V y preferentemente centrado antes de subir
  PGAout. SUMo y LPo necesitan guardas de riel durante cada movimiento.
- LPo se centra al final con IDAC3 para maximizar el rango del ADC.

Arquitectura acordada, dividida en dos rutinas:

### Rutina A: calibración lenta de arranque

1. Arrancar con PGAout x1, sin usar EEPROM como requisito.
2. Esperar estabilidad observada de las medias; no un delay fijo ciego.
3. Calibrar IDAC0 contra PGAgain/ch0.
4. Estimar tau del pasabanda leyendo **ch1**. La excitación preferida es un
   movimiento pequeño de IDAC0, porque ese cambio cruza el acoplamiento lento
   PGA→BP; si se usa otro actuador debe demostrarse que excita el mismo polo.
5. Calibrar IDAC1 contra BPo/ch1 y verificar el tramo lento durante 2*tau.
6. En x1 centrar IDAC2 contra OPA_SUMo/ch2 y terminar IDAC3 contra LPo/ch4.
7. Verificar y guardar por separado el bloque común IDAC0/IDAC1.

### Rutina B: cambio rápido de PGAout

1. Congelar IDAC0 e IDAC1; PGA y BP no cambiaron.
2. Antes de conmutar, comprobar que el error de ch2 multiplicado por la ganancia
   pedida no puede llevar ch3 al riel.
3. Cambiar **directamente** a la ganancia solicitada. No recorrer 2→4→8→… ni
   buscar un único par universal para todas las ganancias.
4. Recalibrar sólo IDAC2 observando ch2/ch3 e IDAC3 observando ch4.
5. Confirmar estabilidad rápida; un segundo es el límite inicial holgado que
   debe medirse después del cambio de resistencia.
6. Si converge, guardar el par IDAC2/IDAC3 asociado a esa ganancia. Si falla,
   restaurar el último estado seguro e informar; opcionalmente ejecutar A.

Después de garantizar x24 desde varios arranques se prueban x32/x48/x50.

Tolerancias de cierre iniciales: PGAgain ±20 mV físicos; BPo ±50 mV físicos,
porque la oscilación ambiental de su media puede superar ±20 mV. La guarda de
seguridad/uso para ambos continúa en ±500 mV. No confundir tolerancia deseada
del controlador con guarda de riel.

### Estructura obligatoria de cada ajuste

Elías confirmó que **todos los IDAC, en ambas rutinas**, deben usar el mismo
patrón: identificación local o Jacobiano válido → salto Newton acotado → PI
pequeño → verificación en lazo cerrado. Newton no sustituye al PI.

Queda pendiente cuantificar cuánto cambia el Jacobiano entre repeticiones,
temperatura, código de operación y ganancia. Si la dispersión es pequeña puede
guardarse por ganancia en EEPROM y usarse como inicialización para ahorrar la
identificación; el PI seguirá cerrando el residual. Si cambia mucho o el punto
sale de su región válida, se reidentifica. Comparar tiempo total de identificar
contra tiempo ahorrado antes de decidir: no precargarlo sólo por intuición.

## 10. Comparadores agregados por Elías

TopDesign contiene `Comp_BP`, `Comp_SUM`, `Comp_LP` muestreados a 1 kHz y
agrupados en `Comp_ref_reg`. El firmware actual no los inicia ni lee.

Pueden indicar de qué lado de Vref está cada referencia, pero un bit de signo no
mide velocidad de deriva, amplitud, distancia al riel ni estabilidad. Para
certificar asentamiento son inferiores a las medias ADC sucesivas. Dejarlos
presentes por ahora y no basar el lazo en ellos; evaluar su costo de recursos y
la advertencia de timing antes de decidir si se eliminan manualmente.

Elías observó que, después del encendido, las tensiones generadas por los VDAC
se mueven erráticamente durante la carga de los capacitores. Esa observación es
la razón para exigir estabilidad temporal medida y para estimar tau; los tres
comparadores pueden aportar una señal auxiliar de cruces, pero no reemplazan la
ventana ADC ni justifican un tiempo fijo por sí solos.

### Hipótesis pendiente sobre `AMuxCapacitor`

Elías propuso conservar la posibilidad de conectarlo sólo al medir las plantas
rápidas OPAsum/PGAout/LP. Puede reducir ruido, pero **no está aprobado aún**:
que una etapa sea rápida no garantiza que el capacitor no cargue un nodo de
alta impedancia. Después de instalar 5,1 kOhm se debe comparar A/B en el mismo
punto, con restauración: `with_cap=0` como referencia y `with_cap=1` como
candidato. Se comparan media, pico-pico, pendiente IDAC, settling e histéresis.
Para ch0/ch1 y especialmente para estimar tau en BPo se mantiene siempre
`with_cap=0`. Sólo se habilitará en ch2/ch3/ch4 si no desplaza la media ni cambia
la planta; si únicamente baja ruido, el FIR digital sigue siendo preferible.

## 11. Estado exacto del código al corte

- Firmware programado mide/calibra sin `AMuxCapacitor`.
- `autocalibrar_seguro.py` está en desarrollo y **no debe correrse todavía en
  hardware**: su espera inicial exige que todos los taps ya estén dentro de la
  ventana, por lo que no rescata ch2/ch3 desde el riel; además, el simulador
  quedó con unidades antiguas y falla todos los casos.
- `diagnosticar_idac2.py` fue reorientado a la topología vigente pero necesita
  reintentos robustos de lectura.
- `caracterizar_respuesta_local.py` existe, registra CSV y restaura el código,
  pero exige que los cinco taps sean válidos: no sirve para rescatar una etapa
  que empieza saturada.
- `testbench/core/lab.py` valida la identidad de cada respuesta y reintenta
  comandos; el comentario superior que llama a la lectura “desviación respecto
  de Vref” es antiguo y debe corregirse para no volver a confundir unidades.
- EEPROM carga slots al boot. No se considera que su contenido actual sea una
  calibración válida de la topología/medición nueva. Antes de validar desde cero
  hay que garantizar por comando que el ensayo no depende de ella.
- El árbol está sucio y contiene cambios de Elías, archivos generados por PSoC
  Creator y cambios de esta investigación. No hacer reset/checkout destructivo.

## 12. Estado eléctrico dejado y apagado

Los ensayos de IDAC2 usaron PGAout x1, códigos pequeños 0..14 y restauraron
IDAC2 a cero en `finally`. La última verificación pasiva encontró aproximadamente:

- ch0 949,554 mV banco;
- ch1 986,118 mV banco;
- ch2 890,865 mV banco;
- ch3 888,042 mV banco;
- ch4 1106,834 mV banco.

Hubo respuestas serie faltantes al leer todos los taps de una vez; las lecturas
individuales de ch1/ch2 sí respondieron. No interpretar estas cinco cifras como
simultáneas ni como estado estacionario.

Al cerrar el último ensayo se encontraron dos procesos Python del mismo runner
(wrapper y proceso real). Se detuvieron y, antes de apagar, se abrió COM8 una
vez más y se recibió confirmación explícita de firmware para:

```text
ADC1 True
PGAout_x1 True
IDACs [True, True, True, True]
```

Por lo tanto, el último estado comandado con alimentación fue ADC en ±2,5 V,
PGAout x1 e IDAC0/1/2/3 en código cero. Después Elías cerró y apagó todo. Una
consulta posterior de procesos no encontró ningún `python.exe` activo. Esto no
es una medición de tensión residual: al volver, inspeccionar la resistencia y
energizar siguiendo el runbook.

## 12.1 Primera implementación y prueba de la rutina A

Se agregó `src/interfaces/python/autocalibracion_dos_fases.py`. No usa semillas,
no escribe EEPROM durante las pruebas y separa explícitamente la rutina lenta
upstream de la futura rutina rápida por ganancia.

Prueba reversible sin capacitor:
`lab/calibracion_nueva/dos_fases_probe-upstream_20260909_100135.json` y `.csv`.

- IDAC0→ch0: +76,17 mV físicos/código, claramente observable.
- IDAC1→ch1 con sólo 2 s: +2,37 mV/código aparente, dominado por deriva; no se
  acepta como pendiente estacionaria.

Primera corrida lenta:
`lab/calibracion_nueva/dos_fases_calibrate-upstream_20260909_100306.json` y
`.csv`.

- IDAC0 llegó a error −8,54 mV en código +20.
- Tau observada en BPo/ch1: 24,9 s, ajuste R²=0,99694 y amplitud ≈805 mV. La
  amplitud incluye el asentamiento del movimiento grande previo de IDAC0; tau
  es útil, pero la próxima versión espera primero estabilidad antes del pulso.
- Identificación estacionaria IDAC1→ch1 con ±4 y 2tau por estado: pendiente
  +1,33 mV físicos/código.
- La corrida abortó correctamente al agotar cuatro incrementos diagnósticos:
  IDAC1 0→4→8→12→16 no alcanzó cero. Siempre permaneció en ventana y el
  `finally` restauró IDAC0/IDAC1 a cero.
- La autoridad estimada de IDAC1 es ≈±0,34 V; el offset observado de BPo estuvo
  alrededor de −0,30…−0,35 V. Es calibrable sólo cerca del extremo y debe
  comprobarse margen/repetibilidad.

Después de esa evidencia el código se cambió a la estructura exigida para las
cuatro etapas: salto Newton acotado, rampa eléctrica verificada, PI pequeño y
ventana final cerrada. Para IDAC1 usa una identificación ±32, salto Newton hasta
±255 como máximo y PI lento. El archivo compila como Python y el estimador
matemático tiene prueba sintética PASS.

Primeras repeticiones de la identificación IDAC0→ch0 sin capacitor: 76,17;
77,30; 63,44; 60,97 y 82,62 mV físicos/código según corrida/instante. El rango
61–83 mV/código es aproximadamente ±15 % respecto del centro y ya muestra que
un Jacobiano guardado puede inicializar Newton, pero no sustituir una
reidentificación/PI. Dos Newton+PI posteriores terminaron en código 19 con
−52,6 y −41,6 mV: mejora segura, todavía fuera de ±20 mV porque la ventana
acabó antes del último paso cuantizado. Se amplió a 30 s con 90 % para control.

Corrida completa más informativa antes del cierre:
`lab/calibracion_nueva/dos_fases_calibrate-upstream_20260909_102051.json`
y `.csv`.

- IDAC0→ch0: 62,86 mV físicos/código; Newton+PI terminó en código +20 y error
  final +18,8 mV: **PASS** de la tolerancia ±20 mV.
- Tau de BPo/ch1: 35,6 s.
- IDAC1→ch1: 2,11 mV físicos/código con perturbación bilateral ±32.
- Newton llevó IDAC1 cerca de +150. El PI empezó demasiado pronto y osciló
  alrededor del punto; acabó en +152 con −27,5 mV. Eso cumple el criterio BP
  revisado de ±50 mV, aunque la versión de ese momento todavía exigía ±20 mV y
  lo registró como aborto. Se modificó después para esperar 1,25*tau antes de
  corregir y limitar el PI de BP a un código por actualización.

Última corrida, interrumpida:
`lab/calibracion_nueva/dos_fases_calibrate-upstream_20260909_103452.json`
y `.csv`.

- IDAC0→ch0: 74,63 mV físicos/código; Newton+PI terminó en código +20 y error
  final +11,2 mV: **PASS**.
- Tau de BPo/ch1: 42,3 s. Frente a 35,6 s, la diferencia es ≈18,8 %, evidencia
  concreta de que no conviene hardcodear tau todavía.
- IDAC1→ch1 volvió a dar 2,11 mV físicos/código y Newton calculó 0→+151.
- La corrida se interrumpió inmediatamente después de iniciar ese salto; el
  JSON terminó con `OSError: [Errno 22] Invalid argument`. No contiene cierre
  de IDAC1 y **no es PASS**. La neutralización explícita posterior descrita en
  §12 es la evidencia del estado seguro, no el `finally` de este archivo.

Conclusión cuantitativa honesta al corte: la primera etapa ya cerró dos veces
dentro de ±20 mV sin semillas; BP tiene autoridad y una pendiente repetida de
≈2,11 mV/código, pero la versión PI lenta modificada aún no tiene una corrida
completa. IDAC2/IDAC3 y x24 no se validaron con la medición sin carga.

## 12.2 Inventario de código que recibe el próximo chat

- `src/interfaces/python/autocalibracion_dos_fases.py`: implementación vigente
  de laboratorio. Hoy sólo ejecuta la porción IDAC0/IDAC1 de la rutina A;
  `probe-upstream` y `calibrate-upstream` son los únicos modos. No guarda
  EEPROM ni implementa todavía la rutina B de IDAC2/IDAC3 por ganancia.
- `src/interfaces/python/testbench/core/lab.py`: transporte/medición robustos,
  con validación de identidad y reintentos. El comentario de unidades en la
  cabecera sigue pendiente de limpieza.
- `src/interfaces/python/diagnosticar_idac2.py`: adaptado a IDAC2→OPAsum, pero
  todavía necesita robustecer las lecturas antes de una adquisición larga.
- `src/interfaces/python/autocalibrar_seguro.py`: prototipo histórico; no usar
  en hardware hasta reparar su simulación/unidades y hacer que sus fallos
  produzcan exit code no cero.
- `AcondicionamientoAnalogico.cydsn/calibration.c` y
  `AcondicionamientoAnalogicoTest/.../psoc_selftest.h`: selección DC corregida
  a `with_cap=0`; esto es lo actualmente programado.
- El árbol está sucio, incluidos cambios manuales de TopDesign y archivos
  generados. No hacer `reset`, `checkout` ni regeneración destructiva.

No falta una implementación escondida: el algoritmo autónomo final en C, la
rutina B, el guardado EEPROM nuevo, la comparación secuencial/vectorial limpia
y la validación repetida x24 son trabajo **pendiente**, no logros.

## 13. Datos que conviene preguntarle a Elías si no aparecen en la placa

No bloquean el trabajo offline, pero deben confirmarse antes del ensayo final:

- designador exacto de la resistencia física de IDAC2 que se cambiará a 5,1 kOhm;
- tolerancia y valor medido de la nueva resistencia;
- si el power-cycle para repetibilidad puede hacerse automáticamente o requiere
  intervención;
- criterio numérico final aceptable para SUMo y LPo (la meta usada hasta ahora
  fue ±20 mV físicos para la salida, con guardas más amplias aguas arriba);
- si el contenido EEPROM actual puede invalidarse/borrarse antes de la prueba
  desde cero, o sólo ignorarse durante la identificación.

## 14. Instrucción exacta para retomar

En un chat nuevo basta indicar:

> Lee `C:\Github\Tesis\lab\HANDOFF_AUTOCALIBRACION_AUTORITATIVO_2026-09-09.md`
> como estado autoritativo y continúa desde el runbook de IDAC2 a 5,1 kOhm.
> No uses como PASS las mediciones anteriores al arreglo `with_cap=0` y no
> modifiques TopDesign.

Primera pregunta del nuevo chat: confirmar si 5,1 kOhm ya fue instalado y qué
valor se midió sin alimentación. Si no fue instalado, no energizar para correr
la rutina nueva. Si fue instalado, actualizar sólo los metadatos nominales y
seguir `RUNBOOK_POST_CAMBIO_IDAC2_5K1.md` desde “Antes de energizar”.
# Actualización 2026-09-09 22:59 — dos fases funcionales y EEPROM

La implementación vigente está en
`src/interfaces/python/autocalibracion_dos_fases.py`. El resultado detallado y
las limitaciones honestas están en
`lab/RESULTADOS_AUTOCALIBRACION_DOS_FASES_2026-09-09.md`.

- Fase 1: `[IDAC0,IDAC1]=[19,140]`, una sola vez, ~62 s.
- Fase 2: cambios x1→x50 en 4,8..9,0 s por ganancia.
- Cinco campañas completas: 45/45 cambios PASS funcional, recorrido entero
  113,5..119,8 s.
- EEPROM guardada con el punto x1 `[19,140,254,83]` después de reverificación.
- LPo es legible en todas las ganancias. ch2/ch3 sólo permanecen válidos en
  x1/x2; desde x4 saturan con la autoridad actual. No ocultar esta limitación.
- Falta comprobar restauración tras power-cycle físico.
