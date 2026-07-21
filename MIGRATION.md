# Migración desde el monorepo

La modularización se realizó el 20 de julio de 2026 a partir de `codex/capture-engine-verilog`, incluyendo los 29 commits locales que todavía no estaban en su remoto.

| Ruta anterior | Destino actual |
|---|---|
| `src/psoc` | `firmware/psoc` → `Tesis-firmware-psoc` |
| `src/esp` | `firmware/esp32` → `Tesis-firmware-esp32` |
| `src/python` | `software/python` → `Tesis-software-python` |
| `src/matlab` | `modelado/matlab` → `Tesis-modelado-matlab` |
| `docs` | `docs` → `Tesis-documentacion` |
| `Obsidian Vault` | `investigacion` → `Tesis-investigacion` |
| `Crudos` | `data/raw` (solo local) |
| `procesados` | `data/processed` (solo local) |
| `third-party/ADsurf`, `third-party/maswavespy` | submódulos internos de `software/python` |
| `third-party/MASW-Matlab-code` | submódulo interno de `modelado/matlab` |
| `third-party/geopsy` | `software/python/third-party/geopsy` (solo local) |

## Preservación local

- Los PDF y fuentes bibliográficas se conservaron en `investigacion/sources`, ignorados por Git.
- Los artefactos generados antiguos, el entorno virtual raíz y dos `.cpp` modificados de `maswavespy` se respaldaron en `C:\Github\Tesis-migration-local-20260720`.
- Dos directorios vacíos de MATLAB pueden permanecer temporalmente bajo `src/` si una aplicación de Windows los tiene abiertos. `src/` está ignorado y puede eliminarse al cerrar esa aplicación.

## Historial de `Tesis`

Esta migración no reescribe ni fuerza el historial del repositorio integrador. Los repositorios nuevos conservan el historial relevante de cada sector y el árbol actual queda modular, pero los objetos históricos del monorepo siguen existiendo en `Tesis` para no invalidar ramas ni commits en curso. Reducir también el tamaño histórico exige una operación posterior de archivo y force-push coordinada.
