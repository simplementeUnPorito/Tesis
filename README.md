# Tesis — sistema integrado MASW

Este repositorio es el **superproyecto** de la tesis. Ya no contiene firmware, aplicaciones, simulaciones, documentación ni mediciones directamente: fija versiones compatibles de repositorios independientes mediante submódulos Git.

## Mapa del proyecto

`src/` se organiza por **propósito**, no por lenguaje: da igual si algo es
MATLAB o Python, importa si es firmware, una interfaz contra el hardware o un
cálculo que se corre unas pocas veces.

| Sector | Ruta | Repositorio | Responsabilidad |
|---|---|---|---|
| Firmware | `src/firmware/psoc` | [Tesis-firmware-psoc](https://github.com/simplementeUnPorito/Tesis-firmware-psoc) | adquisición, acondicionamiento y calibración PSoC 5LP |
| Firmware | `src/firmware/esp32` | [Tesis-firmware-esp32](https://github.com/simplementeUnPorito/Tesis-firmware-esp32) | maestro, esclavos, ESP-NOW y UI web |
| Interfaces | `src/interfaces/python` | [Tesis-interfaces-python](https://github.com/simplementeUnPorito/Tesis-interfaces-python) | Geophone Scope: GUI, revisión de campo y MASW |
| Interfaces | `src/interfaces/matlab` | [Tesis-interfaces-matlab](https://github.com/simplementeUnPorito/Tesis-interfaces-matlab) | scope/GUI del nodo ESP y del circuito analógico |
| Cálculos y modelados | `src/calculos_modelados/matlab` | [Tesis-calculos-matlab](https://github.com/simplementeUnPorito/Tesis-calculos-matlab) | Simulink, modelo SM-24 y análisis de la cadena analógica |
| Cálculos y modelados | `src/calculos_modelados/python` | [Tesis-calculos-python](https://github.com/simplementeUnPorito/Tesis-calculos-python) | compensador, MFB-LPF y MASW offline |
| Documentación | `docs` | [Tesis-documentacion](https://github.com/simplementeUnPorito/Tesis-documentacion) | entregables, diagramas, planes y handoffs |
| Investigación | `docs/investigacion` | [Tesis-investigacion](https://github.com/simplementeUnPorito/Tesis-investigacion) | vault de Obsidian, bitácora y notas académicas (submódulo *de* `docs`) |
| Datos | `data` | [Tesis-datos](https://github.com/simplementeUnPorito/Tesis-datos) | catálogo y estructura local de mediciones |

Cada sector se puede clonar, probar y versionar por separado. `Tesis` solo expresa qué revisión de cada sector forma una configuración integrada.

## Clonar el sistema completo

Los repositorios de datos, investigación, Python, MATLAB y documentación usan
un folderstore externo. Evite que Git intente descargar esos objetos desde
GitHub durante el primer clon:

```powershell
$env:GIT_LFS_SKIP_SMUDGE = '1'
git clone --recurse-submodules --shallow-submodules https://github.com/simplementeUnPorito/Tesis.git
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
cd Tesis
.\scripts\bootstrap.ps1
```

`bootstrap.ps1` configura automáticamente los submódulos para
`C:\Users\elias\OneDrive\Github-LFS`. Si el almacén se movió, defina antes
`GITHUB_LFS_ROOT` con su nueva ubicación. El script deja los archivos grandes
como punteros; para materializar todos —incluidos aproximadamente 30 GiB
lógicos de datos— use `bootstrap.ps1 -HydrateLfs`.

Si el repositorio ya estaba clonado:

```powershell
git pull
git submodule sync --recursive
.\scripts\bootstrap.ps1
```

## Trabajar en una parte aislada

Entre en el submódulo correspondiente y cree allí su rama y commit. Luego vuelva a `Tesis` y actualice el puntero del submódulo en un commit separado. Esto evita que un cambio de Python quede mezclado con firmware o documentación.

Las mediciones de `data/raw/` y los resultados de `data/processed/` están
indexados mediante Git LFS y viven físicamente en el folderstore. La aplicación
Python también acepta `TESIS_DATA_ROOT` para trabajar con otro árbol de datos.

El índice maestro de objetos, manifiestos y procedimiento para mover el drive
está en `C:\Users\elias\OneDrive\Github-LFS\INDEX.md`.

Consulte [ARCHITECTURE.md](./ARCHITECTURE.md) para las fronteras y dependencias entre sectores.
