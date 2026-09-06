# HANDOFF del goal — fin de semana del 2026-09-05

**Fuente de verdad del estado de la tarea.** Si te reanudó el watchdog, empezá
por acá y después mirá `docs/MEDICIONES_2026-09-05.md` (lo medido hoy, con
método) y `docs/MEDICIONES_2026-09-04.md` (lo de ayer).

Mantener este archivo al día es parte del trabajo, no un extra.

---

## ESTADO AL 2026-09-05, 23:00 — el firmware unificado y el lazo arreglado

Lo de abajo (desde "GOAL NO CONSEGUIDO") es el historial del dia y quedo
resuelto; se conserva porque documenta como se llego aca. Esto es lo vigente.

### Lo que se hizo esta noche

**1. Un solo firmware.** El proyecto de autotest era una copia entera del de
campo: 28 fuentes duplicadas, 21 identicas mantenidas a mano y 7 divergidas.
Ahora cada fuente compartida existe UNA vez y el test la incluye. `program_psoc.ps1`
verifica la sincronia y SE NIEGA A GRABAR si alguien vuelve a copiar un archivo.

**2. Tres defectos del firmware DE CAMPO, encontrados al unificar y al medir.**
Los tres son la misma confusion: se uso el tiempo del ADC (30 ms) donde hacia
falta el de la cadena (tau = 29,5 s).

  - la espera de planta vivia en una rama `#else` que no compila, o sea que el
    nodo nunca esperaba a que la cadena se asentara;
  - las esperas estan declaradas en muestras del ADC pero los contadores cuentan
    iteraciones del lazo, que con el lector directo son 78 veces mas largas;
  - despues de mover la referencia el lazo remedia a los 30 ms, antes de que la
    planta conteste, concluye que no paso nada y vuelve a mover: hasta el riel.

**3. Un defecto mio, de la mejora de dos actuadores.** La correccion por la no
linealidad del LP se activaba con `adc_channel == 3`. Al hacer que el ADDER
mire el canal 3, el ADDER quedo usando la curva del LP: ganancia positiva en un
lazo de ganancia negativa. Realimentacion positiva.

**4. Otro defecto mio.** Recortar la tabla de etapas a dos dejo al instrumento
sin poder escribir los IDAC del PGA y del BP, en silencio. Las cuatro etapas
volvieron a la tabla; el campo `en_secuencia` dice cuales se calibran.

### 5. EL HALLAZGO PRINCIPAL: el firmware se quedaba 63 codigos corto

**Con el ADDER (IDAC 2) en -191 y los otros tres IDAC en CERO, la cadena entera
queda centrada a PGA x50:**

    ch1 = 1001,9    ch2 = 1001,1    ch3 = 1001,8   de banco
    o sea ch3 = 2,419 V, que es Vref (2,415) con 4 mV de error

Un solo actuador, sin tocar nada mas. El firmware no podia llegar ahi porque su
clamp para el ADDER era +-128 codigos.

**La curva completa**, medida en lazo abierto el 2026-09-06 (mV de banco en ch3):

    IDAC2   0 .. -128    748,0    plano, zona ciega  <- aca cortaba el firmware
    IDAC2      -144      765,6    primer movimiento
    IDAC2      -160      874,1
    IDAC2      -176      948,3    ya observable
    IDAC2      -191     1001,8    Vref

El LP esta saturado y NO responde nada hasta que la contribucion del ADDER cruza
un umbral cerca de -135 codigos. El firmware se quedaba en el ultimo punto plano,
un paso antes del acantilado.

**Me equivoque dos veces antes de llegar a esto**, y el error fue de metodo:
barri el ADDER hasta -128 y lei el resultado como una propiedad del circuito,
cuando -128 era el limite de mi propio instrumento. Lo destapo un dato viejo
-el JSON de la busqueda de PGAout guardaba que el procedimiento que SI centra la
cadena usa -191-. Las secciones 21 y 24 de MEDICIONES quedan corregidas por la
25; se dejan escritas porque el recorrido importa.

**Arreglado en el firmware:**
- el clamp deja de ser simetrico: `dac_max_change` y `dac_max_change_neg`. Ya
  estaba anotado como pendiente en la propia tabla, con la nota de que se perdia
  el tramo -178..-128 "que si es util". Era justo el que hacia falta;
- al ADDER se le abre todo el recorrido negativo, porque la PC usa -191;
- **rescate en lazo abierto**: el PI ahora pregunta si la lectura significa algo
  antes de realimentar sobre ella. Fuera de la ventana observable no realimenta:
  empuja a ciegas en la direccion conocida, espera 1 tau y vuelve a mirar;
- presupuesto del ADDER dimensionado: 7 pasos de rescate + 7 de lazo.

**Compilado. FALTA GRABARLO Y CORRER `cal`** — es la prueba que cierra el fin de
semana, y el banco esta ocupado terminando el barrido.

### Estado del lazo, medido

| corrida | resultado |
|---|---|
| antes de todo | contestaba ok=0 a los 59,7 s sin esperar nunca |
| con las esperas arregladas | 149 s, pero se iba al riel (realimentacion positiva) |
| con la curva del LP arreglada | 433 s, saca al LP del riel y le recorre 2,7 V |
| con 12 pasos para el ADDER | 648 s; se queda contra su propio clamp |
| con el clamp asimetrico + rescate | **sin probar todavia** |

### Lo que hay que releer con desconfianza

**Las mediciones del dia se tomaron con el instrumento que tenia el lector de
ADC defectuoso** (el que puede devolver un cero inventado si la ISR le come el
flag). No las invalida —las series se toman con el ADC libre corriendo, que es
el uso correcto del polling— pero explica lecturas sueltas raras sobre ch3.

**La seccion 15 de MEDICIONES (10 de 12 combinaciones arrancan railadas) hay que
rehacerla**, y es la que justifica la autocalibracion en la tesis. Razon: la
misma configuracion medida dos veces dio resultados opuestos, y la diferencia
era DE DONDE VENIA la cadena. Volver de la saturacion tarda mucho mas que 2 tau
(71 s de constante mas absorcion dielectrica del electrolitico de 680 uF). Si
las 12 se midieron seguidas, cada una heredaba el estado de la anterior.
Esta escrito el reemplazo: `sin_calibrar.py`, con deteccion de asentamiento
(`src/interfaces/python/asentamiento.py`), orden alternado y tres controles.

### Lo que sigue, en orden

1. **Verificar que el lazo ya converja** (corriendo al cierre de esta nota).
2. **Rehacer la seccion 15** con `sin_calibrar.py`. Es lo mas importante que
   queda: sin eso el argumento de la tesis se apoya en una medida no reproducible.
3. **EXP4c, la deriva.** OJO: la ventana de la madrugada del 2026-09-06 SE
   PERDIO -la sesion quedo inactiva desde las 23:27 y el registro no llego a
   arrancar-. No es fatal: la rampa termica de la manana (de ~11 a ~19 C) sirve
   igual que la de la noche, y el experimento es el mismo. `deriva_noche.py`.
4. EXP4b (rango dinamico perdido) y EXP4d (que calibrar no empeora el ruido).
5. Lunes: cambiar SOLO la resistencia del LP a 1,8 k y repetir la bateria
   (`lab/PLAN_RESISTENCIAS_LUNES.md`).

### Numeros vigentes

| | |
|---|---|
| Escala del banco | 1 mV de banco = 19,9157 mV reales; banco 1001,5 = Vref = 2,415 V |
| Rieles (los cuatro taps) | banco 880,4 y 1122,7 |
| tau de la planta | 29,5 s (tres caminos independientes) |
| Maximo PGAout estable con PGA x50 | **x1** |
| Duracion de una calibracion honesta | ~412 s (2 etapas x (2 tau + hasta 5 pasos de 1 tau)) |
| Ganancias del lazo sobre ch3 | ADDER -2039, LP +280 |

---

## GOAL NO CONSEGUIDO — HAY QUE VERIFICAR EL ORIGEN DE COORDENADAS PRIMERO

**Estado al 2026-09-05 por la tarde: en pausa por una duda de fondo que Elias
detecto y que invalida el criterio con el que se midio todo el dia.**

**Que pasa.** Todo el trabajo del dia informa el error del LP como desvio
respecto de **1000 mV**. Ese numero NO es el objetivo del firmware: es
simplemente lo que el banco lee cuando la cadena esta en reposo. El objetivo
real de GEO es **CERO**:

    CAL_TARGET_GEO_PGA_MV = CAL_TARGET_GEO_BP_MV =
    CAL_TARGET_GEO_SUM_MV = CAL_TARGET_GEO_LP_MV = 0

Los 1000/1024/3500 mV son de **HAMMER**, no de GEO. Elias lo marco y tiene razon.

**Por que no se resuelve leyendo el codigo.** Se reviso: la calibracion y el
comando `dc` del banco usan el MISMO AMux (`psoc_amux_select_exclusive`), el
MISMO ADC (`ADC_GetResult32` + `psoc_adc_counts_right_aligned`) y la MISMA
conversion (`counts x rango / 131072`, sin offset). Y `cal_pi_compare_counts`
para GEO devuelve el valor tal cual. O sea que las cuentas son la misma
magnitud, y sin embargo el objetivo es 0 y el banco lee ~52.429 cuentas (1 V).

**Las dos posibilidades:**

1. El banco tiene un offset o una escala equivocada, y "1000 mV en el banco" ES
   el cero del firmware. Entonces todos los numeros del dia valen tal cual.
2. Hay de verdad ~1 V de desbalance en los taps. **Esto NO es absurdo**, como
   penso primero esta sesion: Elias lo corrigio. Con `polarity_reg` el recorrido
   del IDAC es +-255 x 1875 uV = **+-478 mV en la referencia**, y por la ganancia
   referencia->tap del ADDER (3823/1875 = 2,04) eso da **+-975 mV en ch3**. O sea
   que hay autoridad para mover casi un volt.

**LA PRUEBA QUE LO DECIDE, y hay que hacerla ANTES de seguir midiendo:**

- comparar `snapshot` (0xB8, el reporte por etapa del propio PSoC) contra `dc`
  del banco sobre el mismo canal. Son dos caminos de codigo distintos: si
  coinciden, el banco esta bien y el volt es real;
- correr `cal` del firmware y leer los taps despues. Si el firmware converge y
  el banco lee ~0 mV, el objetivo es 0 de verdad y el reposo de 1000 mV era
  simplemente "sin calibrar".

**Que queda en pie pase lo que pase**, porque no depende del origen: los rieles
(750 y 1122 en unidades del banco), la excursion de 372 mV, la asimetria del
recorrido, y **todas las pendientes en uV/codigo** —que son diferencias y por lo
tanto inmunes a un offset—. Lo que queda en duda es **donde hay que dejar cada
tap**, o sea el criterio de aceptacion.

---

## El objetivo, en una línea

Dejar la autocalibración de la cadena analógica **medida, ajustada y fiable**
para cualquier par de ganancias que Elías vaya a usar la semana que viene, con
el mejor tiempo posible dentro del techo que él fijó: **≤ 2 τ de espera y
≤ 20 mV de error**. Mejor que eso es bienvenido; peor no se acepta.

---

## Estado del banco (verificar antes de creer)

| qué | dónde | ojo |
|---|---|---|
| ESP esclavo | **COM8** | Es el único ESP conectado. El maestro está desenchufado a pedido de Elías. **Verificar siempre**: el 04-09 se perdió una tarde midiendo el maestro. |
| Firmware del ESP | `slaveTest` | |
| Firmware del PSoC | autotest (`AcondicionamientoAnalogicoTest`) | |
| Grabar el PSoC | `.\program_psoc.ps1 [-SelfTest]` | **Funciona**, verificado 2026-09-05. Nunca `-AllRows`. Redirigir PPCLI a archivo (~1100 líneas). |
| Geófono | conectado, en el piso | Ver abajo. |
| Python | `C:\Users\elias\AppData\Local\Python\pythoncore-3.14-64\python.exe` | El de PlatformIO no tiene PyQt6. |

### El geófono: qué es exactamente lo que se está midiendo

- Adentro de una habitación de la casa de Elías, **a 4 m de la pared** que da a
  la calle, y de esa pared a la calle hay **~5 m más**. La fuente de interés son
  los autos golpeando una **lomada** a ~9 m del sensor, a través de una pared.
- **No está clavado**: está acostado en el piso, apoyado con una caja para que la
  punta toque mejor. Eso lo pone **fuera de especificación**: con el eje
  inclinado la masa se corre en el entrehierro, baja la sensibilidad, cambia el
  amortiguamiento, y el eje sensible pasa a ser horizontal.
- **Consecuencia obligatoria:** sirve para **comparaciones relativas** (mismo
  acople en todas las mediciones) y **no** para números absolutos de sensibilidad
  ni para conclusiones sobre la banda. Declararlo en todo lo que se escriba.
- Elías no garantiza que no se mueva, pero la habitación no se usa. **Si una
  tanda da incoherente con la anterior, sospechar del acople antes que del
  circuito.**

### DATO DE CAMPO DE ELIAS — vale mas que cualquier medicion de banco

Dicho el 2026-09-05: **"x50 funciona en el primer PGA en campo real cuando el
geofono esta aterrado"**. Ya lo probo en campo, con el geofono clavado en el
piso.

**Salvedad que el mismo aclaro:** la placa con la que lo probo **no tenia el
segundo PGA (PGAout)**, asi que sobre PGAout no puede afirmar nada.

**Por que esto NO contradice lo medido en banco, y conviene tenerlo claro para
no "arreglar" algo que no esta roto.** En banco, a PGA x50 con PGAout x1:

    ch0 = 958,4 mV   ch1 = 1010,1 mV   ch2 = 1121,8 (riel)   ch3 = 746,6 (riel)

Los dos taps del primer PGA estan **perfectos** y son corregibles con ~16 codigos
(EXP1). Los que se van al riel son ch2 y ch3, o sea el ADDER y el LP, que estan
**aguas abajo** del primer PGA y que la placa de campo de Elias no tenia en esta
forma. Las dos observaciones son compatibles: el problema no esta en el PGA de
entrada.

**Consecuencia para el trabajo:** el x50 de entrada se da por bueno y no hay que
gastar tiempo justificandolo. El esfuerzo va a que el ADDER y el LP vuelvan al
rango, que es donde esta el problema real.

### Ruido de la casa

Elías y su madre circulan **todo el fin de semana salvo la madrugada**. Unos
pasos a 4 m tapan por completo a un auto a 9 m del otro lado de una pared.
Entonces: **las tandas largas de señal van de madrugada**, y en todas hay que
descartar por energía las ventanas contaminadas.

---

## Decisiones ya tomadas por Elías (no volver a preguntar)

1. **τ configurable** como `#define` `uint16`, pero **usar 2 τ** por ahora.
2. **El acople DC entre etapas es normal** y así se modeló en el paper de
   Urucom. No es un defecto a eliminar. Precomputar un valor y después corregir
   de a poco. Probar la **optimización conjunta**: no minimizar cada etapa por
   separado sino el conjunto, **pesando más las etapas con más ganancia
   acumulada** porque son las que más probablemente saturen. El objetivo real es
   **que no sature**, con el LP chico; que todas den cero es ideal pero no es el
   requisito.
3. **ADDER:** intentar tabla para usar el rango completo. Si la medición dice que
   es saturación de verdad y no no-linealidad, se descarta y se acota. Elías
   aprobó decidirlo por medición.
4. **Ki:** probar **1/16** a ver si sube más rápido y anula el remanente.
5. **Sin maestro** hasta que el esclavo esté fino.
6. **Ganancias:** priorizar los **pares altos** (dividir en bajas y altas y
   atacar las altas), porque son los que enfrentan la atenuación de las
   distancias de campo. Elías no puede afirmarlo con autoridad; hay que medirlo.
7. **Temperatura: NO corregir por temperatura.** En su lugar **medir τ** en el
   nodo y ajustar con lo medido. La temperatura es la explicación, no la entrada.
8. **IDACs:** este fin de semana se usan como están (15 kΩ 1 % en las cuatro).
   Si la medición muestra que el rango es malo, **dejar una recomendación en el
   informe** con cuánto se gana y cuánto se pierde, y decide Elías.
9. **La instrumentación de laboratorio no puede quedar en el firmware de campo.**
   Por estructura de archivos, no por disciplina.
10. **Entregables vistosos:** gráficas, tablas y números para mostrar.
    Documentar mientras se trabaja.

---

## LO QUE ELIAS PIDIO CONCRETAMENTE PARA CAMPO (2026-09-05, ultima palabra)

1. **Conseguir la ganancia de PGAout maxima estable**, con el PGA de entrada en
   x50 (que el ya valido en campo). `buscar_max_pgaout.py --pga 8`.
2. **Despues probar si conviene repartir esa ganancia entre los dos** en vez de
   concentrar los primeros x50 en el PGA de entrada. Su hipotesis: si PGAout
   aguanta hasta x24 con el PGA en x50 -x1200 en total- entonces x32 con x32,
   que son x1024, deberia aguantar tambien.

**POR QUE ESA HIPOTESIS PUEDE SER FALSA, y hay que medirla.** El offset a la
salida no depende solo de la ganancia total sino de DONDE ENTRA cada offset:

        offset_salida  ~  A*Gp*Go  +  B*Go  +  C

con A el offset referido a la entrada, B uno que entre entre las dos etapas, y C
uno de la ultima. Entonces (50,24) da 1200A + 24B + C y (32,32) da 1024A + 32B + C.
**Si domina B, el reparto parejo es PEOR pese a tener menos ganancia total.**
Si domina A, la intuicion de Elias se cumple. Cual domina es medible y no se
puede deducir.

Se corre con `buscar_max_pgaout.py --pares 8:5,6:6,5:7,7:5,4:8` una vez que se
sepa el maximo, eligiendo pares de ganancia total parecida y reparto distinto.
Eso separa A de B: si todos los de la misma ganancia total dan lo mismo, manda A;
si los de PGAout alto son peores, manda B.

**Red de seguridad:** PGAout x1 reproduce la placa que Elias ya probo en campo y
que funciona. El peor resultado posible de esta busqueda sigue siendo un nodo
utilizable.

## APARTADO DE TESIS: justificar que la autocalibracion vale su complejidad

Pedido de Elias del 2026-09-05: *"probá cada combinación de ganancia con todos
los IDACs a 0, o sea sólo con el voltaje de base, para medir qué tan útil es el
sistema de autocalibración [...] principalmente buscamos medir su utilidad y
justificar su complejidad. Si no se cumple esto no vale la pena y necesito que
lo justifiques en mi tesis."*

**El argumento mas fuerte ya esta medido**, y es mejor de lo que uno esperaria:

| PGA x PGAout | sin calibrar (IDACs en 0) | calibrado |
|---|---|---|
| x50 x1 | ch2 = 1121,8 mV y ch3 = 746,6 mV: **los dos CONTRA EL RIEL** | LP a **-0,21 mV** |
| x1 x1 | ch3 = 984,6 mV, 15,4 mV fuera | ~2 mV |

O sea que **sin autocalibracion la configuracion de x50 no existe**: la cadena
esta railada y no captura nada. La autocalibracion no es un refinamiento que
mejora un numero, es **lo que hace que esa configuracion sea posible**. Y x50 es
justamente la que Elias valido en campo por dar mejor senal.

De las 12 combinaciones medidas en reposo, **10 arrancan contra el riel**.

### Mediciones que faltan para cerrar el apartado

- **EXP4a — reposo en toda la grilla.** Con los cuatro IDAC en 0 y espera de
  planta correcta, clasificar cada combinacion en: railada (nodo inutil), en
  rango pero fuera de objetivo, o dentro de especificacion. La metrica que
  importa es **cuantas combinaciones son utilizables sin calibrar contra cuantas
  con calibrar**. Parte ya esta (`campana_*.json`, 12 combinaciones con 60 s de
  espera).
- **EXP4b — excursion util perdida.** El offset se come margen de excursion, y
  eso son bits del ADC que se pierden. Cuantificar la amplitud de senal que
  entra antes de recortar, con y sin calibrar. Es el argumento en terminos de
  rango dinamico, que es el que un tribunal entiende sin discutir.
- **EXP4c — deriva del punto calibrado.** Es el que justifica que la calibracion
  sea **automatica y no un ajuste de fabrica**: si el punto deriva con el tiempo
  o la temperatura, un trim fijo no sirve. Dejar el nodo calibrado y medir los
  cuatro taps cada pocos minutos durante horas. **Va de madrugada**, que es
  cuando la casa esta quieta, y de paso la temperatura baja de ~19 a ~11 C esa
  noche, o sea que la excursion termica viene de regalo.
- **EXP4d — la calibracion no empeora el ruido.** Comprobar que el piso de ruido
  con los IDAC calibrados es el mismo que con los IDAC en 0. Es barato y cierra
  la objecion obvia de "si, corrige el offset, pero a que costo".

## IDEAS DE ELIAS ANOTADAS PARA EL FINAL (baja prioridad, dichas por el)

- **Cambiar la resolucion / configuracion del ADC entre mediciones.** El
  componente expone cuatro rangos (+-2,5 / +-0,512 / +-1,024 / +-0,625 V) a la
  misma Fs. La idea es usar el ancho para lo grueso -barridos, busqueda de
  saturacion, donde el tap se mueve cientos de mV- y uno angosto para la
  verificacion final del residuo, donde da hasta 5x mas resolucion sobre el
  mismo dato. Elias: *"valora la posibilidad de cambiar la resolucion del ADC
  entre mediciones si ayuda a mejorar [...] esto ponelo para las ultimas
  pruebas, es lo menos importante pero anotalo"*.

  **Trampa conocida:** cambiar de configuracion exige que el DelSig se
  reasiente, y no esperar eso ya produjo lecturas basura el 2026-09-05 -tres
  rangos pedidos uno tras otro dieron cuentas fisicamente imposibles-. Hay que
  medir cuanto tarda ese reasentamiento antes de usarlo en serio.

  **Requisito previo:** que el tap este dentro del rango angosto. El autotest ya
  avisa (D5) cuando no lo esta, y hoy salta justamente por eso.

## Herramientas que hay que tener presentes

- **El ADC tiene cuatro rangos**, los cuatro a 2604 Hz y 18 bits
  (`PSOC_CMD_ADC_CONFIG`, 0xBA): `1=±2,5 V`, `2=±0,512 V`, `3=±1,024 V`,
  `4=±0,625 V`. **Usarlos según el tipo de medida**: el rango ancho para
  barridos y búsqueda de saturación, y los angostos para offsets residuales,
  ajuste de τ y verificación del error final, donde dan ~5× más resolución. El
  autotest ya avisa (`D5`) cuando el tap quedaría fuera del rango angosto.
- `src/interfaces/python/medir_planta.py` — `escalon`, `curva`, `campana`,
  `matriz`. `--dwell` es la espera de PLANTA por punto, en segundos.
- `src/interfaces/python/analizar_planta.py` — tablas y figuras.
- `src/interfaces/python/registrar_calibracion.py` — evolución temporal de una
  calibración.
- `python -m testbench` — banco manual (`taps`, `dc`, `ac`, `idac`, `gain`,
  `mon`, `sweep`) y automático (`run`).
- Temperatura ambiente sin credenciales:
  `https://api.open-meteo.com/v1/forecast?latitude=-25.3387&longitude=-57.6161&current=temperature_2m`

---

## Plan, y en qué punto está

### Fase 0 — infraestructura
- [x] Watchdog de reanudación (`lab/reanudar_goal.ps1` + tarea programada
      `ClaudeReanudarGoalTesis`, cada 20 min). Freno: crear
      `lab/PARAR_REANUDACION`.
- [x] Verificado que `program_psoc.ps1` graba bien → se puede iterar firmware sin
      Elías.

### Fase 1 — mediciones que deciden el diseño (con el firmware actual)
- [x] **1.1 ADDER: es SATURACIÓN, no no linealidad.** En los extremos ch2 y ch3
      están contra el riel a la vez. **La tabla se descarta.** Y de paso salió
      que el acople ADDER→LP estaba subestimado 1,8× porque se midió con un
      escalón que saturaba el LP: es 3823 µV/cód, no 2121. Ver
      `docs/MEDICIONES_2026-09-05.md` §6.
- [x] **EXP1: la autoridad del IDAC del PGA SÍ escala con la ganancia.** Inyecta
      antes de amplificar, el firmware tenía razón, y ×50 es viable. Ver §4.
      De ahí salieron además los rieles medidos de los taps.
- [ ] 1.2 τ a la temperatura de hoy, con el ADC en rango angosto.
- [~] 1.3 Campaña de las 81 combinaciones en reposo — **corriendo**. OJO: sólo
      dice cuáles arrancan en riel, no cuáles se recuperan. Para eso está
      `calibrar_pc.py`.
- [ ] 1.4 Piso de ruido y saturación por combinación, con el geófono. Las tandas
      con señal van **de madrugada**.
- [ ] 1.5 **Re-medir la matriz de acople con escalones CHICOS (±10 códigos).**
      La del 2026-09-04 usó +120 y al menos una fila salió contaminada por
      saturación. Hay que revisar si las otras también.

### Fase 2 — firmware
- [~] 2.1 τ automedido. **La aritmética ya está y verificada**
      (`calibration_tau.h`, commit `560acf2`): −0,3 % a −0,9 % de error para τ
      entre 16 y 60 s, y rechaza fuera de ahí en vez de inventar. El par es
      etapa 1 → ch2 con t₁ = 45 s, elegido porque su transitorio es más grande
      que su régimen. **Falta** secuenciar las tres muestras: se puede hacer
      desde el ESP o la PC con `idac` + `dc` + esperas, no hace falta máquina de
      estados en el PSoC.
- [x] 2.9 **Ajuste en caliente sin regrabar** (`PSOC_CMD_CAL_PARAM` 0xB2 +
      `calparam` en el ESP, commits `560acf2` y `f578e3a`). τ en unidades de
      250 ms porque el frame lleva dos bytes. Con esto se barre el espacio de
      parámetros sin un solo regrabado.
- [x] 2.2 Espera de planta en **2 τ**, con τ en ms como `uint16` y ajustable en
      ejecución (`psoc_cal_set_tau_ms`). Commit `09f6462`.
- [x] 2.3 ADDER: **la tabla queda descartada por medición**. Falta ajustar el
      clamp: el rango útil real es mucho menor que el ±128 de hoy.
- [x] 2.4 Optimizador conjunto en C, regularizado y verificado contra el modelo
      dentro del 1,2 %. Commit `10480e8`, archivo `calibration_conjunta.h`.
      **Falta integrarlo a la máquina de estados de la calibración.**
- [ ] 2.5 Ki 1/16. **Ojo:** puede quedar sin objeto. El lazo PI con ganancias
      fijas es lo que la medición del 2026-09-05 puso en duda; si la calibración
      pasa a medir la pendiente en el punto, el Ki de un PI con ganancia fija
      deja de ser el parámetro relevante.
- [x] 2.6 Comandos `cal`, `snapshot`, `taps`, `quien` en el ESP. Commit
      `e3cb8a0`. Sacado el `upload_port` fijo del `platformio.ini`.
- [ ] 2.7 Separación campo / laboratorio por archivos.
- [ ] 2.8 **Clamp del IDAC de la etapa 0 escalado por 1/ganancia.** Hoy es fijo
      en ±255 y a ×50 el tap ya está en el riel pasando los ~±66 códigos.

### Fase 3 — validación en placa
- [x] **PGA ×50 CALIBRA.** Medido el 2026-09-05: con el ADDER en el código −176
      el tap del LP queda en 939,4 mV, centrado, y el ADDER en 1010,4 mV.
      Confirma el dato de campo de Elías y valida el emparejamiento LP↔ADDER.
- [~] 3.0 **Máximo PGAout estable con PGA ×50** — corriendo,
      `buscar_max_pgaout.py`. Es el objetivo principal.
- [ ] 3.1 Calibrar, esperar diez minutos, mirar `GEO_LP`. Criterio: ≤ 20 mV.
- [ ] 3.2 Barrido de combinaciones con calibración real.
- [ ] 3.3 Registros largos de madrugada con la lomada.

### Fase 4 — informe
- [ ] Gráficas y tablas.
- [ ] Recomendación sobre las resistencias de los IDAC, con números.

---

## Hallazgos de hoy que cambian decisiones

1. **`program_psoc.ps1` funciona.** Lo que mataba el chip era `-AllRows`. Ver
   `docs/MEDICIONES_2026-09-05.md` §1.
2. **El PGA de entrada no se puede autocorregir por encima de ~×16.** Su offset
   referido a la entrada es ~0,9 mV y su autoridad es ±15,6 mV; a ×50 necesita
   49,5 mV. **No invalida ×50**: obliga a delegar la corrección aguas abajo, que
   es justamente la optimización conjunta del punto 2 de Elías. Ver §4.
3. **El indicador D6b del autotest no detecta el geófono** porque lo mide a ×1,
   donde manda el piso del ADC. Hay que medirlo a ganancia alta. Ver §3.
4. **El rango de temperatura de la semana es 8,1–31,6 °C**, lo que confirma que
   una espera fija de banco no sirve para campo. Ver §2.


---

## Identidad de las placas (para no volver a confundirlas)

| placa | MAC | cómo se confirma |
|---|---|---|
| ESP esclavo (el que tiene el PSoC) | `C8:2E:18:67:68:6C` | comando `quien` → `psoc=1` |

El maestro está desenchufado. Cuando se conecte, correrle `quien`: si contesta
`psoc=0`, **no** es el esclavo por más que la consola funcione.

## Pendientes de higiene del banco

- El maestro quedó con `slaveTest` del error del 2026-09-04. Hay que devolverle
  el suyo cuando se lo conecte.
- El PSoC tiene el firmware de autotest. Para campo: `.\program_psoc.ps1` sin
  `-SelfTest`.
- Dos bugs de instrumentación detectados y uno ya corregido:
  - `measure_ac` perdía medidas en silencio con `idle=1,0 s` (los canales 2 y 3
    volvían `None`). **Corregido**, ahora 6 s.
  - `FALLO set_idac` en ~2 de 22 puntos de un barrido, y un caso donde un tap
    informó `0,000 mV` y se guardó como válido. **Sin corregir.** Un cero
    silencioso es la peor forma de fallar porque un ajuste posterior lo toma
    como dato bueno.
