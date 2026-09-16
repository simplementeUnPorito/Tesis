# Registro de banco: resistencias y AMux de seis canales — 2026-09-07

## Hallazgo manual corregido

Con `PGA = x50`, `PGAout = x16`, dos resistencias de conversión de `33 kΩ` y
los cuatro IDAC en los códigos con signo:

```text
[5, 50, 255, 255]
```

se consiguió centrar parcialmente la cadena. Este dato corrige la hipótesis
anterior de que reducir esas resistencias era necesariamente la dirección
correcta: en esta placa el límite observado fue falta de autoridad para sacar
la cadena del riel. Aumentar la resistencia aumentó la excursión por código y
permitió un punto de trabajo que antes no aparecía.

Estado de la evidencia: **prueba manual útil, no autocalibración validada**. No
se registraron todavía tensiones de cada tap, margen a ambos rieles, estabilidad
temporal ni repetibilidad después de reiniciar. La asociación física exacta de
las dos resistencias de 33 kΩ debe confirmarse por designador antes de cerrar el
BOM; en el software de banco se modelan provisionalmente como las referencias
ADDER y LP, que son las dos que se venían cambiando.

Próxima prueba propuesta por Elías: reemplazar esas dos resistencias por
`47 kΩ` y repetir el ajuste manual. Debe compararse autoridad ganada contra
resolución perdida y comprobar que ningún extremo exceda el rango eléctrico de
la etapa/IDAC. No se registra `47 kΩ` como valor instalado ni aprobado hasta
tener la medición.

## Nuevo orden de AMux_ADC

| Canal | Señal | Descripción |
|---:|---|---|
| 0 | `PGAgain_mux` | salida de PGAgain |
| 1 | `BPo_mux` | salida del pasabanda |
| 2 | `OPA_SUMo` | salida del sumador antes de PGAout |
| 3 | `SUMo_mux` | salida después de PGAout |
| 4 | `LPo_mux` | salida del pasabajos |
| 5 | `AMuxCapacitor` | capacitor auxiliar del AMux |

Se desplazaron `SUMo`, `LPo` y `AMuxCapacitor`; `PGAgain` y `BPo` no cambian.
El proyecto `AcondicionamientoAnalogicoTest` ya contiene este TopDesign. El
proyecto de campo todavía debe recibir la misma modificación gráfica antes de
poder compilar con el mapa nuevo.

## Trabajo de calibración deliberadamente pendiente

No se implementó todavía una nueva ley de autocalibración. La próxima versión
debe tratar el tramo BP/sumador como una optimización con restricción:

1. minimizar el error de `BPo_mux`, por ser la señal de mayor amplitud;
2. observar simultáneamente `OPA_SUMo` y rechazar movimientos que lo acerquen a
   saturación;
3. recién entonces evaluar `SUMo_mux` post-PGAout y continuar hacia `LPo_mux`;
4. validar el criterio con `PGA x50` y `PGAout x16`, incluyendo reinicio y
   deriva, antes de habilitarlo en campo.

Por ahora el firmware conserva la secuencia existente y únicamente cambia los
índices físicos: la calibración final que antes observaba `LPo` en ch3 ahora lo
observa en ch4. `OPA_SUMo` queda accesible desde la interfaz y reservado como
guarda para el algoritmo futuro.

## Implementación y verificación

- El mapa quedó centralizado en `psoc_hw.h` y el build GEO exige seis canales,
  para que un TopDesign viejo no intercambie silenciosamente LPo y el capacitor.
- La captura y las etapas `GEO_SUM_LP`/`GEO_LP` ahora observan ch4.
- El autotest PSoC informa seis canales y permite medir cualquiera de ellos.
- El ESP distingue cuatro actuadores de cinco taps, genera D2 como matriz 4×5,
  conserva `SUMo` ch3 para comprobar PGAout y usa ch4 como tap propio de LP.
- La interfaz Python ofrece los canales 0..5; `taps` lee 0..4 y excluye el
  capacitor. Los ensayos T0–T3 quedaron desplazados al mapa nuevo.

Verificaciones realizadas sin grabar hardware:

- PSoC `AcondicionamientoAnalogicoTest`: **Rebuild Succeeded**, 69 512 bytes de
  flash y 17 416 bytes de SRAM. PSoC Creator mantiene un warning de setup entre
  relojes `CyBUS_CLK` y durante API Generation mostró mensajes de elementos ya
  existentes (`DMA_DelSig_Filter`, `OPAlp`, `OPAbp`); aun así compiló, enlazó y
  generó el HEX con resultado final exitoso.
- ESP32 `slaveTest`: **SUCCESS**, 63,2 % flash y 15,1 % RAM.
- Python: compilación de módulos correcta, checklist **29/29 PASS** y smoke GUI
  **39/39 PASS**.

La interfaz manual se abrió en COM8 después de estas verificaciones. El HEX
nuevo del PSoC y el binario nuevo del ESP quedaron compilados, pero **no fueron
grabados**: el equipo conectado conserva el firmware que ya tenía.
