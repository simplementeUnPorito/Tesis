# Calibración en campo: puesta a punto, identidad de placa y trazabilidad

Arquitectura propuesta por Elías el 2026-09-12, con agregados míos marcados como
tales. No es para implementar entera ahora: es para que lo que se construya deje
lugar a esto.

## El ciclo de vida de una placa

1. **Estado "placa nueva".** El PSoC arranca sin parámetros y se niega a operar.
   Necesita conectarse a una PC para la puesta a punto inicial.
2. **Puesta a punto.** La PC corre la identificación pesada, la que hoy tarda
   veinte minutos: constantes de tiempo, pendientes, signos, consignas por
   ganancia. Se escriben en la placa y se archivan en el servidor.
3. **Identidad.** La placa recibe un **ID**, y el juego de parámetros queda
   asociado a ese ID con su fecha.
4. **Campo.** Cada esclavo manda su ID en los metadatos de cada captura. El
   servidor sabe entonces qué parámetros se usaron y de cuándo son.
5. **Gestión de flota.** El servidor puede avisar si los parámetros de una placa
   están viejos, o si se alejaron del resto de las placas más de lo razonable.

## Requisitos de tiempo, que son los que mandan

| situación | límite |
|---|---|
| dejar el nodo usable tras armar el tendido | **10 minutos** |
| cambiar la ganancia de PGAout | "un tiempo razonable", se itera un par de veces |
| operación sostenida después | horas sin volver a tocar |

El flujo real de campo es: se arma el tendido, el nodo se calibra mientras se
ubica todo, se hace un disparo de prueba para ver amplitudes, se elige ganancia y
resolución del ADC, eso itera dos o tres veces, y después se usa así mucho rato.

## Decisión de Elías: PGAgain fijo, sólo se mueve PGAout

**Está bien fundada y los datos la respaldan.** PGAgain alimenta al pasabanda, y
mover cualquier cosa que llegue a ese nodo arranca la cola de treinta a cincuenta
segundos del acople de 680 µF. PGAout está después del sumador y no la excita.

Consecuencia para el diseño del lazo: **al cambiar de ganancia hay que preferir
el actuador rápido.** Los actuadores que tocan el pasabanda sólo se mueven si el
rápido no alcanza, porque cada uno de esos movimientos cuesta una cola.

Con la consigna de cada ganancia guardada, el rápido debería alcanzar casi
siempre. Estimación honesta del cambio de ganancia: **dos a tres minutos**, no
segundos, porque el efecto del actuador rápido igual decae parcialmente con la
misma constante (18,78 mV/código instantáneos contra 12,35 de régimen).

## Agregados míos

### 1. Guardar las condiciones, no sólo los valores

Comparar una placa contra el resto sólo tiene sentido si se sabe en qué
condiciones se midió cada una. Junto a cada parámetro conviene archivar la
temperatura si está disponible, la tensión de alimentación y la ganancia. Sin
eso, "esta placa está fuera del rango de las demás" puede ser sólo que se midió
en otro momento del día.

### 2. Guardar la calidad de cada medición, no sólo el número

Un parámetro medido mal y uno medido bien ocupan lo mismo y se ven igual. Conviene
archivar junto a cada valor su residuo, cuántos reintentos hizo falta, y si se
usó un respaldo en vez de una medición. Hoy tengo tres casos donde un número
plausible venía de una medición inservible.

### 3. Que el nodo informe qué usó, no sólo quién es

El ID dice qué parámetros **debería** tener. Que el nodo devuelva además la
versión del juego que efectivamente cargó cierra el lazo: si el servidor cree una
cosa y la placa tiene otra, se detecta en la primera captura y no meses después.

### 4. Verificación de signos como diagnóstico de hardware

Los signos de los actuadores son topología del circuito: **no pueden cambiar**
salvo que se rompa algo. Compararlos contra los guardados detecta una resistencia
mal soldada o un componente muerto.

**Corrección del 2026-09-13: medirlos NO es barato, y en el campo no hay que
medirlos.** Son unos 2,5 minutos, dominados por las esperas de τ que necesitan
IDAC0 e IDAC1 para dar una pendiente con sentido. Y sobre todo, no evitan un mal
resultado: si un signo se dio vuelta es porque se rompió algo, y entonces la
calibración va a fallar igual y ruidosamente, con el lazo sin converger y los
taps contra los rieles. La verificación dice *por qué*, no *si*.

Hay además un detector gratis: **el propio lazo delata un signo invertido en
pocos pasos**, porque manda el actuador derecho a su tope, y el regulador ya
reporta eso ("fino en su límite"). No hace falta medir nada para tenerlo.

Entonces:

- **Placa nueva, en el banco:** verificar los siete signos una vez, al crear el
  perfil. Están en `perfil_placa.SIGNOS` y `signos_sospechosos()` dice *cuál* se
  dio vuelta, que es lo que indica dónde mirar en la placa.
- **Campo:** no verificar. Aplicar el punto, esperar el transitorio, arrancar el
  lazo. Si no converge Y el actuador quedó clavado en su tope, ahí se corren los
  signos como diagnóstico.

Con eso la fase 1 en campo queda en **2,2 minutos**, que es sólo el transitorio
del acople de 680 µF. Irreducible: es el capacitor cargándose.

### 5. Mejor que la fecha: cuánta corrección hizo falta

Una fecha estima el envejecimiento; la corrección lo **mide**.

Si el nodo informa cuánto tuvo que mover los actuadores respecto de los valores
guardados, se sabe directamente si los parámetros siguen sirviendo. Correcciones
que crecen captura a captura son la señal de que hay que rehacer la puesta a
punto, y llegan mucho antes que cualquier plazo fijado a ojo.

La fecha igual se guarda, porque es barata y sirve de red de seguridad. Pero el
disparador bueno es la corrección.

### 6. Marcar los datos tomados sin calibración válida

Si el nodo tuvo que operar con parámetros viejos, o sin poder verificar, la
captura debería salir marcada. Un dato dudoso identificable es mucho menos
peligroso que uno dudoso mezclado con los buenos.

## Lo que esto implica para lo que se está construyendo ahora

- El archivo de parámetros que voy a generar tiene que llevar **fecha,
  condiciones y calidad**, no sólo valores. Así el mismo formato sirve después
  para el servidor.
- El firmware tiene que distinguir **"no tengo parámetros"** de **"tengo
  parámetros viejos"**, porque la respuesta correcta es distinta: en el primer
  caso se niega, en el segundo opera y avisa.
- El lazo cerrado tiene que poder informar cuánto corrigió, que es el insumo del
  punto 5.

## Reparto offline / online, con el presupuesto de tiempo medido

Implementado en `perfil_placa.py`. La división no es por comodidad: es por qué
depende cada cosa.

**Va al archivo, se mide una vez en el banco.** Dependen del cobre y de los
componentes, no del día ni del terreno.

| constante | valor medido | cómo se mide |
|---|---|---|
| τ del pasabanda | 26 a 32 s | escalón de IDAC1 y ajuste exponencial |
| IDAC3 → LPo | 6,68 mV/código | ABBA de 4 bloques, con LPo dentro de ventana |
| IDAC2 → ch2 | 12,1 mV/código | ABBA |
| IDAC0 → ch0 | 61 a 63 mV/código | ABBA, en fase 1 |
| IDAC1 → ch1 | 2,9 mV/código | ABBA con corrección por τ |
| Vdda | 4.826 mV | tester |

**Se mide siempre en el campo.** Dependen de la temperatura, del geófono
conectado y de cuánto hace que la placa está encendida.

- Los cuatro códigos del punto de trabajo.
- La validación de que ningún tap quedó contra un riel.

El perfil guarda además el **último punto de trabajo conocido por ganancia**. No
es un valor de confianza: es el punto de partida de la búsqueda, y es lo que
convierte una bisección de nueve pasos en una de tres o cuatro.

### Qué cuesta cada parte, hoy

| etapa | tiempo | ¿se puede saltear con el perfil? |
|---|---|---|
| caracterización de fase 1 (τ y pendientes) | 3 a 5 min | **sí** |
| espera del transitorio del pasabanda | 100 s | no, es física |
| bisección de IDAC3 sobre LPo | 80 s | se acorta con el punto guardado |
| bisección de IDAC2, si hace falta | 80 s | se acorta igual |
| mid-ranging y verificación | 150 s | no |

Con el perfil cargado, lo que queda es del orden de **seis minutos**, dentro del
límite de diez que puso Elías. Sin perfil son diez u once, que es exactamente el
caso "placa nueva" en el que se acepta esperar.

### Regla de vencimiento

`perfil_placa.py` usa noventa días como plazo sugerido y guarda la fecha, así
que quien quiera otro criterio lo aplica sobre el mismo dato. Una fecha en el
futuro **no** cuenta como vigente: un reloj mal puesto no debe hacer pasar por
bueno un perfil que nadie verificó.

## El PI queda permanente, no termina al converger

Decisión de Elías del 2026-09-13, y los datos de esa madrugada la respaldan.

**El problema:** el punto de trabajo se corre solo. Una calibración que converge
y termina pierde el punto en minutos, por buena que haya sido la convergencia.
Eso explica, retrospectivamente, buena parte del historial de PASS que no
sobrevivían.

Cuánto se corre está medido **sólo dos veces**, y conviene decirlo con esa
precisión. De las doce corridas de la madrugada que hicieron la verificación de
un minuto con todo congelado, diez terminaron con LPo contra un riel y midieron
entre 0 y 1,3 mV: **eso es el riel, no la estabilidad**. Un tap clavado no se
mueve. Las únicas dos con LPo dentro de ventana dieron:

| corrida | LPo final | deriva en 60 s |
|---|---|---|
| 08:53, PGA x1 / PGAout x1 | +35,0 mV | **+15,3 mV** |
| 09:2x, PGA x1 / PGAout x1 | −335,6 mV | **+141,4 mV** |

Dos puntos no son una caracterización, y difieren en un factor nueve. Medir esto
bien —con el lazo congelado y LPo centrado, durante varios minutos y a varias
temperaturas— es de las primeras cosas que hay que hacer una vez que el lazo
cierre de forma repetible.

**La decisión:** después de la fase 1, el PI **no se apaga**. Sigue corrigiendo
indefinidamente, y sólo se congela cuando arranca una adquisición.

**Y hay una razón de hardware que la vuelve obligatoria:** el AMux es compartido.
Para medir los taps hay que sacarlo del canal de captura, así que el PI no puede
correr durante una adquisición ni aunque se quisiera. Congelar no es una
concesión al ruido: es forzoso.

### Qué informa el nodo al maestro

Elías pide el mínimo: **en rango / fuera de rango**. De acuerdo, y agregaría un
byte más: **cuánta corrección viene aplicando el PI**. Es el punto 5 de este
mismo documento —la corrección mide el envejecimiento, la fecha sólo lo estima—
y es lo que avisa que los parámetros quedaron viejos *antes* de que el nodo se
salga de rango.

### El número que falta medir

**Cuánto puede estar congelado el lazo.** Sale de la deriva y de cuánta excursión
de LPo se tolere:

| deriva | 200 mV de excursión tolerada |
|---|---|
| 15 mV/min | 13 minutos de captura |
| 141 mV/min | 1,4 minutos |

Los dos valores salen de las dos únicas mediciones válidas que hay, así que la
tabla acota el orden de magnitud y nada más: entre un minuto y un cuarto de
hora. La diferencia entre esos dos extremos decide si un tendido se puede dejar
capturando o hay que recalibrar entre disparos, así que el número merece una
medición propia.

Es un dato de campo de primer orden y sale de la misma medición que ya hace la
verificación final del calibrador: congelar todo y mirar LPo.

### Precauciones de implementación

- Al congelar, el integrador **no debe seguir acumulando** sobre la última
  lectura. Un integrador alimentado con un error estancado se escapa.
- Al reanudar, arrancar de los códigos que quedaron, **sin salto**.
- El período del lazo permanente puede ser lento —una corrección cada treinta o
  sesenta segundos alcanza para una deriva de 15 mV/min— y así los actuadores
  se quedan quietos casi todo el tiempo.

## Las dos fases, como quedan tras el 2026-09-13

### Fase 1 — el adelanto: 2,2 minutos

Deja de medir nada. Aplica el punto guardado, espera el transitorio del acople
de 680 µF y listo. Todo lo que antes medía está fijado, con su justificación:

| qué era | ahora | por qué |
|---|---|---|
| medir τ, dos veces | fijo en 44 s | 102 mediciones: media 30,9, desvío 6,8. Se toma media + 2σ |
| ABBA de IDAC0 y de IDAC1 | fijas | dispersión 5 y 12 % contra una tolerancia del lazo de 9× |
| optimizar IDAC0/IDAC1 | punto del perfil | son de antes de PGAout: no dependen de la ganancia de salida |
| verificar signos | sólo en el banco | ver punto 4: no evitan un mal resultado, sólo lo explican |

Los 2,2 minutos son 3τ y son irreducibles: es el capacitor cargándose.

### Fase 2 — el lazo cerrado

**Etapa A, llevar el sumador a la consigna que deja LPo legible: 1 a 3 minutos.**
La consigna se **busca, no se calcula**. El modelo la predijo mal todas las veces
—el 2026-09-13 dijo −270 mV y LPo siguió contra su riel ahí y en otros diez
candidatos—. Con la consigna de la sesión anterior guardada, la búsqueda arranca
estrecha alrededor de la predicción en vez de rastrear cuatro voltios: uno a tres
candidatos, y cada uno son unos 50 s porque el lazo de ch2 converge en diez pasos.

**Etapa B, cerrar sobre LPo con IDAC3: 80 segundos.** Es el actuador natural de
esta etapa: 6,68 mV por código, ±1,70 V de recorrido, y **no escala con PGAout**
porque entra después. Trece sondeos de seis segundos.

**Etapa C, el lazo no termina.** Período lento —30 a 60 s alcanzan para una
deriva de 15 mV/min—, congelado durante la adquisición, reportando al maestro si
está en rango y cuánta corrección viene aplicando.

### El presupuesto

| | tiempo |
|---|---|
| fase 1 | 2,2 min |
| fase 2 A | 1 a 3 min |
| fase 2 B | 1,3 min |
| **hasta el primer dato usable** | **4,5 a 6,5 min** |

Entra en los diez minutos con margen. Lo que falta demostrar es que la etapa A
converja a PGA x50: el 2026-09-13 no lo logró en ninguna corrida, y la causa está
medida —el punto de trabajo se corre más que la ventana del sumador en decenas de
minutos—. El presupuesto describe el diseño; ese bloqueo está aparte.

---

# Revisión del 2026-09-13 (noche): el techo de ganancia es del circuito

Esta sección corrige supuestos de todo lo anterior. Lo que cambia no es el
diseño del lazo —el PI en cascada con mid-ranging y vernier sigue en pie— sino
**hasta dónde tiene sentido pedirle que llegue**.

## 1. La etapa de salida tiene punto fijo propio

`ch3 = Vref_o + G·(ch2 − Vref_o)`, con **Vref_o entre −260 y −395 mV** según el
punto, medido en cinco corridas. No es el cero del ADC, y no se sabe de dónde
sale: en la placa real todas las referencias son Vdda/2, que es también el cero
del ADC, así que la predicción sería cero.

Consecuencia operativa: la consigna de OPA_SUMo **no es cero** sino

```
ch2* = (ch3_cero + (G−1)·Vref_o) / G
```

Centrar ch2 en cero es lo que hacía imposible pasar de PGAout x1: a x4 empujaba
SUMo 1365 mV, contra el riel, hiciera lo que hiciera el lazo. Con la consigna
correcta el salto a x2 aterriza bien y de forma reproducible —tres corridas
seguidas con LPo entre −46 y +121 mV y los cinco taps en ventana—.

**Los dos números hay que medirlos en el punto, no tabularlos.** `Vref_o` varía
entre corridas y `ch3_cero` se corre ~1650 mV cuando se mueve IDAC3.

## 2. El cero del pasabajos se mueve con IDAC3

`ch3_cero` depende de dónde esté IDAC3. Calcularlo antes de reacomodar IDAC3 y
usarlo después mandó ch2 170 mV para el lado contrario. Hay que rehacerlo
después de cualquier cambio de IDAC3.

Y la ganancia del pasabajos desde SUMo es **×4,8**, no ×18: medida tres veces
seguidas en los intercambios de la fase 0, donde IDAC3 e IDAC2 se mueven de a
poco y LPo se lee en cada paso. El ×18 venía de comparar lecturas de corridas
distintas.

## 3. IDAC3 sólo necesita el margen que la ganancia pide

El fino cubre el error de cuantización del grueso, o sea medio paso de IDAC2
sobre LPo. A x2 son 60 mV, o sea **nueve códigos**. Vaciar IDAC3 de +255 a 0
camina ch2 unos 300 mV y no hace falta: `margen_necesario()` pide 27 códigos
para x2 y 213 para x16.

Importa porque las excursiones grandes de ch2 son las que despiertan el
problema del punto 5.

## 4. El compliance de los IDAC no es el límite

Los cuatro en rango de 32 µA (`calibration.c:666-674`). Con R de 15 k, 15 k,
5,1 k y **10 k** (el `#define` del LP decía 1 k y estaba desactualizado), la
excursión máxima del nodo son 478 mV y el margen al borde de
[VSSA+1, VDDA−1] es de más de 1 V en todos. Cerrado con números en
`COMPLIANCE_DE_LOS_IDAC_Y_MARGEN_DE_IDAC3_2026-09-13.md`.

## 5. A ganancia conjunta 100 la cadena diverge sola

El hallazgo que reordena todo, probado con un experimento de control: se llega
al punto, se **congelan los cuatro códigos** y se mira.

| ganancia conjunta | congelado | qué hace |
|---|---|---|
| 50 (x50 · x1) | 10 min | excursiona 1.044 mV **y se asienta**; los 30 min siguientes se queda en 52 mV |
| 100 (x50 · x2) | 5 min | excursiona ~1.700 mV **y no vuelve**: satura y se queda ahí |

La diferencia no está en cuánto se mueve al principio —los dos tramos empiezan
justo después de aplicar códigos y capturan el transitorio— sino en si vuelve.
A ganancia 100 la cadena va siempre al mismo atractor
—`ch2 = +1672,4 mV`— al que ya había llegado ocho horas antes por otro camino.

Eso descarta que el problema esté en el lazo de calibración: no había lazo
corriendo. Y descarta también que sea el paso por el riel durante la
transición, porque en la corrida citada LPo aterrizó en −45,8 mV y nunca lo
tocó antes de que empezara la divergencia.

Mecanismo candidato, **no comprobado**: los cuatro pines `Vref_XX` cuelgan del
mismo nodo a través de sus resistencias, así que hay realimentación entre
etapas que no pasa por la señal. Si la ganancia de ese lazo parásito escala con
la ganancia de la cadena, hay un umbral por encima del cual el conjunto deja de
ser estable, que es la forma de lo observado. Predicción comprobable: el umbral
debe seguir al **producto** de las ganancias y no a cuál etapa lo aporta.

## 6. Cómo medir la estabilidad, y cómo no

La deriva congelada sólo dice algo **desde un punto calibrado**. El mapa hecho
con los IDAC en cero no distingue nada: con esos códigos LPo queda clavado en
todos los puntos y una cadena con una etapa en el riel deriva por eso, así que
hasta x50·x1=50 —que es estable y reproducible— dio "diverge" con +882 mV/min.

El procedimiento válido es `saltar_ganancia.py --congelado N`: calibrar,
congelar, medir. Y el control corre **calibre o no** la ganancia; un control que
sólo se ejecuta cuando el experimento sale bien no es un control.

## 7. A ganancia 50 el punto se sostiene, y el PI no tuvo que hacer nada

Media hora a PGA x50 / PGAout x1, con el PI corriendo cada 20 s:

```
LPo entre -83,4 y -31,8 mV, excursion 51,5 mV, 87 de 87 lecturas en tolerancia
correccion aplicada: IDAC3 +255 -> +255, IDAC2 -95 -> -95
taps finales: ch0 -1150,6  ch1 -21,6  ch2 +1,7  ch3 +1,2  ch4 -47,9
```

El punto aguanta. Pero **el lazo no movió un solo código**, así que esta corrida
prueba la estabilidad del punto y NO la utilidad del PI: los 52 mV no los logró
el regulador, los logró la cadena sola.

Para medir lo que aporta el lazo hace falta un tramo donde la cadena
efectivamente se mueva —después de un golpe al geófono, o con el orden de los
dos tramos invertido para que el PI reciba el transitorio y el congelado la
cadena ya asentada—. Queda pendiente y es una corrida corta.

Corolario para el dimensionamiento: en un punto asentado la cadena deriva mucho
menos que los 15–141 mV/min que se venían citando, así que el PI permanente no
tiene que ganarle ninguna carrera y le alcanza con decenas de segundos de
período.

## 8. Cierre del 2026-09-14: el techo lo pone el PGA

Las secciones 5 y 6 de arriba concluyen que el problema aparece por encima de
cierta ganancia conjunta. **Es falso**, y la sección 5 hay que leerla sólo por
el método —congelar y mirar— no por su conclusión.

Lo medido, con el PI sosteniendo y juzgando el régimen:

| PGA | máximo sostenido | con PGAout |
|---|---|---|
| x2 | nada, ni 48 | — |
| **x4** | **96** | **x24** |
| x8 | 64 | x8 |
| x16 y más | nada sobre 50 | — |

**PGAout no era el problema**: x16 y x24 se sostienen perfectamente si el PGA
es x4. Lo que no funciona es el PGA alto, y hay un óptimo en x4 con caída a los
dos lados —x2 también falla, lo que impide la explicación simple—.

Ganancia por defecto de campo: **PGA x4 · PGAout x24 = 96**, punto
`IDAC +0 +164 +75 -87`, con el PI permanente encima.

Detalle y tabla completa de las diecisiete combinaciones probadas en
`RESULTADO_GANANCIA_2026-09-14.md`.
