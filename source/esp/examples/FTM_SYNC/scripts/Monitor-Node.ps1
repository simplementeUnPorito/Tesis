<#
.SYNOPSIS  Abre el monitor serie de un nodo (Ctrl+] para salir). Un nodo por terminal.
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
if (-not $Port) { $Port = $cfg.Ports[$Node] }
if (-not $Port -or $Port -match '\?') { throw "Sin puerto COM para $Node." }
$prof = (Get-FtmSyncProfiles).Nodes[$Node].Profile
$wr = Get-FtmSyncWorkRoot $cfg
$bld = Join-Path $wr "build_$prof"; $src = Join-Path $wr 'fts'
if ($DryRun) { Write-Host "[DryRun] python <IDF_PATH>\tools\idf.py -C $src -B $bld -p $Port monitor"; return }
$idfpy = Initialize-FtmSyncIdf $cfg
& python $idfpy -C $src -B $bld -p $Port monitor
