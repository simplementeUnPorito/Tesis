# Bitácora del Proyecto de Tesis
## Sistema de Ondas Superficiales con Geófonos ESP32-PSoC

> **Autor:** Elías David Álvarez  
> **Repo:** [simplementeUnPorito/Tesis](https://github.com/simplementeUnPorito/Tesis)  
> **Período:** Febrero – Mayo 2026  
> **Total de commits:** 197 | **Días de trabajo activo:** 31

---

Este índice agrupa todas las entradas de la bitácora por etapa del proyecto.

---

## Etapa 1 — Arranque y Marco Teórico (Feb–Mar 2026)

| Fecha | Archivo | Descripción |
|-------|---------|-------------|
| 2026-02-25 | [[2026-02-25]] | Commit inicial: repositorio creado |
| 2026-03-03 | [[2026-03-03]] | Vault Obsidian + resumen Capítulo 1 (Foti) |
| 2026-03-11 | [[2026-03-11]] | PDFs de Sebastiano Foti agregados al vault |
| 2026-03-13 | [[2026-03-13]] | Capítulo 2 completo + reorganización de Concepts |
| 2026-03-17 | [[2026-03-17]] | Submodulo MASW-Matlab, scripts teoría, startup.m |
| 2026-03-18 | [[2026-03-18]] | Scripts MATLAB teóricos + primer worklog |
| 2026-03-19 | [[2026-03-19]] | Capítulos 3, 4 y 5 resumidos + sesión nocturna masiva |
| 2026-03-20 | [[2026-03-20]] | Base de datos de papers + PDFs de investigación |
| 2026-03-23 | [[2026-03-23]] | Expansión masiva de la base de papers |

---

## Etapa 2 — Investigación IA Autónoma (Apr 10–15, 2026)

| Fecha | Archivo | Descripción |
|-------|---------|-------------|
| 2026-04-10 | [[2026-04-10]] | Revisión y limpieza de capítulos Obsidian |
| 2026-04-11 | [[2026-04-11]] | **GRAN SESIÓN** — Loop INVESTIGADOR: ~80 commits, 140 conceptos atómicos |
| 2026-04-12 | [[2026-04-12]] | Continuación INVESTIGADOR: Fases 5–6 completas, 4to ejemplo por capítulo |
| 2026-04-15 | [[2026-04-15]] | Cierre de la rama investigada por la IA |

---

## Etapa 3 — Hardware y Electrónica Analógica (Apr 17 – May 10, 2026)

| Fecha | Archivo | Descripción |
|-------|---------|-------------|
| 2026-04-17 | [[2026-04-17]] | MATLAB SM-24 empieza la locura |
| 2026-04-18 | [[2026-04-18]] | Más avances hardware |
| 2026-04-19 | [[2026-04-19]] | Loop auto-mejora Claude: PSoC FIR, ESP32 WiFi, 119 tests |
| 2026-04-22 | [[2026-04-22]] | LocuraCCp: datos reales del osciloscopio, compensador |
| 2026-04-27 | [[2026-04-27]] | Pruebas del circuito analógico |
| 2026-04-29 | [[2026-04-29]] | GeofonoSimplePruebaDeConcepto |
| 2026-04-30 | [[2026-04-30]] | Pre-locura cambios analógicos |
| 2026-05-05 | [[2026-05-05]] | Filtro notch + análisis espectral |
| 2026-05-10 | [[2026-05-10]] | Calibración manual, referencias desplazadas |

---

## Etapa 4 — Sistema Inalámbrico ESP-NOW (May 17–31, 2026)

| Fecha | Archivo | Descripción |
|-------|---------|-------------|
| 2026-05-17 | [[2026-05-17]] | Primer sistema analógico funcionando |
| 2026-05-18 | [[2026-05-18]] | Lucha con el circuito analógico |
| 2026-05-20 | [[2026-05-20]] | PSoC + proyecto analógico LPF + datos masivos |
| 2026-05-24 | [[2026-05-24]] | ESP: nodo comunicación + refactor con Claude |
| 2026-05-25 | [[2026-05-25]] | HELLO beacon, START probe/ACK, debug pulses |
| 2026-05-26 | [[2026-05-26]] | PRESTART + scope multi-start → **¡Funciona!** |
| 2026-05-28 | [[2026-05-28]] | Debug y ajustes post-éxito |
| 2026-05-29 | [[2026-05-29]] | Más ajustes y estabilización |
| 2026-05-31 | [[2026-05-31]] | Refactor final: UART PSoC↔ESP, PR #2 mergeado |

---

## Tecnologías usadas en el proyecto

- **Obsidian** — Vault de conocimiento, notas de capítulos, conceptos atómicos
- **MATLAB/Simulink** — Modelos del geófono SM-24, análisis espectral, interfaz con hardware
- **PSoC (Cypress)** — Microcontrolador para adquisición analógica del geófono
- **ESP32/ESP8266** — Red inalámbrica ESP-NOW (maestro + esclavos) para transmisión de datos
- **Python** — Scripts de organización del vault Obsidian
- **Git** — Control de versiones (este repo)

---

*Generado automáticamente por Claude Code — Bitácora en construcción*
