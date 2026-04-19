# CHANGELOG NOCTURNO — 2026-04-19 (actualizado)

## Resumen Ejecutivo

Sistema de comparación de filtros TIA/Opa en PSoC 5LP con osciloscopio Python.
**Estado hardware:** PSoC requiere compilar y reflashear (ver ACCIONES MANUALES).
**Estado backend Python:** PASS ✓ (test_backend.py — 7277 paquetes en 5s, 0 CRC errors).

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

---

## Sesión nocturna 2026-04-19 (Fase 8 completada + tests exhaustivos)

### Bugs críticos encontrados y corregidos

#### `ChannelFilter.process()` — estado de filtro corrompido entre bloques
- **Bug**: `zi * x[0]` se aplicaba en *cada* llamada a `process()`, no solo en la primera.
  Al procesar bloque a bloque, el estado `zi` era multiplicado por el primer sample del nuevo
  bloque, destruyendo la continuidad del filtrado. Diferencia bloque vs. pasada única: 1.91 (RMS).
- **Fix**: Se agregó flag `_fresh` al `ChannelFilter`. El truco `zi * x[0]` solo se aplica
  cuando `_fresh=True` (primera llamada tras load/reset). Diferencia post-fix: < 1e-10.

#### `simulador_psoc.py` rx_thread — muerto por EIO antes de que el test abra el PTY
- **Bug**: El simulador cierra su extremo slave del PTY (`os.close(slave_fd)`) antes de que el
  test lo abra. En ese intervalo, `os.read(master_fd)` devuelve `EIO`. El `except OSError: break`
  mataba el thread RX permanentemente. Cualquier test que tarde >~0.2s en abrir el slave veía
  0 paquetes sin error explícito.
- **Fix**: rx_thread ahora hace `continue` en `errno.EIO` con `sleep(0.005)`, reviviendo
  automáticamente cuando el slave se conecta.

#### `simulador_psoc.py` — post_digital siempre sintético, ignoraba el FIR cargado
- **Bug**: `_make_data_pkt()` siempre generaba `digital_i = 0.074 * sin(10 Hz)` aunque
  `fir_loaded = True`. El FIR Q1.15 era recibido por el simulador pero nunca ejecutado.
- **Fix**: `_make_data_pkt()` ahora aplica el algoritmo exacto del PSoC (delay circular int32,
  MAC int64, >>15, saturación ±0x7FFFFF) sobre `analog_i` cuando `fir_loaded=True`.
  Delay line se limpia en CMD_LOAD_FIR y CMD_FIR_CLEAR.

#### `design_fir_notch()` — ancho de banda insuficiente para atenuación real
- **Bug**: Usaba `bw = max(2.0, f * 0.05)` que da 3 Hz para 60 Hz. Con N=63 taps y
  fs=1500 Hz, la resolución mínima es ~190 Hz/transición. El filtro producía < 1 dB de
  atenuación en lugar de ≥ 20 dB.
- **Fix**: Default cambiado a `n_taps=255` (máximo firmware) y `bw = max(20.0, f * 0.33)`.
  Resultado: 50 dB de atenuación @ 60 Hz con 255 taps.

#### `vdac_generator.ricker/gauss3` — división por cero con sigma_s=0
- **Bug**: `u = t / sigma_s` producía NaN cuando `sigma_s=0`. Numpy silenciaba la excepción
  y `astype(np.uint8)` convertía NaN a 0, devolviendo una señal muda en lugar de un pulso.
- **Fix**: `sigma_s = max(sigma_s, 1.0 / fs)` antes de la división.

#### `cmd_load_fir` — ValueError/OverflowError con coeficientes NaN/inf
- **Bug**: `int(round(nan * 32768))` lanzaba `ValueError`; `int(round(inf * 32768))` lanzaba
  `OverflowError`. Si algún coeficiente era no-finito, el frame de comando no se generaba.
- **Fix**: Guard `if math.isfinite(c) else 0` mapea NaN/inf a Q1.15=0 silenciosamente.

---

### Nuevos tests (125 scenarios totales — 125/125 PASS)

| Archivo | Scenarios | Qué verifica |
|---------|-----------|--------------|
| `test_fir_math.py` | 7 | Q1.15 FIR pass-through, zeros, notch 60 Hz (255 taps), lowpass 20 Hz, SNR≥60dB, saturación, consistencia cmd |
| `test_protocol_builders.py` | 19 | Todos los command builders byte-by-byte |
| `test_parse_packet.py` | 19 | parse_packet + effective_fullscale, todos CFG×gain |
| `test_debug_protocol.py` | 18 | parse_debug_packet, parse_state_packet, format_event |
| `test_vdac_state.py` | 17 | vdac_generator range/norm, sigma_s=0, NaN guard, parse_state_packet |
| `test_parser_adversarial.py` | 10 | Parser con byte streams hostiles: garbage, interleaved, plen grande |
| `test_fir_robust.py` | 10 | FIR loading + streaming con PTY real |
| `test_protocol_stress.py` | 10 | Stress de protocolo: rate, rollover de secuencia, reload FIR |
| `test_channel_filter.py` | 11 | ChannelFilter: FIR/IIR/notch/bandpass, block processing, state |
| `test_fir_simulador_integration.py` | 4 | FIR aplicado en paquetes reales: identidad, ceros, FIR_CLEAR |

Backend end-to-end: `test_backend.py` → 7342 paquetes en 5s, 0 CRC errors.
ESP receiver: `test_receiver.py` → 12/12 PASS.

---

### Fase 9 — ESP32 WiFi (base planteada)

Archivos creados en `src/esp/`:
- `node/platformio.ini` — proyecto PlatformIO ESP32
- `node/src/psoc_spi.h/cpp` — clase PsocSPI: SPI master @ 4 MHz, decode frame 0xAB, batch de 30 muestras
- `node/src/time_sync.h` — clase TimeSync: NTP via WiFi, `nowUs()` = epoch μs
- `node/src/wifi_transport.h` — UDP sendBatch() con marker 0xBC, timestamp_us (uint64 LE)
- `node/src/main.cpp` — boot: WiFi→NTP→SPI loop
- `base/receiver.py` — servidor UDP base: NodeAccumulator, detección de drops, guardado .npz
- `base/test_receiver.py` — 12 scenarios: happy path, CRC, rollover, multi-nodo

**Estado**: Arquitectura planteada. No probado en hardware real.

---

### Estado actual del firmware PSoC

Sin cambios en esta sesión. El firmware implementado incluye:
- FIR software: hasta 255 taps Q1.15, circular buffer 256, MAC int64
- CMD_LOAD_FIR (0x0A) y CMD_FIR_CLEAR (0x0B) en el protocolo
- Eventos debug 0x51 (FIR_LOADED) y 0x52 (FIR_CLEAR)
- Saturación ±0x7FFFFF en la salida del FIR

**Acción requerida**: compilar y reflashear PSoC con PSoC Creator.
