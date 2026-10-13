<#
.SYNOPSIS
  Compila el firmware FTM_SYNC (perfil ref y/o follower) con ESP-IDF v5.5.1 nativo.
.DESCRIPTION
  upstream/ (pristino) se copia a <WorkRoot>\fts; los builds van a <WorkRoot>\build_<perfil>.
  Requiere un ESP-IDF ya instalado (no instala nada). -DryRun solo imprime las ordenes.
.EXAMPLE
  .\Build-Firmware.ps1 -Profile all
#>
[CmdletBinding()]
param(
    [ValidateSet('ref', 'follower', 'all')][string]$Profile = 'all',
    [string]$ConfigPath,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'FtmSync.Common.ps1')

$cfg = Get-FtmSyncConfig -Path $ConfigPath
$chk = Test-FtmSyncConfigValues $cfg
$chk.Warnings | ForEach-Object { Write-Warning $_ }
if ($chk.Errors.Count) { throw ("Configuracion invalida:`n  " + ($chk.Errors -join "`n  ")) }

$names = if ($Profile -eq 'all') { @('ref', 'follower') } else { @($Profile) }
$wr = Get-FtmSyncWorkRoot $cfg
if ($DryRun) { $src = Join-Path $wr 'fts'; $idfpy = '<IDF_PATH>\tools\idf.py' }
else { $idfpy = Initialize-FtmSyncIdf $cfg; $src = Initialize-FtmSyncWorkspace $cfg }

$genDir = Join-Path $wr 'generated'
foreach ($n in $names) {
    $gen = Join-Path $genDir "$n.defaults"
    $list = Get-FtmSyncDefaultsList -ProfileName $n -Config $cfg -GeneratedPath $gen
    $bld = Join-Path $wr "build_$n"
    $tgt = (Get-FtmSyncProfiles).Profiles[$n].Target
    $argv = @($idfpy, '-C', $src, '-B', $bld, "-DIDF_TARGET=$tgt", "-DSDKCONFIG_DEFAULTS=$($list -join ';')", 'build')
    if ($DryRun) { Write-Host "[DryRun] python $($argv -join ' ')"; continue }
    New-Item -ItemType Directory -Force -Path $genDir | Out-Null
    [IO.File]::WriteAllText($gen, (New-FtmSyncGeneratedDefaults $cfg), [Text.UTF8Encoding]::new($false))
    # Si cambian los defaults hay que regenerar sdkconfig: IDF solo lee SDKCONFIG_DEFAULTS cuando no existe.
    $sdk = Join-Path $bld 'sdkconfig'
    if (Test-Path -LiteralPath $sdk) { Remove-Item -LiteralPath $sdk -Force }
    Write-Host "== Compilando perfil '$n' -> $bld"
    & python @argv
    if ($LASTEXITCODE -ne 0) { throw "idf.py build fallo para '$n' (codigo $LASTEXITCODE)" }
}
Write-Host 'Listo. Binarios en <WorkRoot>\build_ref y build_follower.'
