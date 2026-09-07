$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonDir = Join-Path $repo 'src\interfaces\python'

Set-Location -LiteralPath $pythonDir
python -m testbench.gui --port COM8 --manual --connect --field

if ($LASTEXITCODE -ne 0) {
    Write-Host ''
    Write-Host 'La interfaz terminó con error. Presioná Enter para cerrar.' -ForegroundColor Red
    Read-Host
}
