# A ganancia conjunta 100 la cadena diverge sola — 2026-09-13

Este documento registra un experimento de control cuyo resultado cambia el
diagnóstico de todo el trabajo de autocalibración: **el problema de las
ganancias altas no está en el lazo de calibración.**

## Por qué hizo falta el control

Durante toda la tarde, cada intento de llegar a PGA x50 · PGAout x2 terminaba
igual: el punto se encontraba y se perdía en menos de un minuto. Cada vez
apareció una causa plausible en el algoritmo —una tolerancia mal aplicada, un
cero desactualizado, una espera demasiado larga— y cada vez se arregló y volvió
a fallar.

Ese patrón es la señal de que se está corrigiendo lo que no es. La forma de
salir es dejar de tocar y mirar.

## El experimento

`saltar_ganancia.py --ganancias 2 --congelado 5`. Se llega al punto por el
procedimiento normal, se **congelan los cuatro códigos IDAC** y se observa
cinco minutos leyendo los cinco taps. Nadie corrige nada.

El aterrizaje, en la mejor de las corridas, fue limpio y sin pasar por el riel
en ningún momento:

```
ch2 -215.2  ->  ch3 -99.9  ->  LPo -45.8 mV
```

Cinco minutos después, con los mismos cuatro códigos:

```
ch0 -4228.0 *   ch1 -356.0   ch2 +1672.4   ch3 +1643.0   ch4 -5781.3 *
```

`*` = fuera de ventana.

## Qué dice

**Con todo congelado, la cadena se va sola.** ch2 recorrió 1.700 mV sin que
ningún actuador se moviera.

Y no se va a cualquier lado: `ch2 = +1672,4 mV` es **exactamente** el mismo
valor al que había llegado el primer barrido de la tarde, ocho horas antes, en
otra corrida y por otro camino. Es un atractor, no ruido.

Comparado contra el mismo tap a PGAout x1, con los mismos códigos y en el mismo
experimento:

| | deriva de ch2 |
|---|---|
| PGAout x1 | +28 mV en 45 s |
| PGAout x2 | +1.664 mV en 45 s |

Cincuenta y nueve veces más.

## Lo que esto descarta

- **No es el lazo de calibración.** No había lazo corriendo.
- **No es el orden de las operaciones,** ni las esperas, ni las tolerancias.
  Todo eso se arregló y el resultado no cambió.
- **No es que LPo pase por el riel durante la transición.** En la corrida
  citada LPo aterrizó en −45,8 mV y nunca tocó el riel antes de que empezara la
  divergencia.
- **No es compliance de los IDAC.** Ver
  `COMPLIANCE_DE_LOS_IDAC_Y_MARGEN_DE_IDAC3_2026-09-13.md`: el peor nodo queda a
  1,18 V del límite.

## Lo que hay que averiguar ahora

De qué depende el umbral. Hay tres hipótesis con consecuencias distintas:

**A. Del producto de las ganancias.** Habría un techo de ganancia total, y
repartirla entre PGA y PGAout no serviría de nada.

**B. De que PGAout pase de x1.** El techo sería de esa etapa. Repartir tampoco
ayudaría, pero el arreglo sería otro.

**C. Del PGA solo,** y PGAout no tendría nada que ver — poco probable, porque
PGA x50 con PGAout x1 es estable y reproducible desde hace horas.

`mapa_estabilidad.py` las separa barriendo PGA con PGAout fijo y midiendo la
velocidad de deriva de ch2, que es el tap que delata la divergencia. No hace
falta calibrar para eso: los IDAC se dejan en cero y lo único que cambia entre
punto y punto son las dos ganancias.

## Mecanismo candidato, no comprobado

Los cuatro pines `Vref_XX` cuelgan del mismo nodo a través de sus resistencias,
así que hay un camino de realimentación entre etapas que no pasa por la señal.
Si la ganancia de ese lazo parásito escala con la ganancia de la cadena,
habría un umbral por encima del cual el conjunto deja de ser estable — que es
exactamente la forma de lo observado: estable y reproducible durante horas a
ganancia 50, divergente en decenas de segundos a 100.

Es una hipótesis con una predicción comprobable: si es cierta, el umbral debe
seguir al **producto** de las ganancias y no a cuál de las dos etapas lo aporta.
Eso es lo que mide el mapa.

## Consecuencia para la tesis

Si el umbral está entre 50 y 100, el circuito nuevo tiene un techo de ganancia
que no es el que se le pidió, y eso es un resultado de diseño que hay que
reportar con el número medido, no un fracaso del control. El lazo PI, la
estructura de mid-ranging y el vernier siguen siendo válidos por debajo del
umbral, y el trabajo de hoy dejó además el modelo de la etapa de salida —punto
fijo propio, consigna `ch2* = (G−1)/G · Vref_o`— que es lo que hacía imposible
subir de x1 aunque la cadena hubiera sido estable.

---

# CORRECCIÓN, madrugada del 2026-09-14: el techo NO es el producto

La hipótesis A de más arriba —que habría un techo de ganancia total— **queda
refutada**. Probadas todas las formas de repartir 64 y varias de 128:

| combo | producto | ¿llega al punto? |
|---|---|---|
| 50 · 1 | 50 | sí |
| 32 · 2 | 64 | **no**, y congelada se va al atractor +1.665 mV |
| 16 · 4 | 64 | **no** |
| 8 · 8 | 64 | sí, LPo +52,8 y +54,8 mV en dos corridas |
| 4 · 16 | 64 | sí, LPo −62,3 mV |
| 2 · 32 | 64 | sí, LPo +43,9 mV |
| 24 · 4 | 96 | **no** |
| 50 · 2 | 100 | **no**, atractor +1.672 mV |
| 16 · 8 | 128 | sí, LPo −135,2 mV |
| 8 · 16 | 128 | sí, LPo −42,9 mV |

Tres combinaciones dan 64 y andan, dos dan 64 y no. Y hay dos de 128 que andan.
El producto no explica nada.

## Lo que sí ordena los datos

**Falla exactamente cuando PGAout está en x2 o x4.** Con x1, x8, x16 o x32
llega, sin importar el producto ni el PGA. No tengo explicación para eso y hay
que decirlo así: es un patrón, no un mecanismo.

Algo que puede tener que ver: la consigna que hay que ponerle a ch2 es
`(ch3_cero + (G−1)·Vref_o)/G`, que para G=2 vale unos −165 mV y para G≥8
converge a −310 mV. Los casos que fallan son los de consigna intermedia, donde
la sensibilidad `dch3/dch2 = G` todavía es chica y el término `(G−1)·Vref_o`
ya es grande. Es una pista, no una conclusión.

## Y una advertencia sobre qué significa "llega"

"CALIBRA" es el veredicto del instante posterior al afinado: los cinco taps en
ventana y |LPo| ≤ 200 mV. **No es estabilidad.** Congelados cinco minutos, los
tres que llegan se corren siempre en la misma dirección:

| combo | LPo tras 5 min congelado |
|---|---|
| 8 · 8 = 64 | −730 mV (taps en ventana) |
| 2 · 32 = 64 | −838 mV (taps en ventana) |
| 16 · 8 = 128 | −2.950 mV (LPo fuera de ventana) |

Las dos primeras caen dentro de los ~1.700 mV de autoridad de IDAC3; la tercera
exige que IDAC2 tome el relevo.

Y ahí apareció el fallo del regulador que estaba tapando todo esto: el descargue
neutro entre fino y grueso sólo corría en modo vernier, así que con IDAC3
clavado en +255 el lazo externo calculaba transferir 0,039 códigos contra un
paso mínimo de 0,4 y **nunca movía IDAC2**. Veinte minutos de PI a ganancia 64
con IDAC3 en su tope, IDAC2 quieto en +59 y LPo entre −200 y −320 mV. Corregido:
el descargue es obligatorio cuando el fino satura, esté o no en vernier.

La escalera con el lazo ya corregido —cada escalón exigiendo que el PI lo
sostenga 15 minutos, cortando en el primero que no— es la que decide cuál queda
como ganancia por defecto.
