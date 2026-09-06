# Plan para el cambio de resistencias — sesión del lunes

Elías: *"el lunes vamos a hacer todo cambiando las resistencias, dejalo bien
planteado"*.

Este documento es el protocolo. La idea es que la sesión sea **medir, no
decidir**: todas las decisiones ya están tomadas y justificadas acá, y el lunes
sólo se ejecuta y se compara contra el antes.

---

## 1. Qué se cambia y por qué

Los IDAC tienen 8 bits, o sea 255 pasos. Lo que la resistencia fija es **cuánto
vale un paso**, y con eso el compromiso entre **alcance** y **resolución**: más
resistencia es más alcance y menos finura, y al revés.

Medido el 2026-09-05, con la escala verificada con tester (Vdda = 4,826 V):

| etapa | R hoy | paso real | alcance (±255) |
|---|---:|---:|---:|
| ADDER | 15 k | 76,1 mV | ±19,42 V |
| PGA (a ×50) | 15 k | 61,0 mV | ±15,54 V |
| BP | 15 k | 20,0 mV | ±5,09 V |
| LP | 15 k | 10,5 mV | ±2,67 V |

**El alcance parece excesivo contra una alimentación de 4,83 V, y no lo es.** La
corrección tiene que recorrer un offset que, sin corregir, pondría la salida
muy fuera del riel; el tap está recortado durante ese recorrido pero los códigos
que lo atraviesan hacen falta igual. Lo que decide el dimensionamiento es
**cuánto hay que inyectar**, y eso está medido más abajo.

### Los valores propuestos — CORREGIDOS

**Una versión anterior de este plan proponía bajar el ADDER a 2,0 kΩ y el PGA a
2,2 kΩ. ERA UN ERROR: habría inutilizado la única configuración que funciona.**
Elías lo detectó — la resistencia hay que elegirla por **cuánto hace falta
compensar**, no por llenar el rango.

Cuánto se inyecta de verdad, sacado de los códigos que la calibración
efectivamente aplicó en las corridas que cerraron:

| etapa | **máximo inyectado** | autoridad actual | margen |
|---|---:|---:|---:|
| **ADDER** | **−14,62 V** | ±19,42 V | 33 % |
| **PGA (a ×50)** | **+14,30 V** | ±15,54 V | **9 %** |
| LP | 0,29 V | ±2,67 V | 9× |
| BP | 0,00 V | ±5,09 V | sin usar |

| etapa | **R nueva** | motivo |
|---|---|---|
| **PGA** | **dejar 15 kΩ** | usa el 91 % de su autoridad: el más ajustado de los cuatro |
| **ADDER** | **dejar 15 kΩ** | es el actuador grueso y necesita los 14,6 V de alcance |
| **LP** | **1,8 kΩ** | es el fino: paso de 10,5 → **1,18 mV**, 9× más preciso |
| **BP** | dejar 15 kΩ | no se usó en ninguna calibración que cerró |

**El único cambio es el LP.** Su recorrido pasa de ±2,67 V a ±300 mV, que sigue
cubriendo 4 escalones del ADDER: el par grueso+fino encadena sin huecos.

No contradice el criterio de Elías de *"si perdemos rango en LP perdemos
resolución"*: eso es sobre el rango de **señal**, que no cambia. Acá se achica el
rango del **IDAC de corrección**, hoy 9 veces sobredimensionado.

### AGREGADO 2026-09-06: el ADDER gasta el 75 % de su recorrido en llegar

El barrido completo del ADDER en lazo abierto (MEDICIONES §26) mide algo que
antes no se sabía y que cambia la conversación:

| tramo del IDAC del ADDER | qué hace |
|---|---|
| 0 … −135 (≈ 53 % del recorrido) | **nada**: el LP está saturado y no transmite |
| −176 … −240 (≈ 25 %) | la zona útil; Vref cae en **−191** |
| −240 … −255 | contra el riel |

O sea que **el 75 % del recorrido del actuador se gasta en llegar al punto de
operación**, y sólo queda una cuarta parte para corregir. Y el margen hacia
arriba desde Vref son ~15 códigos.

**Esto NO es un argumento para cambiar la resistencia del ADDER.** Al revés: su
alcance en volts es justo lo que hace falta, y achicarlo lo rompería. Lo que
dice el número es otra cosa: **el cero de su referencia está corrido**. Hacen
falta 191 códigos × 1875 µV = **358 mV** para llegar a donde debería estar el
reposo.

Si ese offset se compensara en el hardware —moviendo el cero de la referencia
del ADDER, no su resistencia en serie—, el código 0 sería el centro y quedarían
los ±255 completos para corregir, que es lo que un sistema de calibración quiere.

**Para el lunes, con el esquemático a la vista:** ver de dónde sale el cero de la
referencia del ADDER y si esos 358 mV se pueden mover ahí. Es independiente del
cambio del LP y no interfiere con él; si no se puede, el firmware ya funciona con
el clamp asimétrico, sólo que sin margen de sobra.

---

## 2. La línea de base — REMEDIDA el 2026-09-06

> **Los números de la tabla de abajo son los viejos y quedaron sin efecto.** Se
> midieron con espera fija de 60 s, y esa espera no alcanza para volver de la
> saturación: la misma configuración daba resultados opuestos según de dónde
> viniera la cadena. Se rehizo todo con detección de asentamiento
> (`MEDICIONES_2026-09-05.md` §23). Lo vigente es:
>
> | | valor |
> |---|---|
> | Combinaciones que arrancan railadas | **12 de 14** |
> | Las dos que no | ×1 ×1 (peor tap 128 mV) y ×2 ×1 (426 mV) |
> | Paso del ADDER sobre ch3 | **61,4 mV reales por código** (§26) |
> | Código del ADDER que centra la cadena | **−191** (§26) |
> | El nodo se calibra solo | **sí**, LP a 34 mV de Vref en 579 s (§27) |
>
> Y no hace falta repetirlo a mano: `python -m lunes.t2_sin_calibrar` lo rehace
> entero, y `python -m lunes.t3_cal_firmware` verifica lo último.


Todo esto está en `docs/MEDICIONES_2026-09-05.md` y en `lab/planta/*.json`. El
lunes se compara contra estos números:

| medición | valor con 15 kΩ | dónde |
|---|---|---|
| PGAout máximo estable con PGA ×50 | **×1** | `max_pgaout_pga8_*.json` |
| Modo de fallo dominante para PGAout ≥ ×2 | "ventana más angosta que un código" | ídem |
| Combinaciones que arrancan railadas (de 12) | **10** | `campana_*.json` |
| Error del LP tras calibrar, ×1/×1 | 6,6 mV reales | `campana_analisis.json` |
| Paso del ADDER sobre ch3 | 76,1 mV | §14 |
| Escala del banco | 19,9157 mV reales por mV de banco | `escala_banco.py` |

---

## 3. Protocolo del lunes, en orden — LOS ENSAYOS YA ESTÁN ARMADOS

Todo lo de abajo son comandos que existen y corren. Viven en
`src/interfaces/python/lunes/`, escriben JSON con fecha en `lab/lunes/`, y
llevan metidas como guardas todas las trampas que costaron un ensayo arruinado
el fin de semana: la configuración del ADC se pide explícitamente, cada
`set_idac` se reintenta y se verifica, se espera a que la cadena deje de moverse
en vez de un tiempo fijo, y no se convierten a milivoltios las lecturas de la
zona ciega.

```
cd src/interfaces/python
python -m lunes.correr_lunes antes       # ~10 min, ANTES de tocar el soldador
python -m lunes.correr_lunes despues     # ~25 min, después de cada cambio
python -m lunes.correr_lunes completo    # ~1 h, la batería entera, al final
```

Y cualquier ensayo suelto:

```
python -m lunes.t0_linea_base            # la huella de la placa
python -m lunes.t1_autoridad 2           # la curva completa del ADDER
python -m lunes.t1_autoridad 3           # la del LP
python -m lunes.t2_sin_calibrar          # las 17 combinaciones de ganancia
python -m lunes.t3_cal_firmware          # ¿se calibra solo?
```

### Paso 0 — antes de desoldar (~10 min)

- [ ] **`python -m lunes.correr_lunes antes`.** Corre T0, que registra el punto
      de reposo y las dieciséis pendientes (cada actuador sobre cada tap). Ésa
      es la huella con la que se compara todo lo de después.
- [ ] Con el tester: **Vdda, Vref, LPo (P0[1]) y PGAgain (P2[7])**, anotando la
      lectura simultánea del banco. Verifica que la escala no cambió.
- [ ] `git commit` de todo lo pendiente, para que el antes quede fijado.

### Paso 1 — cambiar SÓLO el LP a 1,8 kΩ

Es el único cambio recomendado: al LP le sobra 9× de rango y le falta
resolución. Es el actuador fino del par grueso+fino.

- [ ] Cambiar la resistencia.
- [ ] **`python -m lunes.correr_lunes despues`.** Corre T0 otra vez y las curvas
      completas del ADDER y del LP.

      **La pregunta que contesta T0**: ¿la pendiente del LP bajó por el mismo
      factor que la resistencia, de ~10,5 mV a **~1,18 mV** por código? *Si no
      bajó por ~9, el problema es el soldado — parar acá.* Y de las otras quince
      pendientes, **ninguna** debería haber cambiado; si cambió alguna, también
      hay que parar.

      **La pregunta que contesta T1**: ¿el recorrido del LP sigue cubriendo un
      escalón del ADDER? Su recorrido tiene que quedar en ~±300 mV contra los
      76 mV del paso del ADDER; si no lo cubriera quedarían huecos que ningún
      código puede alcanzar. T1 lo dice directamente en la línea "RECORRIDO
      ÚTIL".

- [ ] **`python -m lunes.t3_cal_firmware`.** Es el criterio de aceptación: ¿el
      nodo se calibra solo a ×50? Reconstruye además la trayectoria del lazo,
      que es lo que convierte un "no anduvo" en un diagnóstico.

### La cuenta hecha de antemano: el cambio del LP es seguro por cobertura

Antes de soldar conviene saber si el par grueso+fino va a seguir encadenando.
Con los números medidos —el ADDER da **61,4 mV reales por código** sobre ch3
(§26) y el LP a 15 kΩ da **10,46 mV**—:

| resistencia del LP | paso | recorrido | cubre |
|---|---:|---:|---:|
| 15 kΩ (hoy) | 10,46 mV | 5,33 V | **87 pasos del ADDER** |
| **1,8 kΩ** | **1,26 mV** | **0,64 V** | **10,4 pasos** |

Sigue cubriendo con un orden de magnitud de margen, así que **por el lado de los
huecos el cambio es seguro**. Lo que gana es lo que se busca: el paso del fino
baja de 10,5 a 1,3 mV reales, o sea **8,3× más resolución** en el ajuste final.

*(Es una cuenta sobre el papel: supone que el recorrido del LP es usable entero,
y a ×50 con la cadena railada no lo es. `t4_encadenado` lo mide de verdad,
usando el recorrido que el LP logra **en la ventana observable**, que es el que
cuenta. Si T4 y esta tabla no coinciden, la que vale es T4.)*

### Paso 2 — sólo si el paso 1 no alcanza

Antes de tocar cualquier otra resistencia, **medir cuánto se inyecta**. Eso ya
lo da T1: su línea "PUNTO DE VREF" dice con qué código queda centrada la cadena,
y de ahí sale directo el porcentaje del recorrido que se gasta. Entonces:

- si la etapa usa **más del 80 %** de su recorrido → el problema es de
  **alcance**, y hay que **SUBIR** esa resistencia, no bajarla;
- si no pasa del **50 %** → el problema es de **resolución**, y ahí sí se puede
  bajar;
- si gasta más del 40 % **sólo en llegar** al punto de operación → no es la
  resistencia en serie: es el **cero de la referencia**, que está corrido. T1
  avisa solo en ese caso y da los milivoltios que hay que mover.

**No cambiar nada sin ese número.** Fue exactamente el error de la primera
versión de este plan: se dimensionó por el riel en vez de por el trabajo, y las
dos cuentas daban recomendaciones opuestas para la misma etapa.

### Paso 3 — la batería completa (~1 h, desatendida)

- [ ] **`python -m lunes.correr_lunes completo`.** Agrega T2, las diecisiete
      combinaciones de ganancia sin calibrar, con los tres controles de
      reproducibilidad. Es el número que va a la tesis: hoy son **12 de 14**
      combinaciones que arrancan con una etapa contra el riel.
- [ ] `buscar_max_pgaout.py --pares` con reparto de ganancia, para la pregunta
      de si conviene concentrar o repartir. *(Éste todavía no está dentro de la
      batería: usa el criterio viejo de espera fija y conviene migrarlo antes de
      confiar en su resultado.)*

## 4. Criterios de aceptación

| qué | umbral |
|---|---|
| Paso del LP sobre ch3 | baja a ~1,18 mV (verifica que la resistencia es la que se puso) |
| Alcance del LP | queda en ~±300 mV, o sea 4 escalones del ADDER: sigue encadenando |
| **PGAout máximo con PGA ×50** | **> ×1** ← el objetivo principal |
| Combinaciones que arrancan railadas | baja de 10/12 |
| Error del LP tras calibrar | no empeora respecto de 6,6 mV |
| Ninguna etapa satura | **ningún tap fuera de 880,4…1122,7 de banco, con 25 mV de guarda** |

**Elías fue explícito: "ninguna etapa jamás debe saturar".** Ese criterio es
duro y va antes que cualquier otro.

Y el criterio de error del LP hay que **redefinirlo en voltios reales**: los
"20 mV" con los que se venía trabajando eran unidades del banco, o sea **398 mV
reales**. Hay que decidir si el objetivo real es ése o más exigente.

---

## 5. Qué queda pendiente y NO depende de las resistencias

Para no mezclarlo con la sesión del lunes:

- **Por qué el factor de escala es 19,92** y no el 19,073 µV/cuenta del ADC ni el
  32 del `DEC_DIV`. Hay una conversión mal en el camino del banco. La recta está
  medida así que no bloquea, pero conviene encontrarla.
- **Por qué la resolución efectiva del ADC son 380 µV** y no los 19 µV que darían
  18 bits: sobre los 4,83 V útiles entran ~12.700 cuentas, o sea ~13,6 bits. Se
  pierden 4,4 bits en algún lado. Es probablemente la misma causa que lo
  anterior.
- ~~**Por qué la calibración del firmware aborta en 60 s**~~ **RESUELTO la noche
  del 2026-09-05.** Eran cuatro cosas, todas en el firmware que va al campo: la
  espera de planta vivía en una rama de preprocesador que no compila; las
  esperas se cuentan en iteraciones del lazo pero están declaradas en muestras
  del ADC, que son 78 veces más cortas; el lazo no esperaba nada después de
  mover la referencia, así que medía el pasado y se iba al riel; y la curva no
  lineal del LP se le aplicaba también al ADDER, invirtiéndole el signo. Ver
  `docs/MEDICIONES_2026-09-05.md` §17 a §19.
- ~~**Unificar los dos proyectos de PSoC**~~ **HECHO la noche del 2026-09-05.**
  Cada fuente compartida existe una sola vez; `program_psoc.ps1` se niega a
  grabar si alguien vuelve a copiar un archivo.
- **La deriva térmica** (EXP4c), que es la otra mitad del argumento de la tesis:
  justifica que la calibración sea automática y no un trim de fábrica.
- **Rehacer §15** (las 12 combinaciones sin calibrar). La misma configuración
  medida dos veces dio resultados opuestos según de dónde viniera la cadena:
  volver de la saturación tarda mucho más que 2 τ. El reemplazo ya está escrito
  (`sin_calibrar.py` + `src/interfaces/python/asentamiento.py`).

---

## 6. Si algo sale mal

- **Volver a 15 kΩ en la etapa que se acaba de cambiar.** Se cambia de a una
  justamente para que esto sea posible.
- El método conservador de calibración está guardado en
  `src/interfaces/python/calibracion_conservadora.py` y en la rama de git
  `calibracion-conservadora` de los cuatro repos.
- **PGAout ×1 es la red de seguridad**: reproduce la placa que Elías ya validó
  en campo y que funciona.
