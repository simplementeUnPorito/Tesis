# Cómo pasa a firmware el centrado por bisección

## Por qué este algoritmo se porta y el PI no

El PI que hay hoy en `calibration.c` necesita, para dar un paso, una ganancia de
planta en milivolts por código. La saca de `g_cal_geo_lp_delta_counts`, una curva
medida el 2026-09-03 que resultó estar **once veces por debajo** de la autoridad
real de IDAC3, porque se levantó con la etapa saturada. Un PI con la ganancia mal
estimada por un factor once no converge: o se arrastra o se va al riel, que es
justo lo que se vio los días 12 y 13.

La bisección no usa ninguna ganancia. Sólo pregunta si el tap está por encima o
por debajo de su centro, y esa pregunta se contesta bien incluso con la etapa
contra el riel, porque la saturación conserva el signo. Eso la vuelve inmune al
modo de falla que tiene hoy el firmware.

## Lo que necesita del firmware ya existe

| primitiva | comando | dónde |
|---|---|---|
| escribir un IDAC con signo | `0xA2` | `st_handle_set_idac` en `psoc_selftest.h` |
| medir un tap en continua | `0xA4` | `st_handle_meas_dc` |
| cambiar PGAout | `PSOC_CMD_PGAOUT` | `main.c` |

No hace falta ninguna primitiva nueva, ni punto flotante, ni tabla de
transferencia. El bucle entero son enteros de 16 bits y una comparación de signo.

## El bucle, en la forma en que va a quedar en C

```c
/* Devuelve el codigo que deja el tap mas cerca de su centro. Solo usa el
 * signo de la medida: no necesita saber cuanto mueve el actuador ni en que
 * sentido, y funciona con el tap contra el riel. */
static int16 cal_bisectar(uint8 etapa, uint8 canal, int16 bajo, int16 alto)
{
    int32 v_bajo = cal_sondar(etapa, bajo, canal);
    int32 v_alto = cal_sondar(etapa, alto, canal);
    uint8 subiendo;

    if ((v_bajo > 0) == (v_alto > 0)) {
        return (abs_counts(v_bajo) < abs_counts(v_alto)) ? bajo : alto;
    }
    subiendo = (v_alto > v_bajo) ? 1u : 0u;
    while (alto - bajo > 1) {
        int16 medio = (int16)((bajo + alto) / 2);
        int32 v = cal_sondar(etapa, medio, canal);
        if (((v > 0) ? 1u : 0u) == subiendo) { alto = medio; }
        else                                 { bajo = medio; }
    }
    return bajo;
}
```

`cal_sondar` escribe el código, espera el tiempo de asentamiento de esa etapa y
devuelve la media en cuentas. Trabajar en cuentas y no en microvolts evita la
conversión y el error de escala: el signo es el mismo en las dos unidades.

## El presupuesto de pasos, que es lo que fija el tiempo

Trece sondeos por bisección: dos extremos, nueve pasos y dos de desempate. Con
seis segundos de asentamiento son ochenta segundos por actuador. La secuencia
completa en el nodo:

1. Aplicar el punto guardado en NVS para la ganancia pedida.
2. Esperar tres constantes de tiempo del pasabanda, unos noventa segundos.
3. Bisectar IDAC3 sobre LPo.
4. Si IDAC3 no encierra el cero, bisectar IDAC2 y volver a IDAC3.
5. Si IDAC3 quedó fuera de su zona cómoda, correrlo con IDAC2 y rebisectar.
6. Verificar que los cinco taps estén dentro de ventana y guardar el punto.

## Dos cosas que hay que arreglar en el firmware antes

1. **`g_cal_geo_lp_delta_counts` está mal.** Subestima a IDAC3 en un orden de
   magnitud. Hay que volver a levantarla con la etapa dentro de la ventana, o
   directamente borrarla: la bisección no la necesita y es la única que la usa.
2. **No calibrar al bootear.** El nodo tiene que esperar el pedido explícito del
   operador. Arrancar una bisección sola después de un reset deja los IDAC
   moviéndose mientras alguien está midiendo con el osciloscopio.

## Corrección al orden de actuadores, tras medirlo en la placa

La primera versión de este documento decía que el nivel grueso era IDAC0. **Es
IDAC1.** IDAC0 no tiene autoridad de continua sobre el sumador porque el
capacitor de 680 µF del pasabanda la bloquea; los 244 mV por código que informa
la fase 1 son el resto de un transitorio, no una ganancia. Medido el 2026-09-13:
treinta y un códigos de IDAC0 movieron ch2 trece milivolts.

La jerarquía que va al firmware es entonces:

| nivel | actuador | contra qué tap | espera por sondeo |
|---|---|---|---|
| grueso | IDAC1 (Vref_BP) | ch2 | 2 τ, unos 58 s |
| medio | IDAC2 (Vref_ADDER) | ch2, y después LPo | 6 s |
| fino | IDAC3 (Vref_LP) | LPo | 6 s |

IDAC0 queda para lo que sí gobierna: el punto de trabajo del PGA, o sea ch0. Es
lo que hace la fase 1 y está bien que lo haga.

## Segunda corrección: tres métodos, no uno, y esperas entre niveles

Las mediciones de la madrugada obligan a corregir otra vez este documento. La
jerarquía final que va a firmware es:

| paso | actuador | tap objetivo | método | espera |
|---|---|---|---|---|
| 1 | IDAC0 | ch0 (SEo) | fase 1, ya existe | — |
| 2 | IDAC1 | ch2 (OPA_SUMo) | **barrido monótono de una sola pasada** | 1,5 τ por punto |
| 3 | IDAC2 | ch3 (SUMo) | bisección de signo | 6 s por sondeo |
| 4 | IDAC3 | ch4 (LPo) | bisección de signo | 6 s por sondeo |

Y entre el paso 2 y el 3 hay que **esperar tres constantes de tiempo**, porque el
último escalón del actuador lento sigue llegando y contamina todo lo que el
rápido mida encima.

### Por qué el paso 2 no puede ser una bisección

Dos razones, las dos medidas:

1. **La bisección salta.** Su primer movimiento es de medio rango, y sobre un
   camino con τ de treinta segundos ese salto deja un transitorio que tapa las
   lecturas siguientes por minutos.
2. **Volver no restaura.** El barrido subió de −96 a +4 dando una recta limpia;
   al retroceder al mismo −16 que había leído +320 mV, leyó riel, y siguió en el
   riel ocho minutos. La absorción dieléctrica del acople de 680 µF hace que la
   vuelta no sea simétrica con la ida.

De ahí la regla, que en C es una línea: al detectar el cruce, **quedarse donde se
está**. Nunca volver al punto anterior aunque tuviera menor error. Lo que se
pierde en precisión lo absorbe el nivel siguiente, que tiene ±2,3 V de recorrido
contra un paso de 76 mV.

## Tercera y última corrección: la estructura que quedó funcionando

Verificada en placa el 2026-09-13 a las 08:53, con los cinco taps dentro de
ventana y LPo a 35 mV de su centro.

```c
/* 1. Fase 1: IDAC0 centra ch0. Ya existe. */

/* 2. Buscar el PAR (IDAC1, IDAC2). No sirve fijar uno y buscar con el otro:
 *    el estado lo determina el par. Por cada codigo de IDAC1 -caro, porque
 *    pasa por el pasabanda- se recorre IDAC2 entero -barato, asienta en ms-. */
for (c1 = base1 - ancho; c1 <= base1 + ancho; c1 += paso1) {
    cal_set_idac(1, c1);
    cal_esperar_quieto(CH_OPA_SUM);            /* no un tiempo fijo */
    for (c2 = -255; c2 <= 255; c2 += 32) {
        v = cal_sondar(2, c2, CH_SUM);         /* 6 s alcanza: es rapido */
        if (abs(v) > TOL_CH3) { continue; }
        cal_esperar_quieto(CH_SUM);            /* CONFIRMAR asentado */
        v = cal_medir(CH_SUM);
        if (abs(v) <= TOL_CH3) { goto encontrado; }
    }
}
/* 3. IDAC3 sobre LPo por biseccion de signo. */
c3 = cal_bisectar(3, CH_LP, -255, 255, TOL_LPO);
/* 4. Un minuto sin tocar nada, y verificar los CINCO taps. */
```

Las tres reglas que no se pueden omitir, cada una comprada con una corrida
fallida:

1. **Esperar a que el tap deje de moverse, no un tiempo fijo.** La respuesta
   asentada de IDAC1 sobre el sumador es setenta veces la instantánea.
2. **Confirmar el candidato con la cadena quieta.** Tres candidatos que leían
   dentro de ventana durante el transitorio murieron contra un riel al asentarse.
3. **Una lectura válida no es una lectura buena.** El riel de ch3 cae adentro de
   la ventana del ADC; hay que exigir además una tolerancia.

## Dos errores de DATOS en el firmware, para cuando se haga el porte

No se tocaron hoy —el alcance del día quedó en que el algoritmo funcione, en PC
o en placa— pero están localizados y son de la misma familia que el de la
portadora JitX: el firmware modela un hardware que no es el que hay.

**1. `CAL_IDAC_UV_PER_LSB` vale 1875 µV para las cuatro etapas.** Está en
`calibration_tables.h:88`. Es correcto sólo para las etapas 0 y 1, que tienen
15 kΩ y rango de 32 µA. Las otras dos no:

| etapa | R | rango | µV por LSB real | el firmware usa |
|---|---|---|---|---|
| 0, 1 | 15 k | 32 µA | 1.875 | 1.875 ✓ |
| 2 | 1,5 k | **255 µA** | **1.500** | 1.875 |
| 3 | 10 k | 32 µA | **1.250** | 1.875 |

La infraestructura para arreglarlo ya existe: `psoc_hw.c` tiene las cuatro
resistencias y `psoc_idac_stage_code_to_uv_signed(stage, code)` las usa. Lo que
falta es que `calibration.c` deje de usar la constante plana en sus dos usos,
líneas 1283 y 1342, que además son los dos del camino del pasabajos.

**2. La curva `g_cal_geo_lp_delta_counts` subestima a IDAC3 once veces.**
`calibration.c:1296`. Medida el 2026-09-03 con la etapa contra el riel, da
0,58 mV por código; medida el 2026-09-13 con la etapa dentro de ventana da
**6,68**. El clamp que la acompaña, `[200, 850]`, arrastra el mismo error: con
los 6,68 medidos y los 1.250 µV por LSB reales de la etapa, la ganancia de
cuerda son **5.344**, seis veces el techo del clamp.

Lo más simple y más honesto es borrar la curva y poner la constante medida: la
respuesta resultó lineal, y una tabla de dieciséis puntos tomada en saturación
sólo da una falsa sensación de detalle.
