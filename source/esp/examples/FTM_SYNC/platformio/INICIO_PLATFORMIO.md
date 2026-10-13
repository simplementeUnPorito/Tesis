# Inicio: FTM sincronizado en PlatformIO

Abrí en VS Code / PlatformIO la carpeta `source/esp/examples/FTM_SYNC/platformio` del repositorio. Es un proyecto con ESP-IDF, no requiere Arduino IDE. La configuración tiene cinco entornos: `master`, `slave1`, `slave2`, `slave3` y `slave4`.

Una placa genera la referencia como AP/respondedor FTM; las otras cuatro son STA/iniciadores y disciplinan su temporizador local contra ella. Las cuatro usan la misma lógica de seguidora y se distinguen físicamente por su MAC y por la etiqueta que les pongas. Sincronización entre todas significa aquí que todas siguen la misma referencia. Una malla sin referencia única necesita un protocolo adicional.

## Compilar y cargar

Desde el terminal de PlatformIO, situado en esta carpeta:

```powershell
pio run -e master
pio run -e slave1
```

Después elegí el puerto COM que realmente corresponde a cada placa. `COM9` y `COM10` son ejemplos, no puertos detectados:

```powershell
pio run -e master -t upload --upload-port COM9
pio run -e slave1 -t upload --upload-port COM10
pio device monitor --port COM10 --baud 115200
```

Repetí con slave2, slave3 y slave4 y sus puertos. Podés usar las tareas Build/Upload del entorno en PlatformIO; conectar una sola placa al cargar facilita identificar el puerto. Para estas opciones de consola usá el USB que pasa por el puente serie CH343, no el USB nativo. Confirmá las etiquetas de tus placas.

## LED y osciloscopio

La inscripción que aportaste parece ser YD-ESP32-S3 2022-V1.3 V1120 N16R8. La identificación sigue siendo provisional. Su fabricante documenta WS2812 RGB en GPIO48: está habilitado como WS2812 en este proyecto, nunca como un LED GPIO simple. Las opciones de LED y pulso se cambian en `sdkconfig.defaults`.

Para medir: soldá o prepará un punto de prueba en GPIO7 y GND de cada placa. CH1 va a GPIO7 de la referencia y CH2 a GPIO7 de una seguidora; ambas masas a GND común. No unas las salidas GPIO7 entre sí. Son señales de 3.3 V; usá sondas x10 y cables de masa cortos.

El código de temporizador del snapshot fija 2 kHz y 5 % de ciclo útil: aproximadamente 500 µs entre flancos y 25 µs en alto. Algunos comentarios de upstream todavía dicen 2.5 kHz; prevalecen `DTR_TIMER_PERIOD_US` y `DTR_PULSE_DUTY_PERCENT` en `upstream/components/dtr/include/dtr.h`. El LED visible divide ciclos y su actualización RGB pasa por una tarea: no mide precisión del pulso.

Encendé primero la referencia y después los seguidores, inicialmente dentro de dos minutos. Comenzá con dos placas; después agregá las otras. Compará referencia contra cada seguidora y luego seguidora contra seguidora. Dispará por el flanco ascendente de CH1. Registrá el desfase medio y la variación de ese desfase (jitter) en muchas capturas. Una traza estable con offset fijo no implica desfase cero. Revisá los logs FTM/regresión; un LED que parpadea no demuestra enganche preciso.

## Estado

Se verificaron el snapshot de FTS y los perfiles nativos con comprobaciones estáticas. PlatformIO reconoce los cinco entornos. La compilación no llegó a ejecutarse: PlatformIO intentó descargar platformio/toolchain-riscv32-esp 14.2.0+20251107 (678 MB), pero dos mirrors cortaron la transferencia con IncompleteRead. Se detuvo el intento tras esas fallas. No hay binarios generados, validación de compilación ni medición en hardware. Al volver a ejecutar pio run, PlatformIO reintentará instalar sus dependencias. No se promete precisión de nanosegundos.

Los ejemplos oficiales de distancia están separados en `../FTM`; estimar RTT/distancia y disciplinar un temporizador son experimentos diferentes.

Fuentes: [FTS](https://github.com/abbbe/fts/tree/5d6ea2bfcd516473a98f8aebe7daf690eec21b31), [fabricante de la placa](https://github.com/vcc-gnd/YD-ESP32-S3), [PlatformIO ESP-IDF](https://docs.platformio.org/en/latest/frameworks/espidf.html).

IA principal: Codex GPT-6
Delegados: Claude claude-sonnet-5-5, base FTS; Claude sonnet, integración inicial PlatformIO (timeout antes de handoff); Codex gpt-5.6-sol, ejemplos FTM de Espressif.
Fallbacks: integración PlatformIO completada/revisada por Codex tras timeout del worker; compilación bloqueada por descargas incompletas.