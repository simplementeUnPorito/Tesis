[CmdletBinding()]
param(
    [ValidateRange(1, 8760)]
    [int]$HoursWithoutCommit = 24,

    [string]$RepositoryRoot,

    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = Join-Path $PSScriptRoot ".."
}
$RepositoryRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path

$gitDirectory = (& git -C $RepositoryRoot rev-parse --absolute-git-dir 2>$null)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($gitDirectory)) {
    throw "No se encontro un repositorio Git en $RepositoryRoot"
}
$gitDirectory = $gitDirectory.Trim()
$logPath = Join-Path $gitDirectory "auto-commit-submodules.log"

function Write-AutoCommitLog {
    param([Parameter(Mandatory)][string]$Message)

    $line = "{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Write-Output $line
    Add-Content -LiteralPath $logPath -Value $line -Encoding utf8
}

function Invoke-GitChecked {
    param(
        [Parameter(Mandatory)][string]$WorkingDirectory,
        [Parameter(Mandatory)][string[]]$Arguments
    )

    $result = @(& git -C $WorkingDirectory @Arguments 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') fallo en ${WorkingDirectory}: $($result -join [Environment]::NewLine)"
    }

    # PowerShell representa stderr de programas nativos como ErrorRecord al
    # combinarlo con stdout. Git puede emitir avisos de CRLF aun con exit 0;
    # esos avisos no deben confundirse con nombres de archivos o conflictos.
    return @($result | Where-Object {
        $_ -isnot [System.Management.Automation.ErrorRecord]
    })
}

function Test-GitOperationInProgress {
    param([Parameter(Mandatory)][string]$WorkingDirectory)

    $repositoryGitDirectory = (Invoke-GitChecked -WorkingDirectory $WorkingDirectory `
        -Arguments @("rev-parse", "--absolute-git-dir") | Select-Object -Last 1).Trim()
    foreach ($marker in @(
        "MERGE_HEAD",
        "CHERRY_PICK_HEAD",
        "REVERT_HEAD",
        "BISECT_LOG",
        "rebase-apply",
        "rebase-merge"
    )) {
        if (Test-Path -LiteralPath (Join-Path $repositoryGitDirectory $marker)) {
            return $true
        }
    }
    return $false
}

function Get-SubmodulePathsDepthFirst {
    param(
        [Parameter(Mandatory)][string]$ParentRepository,
        [string]$ParentRelativePath = ""
    )

    $modulesFile = Join-Path $ParentRepository ".gitmodules"
    if (-not (Test-Path -LiteralPath $modulesFile)) {
        return @()
    }

    $paths = [System.Collections.Generic.List[string]]::new()
    $lines = @(Invoke-GitChecked -WorkingDirectory $ParentRepository -Arguments @(
        "config", "--file", ".gitmodules", "--get-regexp",
        "^submodule\..*\.path$"
    ))

    foreach ($line in $lines) {
        if ($line -notmatch "^\S+\s+(.+)$") {
            throw "Entrada de .gitmodules no reconocida en ${ParentRepository}: $line"
        }

        $childPath = $Matches[1].Trim().Replace("\", "/")
        if ([string]::IsNullOrWhiteSpace($ParentRelativePath)) {
            $rootRelativePath = $childPath
        }
        else {
            $rootRelativePath = "$ParentRelativePath/$childPath"
        }

        $childRepository = Join-Path $ParentRepository $childPath
        if (Test-Path -LiteralPath $childRepository) {
            foreach ($nestedPath in @(Get-SubmodulePathsDepthFirst `
                -ParentRepository $childRepository `
                -ParentRelativePath $rootRelativePath)) {
                $paths.Add($nestedPath)
            }
        }

        # Los hijos aparecen antes que su padre para que el commit del padre
        # pueda registrar los punteros que acaban de cambiar.
        $paths.Add($rootRelativePath)
    }

    return $paths.ToArray()
}

$dayNames = @(
    "domingo",
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado"
)
$now = Get-Date
$dayName = $dayNames[[int]$now.DayOfWeek]
$dateText = $now.ToString("yyyy-MM-dd")
$commitMessage = "Auto-guardado: $dayName $dateText"
$threshold = [TimeSpan]::FromHours($HoursWithoutCommit)
$committedSubmodules = [System.Collections.Generic.List[string]]::new()
$failures = 0

$directModuleLines = @(Invoke-GitChecked -WorkingDirectory $RepositoryRoot -Arguments @(
    "config",
    "--file",
    ".gitmodules",
    "--get-regexp",
    "^submodule\..*\.path$"
))
$directModulePaths = @($directModuleLines | ForEach-Object {
    if ($_ -notmatch "^\S+\s+(.+)$") {
        throw "Entrada de .gitmodules no reconocida: $_"
    }
    $Matches[1].Trim().Replace("\", "/")
})
$modulePaths = @(Get-SubmodulePathsDepthFirst -ParentRepository $RepositoryRoot)

foreach ($relativePath in $modulePaths) {
    $modulePath = Join-Path $RepositoryRoot $relativePath

    try {
        if (-not (Test-Path -LiteralPath $modulePath)) {
            Write-AutoCommitLog "SKIP $relativePath no esta inicializado."
            continue
        }

        $insideWorkTree = (Invoke-GitChecked -WorkingDirectory $modulePath `
            -Arguments @("rev-parse", "--is-inside-work-tree") | Select-Object -Last 1).Trim()
        if ($insideWorkTree -ne "true") {
            Write-AutoCommitLog "SKIP $relativePath no es un repositorio de trabajo."
            continue
        }

        $changes = @(Invoke-GitChecked -WorkingDirectory $modulePath `
            -Arguments @("status", "--porcelain=v1", "--untracked-files=all"))
        if ($changes.Count -eq 0) {
            Write-AutoCommitLog "OK   $relativePath sin cambios."
            continue
        }

        if (Test-GitOperationInProgress -WorkingDirectory $modulePath) {
            Write-AutoCommitLog "SKIP $relativePath tiene merge, rebase u otra operacion Git en curso."
            continue
        }

        $unmerged = @(Invoke-GitChecked -WorkingDirectory $modulePath `
            -Arguments @("diff", "--name-only", "--diff-filter=U"))
        if ($unmerged.Count -gt 0) {
            Write-AutoCommitLog "SKIP $relativePath tiene conflictos sin resolver."
            continue
        }

        $lastCommitText = (Invoke-GitChecked -WorkingDirectory $modulePath `
            -Arguments @("log", "-1", "--format=%ct") | Select-Object -Last 1).Trim()
        $lastCommit = [DateTimeOffset]::FromUnixTimeSeconds([long]$lastCommitText)
        $age = [DateTimeOffset]::Now - $lastCommit
        if ($age -lt $threshold) {
            Write-AutoCommitLog ("WAIT {0} tiene cambios, pero el ultimo commit fue hace {1:N1} h." -f `
                $relativePath, $age.TotalHours)
            continue
        }

        if ($DryRun) {
            $branchOutput = @(& git -C $modulePath symbolic-ref --quiet --short HEAD 2>$null)
            if ($LASTEXITCODE -ne 0 -or $branchOutput.Count -eq 0) {
                Write-AutoCommitLog "DRY  $relativePath crearia una rama local auto-guardado/*."
            }
            Write-AutoCommitLog "DRY  $relativePath crearia '$commitMessage'."
            continue
        }

        $branchOutput = @(& git -C $modulePath symbolic-ref --quiet --short HEAD 2>$null)
        if ($LASTEXITCODE -ne 0 -or $branchOutput.Count -eq 0) {
            $branchName = "auto-guardado/{0}" -f (Get-Date -Format "yyyyMMdd-HHmmss")
            Invoke-GitChecked -WorkingDirectory $modulePath `
                -Arguments @("switch", "-c", $branchName) | Out-Null
            Write-AutoCommitLog "BRANCH $relativePath -> $branchName"
        }

        Invoke-GitChecked -WorkingDirectory $modulePath -Arguments @("add", "-A") | Out-Null
        $stagedChanges = @(& git -C $modulePath diff --cached --quiet)
        if ($LASTEXITCODE -eq 0) {
            Write-AutoCommitLog "OK   $relativePath no tenia cambios versionables despues de git add."
            continue
        }
        if ($LASTEXITCODE -ne 1) {
            throw "No se pudo comprobar el indice de $relativePath."
        }

        Invoke-GitChecked -WorkingDirectory $modulePath -Arguments @(
            "-c", "commit.gpgsign=false", "commit", "--no-verify", "-m", $commitMessage
        ) | Out-Null
        $committedSubmodules.Add($relativePath)
        Write-AutoCommitLog "COMMIT $relativePath -> $commitMessage"
    }
    catch {
        $failures++
        Write-AutoCommitLog "ERROR $relativePath -> $($_.Exception.Message)"
    }
}

$rootPointers = @($committedSubmodules.ToArray() | Where-Object {
    $_ -in $directModulePaths
})

if (-not $DryRun -and $rootPointers.Count -gt 0) {
    try {
        if (Test-GitOperationInProgress -WorkingDirectory $RepositoryRoot) {
            throw "El superproyecto tiene una operacion Git en curso."
        }

        $rootBranch = @(& git -C $RepositoryRoot symbolic-ref --quiet --short HEAD 2>$null)
        if ($LASTEXITCODE -ne 0 -or $rootBranch.Count -eq 0) {
            throw "El superproyecto esta en HEAD separado."
        }

        $rootMessage = "Actualizar submodulos: $dayName $dateText"
        $commitArguments = @(
            "-c", "commit.gpgsign=false", "commit", "--no-verify", "--only",
            "-m", $rootMessage, "--"
        ) + $rootPointers
        Invoke-GitChecked -WorkingDirectory $RepositoryRoot `
            -Arguments $commitArguments | Out-Null
        Write-AutoCommitLog "COMMIT superproyecto -> $rootMessage"
    }
    catch {
        $failures++
        Write-AutoCommitLog "ERROR superproyecto -> $($_.Exception.Message)"
    }
}

if ($failures -gt 0) {
    Write-AutoCommitLog "FIN con $failures error(es)."
    exit 1
}

Write-AutoCommitLog "FIN sin errores."
