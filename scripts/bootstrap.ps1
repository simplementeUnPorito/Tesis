[CmdletBinding()]
param(
    [string]$StoreRoot = $env:GITHUB_LFS_ROOT,
    [switch]$HydrateLfs
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    git submodule sync --recursive
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo sincronizar .gitmodules.' }

    $previousSkipSmudge = $env:GIT_LFS_SKIP_SMUDGE
    $env:GIT_LFS_SKIP_SMUDGE = '1'
    try {
        git submodule update --init --recursive
        if ($LASTEXITCODE -ne 0) { throw 'No se pudieron inicializar los submódulos.' }
    }
    finally {
        if ($null -eq $previousSkipSmudge) {
            Remove-Item Env:GIT_LFS_SKIP_SMUDGE -ErrorAction SilentlyContinue
        } else {
            $env:GIT_LFS_SKIP_SMUDGE = $previousSkipSmudge
        }
    }

    if ([string]::IsNullOrWhiteSpace($StoreRoot)) {
        $defaultStore = 'C:\Users\elias\OneDrive\Github-LFS'
        if (Test-Path -LiteralPath $defaultStore) {
            $StoreRoot = $defaultStore
        }
    }

    $lfsRepos = @(
        'software/python',
        'modelado/matlab',
        'docs',
        'investigacion',
        'data'
    )

    if ([string]::IsNullOrWhiteSpace($StoreRoot) -or -not (Test-Path -LiteralPath $StoreRoot)) {
        Write-Warning 'No se encontró Github-LFS. Los archivos grandes permanecerán como punteros.'
    } else {
        foreach ($path in $lfsRepos) {
            $configurator = Join-Path $root (Join-Path $path 'scripts\configure-lfs-folderstore.ps1')
            & $configurator -StoreRoot $StoreRoot
            if ($LASTEXITCODE -ne 0) { throw "No se pudo configurar LFS para $path." }

            if ($HydrateLfs) {
                git -C $path lfs checkout
                if ($LASTEXITCODE -ne 0) { throw "No se pudieron hidratar los objetos de $path." }
            }
        }
    }

    Write-Host ''
    Write-Host 'Repositorios inicializados:'
    git submodule status --recursive
    Write-Host ''
    if ($HydrateLfs) {
        Write-Host 'Objetos LFS hidratados desde el folderstore.'
    } else {
        Write-Host 'Objetos LFS configurados y conservados como punteros.'
    }
}
finally {
    Pop-Location
}
