[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    git submodule sync --recursive
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo sincronizar .gitmodules.' }

    git submodule update --init --recursive
    if ($LASTEXITCODE -ne 0) { throw 'No se pudieron inicializar los submódulos.' }

    New-Item -ItemType Directory -Path 'data\raw' -Force | Out-Null
    New-Item -ItemType Directory -Path 'data\processed' -Force | Out-Null

    Write-Host ''
    Write-Host 'Repositorios inicializados:'
    git submodule status --recursive
    Write-Host ''
    Write-Host 'Datos locales: data\raw y data\processed'
}
finally {
    Pop-Location
}
