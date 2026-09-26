# Plan de edicion tras la vuelta 1 (2026-09-26)

Restriccion que manda: **el martes tiene que estar todo funcional**.  Por eso
el alcance esta deliberadamente recortado y hay punto de retorno.

## Punto de retorno

* tag `bueno-20260926` en el submodulo del PSoC, commit `ed2847c`
* hex archivado en `lab/firmware_bueno/AcondicionamientoAnalogico_bueno_20260926.hex`
* estado verificado: ganancias 64 y 128 estables, FINE_SLOPE 450, aprendizaje
  con margen de vernier, inyeccion manual efectiva, psocreset verificado

Si algo sale mal: `git checkout bueno-20260926` y `ciclo.ps1`, o grabar el hex
archivado. Menos de diez minutos.

## Diagnostico (datos de la vuelta 1, 19 visitas)

Son DOS defectos, no uno:

**(A) La guarda de SUMo congela el lazo fino.**  Si SUMo se sale de
`CP_SUM_BAND_UV` (60 mV) o se vuelve invalido, `control_pi_step` entra en la
rama de guarda, mueve el grueso con 45 s de enfriamiento y **retorna sin
correr el PI fino** salvo rescate de riel.  Medido: x8/x8 CONTROL deja LPo en
+91 mV con IDAC3 en -30 y SUMo valido solo el 63 % del tiempo.  Corregir esos
91 mV pide ~200 codigos y le sobran: no es que no pueda, es que no lo intenta.
x32/x2 es el caso extremo, con SUMo en +90 mV de forma permanente.

**(B) El descargue del vernier es inalcanzable.**  Vive dentro de la rama
`p->holding`, que exige |LPo| <= `CP_HOLD_UV` (25 mV).  Los pares fragiles
asientan mas afuera, asi que nunca corre: IDAC2 no se movio en 11 de 19
visitas, y cuando se movio fueron 1 a 4 codigos.  Resultado: IDAC3 termina en
-231, -233, 252... en banda y sin margen termico.

Los dos salen de la misma raiz -el objetivo de SUMo no se elige para dejar LPo
cerca de cero- pero se arreglan por separado.

## Lo que SI se hace: (B)

Permitir el descargue cuando LPo este dentro de `CP_DEADBAND_UV` (45 mV) y no
solo dentro de HOLD (25).  Es un cambio de una condicion.

Por que recien ahora tiene sentido: el descargue compensa un codigo de IDAC2
con `COARSE_SLOPE/FINE_SLOPE` codigos de IDAC3.  Con la pendiente vieja eso
daba 150000/2500 = 60 codigos, y el movimiento "bumpless" en realidad pateaba
LPo unos 123 mV -no era bumpless, era un salto-.  Con la pendiente medida son
150000/450 = 333 codigos, y IDAC3 tiene 510 de rango: la maniobra es posible
y de verdad no salta.  O sea que el mecanismo ya esta bien; falta dejarlo
correr.

Prediccion falsable: en los pares fragiles, IDAC3 debe terminar cerca del
medio en vez de contra el riel, SIN que empeoren |LPo| ni el pico a pico.

Validacion antes de darlo por bueno:
1. x4/x16 y x8/x16 -los dos que ya andan- no deben empeorar.  Si empeoran,
   se revierte: no se cambia algo que funciona por algo que quiza mejore.
2. x8/x8, que hoy termina con IDAC3 en -231, deberia dejar de ser fragil.
3. Prueba de lazo cerrado: perturbar y ver que vuelve solo.

## Lo que NO se hace: (A)

Tocar la guarda de SUMo es cirugia en el corazon del lazo y no se hace a dos
dias de la entrega.  Queda documentado con los numeros que lo prueban.  Nota
para despues: la guarda tiene sentido -un codigo de IDAC2 patea LPo por toda
la ventana- pero hoy es absoluta, y podria ser condicional a que el rescate de
LPo no este trabajando.

## Orden

1. Esperar el fin de la vuelta 1 (~23:00 del sabado).  El techo sale de ahi.
2. Informe de la vuelta 1 y commit de los datos.
3. Edicion (B) + build + grabado.
4. Validacion 1-2-3 de arriba.  Si falla, revertir al tag.
5. Vuelta 2 como validacion del cambio (no como repeticion).
6. Experimento de ruido.
7. Informe final.
