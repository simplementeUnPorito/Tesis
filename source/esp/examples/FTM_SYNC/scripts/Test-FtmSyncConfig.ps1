<#
.SYNOPSIS
  Verificacion ESTATICA del paquete FTM_SYNC (no compila, no toca hardware, no necesita ESP-IDF).
.DESCRIPTION
  Comprueba: integridad del snapshot upstream contra el manifiesto; que los simbolos CONFIG_FTS_*
  de los perfiles existan en los Kconfig de upstream; coherencia de rol/modo/MQTT/consola del
  sdkconfig resultante (fusion "el ultimo gana", como SDKCONFIG_DEFAULTS); max_connection del AP
  de upstream frente a la cantidad de seguidores; validaciones de pines; sintaxis de los scripts;
  y las ordenes de compilacion/flasheo en modo -DryRun.
  Sale con codigo 1 si algo falla.
#>
[CmdletBinding()]
param([string]$ConfigPath)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'FtmSync.Common.ps1')

$fails = New-Object System.Collections.Generic.List[string]
function Check([string]$name, [bool]$ok, [string]$detail = '') {
    if ($ok) { Write-Host "[ OK ] $name" }
    else { Write-Host "[FAIL] $name $detail" -ForegroundColor Red; $script:fails.Add($name) }
}
function Merge-Defaults([string[]]$files) {
    $m = [ordered]@{}
    foreach ($f in $files) {
        foreach ($line in (Get-Content -LiteralPath $f)) {
            if ($line -match '^\s*CONFIG_([A-Za-z0-9_]+)=(.*)$') { $m[$Matches[1]] = $Matches[2].Trim() }
            elseif ($line -match '^\s*#\s*CONFIG_([A-Za-z0-9_]+) is not set') { $m[$Matches[1]] = 'n' }
        }
    }
    $m
}
function IsOn($m, $k) { $m.Contains($k) -and $m[$k] -eq 'y' }

# 1) Integridad del snapshot
$integ = Test-FtmSyncUpstreamIntegrity
Check "upstream/ coincide con UPSTREAM_MANIFEST.json ($($integ.FileCount) archivos, SHA-256)" ($integ.Problems.Count -eq 0) ($integ.Problems -join '; ')
Check 'manifiesto: commit fijado y sin archivos upstream modificados' (($integ.Manifest.commit -match '^[0-9a-f]{40}$') -and (@($integ.Manifest.modifiedUpstreamFiles).Count -eq 0))
Check 'LICENSE de upstream presente' (Test-Path -LiteralPath (Join-Path $script:Upstream 'LICENSE'))

# 2) Simbolos Kconfig
$kconf = (Get-Content -Raw -LiteralPath (Join-Path $script:Upstream 'main\Kconfig.projbuild')) + "`n" + (Get-Content -Raw -LiteralPath (Join-Path $script:Upstream 'components\dtr\Kconfig'))
$known = @{}
[regex]::Matches($kconf, '(?m)^\s*config\s+([A-Z0-9_]+)') | ForEach-Object { $known[$_.Groups[1].Value] = $true }
$cfg = Get-FtmSyncConfig -Path $ConfigPath -AllowExample
$tmp = Join-Path ([IO.Path]::GetTempPath()) ('ftmsync_test_' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $tmp | Out-Null
try {
    $gen = Join-Path $tmp 'gen.defaults'
    [IO.File]::WriteAllText($gen, (New-FtmSyncGeneratedDefaults $cfg), [Text.UTF8Encoding]::new($false))
    $allFiles = @(Get-ChildItem -LiteralPath $script:ProfilesDir -Filter '*.defaults' | ForEach-Object FullName) + $gen
    $unknown = @()
    foreach ($f in $allFiles) {
        foreach ($line in (Get-Content -LiteralPath $f)) {
            if ($line -match '^\s*CONFIG_(FTS_[A-Z0-9_]+|DTR_[A-Z0-9_]+)=') { if (-not $known[$Matches[1]]) { $unknown += "$([IO.Path]::GetFileName($f)):$($Matches[1])" } }
        }
    }
    Check 'todos los CONFIG_FTS_*/DTR_* de los perfiles existen en el Kconfig de upstream' ($unknown.Count -eq 0) ($unknown -join ', ')

    # 3) Fusion por perfil, para las 4 combinaciones de config (LED on/off x consola)
    $variants = @(
        @{ n = 'config-actual'; c = $cfg },
        @{ n = 'led-on/uart0'; c = ($cfg.Clone() + @{}) },
        @{ n = 'led-off/jtag'; c = ($cfg.Clone() + @{}) },
        @{ n = 'led-ws2812/jtag'; c = ($cfg.Clone() + @{}) }
    )
    $variants[3].c.LedEnabled = $true; $variants[3].c.LedType = 'ws2812'; $variants[3].c.LedGpio = 48; $variants[3].c.Console = 'usb-serial-jtag'
    $variants[1].c.LedEnabled = $true; $variants[1].c.LedType = 'gpio'; $variants[1].c.LedGpio = 4; $variants[1].c.Console = 'uart0'
    $variants[2].c.LedEnabled = $false; $variants[2].c.Console = 'usb-serial-jtag'
    foreach ($v in $variants) {
        $g = Join-Path $tmp ("g_" + $v.n.Replace('/', '_') + '.defaults')
        [IO.File]::WriteAllText($g, (New-FtmSyncGeneratedDefaults $v.c), [Text.UTF8Encoding]::new($false))
        foreach ($p in @('ref', 'follower')) {
            $m = Merge-Defaults (Get-FtmSyncDefaultsList -ProfileName $p -Config $v.c -GeneratedPath $g)
            $tag = "[$($v.n)/$p]"
            $wantMaster = ($p -eq 'ref')
            Check "$tag rol correcto (exactamente uno)" ((IsOn $m 'FTS_ROLE_MASTER') -eq $wantMaster -and (IsOn $m 'FTS_ROLE_SLAVE') -eq (-not $wantMaster))
            Check "$tag modo = AP interno, sin USB-NCM/AP externo" ((IsOn $m 'FTS_MODE_INTERNAL_AP') -and -not (IsOn $m 'FTS_MODE_USB_NCM') -and -not (IsOn $m 'FTS_MODE_EXTERNAL_AP'))
            Check "$tag MQTT apagado" (-not (IsOn $m 'FTS_MQTT_ENABLED'))
            Check "$tag FTM habilitado" (IsOn $m 'ESP_WIFI_FTM_ENABLE')
            Check "$tag pulso MCPWM en GPIO $($v.c.PulseGpio)" ((IsOn $m 'FTS_PULSE_MCPWM_GPIO_ENABLE') -and $m['FTS_PULSE_MCPWM_GPIO'] -eq "$($v.c.PulseGpio)")
            if ($v.c.LedEnabled) { Check "$tag LED tipo $($v.c.LedType) en GPIO $($v.c.LedGpio)" ((IsOn $m 'FTS_LED_ENABLED') -and $m['FTS_LED_GPIO'] -eq "$($v.c.LedGpio)" -and ((IsOn $m 'FTS_LED_WS2812') -eq ($v.c.LedType -eq 'ws2812'))) }
            else { Check "$tag LED apagado (no se toca ningun GPIO de LED)" (-not (IsOn $m 'FTS_LED_ENABLED')) }
            $uart = IsOn $m 'ESP_CONSOLE_UART_DEFAULT'; $jtag = IsOn $m 'ESP_CONSOLE_USB_SERIAL_JTAG'
            Check "$tag consola: exactamente una" ($uart -xor $jtag)
            Check "$tag consola coincide con la config ($($v.c.Console))" (($v.c.Console -eq 'uart0') -eq $uart)
            Check "$tag canal/ssid/clave propagados" (($m['FTS_AP_CHANNEL'] -eq "$($v.c.WifiChannel)") -and ($m['FTS_WIFI_SSID'] -eq "`"$($v.c.WifiSsid)`""))
        }
    }

    # 4) Validaciones de pines/config (casos que DEBEN fallar y que DEBEN pasar)
    $bad = $cfg.Clone(); $bad.PulseGpio = 7; $bad.LedEnabled = $true; $bad.LedGpio = 7
    Check 'LED en el mismo GPIO que el pulso se rechaza' ((Test-FtmSyncConfigValues $bad).Errors.Count -ge 1)
    $bad = $cfg.Clone(); $bad.PulseGpio = 49
    Check 'GPIO fuera de 0..48 se rechaza' ((Test-FtmSyncConfigValues $bad).Errors.Count -ge 1)
    $bad = $cfg.Clone(); $bad.PulseGpio = 19
    Check 'GPIO19 (USB nativo) genera advertencia' (@((Test-FtmSyncConfigValues $bad).Warnings -match 'GPIO19').Count -ge 1)
    $bad = $cfg.Clone(); $bad.WifiPassword = 'corta'
    $bad = $cfg.Clone(); $bad.LedEnabled = $true; $bad.LedGpio = 4; $bad.LedType = 'rgb'
    Check 'LedType desconocido se rechaza' ((Test-FtmSyncConfigValues $bad).Errors.Count -ge 1)
    Check 'clave WiFi < 8 caracteres se rechaza' ((Test-FtmSyncConfigValues $bad).Errors.Count -ge 1)
    $ok = Test-FtmSyncConfigValues $cfg
    Check 'configuracion actual sin errores' ($ok.Errors.Count -eq 0) ($ok.Errors -join '; ')
    $ok.Warnings | ForEach-Object { Write-Host "[AVISO] $_" -ForegroundColor Yellow }

    # 5) max_connection del AP del maestro en upstream
    $ftm = Get-Content -Raw -LiteralPath (Join-Path $script:Upstream 'components\ftm\ftm.c')
    $m = [regex]::Match($ftm, 'ftm_master_ap_init[\s\S]*?\.max_connection\s*=\s*(\d+)')
    $maxConn = if ($m.Success) { [int]$m.Groups[1].Value } else { -1 }
    $followers = @((Get-FtmSyncProfiles).Nodes.GetEnumerator() | Where-Object { $_.Value.Profile -eq 'follower' }).Count
    Check "AP del maestro: max_connection=$maxConn >= $followers seguidores (sin modificar upstream)" ($maxConn -ge $followers)
    Check 'AP del maestro con FTM responder activado' ($ftm -match '(?s)ftm_master_ap_init.*?\.ftm_responder\s*=\s*true')

    # 6) Mapa de nodos
    $pr = Get-FtmSyncProfiles
    $masters = @($pr.Nodes.GetEnumerator() | Where-Object { $pr.Profiles[$_.Value.Profile].Role -eq 'master' }).Count
    Check 'mapa de nodos: 1 referencia + 4 seguidores, perfiles definidos' (($masters -eq 1) -and ($followers -eq 4) -and (@($pr.Nodes.Values | Where-Object { -not $pr.Profiles[$_.Profile] }).Count -eq 0))
    Check 'archivos de perfil referenciados existen' (@($pr.Profiles.Values | Where-Object { -not (Test-Path (Join-Path $script:ProfilesDir $_.Defaults)) }).Count -eq 0)

    # 7) Sintaxis de scripts
    foreach ($s in Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.ps1') {
        $errs = $null; $tok = $null
        [void][System.Management.Automation.Language.Parser]::ParseFile($s.FullName, [ref]$tok, [ref]$errs)
        Check "sintaxis PowerShell: $($s.Name)" ($errs.Count -eq 0) (($errs | ForEach-Object Message) -join '; ')
    }

    # 8) Ordenes en modo DryRun (no ejecutan idf.py)
    $dry = Join-Path $tmp 'dry.psd1'
    $cfgText = (Get-Content -Raw -LiteralPath (Join-Path $script:Root 'config\experiment.example.psd1')) -replace 'BoardPinoutConfirmed = \$false', 'BoardPinoutConfirmed = $true' -replace "WorkRoot = ''", "WorkRoot = '$($tmp.Replace('\','\\'))\w'" -replace "REF = 'COM\?'", "REF = 'COM9'"
    [IO.File]::WriteAllText($dry, $cfgText)
    $o = & (Join-Path $PSScriptRoot 'Build-Firmware.ps1') -Profile all -ConfigPath $dry -DryRun 3>$null 6>&1 | Out-String
    Check 'Build-Firmware -DryRun: 2 ordenes, SDKCONFIG_DEFAULTS en orden y target esp32s3' (([regex]::Matches($o, '\[DryRun\]').Count -eq 2) -and ($o -match 'fts_common\.defaults;[^;]*fts_ref\.defaults;[^;]*console_[a-z_0-9]+\.defaults;[^;]*ref\.defaults') -and ($o -match 'IDF_TARGET=esp32s3'))
    $o = & (Join-Path $PSScriptRoot 'Flash-Node.ps1') -Node REF -ConfigPath $dry -DryRun 6>&1 | Out-String
    Check 'Flash-Node -DryRun (pinout confirmado, COM9): orden con perfil ref' (($o -match 'COM9') -and ($o -match 'build_ref'))
    $threw = $false; try { & (Join-Path $PSScriptRoot 'Flash-Node.ps1') -Node F1 -ConfigPath (Join-Path $script:Root 'config\experiment.example.psd1') -DryRun | Out-Null } catch { $threw = $true }
    Check 'Flash-Node se niega mientras BoardPinoutConfirmed=$false' $threw
}
finally { Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue }

if ($fails.Count) { Write-Host "`n$($fails.Count) verificacion(es) FALLARON." -ForegroundColor Red; exit 1 }
Write-Host "`nTodas las verificaciones estaticas pasaron. (No implica compilacion ni medicion en hardware.)"
