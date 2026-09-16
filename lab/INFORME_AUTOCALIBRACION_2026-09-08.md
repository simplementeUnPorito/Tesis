# Informe de autocalibración segura — 2026-09-08

> **SUPERADO / NO USAR COMO ESTADO ACTUAL.** El 2026-09-09 se comprobó que las
> mediciones DC de estas corridas conectaban `AMuxCapacitor` en paralelo y
> alteraban los nodos. Los resultados describen lo observado entonces, pero no
> validan la planta sin carga ni un x24 repetible. La fuente autoritativa es
> `HANDOFF_AUTOCALIBRACION_AUTORITATIVO_2026-09-09.md`.

## Resultado ejecutivo

La cadena quedó calibrable y repetible con **PGAgain x50 y PGAout hasta x24**
sin cambiar nuevamente las resistencias. La rutina de producción en PC admite
x1, x2, x4, x8, x16 y x24; x32, x48 y x50 quedan experimentales y bloqueadas
por defecto.

No se modificó TopDesign. El único cambio de rango se hace en C al arrancar:
IDAC2/PGAout usa 0–255 µA. La aplicación impone un límite mucho menor,
`|IDAC2| <= 48`; IDAC3/LP queda en el rango original y `|IDAC3| <= 160`.

## Topología y escala vigentes

| Etapa | Función | Resistencia | Corriente/bit | Límite de software |
|---|---|---:|---:|---:|
| IDAC0 | referencia PGAgain | 15 kΩ | 0,125 µA | semilla 0 |
| IDAC1 | referencia compartida OPAbp/OPAsum | 15 kΩ | 0,125 µA | semilla −110 |
| IDAC2 | referencia exclusiva PGAout | 1,5 kΩ | 1 µA | ±48 |
| IDAC3 | referencia LP | 10 kΩ | 0,125 µA | ±160 |

AMux: ch0 PGAgain, ch1 BPo, ch2 OPA_SUMo, ch3 SUMo después de PGAout,
ch4 LPo y ch5 capacitor auxiliar.

## Seguridad eléctrica

- IDAC2 se caracteriza y usa como máximo a código 48: 48 µA y 72 mV sobre
  1,5 kΩ. Es sólo 18,8 % de su rango configurado.
- Incluso el fondo de escala del componente produciría 382,5 mV sobre 1,5 kΩ.
  Alrededor de Vref ≈ 2,062 V, el nodo quedaría aproximadamente entre 1,680 V
  y 2,445 V, con más de 1 V de margen de compliance a ambos rieles para
  Vdda ≈ 4,83 V.
- IDAC3 a código 160 produce 20 µA y 200 mV sobre 10 kΩ.
- La hoja de datos oficial del PSoC 5LP caracteriza el modo 255 µA con carga de
  2,4 kΩ y especifica 1 V mínimo de compliance/dropout. Fuente:
  https://www.infineon.com/assets/row/public/documents/non-assigned/49/infineon-psoc-5lp-cy8c58lp-datasheet-datasheet-en.pdf
- Nunca se habilitó ni se usa el rango de 2,04 mA.

## Algoritmo validado

`src/interfaces/python/autocalibrar_seguro.py`:

1. fija PGAgain x50;
2. aplica una semilla verificada por ganancia;
3. espera 60 s para eliminar el transitorio de ganancia/LP;
4. toma cinco rondas de los cinco taps;
5. decide con la mediana DC, no con una lectura instantánea;
6. no usa pico a pico/50 Hz para mover el offset, aunque lo registra;
7. sólo permite un ajuste final de LP de hasta 24 códigos si la mediana queda
   fuera de ±20 mV;
8. aborta si un tap cruza las guardas analógicas.

Semillas verificadas:

| PGAout | [IDAC0, IDAC1, IDAC2, IDAC3] |
|---:|---|
| x1 | [0, −110, 0, 32] |
| x2 | [0, −110, 24, 40] |
| x4 | [0, −110, 40, 48] |
| x8 | [0, −110, 48, 64] |
| x16 | [0, −110, 48, 90] |
| x24 | [0, −110, 48, 120] |

La razón para usar mediana y banda muerta es experimental: con actuadores
quietos, LPo siguió variando decenas de milivolts por la perturbación ambiental,
mientras ch0–ch3 permanecían estables. Un PI rápido perseguía esa oscilación y
producía resultados intermitentes.

## Resultados en hardware

Todas las cifras son errores respecto del cero diferencial, en mV, y son la
mediana de cinco rondas.

| Corrida | PGAout | PGAgain | BPo | OPA_SUMo | SUMo | LPo | Resultado |
|---|---:|---:|---:|---:|---:|---:|---|
| producción 1 | x1 | −14,87 | −10,56 | +2,88 | +2,77 | −6,96 | PASS |
| producción 1 | x8 | −15,50 | −12,45 | +3,09 | +4,81 | −9,72 | PASS |
| producción 1 | x16 | −14,74 | −10,75 | +2,98 | +6,53 | +3,07 | PASS |
| producción 1 | x24 | −14,72 | −11,54 | +3,07 | +6,47 | −13,14 | PASS |
| producción 2 | x1 | −15,54 | −12,57 | +3,04 | +3,09 | −7,97 | PASS |
| producción 2 | x8 | −14,93 | −10,79 | +3,09 | +4,56 | −6,58 | PASS |
| producción 2 | x16 | −14,99 | −10,49 | +3,04 | +7,04 | −13,71 | PASS |
| producción 2 | x24 | −15,50 | −11,40 | +2,96 | +6,37 | −15,29 | PASS |
| cobertura | x2 | −14,66 | −10,62 | +2,58 | +3,89 | −9,90 | PASS |
| cobertura | x4 | −15,26 | −11,00 | +2,54 | +3,88 | −5,60 | PASS |
| x24 repetición 3 | x24 | −15,48 | −11,19 | +3,06 | +5,25 | −13,29 | PASS |
| x24 repetición 4 | x24 | −15,31 | −12,38 | +2,86 | +6,55 | −2,04 | PASS |
| x24 repetición 5 | x24 | −14,93 | −11,29 | +2,81 | +6,53 | +11,83 | PASS |
| x24 post-flash | x24 | −14,93 | −11,65 | +2,96 | +3,19 | −4,42 | PASS |

x24 pasó **6/6 arranques independientes**. Su mediana LPo quedó entre −15,29
y +11,83 mV. Las excursiones instantáneas algo mayores se atribuyen a la
perturbación ambiental registrada y no provocaron acciones del controlador.

Chequeo pasivo final, sin mover IDACs ni ganancias: enlace PSoC `ARRIBA`,
perfil GEO correcto y errores DC de −14,19, −10,98, +2,58, +2,64 y −16,90 mV
en ch0–ch4 respectivamente; todos los taps respondieron `ok`.

La evidencia cruda está en `lab/calibracion_nueva/*.json` y sus transcriptos
`.log`.

## Firmware e interfaz

- PSoC cargado: `AcondicionamientoAnalogicoTest` / GEO+AUTOTEST, 6 canales,
  2604 Hz. Compiló y se programaron/verificaron 280 filas.
- Uso: flash 69.568/262.144 bytes; SRAM 17.416/65.536 bytes.
- SHA-256 del PSoC cargado:
  `8A96DDBD170A406B85ADAE982569BF9B3038FFEA85A16F8C02998A27EF0139BE`.
- ESP `slaveTest`: compilación PlatformIO exitosa; RAM 49.604 bytes (15,1 %),
  flash 828.669 bytes (63,2 %).
- SHA-256 del binario ESP compilado:
  `1D35009FE1314262933500FC1357705B1FB4E67860A97C6ED0944270FBFE113E`.
- Self-test Python: 29/29 PASS.
- La GUI manual muestra los nombres y escalas actuales, limita IDAC2/IDAC3 y
  aplica los mismos límites a los barridos.
- La rutina experimental anterior `calibrar_topologia_compartida.py` queda
  bloqueada por defecto para impedir el uso accidental de límites obsoletos.
- El proyecto de campo `AcondicionamientoAnalogico` conserva un TopDesign de
  5 canales y no compila contra el código de 6 canales. No se corrigió porque
  se indicó explícitamente no tocar TopDesign. El proyecto cargado y operativo
  es el de test.

## Uso mañana

Autocalibrar todas las ganancias aprobadas y dejar la última (x24) aplicada:

```powershell
cd C:\Github\Tesis\src\interfaces\python
python autocalibrar_seguro.py --port COM8 --gains 1,2,4,8,16,24
```

Abrir la interfaz manual ya conectada:

```powershell
cd C:\Github\Tesis\src\interfaces\python
python -m testbench gui --port COM8 --manual --connect
```

Para una corrida de verificación que restaure x1 al finalizar, agregar
`--restore`.

## Decisión de resistencias y alta ganancia

No cambiar resistencias mañana para el rango aprobado: 1,5 kΩ en PGAout y
10 kΩ en LP tienen autoridad y resolución suficientes hasta x24.

x32/x48/x50 no están declaradas imposibles, pero tampoco están garantizadas.
En x50 se logró mantener ch0–ch3 centrados, pero LPo alternó entre saturación y
una excursión grande bajo la perturbación actual. Antes de habilitarlas se debe
repetir la caracterización con el geófono enterrado. No se recomienda aumentar
resistencias ni corriente para perseguir x50 sin esa medición.
