[CmdletBinding()]
param(
    [switch]$Strict
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

# Se audita documentación operativa. Se excluyen bibliotecas de terceros,
# snapshots históricos y el corpus académico de Obsidian, que usa wikilinks y
# tiene reglas distintas a Markdown convencional.
$excluded = @(
    '[\\/]third-party[\\/]',
    '[\\/]\.venv[\\/]',
    '[\\/]Generated_Source[\\/]',
    '[\\/]esp-web-historicos[\\/][0-9]{2}_',
    '[\\/]docs[\\/]investigacion[\\/]Notes[\\/]Surface Wave Methods[\\/]',
    '[\\/]docs[\\/]investigacion[\\/]Notes[\\/]bitacora[\\/]',
    '[\\/]docs[\\/]Primera Presentación[\\/]recopilacion_figuras[\\/]'
)

function Test-Excluded([string]$Path) {
    foreach ($pattern in $excluded) {
        if ($Path -match $pattern) { return $true }
    }
    return $false
}

$markdown = Get-ChildItem -LiteralPath $repoRoot -Recurse -File -Filter '*.md' |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' -and -not (Test-Excluded $_.FullName) }

$broken = [System.Collections.Generic.List[object]]::new()
$checkedLinks = 0
$linkPattern = '!?(?:\[[^\]]*\])\((?<target><[^>]+>|[^\s\)]+)(?:\s+"[^"]*")?\)'

foreach ($file in $markdown) {
    $text = Get-Content -Raw -LiteralPath $file.FullName
    foreach ($match in [regex]::Matches($text, $linkPattern)) {
        $target = $match.Groups['target'].Value.Trim('<', '>')
        if ($target -match '^(?:https?://|mailto:|data:|codex:|#)') { continue }
        $target = ($target -split '#', 2)[0]
        if ([string]::IsNullOrWhiteSpace($target)) { continue }
        $checkedLinks++
        try { $target = [uri]::UnescapeDataString($target) } catch { }
        $resolved = if ($target -match '^[A-Za-z]:[\\/]') {
            $target
        } else {
            Join-Path $file.DirectoryName ($target -replace '/', [IO.Path]::DirectorySeparatorChar)
        }
        if (-not (Test-Path -LiteralPath $resolved)) {
            $broken.Add([pscustomobject]@{
                File = [IO.Path]::GetRelativePath($repoRoot, $file.FullName)
                Target = $target
            })
        }
    }
}

$legacyPatterns = @(
    '(?<!src/)firmware/(?:psoc|esp32)',
    '(?<!src/)software/python',
    '(?<!docs/)investigacion/sources'
)
$legacyFiles = @(
    'README.md',
    'ARCHITECTURE.md',
    'docs/README.md',
    'docs/investigacion/README.md',
    'PCBs/README.md',
    'data/README.md',
    'src/firmware/esp32/README.md',
    'src/firmware/psoc/README.md',
    'src/interfaces/python/README.md',
    'src/interfaces/matlab/README.md',
    'src/calculos_modelados/python/README.md',
    'src/calculos_modelados/matlab/README.md'
) | ForEach-Object { Get-Item -LiteralPath (Join-Path $repoRoot $_) }

$legacyHits = [System.Collections.Generic.List[object]]::new()
foreach ($file in $legacyFiles) {
    $text = Get-Content -Raw -LiteralPath $file.FullName
    foreach ($pattern in $legacyPatterns) {
        if ($text -match $pattern) {
            $legacyHits.Add([pscustomobject]@{
                File = [IO.Path]::GetRelativePath($repoRoot, $file.FullName)
                Pattern = $pattern
            })
        }
    }
}

Write-Host "Documentos operativos: $($markdown.Count)"
Write-Host "Enlaces locales comprobados: $checkedLinks"
Write-Host "Enlaces locales rotos: $($broken.Count)"
if ($broken.Count) { $broken | Sort-Object File,Target | Format-Table -AutoSize }
Write-Host "Documentos con rutas legacy: $($legacyHits.Count)"
if ($legacyHits.Count) { $legacyHits | Sort-Object File,Pattern | Format-Table -AutoSize }

if ($Strict -and ($broken.Count -gt 0 -or $legacyHits.Count -gt 0)) {
    exit 1
}
