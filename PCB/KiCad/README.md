# PCB intermedia con kits de desarrollo

Este proyecto usa los módulos completos `CY8CKIT-059` y
`ESP32-DevKitC V4 (38 pines)` como componentes enchufables de una placa
portadora de una cara.

## Bibliotecas locales

- `Tesis_DevKits.kicad_sym`: símbolos del PSoC 5LP y del ESP32.
- `Tesis_DevKits.pretty`: huellas para zócalos hembra THT.
- `sym-lib-table` y `fp-lib-table`: registro local de ambas bibliotecas.
- `generate_devkit_symbols.ps1`: regenera los símbolos.
- `generate_devkit_footprints.ps1`: regenera las huellas.
- `generate_complete_schematic.ps1`: genera el traspaso preliminar completo
  del TopDesign en `Tesis_complete.kicad_sch`, sin sobrescribir el esquema
  base que puede estar abierto en KiCad.

Los números de pin conservan el encabezado físico, por ejemplo `J1.9` y
`J2.11`. De esta forma el netlist no pierde la correspondencia entre el
esquema y el pin que se debe cablear en la placa real.

## Enlace PSoC–ESP32 implementado

| Señal | CY8CKIT-059 | ESP32-DevKitC |
|---|---|---|
| UART PSoC → ESP | `Tx = P12[7]`, `J1.9` | `GPIO25`, `J2.9` |
| UART ESP → PSoC | `Rx = P2[0]`, `J1.1` | `GPIO26`, `J2.10` |
| Inicio de captura | `SYNC_IN = P1[5]`, `J1.22` | `GPIO27`, `J2.11` |
| Sync externa opcional | — | `GPIO32`, `J2.7` |
| Referencia común | `GND`, `J2.2` | `GND`, `J2.14` |

La salida `Tx` del PSoC está configurada como `OPEN_DRAIN_LO`. `R1 = 4.7 kΩ`
la eleva a los `3.3 V` del ESP32; no se unen las líneas de `5 V` de los kits.
Durante esta etapa cada kit puede seguir alimentándose por su propio USB, pero
ambos deben compartir GND.

La agrupación GPIO25/GPIO26/GPIO27 en el encabezado J2 del ESP32 es la
asignación nueva para la PCB intermedia. La placa universal anterior debe
recablearse a esos pines o compilarse con las macros antiguas.

## Traspaso preliminar del TopDesign

`Tesis_complete.kicad_sch` contiene:

- ambos development kits, UART, sincronismo y pull-up de nivel;
- entrada de geófono y polarización;
- redes externas de pasa-banda, sumador y pasa-bajos;
- referencia principal y cuatro referencias filtradas por etapa;
- capacitor del AMux, pulsador, LED, sync externa y módulo microSD;
- notas del flujo interno PSoC (AMux, LPF, ADC, DFB, DMA, control y timers);
- huellas THT para todos los componentes físicos;
- marcas explícitas de no-conectado y `PWR_FLAG` para los kits alimentados
  por USB.

El bus SPI quedó bloqueado y compilado en un tramo contiguo del header:

| Función | PSoC | CY8CKIT-059 |
|---|---|---|
| CS | P2[3] | J1.4 |
| SCK | P2[4] | J1.5 |
| MOSI | P2[5] | J1.6 |
| MISO | P2[6] | J1.7 |

Regeneración y validación:

```powershell
.\generate_complete_schematic.ps1
& 'D:\Program Files\KiCad\bin\kicad-cli.exe' sch erc `
  .\Tesis_complete.kicad_sch --format json --severity-all `
  -o .\Tesis_complete_erc.json
```

La última validación cerró con cero violaciones ERC. También se exportan
`Tesis_complete.pdf`, `Tesis_complete.net`, `Tesis_complete_bom.csv` y
`Tesis_complete_render.png` como artefactos de revisión.

## Fuentes físicas

- Infineon CY8CKIT-059 PSoC 5LP Prototyping Kit Guide:
  <https://www.infineon.com/assets/row/public/documents/30/44/infineon-cy8ckit-059-psoc-5lp-prototyping-kit-guide-usermanual-en.pdf?fileId=8ac78c8c7d0d8da4017d0ef981770f63>
- Infineon CY8CKIT-059 schematics and PCB design data:
  <https://www.infineon.com/assets/row/public/documents/30/60/infineon-cy8ckit-059-schematics-pcbdesigndata-en.pdf>
- Espressif ESP32-DevKitC V4 User Guide:
  <https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html>
- Espressif ESP32-DevKitC V4 dimensions:
  <https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_dimensions.pdf>

## Próximo paso

El esquema está armado, pero `Tesis.kicad_pcb` todavía no representa la
portadora terminada. Antes de rutear una cara se deben elegir dimensiones,
posición mecánica de ambos kits y conectores, ancho de pistas, plano/puentes
permitidos y el módulo microSD de 5 V concreto. No usar un socket de tarjeta
crudo: la interfaz del PSoC es de 5 V y requiere adaptación a 3.3 V.
