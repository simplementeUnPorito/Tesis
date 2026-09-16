# PGAout no está referido al cero del ADC — 2026-09-13

Este documento explica por qué **ninguna ganancia de PGAout por encima de x1
había calibrado nunca**, y cuál es la corrección. La causa no es la deriva, ni
la autoridad de los IDAC, ni el acople entre etapas: es un error de consigna.

## El experimento

`barrer_pgaout.py`. Se parte del punto calibrado a PGA x50 / PGAout x1 —el que
reprodujo tres veces: IDAC `+0 +164 −95 +255`—, se **congelan los cuatro IDAC**
y se sube PGAout leyendo los cinco taps en cada escalón. Nadie corrige nada. Lo
único que se mide es qué hace el escalón de ganancia por sí solo.

```
                  ch0         ch1         ch2         ch3         ch4
                  SEo         BPo    OPA_SUMo        SUMo         LPo
       x1 ya   -1183.1       -14.5       -26.6       -26.1       +90.9
     x1 +45s   -1167.5       -20.4        +1.3        +1.2       -42.3
      deriva     +15.6        -6.0       +28.0       +27.3      -133.2
       x2 ya   -1950.6      +228.2        +8.2      +471.5     -5627.5 *
       salto    -783.1      +248.7        +6.8      +470.3     -5585.1
     x2 +45s   -4192.6 *    -118.3     +1672.4     +1642.3     -5782.7 *
      deriva   -2242.0      -346.6     +1664.2     +1170.9      -155.2
```

`*` = fuera de ventana; ese número no es una tensión.

## Qué dice

**ch2 se movió 6,8 mV y ch3 saltó 470,3 mV.** OPA_SUMo está antes de PGAout y
SUMo después, así que el salto es enteramente de la etapa: PGAout no perturba al
sumador —una hipótesis que había que descartar, porque ch0 y ch1 sí se movieron
y por el camino de la señal eso no debería poder pasar—.

Con la entrada en +8,2 mV la salida quedó en +471,5 mV con ganancia 2. Una etapa
de ganancia cumple

```
    ch3 = Vref_o + G · (ch2 − Vref_o)
```

y despejando la referencia propia:

```
    Vref_o = (G·ch2 − ch3) / (G − 1) = (2·8,2 − 471,5) / 1 = −455 mV
```

### Y de dónde sale ese −455 mV: no se sabe

Conviene decirlo antes de que alguien lo dé por explicado. La primera lectura de
este documento atribuía los −455 mV a la diferencia entre el `Vref` de la placa
y Vdda/2, apoyándose en `PSOC_IDAC_VREF_UV_DEFAULT` de `psoc_hw.h`, que vale
2,062 V. **Eso está mal**: ese valor modela la portadora JitX que nunca se
fabricó. En la placa real no hay AMS1117 y todas las referencias son Vdda/2 ≈
2,5 V, que es también el cero del ADC. Con eso, la predicción para el punto fijo
de PGAout es **cero**, y el desplazamiento medido no viene de ahí.

O sea que los −455 mV son un hecho medido sin causa identificada. Los candidatos,
ninguno comprobado:

- El terminal de referencia de PGAout no está en Vdda/2 en el TopDesign, sino
  atado a otra cosa o al bus analógico. El `.cysch` es binario y no se puede
  leer con las herramientas de acá; hay que abrirlo en PSoC Creator y mirar.
  `PGAout_VREF_MODE` vale `0x00`, o sea `GNDVREF` deshabilitado, igual que
  `PGAgain`: eso descarta que la referencia sea Vssa, y nada más.
- Un offset de entrada de PGAout. Para dar este número tendría que valer
  +228 mV referido a la entrada, que es demasiado para un amplificador.
- Inyección de carga entre bloques de capacidades conmutadas.

Para el procedimiento la causa no cambia nada: la consigna sale del número
medido, y el script lo vuelve a medir in situ en cada corrida en vez de
confiar en la constante. Pero mientras no se sepa el mecanismo **no hay que
suponer que −455 mV sea estable entre placas, ni con la temperatura**, y eso sí
importa para el campo.

A x1 el modelo también cierra, y es la comprobación que hace creíble al resto:
con G=1 la fórmula da ch3 = ch2, y se leyó −26,1 contra −26,6 y +1,2 contra
+1,3.

## Por qué esto arruinaba todas las ganancias

El punto fijo de una etapa de ganancia es su propia referencia. Con ch2 centrado
en **cero** —que es lo que hacían `centrar_lpo.py` y `subir_ganancia.py`— cada
duplicación empuja SUMo (G−1)·455 mV hacia arriba:

| PGAout | ch3 con ch2 en cero | ¿entra? |
|---|---|---|
| x2 | +455 mV | en ventana, pero LPo lo amplifica y se clava |
| x4 | +1365 mV | contra el riel |
| x8 | +3185 mV | imposible |
| x16 | +6825 mV | imposible |

La consigna correcta no es cero:

```
    ch2* = (G − 1)/G · Vref_o
```

o sea **−228 mV para x2, −341 para x4, −398 para x8 y −427 para x16**. A la
autoridad medida de IDAC2 sobre ch2 —unos 5,1 mV por código— eso son entre 45 y
84 códigos. Sobra rango: nunca fue un problema de autoridad.

## El segundo hallazgo: el orden importa

La fila `x2 +45s` es la otra mitad. Con los cuatro IDAC quietos, en 45 segundos
ch2 se fue de +8 a **+1672 mV** y ch0 salió de ventana. Eso no es la deriva de
la cadena, que en ese mismo experimento midió 28 mV en 45 s sobre el mismo tap:
es sesenta veces más rápida y arranca justo cuando LPo se clava.

Y no vuelve. Ya sabíamos que los cuatro códigos no definen el punto de trabajo
(`lab/` del 2026-09-12): cada excursión al riel carga el acople y revertir el
código no restaura el punto.

Eso condena a cualquier procedimiento que **primero cambie la ganancia y después
busque el centro**, que es lo que hacían las corridas del 17:22 y todas las
anteriores. Para cuando la búsqueda empieza a medir, la cadena que iba a
centrar ya no existe.

## La corrección

`subir_por_consigna.py`:

1. Con PGAout todavía en **x1** —donde ch3 = ch2 y nada puede clavarse—, lleva
   ch2 a su consigna `(G−1)/G · Vref_o` con pasos proporcionales a la pendiente
   medida.
2. Espera a que la cadena se aquiete.
3. Recién entonces cambia la ganancia. Si el modelo vale, SUMo aterriza cerca de
   cero de una vez y no hay ningún instante saturado.
4. Vuelve a medir `Vref_o` in situ con la lectura de ch2 y ch3, y afina con
   IDAC2 y después LPo con IDAC3.

Los pasos son proporcionales y **no** una bisección, a propósito. Una bisección
necesita dos extremos de signo opuesto y conseguirlos obliga a visitar los
rieles, que es exactamente lo que destruye el punto.

## Primera prueba de la corrección, 18:05

`subir_por_consigna.py --pga 50 --ganancias 2`, desde el punto de x1.

```
1) con PGAout todavia en x1, llevar ch2 a -228 mV
   IDAC2 -> ch2: +12.13 mV/codigo
   IDAC2 -115  ->  ch2 -233.0 mV
2) ahora si, PGAout a x2
   ch2 -239.6  ->  ch3 -153.4 mV
   la referencia de PGAout medida aca da -326 mV
estado final:
   ch0 -1530.0   ch1 +64.8   ch2 -151.6   ch3 +62.2   ch4 -1020.1
```

**SUMo aterrizó en −153 mV en vez de +471, y los cinco taps quedaron en
ventana.** Es la primera vez que la cadena entera sobrevive a un cambio de
ganancia de PGAout. El modelo vale.

Dos cosas que salieron de acá:

- **La referencia remedida dio −326 mV y no −455.** No es una constante fina, y
  refuerza que no se sabe de dónde sale. El procedimiento no depende de eso
  porque la remide y después afina, pero para el firmware significa que hay que
  medirla, no tabularla.
- **La ganancia de la etapa LP desde SUMo es −17,95 mV/mV**, medida en esta
  misma corrida (ch3 de +11,3 a +62,2 movió LPo de −106,3 a −1020,1). De ahí
  sale la tolerancia que hay que exigirle a SUMo: para ±200 mV en LPo son
  **±11 mV en ch3**, no ±200.

Y ahí estuvo el error que hizo fallar esta corrida: se le pasó a ch3 la
tolerancia de LPo, así que el afinado aceptó ch3 = −145 mV —que son −2.600 mV en
LPo— y se dio por terminado. Corregido: los pasos 3 y 4 centran **LPo**, con
IDAC2 de grueso (−435 mV por código a x2) e IDAC3 de vernier (6,68).

## Lo que queda por comprobar

- Que ch0 y ch1 se queden en ventana. El escalón a x2 los movió −783 y +249 mV
  con IDAC2 quieto, y por el camino de la señal eso sigue sin tener explicación.
  Puede ser inyección de carga entre bloques de capacidades conmutadas, o el
  nodo Vref compartido. Si el salto crece con G, va a ser el próximo techo.
- Que el punto **se sostenga** con el PI corriendo (`sostener.py`), que es el
  requisito real: llegar no es sostener.
