# Lo que necesito de Elias (actualizado 2026-10-25)

Esto queda despues del banco S3 sin hardware (ver `INFORME_BANCO_S3.md`).

## Decisiones

1. **Mas de 5-6 nodos a 2604 Hz.** Por tiempo de aire estimo que entran ~5-6 nodos a N=1. Para 8 GEO + HAMMER:
   - a) decimar con N>=2;
   - b) subir la tasa PHY de ESP-NOW (6-11 Mbps). Reduce el aire ~6 veces pero tambien el alcance, y hay que medirlo en campo.
2. **Simulador y log remoto.** Hoy estan prendidos en `slaveS3` (`SIM_SIN_HW=1`, `REMOTE_LOG_ENABLE=1`). Antes de la placa real hay que sacar `SIM_SIN_HW`. Recomiendo dejar el log remoto: con el es que encontre el panico de los esclavos (llega el coredump por radio).

3. **SDK del maestro: IDF 5.5 con FTM, como pediste.** El cuelgue de Espressif (#19269) se esquiva mandando ESP-NOW por `esp_wifi_80211_tx`, y el responder FTM ya no se muere con las sesiones por turnos: 5 corridas de 14 min con 3 nodos sin fallas, START por FTM en todas (1-5 us). Costo: la vista en vivo puede ir 1-3 s atrasada mientras un nodo mide FTM (no se pierde nada). `masterS3_idf44` queda de respaldo.

## Tareas con hardware

1. **PSoC real:** grabar `program_psoc.ps1 -SkipBuild` y probar en placa:
   - el antialias (FIR Kaiser antes de decimar): tiempos de la ISR y respuesta;
   - la carga del FIR del bloque Filter desde la web (pestana Filtros, "FIR del PSoC").
2. **Esclavos con PSoC y SD reales** (`slaveS3` sin `SIM_SIN_HW`):
   - repetir `lab/s3/captura_ws.py` en todos los modos;
   - repetir las firmas con `lab/ruido_firmas` y el procedimiento del README (power bank, sin USB en el esclavo).
3. **Esclavos clasicos (WROOM):** regrabarlos con el firmware actual. El filtro de MAC nuevo hace falta para hablar con un maestro S3. Siguen en IDF 4.4: no tienen FTM, asi que con un clasico en la captura el START sale por broadcast.
4. **Distancia por FTM:** medir en campo con cinta en tres o mas distancias por nodo (pestana Esclavos, "Declarada" + "Punto", o `lab/s3/ftm_registro.py`). Sin calibrar, la distancia FTM es solo indicativa.
5. **Docs:** `docs/diseno_s3/OTA_FTM_DISENO.md` sigue sin commitear en el submodulo `docs`. Confirmame si lo subo.

Los nodos 3 y 4 ya no necesitan nada: volvieron a responder (el 4 tenia guardado un coredump del mismo panico; no se si es lo que lo dejo mudo) y tienen el firmware actual por OTA.

## Como dejo el banco

**Maestro S3 en COM14** con `masterS3_log` (IDF 5.5, log humano por la UART0 mezclado con el binario de MATLAB). Para campo, grabar `masterS3` (sin log):

```
cd "src/firmware/esp32/Nodo comunicación/masterS3"
pio run -e masterS3 -t upload --upload-port COM14
pio run -e masterS3 -t uploadfs --upload-port COM14
```

**Esclavos 2, 3 y 4:** `slaveS3_2`, `slaveS3_3` y `slaveS3_4` con el simulador. Se actualizan por OTA:

```
python lab/s3/ota.py --node N --env slaveS3_N
```
