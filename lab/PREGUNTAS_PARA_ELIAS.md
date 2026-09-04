# Preguntas acumuladas — 2026-09-04

Van numeradas y con contexto para que las puedas contestar de corrido.
No hace falta que contestes las que digan "no bloquea": son para mejorar, no
para destrabar.

---

## 1. El buffer del DelSig: ¿bypass o no?  · **puede bloquear la interpretación**

Me dijiste *"el delsig sí está buffereado internamente"*, pero la captura que me
mandaste muestra **`Buffer mode: Bypass Buffer`**, que es justamente el modo sin
buffer. Si está bypasseado, la entrada del ADC es la red de capacidad conmutada
directamente sobre el nodo del `AMux_ADC`, y entonces:

- la impedancia de fuente de cada tap entra en el asentamiento de cada medición
  (y los taps no tienen todos la misma impedancia);
- el kickback de muestreo cae sobre el nodo compartido.

Cambia cuánto tengo que esperar por punto y cómo interpreto las diferencias
entre taps. ¿Está en bypass a propósito?

## 2. Rango de temperatura en campo  · no bloquea

C1 es un electrolítico de 680 µF y el τ de toda la cadena es `R4·C1`. Su
capacidad deriva fuerte con temperatura, así que el τ de campo no va a ser el de
banco. Para poner la cota conservadora de la espera necesito el rango real:
¿0–40 °C es razonable, o hacen campañas de madrugada con menos?

## 3. ¿La calibración corre en cada arranque?  · no bloquea, pero cambia el diseño

Si corre siempre al bootear, el presupuesto de 5 min pesa en cada encendido en
campo. Si arranca de EEPROM y sólo re-calibra cuando el error se pasa de un
umbral, el presupuesto casi no importa y conviene otro esquema.

## 4. Ganancia del LP: 295 o 651  · no bloquea

`CAL_PI_GAIN_GEO_LP_X1000` vale **295 en el proyecto de campo** y **651 en el de
test**, con el mismo comentario y la misma fecha (barrido D2 del 2026-09-02). En
tus memorias quedó 651.

Sospecho que son dos puntos de la misma curva no lineal (medida: 29 cuentas/código
cerca de Vref, 75,6 en −224; ratio 2,6 ≈ 651/295 = 2,2). Como el LP usa la curva
por trozos y no la constante, hoy no hace daño — pero uno de los dos números está
mal y quiero saber cuál antes de copiarlo a otro lado. **Lo voy a medir igual**,
así que esto es sólo para contrastar contra lo que recordás.

## 5. El proyecto de autotest, ¿quedó al día con la placa nueva?  · **BLOQUEA**

Grabé el firmware de **autotest** en el PSoC (272 filas verificadas, sin
`-AllRows`) y el enlace PSoC↔ESP quedó **muerto**: `probe=0`, `ping=0`, cero
tramas buenas y cero malas. Cero malas es lo raro — no es que llegue basura, es
que no llega **nada**.

Con el firmware de **campo** el enlace sí andaba. La diferencia entre los dos
proyectos es el TopDesign, y vos actualizaste el de campo el 2026-09-03 a las
16:40 para agregarle `polarity_reg`.

Pregunta: **¿el TopDesign de `AcondicionamientoAnalogicoTest` alguna vez se
actualizó a la placa nueva** (I2C de subida, UART sólo RX, `polarity_reg`), o
quedó en la versión vieja? Si quedó viejo, explicaría que no hable por I2C, y
entonces el camino no es debuggear sino portar el autotest sobre el TopDesign de
campo.

Mientras tanto sigo investigando por mi cuenta; si lo resuelvo, tachá ésta.

---

*Se agregan al final a medida que aparecen.*

---

## 6. El Ki no hace nada en el modelo — ¿lo ponemos igual?  · decisión tuya

Barrí Ki de 0 a 1/1 y el error queda **plano en 4,44–4,59 mV**, con la misma
tasa de éxito, y las inversiones de sentido del DAC *suben* (14 sin integrador,
25–32 con él).

No es un bug, y la explicación importa: **el integrador corrige lo que el lazo
observa.** Acá el lazo mide, ve el valor equivocado (está sobre un transitorio),
lo anula perfectamente, declara lock y se va. El error aparece *después*, cuando
el transitorio decae — y para entonces nadie está mirando. Ningún Ki arregla eso.

Tenés razón en el principio: con `Kp=1` puro y una ganancia conocida con dos
cifras, queda error permanente. Pero eso se ve sólo si el lazo sigue observando.
O sea que **el Ki es la herramienta para un ajuste lento de fondo, no para la
calibración de un tiro.**

Mi propuesta: **Ki = 1/64 o 1/32**, que es lo mínimo que no agrega oscilación
medible, puesto como red de seguridad contra lo que el modelo no captura — no
porque la simulación lo pida. Decime si te sirve así o preferís otra cosa.

## 7. Los abortos son por riel del DAC, no por watchdog  · **puede cambiar el hardware**

Separando las causas de aborto, en el modelo salen **15–16 de 40 corridas, todas
por riel** (el DAC pega contra ±255) y **cero por timeout**. Y la tasa **no
cambia** con el multiplicador de τ: 0τ y 6τ abortan igual.

Si esto se confirma en la placa, quiere decir que hay dos problemas separados y
que la espera sólo arregla uno:

- la **espera** arregla el *error* (33,5 mV → 0,37 mV de 0τ a 5τ);
- los **abortos** son falta de *autoridad*, y eso no se arregla con firmware.

Ojo que este número depende de parámetros que inventé (offsets típicos y el
factor de acople en continua), así que **no me lo creas hasta medirlo**. Pero si
se confirma, la conversación pasa a ser de rango de los IDAC o de resistencias
de referencia, no de sintonía.

## 8. `grueso_fino` da mejor y más rápido, pero la tendencia está al revés  · no bloquea

Mi esquema de pasada gruesa → una sola espera → pasada fina da **3,55 mV en 51 s**
contra 12,4 mV en 128 s del esquema de esperar en cada etapa. Mejor y 2,5× más
rápido.

Pero **empeora** al subir el multiplicador (3,55 → 5,2 → 8,3 → 9,7 mV), que es
al revés de lo que debería pasar. Eso me dice que la implementación o el modelo
tienen algo mal y todavía no lo encontré. No lo tomes como resultado.

## 9. Un supuesto mío que no pude verificar  · **conviene descartarlo antes de soldar**

Di por sentado todo el tiempo que **el PSoC está ejecutando** su firmware, porque
graba y verifica bien. Pero grabar y ejecutar no son lo mismo: el KitProg lo
graba con el chip *detenido*.

Lo que sí verifiqué por SWD: responde, y su JTAG ID es `2e 16 10 69`. Eso prueba
que el chip está vivo y alimentado, **no** que esté corriendo tu código.

No pude ir más lejos: `ppcli` no expone lectura de RAM ni estado del núcleo, y
no hay pyocd ni openocd en la máquina.

**Por qué importa:** si el PSoC no está ejecutando, poner los dos 4k7 no va a
arreglar nada y vas a haber soldado al pedo. Se descarta en diez segundos
mirando el **LED D1**, que el firmware maneja como indicador de estado: si
titila o está encendido, está corriendo y el problema es sólo el bus. Si está
apagado, el problema es otro y hay que mirar la alimentación del PSoC antes que
los pull-ups.

Es la única cosa que me quedó sin poder cerrar por software.

---
---

# Estado al cierre del 2026-09-04 — las preguntas 1 a 9 quedaron viejas

Las de arriba se contestaron o quedaron sin objeto. **Todo lo medido está en
`docs/MEDICIONES_2026-09-04.md`**, que es el documento único. Acá quedan sólo las
decisiones que son tuyas.

## A. ¿1τ o 2τ de espera de planta?  · ya está puesto en 1τ

Puse `CAL_PI_PLANT_SETTLE_TAU_X10 = 10` (1τ) porque el modelo, ya calibrado
contra la placa, da **2,09 mV en 119 s** contra tu objetivo de 20 mV. Con 2τ da
**0,47 mV en 237 s**.

Como la recalibración es por umbral y no en cada arranque, el tiempo casi no
importa, así que **2τ es asequible si querés más margen**. Es cambiar un 10 por
un 20. Decidí vos.

**Ojo para campo:** 29,5 s es el τ de banco. Con 5–45 °C el peor caso es ~40 s,
así que una espera fija conservadora hay que dimensionarla con eso, no con 29,5.

## B. El acople ADDER→LP es 4,04×. ¿Firmware o hardware?  · **la decisión de fondo**

Mover la referencia del ADDER corre la salida del LP **cuatro veces más** que la
referencia del propio LP. Con la autoridad del LP en 133,8 mV y el ADDER
metiéndole 254,5 mV al moverse 120 códigos, lo saca de rango.

Dos caminos, y no los puedo elegir por vos:

- **Firmware:** precompensar. Ya está implementado en el modelo
  (`calibrar_precomp`): al cerrar la etapa k se corrigen de una las j>k por
  `G[k][j]·Δ/G[j][j]`, que ahora se conoce porque está medido. No mejora en
  1×/1× porque los offsets son de ~1 mV, pero es exactamente para el caso de
  ganancia alta.
- **Hardware:** subir la autoridad del LP, o bajar el acople del ADDER.

## C. El ADDER pierde el 40 % de su rango. ¿Se acepta o se toca el hardware?

Su pendiente local va de 1963 µV/cód en el centro a **0,4 en los extremos**.
Acoté el IDAC a ±128 por firmware (commit `9af676d`), que es la solución barata.
Se pierde el tramo −178…−128, que sí es útil, porque el clamp es simétrico.
Soportar límites asimétricos es un cambio chico pero toca la estructura y todos
los inicializadores; no lo hice a las apuradas.

## D. Ki: puesto en 1/32 como red de seguridad

El barrido sale plano. El integrador corrige lo que el lazo **observa**, y acá el
lazo cierra y se va antes de que el error aparezca. Va como seguro contra lo que
el modelo no captura, no porque la simulación lo pida.

## E. Lo que hay que revertir del banco

- **COM8 (maestro): le grabé `slaveTest` por error.** Hay que devolverle el
  firmware de master.
- **COM7 (esclavo): tiene `slaveTest`.** Devolverle `slave2` para campo.
- **PSoC: tiene el autotest.** Devolverle el de campo.
- `platformio.ini` tiene `upload_port = COM8` fijo en el entorno `slaveTest`, que
  es lo que causó el error. Conviene sacarlo.
