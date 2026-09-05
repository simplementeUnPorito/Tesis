# Plan para el cambio de resistencias — sesión del lunes

Elías: *"el lunes vamos a hacer todo cambiando las resistencias, dejalo bien
planteado"*.

Este documento es el protocolo. La idea es que la sesión sea **medir, no
decidir**: todas las decisiones ya están tomadas y justificadas acá, y el lunes
sólo se ejecuta y se compara contra el antes.

---

## 1. Qué se cambia y por qué

Los IDAC tienen 8 bits, o sea 255 pasos. Lo que la resistencia fija es **cuánto
vale un paso**, y con 15 kΩ en las cuatro etapas el recorrido resultante es
mucho mayor que la alimentación: los códigos sobrantes **no existen**, porque el
tap ya está contra el riel.

Medido el 2026-09-05 con la escala verificada con tester (Vdda = 4,826 V):

| etapa | R hoy | paso real | recorrido | **códigos útiles** |
|---|---:|---:|---:|---:|
| ADDER | 15 k | 76,1 mV | ±19,4 V | **63 de 510** |
| PGA (a ×50) | 15 k | 61,0 mV | ±15,5 V | **79 de 510** |
| BP | 15 k | 20,0 mV | ±5,09 V | 242 de 510 |
| LP | 15 k | 10,5 mV | ±2,67 V | 462 de 510 |

### Los valores propuestos

| etapa | **R nueva** | paso nuevo | útiles | motivo |
|---|---:|---:|---:|---|
| **ADDER** | **2,0 kΩ** | 10,2 mV | **475** | es el actuador grueso del LP; hoy desperdicia el 88 % de su rango |
| **PGA** | **2,2 kΩ** | 8,9 mV a ×50 | **510** | su paso escala con la ganancia y a ×50 es inusable |
| **BP** | **6,8 kΩ** | 9,1 mV | **510** | es el actuador fino más barato (11:1 a favor) |
| **LP** | **dejar 15 kΩ** | 10,5 mV | 462 | ya está bien dimensionado |

Criterio: que ±255 códigos cubran ~±2,5 V, o sea media alimentación a cada lado.
Todos son valores comerciales E24, 1 %.

**El LP no se toca.** Es el único donde el rango es resolución de señal y no
sólo margen de continua — Elías: *"si perdemos rango en LP perdemos
resolución"*.

### Riesgo y cómo se acota

El único riesgo real es quedarse **corto de autoridad** en alguna combinación
extrema. Se acota con el orden de trabajo: se cambia **primero el ADDER solo**,
se repite la batería, y recién si mejora se siguen los otros. Si algo empeora,
se vuelve a 15 kΩ en esa etapa y se sabe exactamente cuál fue.

---

## 2. La línea de base — YA ESTÁ MEDIDA, no hay que repetirla

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

## 3. Protocolo del lunes, en orden

### Paso 0 — antes de desoldar (30 min)

- [ ] `python -m testbench run --port COM8` → guardar el JSON. Es la foto del
      estado sano antes de tocar nada.
- [ ] Con el tester: **Vdda, Vref, LPo (P0[1]) y PGAgain (P2[7])**, anotando la
      lectura simultánea del banco. Verifica que la escala no cambió.
- [ ] `git commit` de todo lo pendiente, para que el antes quede fijado.

### Paso 1 — cambiar SÓLO el ADDER a 2,0 kΩ

Es el que más gana (63 → 475 códigos útiles) y el que explica el modo de fallo
dominante.

- [ ] Cambiar la resistencia.
- [ ] **Verificar el paso**: `medir_escalado_pgaout.py --pga 8 --outs 0`.
      Esperado: el paso del ADDER sobre ch3 baja de 76,1 mV a **~10,2 mV**.
      *Si no baja por ~7,5, algo salió mal — parar y revisar antes de seguir.*
- [ ] `buscar_max_pgaout.py --pga 8 --outs 0,1,2,3,4,5,6,7,8`
      **La pregunta que contesta: ¿sube el PGAout máximo de ×1?**

### Paso 2 — cambiar el PGA a 2,2 kΩ

- [ ] Cambiar y verificar el paso a ×50 (esperado ~8,9 mV/código).
- [ ] Repetir `buscar_max_pgaout.py`.
- [ ] `campana --rapido` para ver cuántas combinaciones dejan de arrancar
      railadas. **Es el número de la tesis.**

### Paso 3 — cambiar el BP a 6,8 kΩ

- [ ] Cambiar y verificar.
- [ ] `calibrar_permisivo.py --pga 8 --outs 0,1,2,3` — el método que usa el BP
      como actuador fino. Es donde el cambio del BP debería lucirse.

### Paso 4 — la batería completa

- [ ] `campana --rapido` sobre las 81 combinaciones (~90 min, desatendida).
- [ ] `buscar_max_pgaout.py --pares` con reparto de ganancia, para la pregunta
      de si conviene concentrar o repartir.
- [ ] `python -m testbench run` final y comparación contra el paso 0.

---

## 4. Criterios de aceptación

| qué | umbral |
|---|---|
| Paso del ADDER sobre ch3 | baja a ~10 mV (verifica que la resistencia es la que se puso) |
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
- **Por qué la calibración del firmware aborta en 60 s** con `ok=0`, cuando con
  2 τ debería tardar ~240 s.
- **La deriva térmica** (EXP4c), que es la otra mitad del argumento de la tesis:
  justifica que la calibración sea automática y no un trim de fábrica.
- **Unificar los dos proyectos de PSoC**: hoy la calibración está duplicada y
  divergida en 370 líneas, y eso ya causó que el autotest tuviera una versión
  vieja.

---

## 6. Si algo sale mal

- **Volver a 15 kΩ en la etapa que se acaba de cambiar.** Se cambia de a una
  justamente para que esto sea posible.
- El método conservador de calibración está guardado en
  `src/interfaces/python/calibracion_conservadora.py` y en la rama de git
  `calibracion-conservadora` de los cuatro repos.
- **PGAout ×1 es la red de seguridad**: reproduce la placa que Elías ya validó
  en campo y que funciona.
