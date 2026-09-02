[CmdletBinding()]
param(
    [ValidateRange(3, 120)]
    [int]$IntervalMinutes = 12,
    [string]$ClaudeSession = 'c5b7b4a8-6ba3-4c1c-9af9-dd03effc73f6',
    [switch]$Once
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$memoryPath = Join-Path $repoRoot 'AUDIT_SESSION_MEMORY.md'
$stateDir = Join-Path $repoRoot 'tmp\audit-session'
$reviewPath = Join-Path $stateDir 'claude-latest.md'
$logPath = Join-Path $stateDir 'loop.log'

New-Item -ItemType Directory -Force -Path $stateDir | Out-Null

do {
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'
    Add-Content -LiteralPath $logPath -Value "[$stamp] Iniciando revisión read-only."

    $memory = Get-Content -Raw -LiteralPath $memoryPath
    $prompt = @"
Actúa como revisor independiente read-only de la auditoría de correctness de
C:\Github\Tesis. Lee la memoria incluida abajo y revisa únicamente el próximo
ítem P0 no clasificado. No edites archivos, no hagas commits y no cambies
algoritmos. Busca evidencia concreta: ubicación, reproducción mínima, expected
vs actual, derivación matemática cuando corresponda y tests existentes que
deban ejecutarse. Devuelve una nota Markdown breve para que otro agente la
verifique. No declares un bug sólo por inspección visual.

--- MEMORIA ---
$memory
"@

    $commonArguments = @(
        '--print',
        '--effort', 'high',
        '--permission-mode', 'plan',
        '--tools', 'Read,Grep,Glob,Bash',
        $prompt
    )
    $arguments = if ([string]::IsNullOrWhiteSpace($ClaudeSession)) {
        $commonArguments
    } else {
        @('--resume', $ClaudeSession) + $commonArguments
    }

    Push-Location $repoRoot
    try {
        $result = & claude @arguments 2>&1 | Out-String
        if ($LASTEXITCODE -ne 0 -or $result -match 'No deferred tool marker') {
            Add-Content -LiteralPath $logPath -Value "[$stamp] Resume no disponible; reintento con contexto Markdown."
            $result = & claude @commonArguments 2>&1 | Out-String
        }
        Set-Content -LiteralPath $reviewPath -Value "# Revisión Claude — $stamp`r`n`r`n$result"
        Add-Content -LiteralPath $logPath -Value "[$stamp] Revisión terminada."
    } catch {
        Add-Content -LiteralPath $logPath -Value "[$stamp] ERROR: $($_.Exception.Message)"
    } finally {
        Pop-Location
    }

    if (-not $Once) {
        Start-Sleep -Seconds ($IntervalMinutes * 60)
    }
} while (-not $Once)
