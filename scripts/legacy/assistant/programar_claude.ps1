$ErrorActionPreference = "Stop"

$BaseDir = "C:\Github\Tesis"
$SessionId = "3b3f9e01-864c-4a2c-b0d3-ff29c1961670"
$RunRoot = Join-Path $BaseDir ".claude_scheduled_runs"

New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null

$Runs = @(
    [pscustomobject]@{
        TaskName = "Claude_Tesis_resume_1"
        Delay    = New-TimeSpan -Hours 3 -Minutes 27
        Prompt   = "continua desde donde lo dejamos, culmina las goals, buscale un uso si es posible al timer que dejamos huerfano. Verifica si codex no dejo alguna documentaciÃ³n de lo avanzado en su turno"
    },
    [pscustomobject]@{
        TaskName = "Claude_Tesis_resume_2"
        Delay    = New-TimeSpan -Hours 7 -Minutes 17
        Prompt   = "continua desde donde lo dejamos, culmina las goals, segui mejorando el programa, si terminaste con el esclavo, continua con el maestro"
    }
)

function New-ClaudeWorker {
    param (
        [string]$TaskName,
        [string]$Prompt
    )

    $scriptPath = Join-Path $RunRoot "$TaskName.ps1"
    $prompt64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Prompt))

    $content = @"
`$ErrorActionPreference = "Continue"

`$BaseDir = "$BaseDir"
`$SessionId = "$SessionId"
`$TaskName = "$TaskName"
`$Prompt = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("$prompt64"))
`$MaxSeconds = 10800

`$LogDir = Join-Path `$BaseDir ".claude_scheduled_runs"
New-Item -ItemType Directory -Path `$LogDir -Force | Out-Null

`$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
`$OutLog = Join-Path `$LogDir ("{0}_{1}.out.log" -f `$TaskName, `$stamp)
`$ErrLog = Join-Path `$LogDir ("{0}_{1}.err.log" -f `$TaskName, `$stamp)
`$StatusLog = Join-Path `$LogDir ("{0}_{1}.status.log" -f `$TaskName, `$stamp)

try {
    Add-Content -Path `$StatusLog -Value ("[{0}] Iniciando tarea {1}" -f (Get-Date), `$TaskName)

    Set-Location `$BaseDir

    `$claude = (Get-Command "claude" -ErrorAction Stop).Source

    `$safeSession = `$SessionId -replace '"', '\"'
    `$safePrompt = `$Prompt -replace '"', '\"'

    `$argString = "--model fable --resume `"`$safeSession`" `"`$safePrompt`""

    `$proc = Start-Process `
        -FilePath `$claude `
        -ArgumentList `$argString `
        -PassThru `
        -RedirectStandardOutput `$OutLog `
        -RedirectStandardError `$ErrLog

    Add-Content -Path `$StatusLog -Value ("[{0}] Claude iniciado. PID: {1}" -f (Get-Date), `$proc.Id)

    if (-not `$proc.WaitForExit(`$MaxSeconds * 1000)) {
        Add-Content -Path `$StatusLog -Value ("[{0}] LÃ­mite de 3 horas alcanzado. Cerrando Claude y procesos hijos..." -f (Get-Date))
        & taskkill.exe /PID `$proc.Id /T /F | Out-Null
    } else {
        Add-Content -Path `$StatusLog -Value ("[{0}] Claude terminÃ³ solo. CÃ³digo de salida: {1}" -f (Get-Date), `$proc.ExitCode)
    }
}
catch {
    Add-Content -Path `$StatusLog -Value ("[{0}] ERROR: {1}" -f (Get-Date), `$_.Exception.Message)
}
finally {
    Add-Content -Path `$StatusLog -Value ("[{0}] Fin de tarea {1}" -f (Get-Date), `$TaskName)

    try {
        Unregister-ScheduledTask -TaskName `$TaskName -Confirm:`$false -ErrorAction SilentlyContinue
    } catch {}
}
"@

    Set-Content -Path $scriptPath -Value $content -Encoding UTF8
    return $scriptPath
}

$UserId = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

foreach ($run in $Runs) {
    $workerPath = New-ClaudeWorker -TaskName $run.TaskName -Prompt $run.Prompt
    $startAt = (Get-Date).Add($run.Delay)

    $action = New-ScheduledTaskAction `
        -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$workerPath`""

    $trigger = New-ScheduledTaskTrigger -Once -At $startAt

    $settings = New-ScheduledTaskSettingsSet `
        -ExecutionTimeLimit (New-TimeSpan -Hours 3) `
        -WakeToRun `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries

    $principal = New-ScheduledTaskPrincipal `
        -UserId $UserId `
        -LogonType Interactive `
        -RunLevel Limited

    Register-ScheduledTask `
        -TaskName $run.TaskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Principal $principal `
        -Force | Out-Null

    Write-Host "Programado $($run.TaskName) para: $startAt"
}

Write-Host ""
Write-Host "Listo. Logs en: $RunRoot"
Write-Host "Cada ejecuciÃ³n se corta automÃ¡ticamente despuÃ©s de 3 horas."
