# Autocalibración GEO — sesión del 2026-09-11

Reemplaza al handoff del 2026-09-10 por la tarde en todo lo que lo contradiga.
Todo lo de acá está medido en placa este día, con IDAC2 en 11,8 kΩ e IDAC3 en
6,68 kΩ. Los archivos de datos están en `lab/calibracion_nueva/`.

---

## 1. El hito: el punto objetivo existe, es alcanzable y es estable

Esto era lo que estaba en duda al empezar, porque el historial declaraba 166
PASS y ninguno sobrevivía a una re-puntuación honesta.

**Alcanzable.** En la corrida `dos_fases_calibrate-gains_20260911_180304` la
cadena llegó al estado objetivo completo en x4, con los cinco taps vivos y
dentro de rango a la vez: `ch2=-285  ch3=-286  ch4=-444`.

**Estable.** Con la cadena asentada y los cuatro actuadores congelados, LPo se
quedó **seis minutos en +209 mV con 72 mV de deriva total**
(`vigilar_punto_x4_20260911_182104.csv`). Y PGAgain a PGA x50 se quedó cinco
minutos en −965 mV con ±10 mV (`vigilar_punto_pga50_out1_20260911_184829.csv`).
La cadena no deriva sola.

**Matiz importante, agregado al final de la noche.** Esa estabilidad es de
*magnitud*, no de equilibrio. Pasado el registro por `ajustar_deriva_lenta.py`,
los seis minutos son la décima parte de la constante de tiempo del movimiento
que se ve: la excursión es chica pero es una rampa que no llegó a ninguna
asíntota. Sirve para decir que el punto no se desmorona en segundos, que era la
duda original. No sirve para afirmar que la cadena esté en reposo. Ver §2.10.

Lo que falta es que el algoritmo aterrice ahí de forma repetible, y el obstáculo
que queda está identificado y medido en §2.10: no es del algoritmo, es del
hardware.

---

## 2. La causa raíz, y la cadena de errores que la tapaba

### 2.1 El lazo cerraba sobre un transitorio

La fase 2 identificaba y corregía mientras el pasabanda todavía se estaba
asentando. Evidencia directa, durante el ABBA de IDAC2 en x4:

| t (s) | ch2 (mV) |
|---|---|
| 312,6 | −353,8 |
| 319,7 | −417,3 |
| 326,7 | −563,5 |

Son 13 mV/s. Multiplicado por PGAout x4 y por la etapa LP (×9,07) son 3.700 mV
en ocho segundos sobre LPo. Y eso es exactamente lo que pasaba: el lazo cerraba,
la foto daba los cinco taps vivos, y ocho segundos después LPo estaba en −3.916
con el pico a pico colapsado de 17.547 a 381 µV.

El lazo de IDAC3 no rompía nada. Llegaba cuando ya estaba roto.

**El ABBA no protege de esto:** cancela una deriva *lineal*, y la cola del
pasabanda es exponencial con τ entre 30,9 y 38,5 s según la corrida.

### 2.2 De dónde salía el transitorio

De la propia fase 1. Cuando movía sólo IDAC1, esperaba `ABBA_ESPERA_S` = 1,5 s,
con un comentario en el código que afirmaba que mover la referencia del
pasabanda no excita su recuperación lenta.

**Eso es falso.** IDAC1 *es* la referencia del pasabanda, cuyo polo dominante
son los 680 µF de acople. Moverlo arranca la cola entera. La fase 1 daba el
punto por bueno y le entregaba a la fase 2 una cadena moviéndose a 112 mV/s.

Corregido: ahora espera el pasabanda igual que ya hacía con IDAC0. La deriva
inicial de fase 2 bajó de 112 a 36,7 mV/s.

### 2.3 Esperar no congela la cadena

Con la compuerta puesta, el lazo dejaba ch2 en su consigna (−264 mV) y *después*
esperaba a que se aquietara. Durante esa espera la misma deriva que estaba
midiendo se llevó ch2 hasta **+1.882 mV**.

Corregido: primero se espera, después se apunta, y se verifica que siga ahí.

### 2.4 Newton no sirve sobre una ventana de diez códigos

Un código de IDAC2 mueve LPo por la ganancia entera de la cadena:

| G | un código sobre LPo | códigos que sirven |
|---|---|---|
| 4 | 472 mV | unos 10 |
| 16 | 1.887 mV | unos 2,5 |
| 24 | 2.830 mV | menos de 2 |

Un salto de Newton sobre esa pendiente sale disparado y arrastra a ch2: lo dejó
en −5.175 mV. Reemplazado por enumeración acotada a ±15 códigos alrededor de la
consigna de ch2.

### 2.5 El lazo usaba la ganancia equivocada

Medido con esperas de cinco τ (`ganancia_regimen_idac2_20260911_194417.csv`):

| IDAC2 | inmediato (1,5 s) | régimen (5τ) |
|---|---|---|
| −120 | +493,7 mV | +896,3 mV |
| −60 | +1.620,7 mV | +1.637,0 mV |
| **pendiente** | **18,78 mV/cód** | **12,35 mV/cód** |

El ABBA mide la inmediata. La cadena termina donde dice la de régimen. Newton
con la inmediata da un paso 34 % más chico del necesario, la cadena se relaja de
vuelta, y el lazo se queda corto hasta agotar iteraciones.

Corregido: `RAZON_REGIMEN_IDAC2 = 12,345/18,783` convierte una en la otra.

### 2.6 El barrido tenía el mismo defecto que el lazo

Corregido el lazo, el barrido fino **encontró la solución por primera vez**:
IDAC2 en −221, a sólo cuatro códigos de la consigna, dejando LPo en +1.478 mV,
dentro de rango. Y la foto inmediatamente posterior dio `ch2=-5169 ch3=-5052
ch4=+2307`, todo clavado.

Porque el barrido sostenía cada código 1,5 s. Mapeaba la respuesta inmediata y
elegía un código que la cadena no iba a conservar. Es el mismo error que 2.5,
sólo que en otro lugar del código.

Corregido: el barrido espera **tres τ por código**. Eso obliga a achicar la
ventana de ±15 a ±3, porque quince códigos con esperas largas serían cuarenta
minutos por ganancia. Se puede achicar sin perder nada, porque el lazo previo ya
deja ch2 en su consigna de régimen **verificada**, así que el código que sirve
está al lado.

Lo que hace válido todo esto: **la etapa LP responde en milisegundos, así que
LPo es una función estática de ch2.** No hay dos dinámicas que perseguir. Lo
único que hay que esperar es que ch2 llegue a su valor final.

### 2.7 Iterar a ciegas encima una cola sobre otra

Aun con la pendiente de régimen puesta, el lazo dejaba ch2 a **258 mV** de la
consigna, más de lo que el barrido posterior puede absorber.

La causa es estructural, no de sintonía. El lazo de Newton hacía decenas de
movimientos chicos con esperas de segundos, y **cada movimiento arranca una cola
de treinta a cincuenta segundos**. Cuando el lazo terminaba, la suma de todas
esas colas seguía viva y se llevaba el punto puesto.

Con la pendiente de régimen medida no hace falta iterar a ciegas.
`apuntar_ch2_de_una` lee el ch2 ya asentado, calcula el salto entero y lo aplica **una sola
vez**. Queda una cola pendiente en vez de diez encimadas, y el llamador la espera
antes de volver a mirar. `estabilizar_y_apuntar_ch2` alterna esperar y saltar
hasta cinco veces, que con un salto bien calculado debería sobrar.

### 2.8 Cómo detectar un tap saturado, de verdad

Un tap pegado se venía detectando por su valor (fuera de ventana) o por su ruido
(pico a pico bajo). Apareció un caso que burla las dos: ch2 en **+1.885 mV**,
cómodamente dentro de la ventana válida, con pico a pico de 114 µV, o sea bajo
pero no nulo. Ante ocho códigos de IDAC2 se movió **0,3 mV** en vez de los 150
que corresponden. Estaba saturado, a 205 mV del riel.

La prueba que no admite discusión es la **respuesta al propio actuador**. La
pendiente la fija una resistencia y no puede desaparecer, así que una
identificación que devuelve una fracción de la nominal no midió una pendiente:
midió un tap pegado.

Implementado como `pendiente_idac2_plausible`, que acepta entre un cuarto y
cuatro veces la nominal. Fuera de eso se rescata ch2 y se vuelve a medir una
sola vez; si sigue sin responder se sigue con la constante de respaldo y se
informa. **Nunca se aborta la corrida entera por esto**, que es lo que hacía.

Vale la pena quedarse con la jerarquía: el valor y el ruido son indicios, la
falta de respuesta es prueba.

### 2.9 La deriva lenta, y de dónde salía

Lo que sigue es el camino que llevó a §2.10 y queda como registro. La conclusión
de esta sección quedó **explicada** por la de arriba.

Con los nueve arreglos puestos, el barrido en régimen visitó siete códigos
alrededor de −247, esperando tres τ en cada uno:

| IDAC2 | LPo (mV) | t (s) |
|---|---|---|
| −247 | −1.128 | 656 |
| −246 | −1.152 | 739 |
| −248 | −1.177 | 821 |
| −245 | −1.203 | 903 |
| −249 | −1.229 | 986 |
| −244 | −1.258 | 1.069 |
| −250 | −1.285 | 1.151 |

El código sube y baja alternando, pero **LPo sólo decrece**, unos 25 mV en cada
visita, unos 82 s aparte. No está respondiendo al código: está midiendo el paso
del tiempo. Y el efecto real de un código resultó **veinte veces menor** que el
que predice multiplicar las ganancias de cada etapa (24 mV observados contra 448
calculados).

Peor todavía: entre la foto anterior al barrido y la posterior, **con el mismo
código −247**, ch2 se fue de −288 a −4.337 mV en 758 s. Son 5,3 mV/s sostenidos
durante doce minutos.

Es decir: existe una dinámica de **varios minutos** que las esperas de tres τ no
cubren, porque τ son cincuenta segundos. Mientras esa dinámica no se caracterice,
ningún lazo puede cerrar, porque cualquier punto que encuentre se evapora antes
de que termine el paso siguiente.

**Confirmado en §2.10:** era el IDAC quedándose sin compliance cerca del fondo
de escala. La observación pasiva que se había dejado corriendo con IDAC2 en −247
no sirvió, porque ahí ch2 estaba fuera de rango y sus lecturas están comprimidas.
La que contestó fue la comparación entre dos códigos que **sí** dejan ch2 dentro
de rango, con `comparar_deriva_por_codigo.py`.

### 2.10 El límite real: IDAC2 se vuelve inestable pasados 180 códigos

**Este es el hallazgo que cierra la sesión y el que manda sobre todo lo demás.**

Medido con `comparar_deriva_por_codigo.py`, siete a diez minutos por código, con
todo lo demás congelado y siempre con ch2 dentro de rango:

| IDAC2, en módulo | deriva de OPA_SUMo |
|---|---|
| 120 | −0,01 mV/min |
| 140 | −0,10 mV/min |
| 180 | +0,00 mV/min |
| 210 | **+7,08 mV/min** |
| 240 | **+4,81 mV/min** |

El codo está entre 180 y 210, y es **abrupto**: de quieto a inservible entre dos
códigos vecinos. Es **reversible**, al volver a los códigos bajos la deriva
desaparece. Y la **ganancia incremental también se cae**: entre 120 y 240 son
4,57 mV/código contra los 12,35 de la zona buena.

Sobre los diez minutos que dura una calibración, 7 mV/min son 70 mV en ch2, que
amplificados por PGAout y la etapa LP son más de dos volts en LPo. La
calibración entera. Es la magnitud exacta de todas las fallas de la noche.

#### El mecanismo NO se sabe, y conviene no inventarlo

Se probaron dos explicaciones y las dos se cayeron:

- **Autocalentamiento**: no. Sería gradual y proporcional al cuadrado de la
  corriente, no un salto entre dos códigos vecinos. Además la disipación en
  juego son decenas de microwatts.
- **Saturación del sumador**: no. En el código malo ch2 estaba en +1.337 mV y en
  el bueno en +1.885, o sea **más lejos de su riel justo cuando peor derivaba**.
- **Carga de una referencia compartida**: tampoco. Se miró si ch0 y ch1 derivaban
  junto con ch2 y derivan parecido en los códigos buenos, así que ese movimiento
  es ruido propio de esos dos taps y no arrastre.

Averiguarlo pide un osciloscopio sobre el nodo del IDAC, y es tarea de
laboratorio. **Para el algoritmo alcanza con no ir ahí.**

#### Qué se hizo con esto

`IDAC2_MAX_CONFIABLE = 160`, y el optimizador de fase 1 cuenta el recurso de
IDAC2 contra ese número en vez de contra 255. Pasarse deja de ser "casi al
límite" y pasa a ser infactible, igual que pasarse de 255.

Sobre el reposo sintético el optimizador respeta la restricción y deja a IDAC2
entre el 3 % y el 20 % de su zona útil. **Eso no prueba que resuelva el caso
real**, porque la fase 1 en placa usa pendientes medidas y no las del modelo de
respaldo. Falta verificarlo en la placa.

#### La consecuencia de diseño

La cadena necesitaba unos 215 códigos para traer ch2 dentro de rango a PGA x50,
o sea que el punto de trabajo obligado caía justo en la zona mala. La salida es
repartir: IDAC0 tiene entre 197 y 250 mV/código sobre ch2, autoridad de sobra
para dejarlo cerca de la consigna y que IDAC2 trabaje por debajo de 160.

Es el mismo remedio que hace falta para pasar de x24 (§5). Dos límites que
parecían distintos se resuelven igual.

#### La idea de subir el rango del IDAC a miliamperes

Propuesta de Elías. Separada en dos versiones, porque una no sirve:

- **Subir sólo el rango**: no. Multiplica los mV por código, y la resolución ya
  es el cuello de botella: en x24 la ventana útil mide menos de dos códigos.
- **Subir el rango y bajar Rset en la misma proporción**: tiene sentido. Misma
  autoridad en volts y misma resolución, pero con una corriente de señal mucho
  mayor frente a cualquier fuga del nodo. La disipación pasa de once a ochenta y
  ocho microwatts, o sea nada.

Pero sería cambiar hardware sobre una hipótesis sin mecanismo confirmado. Antes
habría que saber si la deriva sigue al **módulo** de la corriente, que es lo que
esa idea atacaría.

**Esa prueba se intentó y no se puede hacer así.** Se corrieron ±210 códigos con
PGA en x1 y el resultado parecía nítido: deriva sólo con códigos negativos. Era
falso. En los bloques negativos las treinta lecturas por bloque estaban **fuera
de rango**, o sea comprimidas contra el borde, y la pendiente sacada de ahí no
mide nada. El mismo error que arruinó media sesión, otra vez.

Y hay una razón de fondo por la que la pregunta no se puede contestar así: el
recorrido de ±210 códigos abarca 5,2 V y la ventana de medición son 4,8. **No
existe un punto de trabajo donde los dos signos queden dentro de rango.** Para
comparar signos hace falta otro método: por ejemplo bajar la ganancia de PGAout
para achicar lo que el tap recorre, o medir el nodo del IDAC directamente con
osciloscopio en vez de a través de la cadena.

`comparar_deriva_por_codigo.py` ya no permite repetir el error: descarta las
lecturas inválidas, informa cuántas descartó, y si un extremo se queda sin datos
válidos dice que no se puede comparar en vez de devolver un número.

### 2.11 Con el límite puesto, la consigna NO se alcanza. Cuánto falta

Aplicar el límite reveló el resultado que estaba tapado. Medido en placa el
2026-09-12 con todos los arreglos puestos, PGA x50 y PGAout x4:

- ch2 quedó en **+634 mV**, la consigna era **+38 mV**.
- IDAC2 en **−160**, su límite útil, pidiendo 48 códigos más que no tiene.
- **Faltan unos 600 mV**, o sea unos 48 códigos de recorrido utilizable.

Esto no es una falla del algoritmo. Es la medida de cuánto hardware falta, y es
la primera vez en toda la sesión que el número se puede leer, porque antes el
programa se pasaba al fondo de escala y "conseguía" un punto que después se
evaporaba.

**Un detalle de implementación que importa.** El límite había que ponerlo en el
punto de escritura, no en el planificador. Puesto sólo en `optimizar_fase1`, la
fase 2 lo ignoró por completo y dejó IDAC2 en −255: el lazo, la bisección de
rescate y el barrido escriben códigos por su cuenta. Ahora pasa todo por
`set_code`, y hay una prueba que recorre seis caminos verificando que ninguno lo
evade.

Y cuando el actuador ya no puede, el bloque de apuntado **corta y lo dice**
(`consigna_inalcanzable`) en vez de reintentar cinco veces el mismo salto
imposible.

#### Qué hacer con esos 600 mV

Dos caminos, y conviene medir el primero antes de tocar nada:

1. **Repartir con IDAC0**, que tiene entre 197 y 250 mV/código sobre ch2. Tres
   códigos suyos cubren el déficit. Ya está la restricción en `optimizar_fase1`,
   pero evidentemente no está eligiendo con ese criterio: hay que revisar el
   término de recurso para que ch2 pese de verdad.
2. **Cambiar el hardware.** La conversación del lunes. Ver la nota sobre subir
   el rango del IDAC más abajo.

El camino 1 es gratis y hay que agotarlo primero.

### 2.12 El reparto con IDAC1, y el salto de 25x que quedó sin explicar

Con IDAC2 acotado a su zona útil, la fase 2 necesita otro actuador para traer
ch2 a su alcance. Se probó con IDAC0 y se descartó: su paso sobre ch2 son 248 mV
y la ventana útil de ch2 es más angosta que eso, así que un solo código lo saca
de rango. IDAC1 mueve unos 8 mV por código y llega al mismo lado, así que es el
correcto.

**La pendiente real de IDAC1 sobre ch2 es −8,3 mV/código**, medida tres veces en
placa (−8,50, −8,45, −8,16). El modelo derivado la venía dando entre −3,0 y
−25,8: un factor ocho de dispersión. Conviene fijar la constante en el valor
medido y dejar de derivarla.

De ahí salió una pieza que vale la pena conservar: **el reparto sondea antes de
saltar.** El primer movimiento es una sonda de 40 códigos que mide la pendiente
real en ese punto de trabajo, y los saltos siguientes usan ese número. Hay una
prueba que le da al algoritmo un modelo con el **signo invertido** y exige que
igual cierre.

**Revertir no restaura la cadena.** Se comprobó dos veces: tras devolver el
código a su lugar, ch2 siguió fuera de rango. Es la absorción dieléctrica del
acople de 680 µF, ya documentada el 2026-09-02. Como el error no es reversible,
la protección no puede ser la corrección posterior sino la prudencia previa: los
repartos van de a **medio paso**, que no puede sobrepasar ni con la pendiente
errada al doble, y converge igual (807 → 516 → 292 mV en la corrida real).

#### El estado depende del CAMINO, no sólo de los códigos

Intentando acotar el salto se hizo un barrido fino de IDAC1 en el punto exacto
donde ocurrió (PGA x50, PGAout x4, IDAC0 +11, IDAC2 −160). Los dos extremos del
tramo, IDAC1 en −70 y en −10, dieron ch2 **clavado en −5.173 mV**. Pero durante
la calibración, con el valor intermedio −50 y los mismos códigos en todo lo
demás, ch2 estaba en **+620 mV**.

Un sistema sin memoria no puede hacer eso. Es la firma de la **absorción
dieléctrica** del acople de 680 µF, ya observada el 2026-09-02 con constantes de
decenas de segundos.

La consecuencia es fuerte y conviene tenerla presente en toda la tesis:

- **Un punto de trabajo no queda definido por los cuatro códigos.** Depende
  además de por dónde se llegó y de cuánto hace. Dos corridas con los mismos
  códigos pueden estar en estados distintos.
- Por eso las pendientes derivadas dieron entre −3,0 y −25,8 mV/código para el
  mismo par de nodos: no estaban midiendo mal, estaban midiendo estados
  distintos.
- Y por eso reponer un código no repone la cadena, que es lo que hizo inútil la
  estrategia de revertir.

Esto también explica por qué la calibración tiene que hacerse **llegando siempre
por el mismo camino**, y por qué una campaña de arranques en frío es la única
forma honesta de medir su repetibilidad.

#### Lo que quedó sin explicar

Con el déficit ya en 292 mV, un movimiento de 18 códigos —previsto en −147 mV con
una pendiente medida tres veces— llevó ch2 a **−5.172 mV**. Son unos −200
mV/código, **veinticinco veces** la pendiente medida minutos antes con
movimientos de 40 y 31 códigos.

No hay explicación con los datos disponibles. Descartado que sea el cruce por
cero de IDAC1, porque un movimiento anterior lo cruzó y midió −8,16 normal. Y
descartado que sea la inestabilidad de IDAC2, que está en −160, dentro de su
zona útil.

**Esto es lo próximo a mirar, y pide banco:** osciloscopio sobre el nodo de
IDAC1 y sobre el del sumador, moviendo IDAC1 de a pocos códigos alrededor de
+21..+39 con IDAC2 en −160, para ver qué salta. Desde el banco de medida
integrado no se puede: la lectura se satura antes de mostrar lo que pasa.

---

## 3. Refutado hoy, con evidencia

| Se creía | Es | Cómo se supo |
|---|---|---|
| El punto se pierde por el lazo de IDAC3 | Se pierde antes, solo | Vigilancia con los IDAC congelados |
| El punto no es un equilibrio | Sí lo es | Seis minutos quieto en +209 mV |
| La cadena deriva sola a x50 | No | PGAgain ±10 mV en cinco minutos |
| Un tap sin ruido está clavado | No | Con los IDAC en cero, ch0 y ch2 dieron −302 mV con pp de 200 µV: silenciosos y centrados |
| IDAC3 puede centrar LPo | No | Su recorrido son ±751 mV medidos; IDAC2 tiene de sobra |
| Mover IDAC1 no excita la cola lenta | La excita entera | Es la referencia del pasabanda |
| El efecto de IDAC2 se desvanece | No, sobrevive el 66 % | Medición de régimen |
| A x50 no hay IDAC2 que sirva | No se puede afirmar | El barrido usaba pasos de 60 códigos, seis ventanas por paso |

Las dos últimas filas son hipótesis propias que la medición desmintió. Quedan
acá para que nadie las reviva.

---

## 4. Cambios en el código, todos con prueba

`src/interfaces/python/autocalibracion_dos_fases.py`, 25 pruebas que corren en
dos segundos con `--autotest`, sin hardware.

1. **`esperar_sin_deriva`** — compuerta que exige que el tap se haya aquietado
   antes de identificar nada. Tolerancia escalada por la ganancia, porque lo que
   importa no es cuánto se mueve ch2 sino cuánto se mueve LPo. Paciencia atada a
   la τ medida, no un número fijo.
2. **Tres lecturas quietas seguidas**, no una. La cadena tiene más de un polo y
   la derivada puede cruzar por cero mientras el sistema sigue viajando. Se
   vieron las dos firmas: una lectura de exactamente +0,00 mV/s, y la deriva
   subiendo de 36 a 57 mV/s, que una exponencial simple no puede hacer.
3. **Corte cuando el tap se va de rango** dentro del lazo de espera. Sin esto
   gastó 208 s mirando un ch2 clavado en −5.177 mV que ni se movía.
4. **`estabilizar_y_apuntar_ch2`** — alterna esperar y reapuntar hasta que la
   espera ya no mueva el punto.
5. **`barrer_idac2_por_lpo`** — enumeración acotada en vez de Newton.
6. **`pendiente_regimen_idac2`** — convierte la pendiente del ABBA a la de
   régimen.
7. **`apuntar_ch2_de_una`** — un solo salto calculado, en vez de un lazo de
   Newton que encima una cola sobre otra.
8. **`pendiente_idac2_plausible`** — detecta un tap saturado por su falta de
   respuesta al actuador, y rescata en vez de abortar la corrida.
9. **Fase 1 espera el pasabanda cuando mueve IDAC1.**
10. **Detector de riel corregido** en `escala_banco.py`: exige poco ruido *y*
   estar contra un borde de la ventana lineal. Antes bastaba el ruido bajo.
11. **Identificación de IDAC3** con 48 códigos en vez de 8, más control de
   plausibilidad. `PASO_IDAC3_CH4_MV` de 4,3 a 6,44 (el 4,3 era con 10 kΩ).

### Scripts nuevos

| archivo | para qué |
|---|---|
| `vigilar_punto.py` | Arma un punto y lo mira sin tocar nada. Es lo que separó "la planta se va sola" de "algo que hago la voltea" |
| `medir_ganancia_regimen_idac2.py` | Inmediata contra régimen, con esperas de cinco τ |
| `medir_signo_idac3.py` | Autoridad de IDAC3 con excitación de 400 códigos |
| `alcance_por_ganancia.py` | Techo de ganancia por resolución; acepta la pendiente de IDAC3 como argumento |

---

## 5. Los dos techos

**Por resolución: x24.** El salto de IDAC2 sobre LPo tiene que entrar en el
recorrido de IDAC3, que es el único que rellena entre código y código. Con la
nominal de IDAC3 (6,44 mV/cód) llega hasta x24; con la medida (2,95, pero tomada
con LPo contra el riel y probablemente subestimada) sólo hasta x8. Correr
`alcance_por_ganancia.py` con las dos.

Para x32 y más haría falta combinar IDAC1 y IDAC2 como vernier. Es posible, los
pasos de 8,2 y 13 mV dan resolución efectiva de décimas, pero es otro desarrollo
y hay que resolverlo enumerando en el modelo, no en la placa.

**Por recorrido: delgado.** Con IDAC2 en cero y PGA x50, ch2 queda en +2.108 mV,
fuera de rango. Bajarlo a la consigna pide unos 215 de los 255 códigos. Quedan 40
de margen, un 16 %. Alcanza para esta placa; es poco para absorber variación
entre placas o temperatura.

---

## 6. Lo que queda por hacer

0. **Explicar el salto de 25× de §2.12.** Es lo primero y necesita banco, no
   código. Un movimiento de 18 códigos de IDAC1 movió ch2 veinticinco veces más
   de lo que la pendiente medida tres veces predecía. Mientras eso pase, ningún
   lazo puede confiar en su propio actuador. Osciloscopio sobre el nodo de IDAC1
   y el del sumador; desde el banco integrado la lectura se satura antes de
   mostrarlo.
1. **Repartir el esfuerzo entre IDAC0 e IDAC2 (§2.10).** Es lo primero y lo que
   manda sobre todo lo demás. Hoy la fase 1 elige IDAC0 mirando sólo a ch0, y
   eso deja a IDAC2 con 215 códigos de trabajo, o sea justo en la zona donde
   pierde compliance, deriva 3 mV/min y su ganancia cae a un tercio. La fase 1
   tiene que elegir IDAC0 e IDAC1 de modo que ch2 quede cerca de su consigna y
   IDAC2 pueda quedarse por debajo de la mitad de su recorrido.
   Hay un `optimizar_fase1` que ya plantea el problema como optimización con
   restricciones; hay que agregarle esta restricción y darle a ch2 el peso que
   corresponde. Verificar después con `comparar_deriva_por_codigo.py` que el
   punto elegido deriva menos de 0,1 mV/min.
2. **Validar x4 y x24 de punta a punta**, después de lo anterior.
3. **Arreglar la identificación de IDAC1.** Está rota de origen y no se tocó.
   El ABBA usa deltas de 2 y 4 códigos y espera 1,5 s sobre **BPo, que es la
   salida del pasabanda**. Después de 1,5 s el nodo recorrió el 4 % del escalón.
   Encima 2 códigos son unos 5 mV sobre un tap cuyo pico a pico son 6: la
   relación señal a ruido es menor que uno. Resultado: +4,464, +2,280 y +0,831
   mV/código en tres corridas del mismo día.
   Tres salidas: esperar 3τ por transición (quince minutos, correcto y carísimo);
   esperar 1τ y corregir por la fracción asentada, que se conoce porque τ ya se
   mide; o no identificarla, porque la fija una resistencia de 15 kΩ.
4. **Repetir la medición de IDAC3 con LPo en rango.** La única limpia se tomó
   con LPo contra el riel, donde el amplificador está saturado y la pendiente
   aparente queda comprimida. Usar PGA x1 con PGAout x4, que es donde LPo
   descansa en +209 mV. El script ya tiene los argumentos.
5. **Después: campaña de arranques en frío** con `endurance_arranque_frio.py`,
   ganancias por prioridad 24, 16, 32, 50, 8, 4, 2, 1.
6. **Al final: pasar el algoritmo a C** dentro del PSoC. Decisión de Elías:
   Python primero, C último.

### Pendiente de firmware, anotado y no hecho

El PSoC **no debe autocalibrar al bootear**. Tiene que esperar el pedido
explícito del operador.

---

## 7. Advertencias para quien siga

- **Nunca sacar una pendiente de un tap fuera de rango o clavado.** Es el error
  que más veces mordió hoy, y en las dos direcciones: identificar sobre un tap
  muerto, y meter puntos clavados en un ajuste por mínimos cuadrados, que aplana
  la pendiente hacia cero. El propio `medir_ganancia_regimen_idac2.py` informó
  4,8 mV/código en su primera versión por eso; los puntos vivos daban 12,3.
- **Un barrido de diagnóstico con paso grueso no ve una ventana angosta.** Con
  pasos de 60 códigos se concluyó que a x50 no había solución. El paso saltaba
  seis ventanas.
- **Congelar y mirar.** Cuando un punto se pierde, congelar los actuadores y
  observar varios minutos separa la planta del algoritmo en una sola medición.
  Ninguna cantidad de lectura de código lo hubiera separado.
- La etapa LP es de segundo orden pero sus constantes son de milisegundos
  (150 k × 47 nF = 7 ms). No explica nada en la escala de segundos. Lo que manda
  ahí son los 680 µF del pasabanda.

---

## 8. Limitaciones que hay que decir en la tesis

- El `ToggleReset` no corta la alimentación, así que la rampa de la fuente queda
  sin probar.
- Todo esto es **un solo nodo** y **una sola placa**.
- El margen de recorrido de IDAC2 es del 16 %. No hay dato de cuánto se lo come
  la temperatura.
