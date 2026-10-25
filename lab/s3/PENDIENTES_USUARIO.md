# Lo que necesito de Elias (2026-10-24)

Esto queda despues del banco S3 sin hardware (ver `INFORME_BANCO_S3.md`).

## Decisiones

1. **FTM (IDF 4.4 y 5 probados, ver informe).** El responder del maestro S3 rechaza todas las sesiones (`FTM_STATUS_CONF_REJECTED`), aun habilitado antes de levantar ESP-NOW y con cinco configuraciones distintas. El prototipo `ftm-test`, que si mide, corre ESP-IDF 5.5. Opciones:
   - a) migrar masterS3/slaveS3 a Arduino 3 (IDF 5.x) con pioarduino. Es un cambio de plataforma grande: hay que revalidar todo.
   - b) dejar FTM fuera de esta version: la sincronia sigue siendo por START broadcast y la distancia queda sin medir.
2. **Mas de 5-6 nodos a 2604 Hz.** Por tiempo de aire estimo que entran ~5-6 nodos a N=1. Para 8 GEO + HAMMER:
   - a) decimar con N>=2;
   - b) subir la tasa PHY de ESP-NOW (6-11 Mbps). Reduce el aire ~6 veces pero tambien el alcance, y hay que medirlo en campo.
3. **Simulador y log remoto.** Hoy estan prendidos en `slaveS3` (`SIM_SIN_HW=1`, `REMOTE_LOG_ENABLE=1`). Antes de la placa real hay que sacar `SIM_SIN_HW`. Conviene decidir si el log remoto queda (sirve para diagnosticar nodos sin cable en campo).

## Tareas con hardware

1. **PSoC real:** grabar `program_psoc.ps1 -SkipBuild` y probar en placa:
   - el antialias (FIR Kaiser antes de decimar): tiempos de la ISR y respuesta;
   - la carga del FIR del bloque Filter desde la web (pestana Filtros, "FIR del PSoC").
2. **Esclavos con PSoC y SD reales** (`slaveS3` sin `SIM_SIN_HW`):
   - repetir `lab/s3/captura_ws.py` en todos los modos;
   - repetir las firmas con `lab/ruido_firmas` y el procedimiento del README (power bank, sin USB en el esclavo).
3. **Nodo 3** (MAC e0:72:a1:f4:99:90): tiene firmware viejo. Grabarlo por USB una vez con `slaveS3_3` (las siguientes van por OTA).
4. **Esclavos clasicos (WROOM):** regrabarlos con el firmware actual. El filtro de MAC nuevo hace falta para hablar con un maestro S3.
5. **Distancia por FTM:** solo si se resuelve la decision 1. Medir en campo con cinta en tres o mas distancias por nodo (`lab/s3/ftm_registro.py`).
6. **Docs:** `docs/diseno_s3/OTA_FTM_DISENO.md` sigue sin commitear en el submodulo `docs`. Confirmame si lo subo.

## Como dejo el banco

**Maestro S3 en COM14** con `masterS3_log`: log humano por la UART0, mezclado con el binario de MATLAB. Para campo, grabar `masterS3` (sin log):

```
cd "src/firmware/esp32/Nodo comunicación/masterS3"
pio run -e masterS3 -t upload --upload-port COM14
pio run -e masterS3 -t uploadfs --upload-port COM14
```

**Esclavos 2 y 4:** `slaveS3_2` y `slaveS3_4` con el simulador. Se actualizan por OTA:

```
python lab/s3/ota.py --node N --env slaveS3_N
```
