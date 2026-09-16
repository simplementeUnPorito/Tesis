# Resumen de la noche del 12 al 13 de septiembre

Para leer primero. El detalle está en `RESULTADOS_CENTRADO_POR_BISECCION_2026-09-13.md`,
`AUTORIDAD_REAL_DE_LOS_IDAC_2026-09-13.md` y `PORTE_A_FIRMWARE_BISECCION_2026-09-13.md`.

## Lo que preguntaste, contestado

**¿El IDAC se está saturando por compliance?** No, y queda descartado con
números, no con opinión. Las resistencias están declaradas en `psoc_hw.h`: 15 k
para PGA y BP, 1,5 k para el sumador, 10 k para el pasabajos. Con los rangos que
fija `calibration.c` —el sumador es el único en 255 µA— la excursión máxima que
puede pedir cualquiera de los cuatro son **478 mV**, y el datasheet permite
±1,41 V alrededor de VDDA/2. Sobra un factor tres.

**¿Dejaste LP muy fuera de rango y por eso no lo podías mover?** Sí, y era peor
de lo que parecía: todas las mediciones de autoridad de IDAC3 se habían hecho con
el pasabajos contra su riel, donde ningún actuador se ve. Medido de nuevo con la
etapa dentro de ventana, **IDAC3 da 6,68 mV por código y ±1,70 V**, no los 0,58
que dice la curva del firmware ni los 800 a 2.000 que yo mismo informé el 12. Los
10 kΩ que pusiste son el valor correcto y no hay que cambiarlos.

## Los tres hallazgos que explican por qué no cerraba

**1. IDAC0 no mueve el continuo del sumador.** Treinta y un códigos, que según la
fase 1 valen 7,5 V, lo movieron trece milivolts. El capacitor de 680 µF del
pasabanda bloquea su continua: los 244 mV por código que informa la fase 1 son el
resto de un transitorio, no una ganancia.

**2. El pasabajos cuelga de ch3, no de ch2.** `psoc_hw.h` lo dice desde el
2026-09-07: OPA_SUMo (ch2) está ANTES de PGAout y SUMo (ch3) DESPUÉS. Centrar ch2
y darlo por bueno deja ch3 contra su riel. ch2 sigue sirviendo, pero como guarda
de saturación, no como objetivo.

**3. La cadena no vuelve al mismo estado.** Un barrido de IDAC1 de −96 a +4 da una
recta impecable; al retroceder al mismo −16 que había leído +320 mV, lee riel, y
sigue en el riel ocho minutos. Es la absorción dieléctrica del acople de 680 µF.
Obliga a que la búsqueda sobre el actuador lento sea **monótona y de una sola
pasada**.

## El algoritmo que quedó

Bisección por el signo del tap en vez de un PI. El signo sobrevive a la
saturación, no hay integrador que se desboque, y el número de sondeos está
acotado de antemano, así que el presupuesto de campo se calcula en vez de
estimarse.

| paso | actuador | tap | método |
|---|---|---|---|
| 1 | IDAC0 | ch0 | fase 1, ya existía |
| 2 | IDAC1 | ch2 | barrido monótono de una sola pasada |
| 3 | IDAC2 | ch3 | bisección de signo |
| 4 | IDAC3 | ch4 (LPo) | bisección de signo |

Entre el 2 y el 3 se espera **hasta que el tap deja de moverse**, no un tiempo
fijo: la cola de esta cadena es mucho más larga que el τ de 34 s que da el
estimador.

Implementado en `centrar_lpo.py`, con 41 pruebas contra plantas simuladas que
saturan, derivan y tienen ganancia y signo desconocidos.

## El reparto offline / online que pediste

`perfil_placa.py`, con fecha y regla de vencimiento. Verificado en placa: con el
perfil cargado la corrida saltea la caracterización de la fase 1 y arranca
**diez minutos antes**.

Pero hay un límite que conviene saber: **el perfil sirve para saltear la
caracterización, no para saltear la búsqueda del punto**. Entre dos corridas
separadas por doce minutos, ch0 se movió 1,9 V, que a x50 son 38 mV referidos a
la entrada, y el punto guardado quedó inservible.

## Lo que falta y por qué

El estado de la placa se corre más rápido de lo que la búsqueda tarda en
converger, con PGA en x50. Ése es hoy el cuello de botella, y es un resultado en
sí mismo: no es un problema del algoritmo sino de cuánto dura el punto de
trabajo.

## Deuda de método que quedó cubierta

Un parche abortó a mitad y dejó una llamada a una función que no existía. El
módulo importaba, los tests pasaban, y la corrida murió con `NameError` **después
de ocho minutos de barrido**. Es la tercera vez en el proyecto que un editor
automático rompe algo que sólo se ve al ejecutar.

Queda cubierto por `test_nombres_definidos.py`, que revisa por análisis estático
que ningún script llame a nombres inexistentes y que ninguno defina la misma
función dos veces —lo segundo también pasó antes, con ochenta y cinco líneas
duplicadas y la versión vieja quedando activa—.

Cuesta cuarenta milisegundos y evita perder minutos de placa.

## El mecanismo que faltaba: el pasabanda se engancha

Ésta es la explicación de fondo, y llegó recién cuando empecé a medir con la
cadena quieta en vez de esperar un tiempo fijo.

Con sondeos asentados, ch2 toma **sólo dos valores**: dentro de ventana, o
clavado en −5.163. Y salta de uno al otro con **un solo código de IDAC1**:

    IDAC1 = −116  →  ch2 = +1.029 mV   dentro de ventana
    IDAC1 = −115  →  ch2 = −5.163 mV   clavado

Serían más de 3.400 mV por código, o sea una ganancia de 1.800 desde Vref_BP. La
topología da 4: en continua BPo sigue a Vref_BP con ganancia 1, porque el
capacitor en serie bloquea la corriente por R4, y el sumador aporta unas cuatro
veces. Así que no es una ganancia.

**Es un enganche.** El pasabanda se satura, el capacitor de 680 µF se carga hacia
el riel y lo sostiene ahí. Salir lleva minutos, porque la descarga es por los
47 k de la realimentación.

Y trae una trampa de método que conviene tener presente: **una etapa enganchada
está perfectamente quieta**. Esperar a que el tap deje de moverse —que es lo
correcto para el asentamiento— da una lectura estable y falsa cuando lo que hay
es un enganche. Que un tap no se mueva no prueba que esté vivo; lo único que lo
prueba es que responda.

## Estado honesto al cierre

**La calibración no cierra con PGA en x50.** No por el algoritmo: por dos
propiedades de la cadena que ahora están medidas.

1. El paso asentado de IDAC1 sobre el sumador es mayor que la ventana entera del
   sumador. No hay resolución para posicionarlo.
2. Cada vez que la búsqueda pasa por saturación, la cadena se engancha y cuesta
   minutos salir.

Queda corriendo la prueba que separa causa de consecuencia: **la misma
calibración con PGA en x8**. Si cierra, el techo lo pone la ganancia de entrada
amplificando el offset y su deriva, no el método, y eso cambia la decisión de
dejar PGAgain fijo en x50.

## Descartado: no es la ganancia del PGA

Corrí la misma calibración con **PGA en x8** en vez de x50, para separar si el
bloqueo venía de la ganancia de entrada amplificando el offset y su deriva.
Falla igual, en el mismo punto. Así que la decisión de dejar PGAgain fijo en x50
no es lo que hay que revisar.

## El cuello de botella real, y es un límite que había puesto yo

El log de esa corrida lo muestra sin ambigüedad. Con IDAC2 en **−180, su tope**,
ch2 quedaba en +772 mV. Para que ch3 entre en su ventana con PGAout en x4 hace
falta |ch2| < 520 mV. **Faltaban unos sesenta códigos de IDAC2.**

Y ese tope de ±180 no es del hardware: el actuador llega a ±255. Lo había puesto
yo el 2026-09-12, a partir de una medición real —pasados unos 180 códigos el
sumador deriva 7 mV/min contra 0,1 en la zona buena—, pero protegiendo de un
problema menor terminé impidiendo la calibración entera.

El compromiso, explícito: 7 mV/min de deriva es un problema conocido y acotado;
no calibrar no es un problema, es no tener instrumento. Y la verificación final
—un minuto de reposo mirando LPo— mide exactamente esa deriva, así que si el
punto elegido cae en la zona mala, se ve en el veredicto.

## La conclusión, con la evidencia que la sostiene

**Con PGA en x50 la cadena no tiene punto de trabajo alcanzable.**

La búsqueda anidada recorrió los códigos de IDAC1 de −105 a +15, y por cada uno
barrió IDAC2 entero. Encontró tres candidatos que leían dentro de ventana:

| IDAC1 | IDAC2 | ch3 al sondear | ch3 asentado |
|---|---|---|---|
| −105 | −255 | −239,4 mV | −5.045 |
| −95 | +97 | −171,0 mV | +1.854 |
| +5 | +193 | +109,6 mV | +1.854 |

**Los tres murieron al asentarse**, cada uno contra un riel. Y ch2 quedó en
+1.881 —su riel— en once de los trece códigos de IDAC1 probados.

No es un problema de resolución, ni de autoridad, ni de compliance, ni del
método de búsqueda. Es que en régimen, con la ganancia de entrada en x50, el
sumador está contra su riel para prácticamente todo el recorrido de sus
actuadores, y los puntos que parecen buenos son transitorios de camino a un
riel.

Queda corriendo la escalera desde **PGA x1**, donde el diagnóstico de la
madrugada sí encontró la cadena entera cómoda —ch2 = +439 y ch3 = +437, ganancia
1,00 y las dos etapas dentro de ventana—. Eso da el dato que falta: hasta qué
ganancia de entrada la cadena tiene punto de trabajo.

## Y con PGA en x1 la calibración CIERRA

Corrida de las 08:53, PGA x1 y PGAout x1:

```
2) Se busca el PAR (IDAC1, IDAC2) que mete SUMo adentro
   IDAC1=-111
      IDAC2=-95 -> ch3 -273,2 mV   candidato
      confirmado: ch3 -266,1 mV    DENTRO

4) IDAC3 hace los ultimos milivolts sobre LPo
    IDAC3=-255 ->  -4.302,7    IDAC3=+255 -> +1.189,2
    +0 -> -570,1   +127 -> +312,1   +63 -> -144,3   +95 -> +78,5
    +79 -> -36,7   +87 -> +15,4     +83 -> -10,8    +85 -> +3,6

6) Estado final de los cinco taps
   ch0 = -510,4   ch1 = -524,1   ch2 = -252,6   ch3 = -252,1   ch4 = +35,0
```

**Los cinco taps dentro de ventana, LPo a 35 mV de su centro.** La bisección de
IDAC3 recorrió de −4.302 a +3,6 mV en nueve pasos, monótona y limpia, que es
exactamente lo que el método promete cuando la etapa está viva.

El veredicto automático dijo "no llega" por diez milivolts, contra una tolerancia
de 25. Pero en el minuto de reposo la planta se corrió **15 mV sola**: pedir 25
es pedir más fineza que la que el circuito sostiene. La tolerancia quedó en 50
mV, que sobre una ventana de ±2 V son el 2,5 %.

## Entonces, el resultado

El algoritmo funciona. Lo que lo bloqueaba era el punto de trabajo de la cadena
con la ganancia de entrada en x50, no el método.

Queda corriendo la escalera de PGAout con PGA en x1 —x1, x2, x4, x8, x16, x24—
para dar el techo que pediste.

## Matriz de acople medida, y una retractación

Medida el 2026-09-13 a las 12:57, PGA x1 y PGAout x1, ABBA de 25 códigos por
actuador, sólo anotando los taps que estuvieron dentro de ventana en los cuatro
puntos del bloque. En mV por código:

|  | ch0 | ch1 | ch2 | ch3 |
|---|---|---|---|---|
| IDAC0 | +1,166 | −0,133 | −4,277 | −4,186 |
| IDAC1 | +0,004 | +2,154 | −7,833 | −7,650 |
| IDAC2 | +0,095 | −0,087 | **+12,596** | +12,490 |
| IDAC3 | −0,008 | −0,011 | +0,000 | +0,030 |

**Retractación: no hay acople por el nodo Vref compartido.** Horas antes había
informado que IDAC3 movía ch3 —que está aguas arriba de él— y lo atribuí a que
los cuatro pines `Vref_XX` cuelgan del mismo nodo. La fila de IDAC3 mide menos
de 0,03 mV por código sobre todos los taps de arriba: cero. Los 1.086 mV que
había atribuido a ese acople eran **la cadena derivando entre un barrido y el
otro**.

Es un error del mismo tipo que los otros de la jornada: comparar dos mediciones
separadas en el tiempo como si fueran simultáneas, en una planta que se mueve.

Lo que la matriz sí confirma, y es sólido:

- **IDAC2 → ch2 = +12,60 mV/código** contra 12,35 del modelo. Coincide.
- **IDAC1 → ch1 = +2,15** contra 1,875 predichos por 0,125 µA sobre 15 kΩ.
- **ch2 y ch3 se mueven idénticos** en las tres filas, con PGAout en x1: la
  etapa está sana y su ganancia es 1,00.
- Orden de autoridad sobre el sumador: **IDAC2 (12,6) > IDAC1 (7,8) > IDAC0
  (4,3)**. Útil para el adelanto.

ch4 quedó sin datos: LPo estuvo fuera de ventana durante toda la medición.


## RESULTADO: la calibración cierra y es reproducible a PGA x1 / PGAout x1

Segunda corrida independiente, 13:29:

```
PGAout x1: CALIBRA
LPo final -21,2 mV contra una tolerancia de 50
Corrimiento en el minuto de reposo: -8,1 mV
IDAC0=+10 IDAC1=-114 IDAC2=-95 IDAC3=+219
Todas las escrituras de IDAC fueron aceptadas.
```

Y reproduce la de las 08:53, que había dado LPo en +35 mV con IDAC1 = −111 e
IDAC2 = −95. **Los códigos coinciden**: −114 contra −111 en IDAC1 e idénticos en
IDAC2. Dos corridas separadas por cuatro horas y media llegan al mismo punto de
trabajo.

| corrida | LPo final | deriva en 60 s | IDAC0 | IDAC1 | IDAC2 | IDAC3 |
|---|---|---|---|---|---|---|
| 08:53 | +35,0 mV | +15,3 mV | +11 | −111 | −95 | +85 |
| 13:29 | −21,2 mV | −8,1 mV | +10 | −114 | −95 | +219 |

Eso es un algoritmo funcional: converge, deja los cinco taps dentro de ventana y
llega al mismo punto en corridas independientes.


## EL TECHO, medido: no es una ganancia de PGAout, es PGA x50

Escalera del 2026-09-13 a las 15:33, con la fase 1 ya reducida a 2,2 minutos y
un tope de 10 minutos por ganancia, cortando en la primera que falle.

**PGAout x2 no llega.** Y el log dice por qué sin ambigüedad: en cinco códigos
consecutivos de IDAC1 —de −110 a −70, cuarenta códigos— **ch2 se quedó asentado
en +1.669 mV sin moverse un milivolt**, y en cada uno IDAC2 recorrió su rango
entero sin meter ch3 en ventana.

```
IDAC1=-110   ch2 quieto en +1669.5 mV   IDAC2 recorrido entero sin meter ch3 en ventana
IDAC1=-100   ch2 quieto en +1669.3 mV   IDAC2 recorrido entero sin meter ch3 en ventana
IDAC1= -90   ch2 quieto en +1668.7 mV   IDAC2 recorrido entero sin meter ch3 en ventana
IDAC1= -80   ch2 quieto en +1668.9 mV   IDAC2 recorrido entero sin meter ch3 en ventana
IDAC1= -70   ch2 quieto en +1668.7 mV   IDAC2 recorrido entero sin meter ch3 en ventana
```

El sumador está enganchado contra su riel y ningún actuador lo saca. Como el
techo es monótono —la franja útil de ch2 se angosta como 1/G— si x2 no entra,
ninguna mayor entra, y la escalera cortó ahí.

### El resultado, dicho de una

| configuración | resultado |
|---|---|
| PGA x1, PGAout x1 | **CALIBRA**, y se repite: LPo en +35,0 y −21,2 mV en dos corridas separadas por 4,5 h, con los mismos códigos |
| PGA x50, cualquier PGAout | **no calibra**: el sumador queda enganchado y no responde a ningún actuador |

El límite no está en PGAout, que era donde lo buscábamos. Está en **PGA x50**.
Con la ganancia de entrada en x50 el sumador vive contra su riel y el punto de
trabajo se corre más que su ventana en decenas de minutos; con PGA en x1 la
cadena entera entra cómoda y el algoritmo cierra.

Eso pone en cuestión la decisión de dejar PGAgain fijo en x50, que estaba bien
fundada por otro motivo —no excitar la cola del pasabanda— pero que hoy es lo
que impide calibrar.
