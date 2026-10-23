# Calibración de firmas de ruido

Este kit aprende la respuesta de **cada placa física** a I2C, SD, ESP-NOW y beacons, compara métodos de limpieza y deja un `firmas_<placa>.json` reutilizable por la web.

## Conexión segura

1. Alimente el conjunto PSoC + ESP esclavo con un power bank.
2. Desconecte del PC los USB del PSoC y del ESP esclavo. Esto evita el lazo de masa.
3. Conecte al PC **solamente** el USB del ESP maestro.
4. Identifique el puerto del maestro (por defecto `COM6`). No abra monitores seriales en paralelo.

`captura.py` abre únicamente ese puerto a 921600 baud. Abrirlo reinicia el maestro, por lo que el programa espera 12 s antes de enviar comandos.

## Calibración completa de una placa nueva

Desde la raíz del repositorio:

```powershell
python lab/ruido_firmas/captura.py --placa GEO_A --puerto COM6
python lab/ruido_firmas/firmas.py lab/ruido_firmas/capturas/GEO_A --placa GEO_A
python lab/ruido_firmas/limpieza.py lab/ruido_firmas/capturas/GEO_A --firmas lab/ruido_firmas/capturas/GEO_A/firmas_GEO_A.json
```

El plan normal hace tres repeticiones de cinco escenarios y muestra la duración estimada antes de tocar el puerto. Se niega a iniciar si la estimación supera 15 min. Para una prueba de humo de menos de tres minutos:

```powershell
python lab/ruido_firmas/captura.py --placa GEO_A --puerto COM6 --rapido
```

Escenarios:

- `base_clasico`: PSoC RAM, sin marcas ni tráfico durante captura; piso quieto.
- `async_comp`: I2C y recepción del maestro, sin SD ni TX durante captura.
- `async_sd`: I2C, SD y recepción del maestro.
- `rt_comp`: I2C, TX ESP-NOW y recepción del maestro.
- `rt_sd`: todas las fuentes activas.

Cada repetición produce un NPZ y un JSON lateral. Una captura solo se acepta si llegan exactamente `N × 30` muestras y el maestro vuelve de RUNNING/DUMPING a ARMED.

## Resultados

`firmas.py` resta la mediana, aplica el mismo ajuste LS de línea de la web y estima todas las fuentes a la vez mediante una regresión FIR dispersa (deconvolución tipo rERP). Cada inicio de marca aporta una copia de su plantilla a la matriz de diseño; `SD_IO`, `RADIO_TX` e `I2C` también prueban una plantilla de fin de corrida, que solo se conserva si mejora la validación entre capturas. Los eventos pueden ser densos y superpuestos. El promedio de eventos exclusivos se guarda únicamente como diagnóstico secundario.

La estimación predeterminada usa `--pre 4 --largo 32 --hp 150 --damp 0.5`. El pasa-altos se usa **solo para aprender** las plantillas; no forma parte de la cadena de medición. `--hp none` permite contrastarlo. La validación par/impar separa capturas completas, el aporte por fuente se obtiene por ablación drop-one-type y un bootstrap por capturas produce el IC 95 % de cada muestra.

Se generan:

- `firmas_<placa>.json`: plantillas `onset`/`offset`, IC, significancia, validación y método recomendado;
- `informe_<placa>.md`: resumen numérico en español;
- `firma_*.png` y `piso_*.png`, si Matplotlib está disponible.

`limpieza.py` compara A) interpolación lineal, B) cúbica, C) AR/LPC, D) SWT `db4` y E) sustracción deconvolutiva. E resta exactamente una plantilla por inicio y, si fue seleccionada, otra por fin de corrida: no alinea ni reajusta amplitud por evento. Las métricas incluyen varianza HF fuera de muestra, PSD 1–100 y 10–50 Hz frente a `base_clasico`, preservación de senos de 5/15/30/50 Hz y chirp 10–80 Hz, y la cadena web completa hasta un FIR LP de 200 Hz/101 taps. PyWavelets se usa si está instalado.

## Resultado GEO_I2C_A (2026-10-23)

Con 13 capturas reales a 2604 Hz, el modelo con HP de 150 Hz explicó 22,65 % de la varianza HF fuera de muestra; sin HP explicó 14,50 %. El piso `base_clasico` tuvo RMS de primera diferencia de 1,50 cuentas. Solo el offset de `RADIO_TX` mejoró la validación. La cadena recomendada cambió la potencia total 1–100 Hz por un factor 0,9962 y 10–50 Hz por 1,0001.

| Fuente | EV drop-one | Pico cuentas | Significativa | Recomendación | E: HF explicada | 10–50 después/antes | Error inyectado |
|---|---:|---:|---|---|---:|---:|---:|
| SD_IO | -0,021 % | 0,067 | sí | none | 0,003 % | 1,0000 | 0 |
| SD_SYNC | -0,019 % | 0,254 | sí | none | -0,049 % | 1,0000 | 0 |
| RADIO_TX | 9,971 % | 1,291 | sí | template | 16,544 % | 1,0004 | <1e-15 |
| I2C | 13,458 % | 1,303 | sí | template | 12,571 % | 1,0000 | <1e-15 |
| AP_BEACON | 0,010 % | 0,187 | sí | template | 0,108 % | 1,0000 | <1e-15 |
| MASTER_RX | 0,153 % | 0,851 | sí | template | -0,149 % aislado; aporte conjunto positivo | 1,0000 | <1e-15 |

`significativa` indica que al menos una muestra de la plantilla tiene IC bootstrap 95 % que excluye cero. La recomendación también exige aporte conjunto positivo; por eso SD queda en `none` aunque aparezcan muestras estadísticamente distintas de cero.

## Cargar las firmas en la web

Para dejarlas fijas en LittleFS:

```powershell
Copy-Item lab/ruido_firmas/capturas/GEO_A/firmas_GEO_A.json "src/firmware/esp32/Nodo comunicación/master/data/firmas.json"
Set-Location "src/firmware/esp32/Nodo comunicación/master"
pio run -e esp32dev -t uploadfs
```

También puede usar **Cargar firmas** en cualquier panel de esclavo. El archivo se valida, se aplica a todos los nodos y queda en `localStorage`, con prioridad sobre `/firmas.json`. El panel muestra placa y fecha cargadas.

Active por nodo las limpiezas I2C, SD, transmisión y beacon. La cadena de “Filtrada” es: quitar offset → línea → I2C → SD → TX → beacon/RX maestro → FIR. “Cruda” conserva su comportamiento y su opción visual **Sin offset DC**.

## Autotest sin hardware

```powershell
python lab/ruido_firmas/autotest.py
```

Genera capturas sintéticas con seis plantillas conocidas y otro caso con eventos densos y superpuestos como los reales. En este último no hay eventos RADIO_TX exclusivos y la deconvolución debe recuperar cada plantilla con correlación > 0,95. También ejecuta la evaluación completa y verifica reducción HF fuera de muestra. No abre puertos.

---
Proveniencia: Codex, ejecución directa sin delegados.
