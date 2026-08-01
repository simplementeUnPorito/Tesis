param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot 'Tesis_DevKits.pretty')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$invariantCulture = [System.Globalization.CultureInfo]::InvariantCulture

function Format-Number {
    param([double]$Value)

    return $Value.ToString('0.###', $invariantCulture)
}

function Get-StableUuid {
    param([string]$Seed)

    $hashAlgorithm = [System.Security.Cryptography.MD5]::Create()
    try {
        $bytes = $hashAlgorithm.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($Seed))
    }
    finally {
        $hashAlgorithm.Dispose()
    }

    $bytes[6] = ($bytes[6] -band 0x0F) -bor 0x30
    $bytes[8] = ($bytes[8] -band 0x3F) -bor 0x80
    return [guid]::new($bytes).ToString()
}

function Add-FootprintProperty {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$FootprintName,
        [string]$Name,
        [string]$Value,
        [double]$X,
        [double]$Y,
        [string]$Layer,
        [switch]$Hidden
    )

    $Lines.Add(('  (property "{0}" "{1}"' -f $Name, $Value))
    $Lines.Add(('    (at {0} {1} 0)' -f (Format-Number $X), (Format-Number $Y)))
    $Lines.Add(('    (layer "{0}")' -f $Layer))
    if ($Hidden) {
        $Lines.Add('    (hide yes)')
    }
    $Lines.Add(('    (uuid "{0}")' -f (Get-StableUuid "$FootprintName/property/$Name")))
    $Lines.Add('    (effects')
    $Lines.Add('      (font')
    $Lines.Add('        (size 1 1)')
    $Lines.Add('        (thickness 0.15)')
    $Lines.Add('      )')
    $Lines.Add('    )')
    $Lines.Add('  )')
}

function Add-Line {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$FootprintName,
        [string]$Key,
        [double]$X1,
        [double]$Y1,
        [double]$X2,
        [double]$Y2,
        [string]$Layer,
        [double]$Width
    )

    $Lines.Add('  (fp_line')
    $Lines.Add(('    (start {0} {1})' -f (Format-Number $X1), (Format-Number $Y1)))
    $Lines.Add(('    (end {0} {1})' -f (Format-Number $X2), (Format-Number $Y2)))
    $Lines.Add('    (stroke')
    $Lines.Add(('      (width {0})' -f (Format-Number $Width)))
    $Lines.Add('      (type solid)')
    $Lines.Add('    )')
    $Lines.Add(('    (layer "{0}")' -f $Layer))
    $Lines.Add(('    (uuid "{0}")' -f (Get-StableUuid "$FootprintName/line/$Key/$Layer")))
    $Lines.Add('  )')
}

function Add-Rectangle {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$FootprintName,
        [string]$Key,
        [double]$X1,
        [double]$Y1,
        [double]$X2,
        [double]$Y2,
        [string]$Layer,
        [double]$Width
    )

    Add-Line -Lines $Lines -FootprintName $FootprintName -Key "$Key/top" -X1 $X1 -Y1 $Y1 -X2 $X2 -Y2 $Y1 -Layer $Layer -Width $Width
    Add-Line -Lines $Lines -FootprintName $FootprintName -Key "$Key/right" -X1 $X2 -Y1 $Y1 -X2 $X2 -Y2 $Y2 -Layer $Layer -Width $Width
    Add-Line -Lines $Lines -FootprintName $FootprintName -Key "$Key/bottom" -X1 $X2 -Y1 $Y2 -X2 $X1 -Y2 $Y2 -Layer $Layer -Width $Width
    Add-Line -Lines $Lines -FootprintName $FootprintName -Key "$Key/left" -X1 $X1 -Y1 $Y2 -X2 $X1 -Y2 $Y1 -Layer $Layer -Width $Width
}

function Add-Pad {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$FootprintName,
        [string]$Number,
        [double]$X,
        [double]$Y,
        [switch]$PinOne
    )

    $shape = if ($PinOne) { 'rect' } else { 'circle' }
    $Lines.Add(('  (pad "{0}" thru_hole {1}' -f $Number, $shape))
    $Lines.Add(('    (at {0} {1})' -f (Format-Number $X), (Format-Number $Y)))
    $Lines.Add('    (size 1.8 1.8)')
    $Lines.Add('    (drill 1)')
    $Lines.Add('    (layers "*.Cu" "*.Mask")')
    $Lines.Add('    (remove_unused_layers no)')
    $Lines.Add(('    (uuid "{0}")' -f (Get-StableUuid "$FootprintName/pad/$Number")))
    $Lines.Add('  )')
}

function New-FootprintHeader {
    param(
        [string]$Name,
        [string]$Description,
        [string]$Tags,
        [double]$ReferenceX,
        [double]$ReferenceY,
        [double]$ValueX,
        [double]$ValueY
    )

    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add(('(footprint "{0}"' -f $Name))
    $lines.Add('  (version 20260206)')
    $lines.Add('  (generator "generate_devkit_footprints.ps1")')
    $lines.Add('  (generator_version "1.0")')
    $lines.Add('  (layer "F.Cu")')
    $lines.Add(('  (descr "{0}")' -f $Description))
    $lines.Add(('  (tags "{0}")' -f $Tags))
    Add-FootprintProperty -Lines $lines -FootprintName $Name -Name 'Reference' -Value 'REF**' -X $ReferenceX -Y $ReferenceY -Layer 'F.SilkS'
    Add-FootprintProperty -Lines $lines -FootprintName $Name -Name 'Value' -Value $Name -X $ValueX -Y $ValueY -Layer 'F.Fab'
    Add-FootprintProperty -Lines $lines -FootprintName $Name -Name 'Datasheet' -Value '' -X 0 -Y 0 -Layer 'F.Fab' -Hidden
    Add-FootprintProperty -Lines $lines -FootprintName $Name -Name 'Description' -Value '' -X 0 -Y 0 -Layer 'F.Fab' -Hidden
    $lines.Add('  (attr through_hole)')
    $lines.Add('  (duplicate_pad_numbers_are_jumpers no)')
    Write-Output -NoEnumerate $lines
}

function Write-Footprint {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$Name
    )

    $Lines.Add(')')
    $path = Join-Path $OutputDirectory "$Name.kicad_mod"
    [System.IO.File]::WriteAllLines($path, $Lines, [System.Text.UTF8Encoding]::new($false))
    Write-Output "Generated $path"
}

if (-not (Test-Path -LiteralPath $OutputDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
}

# CY8CKIT-059 official Rev. 06 Gerber:
# - 2.54 mm pin pitch
# - 20.32 mm between J1 and J2
# - J1.1/J2.1 are at the USB end
# - target-board outline is 68.58 x 24.13 mm after snapping
# The attached KitProg outline is retained on F.Fab so the carrier can reserve it.
$psocName = 'CY8CKIT-059_Target_J1_J2'
$psocLines = New-FootprintHeader `
    -Name $psocName `
    -Description 'CY8CKIT-059 target-board carrier footprint, J1/J2 1x26 at 2.54 mm pitch and 20.32 mm row spacing. Full attached-KitProg clearance shown on F.Fab.' `
    -Tags 'PSoC 5LP CY8CKIT-059 carrier module' `
    -ReferenceX -31.75 `
    -ReferenceY -3.5 `
    -ValueX -31.75 `
    -ValueY 25.5

# Target board: pin 1 is 2.54 mm from the USB-end edge; pin 26 is 2.54 mm
# from the snap edge. The official full-board outline extends 106.35 mm left.
Add-Rectangle -Lines $psocLines -FootprintName $psocName -Key 'target-fab' -X1 -66.04 -Y1 -1.905 -X2 2.54 -Y2 22.225 -Layer 'F.Fab' -Width 0.1
Add-Rectangle -Lines $psocLines -FootprintName $psocName -Key 'full-kit-fab' -X1 -106.35 -Y1 -1.905 -X2 2.54 -Y2 22.225 -Layer 'F.Fab' -Width 0.1
Add-Line -Lines $psocLines -FootprintName $psocName -Key 'snap-line' -X1 -66.04 -Y1 -1.905 -X2 -66.04 -Y2 22.225 -Layer 'F.Fab' -Width 0.2
Add-Rectangle -Lines $psocLines -FootprintName $psocName -Key 'full-kit-courtyard' -X1 -106.85 -Y1 -2.405 -X2 3.04 -Y2 22.725 -Layer 'F.CrtYd' -Width 0.05
Add-Line -Lines $psocLines -FootprintName $psocName -Key 'silk-top' -X1 -66.04 -Y1 -2.1 -X2 2.54 -Y2 -2.1 -Layer 'F.SilkS' -Width 0.12
Add-Line -Lines $psocLines -FootprintName $psocName -Key 'silk-right' -X1 2.74 -Y1 -1.905 -X2 2.74 -Y2 22.225 -Layer 'F.SilkS' -Width 0.12
Add-Line -Lines $psocLines -FootprintName $psocName -Key 'silk-bottom' -X1 2.54 -Y1 22.42 -X2 -66.04 -Y2 22.42 -Layer 'F.SilkS' -Width 0.12
Add-Line -Lines $psocLines -FootprintName $psocName -Key 'silk-snap' -X1 -66.24 -Y1 -1.905 -X2 -66.24 -Y2 22.225 -Layer 'F.SilkS' -Width 0.12
for ($index = 0; $index -lt 26; $index++) {
    $x = -$index * 2.54
    Add-Pad -Lines $psocLines -FootprintName $psocName -Number "J1.$($index + 1)" -X $x -Y 0 -PinOne:($index -eq 0)
    Add-Pad -Lines $psocLines -FootprintName $psocName -Number "J2.$($index + 1)" -X $x -Y 20.32 -PinOne:($index -eq 0)
}
Write-Footprint -Lines $psocLines -Name $psocName

# ESP32-DevKitC V4 official dimensions:
# - board 27.94 x 48.26 mm
# - two 1x19 headers, 2.54 mm pitch, 25.40 mm row spacing
# - J2.1/J3.1 are at the antenna/module end; USB is at the pin-19 end.
$espName = 'ESP32-DevKitC_V4_38Pin'
$espLines = New-FootprintHeader `
    -Name $espName `
    -Description 'Espressif ESP32-DevKitC V4 38-pin WROOM/SOLO carrier footprint, official 27.94 x 48.26 mm board and 25.40 mm header-row spacing.' `
    -Tags 'ESP32 DevKitC V4 WROOM 38 pin carrier module' `
    -ReferenceX 12.7 `
    -ReferenceY -3 `
    -ValueX 12.7 `
    -ValueY 49.8
Add-Rectangle -Lines $espLines -FootprintName $espName -Key 'board-fab' -X1 -1.27 -Y1 -1.27 -X2 26.67 -Y2 46.99 -Layer 'F.Fab' -Width 0.1
Add-Rectangle -Lines $espLines -FootprintName $espName -Key 'board-courtyard' -X1 -1.77 -Y1 -1.77 -X2 27.17 -Y2 47.49 -Layer 'F.CrtYd' -Width 0.05
Add-Line -Lines $espLines -FootprintName $espName -Key 'silk-top' -X1 -1.27 -Y1 -1.47 -X2 26.67 -Y2 -1.47 -Layer 'F.SilkS' -Width 0.12
Add-Line -Lines $espLines -FootprintName $espName -Key 'silk-right' -X1 26.87 -Y1 -1.27 -X2 26.87 -Y2 46.99 -Layer 'F.SilkS' -Width 0.12
Add-Line -Lines $espLines -FootprintName $espName -Key 'silk-bottom' -X1 26.67 -Y1 47.19 -X2 -1.27 -Y2 47.19 -Layer 'F.SilkS' -Width 0.12
Add-Line -Lines $espLines -FootprintName $espName -Key 'silk-left' -X1 -1.47 -Y1 46.99 -X2 -1.47 -Y2 -1.27 -Layer 'F.SilkS' -Width 0.12
for ($index = 0; $index -lt 19; $index++) {
    $y = $index * 2.54
    Add-Pad -Lines $espLines -FootprintName $espName -Number "J2.$($index + 1)" -X 0 -Y $y -PinOne:($index -eq 0)
    Add-Pad -Lines $espLines -FootprintName $espName -Number "J3.$($index + 1)" -X 25.4 -Y $y -PinOne:($index -eq 0)
}
Write-Footprint -Lines $espLines -Name $espName
