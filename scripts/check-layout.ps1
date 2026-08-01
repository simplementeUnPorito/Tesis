[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$expected = @(
    'src/firmware/psoc',
    'src/firmware/esp32',
    'src/interfaces/python',
    'src/interfaces/matlab',
    'src/calculos_modelados/matlab',
    'src/calculos_modelados/python',
    'PCBs',
    'docs',
    'data'
)

Push-Location $root
try {
    $registered = @(git config --file .gitmodules --get-regexp '^submodule\..*\.path$' |
        ForEach-Object { ($_ -split '\s+', 2)[1].Replace('\', '/') })

    $missing = @($expected | Where-Object { $_ -notin $registered })
    $unexpected = @($registered | Where-Object { $_ -notin $expected })
    if ($missing -or $unexpected) {
        throw "Layout inválido. Faltan: $($missing -join ', '); sobran: $($unexpected -join ', ')"
    }

    foreach ($path in $expected) {
        if (-not (Test-Path -LiteralPath $path)) {
            throw "Submódulo no inicializado: $path"
        }
    }

    git submodule status --recursive
    if ($LASTEXITCODE -ne 0) { throw 'git submodule status falló.' }
    Write-Host 'Layout modular válido.'
}
finally {
    Pop-Location
}
