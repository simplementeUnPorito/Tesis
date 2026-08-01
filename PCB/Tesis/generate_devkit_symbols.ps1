param(
    [string]$OutputDirectory = $PSScriptRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$invariantCulture = [System.Globalization.CultureInfo]::InvariantCulture

function Format-Number {
    param([double]$Value)

    return $Value.ToString('0.##', $invariantCulture)
}

function Escape-KiCadString {
    param([string]$Value)

    return $Value.Replace('\', '\\').Replace('"', '\"')
}

function Convert-PinSpec {
    param([string[]]$Specs)

    return @(
        foreach ($spec in $Specs) {
            $fields = $spec.Split('|')
            if ($fields.Count -ne 3) {
                throw "Invalid pin specification: $spec"
            }

            [pscustomobject]@{
                Number = $fields[0]
                Name   = $fields[1]
                Type   = $fields[2]
            }
        }
    )
}

function Add-Property {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$Name,
        [string]$Value,
        [double]$X,
        [double]$Y,
        [string[]]$Justify = @(),
        [switch]$Hidden
    )

    $Lines.Add(('    (property "{0}" "{1}"' -f (Escape-KiCadString $Name), (Escape-KiCadString $Value)))
    $Lines.Add(('      (at {0} {1} 0)' -f (Format-Number $X), (Format-Number $Y)))
    $Lines.Add('      (show_name no)')
    $Lines.Add('      (do_not_autoplace no)')
    if ($Hidden) {
        $Lines.Add('      (hide yes)')
    }
    $Lines.Add('      (effects')
    $Lines.Add('        (font')
    $Lines.Add('          (size 1.27 1.27)')
    $Lines.Add('        )')
    if ($Justify.Count -gt 0) {
        $Lines.Add(('        (justify {0})' -f ($Justify -join ' ')))
    }
    $Lines.Add('      )')
    $Lines.Add('    )')
}

function Add-Pin {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [pscustomobject]$Pin,
        [string]$Side,
        [int]$Index,
        [int]$PinCount
    )

    $pitch = 2.54
    $y = ((($PinCount - 1) / 2.0) - $Index) * $pitch
    if ($Side -eq 'left') {
        $x = -17.78
        $angle = 0
    }
    else {
        $x = 17.78
        $angle = 180
    }

    $Lines.Add(('      (pin {0} line' -f $Pin.Type))
    $Lines.Add(('        (at {0} {1} {2})' -f (Format-Number $x), (Format-Number $y), $angle))
    $Lines.Add('        (length 2.54)')
    $Lines.Add(('        (name "{0}"' -f (Escape-KiCadString $Pin.Name)))
    $Lines.Add('          (effects')
    $Lines.Add('            (font')
    $Lines.Add('              (size 1.27 1.27)')
    $Lines.Add('            )')
    $Lines.Add('          )')
    $Lines.Add('        )')
    $Lines.Add(('        (number "{0}"' -f (Escape-KiCadString $Pin.Number)))
    $Lines.Add('          (effects')
    $Lines.Add('            (font')
    $Lines.Add('              (size 1.27 1.27)')
    $Lines.Add('            )')
    $Lines.Add('          )')
    $Lines.Add('        )')
    $Lines.Add('      )')
}

function Add-DevKitSymbol {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$Name,
        [string]$Description,
        [string]$Datasheet,
        [string]$Keywords,
        [string]$FootprintFilters,
        [string]$DefaultFootprint,
        [object[]]$LeftPins,
        [object[]]$RightPins
    )

    if ($LeftPins.Count -ne $RightPins.Count) {
        throw "$Name must have the same number of pins on each physical header."
    }

    $allNumbers = @($LeftPins.Number) + @($RightPins.Number)
    $duplicateNumbers = @($allNumbers | Group-Object | Where-Object Count -gt 1)
    if ($duplicateNumbers.Count -gt 0) {
        throw "$Name has duplicate pin numbers: $($duplicateNumbers.Name -join ', ')"
    }

    $halfHeight = (($LeftPins.Count - 1) / 2.0) * 2.54 + 1.27
    $referenceY = $halfHeight + 1.27
    $valueY = -$halfHeight - 1.27

    $Lines.Add(('  (symbol "{0}"' -f (Escape-KiCadString $Name)))
    $Lines.Add('    (exclude_from_sim no)')
    $Lines.Add('    (in_bom yes)')
    $Lines.Add('    (on_board yes)')
    $Lines.Add('    (in_pos_files yes)')
    $Lines.Add('    (duplicate_pin_numbers_are_jumpers no)')
    Add-Property -Lines $Lines -Name 'Reference' -Value 'A' -X -15.24 -Y $referenceY -Justify @('left', 'bottom')
    Add-Property -Lines $Lines -Name 'Value' -Value $Name -X -15.24 -Y $valueY -Justify @('left', 'top')
    Add-Property -Lines $Lines -Name 'Footprint' -Value $DefaultFootprint -X 0 -Y 0 -Hidden
    Add-Property -Lines $Lines -Name 'Datasheet' -Value $Datasheet -X 0 -Y 0 -Hidden
    Add-Property -Lines $Lines -Name 'Description' -Value $Description -X 0 -Y 0 -Hidden
    Add-Property -Lines $Lines -Name 'ki_keywords' -Value $Keywords -X 0 -Y 0 -Hidden
    Add-Property -Lines $Lines -Name 'ki_fp_filters' -Value $FootprintFilters -X 0 -Y 0 -Hidden
    $Lines.Add(('    (symbol "{0}_0_1"' -f (Escape-KiCadString $Name)))
    $Lines.Add('      (rectangle')
    $Lines.Add(('        (start -15.24 {0})' -f (Format-Number $halfHeight)))
    $Lines.Add(('        (end 15.24 {0})' -f (Format-Number (-$halfHeight))))
    $Lines.Add('        (stroke')
    $Lines.Add('          (width 0)')
    $Lines.Add('          (type default)')
    $Lines.Add('        )')
    $Lines.Add('        (fill')
    $Lines.Add('          (type background)')
    $Lines.Add('        )')
    $Lines.Add('      )')
    $Lines.Add('    )')
    $Lines.Add(('    (symbol "{0}_1_1"' -f (Escape-KiCadString $Name)))
    for ($index = 0; $index -lt $LeftPins.Count; $index++) {
        Add-Pin -Lines $Lines -Pin $LeftPins[$index] -Side 'left' -Index $index -PinCount $LeftPins.Count
    }
    for ($index = 0; $index -lt $RightPins.Count; $index++) {
        Add-Pin -Lines $Lines -Pin $RightPins[$index] -Side 'right' -Index $index -PinCount $RightPins.Count
    }
    $Lines.Add('    )')
    $Lines.Add('  )')
}

$psocJ1 = Convert-PinSpec @(
    'J1.1|P2.0|bidirectional',
    'J1.2|P2.1 / LED|bidirectional',
    'J1.3|P2.2 / SW|bidirectional',
    'J1.4|P2.3|bidirectional',
    'J1.5|P2.4|bidirectional',
    'J1.6|P2.5|bidirectional',
    'J1.7|P2.6|bidirectional',
    'J1.8|P2.7|bidirectional',
    'J1.9|P12.7 / UART_TX|bidirectional',
    'J1.10|P12.6 / UART_RX|bidirectional',
    'J1.11|P12.5|bidirectional',
    'J1.12|P12.4|bidirectional',
    'J1.13|P12.3|bidirectional',
    'J1.14|P12.2|bidirectional',
    'J1.15|P12.1 / I2C_SDA|bidirectional',
    'J1.16|P12.0 / I2C_SCL|bidirectional',
    'J1.17|P1.0|bidirectional',
    'J1.18|P1.1|bidirectional',
    'J1.19|P1.2|bidirectional',
    'J1.20|P1.3|bidirectional',
    'J1.21|P1.4|bidirectional',
    'J1.22|P1.5|bidirectional',
    'J1.23|P1.6|bidirectional',
    'J1.24|P1.7|bidirectional',
    'J1.25|GND|power_in',
    'J1.26|VDDIO|power_in'
)

$psocJ2 = Convert-PinSpec @(
    'J2.1|VDD|power_in',
    'J2.2|GND|power_in',
    'J2.3|RESET|input',
    'J2.4|P0.7|bidirectional',
    'J2.5|P0.6|bidirectional',
    'J2.6|P0.5|bidirectional',
    'J2.7|P0.4 / BYPASS CAP|bidirectional',
    'J2.8|P0.3 / BYPASS CAP|bidirectional',
    'J2.9|P0.2 / BYPASS CAP|bidirectional',
    'J2.10|P0.1|bidirectional',
    'J2.11|P0.0|bidirectional',
    'J2.12|P15.5|bidirectional',
    'J2.13|P15.4 / CMOD|bidirectional',
    'J2.14|P15.3 / XTAL_IN|bidirectional',
    'J2.15|P15.2 / XTAL_OUT|bidirectional',
    'J2.16|P15.1|bidirectional',
    'J2.17|P15.0|bidirectional',
    'J2.18|P3.7|bidirectional',
    'J2.19|P3.6|bidirectional',
    'J2.20|P3.5|bidirectional',
    'J2.21|P3.4|bidirectional',
    'J2.22|P3.3|bidirectional',
    'J2.23|P3.2 / BYPASS CAP|bidirectional',
    'J2.24|P3.1|bidirectional',
    'J2.25|P3.0|bidirectional',
    'J2.26|GND|power_in'
)

$espJ2 = Convert-PinSpec @(
    'J2.1|3V3|power_in',
    'J2.2|EN|input',
    'J2.3|GPIO36 / VP|input',
    'J2.4|GPIO39 / VN|input',
    'J2.5|GPIO34|input',
    'J2.6|GPIO35|input',
    'J2.7|GPIO32|bidirectional',
    'J2.8|GPIO33|bidirectional',
    'J2.9|GPIO25|bidirectional',
    'J2.10|GPIO26|bidirectional',
    'J2.11|GPIO27|bidirectional',
    'J2.12|GPIO14|bidirectional',
    'J2.13|GPIO12|bidirectional',
    'J2.14|GND|power_in',
    'J2.15|GPIO13|bidirectional',
    'J2.16|GPIO9 / D2 [FLASH]|bidirectional',
    'J2.17|GPIO10 / D3 [FLASH]|bidirectional',
    'J2.18|GPIO11 / CMD [FLASH]|bidirectional',
    'J2.19|5V|power_in'
)

$espJ3 = Convert-PinSpec @(
    'J3.1|GND|power_in',
    'J3.2|GPIO23|bidirectional',
    'J3.3|GPIO22|bidirectional',
    'J3.4|GPIO1 / TX|bidirectional',
    'J3.5|GPIO3 / RX|bidirectional',
    'J3.6|GPIO21|bidirectional',
    'J3.7|GND|power_in',
    'J3.8|GPIO19|bidirectional',
    'J3.9|GPIO18|bidirectional',
    'J3.10|GPIO5|bidirectional',
    'J3.11|GPIO17|bidirectional',
    'J3.12|GPIO16|bidirectional',
    'J3.13|GPIO4|bidirectional',
    'J3.14|GPIO0 / BOOT|bidirectional',
    'J3.15|GPIO2|bidirectional',
    'J3.16|GPIO15|bidirectional',
    'J3.17|GPIO8 / D1 [FLASH]|bidirectional',
    'J3.18|GPIO7 / D0 [FLASH]|bidirectional',
    'J3.19|GPIO6 / CLK [FLASH]|bidirectional'
)

$libraryLines = [System.Collections.Generic.List[string]]::new()
$libraryLines.Add('(kicad_symbol_lib')
$libraryLines.Add('  (version 20251024)')
$libraryLines.Add('  (generator "generate_devkit_symbols.ps1")')
$libraryLines.Add('  (generator_version "1.0")')

Add-DevKitSymbol `
    -Lines $libraryLines `
    -Name 'CY8CKIT-059_PSoC_5LP' `
    -Description 'Infineon CY8CKIT-059 PSoC 5LP prototyping kit target board, CY8C5888LTI-LP097 as selected by this project, with J1/J2 carrier headers.' `
    -Datasheet 'https://www.infineon.com/assets/row/public/documents/30/44/infineon-cy8ckit-059-psoc-5lp-prototyping-kit-guide-usermanual-en.pdf?fileId=8ac78c8c7d0d8da4017d0ef981770f63' `
    -Keywords 'PSoC 5LP CY8CKIT-059 CY8C5888LTI-LP097 development kit module' `
    -FootprintFilters 'Tesis*CY8CKIT*059*' `
    -DefaultFootprint 'Tesis_DevKits:CY8CKIT-059_Target_J1_J2' `
    -LeftPins $psocJ1 `
    -RightPins $psocJ2

Add-DevKitSymbol `
    -Lines $libraryLines `
    -Name 'ESP32-DevKitC_V4_WROOM_38Pin' `
    -Description 'Espressif ESP32-DevKitC V4, 38-pin WROOM/SOLO variant. GPIO6-GPIO11 are marked as internal-flash pins; GPIO16/GPIO17 are not available on WROVER variants.' `
    -Datasheet 'https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html' `
    -Keywords 'ESP32 DevKitC V4 WROOM 38 pin development kit module' `
    -FootprintFilters 'Tesis*ESP32*DevKitC*V4*' `
    -DefaultFootprint 'Tesis_DevKits:ESP32-DevKitC_V4_38Pin' `
    -LeftPins $espJ2 `
    -RightPins $espJ3

$libraryLines.Add(')')

if (-not (Test-Path -LiteralPath $OutputDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}

$libraryPath = Join-Path $OutputDirectory 'Tesis_DevKits.kicad_sym'
[System.IO.File]::WriteAllLines(
    $libraryPath,
    $libraryLines,
    [System.Text.UTF8Encoding]::new($false)
)

Write-Output "Generated $libraryPath"
Write-Output "CY8CKIT-059_PSoC_5LP: $($psocJ1.Count + $psocJ2.Count) pins"
Write-Output "ESP32-DevKitC_V4_WROOM_38Pin: $($espJ2.Count + $espJ3.Count) pins"
