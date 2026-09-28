# A/B: regular el par lento contra OPA_SUM en vez de SUM (2026-09-27)

## Veredicto: NO SIRVE.  Revertido.

## Que se cambio

Un solo `#define`: el aprendizaje del par lento regulando contra el tap
`OPA_SUM` (indice 2, el sumador, ANTES de PGAout) en vez de `SUM` (indice 3,
despues).  El argumento era que anular el offset antes de PGAout hace que la
resolucion del par lento deje de depender de PGAout -a x24, 5 mV en el
sumador llegan al tap SUM como 120-.  Ademas el parametro se llama
`CP_OPA_TARGET_UV` y `psoc_hw.h` ya dejaba anotada esa estrategia como futura.

## Resultado, contra la linea base de la vuelta 1 (72 visitas)

| par | ganancia | base | con el cambio: LPo final | IDAC3 |
|---|---|---|---|---|
| x16/x16 | 256 | 0/6, siempre aprendiendo | **-266,6 mV** | 254 |
| x32/x4  | 128 | 0/6 | **-273,8 mV** | **0** |
| x16/x8  | 128 | 0/6 | **-269,1 mV** | **0** |
| x4/x16  | 64  | **5/6** | -29,6 mV | 43 |

Ninguno de los tres que fallaban mejoro.  El control tampoco empeoro, asi que
el cambio es **inocuo pero inutil**.

## Por que no sirve, y que descarta

Los tres pares que fallan quedan con LPo entre **-266 y -274 mV**, contra una
ventana valida de +-120.  Eso es el **riel fisico**: la etapa esta saturada.
Ningun cambio de objetivo del lazo arregla una etapa saturada, porque la
realimentacion pierde el gradiente -solo queda el signo-.

Y en dos de los tres **IDAC3 quedo en 0, sin moverse nunca**: con SUMo fuera
de banda, la guarda de `control_pi_step` congela el lazo fino y el vernier ni
lo intenta.  Eso ya estaba identificado como defecto (A) y este A/B lo
confirma en tres pares independientes.

## Las tres fuentes coinciden

* **Simulacion** (`lab/sim/SIM_APRENDIZAJE.md`, `IDENTIFICACION.md`): no pudo
  certificar el cambio; el modelo no reproduce el fracaso de x16/x16 porque
  es lineal y el fracaso es saturacion.
* **Medicion directa** (este A/B): no mejora ninguno.
* **Los taps**: LPo clavado en -270 mV dice por que.

## Consecuencia para las conclusiones

El fracaso del PGA alto **no es** un problema de sintonia, ni de resolucion de
actuadores, ni del objetivo del lazo.  Es un **limite de rango dinamico de la
cadena**: a ganancia alta con reparto malo, alguna etapa satura antes de que
el lazo pueda hacer algo.  Eso no se arregla con firmware.

Lo que si funciona esta medido y es una regla de diseno utilizable: **a igual
ganancia, PGA bajo y PGAout alto**.  15 pases de 24 contra 1 de 30.
