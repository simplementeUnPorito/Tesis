# Centrado de LPo por bisección: método, resultados y techo de ganancia

Fecha: 2026-09-13, de madrugada. Documento en curso, se completa con la escalera
de ganancias.

## Qué cambió respecto de todo lo anterior

Los lazos PI del 12 y el 13 de septiembre fallaron siempre igual: estiman una
ganancia de planta, integran, y cuando la ganancia real no es la estimada se
van al riel. El caso peor fue el del 13 a la madrugada, donde el lazo sobre el
sumador llegó a +34 mV de su consigna y treinta segundos después estaba en
−5.170.

El método nuevo no usa ninguna ganancia. Sólo pregunta **de qué lado del centro
está el tap**, y bisecta. Tres propiedades lo hacen inmune al modo de falla del
PI:

1. El signo sobrevive a la saturación. Un tap contra el riel sigue diciendo
   correctamente "estás de más", aunque no diga cuánto. Todas las mediciones
   fallidas de este proyecto se hicieron con alguna etapa saturada, y ésta es
   la única forma de operar ahí.
2. El intervalo sólo se achica. No hay integrador, así que no hay windup ni
   escapada posible.
3. El número de pasos está acotado de antemano: trece sondeos por actuador,
   siempre. El presupuesto de tiempo de campo se puede calcular en vez de
   estimarse.

## La jerarquía de tres actuadores, y por qué cierra

Los números de esta tabla son los medidos el 2026-09-13, no los que informa la
fase 1. La diferencia importa y está explicada más abajo.

| nivel | actuador | contra qué tap | paso medido | costo por sondeo |
|---|---|---|---|---|
| grueso | IDAC1 (Vref_BP) | ch2 | ~640 mV | 58 s, dos constantes del pasabanda |
| medio | IDAC2 (Vref_ADDER) | ch2, luego LPo | 12 mV nominal | 6 s |
| fino | IDAC3 (Vref_LP) | LPo | 6,68 mV | 6 s |

La condición que hace que la cadena cierre es que **el escalón de cada nivel
entre en el recorrido del siguiente**. Ninguna de esas cuentas necesita ser
exacta: en las dos sobra un factor grande. Ésa es la diferencia con el PI, que
necesitaba la ganancia bien.

El orden de ejecución es de abajo hacia arriba y después de vuelta: se prueba
primero IDAC3, que es el que menos perturba; si no encierra el cero entra IDAC2;
si tampoco, IDAC1. Y después se baja otra vez, nivel por nivel.

**IDAC0 no está en la tabla, y ése es uno de los hallazgos de la noche.** Ver
más abajo.

## La medición que faltaba desde el principio

Ver `AUTORIDAD_REAL_DE_LOS_IDAC_2026-09-13.md`. En resumen: la autoridad de
IDAC3 sobre LPo son **6,68 mV por código y ±1,70 V**, no los 0,58 mV que dice la
curva del firmware ni los 800 a 2.000 mV que yo mismo informé el 12 de
septiembre. Las tres mediciones anteriores se hicieron con LPo contra el riel,
que es justo donde ningún actuador se ve.

## Lo que se observó de la planta en el camino

**El mismo código no da el mismo estado.** Con IDAC0 = +11 e IDAC1 = −50, dos
corridas separadas por quince minutos dieron ch0 en −1.489 mV y en +376 mV. Son
1,9 V de diferencia con los mismos códigos. Eso acota lo que se le puede pedir a
un punto guardado: sirve como **punto de partida** de la búsqueda, no como
valor a aplicar y dar por bueno.

**El sumador sale de la fase 1 contra un riel.** En las dos corridas ch2 quedó
fuera de ventana con IDAC2 en cero, una vez por arriba y otra por abajo. Por eso
hace falta el nivel de IDAC0: los ±2,16 V de IDAC2 no alcanzan para traerlo.

## Reparto offline / online

Implementado en `perfil_placa.py` y documentado en
`ARQUITECTURA_CALIBRACION_CAMPO.md`. Verificado en la placa: con el perfil
cargado, la corrida saltea la caracterización de la fase 1 y arranca la búsqueda
**diez minutos antes**.

## El error que costó la madrugada, y su corrección

La primera versión bisectaba IDAC0 e IDAC2 **mirando LPo**. Parecía razonable:
LPo es el objetivo, y la bisección no necesita saber por dónde pasa la señal.

Es incorrecto, y la placa lo mostró sin ambigüedad. Con el sumador clavado en su
riel, un solo código de IDAC2 llevaba a LPo de +2.302 a −5.572, o sea de un riel
al otro. Eso no es la autoridad del actuador: es el sumador cruzando su zona de
saturación. Cualquier conclusión sobre resolución sacada de ahí está mal, y ya
había pasado antes con IDAC3.

Hay además una razón de fondo. El criterio duro que fijó Elías no es que LPo
quede centrado: es que **ningún tap toque un riel**. Centrar la última etapa
dejando el sumador contra su tope no cumple el requisito, y además no sirve,
porque la primera señal que llegue se recorta.

La corrección es centrar cada etapa contra su propio tap, de arriba hacia abajo,
y recién al final ocuparse de LPo:

1. IDAC0 contra ch2, hasta sacar al sumador de su riel.
2. IDAC2 contra ch2, hasta centrarlo.
3. IDAC2 contra LPo, pero apartándose como mucho ±25 códigos del punto
   anterior. Ese límite es deliberado: si el centro de LPo exige más, el
   conflicto entre las dos etapas es real y hay que informarlo, no taparlo
   sacando al sumador de su ventana.
4. IDAC3 contra LPo, para los últimos milivolts.

El paso 3 es donde va a estar el techo de ganancia, y por eso está instrumentado:
informa cuánto tuvo que apartarse de IDAC2 y dónde quedaron las dos etapas.

## Deuda conocida: tres tests viejos rotos

`test_autocalibracion_dos_fases.py` tiene tres casos que llaman a
`calibrator.calibrate_gain_step`, un método que ya no existe: fue reemplazado
por `calibrate_gain_campaign`, con otra firma. No es una regresión de esta
noche, y no afecta al camino nuevo, que no usa ese método. Pero son tres casos
del guardián de ganancia histórica que hoy no prueban nada.

## El hallazgo grande de la noche: IDAC0 no mueve el continuo del sumador

Bisectando IDAC0 contra ch2, con esperas de 43 segundos:

| IDAC0 | ch2 |
|---|---|
| −21 | +1.897 mV |
| −5 | +1.891 |
| +3 | +1.887 |
| +7 | +1.885 |
| +9 | +1.885 |
| +10 | +1.884 |

Treinta y un códigos, que según la pendiente que mide la fase 1 valen 7,5 V
sobre ch2, y el sumador se movió trece milivolts. **IDAC0 no tiene autoridad de
continua sobre el sumador.**

Es lo que dice la topología, y nadie había sacado la consecuencia. Entre el PGA y
el pasabanda hay un capacitor de 680 µF que bloquea la continua. Un escalón de
IDAC0 aparece en BPo al instante y después se va con τ; en régimen no queda nada.
Los 244 mV por código que la fase 1 informa como `ch2/IDAC0` son **el resto de
ese transitorio medido a una constante y media**, no una ganancia de continua.

En el mismo barrido hubo una sola lectura negativa, en IDAC0 = +11. Cayó
inmediatamente después del sondeo en +43: era el transitorio de ese sondeo, no el
efecto del código que se estaba probando. Con un camino acoplado en alterna, un
barrido mide el paso anterior, no el estado.

Esto matiza lo que dice `project_matriz_acople_medida`, que el acople entre
etapas es de continua y permanente: vale entre etapas conectadas en continua, y
no vale a través del bloqueo del pasabanda.

**Consecuencia:** el actuador grueso del sumador es IDAC1, la referencia del
propio pasabanda, con −9,2 mV por código y ±2,35 V de recorrido. Sigue costando
esperas de dos constantes por sondeo, pero su efecto queda.

### Y un efecto secundario: la fase 1 corrige mal la pendiente de IDAC1

La red del pasabanda es `R4 = 43 k` desde SEo, `C1 = 680 µF` en serie hasta el
nodo inversor, y `R5 = 47 k` de realimentación. Con el capacitor en serie no
circula corriente continua por R4, así que **en régimen BPo se pone exactamente
en Vref_BP**, sin ganancia. Un código de IDAC1 mueve su nodo 0,125 µA × 15 k =
1,875 mV, y eso es lo que termina en BPo.

Lo medido por ABBA en la fase 1 fue 1,986 mV/código, que es 1,875 más lo que
falta asentar. Correcto. Pero después el código lo "corrige por la fracción
asentada" y lo lleva a 2,557, alejándolo del valor real un 36 %.

La corrección está pensada para un actuador cuyo efecto **crece** mientras
asienta. El de IDAC1 sobre BPo **decrece**: en el instante del escalón el
capacitor todavía tiene su carga y el amplificador da de más; a medida que C1 se
recarga, la salida baja hasta el valor de continua. Aplicarle la corrección de
un caso al otro la manda para el lado contrario.

No se tocó hoy para no mover la fase 1 en medio de la campaña de medidas, pero
está anotado: la pendiente buena es la cruda, no la corregida.

### Cuántos pasos necesita cada bisección, y por qué seis no alcanzan

Con seis pasos sobre un intervalo de 400 códigos queda una incertidumbre de
siete, y **el sumador cruza toda su ventana dentro de esos siete**: medido, un
código de IDAC1 vale unos 640 mV sobre ch2 contra los 4,4 V que mide la ventana.
La corrida de las 02:36 terminó dejando el tap contra el riel y creyendo que
había convergido.

La cuenta es log2 del ancho del intervalo: 400 códigos piden nueve pasos, no
seis. Es barato equivocarse acá y caro no darse cuenta, porque el resultado se
ve razonable.

Y hay un dato que sale de esto: **la pendiente de IDAC1 sobre ch2 no son los 9,2
mV por código que informa la fase 1, son unos 640**. Un factor setenta. La razón
es la misma de siempre: la fase 1 la mide con ch2 contra su riel, donde la etapa
comprime y cualquier actuador parece débil. Todas las pendientes contra ch2 que
figuran en el perfil están medidas en esa condición y hay que tratarlas como
cotas inferiores, no como ganancias.

## El nodo a centrar es ch3, no ch2

`psoc_hw.h` lo dice sin ambigüedad, en un comentario puesto el 2026-09-07:

> Desde 2026-09-07 GEO tiene dos puntos distintos alrededor de PGAout: OPA_SUMo
> es el sumador ANTES de PGAout y SUMo es la salida DESPUÉS de PGAout.

`OPA_SUMo` es ch2 y `SUMo` es ch3. **El pasabajos cuelga de ch3.**

La corrida de las 03:09 dejó ch2 en +165 mV, impecable, y el veredicto fue "no
llega". El estado final explica por qué: ch3 estaba en **+1.853 mV**, a un pelo
de su riel, y LPo debajo de su ventana. Centrar ch2 no centra nada aguas abajo,
porque entre uno y otro está PGAout con su ganancia y su propio offset.

ch2 no deja de importar: es la **guarda de saturación**, el aviso de que el
sumador se está recortando antes de que PGAout amplifique el recorte. Se
verifica al final; no es el objetivo.

## Y la aclaración que corresponde sobre IDAC1

Escribí más arriba que IDAC1 no movía el sumador, con doscientos códigos de
evidencia. **Eso estaba mal medido**, por el mismo motivo de siempre: esos
doscientos códigos se barrieron con IDAC2 en cero y el sumador contra su riel,
donde ningún actuador se ve.

Con IDAC2 en −180, que deja el sumador dentro de ventana, IDAC1 sí responde:
−77 da +763 mV y −29 da +350 mV, o sea 8,6 mV por código, muy cerca de los 9,2
que informa la fase 1. Lo que falló en esa corrida fue el ancho de la búsqueda,
±24 códigos alrededor del punto guardado, cuando hacían falta unos noventa.

Lo que sí queda firme es lo de **IDAC0**: ése se barrió con el sumador en el
mismo estado, pero su falta de autoridad de continua no es una conclusión de esa
medición sola, sino de la topología —el capacitor de 680 µF— y se sostiene.

## El barrido que ordena todo: ch2 responde, ch3 está clavado

PGA x50, PGAout x4, IDAC0 = +11, IDAC1 = −53, barriendo IDAC2 de −180 a +180:

| IDAC2 | ch2 | ch3 | ch4 |
|---|---|---|---|
| −180 | +228,7 | +1.856,2 | fuera |
| −160 | +497,4 | +1.856,4 | fuera |
| −120 | +1.049,6 | +1.855,6 | fuera |
| −80 | +1.523,3 | +1.856,8 | fuera |
| −60 | +1.763,3 | +1.856,8 | fuera |
| −40 | +1.880,9 | +1.856,6 | fuera |
| 0 a +180 | +1.884 (riel) | +1.856 | fuera |

Dos hechos, los dos claros:

**ch2 responde impecable.** De +229 a +1.763 en 120 códigos son 12,8 mV por
código, que es el nominal de IDAC2 en su rango de 255 µA. No hay ningún problema
de autoridad ni de resolución en el sumador.

**ch3 no se mueve.** Mientras ch2 recorre 1,65 V, ch3 se queda en +1.856 ± 1 mV.
Y +1.856 mV de banco son 4,59 V contra masa, o sea PGAout **saturado contra su
riel positivo**.

Con eso, el diagnóstico del techo de ganancia cambia por completo. No es que
falte resolución para centrar LPo: es que **PGAout sale saturado y ninguna etapa
aguas arriba lo saca**, porque IDAC2 llega a su tope con ch2 todavía en +229 mV.

La cuenta cierra si la ganancia efectiva de PGAout es 8 y no 4: 229 mV × 8 =
1.832, contra los 1.856 medidos. A x1 la etapa se comporta perfecto —en el
diagnóstico de la madrugada ch2 = +439 y ch3 = +437, ganancia 1,00— así que la
etapa está sana y lo que hay que revisar es el mapeo de código a ganancia.

Lo que hace falta es bajar ch2 por debajo de +229, y eso IDAC2 solo no puede.
IDAC1 sí: a 8,6 mV por código necesita unos 27 códigos, o sea IDAC1 ≈ −26 en vez
de −53.

## El punto de trabajo existe y mide ocho códigos de ancho

Barrido de IDAC1 con PGA x50, PGAout x4, IDAC0 = +11 e IDAC2 = −180:

| IDAC1 | ch0 | ch1 | ch2 | ch3 | ch4 |
|---|---|---|---|---|---|
| −60 | −1.532 | −576 | +338 | +1.856 riel | fuera |
| −52 | −1.531 | −546 | +272 | +1.856 riel | fuera |
| −44 | −1.512 | −527 | +218 | +1.855 riel | fuera |
| **−36** | **−951** | **−677** | **−108** | **+240** | fuera |
| −28 | +355 | −460 | fuera | fuera | fuera |
| −20 en adelante | +357 | −249 | fuera | fuera | fuera |

En IDAC1 = −36 la cadena entera sale de saturación por primera vez en la noche:
ch3 lee **+240 mV, dentro de ventana**. Un código más o menos y todo vuelve a
un riel.

**La zona despejada mide unos ocho códigos de IDAC1**, y eso explica por qué
todas las búsquedas anteriores la pasaban de largo: buscaban con ch3 o con LPo
como objetivo, y esos dos taps están contra un riel en el 95 % del recorrido, así
que no daban ninguna señal útil para orientar la búsqueda. ch2, en cambio, está
dentro de ventana en un tramo mucho más ancho y sirve de guía.

De ahí sale la estructura final, cada nivel contra el tap que todavía tiene rango:

| paso | actuador | tap objetivo | paso medido | costo por sondeo |
|---|---|---|---|---|
| 2 | IDAC1 | ch2 (OPA_SUMo) | 41 mV/código | 43 s |
| 3 | IDAC2 | ch3 (SUMo) | ~51 mV/código | 6 s |
| 4 | IDAC3 | ch4 (LPo) | 6,68 mV/código | 6 s |

Y los rangos encajan: el paso de IDAC1 sobre ch2 son 41 mV contra los ±2,3 V de
IDAC2; el paso de IDAC2 sobre LPo son unos 820 mV contra los ±1.700 mV de IDAC3.

### Y un detalle que no es un detalle: desde dónde se busca

La bisección de IDAC1 hay que hacerla **con IDAC2 en su extremo negativo**. Con
IDAC2 en cero, ch2 está clavado en +1.884 haga lo que haga IDAC1 —el barrido lo
muestra: de IDAC2 = −40 para arriba el tap no se mueve más— y buscar ahí es
buscar a ciegas. La corrida de las 04:02 leyó +1.884 en los dos extremos de
IDAC1 y concluyó que la cadena no llegaba, cuando lo único que pasaba era que
estaba mirando desde el lugar equivocado.

En IDAC2 = −180 el sumador queda en +229 mV, dentro de ventana, y desde ahí
IDAC1 lo puede llevar hasta el cero y cruzarlo.

Es la misma lección de toda la noche, en su forma más pura: **un actuador sólo
se puede medir si la etapa que mira está dentro de su ventana**, y conseguir eso
a veces exige mover primero otro actuador a una posición que no es la final.

## Tres métodos, y cuándo sirve cada uno

Terminé usando los tres, y la elección no es de gusto: la dicta cómo se comporta
el camino entre el actuador y el tap.

**Bisección de signo**, para los actuadores rápidos (IDAC2 e IDAC3). El camino
asienta en milisegundos, así que un salto de medio rango no deja transitorio, y
la bisección da el resultado en trece sondeos acotados de antemano. Es inmune a
la saturación porque sólo usa el signo.

**Barrido monótono en pasos chicos**, para explorar con el actuador lento. La
bisección salta medio rango de entrada, y sobre un camino con τ de treinta
segundos eso deja un transitorio que tapa las lecturas siguientes: medido, IDAC1
= −96 leyó +676 mV la primera vez y −5.165 al volver, con el mismo código y la
misma espera. Con pasos de ocho códigos el transitorio de cada escalón es chico
y todos van en la misma dirección, así que el sesgo no cambia de signo. El
barrido de las 04:29 dio dieciséis puntos perfectamente lineales.

**Medir la pendiente y saltar, verificando**, para operar con el actuador lento.
Barrer su rango entero cuesta veintidós minutos. Como el barrido mostró que la
respuesta es una recta limpia de 6,9 mV por código, medir la pendiente local con
un escalón chico y saltar al cero cuesta cinco sondeos. La diferencia con un PI
—y es toda la diferencia— es que **cada salto se verifica con una lectura
nueva** antes del siguiente: un error de modelo se corrige en la iteración que
sigue, en vez de acumularse en un integrador.

## Un dato incómodo sobre la estabilidad

Entre las 03:57 y las 04:29, con los mismos códigos y las mismas condiciones,
ch2 pasó de −108 mV a +477 mV. Son 585 mV de deriva en media hora.

No bloquea la calibración —el algoritmo vuelve a encontrar el punto en pocos
minutos— pero sí dice algo sobre el requisito de campo: **el punto de trabajo se
corre con el tiempo**, y la calibración no es algo que se hace una vez y queda.
Habrá que medir cuánto aguanta antes de necesitar un retoque, y ése es
exactamente el dato que el punto 5 de la arquitectura pide informar: cuánta
corrección hizo falta.

### Por qué el apuntado por pendiente tampoco sirve en IDAC1

Lo probé y falló, por una razón que vale la pena anotar: **la respuesta de ch2 a
IDAC1 no es una recta**. Lejos del cruce son 6,5 mV por código, medidos sobre
dieciséis puntos limpios; cerca del cruce se empina a más de 40. Una pendiente
medida lejos manda el salto muy lejos —en la corrida de las 04:40, con la
pendiente medida en −178 mV/código, el salto se fue al tope del actuador— y una
medida cerca exige ya estar cerca.

Queda entonces el barrido monótono, que no depende ni de la linealidad ni de una
ganancia estimada. Para que no cueste veintidós minutos se hace en dos etapas:
un grueso que ubica el cruce con pocos puntos y un fino que sólo recorre el
intervalo que quedó.

Los tres métodos y su dominio, que es lo que hay que llevarse a firmware:

| método | cuándo | por qué |
|---|---|---|
| bisección de signo | actuadores rápidos (IDAC2, IDAC3) | asientan en ms: un salto grande no deja transitorio |
| barrido en dos etapas | actuador lento (IDAC1) | pasos chicos, transitorios chicos, sesgo del mismo signo en todos los puntos |
| apuntar por pendiente | ninguno, acá | la respuesta no es lineal en el entorno que importa |

## El hallazgo que obliga a que la búsqueda sea de una sola dirección

Barrido de IDAC1 de −96 hacia arriba en pasos de 10, con IDAC2 en −180:

| IDAC1 | ch2 |
|---|---|
| −96 | +669,1 |
| −86 | +779,2 |
| −76 | +744,3 |
| −66 | +678,1 |
| −56 | +612,7 |
| −46 | +544,0 |
| −36 | +468,6 |
| −26 | +392,2 |
| −16 | +320,4 |
| −6 | +244,5 |
| +4 | **−456,8** ← cruza |

Una recta impecable de 7,6 mV por código, y el cruce localizado entre −6 y +4.

Entonces el barrido fino **volvió** a −16 para afinar, y ahí apareció lo
importante: **ch2 leyó riel**. Y siguió en el riel los once puntos siguientes,
ocho minutos, recorriendo de −16 a +4 otra vez, sin recuperarse nunca.

El mismo código, la misma configuración, y un estado completamente distinto
según de dónde se venga. Es el acople de 680 µF con su absorción dieléctrica: la
vuelta no es simétrica con la ida, y la recuperación lleva mucho más que las
constantes de tiempo que uno esperaría.

**Consecuencia para el algoritmo, y para el firmware:** la búsqueda sobre el
actuador lento tiene que ser **monótona y de una sola pasada**, y al detectar el
cruce hay que **quedarse donde se está**, no volver al punto anterior aunque ese
tuviera menor error. La precisión que se pierde no importa: quien sigue es
IDAC2, con 12,8 mV por código y ±2,3 V de recorrido sobre ch2, y le sobra para
absorber un paso entero del barrido.

Esto le da respaldo, con datos limpios, a lo que se había anotado como "el
estado depende del camino" y había quedado como no demostrado.

## Casi: ch3 centrado en −97,6 mV, y perdido por no esperar

Corrida de las 05:15. El barrido de IDAC1 terminó en +4 con ch2 en −374, y la
bisección de IDAC2 sobre ch3 dio:

| IDAC2 | ch3 |
|---|---|
| −180 | fuera |
| +180 | +1.854 riel |
| 0 | +1.854 riel |
| −90 | +1.854 riel |
| **−135** | **−97,6** ← centrado |
| −113 | +613,7 |
| −124 | −481,6 |
| −119 | −2.046,1 |
| −116 en adelante | fuera |

**IDAC2 = −135 dejó ch3 en −97,6 mV**, que es el objetivo. Y los sondeos
siguientes lo perdieron: −124 dio −481, −119 dio −2.046, y de ahí al riel.

Los números no son consistentes entre sí —de −135 a −113 ch3 sube 711 mV, pero
de −124 a −119 baja 1.565— así que no es la respuesta al código lo que se está
midiendo. Es la cadena corriéndose: el barrido de IDAC1 había terminado con un
escalón fresco sobre la referencia del pasabanda, y su cola seguía llegando
mientras IDAC2 sondeaba.

**La corrección es esperar entre niveles.** Tres constantes de tiempo después
del último movimiento del actuador lento, antes de empezar con el rápido. Es la
misma disciplina que el resto del algoritmo ya aplica al arrancar, aplicada
también en el medio.

## Cuánto dura un punto guardado: menos de lo que uno querría

Entre las 05:15 y las 05:27, con la misma placa, la misma configuración y doce
minutos de diferencia, ch0 pasó de **−1.525 mV a +364 mV**. Son 1,9 V, que a
PGA x50 corresponden a **38 mV de corrimiento referido a la entrada**.

Con IDAC0 sin tocar, en +11, ese corrimiento deja el punto guardado inservible:
el barrido de IDAC1 que doce minutos antes daba una recta limpia pasó a leer
riel en los trece puntos, de −66 a +54.

Esto acota lo que se le puede pedir al perfil, y hay que decirlo con todas las
letras en el diseño de campo:

- El perfil sirve para **saltear la caracterización** —τ y las pendientes, que
  son del cobre y no cambian—, y eso ya está verificado: ahorra diez minutos.
- El perfil **no sirve** para saltear la búsqueda del punto de trabajo. Los
  cuatro códigos dependen del offset de entrada, que se mueve decenas de
  milivolts en minutos.
- Y no basta con partir del último punto conocido: si el estado se movió lo
  suficiente, hay que volver a correr la fase 1, que es la que recentra ch0 con
  IDAC0.

El criterio para decidirlo es barato: **leer ch0 y ver si sigue dentro de su
ventana con margen**. Si no, fase 1 completa. Es una lectura de tres segundos
contra diez minutos, así que conviene siempre hacerla.

## El número que explica todos los fracasos: asentado contra instantáneo

Medido el 2026-09-13 a las 06:22, y es el dato más importante de la noche.

El último escalón del barrido de IDAC1, de −6 a +4, movió ch2 de +245 a −475: son
720 mV, o 72 mV por código, y eso es lo que lee cualquier sondeo a los 43 s.
Después se esperó a que la cadena se quedara quieta, y ch2 terminó en **−5.164**.

    respuesta instantanea   72 mV por codigo
    respuesta asentada     ~540 mV por codigo
    relacion                  unas 70 veces

Con esa relación, **un barrido que lee a los 43 s no mide la respuesta al
código: mide un transitorio que todavía no empezó.** El barrido de las 06:22 dio
una recta de 7,6 mV por código, limpia y convincente, y el punto donde terminó
—medido con la cadena ya quieta— estaba 4.700 mV más abajo de lo que esa recta
predecía.

Eso invalida, de un plumazo, todas las búsquedas de la noche sobre IDAC1: la
bisección, el barrido monótono y el apuntado por pendiente fallaron los tres por
la misma causa, y ninguna de las explicaciones que fui dando —transitorios que
tapan, no linealidad, asimetría de la vuelta— era la causa raíz. Eran síntomas
de leer antes de tiempo.

**La corrección es una sola: cada sondeo del actuador lento espera a que el tap
deje de moverse antes de leer.** Con eso la bisección vuelve a ser el método
correcto, porque cada lectura significa lo que dice. Lo que cuesta es el tiempo
de asentamiento, y de eso no se escapa por ningún camino: es física del acople
de 680 µF, no del algoritmo.

Y el número tiene una consecuencia directa para el campo: **nueve códigos de
IDAC1 barren toda la ventana del sumador**. La resolución de ese actuador es de
540 mV, así que quien tiene que hacer el trabajo fino es IDAC2, con 12,8 mV, y
después IDAC3 con 6,68.

## La regla que faltaba: parar apenas alcanza

La corrida de las 06:33 encontró **IDAC2 = +45 con ch3 en −183 mV**, centrado. Y
después siguió sondeando cinco veces más buscando el cero exacto. Al volver a
+45, el punto ya no estaba.

En una cadena donde un punto bueno no sobrevive a los sondeos siguientes,
**buscar el cero exacto es contraproducente**: cada sondeo de más es una
oportunidad de perder lo conseguido, y no compra nada, porque el nivel de abajo
tiene resolución de sobra para el resto.

Las tolerancias que quedaron, y de dónde salen:

| tap | tolerancia | por qué |
|---|---|---|
| ch2 | 800 mV | es la guarda de saturación; alcanza con estar cómodo dentro de sus ±2,4 V, y el nivel siguiente tiene ±2,3 V de recorrido |
| ch3 | 300 mV | es lo que ve el pasabajos, así que se pide más; lo que quede lo tapa IDAC3 con sus ±1,7 V |

Es la misma idea que hay detrás de todo el método: **no perseguir precisión que
la planta no puede sostener**. Cada nivel deja un residuo, y el diseño consiste
en que el residuo de cada uno entre cómodo en el recorrido del siguiente.

## La estructura correcta es anidada, y las dos escalas de tiempo la pagan

Todas las corridas de la madrugada fijaban un actuador y buscaban con el otro.
Ninguna podía funcionar, y el motivo se ve comparando dos intentos consecutivos:

- Con IDAC2 pre-posicionado en **−180**, la búsqueda de IDAC1 dejaba ch2 en
  +772 mV. Para que ch3 entrara en ventana con PGAout x4 hacía falta
  |ch2| < 520, o sea unos sesenta códigos más de IDAC2 — y −180 era su tope.
- Con el tope liberado a **−255**, la misma búsqueda dejaba ch2 clavado por
  **debajo** en los dos extremos de IDAC1. El pre-posicionamiento se pasaba.

No existe un valor de IDAC2 que sirva para pre-posicionar, porque el correcto
depende de dónde quede IDAC1, y al revés. **Lo que determina el estado es el
par, no cada uno por separado.**

La estructura que corresponde es anidada, y sale barata justamente porque los dos
actuadores cuestan cosas muy distintas:

| actuador | costo por sondeo | por qué |
|---|---|---|
| IDAC1 | minutos | pasa por el pasabanda y hay que esperar el asentamiento |
| IDAC2 | 6 segundos | el sumador y PGAout asientan en milisegundos |

Así que por cada código de IDAC1 —pocos y caros— se recorre IDAC2 entero
—muchos y baratos—, y se corta apenas ch3 aparece dentro de su ventana. Nueve
puntos de IDAC1 por diecisiete de IDAC2 son unos diez minutos, contra los veinte
que costaba una búsqueda que además no podía encontrar nada.

## Una lectura válida no es una lectura buena

Bug propio, y vale anotarlo porque es la tercera variante del mismo error en este
proyecto. La búsqueda anidada aceptó **ch3 = +1.854,8 mV como «DENTRO»** y siguió
adelante sobre un tap clavado.

El motivo: `lectura_valida` comprueba que el valor caiga en la ventana del ADC,
que son ±2,4 V. El riel de ch3 está en +1.855, cómodo adentro de esa ventana. Y
`clavado`, que sí mira el pico a pico, exige además estar cerca de un borde de
la ventana del ADC, y +1.855 no lo está.

Los rieles medidos de cada tap, que no coinciden con la ventana del ADC:

| tap | riel superior |
|---|---|
| ch2 (OPA_SUMo) | +1.882 mV |
| ch3 (SUMo) | +1.855 mV |
| ch4 (LPo) | +2.300 mV |

La corrección no fue agregar nada: la tolerancia ya venía como parámetro de la
función y no se estaba usando. Ahora un candidato se acepta sólo si además está
dentro de esa tolerancia, que para ch3 son 300 mV.

La regla general, que ya estaba escrita para IDAC3 y para el sumador y que hay
que aplicar en todos lados: **que el ADC pueda leer un número no quiere decir que
la etapa esté viva.** Los criterios en orden de confiabilidad son que la etapa
responda a su actuador, que tenga ruido propio, y recién último que la lectura
caiga en el rango del conversor.
