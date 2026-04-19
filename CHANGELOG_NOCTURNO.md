# CHANGELOG NOCTURNO — 2026-04-19

## Resumen ejecutivo
Correcciones de 4 bugs críticos en la GUI Python que impedían el arranque, y verificación del protocolo PSoC-Python mediante test headless.

---

## Python — `src/python/geophone_scope/`

### `main_window.py` — 4 bugs críticos corregidos
Todos causaban `AttributeError` / crash al iniciar la aplicación:

1. **`self._uart` no inicializado** — `UartWorker()` no se creaba; `closeEvent()` y `_toggle_uart()` lanzaban AttributeError.
   Fix: Inicializado en `__init__`; señal `debug_event` conectada a `_on_debug_event`.

2. **`self._uart_combo` no creado** — `_refresh_ports()` crasheaba al limpiar el combo UART.
   Fix: `QComboBox` creado en `_build_debug_tab()`.

3. **`self._btn_uart` no creado** — `_toggle_uart()` crasheaba.
   Fix: Botón checkable "Conectar UART" creado en `_build_debug_tab()`.

4. **`self._debug_ch_combo` no creado** — `_on_state_update()` crasheaba al sincronizar estado del PSoC.
   Fix: Combo ["USB", "UART", "Ambos"] creado en `_build_debug_tab()`.

### Funcionalidad añadida en `_build_debug_tab()`
- Sección UART: combo de puerto + **combo de baudios** (9600–230400, default 115200).
  Satisface regla 2 — el usuario elige baudrate para que coincida con el PSoC.
- Selector de canal de debug (USB / UART / Ambos) → dispatch a `_on_debug_ch_changed()`.
- Botón `CMD_GET_STATE` para solicitar estado PSoC bajo demanda.

### Nuevo import en `main_window.py`
`from uart_worker import UartWorker`

---

## Firmware PSoC — `src/psoc/Comparation.cydsn/`

**No se modificaron archivos en esta sesión.** El firmware ya estaba correcto:

- `AnalogToDigital.c`: constantes `ADC_DelSig_BUF_GAIN_8X/4X/2X/1X` con sufijo `X` correcto.
- `Communication.c`: transparencia USB/UART via `s_last_iface` — responde por donde recibió el comando.
- `main.c`: TDs de DMA configurados en bucle infinito — no satura el buffer.
- `.cyprj`: archivos de `shared/` (debug.c, transport_uart.c, transport_usb.c, *.h) ya en el proyecto; `Additional Include Directories` apunta a `../shared`.

### Acción manual en PSoC Creator (si hay errores de compilación)
1. Build → Clean → Build → Rebuild All.
2. Verificar en Project Properties → Build → C/C++ → Additional Include Directories: `../shared`.

---

## Test headless del protocolo

```
[TEST] Resultados tras 5 s de captura:
  Paquetes 0xAA (data):     7228  (mínimo esperado: 5625)
  Paquetes 0xCC (state):       1
  Paquetes 0xDD (debug):       2
  Paquetes malos (CRC):        0
  Errores de rango:            0
[TEST] PASS ✓
```

Protocolo PSoC → Python estable y coherente con el firmware real.

---

## Análisis DMA (regla 3 — no saturar buffer)

- TDs configurados en bucle infinito (TD apunta a sí mismo): no hay overflow por underrun.
- ADC_DelSig genera EOC a 1500 Hz; DMA mueve 3 bytes/muestra en cada cadena.
- Python: chunks de 256 bytes, timeout 50 ms. `BATCH_SIZE=30` en SerialWorker.
- PyQtGraph actualiza a ~50 Hz real — sin acumulación de backlog en el buffer.
