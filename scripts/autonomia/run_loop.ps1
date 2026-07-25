# Lanzador del loop de porteo.
#
# Dos razones para que esto sea un archivo y no un -Command:
#
# 1. Start-Process -ArgumentList se come las comillas: $env:PYTHONIOENCODING="utf-8"
#    llegaba como =utf-8 y PowerShell lo trataba como un comando inexistente.
# 2. Windows PowerShell 5.1 lee los .ps1 como ANSI (cp1252), no como UTF-8, salvo
#    que tengan BOM. Por eso este archivo es ASCII puro, SIN acentos ni simbolos:
#    con acentos y sin BOM, 5.1 rompe el parseo del script entero.
#    Si editas esto, no metas acentos.
#
# Uso:
#   powershell -ExecutionPolicy Bypass -File scripts\autonomia\run_loop.ps1
#   ... o en una ventana nueva:
#   Start-Process powershell -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-File','C:\Github\Tesis\scripts\autonomia\run_loop.ps1'

$ErrorActionPreference = 'Continue'

# La salida del loop SI tiene acentos. Esto es lo que evita que se vean roros.
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUNBUFFERED = '1'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

Set-Location -Path 'C:\Github\Tesis\scripts\autonomia'

$log = Join-Path (Get-Location) 'state\terminal.log'
Write-Host "=== loop de porteo; terminal.log -> $log ===" -ForegroundColor Cyan
Write-Host "    ver estado : python port_loop.py --status"
Write-Host "    frenar     : python port_loop.py --stop   (para al terminar la fase en curso)"
Write-Host ""

python port_loop.py 2>&1 | Tee-Object -FilePath $log -Append
$code = $LASTEXITCODE

Write-Host ""
if ($code -eq 0) {
    Write-Host "=== el loop termino bien (alcance completo o freno pedido) ===" -ForegroundColor Green
} elseif ($code -eq 1) {
    Write-Host "=== el loop PARO bloqueado: leer C:\Github\Tesis\DUDAS_LUNES.md ===" -ForegroundColor Yellow
} elseif ($code -eq 3) {
    Write-Host "=== no arranco: ya hay otro loop corriendo, o hay un freno puesto ===" -ForegroundColor Yellow
} else {
    Write-Host "=== el loop salio con codigo $code ===" -ForegroundColor Red
}
