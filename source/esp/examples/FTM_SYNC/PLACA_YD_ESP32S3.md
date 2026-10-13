# Placas del ensayo: probable YD-ESP32-S3 V1.3 N16R8

El usuario indica cinco placas EGBO ESP32-S3 N16R8 y una inscripción trasera que leyó como «V1120 YO-ESP32-S3 2022-V1.3». Probablemente sea YD-ESP32-S3; la identificación es provisional porque no se pudo abrir la ficha de AliExpress y no se inspeccionó físicamente la placa.

Fuente primaria del fabricante: https://github.com/vcc-gnd/YD-ESP32-S3/blob/main/README.md . Documenta WS2812 RGB en GPIO48, GPIO7 disponible, USB nativo en GPIO19/20 y otro puerto con puente CH343P. Confirmar que la serigrafía y el módulo coincidan antes de cargar/conectar.

Para el ensayo: GPIO7 como salida MCPWM de pulsos; las sondas van al pad/pin rotulado 7 y GND de cada placa. El número GPIO no es el número de posición del conector. Usar sondas x10, señales de 3.3V y masa común. No conectar las salidas de dos placas entre sí. Sólo hacen falta pines o puntos de prueba en GPIO7 y GND para medir.

LED integrado opcional: en menuconfig, Time Synchronization Configuration > GPIO and Timing: Enable status LED = yes, LED GPIO Pin Number = 48, LED is WS2812 RGB type = yes. Aplicar en los cinco perfiles. El GPIO48 transmite datos del LED; no es el flanco de referencia a comparar en el osciloscopio. El parpadeo visual pasa por una tarea y no demuestra precisión de nanosegundos.

N16R8 anuncia 16 MB de flash y 8 MB de PSRAM. Este ensayo no necesita PSRAM: mantenerla deshabilitada evita depender de su configuración. Una imagen configurada para 4 MB puede usar la región inicial de una flash de 16 MB; no equivale a utilizar toda la memoria. Confirmar tamaño de flash durante la carga.

Los perfiles de LED y GPIO no sustituyen la comprobación física del modelo. No hay prueba de hardware ni promesa de desfase/jitter.

IA principal: Codex GPT-6
Delegados: Claude claude-sonnet-5-5, preparación FTS; Codex gpt-5.6-sol, ejemplos oficiales.
Fallbacks: ninguno.