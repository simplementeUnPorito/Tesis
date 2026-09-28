# El experimento de ruido no se pudo correr (2026-09-28)

## Estado: BLOQUEADO, con el defecto localizado

Es el unico de los cinco entregables que no se logro.  Queda diagnosticado
hasta el punto exacto donde falla, para que retomarlo no cueste empezar de
cero.

## Sintoma

Las veinte corridas fallan con `captura corta: 5 de 500 lotes`, en 30
segundos.

## Lo que SI era un defecto y se corrigio

El host mandaba `capwait 500` y esperaba **0,5 s**.  El comentario del codigo
decia "capwait bloquea en el firmware hasta que la captura termina" -cierto-
y el host asumia que con eso alcanzaba.  Una captura de 500 lotes de 30
muestras a 2604 Hz dura **5,76 s**.  Corregido: ahora se calcula y se espera.

Mismo patron que ya mordio cuatro veces este fin de semana: el comentario
describe el FIRMWARE y el codigo del host da por hecho que eso basta.

## Lo que sigue bloqueado

Con la espera corregida, la captura **sigue sin llenarse**.  El ESP responde:

    [USB] sync ignored state=2 ready=0
    [LAB] LAB_CAPWAIT done=0 fill=0/500

o sea que **el sync que dispara la captura se ignora porque el PSoC no esta
armado** (`ready=0`).  Los "5 lotes" que aparecian eran restos de una captura
anterior, no una captura corta.

Por la via de `startwait`, que es la que `_asegurar_adquisicion` usa con
exito, el resultado es distinto pero tampoco sirve:

    [LAB] LAB_STARTWAIT done=0 timeout=1 state=3 fill=0/500 dOK=500

**La captura OCURRE** -`dOK=500`, quinientos lotes procesados- **pero no queda
nada en la RAM del ESP** (`fill=0`), que es de donde lee `dumpusb`.  Los lotes
se van por otro camino.

## Por donde seguir

El defecto esta en el camino de captura del ESP, entre que los lotes se
procesan y que quedan retenidos para el volcado por USB.  Hay que mirar:

* en que estado tiene que estar el PSoC para que el `sync` no se ignore
  (`ready=1`), y si el lazo de control corriendo lo impide;
* por que `dOK=500` convive con `fill=0`: donde se estan yendo esos lotes
  -encadenado al PSoC, SD, streaming- en vez de quedarse en la RAM del ESP;
* si `capwait` y `startwait` dejan el nodo en estados distintos (se vieron
  state=2, 3 y 4 segun el camino).

Relacionado en memoria: la jerarquia ESP RAM -> encadenado PSoC -> SD, y que
la auto-calibracion del PSoC puede trabar la captura.

## Que se pierde y que no

Se pierde la cuantificacion de cuanto ruido agregan la SD y la radio, y si
depende de la ganancia.  **No** se pierde nada de lo demas: el experimento
corre al final de la cadena y sus fallos costaron 30 segundos cada uno.
