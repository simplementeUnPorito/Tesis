' Lanza auto-commit-submodules.ps1 sin abrir ninguna ventana de consola.
' Task Scheduler no puede correr la tarea en sesion 0 (S4U requiere permisos de
' administrador), asi que este envoltorio esconde la ventana desde la sesion
' interactiva. Espera al proceso y devuelve su codigo de salida para que
' MultipleInstances, ExecutionTimeLimit y el historial de la tarea sigan
' funcionando igual que con la invocacion directa.
Option Explicit

Dim fso, shell, scriptDirectory, workerScript, powerShell, hours, command

Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")

scriptDirectory = fso.GetParentFolderName(WScript.ScriptFullName)
workerScript = fso.BuildPath(scriptDirectory, "auto-commit-submodules.ps1")

powerShell = fso.BuildPath(shell.ExpandEnvironmentStrings("%ProgramFiles%"), _
    "PowerShell\7\pwsh.exe")
If Not fso.FileExists(powerShell) Then
    powerShell = fso.BuildPath(shell.ExpandEnvironmentStrings("%SystemRoot%"), _
        "System32\WindowsPowerShell\v1.0\powershell.exe")
End If

hours = "24"
If WScript.Arguments.Count > 0 Then
    hours = WScript.Arguments(0)
End If

command = """" & powerShell & """" & _
    " -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File """ & _
    workerScript & """ -HoursWithoutCommit " & hours

' 0 = ventana oculta, True = esperar a que termine.
WScript.Quit shell.Run(command, 0, True)
