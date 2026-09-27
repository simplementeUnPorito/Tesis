# Revisión crítica de las herramientas de medición

Fecha: 2026-09-27. Alcance: lectura estática de `lab/` y contraste del formato USB con el firmware. No se ejecutó ninguna herramienta de medición, no se abrió COM8 y no se modificó código de operación.

## Prioridad 1 — puede falsear la campaña que está corriendo

### R1. El escalón promedia fotos repetidas y acepta taps inválidos

**Archivo/líneas:** `lab/escalon_idac.py:94-125`, especialmente 107-112 y 122-125; uso en 263-270 y 308-320.

**Defecto y número falso:** `observar()` copia el último valor de `bt._est` cada 5 s, sin guardar edad/sello de adquisición ni exigir `valido[i] == 1`. Por tanto `cola()` puede promediar seis copias del mismo barrido físico —el firmware reduce el barrido a 20 s y el reporte a 30 s al asentarse— y puede calcular mV/código a partir de una lectura fuera de rango. El JSON resultante parece tener seis muestras y una pendiente estable, pero puede contener una sola medición real, o una medición inválida.

**Reproducción:** con un tap actualizado una vez cada 20–30 s, un tramo de 30 s entrega seis entradas de `serie`, pero hasta cinco pueden ser la misma muestra. Si la bandera es 0 y el valor no es `None`, `cola()` igualmente lo incorpora.

**Gravedad:** crítica. Es la herramienta indicada como activa y su salida es directamente la autoridad del IDAC.

### R2. El escalón principal aún puede cruzar cero en un IDAC con signo

**Archivo/líneas:** `lab/escalon_idac.py:257-281`, en particular 279-281; estimación en 297-320.

**Defecto y número falso:** se calcula `alto = clamp(base - paso)` pero no se exige que `base` y `alto` permanezcan del mismo lado de cero. Si `base=+20` y el sondeo elige `paso=80`, el escalón real es `+20 -> -60`. La pendiente informada mezcla los dos regímenes/polaridades bajo un único `dcod`, aunque el valor final y los dos estimadores pueden ser finitos y visualmente razonables.

**Reproducción:** usar un IDAC positivo pequeño y dejar que el sondeo adapte un paso mayor que `base`; o proporcionar `--escalon` mayor que `base`. El clamp no evita el cruce, sólo limita a ±255.

**Gravedad:** crítica.

### R3. Restauración sólo para salida normal; una muerte deja estado de banco alterado

**Archivo/líneas:** `lab/escalon_idac.py:203-223` y 329-346.

**Defecto y número falso:** se ensanchan tres bandas, se desactiva el recentrado y se cambia ganancia antes del `try/finally`; la restauración existe sólo al abandonar normalmente el intérprete. Un kill, caída de alimentación o terminación no manejada durante la corrida deja el nodo con bandas anchas/recentrado apagado y con la ganancia elegida. La campaña siguiente puede medir un controlador distinto del etiquetado. Además, aun en salida normal se restaura `FABRICA` para las bandas (333-334), no los valores guardados en 206-208; una configuración inicial no-fábrica se cambia en silencio.

**Reproducción:** interrumpir después de que `poner()` complete la primera banda y antes de 329; o arrancar con una banda no-fábrica y completar la corrida.

**Gravedad:** crítica para continuidad entre campañas.

### R4. `barrido_total` todavía emite `PASA` con evidencia insuficiente

**Archivo/líneas:** `lab/barrido_total.py:679-711`, 722-741 y 797-808.

**Defecto y número falso:** el veredicto público histórico `veredicto` usa `pasa = dentro and t_banda is not None and t_estable is not None` (711). No requiere `quieto`, seis muestras distintas ni tramo temporal suficiente. Esas salvaguardas aparecen sólo en `nota`/`veredicto_estricto`. Un único LPo válido dentro de ventana, repetido por telemetría, puede dejar `t_estable` no nulo y producir `"veredicto": "PASA"`; el mismo registro puede traer `veredicto_estricto: FALLA` y `nota: null`.

**Reproducción:** serie con una sola medida LPo fresca y dentro de ±60 mV, seguida de fotos repetidas dentro de banda. `t_banda` se toma de la primera foto (602-603) y `t_estable` de la serie cruda (680-692); 711 queda verdadero sin cubrir `MUESTRAS_VALIDAS_MIN` ni `SPAN_QUIETUD_MIN_S`.

**Gravedad:** crítica. `experimento_semilla.py`/`banco.py` dependen de este núcleo.

### R5. Al faltar `edad`, la deduplicación degrada a “todo es nuevo”

**Archivo/líneas:** `lab/barrido_total.py:397-430`, especialmente 420-424.

**Defecto y número falso:** si no llega `edad` (o llega negativa), `_distintas` agrega la foto y reinicia `sello_prev`. Eso convierte cada publicación de una misma lectura en una medición independiente. Puede satisfacer `len(cola) >= 6`, simular 54 s de quietud con muestras copiadas y habilitar el corte temprano de `_visitar` (618-630).

**Reproducción:** omitir edad de LPo en una secuencia de fotos cada 2 s con idéntico valor y bandera válida. `_distintas` devuelve todas las fotos.

**Gravedad:** alta/crítica: una telemetría incompleta aumenta, en vez de reducir, la confianza.

### R6. La condición de contexto de semilla se etiqueta “asentada” sin medirla

**Archivo/líneas:** `lab/experimento_semilla.py:131-170`; la visita empieza en 353-362.

**Defecto y número falso:** `_preparar()` fija el par de contexto y sólo espera `espera_s`; no exige LPo fresco, válido, dentro de banda, quieto ni que el estado haya terminado de aprender. Luego se atribuyen diferencias de `t_estable`, origen o residuo a FRIO/DESDE_X1/DESDE_ALTA aunque el punto de partida puede ser transitorio.

**Reproducción:** usar contexto que tarde más de 60 s o aún aprenda al vencer `--espera-contexto` por defecto. La siguiente visita se etiqueta con `par_previo` sin evidencia de que esa condición se estableció.

**Gravedad:** alta. Puede producir una ventaja/desventaja aparente de la memoria que es historia de la planta.

### R7. La siembra se declara exitosa aunque ningún punto sea confirmado

**Archivo/líneas:** `lab/experimento_semilla.py:110-128`.

**Defecto y número falso:** `_sembrar()` incrementa `ok` tras cada `_cmd` y devuelve todos los puntos, sin ACK, lectura posterior ni comprobación de la tabla del firmware. Si un comando se pierde, se rechaza o se aplica parcialmente, la campaña llama a ese par “sembrado”; luego interpreta un arranque desde cero o una semilla vieja como ensayo de memoria.

**Reproducción:** hacer que el firmware no acepte un `ctl punto`. El host igualmente cuenta el punto y registra `sembrados N puntos`.

**Gravedad:** alta.

## Prioridad 2 — primera campaña de ruido

### R8. El volcado USB ignora el CRC que el firmware envía por cada lote

**Archivo/líneas:** `lab/experimento_ruido.py:101-107` y 122-126. Contraste de protocolo: `src/firmware/esp32/Nodo comunicación/slave/src/main.cpp:2364-2375` y 2382-2442.

**Defecto y número falso:** el firmware emite `#DUMP <seq> <600-hex> <crc8>`. El parser toma `partes[2]` y descarta `partes[3]`; `_guardar()` persiste los datos sin CRC. Un byte/hex alterado que siga siendo decodificable entra al RMS y espectro como ruido real. El analizador posterior tampoco tiene CRC guardado.

**Reproducción:** alterar un nibble del payload sin cambiar longitud, o proporcionar CRC incorrecto: `_volcar()` conserva el lote y la corrida termina `ok`. El firmware diseñó explícitamente ese CRC para detectar una línea cortada.

**Gravedad:** crítica: puede atribuir corrupción de USB a SD, RF o ganancia.

### R9. El experimento de ruido no prueba que el dump pertenezca a la captura pedida

**Archivo/líneas:** `lab/experimento_ruido.py:157-186`, especialmente 163-176; parser de cabecera en 101-103.

**Defecto y número falso:** tras `capwait`, el host no inspecciona `[LAB] ... done=1 ... fill=500/500`, no asocia una sesión y no valida `#DUMP_BEGIN`: `n`, `spb`, `bpp`, `fs`, `pga` ni `pgaout`. Sólo exige `len(lotes) >= 500`. Si `capwait` no inició/completó y quedó RAM de la corrida anterior, `dumpusb` puede devolver 500 lotes viejos y la herramienta los etiqueta con el par/condición nuevos. También acepta secuencias repetidas o con huecos si totalizan 500.

**Reproducción:** dejar una captura completa previa en RAM; hacer que `capwait` sea rechazado o expire; obtener un dump de 500 lotes. El chequeo 163-176 lo acepta y 178-185 lo etiqueta como nuevo.

**Gravedad:** crítica. Es un número correcto con dueño equivocado, fatal para BASE/SD/RF.

## Observaciones

- No se encontró en los cinco archivos otra invocación del vigilante shell con la negación de código de salida descrita. `banco.py:164-189` usa conteo Python. Su éxito textual (`'RESUELTO' in r and 'NO_RESUELTO' not in r`, línea 180) es frágil a texto citado, pero no convierte datos en PASA.
- `python -m py_compile` sobre los cinco módulos finalizó correctamente; no abre puertos serie.
- Este documento reporta defectos; no aplica cambios a las herramientas ni al nodo.

