# Compliance de los IDAC, y por qué IDAC3 parecía no tener autoridad

Elías planteó la hipótesis de que los IDAC estuvieran saturando por compliance:
el IDAC8 sólo funciona con su nodo de salida entre VSSA+1 y VDDA−1, y como la
resistencia va entre VDDA/2 y el IDAC, el nodo se aleja de 2,5 V a medida que
sube el código. Es una hipótesis correcta de plantear y hay que cerrarla con
números, porque explicaría de un plumazo todos los actuadores que "se quedan
sin fuerza".

## La cuenta

Los cuatro IDAC se programan explícitamente al rango de 32 µA
(`calibration.c:666-674`), o sea 31,875 µA de fondo de escala, 0,125 µA por
código. Las resistencias:

| IDAC | etapa | R | I·R máximo | nodo | margen al límite |
|---|---|---|---|---|---|
| 0 | PGA | 15 kΩ | 478 mV | 2,02 – 2,98 V | 1,02 V |
| 1 | BP | 15 kΩ | 478 mV | 2,02 – 2,98 V | 1,02 V |
| 2 | ADDER | 5,1 kΩ | 163 mV | 2,34 – 2,66 V | 1,34 V |
| 3 | LP | 10 kΩ | 319 mV | 2,18 – 2,82 V | 1,18 V |

El compliance exige el nodo dentro de [VSSA+1, VDDA−1] = [1,0 , 4,0] V. El peor
caso está a **más de un voltio** del borde, con los IDAC en su código máximo.

**No hay saturación por compliance en ninguno de los cuatro.** Y esto vale para
todo el recorrido, no sólo en el punto de trabajo: el margen es el mismo porque
está calculado con el fondo de escala.

### Un dato del repositorio que estaba mal

`PSOC_IDAC_LP_RSET_OHM` decía `1000u`, con un comentario del 2026-09-10 que
avisaba del zócalo. La resistencia real es de **10 kΩ**. Corregido.

No es un detalle cosmético: con 1 kΩ la autoridad calculada de IDAC3 en su
propio nodo son 32 mV, y como LPo se mueve 6,68 mV por código (medido), habría
que creer que la etapa amplifica **×53** desde su referencia. Con 10 kΩ son
319 mV y la ganancia sale **×5,3**, que es un número de circuito razonable. El
valor equivocado producía un absurdo que debería haberse notado antes de citarlo.

## Entonces qué le pasaba a IDAC3

La intuición de fondo era correcta, con otro mecanismo: **no le faltaba
autoridad, le faltaba margen.**

Medido el 2026-09-13 en dos corridas, IDAC3 mueve LPo entre 6,68 y
**16,99 mV por código** según el punto —la dispersión es en sí misma un dato: la
pendiente depende del punto de trabajo—. Con 255 códigos eso son entre 1.703 y
**4.332 mV de recorrido**.

Pero la calibración a PGAout x1 lo deja apoyado en **+255**. Es lógico: es el
único actuador que puede centrar LPo desde donde arranca la cadena, así que se
gasta entero. Y ahí queda sin nada hacia arriba, que es justo el sentido en el
que hacía falta corregir al subir la ganancia. Cada vez que se lo intentó usar,
el log decía "IDAC3 ya está en su tope" o directamente medía una pendiente de
1 mV en 510 códigos, que se leía como un actuador muerto.

## Por qué esto abre x16 y x24

El techo de las ganancias altas es la **granularidad** del actuador grueso, no
su recorrido:

```
IDAC2 -> ch2       +12,2 mV/codigo
etapa LP           x(-17,95) desde SUMo
=> IDAC2 -> LPo    -219 * G mV/codigo
```

o sea 3.504 mV por código a x16 y 5.256 a x24. Con la tolerancia en 200 mV, un
solo actuador grueso se pasa de largo diecisiete veces. Lo que salva la
situación es que el error de cuantización es como mucho medio código:

| PGAout | paso de IDAC2 sobre LPo | error máximo | ¿lo cubre IDAC3 (±4.332)? |
|---|---|---|---|
| x2 | 438 mV | 219 mV | sí, con enorme margen |
| x4 | 876 mV | 438 mV | sí |
| x8 | 1.752 mV | 876 mV | sí |
| x16 | 3.504 mV | 1.752 mV | sí |
| x24 | 5.256 mV | 2.628 mV | sí |
| x32 | 7.008 mV | 3.504 mV | justo |
| x48 | 10.512 mV | 5.256 mV | **no** |

Así que la estructura de mid-ranging alcanza hasta x32 —ganancia conjunta
1.600— siempre y cuando **IDAC3 esté centrado**. Devolverle el recorrido es la
fase 0 de `saltar_ganancia.py`: se lo baja de +255 hacia 0 de a doce códigos,
compensando cada paso con uno de IDAC2, y midiendo LPo en cada intercambio para
no salirse de ventana en el camino.

Si aun así hiciera falta más resolución, `nonio.py` tiene la salida: IDAC1 e
IDAC2 mueven ch2 con pasos inconmensurables (8,3 y 12,2 mV), así que la
combinación `3 códigos de IDAC1 contra −2 de IDAC2` da un escalón de 144 mV a
x16, veinticuatro veces más fino que cualquiera de los dos por separado. Tiene
pruebas propias en `test_nonio.py` y no se usa mientras IDAC3 alcance, porque
mover IDAC1 arrastra los 44 s del pasabanda.
