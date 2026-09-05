

# Estado al cierre del 2026-09-04 

Las de arriba se contestaron o quedaron sin objeto. **Todo lo medido está en
`docs/MEDICIONES_2026-09-04.md`**, que es el documento único. Acá quedan sólo las
decisiones que son tuyas.

## A. ¿1τ o 2τ de espera de planta?  · ya está puesto en 1τ

Puse `CAL_PI_PLANT_SETTLE_TAU_X10 = 10` (1τ) porque el modelo, ya calibrado
contra la placa, da **2,09 mV en 119 s** contra tu objetivo de 20 mV. Con 2τ da
**0,47 mV en 237 s**.

Como la recalibración es por umbral y no en cada arranque, el tiempo casi no
importa, así que **2τ es asequible si querés más margen**. Es cambiar un 10 por
un 20. Decidí vos.

**Ojo para campo:** 29,5 s es el τ de banco. Con 5–45 °C el peor caso es ~40 s,
así que una espera fija conservadora hay que dimensionarla con eso, no con 29,5.

## B. El acople ADDER→LP es 4,04×. ¿Firmware o hardware?  · **la decisión de fondo**

Mover la referencia del ADDER corre la salida del LP **cuatro veces más** que la
referencia del propio LP. Con la autoridad del LP en 133,8 mV y el ADDER
metiéndole 254,5 mV al moverse 120 códigos, lo saca de rango.

Dos caminos, y no los puedo elegir por vos:

- **Firmware:** precompensar. Ya está implementado en el modelo
  (`calibrar_precomp`): al cerrar la etapa k se corrigen de una las j>k por
  `G[k][j]·Δ/G[j][j]`, que ahora se conoce porque está medido. No mejora en
  1×/1× porque los offsets son de ~1 mV, pero es exactamente para el caso de
  ganancia alta.
- **Hardware:** subir la autoridad del LP, o bajar el acople del ADDER.

## C. El ADDER pierde el 40 % de su rango. ¿Se acepta o se toca el hardware?

Su pendiente local va de 1963 µV/cód en el centro a **0,4 en los extremos**.
Acoté el IDAC a ±128 por firmware (commit `9af676d`), que es la solución barata.
Se pierde el tramo −178…−128, que sí es útil, porque el clamp es simétrico.
Soportar límites asimétricos es un cambio chico pero toca la estructura y todos
los inicializadores; no lo hice a las apuradas.

## D. Ki: puesto en 1/32 como red de seguridad

El barrido sale plano. El integrador corrige lo que el lazo **observa**, y acá el
lazo cierra y se va antes de que el error aparezca. Va como seguro contra lo que
el modelo no captura, no porque la simulación lo pida.

## E. Lo que hay que revertir del banco

- **COM8 (maestro): le grabé `slaveTest` por error.** Hay que devolverle el
  firmware de master.
- **COM7 (esclavo): tiene `slaveTest`.** Devolverle `slave2` para campo.
- **PSoC: tiene el autotest.** Devolverle el de campo.
- `platformio.ini` tiene `upload_port = COM8` fijo en el entorno `slaveTest`, que
  es lo que causó el error. Conviene sacarlo.
