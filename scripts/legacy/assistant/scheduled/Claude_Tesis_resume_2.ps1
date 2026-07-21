$ErrorActionPreference = "Continue"

$BaseDir = "C:\Github\Tesis"
$SessionId = "3b3f9e01-864c-4a2c-b0d3-ff29c1961670"
$TaskName = "Claude_Tesis_resume_2"
$Prompt = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String("Y29udGludWEgZGVzZGUgZG9uZGUgbG8gZGVqYW1vcywgY3VsbWluYSBsYXMgZ29hbHMsIHNlZ3VpIG1lam9yYW5kbyBlbCBwcm9ncmFtYSwgc2kgdGVybWluYXN0ZSBjb24gZWwgZXNjbGF2bywgY29udGludWEgY29uIGVsIG1hZXN0cm8="))
$MaxSeconds = 10800

$LogDir = Join-Path $BaseDir ".claude_scheduled_runs"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$OutLog = Join-Path $LogDir ("{0}_{1}.out.log" -f $TaskName, $stamp)
$ErrLog = Join-Path $LogDir ("{0}_{1}.err.log" -f $TaskName, $stamp)
$StatusLog = Join-Path $LogDir ("{0}_{1}.status.log" -f $TaskName, $stamp)

try {
    Add-Content -Path $StatusLog -Value ("[{0}] Iniciando tarea {1}" -f (Get-Date), $TaskName)

    Set-Location $BaseDir

    $claude = (Get-Command "claude" -ErrorAction Stop).Source

    $safeSession = $SessionId -replace '"', '\"'
    $safePrompt = $Prompt -replace '"', '\"'

    $argString = '--model fable --resume "{0}" "{1}"' -f $safeSession, $safePrompt

    $proc = Start-Process -FilePath $claude -ArgumentList $argString -PassThru -RedirectStandardOutput $OutLog -RedirectStandardError $ErrLog

    Add-Content -Path $StatusLog -Value ("[{0}] Claude iniciado. PID: {1}" -f (Get-Date), $proc.Id)

    if (-not $proc.WaitForExit($MaxSeconds * 1000)) {
        Add-Content -Path $StatusLog -Value ("[{0}] LÃ­mite de 3 horas alcanzado. Cerrando Claude y procesos hijos..." -f (Get-Date))
        & taskkill.exe /PID $proc.Id /T /F | Out-Null
    } else {
        Add-Content -Path $StatusLog -Value ("[{0}] Claude terminÃ³ solo. CÃ³digo de salida: {1}" -f (Get-Date), $proc.ExitCode)
    }
}
catch {
    Add-Content -Path $StatusLog -Value ("[{0}] ERROR: {1}" -f (Get-Date), $_.Exception.Message)
}
finally {
    Add-Content -Path $StatusLog -Value ("[{0}] Fin de tarea {1}" -f (Get-Date), $TaskName)

    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    } catch {}
}
