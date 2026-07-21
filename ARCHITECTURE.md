# Arquitectura de repositorios

## Principio de separación

Cada repositorio posee una tecnología, sus instrucciones de ejecución, sus artefactos ignorados y sus dependencias externas. Las interfaces entre sectores son protocolos o formatos documentados; no se comparten árboles de fuentes mediante rutas internas.

```text
PSoC 5LP ──UART/SYNC──> ESP32 esclavo ──ESP-NOW──> ESP32 maestro
   │                                                    │
   └── muestras binarias                               ├── UI web
                                                        ├── Python/PyQt
                                                        └── MATLAB

data/raw ──> software/python ──> data/processed
     └─────> modelado/matlab
```

## Reglas de dependencia

- `firmware/psoc` y `firmware/esp32` se coordinan por el protocolo UART y las señales de sincronización; ninguno incluye fuentes del otro.
- `software/python` contiene sus propios submódulos `ADsurf` y `maswavespy`.
- `modelado/matlab` contiene su propio submódulo `MASW-Matlab-code`.
- `docs` puede enlazar a todos los sectores, pero ningún componente necesita `docs` para compilar.
- `investigacion/sources` es una biblioteca local ignorada. Las notas sí se versionan; los PDF de terceros no.
- `data` versiona estructura y catálogo, nunca los binarios de medición.

## Versionado integrado

Un commit de `Tesis` es una línea base reproducible: registra un SHA concreto para cada submódulo. El desarrollo ocurre dentro del repositorio dueño del cambio; el superproyecto se actualiza únicamente cuando una combinación de revisiones debe probarse o entregarse como conjunto.
