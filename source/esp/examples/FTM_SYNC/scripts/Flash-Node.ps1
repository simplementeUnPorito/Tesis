<#
.SYNOPSIS
  Flashea un nodo (REF, F1..F4) con la imagen de su perfil. Se niega si BoardPinoutConfirmed es $false.
.EXAMPLE
  .\Flash-Node.ps1 -Node REF
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidateSet('REF', 'F1', 'F2', 'F3', 'F4')][string]$Node,
    [string]$Port,
    [string]$ConfigPath,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'FtmSync.Common.ps1')

$cfg = Get-FtmSyncConfig -Path $ConfigPath
if (-not $cfg.BoardPinoutConfirmed) { throw 'BoardPinoutConfirmed=$false: confirmar el pinout de la placa (PulseGpio/LedGpio) y recien entonces ponerlo en $true.' }
$chk = Test-FtmSyncConfigValues $cfg
if ($chk.Errors.Count) { throw ("Configuracion invalida:`n  " + ($chk.Errors -join "`n  ")) }
if (-not $Port) { $Port = $cfg.Ports[$Node] }
if (-not $Port -or $Port -match '\?') { throw "Sin puerto COM para $Node (parametro -Port o Ports.$Node en la config)." }

$prof = (Get-FtmSyncProfiles).Nodes[$Node].Profile
$bld = Join-Path (Get-FtmSyncWorkRoot $cfg) "build_$prof"
$src = Join-Path (Get-FtmSyncWorkRoot $cfg) 'fts'
if ($DryRun) { Write-Host "[DryRun] python <IDF_PATH>\tools\idf.py -C $src -B $bld -p $Port flash   # nodo $Node, perfil $prof"; return }
if (-not (Test-Path -LiteralPath (Join-Path $bld 'sdkconfig'))) { throw "No hay build del perfil '$prof'. Correr Build-Firmware.ps1 primero." }
$idfpy = Initialize-FtmSyncIdf $cfg
Write-Host "== Flasheando $Node (perfil $prof) en $Port. Orden de arranque: REF primero, luego F1..F4 (<2 min despues)."
& python $idfpy -C $src -B $bld -p $Port flash
if ($LASTEXITCODE -ne 0) { throw "flash fallo ($LASTEXITCODE)" }
