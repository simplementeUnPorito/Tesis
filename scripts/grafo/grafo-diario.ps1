<#
    Actualiza el indice codebase-memory como maximo una vez por dia.
    Se puede ejecutar manualmente o desde una tarea programada de Windows.
#>

$repo = 'C:\Github\Tesis'
$project = 'C-Github-Tesis'
$exe = "$env:LOCALAPPDATA\Programs\codebase-memory-mcp\codebase-memory-mcp.exe"
$stamp = Join-Path $env:LOCALAPPDATA 'codebase-memory-mcp\grafo-sync.stamp'

if (Test-Path $stamp) {
    $age = (New-TimeSpan -Start (Get-Item $stamp).LastWriteTime -End (Get-Date)).TotalHours
    if ($age -lt 24) { exit 0 }
}

if (-not (Test-Path $exe)) { exit 0 }

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) "grafo-diario-$([guid]::NewGuid().ToString('N')).json"
try {
    @{ project = $project } | ConvertTo-Json -Compress | Set-Content -Path $tmp -Encoding utf8
    $raw = & $exe cli detect_changes --args-file $tmp 2>$null
    $json = ($raw | Where-Object { $_ -match '^\s*[\{\[]' }) -join "`n" | ConvertFrom-Json
    if ([int]$json.changed_count -gt 0) {
        @{ repo_path = $repo; mode = 'moderate' } | ConvertTo-Json -Compress | Set-Content -Path $tmp -Encoding utf8
        & $exe cli index_repository --args-file $tmp 2>$null | Out-Null
    }
    New-Item -ItemType File -Path $stamp -Force | Out-Null
}
finally {
    Remove-Item $tmp -ErrorAction SilentlyContinue
}
