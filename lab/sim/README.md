# Simulador del lazo

El codigo C **real** del firmware (`control_config.c`, compilado tal cual)
contra un modelo de la cadena analogica. No hay reescritura: reimplementar el
PI en Python probaria la reimplementacion, que es justo lo que no sirve.

    gcc -O2 -shared -o lazo.dll shim.c ../../src/firmware/psoc/AcondicionamientoAnalogico.cydsn/control_config.c -I...
    python lab/sim/simulador_lazo.py --escenarios

`shim.c` expone el lazo con tipos primitivos nada mas, para que no haya que
alinear layouts de structs entre C y Python.

## Para que sirve y para que no

Sirve para descartar ideas rapido -una prueba tarda milisegundos contra los 30
a 90 minutos que cuesta en el banco- y para entender mecanismos. **No** sirve
para dar por bueno un arreglo: el modelo es de primer orden y los parametros
tienen incertidumbre. Todo lo que sale de aca se confirma en la placa.

## Parametros de la planta

Medidos con el PI congelado, escalones A-B-A-B-A, permanencias de 360 s:

| | |
|---|---|
| IDAC3 -> LPo | +0,45 mV/codigo (x4/x16: 0,49 · x1/x1: 0,41) |
| IDAC1 -> SUMo | -5,24 mV/codigo |
| IDAC1 -> LPo | +17,79 mV/codigo, o sea LPo/SUMo = -3,40 |
| IDAC2 -> LPo | **+45 mV/codigo** (despejado, no medido directo) |

## El hallazgo que produjo

`CP_COARSE_SLOPE_UV` esta en **-150 mV/codigo** y el valor real parece ser
**+45**: mal en magnitud y **en signo**.

Se despeja de la campana sin tocar la placa. Dos visitas del mismo par de
ganancia, con el mismo par lento y distinto IDAC2, dejan una sola incognita:

    x8/x8 FRIO       dLPo=-57,5  a*dSUMo=-68,0  b*dI3=-77,9  =>  +44,2 mV/cod
    x8/x8 DESDE_X1   dLPo=-64,3  a*dSUMo=-66,0  b*dI3=-90,5  =>  +46,1 mV/cod

Dos comparaciones independientes, 4 % de diferencia.

**Por que el signo importa.** La guarda de SUMo elige la direccion del paso
grueso con el signo de `COARSE_SLOPE_UV`:

    step = ((sum>0)==(v[CP_COARSE_SLOPE_UV]>0)) ? +COARSE_STEP : -COARSE_STEP;

Si el signo esta invertido, la guarda **empuja SUMo para el lado equivocado**.
Encaja con x32/x2, donde SUMo quedo clavado en +90,4 mV mientras la guarda
llevaba IDAC2 hasta -30 codigos sin conseguir nada.

Y encaja con el simulador: con -150 la simulacion deja IDAC3 comodo en +29;
con +45 lo manda a -255, que es lo que hace la placa (-231).

**Falta confirmarlo con un escalon controlado de IDAC2 en la placa**, igual
que se hizo con IDAC3. Hasta entonces es una hipotesis fuerte, no un hecho.
