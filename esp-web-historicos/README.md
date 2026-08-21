# Interfaces web históricas del maestro ESP32

Este directorio contiene copias independientes de siete hitos de la SPA que el
maestro ESP32 sirve desde su memoria. Cada copia fue extraída directamente del
historial Git de `src/firmware/esp32`; no es una reconstrucción manual.

| Carpeta | Fecha | Commit | Hito visible |
|---|---:|---|---|
| `01_2026-06-08_ui-inicial` | 2026-06-08 | `323fcb7` | Primera UI web, relay WebSocket y pruebas |
| `02_2026-06-08_funcional-incompleta` | 2026-06-08 | `76d6092` | Primer estado funcional, todavía incompleto |
| `03_2026-06-15_autocalibracion` | 2026-06-15 | `70ca42e` | Autocalibración incorporada |
| `04_2026-07-01_pagina-operativa` | 2026-07-01 | `8b63d2b` | Página declarada operativa en campo |
| `05_2026-07-12_ui-finalizada` | 2026-07-12 | `89384d8` | UI y herramientas de captura E5c finalizadas |
| `06_2026-07-24_enlace-mdns` | 2026-07-24 | `9eb8b5a` | Pestaña Enlace, escaneo, canal y `geo.local` |
| `07_2026-08-03_pga-pgaout` | 2026-08-03 | `d6463a` | Compilación local estable y selección PGA/PGAout |

## Levantar una versión sin ESP conectado

Desde PowerShell:

```powershell
cd C:\Github\Tesis\esp-web-historicos
python serve_demo.py --list
python serve_demo.py --version 07_2026-08-03_pga-pgaout --port 8010
```

Luego se abre `http://127.0.0.1:8010/`. El servidor emula:

- el WebSocket `/ws`, incluido un estado de enlace periódico;
- `/enlace/status`, con red, canal, cola de archivos e IP;
- `/enlace/scan`, con tres redes 2,4 GHz simuladas;
- `/enlace/config`, para probar el formulario sin escribir en un ESP;
- `/ws-reset`.

Los archivos históricos permanecen intactos. Para cambiar de versión se detiene
el servidor con `Ctrl+C` y se vuelve a ejecutar con otra carpeta. Las operaciones
de adquisición, calibración y exportación se pueden recorrer visualmente, pero
no representan una prueba del firmware ni generan una captura sísmica real.
