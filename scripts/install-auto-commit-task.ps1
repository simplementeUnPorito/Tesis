[CmdletBinding()]
param(
    [string]$TaskName = "Tesis - Auto-commit de submodulos",

    [ValidateRange(1, 168)]
    [int]$CheckEveryHours = 1,

    [ValidateRange(1, 8760)]
    [int]$HoursWithoutCommit = 24
)

$ErrorActionPreference = "Stop"
$workerScript = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot `
    "auto-commit-submodules.ps1")).Path
$repositoryRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path

$powerShell = Get-Command pwsh.exe -ErrorAction SilentlyContinue
if ($null -eq $powerShell) {
    $powerShell = Get-Command powershell.exe -ErrorAction Stop
}

$actionArguments = '-NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "{0}" -HoursWithoutCommit {1}' -f `
    $workerScript, $HoursWithoutCommit
$action = New-ScheduledTaskAction -Execute $powerShell.Source `
    -Argument $actionArguments -WorkingDirectory $repositoryRoot

# La comprobacion es frecuente, pero solo actua cuando pasaron 24 horas sin
# commits. La duracion de diez anos evita el limite de repeticion de Task
# Scheduler manteniendo la tarea facil de inspeccionar y renovar.
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) `
    -RepetitionInterval (New-TimeSpan -Hours $CheckEveryHours) `
    -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
$principal = New-ScheduledTaskPrincipal `
    -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) `
    -LogonType Interactive -RunLevel Limited

$task = New-ScheduledTask -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal `
    -Description "Crea un commit en cada submodulo modificado tras 24 horas sin commits y actualiza sus punteros en Tesis."
Register-ScheduledTask -TaskName $TaskName -InputObject $task -Force | Out-Null

Write-Output "Tarea instalada: $TaskName"
Write-Output "Revision: cada $CheckEveryHours hora(s)"
Write-Output "Umbral: $HoursWithoutCommit horas sin commit"
Write-Output "Script: $workerScript"
