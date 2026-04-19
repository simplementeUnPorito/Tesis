# CHANGELOG NOCTURNO — 2026-04-19

Cambios técnicos realizados en la sesión nocturna automatizada.

---

## Firmware PSoC 5LP (`src/psoc/Comparation.cydsn` + `src/psoc/shared/`)

### 1. Transparencia UART/USB en `Communication.c`

**Problema:** El firmware solo leía comandos del USB CDC y respondía siempre por USB.  
Si alguien enviaba un comando por UART_PC, la respuesta iba por USB (invisible).

**Cambio:**
- Añadida variable `s_last_iface` (IfaceId_t: IFACE_USB / IFACE_UART).
- En `Communication_Task()`: se agrega loop de lectura UART_PC con `TransportUART_RxAvailable()` / `TransportUART_RxRead()`. Al leer un byte por UART, se marca `s_last_iface = IFACE_UART`.
- En `Communication_SendState()`: se selecciona `TransportUART_SendState()` o `TransportUSB_SendState()` según `s_last_iface`.

**Líneas modificadas:** `Communication.c` — `Communication_Init()`, `Communication_Task()`, `Communication_SendState()`.

### 2. UART_PC siempre activo en `Communication_Init()`

**Cambio:** `Communication_Init()` llama `TransportUART_Init()` (= `UART_PC_Start()`) de forma incondicional, independientemente de si `uart_transport` está registrado como transporte de datos. Esto permite el RX de transparencia sin activar el stream UART.

### 3. Nuevas funciones en `transport_uart.h/.c`

| Función | Descripción |
|---|---|
| `TransportUART_SendState(...)` | Envía paquete 0xCC de estado por UART_PC (mismo formato que USB) |
| `TransportUART_Init()` | Llama `UART_PC_Start()` (separado del callback UART_Init en Transport_t) |
| `TransportUART_RxAvailable()` | Wrapper de `UART_PC_GetRxBufferSize()` |
| `TransportUART_RxRead()` | Wrapper de `UART_PC_ReadRxData()` |

### 4. Corrección previa (de sesión anterior) — BUF_GAIN constants

- `AnalogToDigital.c`: `ADC_DelSig_BUF_GAIN_8` → `ADC_DelSig_BUF_GAIN_8X` (y equivalentes para 1X/2X/4X). El sufijo `X` es requerido por la API del PSoC Creator.

### 5. USB CONFIG NUM (corrección de raíz)

- `transport_usb.c`: `USBFS_Start(USB_CONFIG_NUM, ...)` donde `USB_CONFIG_NUM = 0u` (0-based). El firmware viejo usaba `1u` → **"Invalid Device Descriptor"**.

---

## Software Python (`src/python/geophone_scope/`)

### 1. `simulador_psoc.py` — NUEVO

Emulador completo del PSoC para pruebas sin hardware:
- Crea un par PTY virtual con `os.openpty()` (Linux).
- Genera 3 señales sintéticas: señal de 10 Hz + ruido 60 Hz (cruda), versión filtrada analógica, filtrada digital.
- Emite paquetes `0xAA` a 1500 Hz cuando streaming está activo.
- Parsea comandos `0xBB` con la misma máquina de estados que el firmware C.
- Responde con paquetes `0xCC` de estado tras cada comando.
- Emite paquetes `0xDD` de debug en boot y en START/STOP.

**Uso:** `python simulador_psoc.py` → imprime el path del puerto PTY.

### 2. `test_backend.py` — NUEVO

Prueba headless (sin GUI, sin Display) que valida el protocolo end-to-end:
- Lanza `simulador_psoc.py` como subproceso.
- Conecta al PTY slave, envía `CMD_START`.
- Captura paquetes durante 5 segundos.
- Verifica: tasa ≥75% (1500 Hz × 5 s = 7500 pkts, mínimo 5625), CRC correcto en todos, voltajes dentro de rango físico.
- Sale con código 0 (PASS) o 1 (FAIL).

**Uso:** `./venv/bin/python test_backend.py`

### 3. `app_logger.py` — Logs en carpeta `logs/`

Los archivos `.log` se generan en `logs/geophone_YYYYMMDD_HHMMSS.log` (no en la raíz). Directorio creado automáticamente.

---

## Archivos que necesitan acción manual en PSoC Creator

> **Estos cambios NO se pueden hacer desde el script — requieren el IDE:**

1. **Abrir PSoC Creator** y cerrar/reabrir el proyecto `Comparation.cydsn`.
2. **Agregar los archivos al proyecto** (click derecho → Add → Existing Item):
   - `src/psoc/shared/debug.c`
   - `src/psoc/shared/transport_usb.c`
   - `src/psoc/shared/transport_uart.c`
3. **Verificar que el path `../shared` esté en** Build Settings → Compiler → Additional Include Directories.
4. **Build → Rebuild All** (debe compilar sin errores).
5. **Program → PSoC** para flashear.
6. **Reconectar cable USB** del PSoC para que enumere con nuevo firmware.

---

## Prueba recomendada post-flash

```
# 1. Verificar protocolo con simulador (headless)
cd src/python/geophone_scope
./venv/bin/python test_backend.py

# 2. Arrancar osciloscopio real
./venv/bin/python main.py
```

El log en `logs/` mostrará bytes recibidos (`RAW(...)`) si el PSoC envía correctamente.
