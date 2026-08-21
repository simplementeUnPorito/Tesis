[CmdletBinding()]
param(
    [string]$TaskName = "Tesis - Auto-commit de submodulos",

    [ValidateRange(1, 168)]
    [int]$CheckEveryHours = 1,

    [ValidateRange(1, 8760)]
    [int]$HoursWithoutCommit = 24
)

$ErrorActionPreference = "Stop"
$launcherScript = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot `
    "run-auto-commit-hidden.vbs")).Path
$repositoryRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path

# La tarea corre en la sesion interactiva porque LogonType S4U (sesion 0, sin
# ventana) exige permisos de administrador. El envoltorio .vbs lanza pwsh con la
# ventana oculta, espera y propaga su codigo de salida, de modo que la tarea
# nunca muestra una consola pero conserva historial, limite de tiempo y control
# de instancias.
$wscript = Get-Command wscript.exe -ErrorAction Stop
$actionArguments = '//B //Nologo "{0}" {1}' -f $launcherScript, $HoursWithoutCommit
$action = New-ScheduledTaskAction -Execute $wscript.Source `
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
Write-Output "Lanzador: $launcherScript (ventana oculta)"
