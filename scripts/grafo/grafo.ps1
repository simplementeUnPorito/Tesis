<#
    grafo.ps1 — acceso al grafo de conocimiento del repo (codebase-memory-mcp)

    Uso:
        . C:\Github\Tesis\scripts\grafo\grafo.ps1     # dot-source
        grafo                                          # abre la UI

    Ver scripts\grafo\README.md para la documentacion completa.

    Todas las funciones verifican que el indice este al dia antes de responder
    (ver _grafoEnsure). Con -NoSync se saltea la verificacion.
#>

# ---------------------------------------------------------------- configuracion

# Carpeta de este script; se captura al cargar porque $PSScriptRoot no esta
# disponible dentro de las funciones una vez dot-sourceadas al scope global.
$GrafoDir     = $PSScriptRoot

$GrafoRepo    = 'C:\Github\Tesis'
$GrafoProject = 'C-Github-Tesis'
$GrafoPort    = 9749
$GrafoExe     = "$env:LOCALAPPDATA\Programs\codebase-memory-mcp\codebase-memory-mcp.exe"

# Re-indexar solo si detect_changes encuentra cambios. $false = solo avisar.
$GrafoAutoSync = $true
# No volver a chequear frescura si ya se chequeo hace menos de N minutos.
$GrafoSyncThrottleMin = 10
# Modo de indexado: full | moderate | fast
$GrafoIndexMode = 'moderate'

$GrafoStamp = Join-Path $env:LOCALAPPDATA 'codebase-memory-mcp\grafo-sync.stamp'

# ---------------------------------------------------------------------- helpers

function _grafoCli {
    <# Ejecuta una tool del MCP por CLI y devuelve el JSON ya parseado. #>
    param(
        [Parameter(Mandatory)][string]$Tool,
        [hashtable]$Args = @{}
    )

    if (-not (Test-Path $GrafoExe)) {
        Write-Host "No encuentro codebase-memory-mcp.exe en $GrafoExe" -ForegroundColor Red
        return $null
    }

    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) "grafo-$([guid]::NewGuid().ToString('N')).json"
    try {
        ($Args | ConvertTo-Json -Depth 6 -Compress) | Set-Content -Path $tmp -Encoding UTF8
        $raw = & $GrafoExe cli $Tool --args-file $tmp 2>$null
        $json = ($raw | Where-Object { $_ -match '^\s*[\{\[]' }) -join "`n"
        if (-not $json) { return $null }
        return $json | ConvertFrom-Json
    }
    catch {
        Write-Host "Fallo '$Tool': $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
    finally { Remove-Item $tmp -ErrorAction SilentlyContinue }
}

function _grafoEnsure {
    <#
        Garantiza que el grafo refleje el estado actual del repo.
        Estrategia: detect_changes (barato) y solo re-indexar si hay cambios.
        Se throttlea con un stamp para no chequear en cada comando.
    #>
    param([switch]$NoSync, [switch]$Force)

    if ($NoSync) { return }

    if (-not $Force -and (Test-Path $GrafoStamp)) {
        $last = (Get-Item $GrafoStamp).LastWriteTime
        if ((New-TimeSpan -Start $last -End (Get-Date)).TotalMinutes -lt $GrafoSyncThrottleMin) { return }
    }

    $chg = _grafoCli -Tool detect_changes -Args @{ project = $GrafoProject }
    if ($null -eq $chg) { return }

    $n = [int]$chg.changed_count
    if ($n -eq 0) {
        New-Item -ItemType File -Path $GrafoStamp -Force | Out-Null
        (Get-Item $GrafoStamp).LastWriteTime = Get-Date
        return
    }

    if (-not $GrafoAutoSync) {
        Write-Host "  ! el indice esta $n archivo(s) atras — corre 'grafoSync'" -ForegroundColor Yellow
        return
    }

    Write-Host "> $n archivo(s) cambiaron; re-indexando ($GrafoIndexMode)..." -ForegroundColor Cyan
    $r = _grafoCli -Tool index_repository -Args @{
        repo_path = $GrafoRepo
        mode      = $GrafoIndexMode
    }
    if ($r) {
        Write-Host "  indice al dia: $($r.nodes) nodos / $($r.edges) aristas" -ForegroundColor Green
        New-Item -ItemType File -Path $GrafoStamp -Force | Out-Null
        (Get-Item $GrafoStamp).LastWriteTime = Get-Date
    }
}

function _grafoOut {
    <# Imprime JSON legible, o crudo con -Raw. #>
    param($Obj, [switch]$Raw)
    if ($null -eq $Obj) { Write-Host "(sin resultados)" -ForegroundColor DarkGray; return }
    if ($Raw) { $Obj | ConvertTo-Json -Depth 12 } else { $Obj }
}

# ------------------------------------------------------------------- comandos

function grafo {
    <#
    .SYNOPSIS
        Abre la UI del grafo de arquitectura.
    .PARAMETER Cable
        Abre ademas scripts\grafo\protocolos.html: los enlaces UART / ESP-NOW /
        WebSocket / HTTP entre PSoC, ESP32 y navegador, que el grafo de llamadas
        no puede representar (viven en binarios distintos).
    .PARAMETER Reindex
        Fuerza un re-indexado completo antes de abrir.
    .PARAMETER NoSync
        No verifica frescura del indice.
    .EXAMPLE
        grafo
    .EXAMPLE
        grafo -Cable
    #>
    param([switch]$Cable, [switch]$Reindex, [switch]$NoSync, [int]$Port = $GrafoPort)

    if ($Reindex) {
        Write-Host "> Re-indexando $GrafoRepo ($GrafoIndexMode)..." -ForegroundColor Cyan
        $r = _grafoCli -Tool index_repository -Args @{ repo_path = $GrafoRepo; mode = $GrafoIndexMode }
        if ($r) { Write-Host "  $($r.nodes) nodos / $($r.edges) aristas" -ForegroundColor Green }
    } else {
        _grafoEnsure -NoSync:$NoSync
    }

    $url = "http://127.0.0.1:$Port"
    $up  = $false
    try { Invoke-WebRequest "$url/api/ui-config" -TimeoutSec 2 -UseBasicParsing | Out-Null; $up = $true } catch {}

    if (-not $up) {
        Write-Host "> Levantando la UI en $url ..." -ForegroundColor Yellow
        Start-Process -FilePath $GrafoExe -ArgumentList "--ui=true", "--port=$Port" -WindowStyle Hidden
        foreach ($i in 1..30) {
            Start-Sleep -Milliseconds 300
            try { Invoke-WebRequest "$url/api/ui-config" -TimeoutSec 2 -UseBasicParsing | Out-Null; $up = $true; break } catch {}
        }
    }
    if (-not $up) { Write-Host "La UI no respondio en $url" -ForegroundColor Red; return }

    Write-Host "  UI      $url" -ForegroundColor Green
    Start-Process $url

    if ($Cable) {
        $html = Join-Path $GrafoDir 'protocolos.html'
        if (Test-Path $html) {
            Write-Host "  Cable   $html" -ForegroundColor Green
            Start-Process $html
        } else {
            Write-Host "  (falta $html)" -ForegroundColor DarkGray
        }
    }
}

function grafoSync {
    <#
    .SYNOPSIS
        Sincroniza el grafo con el estado actual del repo.
    .PARAMETER Force
        Re-indexa aunque detect_changes no encuentre cambios.
    .PARAMETER Mode
        full | moderate | fast. Default: $GrafoIndexMode.
    #>
    param([switch]$Force, [string]$Mode = $GrafoIndexMode)

    if ($Force) {
        Write-Host "> Re-indexado forzado ($Mode)..." -ForegroundColor Cyan
        $r = _grafoCli -Tool index_repository -Args @{ repo_path = $GrafoRepo; mode = $Mode }
        if ($r) {
            Write-Host "  $($r.nodes) nodos / $($r.edges) aristas" -ForegroundColor Green
            if ($r.skipped_count) { Write-Host "  $($r.skipped_count) archivos salteados" -ForegroundColor DarkGray }
            New-Item -ItemType File -Path $GrafoStamp -Force | Out-Null
        }
        return
    }

    $chg = _grafoCli -Tool detect_changes -Args @{ project = $GrafoProject }
    if ($null -eq $chg) { return }
    Write-Host "  $($chg.changed_count) archivo(s) cambiados desde el ultimo indexado" -ForegroundColor Cyan
    if ($chg.changed_count -gt 0) {
        $chg.changed_files | Select-Object -First 20 | ForEach-Object { Write-Host "    $_" -ForegroundColor DarkGray }
        _grafoEnsure -Force
    } else {
        Write-Host "  el grafo esta al dia" -ForegroundColor Green
    }
}

function grafoEstado {
    <# .SYNOPSIS Estado del indice: nodos, aristas, rama, HEAD. #>
    param([switch]$NoSync)
    _grafoEnsure -NoSync:$NoSync
    _grafoOut (_grafoCli -Tool index_status -Args @{ project = $GrafoProject })
}

function grafoBuscar {
    <#
    .SYNOPSIS
        Busca texto/regex en el codigo indexado (search_code).
    .EXAMPLE
        grafoBuscar 'esp_now_send'
    .EXAMPLE
        grafoBuscar 'field_review_data' -FilePattern '*.py' -Mode full
    #>
    param(
        [Parameter(Mandatory, Position = 0)][string]$Pattern,
        [string]$FilePattern,
        [string]$PathFilter,
        [ValidateSet('compact', 'full', 'files')][string]$Mode = 'compact',
        [int]$Context,
        [int]$Limit = 15,
        [switch]$Raw,
        [switch]$NoSync
    )
    _grafoEnsure -NoSync:$NoSync
    $a = @{ project = $GrafoProject; pattern = $Pattern; mode = $Mode; limit = $Limit }
    if ($FilePattern) { $a.file_pattern = $FilePattern }
    if ($PathFilter)  { $a.path_filter  = $PathFilter }
    if ($Context)     { $a.context      = $Context }
    _grafoOut (_grafoCli -Tool search_code -Args $a) -Raw:$Raw
}

function grafoSimbolo {
    <#
    .SYNOPSIS
        Busca simbolos en el grafo (search_graph): BM25 + filtros + semantico.
    .EXAMPLE
        grafoSimbolo 'calibracion adc'
    .EXAMPLE
        grafoSimbolo -Label Function -FilePattern '*psoc*' -MinDegree 5
    .EXAMPLE
        grafoSimbolo -Semantic @('espnow','paquete','envio')
    #>
    param(
        [Parameter(Position = 0)][string]$Query,
        [string]$Label,
        [string]$NamePattern,
        [string]$FilePattern,
        [string[]]$Semantic,
        [int]$MinDegree,
        [int]$Limit = 30,
        [switch]$Raw,
        [switch]$NoSync
    )
    _grafoEnsure -NoSync:$NoSync
    $a = @{ project = $GrafoProject; limit = $Limit }
    if ($Query)       { $a.query          = $Query }
    if ($Label)       { $a.label          = $Label }
    if ($NamePattern) { $a.name_pattern   = $NamePattern }
    if ($FilePattern) { $a.file_pattern   = $FilePattern }
    if ($Semantic)    { $a.semantic_query = @($Semantic) }
    if ($MinDegree)   { $a.min_degree     = $MinDegree }
    _grafoOut (_grafoCli -Tool search_graph -Args $a) -Raw:$Raw
}

function grafoArq {
    <#
    .SYNOPSIS
        Vista de arquitectura: capas, fronteras, clusters, rutas, hotspots.
    .EXAMPLE
        grafoArq
    .EXAMPLE
        grafoArq -Path src/interfaces/python -Aspects clusters,routes
    #>
    param(
        [string]$Path,
        [string[]]$Aspects = @('overview'),
        [switch]$Raw,
        [switch]$NoSync
    )
    _grafoEnsure -NoSync:$NoSync
    $a = @{ project = $GrafoProject; aspects = @($Aspects) }
    if ($Path) { $a.path = $Path }
    _grafoOut (_grafoCli -Tool get_architecture -Args $a) -Raw:$Raw
}

function grafoRuta {
    <#
    .SYNOPSIS
        Traza el camino de llamadas desde/hacia una funcion (trace_path).
    .EXAMPLE
        grafoRuta uart_service
    .EXAMPLE
        grafoRuta build_capture_rows -Direction callers -Depth 4 -Risk
    #>
    param(
        [Parameter(Mandatory, Position = 0)][string]$Function,
        [ValidateSet('callers', 'callees', 'both')][string]$Direction = 'both',
        [int]$Depth = 3,
        [ValidateSet('calls', 'data_flow', 'cross_service')][string]$Mode = 'calls',
        [switch]$Risk,
        [switch]$IncludeTests,
        [switch]$Raw,
        [switch]$NoSync
    )
    _grafoEnsure -NoSync:$NoSync
    $a = @{
        project       = $GrafoProject
        function_name = $Function
        direction     = $Direction
        depth         = $Depth
        mode          = $Mode
    }
    if ($Risk)         { $a.risk_labels   = $true }
    if ($IncludeTests) { $a.include_tests = $true }
    _grafoOut (_grafoCli -Tool trace_path -Args $a) -Raw:$Raw
}

function grafoCodigo {
    <#
    .SYNOPSIS
        Devuelve el codigo fuente de un simbolo (get_code_snippet).
    .EXAMPLE
        grafoCodigo psoc_enter_sampling
    .EXAMPLE
        grafoCodigo build_capture_rows -Neighbors
    #>
    param(
        [Parameter(Mandatory, Position = 0)][string]$Name,
        [switch]$Neighbors,
        [switch]$Raw,
        [switch]$NoSync
    )
    _grafoEnsure -NoSync:$NoSync
    $a = @{ project = $GrafoProject; qualified_name = $Name }
    if ($Neighbors) { $a.include_neighbors = $true }
    _grafoOut (_grafoCli -Tool get_code_snippet -Args $a) -Raw:$Raw
}

function grafoQuery {
    <#
    .SYNOPSIS
        Cypher crudo contra el grafo (query_graph).
    .DESCRIPTION
        Ojo con el dialecto: los patrones anonimos con WHERE fallan.
        Poner label en los nodos — MATCH (a:Function)-[:CALLS]->(b:Function).
    .EXAMPLE
        grafoQuery 'MATCH (f:Function) WHERE f.transitive_loop_depth >= 3 RETURN f.qualified_name, f.transitive_loop_depth ORDER BY f.transitive_loop_depth DESC LIMIT 20'
    #>
    param(
        [Parameter(Mandatory, Position = 0)][string]$Cypher,
        [int]$MaxRows = 200,
        [switch]$Raw,
        [switch]$NoSync
    )
    _grafoEnsure -NoSync:$NoSync
    $r = _grafoCli -Tool query_graph -Args @{ project = $GrafoProject; query = $Cypher; max_rows = $MaxRows }
    if ($null -eq $r) { return }
    if ($Raw -or -not $r.columns) { return (_grafoOut $r -Raw:$Raw) }

    # filas -> objetos con las columnas como propiedades
    $cols = $r.columns
    $r.rows | ForEach-Object {
        $row = $_; $o = [ordered]@{}
        for ($i = 0; $i -lt $cols.Count; $i++) { $o[$cols[$i]] = $row[$i] }
        [PSCustomObject]$o
    }
}

function grafoAdr {
    <#
    .SYNOPSIS
        Lee (o abre para editar) el Architecture Decision Record del proyecto.
    .PARAMETER Sections
        Solo estas secciones.
    .PARAMETER Editar
        Vuelca el ADR a un .md temporal y lo abre en el editor por defecto.
    .EXAMPLE
        grafoAdr
    .EXAMPLE
        grafoAdr -Editar
    #>
    param([string[]]$Sections, [switch]$Editar)

    $a = @{ project = $GrafoProject; mode = 'get' }
    if ($Sections) { $a.sections = @($Sections); $a.mode = 'sections' }
    $r = _grafoCli -Tool manage_adr -Args $a
    if ($null -eq $r) { return }

    $txt = if ($r.content) { $r.content } else { $r | ConvertTo-Json -Depth 8 }
    if ($Editar) {
        $f = Join-Path ([System.IO.Path]::GetTempPath()) 'grafo-adr.md'
        Set-Content -Path $f -Value $txt -Encoding UTF8
        Write-Host "  $f" -ForegroundColor DarkGray
        Write-Host "  (guardalo y aplicalo con: grafoAdrGuardar $f)" -ForegroundColor DarkGray
        Start-Process $f
    } else { $txt }
}

function grafoAdrGuardar {
    <#
    .SYNOPSIS
        Escribe un archivo markdown como ADR del proyecto.
    .EXAMPLE
        grafoAdrGuardar C:\temp\grafo-adr.md
    #>
    param([Parameter(Mandatory, Position = 0)][string]$Path)
    if (-not (Test-Path $Path)) { Write-Host "No existe $Path" -ForegroundColor Red; return }
    $r = _grafoCli -Tool manage_adr -Args @{
        project = $GrafoProject
        mode    = 'update'
        content = (Get-Content -Raw $Path)
    }
    if ($r.status) { Write-Host "  ADR $($r.status)" -ForegroundColor Green }
}

function grafoAyuda {
    <# .SYNOPSIS Lista los comandos disponibles. #>
    @(
        [PSCustomObject]@{ Comando = 'grafo';           Que = 'abre la UI del grafo (-Cable para los protocolos)' }
        [PSCustomObject]@{ Comando = 'grafoSync';       Que = 'sincroniza el indice con el repo (-Force)' }
        [PSCustomObject]@{ Comando = 'grafoEstado';     Que = 'nodos, aristas, rama, HEAD' }
        [PSCustomObject]@{ Comando = 'grafoBuscar';     Que = 'busca texto/regex en el codigo' }
        [PSCustomObject]@{ Comando = 'grafoSimbolo';    Que = 'busca simbolos (BM25, filtros, semantico)' }
        [PSCustomObject]@{ Comando = 'grafoArq';        Que = 'capas, fronteras, clusters, rutas' }
        [PSCustomObject]@{ Comando = 'grafoRuta';       Que = 'traza llamadas desde/hacia una funcion' }
        [PSCustomObject]@{ Comando = 'grafoCodigo';     Que = 'codigo fuente de un simbolo' }
        [PSCustomObject]@{ Comando = 'grafoQuery';      Que = 'Cypher crudo' }
        [PSCustomObject]@{ Comando = 'grafoAdr';        Que = 'lee el ADR (-Editar)' }
        [PSCustomObject]@{ Comando = 'grafoAdrGuardar'; Que = 'escribe un .md como ADR' }
    ) | Format-Table -AutoSize
    Write-Host "Detalle de cada uno: Get-Help grafoRuta -Full" -ForegroundColor DarkGray
    Write-Host "Documentacion: scripts\grafo\README.md" -ForegroundColor DarkGray
}
