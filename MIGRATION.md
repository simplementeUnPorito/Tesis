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
| `Crudos` | `data/raw` → `Tesis-datos` + folderstore LFS |
| `procesados` | `data/processed` → `Tesis-datos` + folderstore LFS |
| `third-party/ADsurf`, `third-party/maswavespy` | submódulos internos de `software/python` |
| `third-party/MASW-Matlab-code` | submódulo interno de `modelado/matlab` |
| `third-party/geopsy` | `software/python/third-party/geopsy` + folderstore LFS |

## Preservación y objetos grandes

- Los PDF y fuentes bibliográficas se conservaron en `investigacion/sources`
  mediante punteros LFS.
- Las mediciones, resultados, Geopsy, datasets MATLAB y paquetes documentales
  grandes están inventariados en
  `C:\Users\elias\OneDrive\Github-LFS\INDEX.md`.
- Los artefactos generados antiguos, el entorno virtual raíz y dos `.cpp` modificados de `maswavespy` se respaldaron en `C:\Github\Tesis-migration-local-20260720`.
- Dos directorios vacíos de MATLAB pueden permanecer temporalmente bajo `src/` si una aplicación de Windows los tiene abiertos. `src/` está ignorado y puede eliminarse al cerrar esa aplicación.

## Archivo del monorepo

El monorepo completo, incluidas sus ramas históricas anteriores a la separación,
se conserva en el repositorio privado
`simplementeUnPorito/Tesis-legacy`. Su historia fue reescrita sólo para mover
objetos mayores a 10 MiB al folderstore; el commit monolítico original más
reciente era `5df22e512cced54c80cdba6f5b595e246e181598`.

El `Tesis` público comienza desde una línea base modular nueva. Los historiales
específicos continúan en cada repositorio componente y el historial monolítico
queda aislado en `Tesis-legacy`.
