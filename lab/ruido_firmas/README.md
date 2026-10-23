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

`firmas.py` resta la mediana y aplica el mismo ajuste LS de 50 Hz de la web. Solo aprende eventos exclusivos, refina el alineamiento por correlación y genera:

- `firmas_<placa>.json`: plantillas, estadística y método recomendado;
- `informe_<placa>.md`: resumen numérico en español;
- `firma_*.png` y `piso_*.png`, si Matplotlib está disponible.

`limpieza.py` compara sustracción de plantilla, alineamiento, interpolación lineal/cúbica, AR/LPC y, cuando ya está instalado, SWT `db4`. No instala PyWavelets: si falta, lo informa y omite ese método. La recomendación pondera el residual contra el piso clásico y el error sobre senos de 5/15/30/50 Hz y un chirp 10–80 Hz.

En el informe, SNR alto y correlación cercana a 1 indican una firma repetible. `scales_with_length` sugiere una perturbación sostenida; `fixed_edge_transient` indica que dominan los flancos. Un residual/base cercano a 1 llega al piso del modo clásico; el error normalizado de señal debe quedar bajo.

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

Genera capturas sintéticas con seis plantillas conocidas, ejecuta aprendizaje y evaluación, exige correlación ≥ 0,85 y verifica una reducción de RMS. No abre puertos.

---
Proveniencia: Codex (GPT-5), ejecución directa sin delegados.
