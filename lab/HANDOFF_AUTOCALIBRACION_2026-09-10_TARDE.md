# Handoff autoritativo — autocalibración GEO, 2026-09-10 tarde

> **Reemplaza** a `HANDOFF_AUTOCALIBRACION_AUTORITATIVO_2026-09-09.md` y a
> `DIAGNOSTICO_AUTORIDAD_Y_CENTRADO_2026-09-10.md` en todo lo que se contradiga.
> Esos documentos siguen siendo historia útil; no son estado.

## 1. Lo que quedó refutado hoy, con su evidencia

| Afirmación anterior | Estado | Evidencia |
|---|---|---|
| IDAC2 tiene 10 kΩ | **falsa**, son 5,1 kΩ | código de colores, TopDesign, inspección, óhmetro 4,9 kΩ con placa apagada |
| `d(ch2)/d(IDAC2) = 9,56 mV/código` | **falsa**, son ~5,1 | ABBA en 14 bloques de IDAC1, dos pasadas, `mapear_alcance_sumador_20260910_133605.csv` |
| 100/100 cambios de ganancia PASS | **falsa** | re-puntuación: 0/100 sobreviven, `REPUNTUACION_ENDURANCE_2026-09-10.md` |
| LPo "legible en todas las ganancias" | **falsa**, estaba clavado al riel | pico a pico de 114 µV contra 1125–3166 µV de los demás taps |
| Hace falta cambiar resistencias | **falsa** | ver §4 |
| El déficit venía de un cero DC del sumador | **falsa** | ver §3 |

Regla de higiene que sale de esto: **ningún barrido monótono corto mide
pendiente en esta cadena**. Con τ ≈ 29,5 s, una barrida de ±8 códigos con 90 s
de espera dio pendientes de +6,81 a −7,41 mV/código según el bloque, o sea que
cambiaba de signo. Sólo valen ABBA y esperas hasta estabilidad observada.

## 2. Constantes medidas, todas por ABBA salvo donde se indica

```
sumador desde SEo, continua     a = 3,97      27k/6,8k, del esquematico
sumador desde BPo, continua     b = 4,16      ABBA
ganancia no inversora           n = 8,58
IDAC0 -> ch0                   49,7 mV/codigo
IDAC1 -> ch1                    2,0 mV/codigo
IDAC2 -> ch2                    5,1 mV/codigo   prediccion previa 5,26
etapa LP desde ch2             -9,07 mV/mV      R2 = 0,993
R de IDAC2                      5,1 kOhm        ohmetro 4,9 con placa apagada
tau dominante del pasabanda    ~29,5 s          = R4*C1 = 43k * 680uF
riel alto de LPo             1106,1 mV de banco = 4,50 V
riel bajo de LPo                0,040 V         tester
Vref                            Vdda/2, hoy 2,48 V con Vdda = 4,96 (USB)
```

Vistas en ch2, que es lo que importa para la fase 2:

```
IDAC0   197,3 mV/codigo   alcance 50,3 V    el GRUESO de verdad
IDAC1     8,3 mV/codigo   alcance  2,12 V   limitado por +-0,51 V sobre ch1
IDAC2     5,1 mV/codigo   alcance  1,30 V   el FINO
```

**IDAC1 no es un actuador grueso**: su paso es apenas 1,6 veces el de IDAC2. La
idea de "IDAC1 grueso, IDAC2 fino" que circuló durante el día es falsa.

## 3. Asimetría de velocidad, que es la clave operativa

El sumador y el pasabajos asientan en milisegundos. El único elemento lento de
la cadena es el pasabanda, por su capacitor de acople. Por lo tanto:

- mover IDAC2 o IDAC3 **no requiere esperar nada**
- mover IDAC0 o IDAC1 obliga a esperar entre 2 y 5 τ

Eso es lo que hace rápida a la fase 2 y lo que hace cara a la fase 1.

## 4. Por qué no se cambian las resistencias

Con x24 como techo comprometido, y como PGAout está referenciado al mismo Vref:

```
SUMo - Vref = G * (ch2 - Vref)      ->   |ch2| max = (2000 - 250)/G  mV
```

o sea 1500 mV en x1 y 62 mV en x24. El paso de IDAC2 con 5,1 kΩ es de 5,1 mV,
así que la cuantización deja ±2,6 mV contra un presupuesto de 62. Sobra un
factor de veinte. Con 10 kΩ el paso sería 10,3 mV y medio paso ya se come un
sexto del presupuesto de la ganancia más alta. **La resolución que parecía un
lujo es el requisito.** El alcance lo aportan IDAC0 e IDAC1.

## 5. Criterio de aceptación fijado por Elías

- **Único requisito duro**: ningún tap toca el riel, evaluado sobre `media ± pp/2`,
  con 250 mV de margen. Aplica a los cinco taps por igual.
- **LPo se minimiza y se informa**, nunca hace fallar.
- **Fase 1** debe dejar ch0 y ch1 a más de 1 V de ambos rieles. 1,5 V es
  deseable; 2 V es inviable porque el centrado perfecto sólo deja 2,23 V.
- **Rango comprometido x1..x24**; x32/x48/x50 son mejor esfuerzo y se validan
  con una amplitud de señal acorde a cada uno.
- **Tiempos**: pasabanda entre 2 y 5 τ del τ medido; el resto, decenas de segundos.
- **Ganancia fija por campaña**: la fase 2 corre una sola vez, no por disparo.
- **No calibrar al bootear**: el nodo espera el pedido del operador, que avisa
  cuando el geófono está plantado y quieto. Esto exige cambiar el firmware, que
  hoy autocalibra al arrancar y rechaza configs entre 10 s y 4 min.
- **Si no hay punto factible**: usar el último guardado si su puntaje es mejor,
  marcar la bandera y mandar los datos para saber qué tan mal está el nodo.

Puntaje escalar, para poder ordenar dos estados:

```
puntaje = menor margen al riel entre todos los taps, sobre media +- pp/2
desempate = menor |error de LPo|
```

## 5.bis El error de signo, y por que la validacion a mano no lo vio

El sumador es INVERSOR desde sus dos entradas, asi que subir IDAC0 o IDAC1 BAJA
ch2. Los coeficientes de ch2 son negativos:

```
d(ch2)/d(IDAC1) = -7,61 mV/codigo   mediana de 52 tramos vivos del mapa,
                                    negativa en las dos pasadas y en los siete
                                    valores de IDAC2
d(ch2)/d(IDAC0) = negativo tambien, por el mismo camino inversor
```

Durante el desarrollo se escribieron como POSITIVOS. El optimizador eligio en
consecuencia el sentido equivocado, y al aplicarlo en placa ch2 subio hasta
clavarse en el riel en vez de bajar.

Lo importante de este episodio no es el signo sino como se detecto. El punto
optimo se habia "validado" comparandolo contra un calculo hecho a mano... que
usaba el MISMO signo equivocado. Las dos cuentas coincidieron perfectamente y no
probaron nada. **Dos derivaciones que comparten una premisa no se validan entre
si.** Lo que lo detecto fue el hardware, y lo atajo la guarda de aceptacion
nueva, que marco FAIL en vez de declarar exito.

## 5.ter Las constantes del modelo NO pueden estar escritas a mano

`d(ch0)/d(IDAC0)` dio +49,7 mV/codigo en el brazo ABBA del mapa y 85,0
realizado en la corrida de validacion, con la planta asentada. Setenta por ciento
de diferencia. La hipotesis es que el ABBA rapido mide la respuesta EN BANDA,
donde el sumador cancela por diseno, y no la de continua, que es la que usa una
fase 1 que espera tau.

Con varios nodos esto empeora: cada placa tendra las suyas. El diseno correcto es
que la fase 1 MIDA las pendientes rapidas (ch0 y ch1 no arrastran el tau del
pasabanda, asi que cuestan segundos) y derive las de ch2 con las relaciones de
resistencias del sumador, que si son estables entre placas.

## 6. Requisito nuevo, descubierto por accidente

Alguien pateó el geófono en el laboratorio y la cadena quedó apoyada contra el
riel. Con PGA en x50 un golpe satura la entrada, y con τ de 29,5 s la
recuperación tarda minutos. **En campo alguien va a pasar caminando al lado de
un sensor**, así que la autocalibración tiene que sobrevivir a un tap clavado:
prohibido identificar pendientes sobre él, y hay que rescatarlo con el
coeficiente documentado antes de medir nada.

## 6.bis La etapa LP, medida la noche del 2026-09-10

Es un **MFB** (realimentacion multiple), con `LPm_ref` en la pata no inversora y
un capacitor de 47 nF que vuelve a Vref. En continua los dos capacitores son
abiertos, asi que **ese 47 nF no fija el punto de reposo**, y como por la
resistencia hacia LPm no circula corriente, el nodo interno queda en `LPm_ref`.
Por eso IDAC3 llega a LPo amplificado por la red y no directo.

Numeros medidos con ch2 centrado en -7,4 mV y barrido completo de IDAC3:

```
ganancia desde Vref_LP hacia LPo      ~37    (510 codigos mueven el nodo 64 mV
                                              y LPo 2385 mV, con R = 1 kOhm)
ganancia desde ch2 hacia LPo          -9,07  (mapa, R2 = 0,993)
offset propio de la etapa             ~1,05 V, con ch2 y SUMo centrados
```

El offset se explica por la **corriente de polarizacion del operacional por los
150 kOhm de realimentacion**: 200 nA por 150 k son 30 mV en la entrada, que por
37 dan 1,1 V en la salida. Si es eso, es un offset FIJO y no una deriva: IDAC3 lo
cancela una vez.

### IDAC3 es fuertemente NO lineal

En el barrido con 1 kOhm el paso vale unos 11 mV/codigo en el extremo negativo y
0,9 en el positivo: doce veces de diferencia, con residuo de 280 mV contra una
recta. **El lazo de IDAC3 tiene que usar la pendiente LOCAL**, medida donde este
trabajando, nunca una constante.

### Eleccion de la resistencia de IDAC3

| R | alcance sobre LPo | paso cerca del punto | error final |
|---|---:|---:|---:|
| 10 kOhm | ~24 V | 230 a 700 mV | +-115 a +-350 mV |
| 1 kOhm | 1,02 V | ~4,3 mV | +-2 mV, pero NO ALCANZA a cancelar el offset |
| 2 kOhm | ~2,0 V | ~8,6 mV | +-4 mV, cancela el offset con la mitad del rango |

Con 10 kOhm IDAC3 actuaba como llave; con 1 kOhm se queda sin alcance a 733 mV de
LPo. **2 kOhm es el valor elegido.** Elias solto un zocalo para cambiarla rapido.

## 6.ter La vuelta completa sobre IDAC3, y el error que la causo

Secuencia de recomendaciones sobre la resistencia de IDAC3 en una sola noche:

    10 kOhm (original)  ->  "inutilizable, actua como llave"   -> bajar a 1 k
    1 kOhm              ->  "sin alcance ni para el offset"    -> subir a 2 k
    2 kOhm              ->  "tampoco alcanza"                   -> subir a 4,7 k
    4,7 kOhm            ->  "alcanza si ch2 absorbe el offset"  -> quedarse en 1 k
    1 kOhm en placa     ->  x24 sin alcance, medido            -> volver a 10 kOhm

**Se termino donde se empezo.** La causa es siempre la misma y esta escrita mas
arriba en este mismo documento: *una pendiente medida sobre un tap clavado no es
una pendiente*. El barrido de IDAC3 con 10 kOhm dio 230 a 700 mV/codigo, pero se
hizo con LPo contra el riel: lo que se midio fue la transicion entre dos
saturaciones. La medicion limpia, con ch2 centrado y 1 kOhm, dio 4,3 mV/codigo
cerca del punto de trabajo, que escalado a 10 kOhm son 43, no 700. Dieciseis
veces menos.

Numeros validos, todos con ch2 centrado:

```
paso de IDAC3 con 1 kOhm, local     4,3 mV/codigo
autoridad con 1 kOhm, A CADA LADO   510 mV   (el recorrido total es 1020)
LPo que hay que cancelar en x24     ~4083 mV
factor que falta con 1 kOhm         8
con 10 kOhm: autoridad 5100 mV, paso 43 mV/codigo, error final +-21 mV
```

**Lo que NO se pierde de toda la vuelta.** El reparto de trabajo entre
actuadores, la consigna de ch2 apuntando al valor que centra LPo en vez de a
Vref, el rescate de LPo desde riel por biseccion, y los ocho defectos corregidos.
Nada de eso dependia del valor de la resistencia.

## 6.quater Los ocho defectos corregidos el 2026-09-10

Todos de la misma familia: **un numero fisico que el hardware contradice**.

1. signo de los coeficientes de ch2: el sumador es inversor desde sus dos
   entradas, estaban escritos positivos
2. asimetria de polaridad de IDAC0: 89 mV/codigo hacia negativos, 51 hacia
   positivos
3. paso de IDAC1 errado 2,6 veces
4. objetivo de ch2 derivado solo de los rieles de SUMo, ignorando la etapa LP
5. el mismo objetivo, despues, ignorando el offset propio de la etapa LP
6. la semilla historica pisando una medicion fresca de la fase 1
7. la aceptacion comparando el margen contra CERO en vez de contra los 250 mV
   exigidos: el criterio existia y no se aplicaba
8. la consigna del lazo de ch2 apuntando a Vref cuando debia apuntar al valor
   que centra LPo

Y uno de metodo, que vale mas que los ocho: **el punto optimo se "validó"
comparandolo contra un calculo a mano que usaba el mismo signo equivocado**. Dos
derivaciones que comparten una premisa no se verifican entre si. Lo detecto el
hardware.

## 6.quinquies VEREDICTO MEDIDO sobre 1 kOhm en IDAC3

Campana de arranques en frio detenida a los tres intentos porque el dato ya era
concluyente. Evidencia en `lab/arranque_frio/ARRANQUE_FRIO_20260910_203355.csv`
y sus JSON por intento.

| intento | modo | ganancia | resultado | LPo logrado |
|---:|---|---:|---|---:|
| 1 | aleatorio | x1 | PASS | -582 mV |
| 2 | golpe | x2 | FAIL | — |
| 3 | aleatorio | x4 | FAIL | — |

El intento 3 es el decisivo porque fue en modo aleatorio, sin golpe que lo
ensuciara. Fallo con `lpo_rescate_fallido`: la biseccion recorrio los 511 codigos
de IDAC3 y no encontro NINGUN punto donde LPo estuviera vivo.

**El corte de 1 kOhm esta en x4, no en x16 como se esperaba.** Sirve unicamente
en x1. Con el rango comprometido x1..x24, no alcanza.

**Decision: volver a 10 kOhm.** Da 5100 mV de autoridad a cada lado y 43
mV/codigo de paso local, o sea +-21 mV de error final de centrado en todas las
ganancias. Elias dejo un zocalo, asi que el cambio son dos minutos.

Estado de la placa al cierre: PGA x50, PGAout x1, los cuatro IDAC en cero,
puerto cerrado, sin procesos activos.

## 6.sexies COMO RETOMAR: un paso de mano y un comando

**Paso fisico, unico bloqueante:** poner 10 kOhm en el zocalo de IDAC3.
Esta puesta 1 kOhm, que se midio insuficiente (corte en x4).

**Despues, un solo comando:**

```
cd src/interfaces/python
py -3 endurance_arranque_frio.py --port COM8 --intentos 60        --ganancias-por-intento 1 --gains 24,16,32,50,8,4,2,1        --reset-cada 4 --modo mixto --max-h 8
```

El orden de `--gains` es la PRIORIDAD fijada por Elias: las altas primero,
porque son las del martillo lejos. Si la campana se corta, lo cubierto es lo que
mas importa.

Antes de largarla conviene una validacion corta, que tarda unos 15 min:

```
py -3 autocalibracion_dos_fases.py calibrate-gains --port COM8 --gains 24,1
```

Tiene que cerrar las dos. Si x24 falla con `lpo_rescate_fallido`, la resistencia
no quedo bien puesta: ese es exactamente el sintoma de falta de alcance en IDAC3.

**Prediccion contra la que contrastar**, escrita antes de medir: con 10 kOhm el
error final de LPo debe quedar en unos +-22 mV y ser INDEPENDIENTE de la
ganancia, porque IDAC3 actua despues de PGAout. Si sale dependiente de la
ganancia, el limitante no es IDAC3 sino la cuantizacion de IDAC2 propagandose, y
ahi la que hay que mirar es la resistencia de IDAC2.

## 7. Lo que NO se sabe

- El equilibrio real de la cadena en reposo. Dos veces hoy se tomó por reposo lo
  que era transitorio de encendido. Hay una corrida de 14 min en marcha para eso.
- Si la fase 1 nueva converge en placa. Está escrita y con pruebas sin hardware,
  sin validar contra hardware todavía.
- Nada sobre otros nodos: todo esto es una placa.
- El `ToggleReset` del KitProg resetea el chip pero **no corta la alimentación**,
  así que la rampa de la fuente al encender queda sin probar.

## 8. Archivos

- `src/interfaces/python/autocalibracion_dos_fases.py` — implementación vigente
- `src/interfaces/python/mapear_alcance_sumador.py` — mapa con ABBA
- `src/interfaces/python/analizar_mapa_sumador.py` — informe del mapa
- `src/interfaces/python/repuntuar_endurance.py` — re-puntuación del historial
- `src/interfaces/python/escala_banco.py` — escala, rieles y `clavado()`
- `scripts/autonomia/device_reset.py` — reset del PSoC por KitProg, ya validado
