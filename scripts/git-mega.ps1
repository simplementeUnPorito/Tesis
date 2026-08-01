# Helpers Git del superproyecto Tesis.
# Este archivo se carga desde el perfil de PowerShell del usuario.

function Invoke-MegaGit {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][string[]]$Arguments
    )

    $allOutput = @(& git -C $Repository @Arguments 2>&1)
    $exitCode = $LASTEXITCODE
    $standardOutput = @($allOutput | Where-Object {
        $_ -isnot [System.Management.Automation.ErrorRecord]
    } | ForEach-Object { $_.ToString() })
    $errorOutput = @($allOutput | Where-Object {
        $_ -is [System.Management.Automation.ErrorRecord]
    } | ForEach-Object { $_.ToString() })

    [pscustomobject]@{
        Code = $exitCode
        Out = ($standardOutput -join "`n")
        Error = ($errorOutput -join "`n")
        Combined = (@($standardOutput) + @($errorOutput) -join "`n")
    }
}

function Get-MegaRepositoryRoot {
    $probe = Invoke-MegaGit -Repository (Get-Location).Path `
        -Arguments @("rev-parse", "--show-toplevel")
    if ($probe.Code -ne 0 -or [string]::IsNullOrWhiteSpace($probe.Out)) {
        throw "No estás dentro de un repositorio Git."
    }

    $root = $probe.Out.Trim()
    while ($true) {
        $superproject = Invoke-MegaGit -Repository $root `
            -Arguments @("rev-parse", "--show-superproject-working-tree")
        if ($superproject.Code -ne 0 -or
            [string]::IsNullOrWhiteSpace($superproject.Out)) {
            break
        }
        $root = $superproject.Out.Trim()
    }
    return $root
}

function Get-MegaSubmodulePathsDepthFirst {
    param(
        [Parameter(Mandatory)][string]$ParentRepository,
        [string]$ParentRelativePath = ""
    )

    if (-not (Test-Path -LiteralPath (Join-Path $ParentRepository ".gitmodules"))) {
        return @()
    }

    $config = Invoke-MegaGit -Repository $ParentRepository -Arguments @(
        "config", "--file", ".gitmodules", "--get-regexp",
        "^submodule\..*\.path$"
    )
    if ($config.Code -ne 0) {
        throw "No se pudo leer $ParentRepository/.gitmodules: $($config.Combined)"
    }

    $paths = [System.Collections.Generic.List[string]]::new()
    foreach ($line in @($config.Out -split "`n")) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($line -notmatch "^\S+\s+(.+)$") {
            throw "Entrada de .gitmodules no reconocida: $line"
        }

        $childPath = $Matches[1].Trim().Replace("\", "/")
        $rootRelativePath = if ($ParentRelativePath) {
            "$ParentRelativePath/$childPath"
        }
        else {
            $childPath
        }
        $childRepository = Join-Path $ParentRepository $childPath

        if (Test-Path -LiteralPath $childRepository) {
            foreach ($nested in @(Get-MegaSubmodulePathsDepthFirst `
                -ParentRepository $childRepository `
                -ParentRelativePath $rootRelativePath)) {
                $paths.Add($nested)
            }
        }
        $paths.Add($rootRelativePath)
    }

    return $paths.ToArray()
}

function Get-MegaDirectSubmodulePaths {
    param([Parameter(Mandatory)][string]$RepositoryRoot)

    if (-not (Test-Path -LiteralPath (Join-Path $RepositoryRoot ".gitmodules"))) {
        return @()
    }
    $config = Invoke-MegaGit -Repository $RepositoryRoot -Arguments @(
        "config", "--file", ".gitmodules", "--get-regexp",
        "^submodule\..*\.path$"
    )
    if ($config.Code -ne 0) { return @() }

    return @($config.Out -split "`n" | ForEach-Object {
        if ($_ -match "^\S+\s+(.+)$") {
            $Matches[1].Trim().Replace("\", "/")
        }
    } | Where-Object { $_ })
}

function Get-MegaRemoteBranches {
    param([Parameter(Mandatory)][string]$Repository)

    $remote = Invoke-MegaGit -Repository $Repository `
        -Arguments @("ls-remote", "--heads", "origin")
    if ($remote.Code -ne 0) {
        throw "No se pudo consultar origin: $($remote.Combined)"
    }

    $branches = [System.Collections.Generic.List[object]]::new()
    foreach ($line in @($remote.Out -split "`n")) {
        if ($line -match "^([0-9a-f]{40})\s+refs/heads/(.+)$") {
            $branches.Add([pscustomobject]@{
                Sha = $Matches[1]
                Name = $Matches[2]
            })
        }
    }
    return $branches.ToArray()
}

function Get-MegaDefaultRemoteBranch {
    param([Parameter(Mandatory)][string]$Repository)

    $remoteHead = Invoke-MegaGit -Repository $Repository `
        -Arguments @("ls-remote", "--symref", "origin", "HEAD")
    if ($remoteHead.Code -ne 0) { return $null }
    foreach ($line in @($remoteHead.Out -split "`n")) {
        if ($line -match "^ref:\s+refs/heads/(.+)\s+HEAD$") {
            return $Matches[1]
        }
    }
    return $null
}

function Get-MegaBranchPlan {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][object[]]$RemoteBranches
    )

    $symbolic = Invoke-MegaGit -Repository $Repository `
        -Arguments @("symbolic-ref", "--quiet", "--short", "HEAD")
    if ($symbolic.Code -eq 0 -and $symbolic.Out.Trim()) {
        return [pscustomobject]@{
            Name = $symbolic.Out.Trim()
            Detached = $false
            TrackRemote = $false
        }
    }

    $headResult = Invoke-MegaGit -Repository $Repository `
        -Arguments @("rev-parse", "HEAD")
    if ($headResult.Code -ne 0) {
        throw "No se pudo leer HEAD: $($headResult.Combined)"
    }
    $head = $headResult.Out.Trim()
    $matching = @($RemoteBranches | Where-Object { $_.Sha -eq $head })
    $defaultBranch = Get-MegaDefaultRemoteBranch -Repository $Repository
    $selected = $matching | Where-Object { $_.Name -eq $defaultBranch } |
        Select-Object -First 1
    if (-not $selected) {
        $selected = $matching | Where-Object { $_.Name -in @("main", "master") } |
            Select-Object -First 1
    }
    if (-not $selected) {
        $selected = $matching | Sort-Object Name | Select-Object -First 1
    }

    if ($selected) {
        return [pscustomobject]@{
            Name = $selected.Name
            Detached = $true
            TrackRemote = $true
        }
    }

    return [pscustomobject]@{
        Name = "auto-guardado/{0}-{1}" -f `
            (Get-Date -Format "yyyyMMdd-HHmmss"), $head.Substring(0, 8)
        Detached = $true
        TrackRemote = $false
    }
}

function Set-MegaCommitBranch {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][pscustomobject]$Plan
    )

    if (-not $Plan.Detached) { return }

    $localBranch = Invoke-MegaGit -Repository $Repository -Arguments @(
        "show-ref", "--verify", "--hash", "refs/heads/$($Plan.Name)"
    )
    if ($localBranch.Code -eq 0) {
        $head = (Invoke-MegaGit -Repository $Repository `
            -Arguments @("rev-parse", "HEAD")).Out.Trim()
        if ($localBranch.Out.Trim() -ne $head) {
            throw "La rama local $($Plan.Name) existe en otro commit."
        }
        $switch = Invoke-MegaGit -Repository $Repository `
            -Arguments @("switch", $Plan.Name)
    }
    elseif ($Plan.TrackRemote) {
        $switch = Invoke-MegaGit -Repository $Repository -Arguments @(
            "switch", "-c", $Plan.Name, "--track", "origin/$($Plan.Name)"
        )
    }
    else {
        $switch = Invoke-MegaGit -Repository $Repository `
            -Arguments @("switch", "-c", $Plan.Name)
    }

    if ($switch.Code -ne 0) {
        throw "No se pudo seleccionar $($Plan.Name): $($switch.Combined)"
    }
}

function Invoke-MegaCommitRepository {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][string]$Label,
        [Parameter(Mandatory)][string]$Message,
        [switch]$DryRun,
        [switch]$NoPush
    )

    try {
        $remoteBranches = @(Get-MegaRemoteBranches -Repository $Repository)
        $plan = Get-MegaBranchPlan -Repository $Repository `
            -RemoteBranches $remoteBranches
        $head = (Invoke-MegaGit -Repository $Repository `
            -Arguments @("rev-parse", "HEAD")).Out.Trim()
        $remoteBranch = $remoteBranches | Where-Object { $_.Name -eq $plan.Name } |
            Select-Object -First 1
        $remoteSha = if ($remoteBranch) { $remoteBranch.Sha } else { $null }
        $status = Invoke-MegaGit -Repository $Repository -Arguments @(
            "status", "--porcelain=v1", "--untracked-files=all"
        )
        if ($status.Code -ne 0) {
            throw "status falló: $($status.Combined)"
        }
        $dirty = -not [string]::IsNullOrWhiteSpace($status.Out)

        if (-not $dirty -and $head -eq $remoteSha) {
            $detail = "$($plan.Name) al día"
            if ($plan.Detached) { $detail += " (HEAD separado válido)" }
            return [pscustomobject]@{
                Label = $Label; Status = "SKIP"; Detail = $detail
            }
        }

        if ($DryRun) {
            $actions = [System.Collections.Generic.List[string]]::new()
            if ($plan.Detached) { $actions.Add("switch $($plan.Name)") }
            if ($dirty) {
                $fileCount = @($status.Out -split "`n").Count
                $actions.Add("commit $fileCount cambio(s)")
            }
            if ($NoPush) { $actions.Add("sin push") }
            else { $actions.Add("push origin/$($plan.Name)") }
            return [pscustomobject]@{
                Label = $Label; Status = "OK"
                Detail = "[dry] $($actions -join '; ')"
            }
        }

        Set-MegaCommitBranch -Repository $Repository -Plan $plan

        $didCommit = $false
        if ($dirty) {
            $add = Invoke-MegaGit -Repository $Repository -Arguments @("add", "-A")
            if ($add.Code -ne 0) { throw "add falló: $($add.Combined)" }
            $commit = Invoke-MegaGit -Repository $Repository -Arguments @(
                "-c", "commit.gpgsign=false", "commit", "--no-verify",
                "-m", $Message
            )
            if ($commit.Code -ne 0) { throw "commit falló: $($commit.Combined)" }
            $didCommit = $true
        }

        $head = (Invoke-MegaGit -Repository $Repository `
            -Arguments @("rev-parse", "HEAD")).Out.Trim()
        if ($NoPush) {
            return [pscustomobject]@{
                Label = $Label; Status = "OK"
                Detail = "$($plan.Name) local; push omitido"
            }
        }
        if ($head -eq $remoteSha) {
            return [pscustomobject]@{
                Label = $Label; Status = $(if ($didCommit) { "OK" } else { "SKIP" })
                Detail = "$($plan.Name) al día"
            }
        }

        $push = Invoke-MegaGit -Repository $Repository -Arguments @(
            "push", "-u", "origin", "$($plan.Name):$($plan.Name)"
        )
        if ($push.Code -ne 0) { throw "push falló: $($push.Combined)" }

        $verify = Get-MegaRemoteBranches -Repository $Repository |
            Where-Object { $_.Name -eq $plan.Name } | Select-Object -First 1
        if (-not $verify -or $verify.Sha -ne $head) {
            throw "origin/$($plan.Name) no quedó en $head después del push."
        }
        return [pscustomobject]@{
            Label = $Label; Status = "OK"
            Detail = "$($plan.Name) -> origin ($($head.Substring(0, 8)))"
        }
    }
    catch {
        return [pscustomobject]@{
            Label = $Label; Status = "ERROR"; Detail = $_.Exception.Message
        }
    }
}

function Write-MegaResult {
    param([Parameter(Mandatory)][pscustomobject]$Result)

    $display = switch ($Result.Status) {
        "OK" { @("OK", "Green") }
        "SKIP" { @("--", "DarkGray") }
        default { @("XX", "Red") }
    }
    Write-Host ("  {0} {1,-48} {2}" -f `
        $display[0], $Result.Label, $Result.Detail) -ForegroundColor $display[1]
}

function megacommit {
    <#
    .SYNOPSIS
        Commit y push de submódulos anidados y del superproyecto.
    .DESCRIPTION
        Procesa los submódulos de adentro hacia afuera para propagar gitlinks.
        Un HEAD separado limpio es válido. Si necesita commitear desde uno,
        selecciona la rama remota que apunta al SHA actual o crea una rama
        local auto-guardado/* para que el commit nunca quede huérfano.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, Position = 0)][string]$message,
        [switch]$DryRun,
        [switch]$NoPush,
        [ValidateRange(1, 32)][int]$ThrottleLimit = 8
    )

    if ([string]::IsNullOrWhiteSpace($message)) {
        throw "Proporciona un mensaje de commit."
    }

    try { $root = Get-MegaRepositoryRoot }
    catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red; return }
    $paths = @(Get-MegaSubmodulePathsDepthFirst -ParentRepository $root)

    Write-Host "megacommit: '$message'" -ForegroundColor Cyan
    Write-Host "  raíz: $root" -ForegroundColor DarkGray
    Write-Host "  submódulos: $($paths.Count) (orden dependiente)$(if ($DryRun) { ' [DRY-RUN]' })$(if ($NoPush) { ' [NO-PUSH]' })" -ForegroundColor DarkGray
    if ($ThrottleLimit -ne 8) {
        Write-Host "  ThrottleLimit se conserva por compatibilidad; los niveles dependientes se procesan en serie." -ForegroundColor DarkGray
    }
    Write-Host ""

    $results = [System.Collections.Generic.List[object]]::new()
    foreach ($path in $paths) {
        $repository = Join-Path $root $path
        if (-not (Test-Path -LiteralPath $repository)) {
            $result = [pscustomobject]@{
                Label = $path; Status = "SKIP"; Detail = "no inicializado"
            }
        }
        else {
            $result = Invoke-MegaCommitRepository -Repository $repository `
                -Label $path -Message $message -DryRun:$DryRun -NoPush:$NoPush
        }
        $results.Add($result)
        Write-MegaResult -Result $result
        if ($result.Status -eq "ERROR") {
            Write-Host ""
            Write-Host "Megacommit detenido; no se procesa el padre de un submódulo fallido." -ForegroundColor Red
            return
        }
    }

    Write-Host ""
    $main = Invoke-MegaCommitRepository -Repository $root `
        -Label "(repo principal)" -Message $message `
        -DryRun:$DryRun -NoPush:$NoPush
    Write-MegaResult -Result $main
    Write-Host ""
    if ($main.Status -eq "ERROR") {
        Write-Host "Megacommit incompleto." -ForegroundColor Red
    }
    else {
        Write-Host "Megacommit completado." -ForegroundColor Green
    }
}

function Get-MegaRootRelation {
    param(
        [Parameter(Mandatory)][string]$Repository,
        [Parameter(Mandatory)][string]$LocalSha,
        [Parameter(Mandatory)][string]$RemoteSha
    )

    if ($LocalSha -eq $RemoteSha) { return "equal" }
    $remoteAncestor = Invoke-MegaGit -Repository $Repository `
        -Arguments @("merge-base", "--is-ancestor", $RemoteSha, $LocalSha)
    if ($remoteAncestor.Code -eq 0) { return "ahead" }
    $localAncestor = Invoke-MegaGit -Repository $Repository `
        -Arguments @("merge-base", "--is-ancestor", $LocalSha, $RemoteSha)
    if ($localAncestor.Code -eq 0) { return "behind" }
    return "diverged"
}

function megapull {
    <#
    .SYNOPSIS
        Actualiza el superproyecto y sincroniza sus submódulos fijados.
    .DESCRIPTION
        Hace pull únicamente de la rama del superproyecto. Después ejecuta
        submodule sync/update --recursive para dejar cada submódulo exactamente
        en el SHA registrado. Detached HEAD es el estado normal y correcto.
    #>
    [CmdletBinding()]
    param(
        [switch]$DryRun,
        [switch]$Rebase,
        [ValidateRange(1, 32)][int]$ThrottleLimit = 8
    )

    try { $root = Get-MegaRepositoryRoot }
    catch { Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red; return }

    Write-Host "megapull" -ForegroundColor Cyan
    Write-Host "  raíz: $root$(if ($DryRun) { ' [DRY-RUN]' })$(if ($Rebase) { ' [REBASE]' })" -ForegroundColor DarkGray
    if ($ThrottleLimit -ne 8) {
        Write-Host "  ThrottleLimit se conserva por compatibilidad; git submodule update controla el recorrido." -ForegroundColor DarkGray
    }

    $rootStatus = Invoke-MegaGit -Repository $root -Arguments @(
        "status", "--porcelain=v1", "--untracked-files=all",
        "--ignore-submodules=dirty"
    )
    if ($rootStatus.Code -ne 0) {
        Write-Host "Error leyendo el estado raíz: $($rootStatus.Combined)" -ForegroundColor Red
        return
    }
    if ($rootStatus.Out.Trim()) {
        Write-Host "  XX repo principal con cambios; commit o stash antes de actualizar." -ForegroundColor Red
        return
    }

    $dirtyModules = [System.Collections.Generic.List[string]]::new()
    foreach ($path in @(Get-MegaSubmodulePathsDepthFirst -ParentRepository $root)) {
        $repository = Join-Path $root $path
        if (-not (Test-Path -LiteralPath $repository)) { continue }
        $status = Invoke-MegaGit -Repository $repository -Arguments @(
            "status", "--porcelain=v1", "--untracked-files=all"
        )
        if ($status.Code -eq 0 -and $status.Out.Trim()) {
            $dirtyModules.Add($path)
        }
    }
    if ($dirtyModules.Count -gt 0) {
        Write-Host "  XX submódulos con cambios: $($dirtyModules -join ', ')" -ForegroundColor Red
        Write-Host "     Usa megacommit o stash antes de actualizar." -ForegroundColor Yellow
        return
    }

    $branchResult = Invoke-MegaGit -Repository $root `
        -Arguments @("symbolic-ref", "--quiet", "--short", "HEAD")
    if ($branchResult.Code -ne 0 -or -not $branchResult.Out.Trim()) {
        Write-Host "  XX el repo principal está en HEAD separado." -ForegroundColor Red
        return
    }
    $branch = $branchResult.Out.Trim()
    $remoteBranches = @(Get-MegaRemoteBranches -Repository $root)
    $remoteBranch = $remoteBranches | Where-Object { $_.Name -eq $branch } |
        Select-Object -First 1
    if (-not $remoteBranch) {
        Write-Host "  XX origin/$branch no existe." -ForegroundColor Red
        return
    }

    $localSha = (Invoke-MegaGit -Repository $root `
        -Arguments @("rev-parse", "HEAD")).Out.Trim()
    $relation = Get-MegaRootRelation -Repository $root `
        -LocalSha $localSha -RemoteSha $remoteBranch.Sha

    if ($DryRun) {
        $detail = switch ($relation) {
            "equal" { "$branch ya está al día" }
            "ahead" { "$branch tiene commits locales; no requiere pull" }
            "behind" { "actualizaría $($localSha.Substring(0,8)) -> $($remoteBranch.Sha.Substring(0,8))" }
            default { if ($Rebase) { "rebasaría la divergencia con origin/$branch" } else { "divergencia; requiere -Rebase o resolución manual" } }
        }
        Write-Host "  OK [dry] $detail" -ForegroundColor Green
        Write-Host "  OK [dry] sincronizaría e inicializaría submódulos recursivamente" -ForegroundColor Green
        Write-Host ""
        Write-Host "Megapull comprobado sin cambios." -ForegroundColor Green
        return
    }

    $fetch = Invoke-MegaGit -Repository $root `
        -Arguments @("fetch", "origin", $branch)
    if ($fetch.Code -ne 0) {
        Write-Host "  XX fetch falló: $($fetch.Combined)" -ForegroundColor Red
        return
    }
    $remoteSha = (Invoke-MegaGit -Repository $root `
        -Arguments @("rev-parse", "origin/$branch")).Out.Trim()
    $localSha = (Invoke-MegaGit -Repository $root `
        -Arguments @("rev-parse", "HEAD")).Out.Trim()
    $relation = Get-MegaRootRelation -Repository $root `
        -LocalSha $localSha -RemoteSha $remoteSha

    if ($relation -eq "behind" -or ($relation -eq "diverged" -and $Rebase)) {
        $pullArguments = if ($Rebase) {
            @("pull", "--rebase", "origin", $branch)
        }
        else {
            @("pull", "--ff-only", "origin", $branch)
        }
        $pull = Invoke-MegaGit -Repository $root -Arguments $pullArguments
        if ($pull.Code -ne 0) {
            Write-Host "  XX pull falló: $($pull.Combined)" -ForegroundColor Red
            return
        }
        Write-Host "  OK repo principal actualizado" -ForegroundColor Green
    }
    elseif ($relation -eq "diverged") {
        Write-Host "  XX rama divergente; usa megapull -Rebase o resuelve manualmente." -ForegroundColor Red
        return
    }
    elseif ($relation -eq "ahead") {
        Write-Host "  -- repo principal tiene commits locales; no requiere pull" -ForegroundColor DarkGray
    }
    else {
        Write-Host "  -- repo principal ya está al día" -ForegroundColor DarkGray
    }

    $sync = Invoke-MegaGit -Repository $root `
        -Arguments @("submodule", "sync", "--recursive")
    if ($sync.Code -ne 0) {
        Write-Host "  XX submodule sync falló: $($sync.Combined)" -ForegroundColor Red
        return
    }
    $update = Invoke-MegaGit -Repository $root `
        -Arguments @("submodule", "update", "--init", "--recursive")
    if ($update.Code -ne 0) {
        Write-Host "  XX submodule update falló: $($update.Combined)" -ForegroundColor Red
        return
    }

    $count = @(Get-MegaSubmodulePathsDepthFirst -ParentRepository $root).Count
    Write-Host "  OK $count submódulos sincronizados con los gitlinks" -ForegroundColor Green
    Write-Host ""
    Write-Host "Megapull completado." -ForegroundColor Green
}
