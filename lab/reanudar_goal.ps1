<#
    reanudar_goal.ps1 - Watchdog que mantiene viva la sesion de Claude Code que
    esta trabajando el goal del fin de semana del 2026-09-05.

    QUE HACE. Corre desde el Programador de tareas de Windows. Si la sesion esta
    trabajando, no hace nada. Si se murio -tipicamente porque se acabo la cuota
    de tokens- la vuelve a levantar con el goal puesto y con el REMOTE CONTROL
    activo, para que Elias pueda seguirla desde el celular. Cuando la
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

El Remote Control queda activo con el nombre 'tesis-goal' para que Elias pueda
mirar desde el celular. No lo apagues.

No apagues la computadora. Commitea seguido explicando POR QUE.
'@

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$log   = Join-Path $LogDir "goal_$stamp.log"

# ---------------------------------------------------------------------------
# COMO SE LANZA, Y POR QUE ASI
#
# Elias pidio que la reanudacion deje el Remote Control activo para poder mirar
# desde el celular. Eso obliga a dos cambios respecto de la version anterior:
#
# 1. `--remote-control` arranca una sesion INTERACTIVA, mientras que la version
#    anterior usaba `-p`, que es el modo no interactivo. Son incompatibles: no se
#    puede tener las dos cosas. Se elige interactiva, porque sin ella no hay
#    Remote Control y Elias se queda sin ver nada.
#
# 2. Una sesion interactiva necesita una TERMINAL, y una tarea del Programador
#    no le da ninguna. Por eso no se invoca claude directo sino que se abre una
#    CONSOLA NUEVA con Start-Process: ahi si hay TTY. Como efecto util, la
#    ventana queda visible en la maquina, asi que tambien se ve sin el celular.
#
# El goal viaja como prompt posicional, que en modo interactivo se manda como
# primer mensaje. O sea que la sesion arranca sola y trabajando, no esperando.
#
# El nombre del Remote Control es fijo para que sea reconocible en la lista del
# celular entre otras sesiones.
$NombreRemoto = 'tesis-goal'

Anotar "lanzando consola nueva: claude --resume $Sesion --remote-control $NombreRemoto"

# El goal se guarda en un archivo y se pasa por -f para no pelearse con el
# escapado de comillas y saltos de linea a traves de dos capas de shell.
$goalFile = Join-Path $LogDir "goal_$stamp.txt"
Set-Content -LiteralPath $goalFile -Value $goal -Encoding UTF8

$inner = @"
Set-Location '$Repo'
`$g = Get-Content -Raw -LiteralPath '$goalFile'
& '$Claude' --resume '$Sesion' --remote-control '$NombreRemoto' --dangerously-skip-permissions `$g
"@
$innerFile = Join-Path $LogDir "lanzar_$stamp.ps1"
Set-Content -LiteralPath $innerFile -Value $inner -Encoding UTF8

try {
    Start-Process -FilePath 'powershell.exe' `
        -ArgumentList '-NoProfile', '-ExecutionPolicy', 'Bypass', '-NoExit', '-File', $innerFile `
        -WorkingDirectory $Repo
    Anotar "consola lanzada (script: $innerFile)"
}
catch {
    Anotar ("no se pudo lanzar la consola: {0}" -f $_.Exception.Message)
}
