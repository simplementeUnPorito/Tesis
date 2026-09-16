# Conclusiones parciales — 2026-09-11, 17:00

## Lo que quedó demostrado hoy

**El bloqueo de las ganancias altas no era de calibración.** PGAout **carga al
sumador**, y la carga crece con la ganancia. Medido: la pendiente de ch2 contra
IDAC2 vale 5,04 mV/código en x1 y 10,89 en x2, y ch2 se clava contra su riel
desde x4. Cambia la planta, no sólo el punto de trabajo. Todo lo que se probó
antes de entender eso atacaba síntomas.

**El cambio de IDAC2 a 11,8 kΩ era necesario y funciona.** Paso medido en x4:
13,4 mV/código, exactamente lo que predice la resistencia. Y por primera vez ch2
se centró en una ganancia alta, quedando en −9,7 mV. Antes era imposible: hacían
falta 3206 mV de recorrido y había 1556.

**La ventana de validez estaba mal y dejaba pasar taps rielados.** El límite de
arriba usaba Vdda (banco 1122,7) en vez del riel de salida medido (1106,1). Los
lazos de x16 y x24 daban por bueno un LPo de +2115 y +2142 mV estando el riel en
+2084. Corregido: ahora la ventana se acota al riel medido.

## Lo que quedó refutado

**Que el offset de LPo fuera de la etapa LP.** Con ch2 centrado en cada ganancia,
LPo queda en −1797 mV en x1 y fuera de rango desde x2. El offset escala con la
ganancia, así que nace antes de PGAout, no después.

## CORRECCIÓN de las 17:30 — la consigna SÍ es casi independiente de la ganancia

A las 17:00 escribí que la medición desmentía esa hipótesis. **Estaba mal, y la
culpa era de la medición, no del modelo.** El criterio de validez aceptaba
lecturas por encima del riel, así que la búsqueda daba por bueno un LPo apoyado
contra el tope y se detenía en un ch2 cualquiera.

Repetida con la validez corregida:

| PGAout | ch2 que mejor centra LPo |
|---:|---:|
| x4 | −342 mV |
| x8 | −334 |
| x16 | −341 |
| x24 | −332 |

Cuatro ganancias, −337 ± 5 mV. La consigna es efectivamente la misma, que es lo
que predice el modelo de un offset que se amplifica junto con la señal.

## El límite real, medido

**En x24 un solo código de IDAC2 mueve LPo unos 2,8 V**, más de la mitad de toda
su ventana útil. La cuantización de IDAC2, vista desde LPo, es más gruesa que el
rango de LPo. Por eso ninguna búsqueda sobre IDAC2 sola puede centrarlo.

Eso confirma el reparto que el algoritmo ya implementa: IDAC2 deja LPo dentro de
medio código, o sea ±1,4 V, e **IDAC3 hace el trim fino** con ±1,65 V de
autoridad y 6,5 mV de paso. Justo alcanza, y es la razón por la que el cambio de
IDAC3 a 6,68 kΩ también hacía falta.

**Que 1 kΩ sirviera para IDAC3.** El corte está en x4, medido.

## Lo que sigue sin saberse

Por qué LPo se va de rango en las ganancias altas aun con ch2 centrado. Las dos
hipótesis que tenía quedaron descartadas hoy. La medición de la consigna por
ganancia salió contaminada porque el criterio de validez aceptaba lecturas
rieladas; hay que repetirla ahora que eso está corregido.

## Estado del código

16 pruebas sin hardware pasando. Nueve defectos corregidos en dos días, todos de
la misma familia: un número físico o una guarda que el hardware contradice.

## Lo que haría falta para cerrar

Repetir la medición de la consigna por ganancia con la validez corregida. Si
resulta que existe un ch2 que centra LPo en cada ganancia, el algoritmo ya sabe
buscarlo y sólo hay que dejarlo. Si no existe para las ganancias altas, el límite
es de la topología y hay que decirlo como tal.


---

# Cierre del dia — 18:00

## Estado: x4 y x24 todavia NO cierran

Hay que decirlo asi. Se avanzo mucho en entender el problema, pero la fase 2 no
completa en ganancias altas.

## Lo que SI quedo demostrado hoy, con medicion

**El mecanismo.** PGAout carga al sumador y la carga crece con la ganancia: la
pendiente de ch2 contra IDAC2 vale 5,04 mV/codigo en x1 y 10,89 en x2. Cambia la
planta, no el punto. Explica de una sola vez todos los sintomas que se venian
atacando por separado.

**La consigna de ch2, confirmada por dos metodos independientes.** Buscando en x1
da -349 mV; barriendo ganancia por ganancia da -337 +- 5 mV entre x4 y x24; y
remedida en x4 durante una corrida da -314. Es efectivamente la misma en todas
las ganancias, como predice un offset que nace antes de PGAout y se amplifica con
la senal.

**Los dos cambios de resistencia eran necesarios, por motivos distintos.**
IDAC2 a 11,8 kOhm da el RANGO: en x4 hacian falta 3206 mV de recorrido y habia
1556. Paso medido despues del cambio: 13,0 a 13,6 mV/codigo, lo que predice la
resistencia. IDAC3 a 6,68 kOhm da la RESOLUCION que IDAC2 no puede dar: en x24 un
codigo de IDAC2 mueve LPo unos 2,8 V, mas de la mitad de su ventana util.

## Defectos corregidos hoy

1. la ventana de validez llegaba hasta Vdda en vez del riel medido, en
   `escala_banco`
2. y otra vez en el calibrador, que tenia su propia copia
3. la consigna de ch2 se dividia por la ganancia cuando no corresponde
4. el despeje de la consigna sumaba en vez de restar
5. el lazo seguia corrigiendo sobre lecturas fuera de rango
6. y al frenar no volvia al mejor punto valido
7. la precompensacion de IDAC3 traducia mV a codigos con una constante vieja:
   eliminada, la biseccion hace lo mismo sin suponer nada

Todos de la misma familia que los de ayer: **un criterio que existe y un lugar
que decide sin consultarlo**, o un numero fisico que el hardware contradice.

## Lo que falta, concreto

Al entrar a fase 2 en x4, ch2 llega fuera de rango y el rescate por biseccion no
lo recupera. Ese es el proximo punto a atacar, y hay evidencia suficiente para
hacerlo sin adivinar: la consigna se conoce, el paso de IDAC2 se conoce, y el
rango alcanza. Es un problema de secuencia, no de autoridad.

## Advertencia de metodo

Dos veces hoy di por refutado un modelo correcto porque la medicion que lo
contradecia estaba contaminada por aceptar lecturas rieladas. La regla ya estaba
escrita en el handoff de ayer y la volvi a violar. Por eso ahora esta en el
CODIGO y no en la documentacion.


---

# HALLAZGO FINAL DEL DIA — el que satura es SUMo, no LPo

Ultima corrida, `dos_fases_calibrate-gains_20260911_165732.json`:

```
ch2   -306 mV    VALIDO, y en su consigna de -285
SUMo  -5064 mV   FUERA DE RANGO
LPo   +2299 mV   clavado, y no se mueve ni con IDAC3 en -255
```

El lazo de IDAC2 funciono perfecto: llevo ch2 a su consigna convergiendo suave de
-67 a -306 mV. **Pero SUMo, que es la salida de PGAout, esta saturado.**

Con ch2 en -306 mV y ganancia x4, SUMo deberia estar en -1224. Esta en -5064:
cuatro veces mas abajo. **PGAout tiene su propio offset grande**, y es el que
satura. LPo llega clavado porque su entrada ya viene contra el riel, y por eso
IDAC3 no puede rescatarlo por mucha autoridad que tenga: el problema nace antes
que el.

## Lo que esto cambia

La consigna de ch2 se venia calculando para centrar **LPo**. Pero la restriccion
que manda PRIMERO es que **SUMo no sature**, porque si satura todo lo que viene
despues es ciego. Y la consigna que centra SUMo no tiene por que ser la misma que
centra LPo.

## Por donde empezar manana

1. Medir el offset propio de PGAout: con ch2 centrado, leer SUMo en cada ganancia
   y ver cuanto se aparta de `G * ch2`. Eso da el offset referido a su entrada.
2. Recalcular la consigna de ch2 para centrar SUMo, no LPo.
3. Recien despues mirar LPo, que con SUMo en zona lineal deberia ser tratable con
   IDAC3.

## Nota de metodo

Es la TERCERA vez en el dia que el tap que habia que mirar no era el que yo
miraba: primero crei que faltaba alcance en IDAC3, despues que el offset era de
la etapa LP, y resulta ser de PGAout. El patron que lo hubiera evitado es simple
y esta a mano: **ante un tap saturado, leer el tap ANTERIOR antes de concluir
nada sobre el actuador que lo alimenta.**


---

# HALLAZGO CONFIRMADO — 18:00

## El offset de PGAout es -270 mV y cancelarlo desde ch2 destraba la cadena

Medido `Vos = ch2 - SUMo/G` en varias ganancias, con SUMo legible:

    x1   +7 mV     (ganancia unitaria: el PGA no usa su escalera, no hay offset)
    x2  -276 mV
    x8  -265 mV

Constante para G > 1. Confirmado poniendo ch2 en -270 mV a mano y leyendo:

| G | ch2 | SUMo | LPo | SUMo | LPo |
|---:|---:|---:|---:|---|---|
| x2 | -287 | -350 | +48 | vivo | vivo |
| x4 | -275 | -241 | -647 | vivo | vivo |
| x8 | -279 | -221 | -688 | vivo | vivo |
| x16 | -273 | -56 | -2867 | vivo | fuera |
| x24 | -280 | -1320 | -617 | vivo | vivo |

**SUMo entra en rango en las cinco ganancias, incluidas x16 y x24 que nunca
habian cerrado.** Y LPo queda vivo en cuatro de cinco SIN QUE IDAC3 MUEVA UN
CODIGO: quedo en cero toda la corrida.

## Las resistencias NO hay que cambiarlas

Poner ch2 en -270 mV cuesta **21 codigos** de los 255 de IDAC2 con los 11,8 kOhm
ya instalados. El problema nunca fue de autoridad: era que la consigna apuntaba
al tap equivocado.

**El orden de las restricciones importa.** Si SUMo satura, LPo queda ciego y
ningun actuador posterior lo arregla. La consigna tiene que calcularse para
centrar SUMo; LPo se termina despues con IDAC3.

## Lo que falta, y es acotado

El cambio ya esta en el codigo y la consigna sale bien (-270 mV, registrado en el
evento), la pendiente se mide bien (12,478 mV/codigo), pero **el lazo de IDAC2 se
pasa igual**: lleva ch2 a -5180 mV en vez de a -270.

Con la consigna correcta y la pendiente correcta, el defecto esta en
`ajustar_actuador`: en como aplica la correccion respecto de la consigna. Es el
unico lugar que queda por revisar y esta acotado a una funcion.

## Estado

16 pruebas sin hardware pasando. Placa en su estado normal.
