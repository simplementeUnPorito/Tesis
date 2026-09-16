# El lazo cerrado que culmina la calibración

Elías señaló que el diseño original era PI puro y que el trabajo había derivado
hacia una calibración a lazo abierto cada vez más elaborada. Tenía razón. Esto
documenta el lazo cerrado que faltaba.

## Por qué el lazo abierto no podía alcanzar

La calibración en dos fases mide la planta, calcula los códigos, los escribe y
suelta. Eso exige que el modelo sea correcto, y esta cadena no lo permite:

- Las pendientes derivadas variaron **un factor ocho** entre corridas del mismo
  día para el mismo par de nodos.
- El punto de trabajo **depende del camino recorrido**, por la absorción
  dieléctrica del acople de 680 µF.
- Hay una deriva de varios milivolts por minuto en parte del rango.

A lazo abierto cada una de esas cosas es fatal. A lazo cerrado son perturbaciones
que el integrador rechaza sin enterarse de por qué ocurren.

**El lazo abierto no se tira.** Queda como adelanto, con un trabajo acotado:
dejar la cadena en un punto donde los taps sean legibles y respondan. No tiene
que ser exacto.

## Qué necesita saber el regulador, y qué no

Sólo el **signo** de cada actuador. No el módulo, no el camino, no la causa de
una deriva. Por eso el signo se mide en placa antes de arrancar, con excitación
grande, y todo lo demás se deja que el lazo lo absorba.

## La sintonía sale de la física

La planta es un retardo de primer orden con la τ del pasabanda. Con un
integrador, el margen de fase razonable aparece cuando la ganancia de lazo cruza
uno cerca de 1/τ, y eso equivale a corregir por paso una fracción
`alpha = T/tau`. Con T de 5 s y τ de 34 s da 0,15.

De ahí salen las dos propiedades que importan:

| propiedad | valor |
|---|---|
| constante de tiempo del lazo cerrado | del orden de τ, unos 100 s al 95 % |
| error de ganancia que tolera | unas 7 veces en teoría; **4 verificadas** |

Esa tolerancia es exactamente lo que hacía falta: las pendientes medidas variaron
un factor ocho.

## La cascada con mid-ranging

Dos actuadores sobre el mismo nodo, uno con resolución y otro con recorrido. El
lazo rápido usa el fino para seguir la referencia; un lazo diez veces más lento
mueve el grueso para devolver al fino **al centro de su rango**.

Resuelve dos cosas a la vez: el fino nunca se acerca a los 180 códigos donde se
vuelve inestable, y la combinación de los dos da una resolución efectiva muy
fina.

**El par se elige midiendo, no por diseño.** Cuál actuador sirve de grueso
depende del punto de trabajo: el 2026-09-12, con el sumador en +1.847 mV, el
candidato natural no respondía en absoluto (−0,00 mV/código) mientras el de
entrada respondía a −58 mV/código.

## Las tres piezas que la cadena obligó a inventar

### El vernier

A ganancias altas un código del fino mueve LPo más que el ancho de la ventana
entera: en x24 son 2.830 mV sobre 4.826. Con un solo actuador **es imposible**
centrar nada.

Pero los dos pasos son incomensurables, 12,35 y 8,3 mV, así que combinándolos en
oposición se llega a décimas de milivolt. Es un vernier, la idea del calibre.
Sólo se usa cuando el paso del fino supera la precisión pedida, porque mover el
grueso arrastra la cola del pasabanda.

### El descargue neutro

En mid-ranging clásico el externo mueve el grueso y el interno compensa. Acá no
se puede: a x24 un código del grueso son 1.807 mV y uno del fino 2.688, así que
cualquiera solo es una patada enorme y el otro no tiene con qué corregirla.

La salida es moverlos **juntos** de modo que sus efectos se cancelen: dos códigos
de uno contra tres del otro dejan 43 mV de residuo sobre movimientos de miles. Es
un desplazamiento en el núcleo de la transformación.

### El lazo en dos etapas

Con la cadena saturada, LPo no dice nada: se rastreó el rango completo de los dos
actuadores, en ambos signos, y se movió dos milivolts. Pero el sumador se lee
perfectamente en esa misma situación.

Así que primero se cierra el lazo sobre el sumador, hasta ponerlo donde LPo
vuelve a ser legible, y recién después se regula LPo.

## Resultados

**En simulación**, con una planta de primer orden, dos actuadores, deriva y
saturación: convergen **todas las ganancias de x1 a x50**, con el actuador fino
como mucho al 60 % de su zona útil. Veinte pruebas automáticas en 0,3 s.

Las que importan no son las que usan el modelo correcto sino las que lo usan mal:

- converge con la ganancia estimada **cuatro veces mayor** que la real;
- converge con la ganancia **cuatro veces menor**;
- rechaza la deriva de 7 mV/min que se midió en placa;
- con el signo invertido no diverge, pero deja el fino clavado en su límite, y
  esa prueba existe para documentar que el signo hay que medirlo.

**En placa, el lazo cerró la calibración completa** el 2026-09-12 a las 18:54,
con PGA x50 y PGAout x4:

| resultado | valor |
|---|---|
| error final en LPo | **−49 mV** sobre una ventana de ±2.400 |
| actuador fino | +36 de ±160, el 22 % de su zona útil |
| actuador grueso | +16 |
| pasos con vernier | 0, no hizo falta a esta ganancia |

Archivo: `lab/calibracion_nueva/cerrar_lazo_20260912_185431.csv`.

La etapa del sumador había convergido antes con 1,3 mV de error, llevándolo de
+1.862 a −268,7. En el camino el fino saturó en −160, el grueso se hizo cargo y
después el fino volvió a +2: mid-ranging de manual.

### Por qué el lazo abierto nunca llegó

**La consigna real del sumador es −1.600 mV y el modelo decía −270.** Un error de
mil trescientos milivolts. Eso explica de una sola vez por qué una jornada entera
de correcciones al lazo abierto no alcanzó: no estaba fallando la ejecución,
estaba apuntando al lugar equivocado.

El rastreo la encontró en su **primer punto**, porque empieza por el extremo
negativo, que es justamente el lado que una búsqueda con dirección supuesta nunca
mira.

## Errores propios que la placa desmintió, y quedan anotados

Cuatro suposiciones que estaban escritas como si fueran hechos:

1. **Que la bisección era ciega.** Suponía que subir el código sube el tap. Con
   la pendiente negativa recorrió de 0 a +255 y concluyó que la cadena no
   llegaba, sin haber mirado nunca los códigos negativos.
2. **Que estar dentro del rango de lectura implica responder.** El sumador
   marcaba +1.868 mV, cómodamente adentro, y no se movía ante ocho códigos de su
   actuador.
3. **Que la franja se podía calcular.** El modelo puso el sumador exactamente
   donde predijo y LPo siguió clavado.
4. **Que el par grueso y fino se podía elegir por diseño.** Depende del punto de
   trabajo.

Y una que cometí **dos veces**: la búsqueda de consigna volvió a suponer la
dirección, en código nuevo escrito para ser ciego, después de haber corregido ese
mismo defecto en el rastreo dos horas antes.

## Lo que queda

1. Barrer las ganancias con el lazo, empezando por x24, que es donde el vernier
   deberia entrar en juego. A x4 no hizo falta.
2. Repetir varias veces la misma ganancia para medir repetibilidad, que en un
   sistema con memoria es la unica forma honesta de afirmarla.
3. Decidir cada cuánto corre el lazo en campo. No puede correr **durante** la
   adquisición, porque cada paso mete un escalón en el registro. Entre disparos
   sí, que en un tendido MASW es la mayor parte del tiempo.
4. Pasarlo a C dentro del PSoC, que era el plan desde el principio.
