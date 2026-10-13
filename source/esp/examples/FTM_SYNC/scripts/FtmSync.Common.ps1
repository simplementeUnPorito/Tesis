# FTM_SYNC - funciones compartidas (dot-source desde los demas scripts).
# No instala nada. Requiere PowerShell 5.1+ (probado el parser con 7.x).
Set-StrictMode -Version Latest

$script:Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$script:Upstream = Join-Path $script:Root 'upstream'
$script:ProfilesDir = Join-Path $script:Root 'profiles'

# Pines del ESP32-S3 que NO conviene usar como salida de experimento.
# Fuente: hoja de datos / guia de pines de ESP-IDF para ESP32-S3 (verificar con TU placa).
$script:S3Strapping = @(0, 3, 45, 46)
$script:S3UsbJtag = @(19, 20)
$script:S3FlashPsram = @(26, 27, 28, 29, 30, 31, 32)   # SPI flash / PSRAM (33-37 tambien con PSRAM octal)
$script:S3OctalPsram = @(33, 34, 35, 36, 37)
$script:S3Uart0 = @(43, 44)

function Get-FtmSyncProfiles {
    Import-PowerShellDataFile -LiteralPath (Join-Path $script:ProfilesDir 'profiles.psd1')
}

function Get-FtmSyncConfig {
    param([string]$Path, [switch]$AllowExample)
    if (-not $Path) {
        $Path = Join-Path $script:Root 'config\experiment.local.psd1'
        if (-not (Test-Path -LiteralPath $Path)) {
            if ($AllowExample) { $Path = Join-Path $script:Root 'config\experiment.example.psd1' }
            else { throw "Falta config\experiment.local.psd1. Copiar config\experiment.example.psd1 y editarlo." }
        }
    }
    Import-PowerShellDataFile -LiteralPath $Path
}

# Devuelve @{ Errors = @(); Warnings = @() } sin lanzar excepciones.
function Test-FtmSyncConfigValues {
    param([Parameter(Mandatory)]$Config)
    $err = New-Object System.Collections.Generic.List[string]
    $warn = New-Object System.Collections.Generic.List[string]

    $pulse = $Config.PulseGpio
    if ($pulse -isnot [int] -or $pulse -lt 0 -or $pulse -gt 48) { $err.Add("PulseGpio debe ser entero 0..48 (rango del Kconfig de upstream), es '$pulse'.") }
    $ledOn = [bool]$Config.LedEnabled
    $led = $Config.LedGpio
    if ($ledOn) {
        if (@('gpio', 'ws2812') -notcontains $Config.LedType) { $err.Add("LedType debe ser 'gpio' (LED simple activo en bajo) o 'ws2812' (RGB direccionable), es '$($Config.LedType)'.") }
        if ($led -isnot [int] -or $led -lt 0 -or $led -gt 48) { $err.Add("LedEnabled=`$true requiere LedGpio entero 0..48, es '$led'.") }
        elseif ($led -eq $pulse) { $err.Add("LedGpio no puede ser igual a PulseGpio: el LED lo maneja la ISR por software y el pulso el MCPWM.") }
    }
    $pins = @($pulse); if ($ledOn -and $led -is [int]) { $pins += $led }
    foreach ($p in $pins) {
        if ($p -isnot [int]) { continue }
        if ($script:S3Strapping -contains $p) { $warn.Add("GPIO$p es pin de strapping del ESP32-S3: evitar cargas externas.") }
        if ($script:S3UsbJtag -contains $p) { $warn.Add("GPIO$p es D-/D+ del USB nativo (USB-Serial/JTAG): romperia el puerto USB.") }
        if ($script:S3FlashPsram -contains $p) { $warn.Add("GPIO$p esta ocupado por SPI flash/PSRAM en modulos ESP32-S3: no usar.") }
        if ($script:S3OctalPsram -contains $p) { $warn.Add("GPIO$p lo usa la PSRAM octal (modulos N*R8): no usar en esos modulos.") }
        if (($script:S3Uart0 -contains $p) -and $Config.Console -eq 'uart0') { $warn.Add("GPIO$p es UART0 y la consola esta en uart0.") }
    }
    if (@('usb-serial-jtag', 'uart0') -notcontains $Config.Console) { $err.Add("Console debe ser 'usb-serial-jtag' o 'uart0'.") }
    if (-not $Config.WifiSsid -or $Config.WifiSsid.Length -gt 32) { $err.Add('WifiSsid vacio o mayor a 32 caracteres.') }
    if ($Config.WifiPassword.Length -lt 8 -or $Config.WifiPassword.Length -gt 63) { $err.Add('WifiPassword debe tener 8..63 caracteres (WPA2).') }
    if ($Config.WifiChannel -isnot [int] -or $Config.WifiChannel -lt 1 -or $Config.WifiChannel -gt 13) { $err.Add('WifiChannel debe ser 1..13 (rango del Kconfig de upstream).') }
    if ($Config.WifiSsid -match '["\\]' -or $Config.WifiPassword -match '["\\]') { $err.Add('SSID/clave no deben contener comillas ni barra invertida (van a un archivo .defaults).') }
    if (-not [bool]$Config.BoardPinoutConfirmed) { $warn.Add('BoardPinoutConfirmed=$false: se puede compilar pero Flash-Node.ps1 se niega a flashear.') }
    [pscustomobject]@{ Errors = $err.ToArray(); Warnings = $warn.ToArray() }
}

# Texto del archivo .defaults generado (GPIO, LED, consola-independiente, WiFi).
function New-FtmSyncGeneratedDefaults {
    param([Parameter(Mandatory)]$Config)
    $l = New-Object System.Collections.Generic.List[string]
    $l.Add('# GENERADO por FtmSync.Common.ps1 desde config\experiment.local.psd1 - no editar.')
    $l.Add('CONFIG_FTS_PULSE_MCPWM_GPIO_ENABLE=y')
    $l.Add("CONFIG_FTS_PULSE_MCPWM_GPIO=$($Config.PulseGpio)")
    if ($Config.LedEnabled) {
        $l.Add('CONFIG_FTS_LED_ENABLED=y')
        $l.Add("CONFIG_FTS_LED_GPIO=$($Config.LedGpio)")
        $l.Add($(if ($Config.LedType -eq 'ws2812') { 'CONFIG_FTS_LED_WS2812=y' } else { 'CONFIG_FTS_LED_WS2812=n' }))
    }
    else {
        $l.Add('CONFIG_FTS_LED_ENABLED=n')
    }
    $l.Add("CONFIG_FTS_WIFI_SSID=`"$($Config.WifiSsid)`"")
    $l.Add("CONFIG_FTS_WIFI_PASSWORD=`"$($Config.WifiPassword)`"")
    $l.Add("CONFIG_FTS_AP_CHANNEL=$($Config.WifiChannel)")
    ($l -join "`n") + "`n"
}

function Get-FtmSyncWorkRoot {
    param([Parameter(Mandatory)]$Config)
    if ($Config.WorkRoot) { return [IO.Path]::GetFullPath($Config.WorkRoot) }
    Join-Path $script:Root 'work'
}

# Lista ordenada de rutas absolutas de defaults para un perfil.
function Get-FtmSyncDefaultsList {
    param([Parameter(Mandatory)][string]$ProfileName, [Parameter(Mandatory)]$Config, [Parameter(Mandatory)][string]$GeneratedPath)
    $p = (Get-FtmSyncProfiles).Profiles[$ProfileName]
    if (-not $p) { throw "Perfil desconocido: $ProfileName" }
    $console = if ($Config.Console -eq 'uart0') { 'console_uart0.defaults' } else { 'console_usb_serial_jtag.defaults' }
    @(
        (Join-Path $script:ProfilesDir 'fts_common.defaults'),
        (Join-Path $script:ProfilesDir $p.Defaults),
        (Join-Path $script:ProfilesDir $console),
        $GeneratedPath
    )
}

# Compara el SHA-256 de cada archivo contra UPSTREAM_MANIFEST.json y detecta archivos de mas.
function Test-FtmSyncUpstreamIntegrity {
    param([string]$UpstreamDir = $script:Upstream)
    $man = Get-Content -Raw -LiteralPath (Join-Path $script:Root 'UPSTREAM_MANIFEST.json') | ConvertFrom-Json
    $problems = New-Object System.Collections.Generic.List[string]
    $expected = @{}
    foreach ($f in $man.files) { $expected[$f.path] = $f }
    foreach ($f in $man.files) {
        $fp = Join-Path $UpstreamDir ($f.path -replace '/', '\')
        if (-not (Test-Path -LiteralPath $fp)) { $problems.Add("falta: $($f.path)"); continue }
        $h = (Get-FileHash -Algorithm SHA256 -LiteralPath $fp).Hash.ToLowerInvariant()
        if ($h -ne $f.sha256) { $problems.Add("sha256 distinto: $($f.path)") }
    }
    $base = (Resolve-Path -LiteralPath $UpstreamDir).Path.TrimEnd('\') + '\'
    Get-ChildItem -LiteralPath $UpstreamDir -Recurse -File -Force | ForEach-Object {
        $rel = $_.FullName.Substring($base.Length) -replace '\\', '/'
        if (-not $expected.ContainsKey($rel)) { $problems.Add("archivo no listado en el manifiesto: $rel") }
    }
    [pscustomobject]@{ FileCount = @($man.files).Count; Problems = $problems.ToArray(); Manifest = $man }
}

# Activa el entorno ESP-IDF ya instalado si idf.py no esta disponible. No instala nada.
function Initialize-FtmSyncIdf {
    param([Parameter(Mandatory)]$Config)
    if (-not $env:IDF_PATH -or -not (Get-Command python -ErrorAction SilentlyContinue)) {
        if ($Config.IdfPath) {
            $exp = Join-Path $Config.IdfPath 'export.ps1'
            if (-not (Test-Path -LiteralPath $exp)) { throw "No existe $exp. IdfPath debe apuntar a la carpeta de ESP-IDF v5.5.1 ya instalada." }
            . $exp | Out-Null
        }
    }
    if (-not $env:IDF_PATH) { throw 'ESP-IDF no esta activo (IDF_PATH vacio). Abrir "ESP-IDF 5.5 PowerShell" o completar IdfPath en la config. Este paquete no instala ESP-IDF.' }
    $idfpy = Join-Path $env:IDF_PATH 'tools\idf.py'
    if (-not (Test-Path -LiteralPath $idfpy)) { throw "No se encuentra $idfpy" }
    $ver = (& python $idfpy --version 2>&1 | Out-String).Trim()
    if ($ver -notmatch 'v5\.5(\.|-|\s|$)') { throw "ESP-IDF detectado: '$ver'. Este experimento esta fijado a v5.5.1 (esp_wifi_internal_get_mac_clock_time existe desde v5.5; no esta en v5.4.2). No se continua." }
    if ($ver -notmatch 'v5\.5\.1') { Write-Warning "ESP-IDF detectado '$ver'; el pin verificado es v5.5.1. Otras 5.5.x tienen la API pero no fueron probadas aca." }
    $idfpy
}

# Copia upstream/ a <WorkRoot>/fts (pristino queda intacto) y verifica integridad antes y despues.
function Initialize-FtmSyncWorkspace {
    param([Parameter(Mandatory)]$Config)
    $integ = Test-FtmSyncUpstreamIntegrity
    if ($integ.Problems.Count) { throw "upstream/ no coincide con el manifiesto:`n  " + ($integ.Problems -join "`n  ") }
    $wr = Get-FtmSyncWorkRoot $Config
    $src = Join-Path $wr 'fts'
    New-Item -ItemType Directory -Force -Path $src | Out-Null
    # /MIR no borra managed_components ni dependencies.lock porque se excluyen (/XD /XF).
    $null = robocopy $script:Upstream $src /MIR /XD managed_components /XF dependencies.lock /NFL /NDL /NJH /NJS /NP
    if ($LASTEXITCODE -ge 8) { throw "robocopy fallo ($LASTEXITCODE)" }
    $global:LASTEXITCODE = 0
    $src
}
