# Auto-commit de submódulos

`auto-commit-submodules.ps1` recorre de adentro hacia afuera todas las rutas
declaradas en `.gitmodules`, incluidos los submódulos anidados. Cuando
encuentra cambios y el último commit del submódulo tiene al menos 24 horas,
crea un commit con un mensaje como:

```text
Auto-guardado: sábado 2026-08-01
```

Luego registra únicamente los punteros de esos submódulos en el superproyecto.
No realiza `push`. Por seguridad omite repositorios con conflictos u
operaciones Git en curso. Si un submódulo está en `HEAD` separado, crea una
rama local `auto-guardado/AAAAMMDD-HHMMSS` antes del commit para que este no
quede huérfano. El registro se guarda localmente en
`.git/auto-commit-submodules.log`.

La tarea de Windows se instala con:

```powershell
.\scripts\install-auto-commit-task.ps1
```

Aunque comprueba cada hora, solo crea commits después de alcanzar el umbral de
24 horas. Esto evita que una comprobación diaria pueda retrasar el respaldo
casi 48 horas dependiendo de la hora del último commit.

Comprobación manual sin escribir commits:

```powershell
.\scripts\auto-commit-submodules.ps1 -DryRun
```

Para desinstalar la tarea:

```powershell
Unregister-ScheduledTask -TaskName "Tesis - Auto-commit de submodulos" -Confirm:$false
```
