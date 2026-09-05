# HANDOFF del goal — fin de semana del 2026-09-05

**Fuente de verdad del estado de la tarea.** Si te reanudó el watchdog, empezá
por acá y después mirá `docs/MEDICIONES_2026-09-05.md` (lo medido hoy, con
método) y `docs/MEDICIONES_2026-09-04.md` (lo de ayer).

Mantener este archivo al día es parte del trabajo, no un extra.

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
- [ ] 2.1 τ automedido por el propio nodo. Estimador elegido: dos puntos a t y
      2t, que da τ sin necesidad de conocer el valor final —
      `e^(-t/τ) = r - 1` con `r = (y(2t)-y(0))/(y(t)-y(0))`.
- [x] 2.2 Espera de planta en **2 τ**, con τ en ms como `uint16` y ajustable en
      ejecución (`psoc_cal_set_tau_ms`). Commit `09f6462`.
- [x] 2.3 ADDER: **la tabla queda descartada por medición**. Falta ajustar el
      clamp: el rango útil real es mucho menor que el ±128 de hoy.
- [x] 2.4 Optimizador conjunto en C, regularizado y verificado contra el modelo
      dentro del 1,2 %. Commit `10480e8`, archivo `calibration_conjunta.h`.
      **Falta integrarlo a la máquina de estados de la calibración.**
- [ ] 2.5 Ki 1/16.
- [x] 2.6 Comandos `cal`, `snapshot`, `taps`, `quien` en el ESP. Commit
      `e3cb8a0`. Sacado el `upload_port` fijo del `platformio.ini`.
- [ ] 2.7 Separación campo / laboratorio por archivos.
- [ ] 2.8 **Clamp del IDAC de la etapa 0 escalado por 1/ganancia.** Hoy es fijo
      en ±255 y a ×50 el tap ya está en el riel pasando los ~±66 códigos.

### Fase 3 — validación en placa
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
