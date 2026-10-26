# Pendientes de Elias — 26 de octubre de 2026

El estado completo y la separación entre resultados medidos y funciones todavía no probadas en placa están en `INFORME_SISTEMA_2026-10.md`.

Siglas usadas: Analog-to-Digital Converter (ADC), inicio de conversión (SOC), fin de conversión (EOC), entrada/salida digital de propósito general (GPIO), Low-Voltage Transistor-Transistor Logic (LVTTL), interconexión digital (DSI), Phase-Locked Loop (PLL), bloque digital universal (UDB), memoria de acceso aleatorio (RAM), Secure Digital (SD), Fine Timing Measurement (FTM), Espressif IoT Development Framework (ESP-IDF), filtro de respuesta finita al impulso (FIR), valores separados por comas (CSV), contenedor comprimido (ZIP), capa física (PHY), transmisión (TX), receptor-transmisor asíncrono universal (UART), Universal Serial Bus (USB) y actualización por el aire (OTA).

## 1. PSoC Creator: reloj, SOC y ADC

Estas tareas son obligatorias antes de considerar validada la nueva base de tiempo de 2000 Hz.

### 1.1. Cableado

1. Unir las masas del ESP32-S3 y del PSoC 5LP.
2. Conectar **ESP GPIO 1 → pin digital libre del PSoC para SOC**.
   - Configurar la entrada con umbral Low-Voltage Transistor-Transistor Logic (LVTTL), porque el PSoC está alimentado a 5 V y el ESP entrega 3,3 V.
   - Agregar una resistencia serie de 22–47 ohm cerca del emisor para amortiguar flancos.
3. Conectar **ESP GPIO 2 → pin digital libre del PSoC para reloj**.
   - Configurar también como LVTTL.
   - Llevar la señal por Digital System Interconnect (DSI) al bloque de reloj/Phase-Locked Loop (PLL).
4. Elegir pines alejados de los puertos analógicos 0 y 3. Orden sugerido:
   - P12[x] con Special Input/Output (SIO), si está disponible en la placa;
   - en su defecto P2[0], P2[2]–P2[5], P15[1] o P15[4]–P15[7].
5. Verificar en el esquema y en la placa que el pin elegido no tenga otra carga, función de arranque ni conexión externa incompatible.

### 1.2. Reloj del PSoC

1. Crear o configurar la entrada de reloj externa desde el pin conectado a GPIO 2.
2. Enrutarla por DSI al PLL.
3. Configurar **8 MHz / 4 × 12 = 24 MHz**.
4. Usar esos 24 MHz como reloj de bus, igual que en la configuración actual.
5. Confirmar en el reporte de timing que no se introdujeron violaciones y que el IMO deja de ser la referencia de frecuencia de la adquisición.

### 1.3. ADC Delta-Sigma

Configurar el Analog-to-Digital Converter Delta-Sigma (ADC_DelSig) de la siguiente forma:

- modo **Single Sample**;
- resolución **18 bits**;
- disparo **Hardware SOC**;
- reloj del ADC **≤ 3,027 MHz**;
- tasa de conversión solicitada cercana a **2400 muestras/s**, con margen para aceptar un pulso SOC cada **500 us**.

La latencia calculada actual es cercana a 414 us, pero debe medirse. Si PSoC Creator informa que la conversión no termina antes del SOC siguiente, se debe bajar el reloj/tasa solicitada o revisar la configuración antes de grabar.

### 1.4. `superMaquina`

Modificar el esquema/componente para que:

1. SYNC habilite la ventana de adquisición.
2. Los pulsos SOC externos lleguen al ADC solamente con SYNC alto.
3. La compuerta sea de hardware —DSI/UDB— y no dependa de firmware ni de una interrupción.
4. Al bajar SYNC no quede un nuevo SOC pendiente; se debe documentar qué ocurre si baja durante una conversión ya iniciada.
5. El primer pulso aceptado después del START corresponda a la muestra 0.

### 1.5. Recompilación y memoria

1. Abrir `AcondicionamientoAnalogico.cydsn` en PSoC Creator.
2. Regenerar componentes y compilar el proyecto completo.
3. Revisar RAM, flash, uso de UDB y timing.
4. Confirmar el costo de `aa_decim.h` en Q1.23:
   - 2044 B para 511 coeficientes `int32`;
   - 2044 B para el historial;
   - acumulador de 64 bits.
5. Confirmar que el bloque Filter acepta las 128 palabras Q1.23 y que el FIR de 2000 Hz carga 127 taps útiles más un cero.
6. No usar `program_psoc.ps1 -SkipBuild` hasta comprobar que el artefacto generado corresponde a esta compilación.

## 2. Medición con osciloscopio

Realizar y guardar capturas de pantalla o CSV de estas mediciones:

1. **GPIO 2:** 8 MHz estables, ciclo útil cercano a 50 %, presentes desde el arranque y antes de liberar el PSoC.
2. **GPIO 1:** período de 500 us y pulso cercano a 3 us.
3. **SOC→EOC:** medir la latencia real; valor calculado de referencia, aproximadamente 414 us.
4. **SYNC→primera muestra:** verificar que el primer SOC aceptado sea el previsto y que no se cuele un pulso con SYNC bajo.
5. **Dos esclavos contra el maestro:** comparar GPIO 1 de dos S3 y el marcador de START del maestro.
6. Repetir durante varios minutos con Fine Timing Measurement (FTM) activo, pausado y radio apagada para observar fase y deriva.
7. Para N=4, comprobar indirectamente o mediante datos que sobrevivan las muestras 0, 4, 8, 12, ...

## 3. Pruebas con hardware real

1. Desactivar `SIM_SIN_HW` en `slaveS3`; se recomienda mantener `REMOTE_LOG_ENABLE`.
2. Probar esclavos con PSoC y Secure Digital (SD) reales en:
   - asincrónico, almacenes 0, 1 y 2;
   - tiempo real, almacenes 0, 1 y 2;
   - descarga rápida;
   - captura sin límite y STOP;
   - recuperación `FILL`;
   - FTM activo, pausado y radio apagada.
3. Ejecutar:

```powershell
python lab/s3/matriz_pruebas.py --con-ota --con-duracion --duracion-s 840
```

4. Repetir las firmas de ruido con `lab/ruido_firmas`, power bank y sin USB en el esclavo.
5. Verificar que el ZIP incluya `time_marks.csv`, `sample_rate_mhz=2000000` para N=1 y metadata coherente de FIR, N, fase y retardos.
6. Cargar el ZIP en la aplicación Python y comparar `fs_hz` y `residual_rms_us` entre nodos.
7. Corregir antes de congelar el formato dos campos heredados de metadata en `applyNodeDecimation()`: `first_surviving_input_index` todavía informa `N-1` aunque la fase vigente conserva 0, N, 2N, ...; `verification_candidate` todavía apunta al CSV Q15 eliminado en vez del Q1.23.

## 4. Compatibilidad y escala

1. Regrabar los esclavos clásicos WROOM con el firmware actual. Siguen en ESP-IDF 4.4, no poseen FTM y fuerzan START por broadcast cuando participan.
2. Probar más de 5–6 nodos. La capacidad actual a N=1 es una estimación por tiempo de aire, no una medición.
3. Para 8 GEO + HAMMER, decidir entre:
   - N≥2;
   - tasa Physical Layer (PHY) de 6–11 Mbps, con medición de alcance;
   - otra reducción de tráfico.
4. Calibrar distancia FTM en campo con cinta, en al menos tres distancias por nodo. Sin calibración, la distancia es indicativa.

## 5. Decisiones pendientes

1. Confirmar `SIM_SIN_HW=0` para las imágenes de placa.
2. Decidir si el registro remoto queda activo en campo; se recomienda conservarlo.
3. Mantener ESP-IDF 5.5 con TX raw y FTM por turnos como configuración principal; conservar `masterS3_idf44` como respaldo.
4. Definir la política de N/tasa PHY para la cantidad final de nodos.
5. Decidir si se incorpora `docs/diseno_s3/OTA_FTM_DISENO.md` al historial del submódulo `docs`.

## 6. Estado del banco

- Maestro en COM14: `masterS3_log`, ESP-IDF 5.5, registro humano por UART0 mezclado con el protocolo binario.
- Esclavos 2, 3 y 4: `slaveS3_2`, `slaveS3_3` y `slaveS3_4`, todavía con simulador.
- Para campo, grabar `masterS3` sin log:

```powershell
cd "src/firmware/esp32/Nodo comunicación/masterS3"
pio run -e masterS3 -t upload --upload-port COM14
pio run -e masterS3 -t uploadfs --upload-port COM14
```

- OTA de esclavos:

```powershell
python lab/s3/ota.py --node N --env slaveS3_N
```

---

Proveniencia: IA principal Codex (modelo no reportado); delegados: ninguno; fallbacks: ninguno.
