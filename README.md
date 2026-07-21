# Tesis — sistema integrado MASW

Este repositorio es el **superproyecto** de la tesis. Ya no contiene firmware, aplicaciones, simulaciones, documentación ni mediciones directamente: fija versiones compatibles de repositorios independientes mediante submódulos Git.

## Mapa del proyecto

| Sector | Ruta | Repositorio | Responsabilidad |
|---|---|---|---|
| Firmware | `firmware/psoc` | [Tesis-firmware-psoc](https://github.com/simplementeUnPorito/Tesis-firmware-psoc) | adquisición, acondicionamiento y calibración PSoC 5LP |
| Firmware | `firmware/esp32` | [Tesis-firmware-esp32](https://github.com/simplementeUnPorito/Tesis-firmware-esp32) | maestro, esclavos, ESP-NOW y UI web |
| Software | `software/python` | [Tesis-software-python](https://github.com/simplementeUnPorito/Tesis-software-python) | GUI, revisión de campo y análisis MASW |
| Modelado | `modelado/matlab` | [Tesis-modelado-matlab](https://github.com/simplementeUnPorito/Tesis-modelado-matlab) | MATLAB, Simulink y modelos de la cadena analógica |
| Documentación | `docs` | [Tesis-documentacion](https://github.com/simplementeUnPorito/Tesis-documentacion) | entregables, diagramas, planes y handoffs |
| Investigación | `investigacion` | [Tesis-investigacion](https://github.com/simplementeUnPorito/Tesis-investigacion) | vault de Obsidian, bitácora y notas académicas |
| Datos | `data` | [Tesis-datos](https://github.com/simplementeUnPorito/Tesis-datos) | catálogo y estructura local de mediciones |

Cada sector se puede clonar, probar y versionar por separado. `Tesis` solo expresa qué revisión de cada sector forma una configuración integrada.

## Clonar el sistema completo

```powershell
git clone --recurse-submodules https://github.com/simplementeUnPorito/Tesis.git
cd Tesis
.\scripts\bootstrap.ps1
```

Si el repositorio ya estaba clonado:

```powershell
git pull
git submodule sync --recursive
git submodule update --init --recursive
```

## Trabajar en una parte aislada

Entre en el submódulo correspondiente y cree allí su rama y commit. Luego vuelva a `Tesis` y actualice el puntero del submódulo en un commit separado. Esto evita que un cambio de Python quede mezclado con firmware o documentación.

Los datos locales viven en `data/raw/` y `data/processed/`; Git ignora ambos directorios. La aplicación Python también acepta `TESIS_DATA_ROOT` para usar un almacén situado fuera de este árbol.

Consulte [ARCHITECTURE.md](./ARCHITECTURE.md) para las fronteras y dependencias entre sectores.
