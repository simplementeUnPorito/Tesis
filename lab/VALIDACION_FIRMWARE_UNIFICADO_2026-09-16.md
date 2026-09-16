# Validacion del firmware unificado - 2026-09-16

## Resultado

Se valido en las dos placas conectadas el proyecto PSoC unico
`AcondicionamientoAnalogico.cydsn` y el ESP32 esclavo `slave2`.

- PSoC Release: compilado, programado y verificado (209 filas de flash).
- PSoC Debug/`PSOC_TEST`: compilado, programado y verificado (326 filas).
- ESP32 `slave2` y `slaveTest`: compilacion correcta.
- ESP32 `slave2`: programado por COM8; MAC `c8:2e:18:67:68:6c`.
- Prueba host del PI/configuracion entera: PASS.

Uso medido: PSoC Release 51 336 bytes de flash (19,6 %) y 53 537 bytes de
SRAM (81,7 %); Debug 81 280 bytes de flash (31,0 %) y 53 240 bytes de SRAM
(81,2 %). ESP32 `slave2`: 53 256 bytes RAM (16,3 %) y 828 773 bytes flash
(63,2 %); `slaveTest`: 53 708 bytes RAM (16,4 %) y 830 469 bytes flash
(63,4 %).

## Pruebas fisicas

- Autotest PSoC: 23 PASS, 3 FAIL, 0 WARN. Los tres FAIL restantes pertenecen
  a criterios heredados: C6 espera un reporte SD antiguo, y D1/D2 barren la
  cadena analogica sin el nuevo asentamiento/calibracion. I2C, tramas, FIR,
  ganancias y ruido pasan.
- Configuracion: set/apply, rechazo de valor invalido, defaults, cambio de
  canal, pause/resume y rechazo durante captura verificados.
- Aprendizaje: perfil lento valido IDAC0/IDAC1 `(+14,+4)` guardado. Despues de
  reiniciar/programar, arranco directamente en RUNNING desde EEPROM, sin
  reaprender. El perfil y configuracion conservan CRC/version.
- Ruta de capacitor: habilitar/deshabilitar fue aceptado y un cambio
  incompatible marco correctamente `FALTA_APRENDER`.
- Captura LPo: 4 lotes a SD, `ARMED`, `SD_SESSION`, `CAPTURE_DONE 4/4`.
- Captura SUMo (canal 3): 2 lotes a SD, `ARMED` antes de SYNC y
  `CAPTURE_DONE 2/2`. Esta repeticion valida la correccion de la carrera por la
  que el ESP enviaba SYNC antes de recibir `ARMED` cuando los metadatos tardaban
  mas de 800 ms.
- Estado final: firmware Release normal en ambas placas, canal de captura 4
  (LPo), capacitor habilitado, perfil valido cargado y PI reanudado.

Durante una captura, la instantanea de metadatos mantuvo los IDAC congelados;
el PI, los barridos y los cambios de configuracion se reanudaron solo al acabar.
Los metadatos incluyen configuracion efectiva, perfil/origen, ganancias, IDAC,
canal y las ultimas estimaciones DC con validez y antiguedad.

## Limitaciones conocidas

- PSoC Creator conserva el warning de timing `Warning-1366` de `CyBUS_CLK`, ya
  presente en el proyecto; no impidio programacion ni las pruebas de banco.
- Los casos C6/D1/D2 del autotest antiguo deben redefinirse para comprobar la
  nueva semantica, no usarse como criterio de rechazo del firmware unificado.
- En la medicion final LPo estaba aproximadamente en +115 mV respecto de Vref,
  apenas fuera de la banda de +/-100 mV; el PI entero aplicaba correcciones
  limitadas por la banda muerta cada 5 s, sin la agresividad del controlador
  Python anterior.
