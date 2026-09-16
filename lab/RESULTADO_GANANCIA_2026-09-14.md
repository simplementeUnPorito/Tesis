# Ganancia conjunta: qué se logró y dónde está el techo — 2026-09-14

Informe de cierre de la sesión del 13 al 14 de septiembre. Reemplaza las
conclusiones intermedias de esa noche, varias de las cuales resultaron falsas y
están señaladas como tales.

## El resultado

**PGAout x24 sostenido, con ganancia conjunta 96: PGA x4 por PGAout x24.**
Queda como punto por defecto de la placa `geo-01`:

```
IDAC  +0  +164  +75  -87
```

Es el "en el mejor caso x24" que se había pedido, y supera con holgura el
mínimo de 60 fijado como condición para que el circuito nuevo se justifique.

Sostenido con el PI: descontando los cinco minutos de convergencia, **43 de 43
lecturas de régimen en tolerancia, LPo entre −84,4 y +96,6 mV**.

Y PGAout x16 también, a ganancia 64 (PGA x4 por PGAout x16): **57 de 57 en
régimen, LPo entre −68,5 y +64,8 mV**.

## EL TECHO NO ES LA GANANCIA CONJUNTA: ES EL PGA

Esta es la corrección más importante del informe, y contradice lo que yo mismo
escribí durante toda la noche del 13.

| combo | PGA | PGAout | ganancia | llega | se sostiene |
|---|---|---|---|---|---|
| 50 · 1 | 50 | 1 | 50 | sí | sí |
| 32 · 2 | 32 | 2 | 64 | no | — |
| 16 · 4 | 16 | 4 | 64 | no | — |
| 8 · 8 | 8 | 8 | 64 | sí | **sí**, 45 min, 116/116 |
| **4 · 16** | 4 | **16** | 64 | sí | **sí**, 57/57 |
| 2 · 32 | 2 | 32 | 64 | no | — |
| 2 · 24 | 2 | 24 | 48 | sí | no (74 %) |
| 24 · 4 | 24 | 4 | 96 | no | — |
| **4 · 24** | 4 | **24** | **96** | sí | **sí**, 43/43 |
| 50 · 2 | 50 | 2 | 100 | no | — |
| 16 · 8 | 16 | 8 | 128 | sí | no (1/37) |
| 8 · 16 | 8 | 16 | 128 | sí | no (30/43) |
| 4 · 32 | 4 | 32 | 128 | sí | no (21/43) |
| 8 · 24 | 8 | 24 | 192 | no | — |
| 4 · 48 | 4 | 48 | 192 | no | — |
| 8 · 32 | 8 | 32 | 256 | no | — |
| 16 · 24 | 16 | 24 | 384 | sí | no |

Ordenado por PGA, el patrón es limpio:

- **PGA x4**: sostiene hasta ganancia 96 (con PGAout x24). A 128 ya no.
- **PGA x8**: sostiene 64. A 128 no.
- **PGA x16 o más**: no sostiene nada por encima de 50.
- **PGA x2**: tampoco anda, ni siquiera a ganancia 48.

Hay un óptimo en **PGA x4**, con caída a los dos lados. Que PGA x2 sea peor que
x4 es el dato que impide explicarlo sólo como "menos ganancia adelante, menos
deriva", y no tiene explicación por ahora.

## Por qué falla arriba: la deriva de la planta

Se despeja de la traza del PI, descontando de la excursión de LPo lo que aportó
el actuador:

| combo | corrección aplicada | LPo resultante | deriva de la planta |
|---|---|---|---|
| 4 · 24 = 96 | IDAC3, 3 códigos en 10 min | estable en ±97 mV | **~10 mV/min** |
| 16 · 8 = 128 | IDAC3, 438 códigos en 11 min (−4.599 mV) | subió igual +587 mV | **~467 mV/min** |

Cuarenta y siete veces más. Cuando la planta deriva así, el recorrido completo
del actuador fino —unos 1.700 a 2.700 mV— se consume en menos de seis minutos;
al agotarse, el descargue neutro mueve un código del grueso, que a esas
ganancias vale entre 1.200 y 1.900 mV, y eso inyecta cerca de un voltio de error
que el lazo tarda minutos en absorber. Para entonces el fino se está agotando
otra vez: ciclo límite.

O sea que hay dos límites distintos y conviene no confundirlos:

1. **La deriva de la planta**, que es del circuito y depende del PGA.
2. **La granularidad del actuador grueso**, que es del control y tiene remedio
   escrito y probado —`nonio.py`, que combina IDAC1 e IDAC2 para un escalón de
   144 mV donde cada uno por separado da miles—. No se aplicó porque a esa
   altura la consigna era dejar de afinar.

## Reproducir el resultado

```
py -3 saltar_ganancia.py --pga 4 --punto "0,164,-95,255"     --ganancias 24 --sostener 20 --periodo 20
```

## Los dos repartos de 128 fallan por motivos distintos

**16 · 8** falla por deriva: 1 de 37 lecturas de régimen en tolerancia, con la
planta corriéndose 467 mV/min.

**8 · 16** falla por granularidad del actuador grueso, y es un caso distinto que
conviene separar: 30 de 43 en régimen (70 %), con LPo entre −156 y +738 mV. Las
pendientes medidas en el punto son IDAC3 **+8,02** y IDAC2 **−1.522,5**
mV/código, o sea que **un solo código del grueso vale 7,6 veces la tolerancia**.
Cada vez que el fino agota su recorrido y el grueso lo releva, la maniobra
inyecta cerca de un voltio de error que el lazo tarda minutos en absorber, y
para entonces el fino se está agotando otra vez. El pico de +738 mV es
exactamente eso, no deriva:

```
t=256s  LPo -224,4   IDAC3=+239           el fino casi en su tope
t=382s  LPo +738,4   IDAC2=+57 IDAC3=+210 el relevo, y el salto que deja
t=506s  LPo +285,6   IDAC3=+135           el lazo absorbiendolo
```

El remedio para este caso concreto ya está escrito y probado y **no** se aplicó,
porque a esa altura la consigna era dejar de afinar: `nonio.py` combina IDAC1 e
IDAC2, cuyos pasos sobre ch2 son 8,3 y 12,2 mV —inconmensurables—, para formar
un escalón grueso mucho más fino. `3 códigos de IDAC1 contra −2 de IDAC2` da
144 mV donde cada uno por separado da miles. Tiene sus propias pruebas en
`test_nonio.py`.

Así que el techo de 64 tiene dos causas separadas según el reparto, y sólo una
—la deriva— es del circuito. La otra es del control y tiene arreglo conocido.

## Un patrón sin explicación

Los repartos que **no llegan** al punto son exactamente los que tienen PGAout en
**x2 o x4** —50·2, 32·2, 16·4, 24·4—, sin importar el producto ni el PGA. Con
PGAout en x1, x8, x16 o x32 se llega siempre. Además, los que fallan divergen
al mismo atractor, `ch2 = +1.665/+1.672 mV`, alcanzado por caminos distintos con
horas de diferencia.

No hay mecanismo identificado. La pista es que la consigna de ch2 vale
`(ch3_cero + (G−1)·Vref_o)/G`: para G=2 son unos −165 mV y para G≥8 converge a
−310 mV, así que los que fallan son los de consigna intermedia. Es una pista, no
una conclusión.

## Lo que hubo que arreglar del lazo

Tres errores reales, los tres encontrados por sus síntomas en las trazas:

1. **El descargue neutro entre fino y grueso sólo corría en modo vernier.** Con
   IDAC3 clavado en +255, el lazo externo calculaba transferir 0,039 códigos
   contra un paso mínimo de 0,4 y no movía IDAC2 nunca: veinte minutos de PI con
   el fino en su tope y LPo entre −200 y −320 mV. Ahora es obligatorio cuando el
   fino satura. Un actuador saturado no necesita que le transfieran de a poco.
2. **Las pendientes se medían a PGAout x1 y se usaban a la ganancia final.** A
   x8 el signo de IDAC3 sobre LPo aparece invertido respecto de x1, y un PI con
   el signo al revés es realimentación positiva. Ahora se remiden en el punto,
   con dos ABBA que cuestan segundos.
3. **El veredicto contaba el transitorio de convergencia como fallo.** A
   ganancia 64 el lazo partía de +245 mV y tardaba seis minutos en llegar a
   cero; con eso daba 40 de 44 lecturas en tolerancia y se declaraba fracaso.
   Ahora se descartan los primeros cinco minutos y se juzga el régimen.

## Y lo que hubo que arreglar del procedimiento de subida

Está en `PGAOUT_TIENE_REFERENCIA_PROPIA_2026-09-13.md` con el detalle. En
resumen: PGAout tiene punto fijo propio (−260 a −395 mV según el punto, no
cero), el cero del pasabajos se corre cuando se mueve IDAC3 y hay que
recalcularlo, la etapa LP amplifica ×4,8 y no ×18, e IDAC3 sólo necesita el
margen que la ganancia pide —27 códigos para x2, no los 255 que le estaba
sacando—.

## Reproducir el resultado

```
py -3 saltar_ganancia.py --pga 8 --punto "0,164,-95,255" \
    --ganancias 8 --sostener 45 --periodo 20
```

## Qué queda

- Probar el sostenimiento de 4·16 y 2·32, que llegan a 64 por otros repartos.
- Entender el patrón de PGAout x2/x4.
- Medir si el techo de deriva se puede correr: es la pregunta que decide si
  128 es alcanzable con otra placa o con un cambio de circuito.
- Portar el procedimiento al firmware del PSoC, que se dejó para el final por
  decisión explícita.
