# `grafo` — consultar el grafo de conocimiento del repo

Envoltorio de PowerShell sobre [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp),
que indexa el repo en un grafo de nodos (funciones, clases, rutas, archivos) y
aristas (llamadas, imports, configuraciones). Sirve para responder preguntas de
arquitectura sin abrir cincuenta archivos a mano.

## Instalación

```powershell
# en el $PROFILE
. 'C:\Github\Tesis\scripts\grafo\grafo.ps1'
```

Requiere el binario en
`%LOCALAPPDATA%\Programs\codebase-memory-mcp\codebase-memory-mcp.exe`.
Si no está:

```powershell
$dst = "$env:LOCALAPPDATA\Programs\codebase-memory-mcp"
Invoke-WebRequest -Uri "https://github.com/DeusData/codebase-memory-mcp/releases/latest/download/codebase-memory-mcp-ui-windows-amd64.zip" -OutFile "$env:TEMP\cbm.zip"
Expand-Archive "$env:TEMP\cbm.zip" "$env:TEMP\cbm" -Force
Copy-Item (Get-ChildItem "$env:TEMP\cbm" -Recurse -Filter *.exe | Select-Object -First 1).FullName "$dst\codebase-memory-mcp.exe" -Force
```

## Comandos

| Comando | Qué hace |
|---|---|
| `grafo` | Abre la UI en `http://127.0.0.1:9749` |
| `grafo -Cable` | + la vista de protocolos PSoC/ESP/web |
| `grafo -Reindex` | Fuerza re-indexado y abre |
| `grafoSync` | Sincroniza el índice con el repo |
| `grafoSync -Force` | Re-indexa aunque no haya cambios |
| `grafoEstado` | Nodos, aristas, rama, HEAD |
| `grafoBuscar <patrón>` | Busca texto/regex en el código indexado |
| `grafoSimbolo <query>` | Busca símbolos (BM25 + filtros + semántico) |
| `grafoArq` | Capas, fronteras, clusters, rutas, hotspots |
| `grafoRuta <función>` | Traza llamadas desde/hacia una función |
| `grafoCodigo <símbolo>` | Código fuente de un símbolo |
| `grafoQuery <cypher>` | Cypher crudo |
| `grafoAdr` | Lee el ADR del proyecto |
| `grafoAdrGuardar <.md>` | Escribe un markdown como ADR |
| `grafoAyuda` | Lista todo lo anterior |

`Get-Help grafoRuta -Full` para el detalle de cada uno.

## Frescura del índice

**Todas las funciones verifican que el grafo refleje el estado actual del repo
antes de responder.** El mecanismo, en `_grafoEnsure`:

1. Si se chequeó hace menos de `$GrafoSyncThrottleMin` minutos (default 10), no
   hace nada — evita re-indexar en cada comando.
2. Si no, corre `detect_changes` (barato).
3. Si hay archivos cambiados y `$GrafoAutoSync` está en `$true` (default),
   re-indexa antes de responder. Si está en `$false`, sólo avisa.

Cualquier comando acepta `-NoSync` para saltear la verificación.

Variables configurables (en `grafo.ps1` o pisadas desde el `$PROFILE` después
del dot-source):

```powershell
$GrafoAutoSync        = $true        # re-indexar solo, o solo avisar
$GrafoSyncThrottleMin = 10           # minutos entre chequeos
$GrafoIndexMode       = 'moderate'   # full | moderate | fast
$GrafoPort            = 9749
```

`moderate` filtra archivos y calcula aristas de similitud/semánticas.
`full` incluye todo (más lento). `fast` omite similitud y semántica.

## Ejemplos

```powershell
# ¿Quién llama a qué, entre archivos de un sector?
grafoQuery "MATCH (a:Function)-[:CALLS]->(b:Function) WHERE a.file_path CONTAINS 'server' RETURN a.file_path AS src, b.file_path AS dst, count(*) AS n ORDER BY n DESC LIMIT 30"

# ¿Quién llama a una función concreta?
grafoQuery "MATCH (a:Function)-[:CALLS]->(b:Function) WHERE b.name = 'build_capture_rows' RETURN a.qualified_name AS llamador, a.file_path AS archivo"

# Buscar el manejo de ESP-NOW
grafoBuscar 'esp_now_send' -Mode full

# Búsqueda semántica: no hace falta acertar el nombre exacto
grafoSimbolo -Semantic @('espnow','paquete','envio')

# Funciones con bucles anidados profundos (candidatas a cuello de botella)
grafoQuery 'MATCH (f:Function) WHERE f.transitive_loop_depth >= 3 RETURN f.qualified_name, f.transitive_loop_depth ORDER BY f.transitive_loop_depth DESC LIMIT 20'

# Llamadas entre archivos de un sector
grafoQuery "MATCH (a:Function)-[:CALLS]->(b:Function) WHERE a.file_path CONTAINS 'interfaces' RETURN a.file_path AS src, b.file_path AS dst, count(*) AS n ORDER BY n DESC LIMIT 50"

# Arquitectura de un subárbol
grafoArq -Path src/interfaces/python -Aspects clusters,routes
```

## Trampas conocidas de este índice

Vale la pena tenerlas presentes: sin ellas se sacan conclusiones equivocadas.

**El dialecto de Cypher es parcial.** Los patrones anónimos con `WHERE` fallan
en silencio (devuelven cero filas). Hay que ponerle label a los nodos:

```powershell
# mal — devuelve 0 filas
grafoQuery "MATCH (a)-[:CALLS]->(b) WHERE a.file_path CONTAINS 'x' RETURN a.name"
# bien
grafoQuery "MATCH (a:Function)-[:CALLS]->(b:Function) WHERE a.file_path CONTAINS 'x' RETURN a.name"
```

**`trace_path` (o sea `grafoRuta`) devuelve vacío en la v0.9.0.** Probado con
nombre corto, con `qualified_name` completo, en ambas direcciones y con
funciones de C y de Python: siempre responde sólo los metadatos, sin `paths`.
No es el wrapper — el CLI directo hace lo mismo. Queda expuesto por si se
arregla en una versión futura; mientras tanto, usar `grafoQuery` sobre las
aristas `CALLS`, que sí funciona (ver ejemplos arriba).

**`Generated_Source/PSoC5` está indexado.** Es código de PSoC Creator, no diseño
propio, y domina cualquier ranking por fan-in: `CyEnterCriticalSection` y
`CyExitCriticalSection` salen primeros con 146 llamadas entrantes cada uno. Al
leer hotspots, descartar los símbolos `Cy*` y `USBUART_*`.

**Hay falsos positivos entre lenguajes.** El resolvedor cruza símbolos homónimos
(`main`, `setup`) y produce aristas imposibles: `calibration.c →
fix_dispersion_layer.py`, `slave/main.cpp → masw_adsurf.py`, `masw_analysis.py →
enlace.js`. Si una arista cruza lenguajes y no tiene sentido físico, no lo tiene.

**El grafo no ve el sistema real.** Las aristas `CALLS` sólo existen *dentro* de
cada binario. Un `.c` del PSoC no puede llamar a un `.js` del navegador. Los
enlaces que efectivamente forman el sistema —UART, ESP-NOW, WebSocket, HTTP— son
invisibles para el índice:

| Enlace | Archivos |
|---|---|
| UART + SYNC | `psoc/main.c` ↔ `slave/src/psoc_uart.cpp` |
| ESP-NOW | `slave/src/espnow_transport.h` ↔ `master/src/espnow_rx.h` |
| WebSocket `/ws` | `master/src/web_relay.h` ↔ `js/ws_client.js` |
| HTTP `/enlace/*` | `master/src/web_server.h` ↔ `js/enlace.js` |
| Transporte MATLAB | `master/src/matlab_transport.h` ↔ `interfaces/matlab/InterfazESP` |

`ingest_traces` devuelve *"Runtime edge creation from traces not yet
implemented"* en la v0.9.0, así que estas aristas no se pueden inyectar al
grafo. Viven en el ADR (`grafoAdr`, §4) y en `scripts/grafo/protocolos.html`
(`grafo -Cable`).

**172 archivos se saltean por timeout de parseo**: todos
`data/raw/**/combined/signals.csv`. No afectan al grafo de código.

## El ADR

`grafoAdr` devuelve el Architecture Decision Record del proyecto: la memoria
arquitectónica que persiste entre sesiones y que la UI muestra en su panel. Hoy
documenta la estructura de `src/`, las capas medidas, los módulos de facto por
detección de comunidades, los acoplamientos reales a nivel archivo, la capa de
protocolos y las restricciones operativas de hardware.

Para editarlo: `grafoAdr -Editar`, guardar, `grafoAdrGuardar <ruta>`.

