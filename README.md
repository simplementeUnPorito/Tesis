# Tesis — sistema integrado MASW

Este repositorio es el **superproyecto** de la tesis. El firmware, las
interfaces, los cálculos, los PCB, los datos y la documentación principal viven
en repositorios independientes fijados como submódulos Git. La raíz conserva
además herramientas de integración, activos mecánicos compartidos, snapshots
históricos de la web y algunos modelos que todavía no fueron extraídos.

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
| PCBs | `PCBs` | [Tesis-PCBs](https://github.com/simplementeUnPorito/Tesis-PCBs) | esquemáticos, placa, símbolos y diseño programático en KiCad/JitX |
| Documentación | `docs` | [Tesis-documentacion](https://github.com/simplementeUnPorito/Tesis-documentacion) | entregables, diagramas, planes y handoffs |
| Investigación | `docs/investigacion` | [Tesis-investigacion](https://github.com/simplementeUnPorito/Tesis-investigacion) | vault de Obsidian, bitácora y notas académicas (submódulo *de* `docs`) |
| Datos | `data` | [Tesis-datos](https://github.com/simplementeUnPorito/Tesis-datos) | catálogo y estructura local de mediciones |

Cada sector se puede clonar, probar y versionar por separado. `Tesis` solo expresa qué revisión de cada sector forma una configuración integrada.

Contenido gestionado directamente por el superproyecto:

| Ruta | Estado y función |
|---|---|
| `scripts/` | bootstrap, auditoría, automatización y utilidades de integración |
| `src/mecanica/` | CAD, STL, planillas y entradas mecánicas compartidas |
| `esp-web-historicos/` | siete snapshots congelados de la UI, no firmware activo |
| `src/modelado_matlab/martinete_leva_multibody/` | modelo MATLAB del martinete gestionado por el superproyecto |
| `docs/proyecto/` | arquitectura, migración, planes y notas del proyecto |
| `docs/auditorias/` | auditorías e inventarios documentales versionados |

## Dónde va cada cosa

Todo resultado interno o intermedio —figuras de trabajo, MAT, CSV de resultados,
logs, cachés y exports de simulación— va en `outputs/`, fuera de Git. `docs/`
contiene únicamente entregables versionados: informes, PDF finales y figuras que
forman parte de la tesis. Los generadores Python y MATLAB deben usar
`scripts/shared/rutas.py` o `scripts/shared/dir_salida.m`; nunca deben escribir
al lado del código fuente.

## Dónde empezar

- [Arquitectura integrada](./docs/proyecto/ARCHITECTURE.md)
- [Inventario y auditoría documental del 2 de septiembre](./docs/auditorias/REPOSITORY_AUDIT_2026-09-02.md)
- [Firmware ESP32](./src/firmware/esp32/README.md)
- [Firmware PSoC](./src/firmware/psoc/README.md)
- [Software de campo en Python](./src/interfaces/python/README.md)
- [Bitácora cronológica](./docs/investigacion/Notes/bitacora/INDICE.md)
- [Puesta en marcha digital de la primera placa](./docs/investigacion/Notes/bitacora/2026-09-01.md)

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

Como red de seguridad local, `scripts/auto-commit-submodules.ps1` puede crear
un commit cuando un submódulo lleva 24 horas sin commits y conserva cambios.
La instalación de la tarea de Windows se documenta en
[`scripts/AUTO_COMMIT_SUBMODULES.md`](./scripts/AUTO_COMMIT_SUBMODULES.md).

Las mediciones de `data/raw/` y los resultados de `data/processed/` están
indexados mediante Git LFS y viven físicamente en el folderstore. La aplicación
Python también acepta `TESIS_DATA_ROOT` para trabajar con otro árbol de datos.

El índice maestro de objetos, manifiestos y procedimiento para mover el drive
está en `C:\Users\elias\OneDrive\Github-LFS\INDEX.md`.

Consulte [ARCHITECTURE.md](./docs/proyecto/ARCHITECTURE.md) para las fronteras y dependencias entre sectores.
