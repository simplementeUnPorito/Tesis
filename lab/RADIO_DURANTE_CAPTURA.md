# ESP-NOW durante captura

Archivo inspeccionado: `src/firmware/esp32/Nodo comunicación/slave/src/main.cpp`.

| llamada | linea | disparador | durante muestreo si/no |
|---|---:|---|---|
| `espnowSend` en `sendToMaster` | 629 | Primitiva común para cualquier envío al maestro | depende del llamador |
| `sendToMaster` en `sendCfgAck` | 1530 | ACK de configuración; usado por comandos y ACK de finalización | no en captura normal |
| `sendToMaster` en `servicePsocConfigAck` | 1677 | NACK de `SD_READ_BATCH`; la función retorna si `g_state == SAMPLING` | no |
| `espnowSend` en `serviceRfTest` | 2740 | Test RF de laboratorio, cada ejecución del período configurado | sí, si se ejecuta durante captura; no es captura normal |
| `sendToMaster` en `serviceRfTest` | 2741 | Rama unicast del mismo test RF cuando no usa broadcast | sí, si se ejecuta durante captura; no es captura normal |
| `sendToMaster` en `sendStartAck` | 4047 | ACK/NACK de START probe o START inválido | no; START durante `SAMPLING` retorna sin ACK |
| `sendToMaster` en `sendHotWaitAck` | 4194 | Entrada, consulta o aborto de `HOT_WAIT` | no |
| `sendToMaster` en `handleCommand` | 4480 | ACK de `CMD_ARM` | no |
| `sendToMaster` en `handleCommand` vía `sendStartAck` | 4557 | `CMD_START` no permitido cuando no está listo | no |
| `sendToMaster` en `handleCommand` | 4610 | ACK de `CMD_DEBUG` | no en captura normal |
| `sendToMaster` en `handleCommand` | 4663 | ACK de `CMD_SET_RECLEN` | no en captura normal |
| `sendToMaster` en `handleReqBatch` | 4762 | NACK de `CMD_REQ_BATCH` fuera de rango; se rechaza antes si `SAMPLING` | no |
| `sendToMaster` en `handleReqBatch` | 4772 | NACK de retry mientras una lectura SD está pendiente | no |
| `sendToMaster` en `handleReqBatch` | 4784 | NACK si falta el lote en RAM | no |
| `transport.sendStoredBatch` en `handleReqBatch` | 4789 | `CMD_REQ_BATCH` válido, después de terminar la captura | no |
| `sendToMaster` en `servicePsocSdReadTimeout` | 4800 | Timeout de lectura SD solicitada | no durante captura normal |
| `transport.sendStoredBatch` en `onPsocBatch` | 4897 | Respuesta a lote leído desde SD; la captura ya terminó | no |
| `transport.sendStoredBatch` en `onPsocBatch` | 4951 | `g_debug_mode`: lote de rampa transmitido al recibir cada batch | sí, excepción de laboratorio |
| `sendToMaster` en `loop`/servicio periódico | 5325 | HELLO cada 2 s, condicionado a no estar en `SAMPLING`/`HOT_WAIT` | no |
| `sendToMaster` en `loop`/servicio periódico | 5349 | STATUS cada 10 s, condicionado a no estar en `SAMPLING` | no |

Conclusión 1: una captura de campo normal (`CMD_START` con store-and-forward) no transmite lotes ESP-NOW en vivo durante `SAMPLING`.
Conclusión 2: los lotes normales se guardan en RAM o SD, se pasa a `STOPPED` al completar y se transmiten después mediante `CMD_REQ_BATCH` o lectura SD.
Conclusión 3: solo el modo explícito de laboratorio `g_debug_mode` transmite lotes durante muestreo; el test RF de laboratorio también puede transmitir, pero no representa una captura normal.

IA principal: Codex modelo no reportado
Delegados: ninguno
Fallbacks: ninguno
