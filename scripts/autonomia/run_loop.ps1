# Lanzador del loop de porteo.
#
# Existe porque pasar el comando por -ArgumentList a Start-Process se come las
# comillas: `$env:PYTHONIOENCODING="utf-8"` llegaba como `=utf-8` y PowerShell lo
# interpretaba como un comando inexistente. Con un archivo .ps1 no hay quoting de
# por medio.
#
# Uso:
#   powershell -ExecutionPolicy Bypass -File scripts\autonomia\run_loop.ps1
#   ... o en una ventana nueva:
#   Start-Process powershell -ArgumentList '-NoExit','-ExecutionPolicy','Bypass','-File','C:\Github\Tesis\scripts\autonomia\run_loop.ps1'

$ErrorActionPreference = 'Continue'

# Sin esto los acentos y el separador '·' de los mensajes de la CLI salen como
# basura en la consola (cp850/cp1252) y el log queda ilegible.
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUNBUFFERED = '1'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Set-Location -Path 'C:\Github\Tesis\scripts\autonomia'

$log = Join-Path (Get-Location) 'state\terminal.log'
Write-Host "=== loop de porteo; terminal.log -> $log ===" -ForegroundColor Cyan
Write-Host "    ver estado : python port_loop.py --status"
Write-Host "    frenar     : python port_loop.py --stop   (para al terminar la fase en curso)"
Write-Host ""

python port_loop.py 2>&1 | Tee-Object -FilePath $log -Append
$code = $LASTEXITCODE

Write-Host ""
switch ($code) {
    0 { Write-Host "=== el loop terminó bien (alcance completo o freno pedido) ===" -ForegroundColor Green }
    1 { Write-Host "=== el loop PARÓ bloqueado: leer C:\Github\Tesis\DUDAS_LUNES.md ===" -ForegroundColor Yellow }
    3 { Write-Host "=== no arrancó: ya hay otro loop corriendo, o hay un freno puesto ===" -ForegroundColor Yellow }
    default { Write-Host "=== el loop salió con código $code ===" -ForegroundColor Red }
}
