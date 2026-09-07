param(
    [string]$Registro = "C:\Github\Tesis\lab\planta\deriva_20260906_0954.json",
    [double]$Horas = 24.0
)

$ErrorActionPreference = "Stop"
$registroEsperado = [IO.Path]::GetFullPath("C:\Github\Tesis\lab\planta\deriva_20260906_0954.json")
$registroResuelto = [IO.Path]::GetFullPath($Registro)
if ($registroResuelto -ne $registroEsperado) {
    throw "Registro inesperado: $registroResuelto"
}

$bitacora = "C:\Github\Tesis\lab\planta\finalizar_deriva_24h.log"
while ($true) {
    try {
        $datos = Get-Content -LiteralPath $registroResuelto -Raw | ConvertFrom-Json
        if ($datos.muestras.Count -gt 1) {
            $primera = Get-Date $datos.muestras[0].t
            $ultima = Get-Date $datos.muestras[-1].t
            $duracion = ($ultima - $primera).TotalHours
            if ($duracion -ge $Horas) {
                # La version que esta corriendo es anterior al corte automatico.
                # Se detiene solo el arbol cuyo comando exacto es exp_deriva.py.
                $procesos = Get-CimInstance Win32_Process | Where-Object {
                    $_.Name -eq "python.exe" -and $_.CommandLine -match '(^|\s)exp_deriva\.py(\s|$)'
                }
                foreach ($proceso in $procesos) {
                    Stop-Process -Id $proceso.ProcessId -Force -ErrorAction SilentlyContinue
                }
                "$(Get-Date -Format o) corte al cumplir $([math]::Round($duracion, 3)) h; muestras=$($datos.muestras.Count); procesos=$($procesos.ProcessId -join ',')" |
                    Out-File -LiteralPath $bitacora -Encoding utf8
                break
            }
        }
    }
    catch {
        # La adquisicion anterior reescribe el JSON en cada muestra. Si justo
        # se lo lee a mitad de escritura, se reintenta sin tocar el proceso.
    }
    Start-Sleep -Seconds 30
}
