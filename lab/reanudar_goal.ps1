<#
    reanudar_goal.ps1 - Reanuda ESTA sesion de Claude Code cuando se repone la
    cuota, y vuelve a activar el goal de caracterizacion de la planta.

    Lo pidio Elias explicitamente el 2026-09-04 al ver que quedaba 29 % de la
    sesion y 3 h 02 min para el reset. Es de UN SOLO DISPARO: no es una rutina
    que se levante sola todos los dias. Se autoborra al terminar.

    Uso manual:  .\reanudar_goal.ps1
#>

$ErrorActionPreference = 'Stop'

$Sesion = 'e4c99118-5337-4ae4-b0d6-b84aa42db56b'
$Repo   = 'C:\Github\Tesis'
$LogDir = Join-Path $env:LOCALAPPDATA 'claude_reanudar'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$log = Join-Path $LogDir ("goal_{0}.log" -f (Get-Date -Format 'yyyyMMdd_HHmmss'))

$goal = @'
Reanudas con el goal activo. Seguilo tal cual: "Todo lo que hayas medido creele
mas que lo que sea testeado. Si da demasiado diferente medi muchas veces, pero si
siempre sale asi deja lo medido y registralo para que despues lo verifique Elias.
Medi tambien las otras curvas, no te quedes con supuestos de linealidad. Sin
importar la ganancia de los DOS PGA la cadena siempre se tiene que poder
calibrar: proba todas las combinaciones que puedas y empeza por las mas dificiles.
La calibracion no tiene que ser perfecta, tiene que ser FIABLE: +-100 mV
exagerando mucho, idealmente del orden de 20 mV, porque la medicion mas fina es
+-0,512 V y mas de 100 mV ya es tragico. El Ki chico hay que definirlo: lo minimo
viable para que corrija el error remanente sin oscilar. Hace primero todas las
mediciones que puedas."

ESTADO AL CORTE (leelo antes de tocar nada):
- docs/HANDOFF_NOCHE_2026-09-03.md es la fuente de verdad del banco.
- lab/PREGUNTAS_PARA_ELIAS.md tiene las preguntas acumuladas; NO lo pises,
  agregale al final.
- src/interfaces/python/medir_planta.py es el programa de medicion ya escrito
  (subcomandos escalon / curva / matriz). Se corre con el Python 3.14:
  C:\Users\elias\AppData\Local\Python\pythoncore-3.14-64\python.exe
  y OJO: --port va ANTES del subcomando.
- Los crudos van a lab/planta/ en JSON, y Elias pidio graficas ademas de tablas.
- BLOQUEO ACTIVO: con el firmware de AUTOTEST grabado, el enlace PSoC<->ESP
  quedo CAIDO (probe=0, ping=0, sin tramas). El firmware de CAMPO si enlazaba.
  Antes de medir hay que resolver eso.

REGLA DE TOKENS: delegar a codex lo pesado y de poco juicio (compilar, grabar,
baterias largas), pidiendole SIEMPRE informe corto:
  codex exec --dangerously-bypass-approvals-and-sandbox "<tarea>" < /dev/null

No apagues la computadora. Commitea seguido explicando POR QUE.
'@

Push-Location $Repo
try {
    & claude --resume $Sesion --dangerously-skip-permissions -p $goal *>&1 |
        Tee-Object -FilePath $log
}
finally {
    Pop-Location
}

# Un solo disparo: la tarea se borra sola para no quedar como rutina permanente.
Unregister-ScheduledTask -TaskName 'ClaudeGoalPlanta' -Confirm:$false `
    -ErrorAction SilentlyContinue
