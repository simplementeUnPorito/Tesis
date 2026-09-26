# Hallazgos del simulador (2026-09-26)

## CONCLUYENTE

**1. "Arreglar" el signo de `CP_COARSE_SLOPE_UV` sin tocar nada mas rompe el
lazo.**  La guarda de SUMo deduce la direccion del paso grueso del SIGNO de
ese parametro.  Simulado desde SUMo = -80 mV:

| COARSE_SLOPE_UV | SUMo final |
|---|---|
| -150000 (config actual) | **+52 mV**, se recupera |
| +11600 | **-601 mV**, se dispara |

Sea cual sea el valor correcto, el signo NO se toca solo.

**2. El lazo fino se congela en un caso concreto y acotado.**  No es que la
guarda de SUMo lo apague siempre: cuando LPo esta contra el riel, el rescate
por biseccion SI corre desde adentro de la guarda.  El caso muerto es
**SUMo fuera de banda Y LPo valido pero corrido**: ahi no hay rescate -LPo no
esta en riel- y la guarda bloquea el PI, asi que nada corrige.  Es exactamente
x8/x8 CONTROL en la placa: LPo +91 mV, IDAC3 en -30, SUMo valido 63 %.
Corregir esos 91 mV pide ~200 codigos de IDAC3 y le sobran.

**3. El estimador de pendiente del propio firmware subestima.**  Contra una
planta con 450 uV/codigo exactos, `pi.slope_uv` converge a ~200.  Mide la
respuesta antes de que la etapa asiente, que es la trampa de la pendiente
instantanea contra la de regimen ya documentada.  Como el PI divide el error
por la pendiente, subestimarla lo vuelve MAS agresivo.

## RETRACTADO

**El signo de `CP_COARSE_SLOPE_UV` NO esta mal.**  Lo afirme sobre un ajuste
de tres parametros hecho con dos fotos sueltas de la campana, que daba un
camino directo de IDAC2 a LPo de +45 mV/codigo.  La topologia lo contradice:
IDAC2 entra por la entrada positiva del operacional, sube SUMo, y **LPo
invierte a SUMo** (medido: -3,40).  Si IDAC2 solo entra por el sumador, su
efecto sobre LPo es NEGATIVO: 9,85 * (-3,40) = **-33,5 mV/codigo**.

Ademas el ajuste no se sostiene solo: forzando "sin camino directo", las dos
ecuaciones dan a = -0,65 cuando la medicion directa da -3,40.  Dos fotos con
ruido y deriva no alcanzan para despejar tres incognitas.

Lo que queda en pie de eso: **la magnitud sigue sospechada** (-150 configurado
contra ~-33 esperado por topologia, factor 4,5).  Importa porque la prediccion
del descargue "sin salto" usa `COARSE_SLOPE/FINE_SLOPE` para compensar un
codigo de grueso con codigos de vernier.

## PENDIENTE DE MEDIR EN LA PLACA

`IDAC2 -> LPo` y `IDAC2 -> SUMo`, con el mismo rigor que se uso para IDAC3:
PI congelado por banda muerta ancha, escalones A-B-A-B-A, permanencias de
360 s, deriva verificada antes de empezar, e inyeccion confirmada leyendo el
codigo de vuelta tras un `ctl report`.  Sin eso, cualquier cambio a la guarda
o al descargue es adivinanza.
