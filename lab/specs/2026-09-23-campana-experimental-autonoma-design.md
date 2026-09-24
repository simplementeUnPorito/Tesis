# Diseño de campaña experimental autónoma y acumulativa

Fecha: 2026-09-23

Estado: propuesta para revisión

Banco: ESP32 en COM8 y PSoC 5LP conectado a la placa soldada

## 1. Objetivo

Convertir el barrido actual en una campaña experimental autónoma que obtenga
evidencia reutilizable para los trabajos futuros de la tesis, sin cambiar la
asignación de pines y sin depender de que un operador permanezca frente al
banco.

La campaña debe:

- ejecutar experimentos en un orden explícito y reproducible;
- reservar la noche para experimentos largos o que requieren continuidad;
- desde las 07:00 ejecutar solamente unidades breves y reanudables;
- permitir observaciones continuas y reinicios controlados, según el objetivo;
- persistir datos a medida que se producen;
- detenerse en cualquier momento sin perder los datos ya adquiridos;
- reanudarse sin duplicar visitas terminadas;
- separar la adquisición del análisis, de modo que analizar nunca abra COM8;
- respetar un presupuesto predeterminado de 3 GiB sin borrar resultados.

La zona horaria de planificación será `America/Asuncion`. Las marcas de tiempo
guardarán tanto hora local con desplazamiento como UTC.

## 2. Alcance respecto de los trabajos futuros

### 2.1 Evidencia obtenible con el banco actual

La campaña puede caracterizar directamente:

1. offset residual por par PGA/PGAout;
2. variación temporal del offset y de los códigos IDAC;
3. tiempo de convergencia, estabilidad y permanencia dentro de banda;
4. margen dinámico y frecuencia de saturación de cada tap;
5. repetibilidad entre vueltas;
6. dependencia del orden de recorrido e histéresis;
7. persistencia de la calibración y recuperación después de un reinicio del
   PSoC ordenado por el ESP32;
8. diferencias entre arranque en caliente y estado estabilizado.

Estos resultados responden al trabajo futuro que propone caracterizar el
offset residual, su variación temporal y el margen dinámico de cada ganancia.

### 2.2 Evidencia que requiere otro montaje

La campaña no declarará resueltos los siguientes puntos:

- inicio efectivo y deriva relativa entre varios ADC;
- efecto de un excitador con mayor energía por debajo de 10 Hz;
- adquisición simultánea con más nodos GEO;
- validación MASW simultánea en campo.

Esos puntos se registrarán como `BLOQUEADO_POR_HARDWARE`, con la evidencia que
falta. Las curvas de dispersión y la inversión podrán procesarse fuera de línea
con datos de campo existentes, pero no se confundirán con una nueva validación
del banco electrónico.

## 3. Arquitectura

Se añadirá un orquestador único sobre las primitivas ya verificadas de
`barrido_total.py`. El proceso tendrá cinco componentes con responsabilidades
separadas:

1. **Catálogo de experimentos:** declara requisitos, duración máxima, política
   de reinicio, orden y criterio de terminación.
2. **Planificador horario:** decide qué experimento puede comenzar según la
   hora local y el tiempo disponible antes de las 07:00.
3. **Ejecutor:** controla exclusivamente COM8 y emite eventos; sólo utiliza una
   lista permitida de comandos existentes.
4. **Diario y checkpoint:** persiste muestras, visitas y posición de campaña.
5. **Analizador:** lee un snapshot del diario y produce informes sin abrir el
   puerto serie.

Sólo puede existir un ejecutor dueño de COM8. El supervisor reiniciará fallos
transitorios y reanudará desde el diario. Codex actuará únicamente frente a una
alerta no resoluble por reglas deterministas.

## 4. Orden de experimentos

### 4.1 Fase nocturna: antes de las 07:00

Los experimentos se ejecutarán en este orden:

1. **N0 — completar incertidumbre heredada:** repetir los pares que estén
   `APRENDIENDO`, `INVALIDA` o tengan menos observaciones que el mínimo.
2. **N1 — deriva cálida sin reinicio:** mantener continuidad eléctrica y
   observar durante bloques largos el control `x1/x1`, los cinco pares estables
   de mayor amplitud y dos pares próximos al límite estable.
3. **N2 — efecto del recorrido sin reinicio:** ejecutar órdenes ascendente,
   descendente y serpenteante. Cada bloque registra el estado inicial para
   separar efecto de ganancia y efecto de historia.
4. **N3 — persistencia con reinicio:** tomar una referencia, ordenar
   `psocreset` mediante el ESP32 por GPIO19, esperar el arranque, cebar la
   adquisición en condición segura y repetir el conjunto representativo.
5. **N4 — endurance de recuperación:** repetir ciclos N3 con límites de fallos
   consecutivos y backoff. Cada ciclo completo es una unidad independiente.

La selección de pares representativos se congela al iniciar un bloque. Incluye
siempre `x1/x1`; los demás se seleccionan del diario anterior por tasa de PASA,
amplitud, variabilidad y cercanía al límite. Nunca se cambia la selección a
mitad de un bloque para favorecer el resultado.

Un experimento nocturno sólo comenzará si su duración máxima cabe antes de las
07:00, dejando un margen configurable de diez minutos. Si no cabe, el
planificador pasa anticipadamente a la fase diurna.

### 4.2 Fase diurna: desde las 07:00

Se ejecutarán unidades cortas y cancelables:

1. **D0 — visitas prioritarias:** pares con menos datos, veredictos discordantes
   o alta dispersión.
2. **D1 — ronda balanceada:** una visita por par, con checkpoint en cada
   muestra y sin prórrogas nocturnas.
3. **D2 — controles intercalados:** `x1/x1` entre grupos para medir deriva del
   banco y distinguirla de la dependencia con ganancia.
4. **D3 — análisis incremental:** regenerar resúmenes desde un snapshot; no
   ocupa COM8 y puede interrumpirse y repetirse libremente.

Después de las 07:00 no se iniciarán reinicios de endurance ni bloques cuya
unidad atómica exceda el límite diurno configurado. Una visita que se detenga
se conservará como censurada, no se convertirá artificialmente en FALLA.

## 5. Persistencia y modelo de datos

Cada campaña tendrá un directorio independiente:

```text
campana_<fecha>/
  campaign.json
  events.jsonl
  visits.jsonl
  state.json
  .run/
    health.json
    alert.json
    STOP
  analysis/
    resumen.csv
    INFORME.md
```

`campaign.json` será inmutable e incluirá versión de esquema, configuración,
commit de Git, firmware declarado, mapa de pines bloqueado, zona horaria,
presupuesto de disco y semilla de los órdenes reproducibles.

`events.jsonl` será append-only. Cada línea completa representará una muestra o
evento y tendrá, como mínimo:

- `campaign_id`, `experiment_id`, `block_id`, `visit_id` y `event_id`;
- timestamps local, UTC y monotónico;
- fase, tipo de experimento, orden y época de reinicio;
- PGA/PGAout pedidos y confirmados;
- estado, banda, taps, validez, edades e IDAC;
- causa de reinicio, alerta, parada o transición, cuando corresponda.

`visits.jsonl` contendrá una fila resumida al cerrar cada visita. Su estado será
`COMPLETE`, `INTERRUPTED`, `INVALID` o `ERROR`. Una visita interrumpida conserva
su serie y se trata como observación censurada; no cuenta como PASA ni FALLA.

`state.json` se escribirá de manera atómica y será sólo una aceleración para
reanudar. Si falta o está corrupto, debe poder reconstruirse desde los diarios.
Una última línea JSONL incompleta por corte de energía se ignora sin alterar las
líneas previas.

El tamaño total se vigilará antes de cada visita. Al 90 % del presupuesto se
emitirá advertencia; al 95 % no comenzarán capturas nuevas, se generará el
análisis y se solicitará intervención. No se borrarán ni truncarán datos.

## 6. Parada y reanudación

Habrá tres mecanismos equivalentes:

- comando de consola `stop`;
- archivo `.run/STOP`;
- señales `SIGINT` o `SIGTERM`.

El ejecutor comprobará la solicitud al menos una vez por intervalo de muestreo.
Al detenerse:

1. deja de iniciar comandos nuevos;
2. completa la escritura de la muestra ya recibida;
3. agrega un evento `STOP_REQUESTED`;
4. cierra la visita como `INTERRUPTED` si estaba abierta;
5. hace `flush` y `fsync` de ambos diarios;
6. actualiza `state.json` y `health.json`;
7. libera COM8.

Al reanudar, las visitas `COMPLETE` no se repiten salvo que el catálogo pida
otra repetición. Una visita `INTERRUPTED` puede continuarse como una nueva
visita enlazada mediante `resumes_visit_id`; nunca se sobrescribe la anterior.

La parada por el usuario es un resultado normal (`stopped_by_operator`) y no
consume el presupuesto de reinicios del supervisor.

## 7. Seguridad del banco

- El mapa GPIO19, GPIO26 y GPIO27 queda fijado y registrado en
  `campaign.json`; el orquestador no contiene operaciones para reasignarlo.
- El único reinicio de PSoC permitido es el comando existente `psocreset` del
  ESP32 por GPIO19.
- No se flashea firmware durante una campaña.
- Antes de un bloque con reinicio se verifica comunicación, telemetría y una
  condición segura de adquisición.
- Los comandos serie estarán en una lista permitida; cualquier comando ajeno
  al catálogo aborta el bloque y crea una alerta.
- Los archivos de campañas anteriores son de sólo lectura para el ejecutor.

## 8. Análisis acumulativo

El análisis podrá ejecutarse mientras la adquisición continúa, leyendo hasta
el último salto de línea completo de un snapshot. Producirá:

- cantidad de observaciones por par y condición;
- tasa de PASA con denominador explícito;
- mediana, percentiles y peor tiempo de estabilización;
- offset final, pico a pico y pendiente temporal en mV/h;
- variación de cada IDAC;
- comparación pareada antes/después de reinicio;
- diferencias entre órdenes ascendente, descendente y serpenteante;
- tasa de saturación por tap y margen disponible;
- cantidad de observaciones `INTERRUPTED`, sin tratarlas como fallos;
- trazabilidad desde cada resumen hasta sus `visit_id` y muestras.

Las recomendaciones requerirán un mínimo configurable de visitas completas y
separarán evidencia exploratoria de evidencia confirmatoria. El informe no
afirmará sincronización multicanal ni desempeño MASW sin el montaje requerido.

## 9. Interfaz operativa prevista

La interfaz será la misma en Windows y Linux:

```text
python lab/campana_experimental.py run --port COM8 --output <directorio>
python lab/campana_experimental.py status --output <directorio>
python lab/campana_experimental.py stop --output <directorio>
python lab/campana_experimental.py resume --port COM8 --output <directorio>
python lab/campana_experimental.py analyze --output <directorio>
```

`run` y `resume` usarán por defecto el horario descrito y un límite de 3 GiB.
El README incluirá un bloque para copiar y pegar, además de instrucciones para
Windows y Linux, comprobación del puerto y significado de cada estado.

## 10. Verificación

El desarrollo seguirá TDD e incluirá:

### Pruebas unitarias

- selección nocturna y diurna exactamente antes, durante y después de las
  07:00;
- rechazo de un experimento largo que no cabe en la ventana nocturna;
- selección reproducible de pares y órdenes;
- escritura append-only y recuperación ante última línea truncada;
- reconstrucción de `state.json` desde los diarios;
- deduplicación de visitas completas;
- conservación y enlace de visitas interrumpidas;
- límite de 3 GiB y umbrales de advertencia/parada;
- imposibilidad de emitir comandos o pines fuera de la lista permitida.

### Pruebas de integración sin hardware

- puerto serie simulado con telemetría normal, tardía, inválida y ausente;
- parada durante espera, captura y análisis;
- caída del proceso entre append y checkpoint;
- reanudación después de error transitorio;
- reinicio controlado con secuencia y backoff correctos;
- análisis concurrente que no abre el puerto.

### Prueba de humo con hardware

En una campaña temporal: telemetría, visita `x1/x1`, parada solicitada,
liberación de COM8 y reanudación. Luego se habilitará la campaña real. Esta
prueba no cambiará pines ni flasheará firmware.

## 11. Migración de la campaña en curso

El barrido actual no se interrumpirá hasta que el nuevo orquestador y sus
pruebas estén listos. Para migrar:

1. solicitar parada segura en un límite de muestra;
2. conservar intacto `resultados.jsonl` y sus informes;
3. importar cada visita histórica con identificadores deterministas;
4. validar que los conteos y veredictos coincidan;
5. ejecutar la prueba de humo;
6. iniciar la nueva campaña desde el próximo experimento pendiente.

La importación será idempotente. El archivo histórico seguirá siendo la fuente
original y no se modificará.

## 12. Criterios de aceptación

La implementación se considerará lista cuando:

1. todas las pruebas unitarias y de integración pasen;
2. la prueba de humo demuestre parada y reanudación sin perder una muestra ya
   escrita;
3. el analizador reproduzca los conteos de la campaña histórica;
4. ningún cambio modifique el mapa de pines;
5. el proceso nocturno cambie automáticamente a trabajo diurno desde las
   07:00;
6. el usuario pueda iniciar, consultar, detener, reanudar y analizar mediante
   los cinco comandos documentados;
7. el supervisor permanezca silencioso durante operación sana y alerte sólo
   cuando agote recuperaciones deterministas.
