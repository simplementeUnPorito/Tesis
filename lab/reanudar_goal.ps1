<#
    reanudar_goal.ps1 - Watchdog que mantiene viva la sesion de Claude Code que
    esta trabajando el goal del fin de semana del 2026-09-05.

    QUE HACE. Corre cada 20 min desde el Programador de tareas de Windows. Si la
    sesion esta trabajando, no hace nada. Si se murio -tipicamente porque se
    acabo la cuota de tokens- la vuelve a levantar con el goal puesto. Cuando la
    cuota todavia no se repuso, el intento falla en segundos y se reintenta a los
    20 min, asi que el costo de fallar es despreciable y no hace falta saber
    cuando es el reset.

    COMO SE APAGA. Crear el archivo lab\PARAR_REANUDACION (vacio, el contenido
    da igual). El watchdog lo mira antes que nada y se va sin hacer nada. Para
    sacar la tarea del todo:
        Unregister-ScheduledTask -TaskName 'ClaudeReanudarGoalTesis' -Confirm:$false

    POR QUE UN WATCHDOG Y NO UN CRON DE CLAUDE. La herramienta CronCreate de
    Claude vive dentro de la sesion: si la sesion muere, el cron muere con ella,
    que es exactamente el caso que hay que cubrir. Tiene que ser algo del sistema
    operativo, afuera de Claude.

    Uso manual (fuerza un intento, ignorando la deteccion de "ya esta viva"):
        .\reanudar_goal.ps1 -Forzar
#>
[CmdletBinding()]
param(
    [switch]$Forzar,
    # Minutos sin escribir en el log de la sesion tras los cuales se la
    # considera muerta. 15 es holgado: una sesion trabajando escribe seguido.
    [int]$MinutosSinVida = 15
)

$ErrorActionPreference = 'Stop'

$Sesion  = 'ce5b6f0c-ab02-4d84-8e8e-85a6287aa68c'
$Repo    = 'C:\Github\Tesis'
$Claude  = 'C:\Users\elias\.local\bin\claude.exe'
$Jsonl   = "C:\Users\elias\.claude\projects\C--Github-Tesis\$Sesion.jsonl"
$Freno   = Join-Path $Repo 'lab\PARAR_REANUDACION'
$LogDir  = Join-Path $env:LOCALAPPDATA 'claude_reanudar'
$Bitacora = Join-Path $LogDir 'watchdog.log'

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Anotar([string]$texto) {
    $linea = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texto
    Add-Content -LiteralPath $Bitacora -Value $linea -Encoding UTF8
    Write-Host $linea
}

if (Test-Path -LiteralPath $Freno) {
    Anotar "FRENO: existe lab\PARAR_REANUDACION, no hago nada."
    exit 0
}

# ---------------------------------------------------------------------------
# Deteccion de vida. Se piden las DOS condiciones para declararla muerta, para
# no duplicar una sesion interactiva que este simplemente esperando a Elias:
#   1. no hay ningun claude.exe corriendo, y
#   2. el log de la sesion no se toco en los ultimos $MinutosSinVida minutos.
# ---------------------------------------------------------------------------
if (-not $Forzar) {
    $vivos = @(Get-Process -Name 'claude' -ErrorAction SilentlyContinue)
    if ($vivos.Count -gt 0) {
        Anotar ("viva: hay {0} proceso(s) claude.exe. Nada que hacer." -f $vivos.Count)
        exit 0
    }
    if (Test-Path -LiteralPath $Jsonl) {
        $edad = (Get-Date) - (Get-Item -LiteralPath $Jsonl).LastWriteTime
        if ($edad.TotalMinutes -lt $MinutosSinVida) {
            Anotar ("viva: el log se toco hace {0:N1} min. Nada que hacer." -f $edad.TotalMinutes)
            exit 0
        }
        Anotar ("MUERTA: sin proceso y log de hace {0:N1} min. Reanudo." -f $edad.TotalMinutes)
    } else {
        Anotar "MUERTA: no existe el log de la sesion. Reanudo igual."
    }
} else {
    Anotar "FORZADO por parametro."
}

$goal = @'
Se te corto la sesion (casi seguro por cuota de tokens) y este watchdog te
reanuda. Retomas el goal del fin de semana del 2026-09-05 tal cual estaba.

LEE PRIMERO, EN ESTE ORDEN:
  1. lab/HANDOFF_GOAL_2026-09-05.md  <- estado de la tarea, que sigue, que ya
     esta hecho. Es la fuente de verdad. Mantenelo actualizado vos.
  2. docs/MEDICIONES_2026-09-05.md   <- lo medido hoy, con metodo y crudos.
  3. docs/MEDICIONES_2026-09-04.md   <- lo medido ayer.

EL GOAL, en palabras de Elias:
"segui con lo que estuvimos planteando hasta dejar todo como concordamos o
encuentres una pared que te obligue a pedirme interaccion con el mundo fisico"

Y de antes, que sigue vigente:
"Todo lo que hayas medido creele mas que lo que sea testeado. Si da demasiado
diferente medi muchas veces, pero si siempre sale asi deja lo medido y
registralo. Sin importar la ganancia de los DOS PGA la cadena siempre se tiene
que poder calibrar. La calibracion no tiene que ser perfecta, tiene que ser
FIABLE: el maximo aceptado es 2 tau de espera y 20 mV de error, y si se
consigue mejor, mejor. Elias quiere el mejor TIEMPO posible dentro de eso."

REGLAS QUE NO SE NEGOCIAN:
- El ESP esclavo esta en COM8. VERIFICALO antes de concluir nada (perdimos una
  tarde midiendo el ESP equivocado). El maestro esta desenchufado a proposito.
- Grabar el PSoC: .\program_psoc.ps1 [-SelfTest]. SI funciona, esta verificado
  el 2026-09-05. NUNCA con -AllRows. Redirigi la salida de PPCLI a un archivo,
  son ~1100 lineas.
- Python 3.14: C:\Users\elias\AppData\Local\Python\pythoncore-3.14-64\python.exe
  El de PlatformIO no tiene PyQt6.
- El geofono esta acostado en el piso de una habitacion, a 4 m de la pared y
  ~9 m de la lomada de la calle. Esta FUERA DE ESPECIFICACION por la
  inclinacion: sirve para comparaciones relativas, NO para numeros absolutos de
  sensibilidad ni de espectro. Declararlo siempre.
- La casa tiene gente circulando todo el fin de semana salvo la madrugada: las
  tandas largas de senal van de madrugada, y hay que descartar por energia las
  ventanas contaminadas.
- Toda la instrumentacion de laboratorio tiene que quedar FUERA del firmware de
  campo, por estructura de archivos y no por disciplina.
- Elias quiere graficas, tablas y numeros para mostrar. Documentar mientras se
  trabaja, no al final.
- Si algo te obliga a que Elias toque el hardware, PARA y dejale el pedido
  escrito en lab/PREGUNTAS_PARA_ELIAS.md (agregar al final, no pisar).

No apagues la computadora. Commitea seguido explicando POR QUE.
'@

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$log   = Join-Path $LogDir "goal_$stamp.log"
Anotar "lanzando claude --resume $Sesion (log: $log)"

Push-Location $Repo
try {
    & $Claude --resume $Sesion --dangerously-skip-permissions -p $goal *>&1 |
        Tee-Object -FilePath $log
    Anotar ("claude termino con exit={0}" -f $LASTEXITCODE)
}
catch {
    Anotar ("claude fallo: {0}" -f $_.Exception.Message)
}
finally {
    Pop-Location
}
