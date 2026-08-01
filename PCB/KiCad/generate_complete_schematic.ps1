[CmdletBinding()]
param(
    [string]$BasePath = (Join-Path $PSScriptRoot 'Tesis.kicad_sch'),
    [string]$OutputPath = (Join-Path $PSScriptRoot 'Tesis_complete.kicad_sch'),
    [string]$BaseProjectPath = (Join-Path $PSScriptRoot 'Tesis.kicad_pro'),
    [string]$OutputProjectPath = (Join-Path $PSScriptRoot 'Tesis_complete.kicad_pro')
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$deviceLibrary = 'D:\Program Files\KiCad\share\kicad\symbols\Device.kicad_sym'
$connectorLibrary = 'D:\Program Files\KiCad\share\kicad\symbols\Connector_Generic.kicad_sym'
$switchLibrary = 'D:\Program Files\KiCad\share\kicad\symbols\Switch.kicad_sym'
$powerLibrary = 'D:\Program Files\KiCad\share\kicad\symbols\power.kicad_sym'

$resistorFootprint = 'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal'
$capacitorFootprint = 'Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm'
$smallElectrolyticFootprint = 'Capacitor_THT:CP_Radial_D5.0mm_P2.00mm'
$largeElectrolyticFootprint = 'Capacitor_THT:CP_Radial_D10.0mm_P5.00mm'

function Format-Number {
    param([double]$Value)

    return [string]::Format(
        [System.Globalization.CultureInfo]::InvariantCulture,
        '{0:0.###}',
        $Value
    )
}

function ConvertTo-KicadString {
    param([string]$Value)

    return $Value.
        Replace('\', '\\').
        Replace('"', '\"').
        Replace("`r", '').
        Replace("`n", '\n')
}

function New-StableUuid {
    param([string]$Key)

    $md5 = [System.Security.Cryptography.MD5]::Create()
    try {
        $hash = $md5.ComputeHash([System.Text.Encoding]::UTF8.GetBytes("Tesis-complete:$Key"))
    }
    finally {
        $md5.Dispose()
    }

    $hex = -join ($hash | ForEach-Object { $_.ToString('x2') })
    return '{0}-{1}-{2}-{3}-{4}' -f
        $hex.Substring(0, 8),
        $hex.Substring(8, 4),
        $hex.Substring(12, 4),
        $hex.Substring(16, 4),
        $hex.Substring(20, 12)
}

function Get-SExpressionBlock {
    param(
        [string]$Text,
        [string]$Marker
    )

    $start = $Text.IndexOf($Marker, [System.StringComparison]::Ordinal)
    if ($start -lt 0) {
        throw "No se encontró el marcador S-expression: $Marker"
    }

    $depth = 0
    $inQuote = $false
    $escaped = $false

    for ($index = $start; $index -lt $Text.Length; $index++) {
        $character = $Text[$index]

        if ($inQuote) {
            if ($escaped) {
                $escaped = $false
            }
            elseif ($character -eq '\') {
                $escaped = $true
            }
            elseif ($character -eq '"') {
                $inQuote = $false
            }
            continue
        }

        if ($character -eq '"') {
            $inQuote = $true
        }
        elseif ($character -eq '(') {
            $depth++
        }
        elseif ($character -eq ')') {
            $depth--
            if ($depth -eq 0) {
                return [pscustomobject]@{
                    Start = $start
                    End = $index
                    Text = $Text.Substring($start, $index - $start + 1)
                }
            }
        }
    }

    throw "S-expression sin cierre para: $Marker"
}

function ConvertTo-EmbeddedSymbol {
    param(
        [string]$Block,
        [string]$SourceName,
        [string]$LibraryId
    )

    $renamed = $Block.Replace(
        "(symbol `"$SourceName`"",
        "(symbol `"$LibraryId`""
    )

    $lines = $renamed -split "`r?`n"
    $indented = foreach ($line in $lines) {
        if ($line.StartsWith("`t")) {
            "`t$line"
        }
        else {
            "`t`t$line"
        }
    }

    return $indented -join "`r`n"
}

function New-Label {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [ValidateSet('left', 'right')]
        [string]$Justify = 'left',
        [string]$Key = ''
    )

    if (-not $Key) {
        $Key = "$Name@$X,$Y"
    }

    $escapedName = ConvertTo-KicadString $Name
    $xText = Format-Number $X
    $yText = Format-Number $Y
    $uuid = New-StableUuid "label:$Key"

    return @"
	(label "$escapedName"
		(at $xText $yText 0)
		(effects
			(font
				(size 1 1)
			)
			(justify $Justify bottom)
		)
		(uuid "$uuid")
	)
"@
}

function New-TextNote {
    param(
        [string]$Text,
        [double]$X,
        [double]$Y,
        [double]$Size = 1.27,
        [string]$Key = ''
    )

    if (-not $Key) {
        $Key = "$Text@$X,$Y"
    }

    $escapedText = ConvertTo-KicadString $Text
    $xText = Format-Number $X
    $yText = Format-Number $Y
    $sizeText = Format-Number $Size
    $uuid = New-StableUuid "text:$Key"

    return @"
	(text "$escapedText"
		(exclude_from_sim no)
		(at $xText $yText 0)
		(effects
			(font
				(size $sizeText $sizeText)
			)
			(justify left bottom)
		)
		(uuid "$uuid")
	)
"@
}

function New-NoConnect {
    param(
        [double]$X,
        [double]$Y,
        [string]$Key
    )

    $xText = Format-Number $X
    $yText = Format-Number $Y
    $uuid = New-StableUuid "no-connect:$Key"

    return @"
	(no_connect
		(at $xText $yText)
		(uuid "$uuid")
	)
"@
}

function New-SymbolInstance {
    param(
        [string]$LibraryId,
        [string]$Reference,
        [string]$Value,
        [string]$Footprint,
        [string]$Description,
        [double]$X,
        [double]$Y,
        [int]$Rotation,
        [string[]]$Pins,
        [string]$RootUuid,
        [bool]$InBom = $true,
        [bool]$OnBoard = $true,
        [bool]$InPosFiles = $true
    )

    $libText = ConvertTo-KicadString $LibraryId
    $refText = ConvertTo-KicadString $Reference
    $valueText = ConvertTo-KicadString $Value
    $footprintText = ConvertTo-KicadString $Footprint
    $descriptionText = ConvertTo-KicadString $Description
    $xText = Format-Number $X
    $yText = Format-Number $Y
    $refY = Format-Number ($Y - 4.5)
    $valueY = Format-Number ($Y + 4.5)
    $symbolUuid = New-StableUuid "symbol:$Reference"
    $inBomText = if ($InBom) { 'yes' } else { 'no' }
    $onBoardText = if ($OnBoard) { 'yes' } else { 'no' }
    $inPosFilesText = if ($InPosFiles) { 'yes' } else { 'no' }

    $pinText = foreach ($pin in $Pins) {
        $pinUuid = New-StableUuid "symbol:$Reference:pin:$pin"
@"
		(pin "$pin"
			(uuid "$pinUuid")
		)
"@
    }

    return @"
	(symbol
		(lib_id "$libText")
		(at $xText $yText $Rotation)
		(unit 1)
		(body_style 1)
		(exclude_from_sim no)
		(in_bom $inBomText)
		(on_board $onBoardText)
		(in_pos_files $inPosFilesText)
		(dnp no)
		(fields_autoplaced yes)
		(uuid "$symbolUuid")
		(property "Reference" "$refText"
			(at $xText $refY 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Value" "$valueText"
			(at $xText $valueY 0)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Footprint" "$footprintText"
			(at $xText $yText $Rotation)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Datasheet" ""
			(at $xText $yText 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
		(property "Description" "$descriptionText"
			(at $xText $yText 0)
			(hide yes)
			(show_name no)
			(do_not_autoplace no)
			(effects
				(font
					(size 1.27 1.27)
				)
			)
		)
$($pinText -join "`r`n")
		(instances
			(project "Tesis"
				(path "/$RootUuid"
					(reference "$refText")
					(unit 1)
				)
			)
		)
	)
"@
}

$baseText = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $BasePath))
$rootUuidMatch = [regex]::Match($baseText, '^\s*\(uuid "([^"]+)"\)', 'Multiline')
if (-not $rootUuidMatch.Success) {
    throw 'No se pudo obtener el UUID raíz del esquema base.'
}
$rootUuid = $rootUuidMatch.Groups[1].Value

$text = $baseText.Replace('(paper "A4")', '(paper "A3")')

# The base schematic predates the fitted carrier pinout. Remove the two PSoC
# endpoint labels whose physical pins moved; their ESP32-side labels remain
# valid and the new PSoC-side labels are added below.
foreach ($obsoleteLabelMarker in @(
        '(label "PSOC_UART_RX"',
        '(label "PSOC_SYNC_IN"'
    )) {
    $obsoleteLabel = Get-SExpressionBlock -Text $text -Marker $obsoleteLabelMarker
    $text = $text.Remove(
        $obsoleteLabel.Start,
        $obsoleteLabel.End - $obsoleteLabel.Start + 1
    )
}

$symbolsToEmbed = @(
    @{
        Path = $deviceLibrary
        Name = 'C'
        LibraryId = 'Device:C'
    },
    @{
        Path = $deviceLibrary
        Name = 'C_Polarized'
        LibraryId = 'Device:C_Polarized'
    },
    @{
        Path = $deviceLibrary
        Name = 'R_Potentiometer'
        LibraryId = 'Device:R_Potentiometer'
    },
    @{
        Path = $deviceLibrary
        Name = 'LED'
        LibraryId = 'Device:LED'
    },
    @{
        Path = $connectorLibrary
        Name = 'Conn_01x02'
        LibraryId = 'Connector_Generic:Conn_01x02'
    },
    @{
        Path = $connectorLibrary
        Name = 'Conn_01x06'
        LibraryId = 'Connector_Generic:Conn_01x06'
    },
    @{
        Path = $switchLibrary
        Name = 'SW_Push'
        LibraryId = 'Switch:SW_Push'
    },
    @{
        Path = $powerLibrary
        Name = 'PWR_FLAG'
        LibraryId = 'power:PWR_FLAG'
    }
)

$embeddedBlocks = foreach ($symbolInfo in $symbolsToEmbed) {
    if ($text.Contains("(symbol `"$($symbolInfo.LibraryId)`"")) {
        continue
    }

    $libraryText = [System.IO.File]::ReadAllText($symbolInfo.Path)
    $sourceBlock = Get-SExpressionBlock `
        -Text $libraryText `
        -Marker "(symbol `"$($symbolInfo.Name)`""
    ConvertTo-EmbeddedSymbol `
        -Block $sourceBlock.Text `
        -SourceName $symbolInfo.Name `
        -LibraryId $symbolInfo.LibraryId
}

if ($embeddedBlocks.Count -gt 0) {
    $libraryBlock = Get-SExpressionBlock -Text $text -Marker '(lib_symbols'
    $embeddedText = "`r`n" + ($embeddedBlocks -join "`r`n") + "`r`n`t"
    $text = $text.Substring(0, $libraryBlock.End) +
        $embeddedText +
        $text.Substring($libraryBlock.End)
}

$labels = [System.Collections.Generic.List[string]]::new()
$notes = [System.Collections.Generic.List[string]]::new()
$noConnects = [System.Collections.Generic.List[string]]::new()
$instances = [System.Collections.Generic.List[string]]::new()

function Add-LabelBlock {
    param(
        [string]$Name,
        [double]$X,
        [double]$Y,
        [string]$Justify,
        [string]$Key
    )

    $labels.Add((New-Label -Name $Name -X $X -Y $Y -Justify $Justify -Key $Key))
}

function Add-TwoPinHorizontal {
    param(
        [string]$LibraryId,
        [string]$Reference,
        [string]$Value,
        [string]$Footprint,
        [string]$Description,
        [double]$X,
        [double]$Y,
        [double]$PinOffset,
        [string]$LeftNet,
        [string]$RightNet
    )

    $instances.Add((New-SymbolInstance `
        -LibraryId $LibraryId `
        -Reference $Reference `
        -Value $Value `
        -Footprint $Footprint `
        -Description $Description `
        -X $X `
        -Y $Y `
        -Rotation 90 `
        -Pins @('1', '2') `
        -RootUuid $rootUuid))

    Add-LabelBlock `
        -Name $LeftNet `
        -X ($X - $PinOffset) `
        -Y $Y `
        -Justify 'right' `
        -Key "$Reference:left"
    Add-LabelBlock `
        -Name $RightNet `
        -X ($X + $PinOffset) `
        -Y $Y `
        -Justify 'left' `
        -Key "$Reference:right"
}

function Add-NoConnectBlock {
    param(
        [double]$X,
        [double]$Y,
        [string]$Key
    )

    $noConnects.Add((New-NoConnect -X $X -Y $Y -Key $Key))
}

# Physical PSoC pin labels. These positions follow the custom CY8CKIT-059
# symbol: J1 is at x=63.5 and J2 is at x=99.06.
$psocLabels = @(
    @('PSOC_UART_RX', 63.5, 45.72, 'right', 'A1:J1.1'),
    @('SD_CS', 63.5, 53.34, 'right', 'A1:J1.4'),
    @('SD_SCK', 63.5, 55.88, 'right', 'A1:J1.5'),
    @('SD_MOSI', 63.5, 58.42, 'right', 'A1:J1.6'),
    @('SD_MISO', 63.5, 60.96, 'right', 'A1:J1.7'),
    @('SE_OUT', 63.5, 63.5, 'right', 'A1:J1.8'),
    @('BUTTON_IN', 63.5, 73.66, 'right', 'A1:J1.12'),
    @('LED_OUT', 63.5, 91.44, 'right', 'A1:J1.19'),
    @('AMUX_CAP', 63.5, 96.52, 'right', 'A1:J1.21'),
    @('PSOC_SYNC_IN', 63.5, 99.06, 'right', 'A1:J1.22'),
    @('GEO_IN_N', 63.5, 101.6, 'right', 'A1:J1.23'),
    @('GEO_IN_P', 63.5, 104.14, 'right', 'A1:J1.24'),
    @('GND', 63.5, 106.68, 'right', 'A1:J1.25'),
    @('PSOC_VDD_5V', 99.06, 45.72, 'left', 'A1:J2.1'),
    @('VREF_ADDER', 99.06, 53.34, 'left', 'A1:J2.4'),
    @('VREF_LP', 99.06, 55.88, 'left', 'A1:J2.5'),
    @('SUM_M', 99.06, 58.42, 'left', 'A1:J2.6'),
    @('LP_M', 99.06, 63.5, 'left', 'A1:J2.8'),
    @('LP_OUT', 99.06, 68.58, 'left', 'A1:J2.10'),
    @('SUM_OUT', 99.06, 71.12, 'left', 'A1:J2.11'),
    @('BP_OUT', 99.06, 88.9, 'left', 'A1:J2.18'),
    @('VREF', 99.06, 91.44, 'left', 'A1:J2.19'),
    @('PGA_OUT', 99.06, 96.52, 'left', 'A1:J2.21'),
    @('BP_M', 99.06, 99.06, 'left', 'A1:J2.22'),
    @('VREF_BP', 99.06, 104.14, 'left', 'A1:J2.24'),
    @('VREF_PGA', 99.06, 106.68, 'left', 'A1:J2.25'),
    @('GND', 99.06, 109.22, 'left', 'A1:J2.26')
)

foreach ($labelInfo in $psocLabels) {
    Add-LabelBlock `
        -Name $labelInfo[0] `
        -X $labelInfo[1] `
        -Y $labelInfo[2] `
        -Justify $labelInfo[3] `
        -Key $labelInfo[4]
}

# The ESP32 module has three exposed grounds. Keeping them on the shared GND
# net avoids leaving module ground pins electrically ambiguous.
Add-LabelBlock -Name 'GND' -X 191.77 -Y 54.61 -Justify 'left' -Key 'A2:J3.1'
Add-LabelBlock -Name 'GND' -X 191.77 -Y 69.85 -Justify 'left' -Key 'A2:J3.7'

# Explicit no-connect markers make the carrier intent reproducible and keep
# future ERC runs focused on the pins that are actually part of this prototype.
$usedA1J1 = @(1, 4, 5, 6, 7, 8, 9, 12, 19, 21, 22, 23, 24, 25)
$usedA1J2 = @(1, 2, 4, 5, 6, 8, 10, 11, 18, 19, 21, 22, 24, 25, 26)
for ($pinNumber = 1; $pinNumber -le 26; $pinNumber++) {
    $pinY = 45.72 + (($pinNumber - 1) * 2.54)
    if ($pinNumber -notin $usedA1J1) {
        Add-NoConnectBlock -X 63.5 -Y $pinY -Key "A1:J1.$pinNumber"
    }
    if ($pinNumber -notin $usedA1J2) {
        Add-NoConnectBlock -X 99.06 -Y $pinY -Key "A1:J2.$pinNumber"
    }
}

$usedA2J2 = @(1, 7, 9, 10, 11, 14)
$usedA2J3 = @(1, 7)
for ($pinNumber = 1; $pinNumber -le 19; $pinNumber++) {
    $pinY = 54.61 + (($pinNumber - 1) * 2.54)
    if ($pinNumber -notin $usedA2J2) {
        Add-NoConnectBlock -X 156.21 -Y $pinY -Key "A2:J2.$pinNumber"
    }
    if ($pinNumber -notin $usedA2J3) {
        Add-NoConnectBlock -X 191.77 -Y $pinY -Key "A2:J3.$pinNumber"
    }
}

# Input biasing around the geophone.
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R2' `
    -Value '50k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign input bias, GEO_IN_P to VREF.' `
    -X 55.88 `
    -Y 147.32 `
    -PinOffset 3.81 `
    -LeftNet 'GEO_IN_P' `
    -RightNet 'VREF'
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R3' `
    -Value '50k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign input bias, VREF to GEO_IN_N.' `
    -X 88.9 `
    -Y 147.32 `
    -PinOffset 3.81 `
    -LeftNet 'VREF' `
    -RightNet 'GEO_IN_N'

# External band-pass network around the internal OPAbp block.
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R4' `
    -Value '43k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign band-pass input resistance.' `
    -X 134.62 `
    -Y 147.32 `
    -PinOffset 3.81 `
    -LeftNet 'SE_OUT' `
    -RightNet 'BP_M'
Add-TwoPinHorizontal `
    -LibraryId 'Device:C_Polarized' `
    -Reference 'C1' `
    -Value '680uF' `
    -Footprint $largeElectrolyticFootprint `
    -Description 'TopDesign band-pass input capacitor; polarity must be checked at bring-up.' `
    -X 170.18 `
    -Y 147.32 `
    -PinOffset 3.81 `
    -LeftNet 'SE_OUT' `
    -RightNet 'BP_M'
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R5' `
    -Value '47k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign band-pass feedback resistance.' `
    -X 210.82 `
    -Y 147.32 `
    -PinOffset 3.81 `
    -LeftNet 'BP_OUT' `
    -RightNet 'BP_M'
Add-TwoPinHorizontal `
    -LibraryId 'Device:C' `
    -Reference 'C2' `
    -Value '27pF' `
    -Footprint $capacitorFootprint `
    -Description 'TopDesign band-pass feedback capacitor.' `
    -X 246.38 `
    -Y 147.32 `
    -PinOffset 3.81 `
    -LeftNet 'BP_OUT' `
    -RightNet 'BP_M'

# External summing network around the internal OPAsum block.
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R6' `
    -Value '6.8k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign SE_OUT contribution to the analog summing node.' `
    -X 45.72 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'SE_OUT' `
    -RightNet 'SUM_M'
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R7' `
    -Value '47k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign BP_OUT contribution before gain trim.' `
    -X 83.82 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'BP_OUT' `
    -RightNet 'BP_GAIN_ADJ'

$instances.Add((New-SymbolInstance `
    -LibraryId 'Device:R_Potentiometer' `
    -Reference 'RV1' `
    -Value '2k (31.7% nominal)' `
    -Footprint 'Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical' `
    -Description 'TopDesign R_12 band-pass contribution trim; wiper tied to the SUM_M end.' `
    -X 124.46 `
    -Y 175.26 `
    -Rotation 0 `
    -Pins @('1', '2', '3') `
    -RootUuid $rootUuid))
Add-LabelBlock -Name 'BP_GAIN_ADJ' -X 124.46 -Y 171.45 -Justify 'right' -Key 'RV1:pin1'
Add-LabelBlock -Name 'SUM_M' -X 128.27 -Y 175.26 -Justify 'left' -Key 'RV1:pin2'
Add-LabelBlock -Name 'SUM_M' -X 124.46 -Y 179.07 -Justify 'right' -Key 'RV1:pin3'

Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R8' `
    -Value '27k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign summing amplifier feedback resistance.' `
    -X 170.18 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'SUM_OUT' `
    -RightNet 'SUM_M'
Add-TwoPinHorizontal `
    -LibraryId 'Device:C' `
    -Reference 'C3' `
    -Value '15nF' `
    -Footprint $capacitorFootprint `
    -Description 'TopDesign summing amplifier feedback capacitor.' `
    -X 208.28 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'SUM_OUT' `
    -RightNet 'SUM_M'

# External low-pass network around the internal OPAlp block.
Add-TwoPinHorizontal `
    -LibraryId 'Device:C' `
    -Reference 'C4' `
    -Value '47nF' `
    -Footprint $capacitorFootprint `
    -Description 'TopDesign PGA_OUT shunt capacitor to VREF.' `
    -X 256.54 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'PGA_OUT' `
    -RightNet 'VREF'
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R9' `
    -Value '12k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign low-pass input resistance.' `
    -X 294.64 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'PGA_OUT' `
    -RightNet 'LP_M'
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R10' `
    -Value '150k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign low-pass feedback resistance.' `
    -X 337.82 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'LP_OUT' `
    -RightNet 'LP_M'
Add-TwoPinHorizontal `
    -LibraryId 'Device:C' `
    -Reference 'C5' `
    -Value '3.3nF' `
    -Footprint $capacitorFootprint `
    -Description 'TopDesign low-pass feedback capacitor.' `
    -X 378.46 `
    -Y 175.26 `
    -PinOffset 3.81 `
    -LeftNet 'LP_OUT' `
    -RightNet 'LP_M'

# Main VREF decoupling.
Add-TwoPinHorizontal `
    -LibraryId 'Device:C_Polarized' `
    -Reference 'C6' `
    -Value '1uF' `
    -Footprint $smallElectrolyticFootprint `
    -Description 'TopDesign main VREF decoupling.' `
    -X 40.64 `
    -Y 246.38 `
    -PinOffset 3.81 `
    -LeftNet 'VREF' `
    -RightNet 'GND'
Add-TwoPinHorizontal `
    -LibraryId 'Device:C' `
    -Reference 'C7' `
    -Value '100nF' `
    -Footprint $capacitorFootprint `
    -Description 'TopDesign main VREF high-frequency decoupling.' `
    -X 71.12 `
    -Y 246.38 `
    -PinOffset 3.81 `
    -LeftNet 'VREF' `
    -RightNet 'GND'

$referenceBranches = @(
    @{
        Name = 'PGA'
        Net = 'VREF_PGA'
        R = 'R11'
        CPolar = 'C8'
        CSmall = 'C9'
        X = 109.22
    },
    @{
        Name = 'BP'
        Net = 'VREF_BP'
        R = 'R12'
        CPolar = 'C10'
        CSmall = 'C11'
        X = 185.42
    },
    @{
        Name = 'SUM'
        Net = 'VREF_ADDER'
        R = 'R13'
        CPolar = 'C12'
        CSmall = 'C13'
        X = 261.62
    },
    @{
        Name = 'LP'
        Net = 'VREF_LP'
        R = 'R14'
        CPolar = 'C14'
        CSmall = 'C15'
        X = 337.82
    }
)

foreach ($branch in $referenceBranches) {
    Add-TwoPinHorizontal `
        -LibraryId 'Device:R' `
        -Reference $branch.R `
        -Value '30k' `
        -Footprint $resistorFootprint `
        -Description "TopDesign $($branch.Name) reference feed from VREF." `
        -X $branch.X `
        -Y 226.06 `
        -PinOffset 3.81 `
        -LeftNet 'VREF' `
        -RightNet $branch.Net
    Add-TwoPinHorizontal `
        -LibraryId 'Device:C_Polarized' `
        -Reference $branch.CPolar `
        -Value '1uF' `
        -Footprint $smallElectrolyticFootprint `
        -Description "TopDesign $($branch.Name) reference decoupling." `
        -X ($branch.X + 20.32) `
        -Y 246.38 `
        -PinOffset 3.81 `
        -LeftNet $branch.Net `
        -RightNet 'GND'
    Add-TwoPinHorizontal `
        -LibraryId 'Device:C' `
        -Reference $branch.CSmall `
        -Value '100nF' `
        -Footprint $capacitorFootprint `
        -Description "TopDesign $($branch.Name) reference high-frequency decoupling." `
        -X ($branch.X + 45.72) `
        -Y 246.38 `
        -PinOffset 3.81 `
        -LeftNet $branch.Net `
        -RightNet 'GND'
}

Add-TwoPinHorizontal `
    -LibraryId 'Device:C' `
    -Reference 'C16' `
    -Value '100nF' `
    -Footprint $capacitorFootprint `
    -Description 'External capacitor used by AMux_ADC.' `
    -X 55.88 `
    -Y 266.7 `
    -PinOffset 3.81 `
    -LeftNet 'AMUX_CAP' `
    -RightNet 'GND'

# Button, external sync and microSD module headers.
$instances.Add((New-SymbolInstance `
    -LibraryId 'Switch:SW_Push' `
    -Reference 'SW1' `
    -Value 'USER_BUTTON' `
    -Footprint 'Button_Switch_THT:SW_PUSH_6mm' `
    -Description 'User button from the PSoC analog supply to BUTTON_IN.' `
    -X 279.4 `
    -Y 81.28 `
    -Rotation 0 `
    -Pins @('1', '2') `
    -RootUuid $rootUuid))
Add-LabelBlock -Name 'PSOC_VDD_5V' -X 274.32 -Y 81.28 -Justify 'right' -Key 'SW1:pin1'
Add-LabelBlock -Name 'BUTTON_IN' -X 284.48 -Y 81.28 -Justify 'left' -Key 'SW1:pin2'

Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R15' `
    -Value '30k' `
    -Footprint $resistorFootprint `
    -Description 'TopDesign button pull-down.' `
    -X 327.66 `
    -Y 81.28 `
    -PinOffset 3.81 `
    -LeftNet 'BUTTON_IN' `
    -RightNet 'GND'

# The firmware drives LED=1 during its boot/ping indication. The recovered
# legacy value beside D_1 is 390 ohm, so the carrier keeps an active-high LED.
Add-TwoPinHorizontal `
    -LibraryId 'Device:R' `
    -Reference 'R16' `
    -Value '390' `
    -Footprint $resistorFootprint `
    -Description 'Current limiter for the active-high PSoC status LED.' `
    -X 314.96 `
    -Y 104.14 `
    -PinOffset 3.81 `
    -LeftNet 'LED_OUT' `
    -RightNet 'LED_ANODE'

$instances.Add((New-SymbolInstance `
    -LibraryId 'Device:LED' `
    -Reference 'D1' `
    -Value 'LED_GREEN' `
    -Footprint 'LED_THT:LED_D3.0mm' `
    -Description 'Active-high status LED driven by the PSoC LED pin.' `
    -X 365.76 `
    -Y 104.14 `
    -Rotation 0 `
    -Pins @('1', '2') `
    -RootUuid $rootUuid))
Add-LabelBlock -Name 'GND' -X 361.95 -Y 104.14 -Justify 'right' -Key 'D1:pin1'
Add-LabelBlock -Name 'LED_ANODE' -X 369.57 -Y 104.14 -Justify 'left' -Key 'D1:pin2'

$instances.Add((New-SymbolInstance `
    -LibraryId 'Connector_Generic:Conn_01x02' `
    -Reference 'J3' `
    -Value 'SYNC_EXT' `
    -Footprint 'Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical' `
    -Description 'Optional external synchronization input to ESP32 GPIO32.' `
    -X 269.24 `
    -Y 55.88 `
    -Rotation 0 `
    -Pins @('1', '2') `
    -RootUuid $rootUuid))
Add-LabelBlock -Name 'SYNC_EXT_IN' -X 264.16 -Y 55.88 -Justify 'right' -Key 'J3:pin1'
Add-LabelBlock -Name 'GND' -X 264.16 -Y 58.42 -Justify 'right' -Key 'J3:pin2'

$instances.Add((New-SymbolInstance `
    -LibraryId 'Connector_Generic:Conn_01x02' `
    -Reference 'J4' `
    -Value 'GEOPHONE' `
    -Footprint 'TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2_1x02_P5.00mm_Horizontal' `
    -Description 'Geophone input terminal.' `
    -X 25.4 `
    -Y 147.32 `
    -Rotation 0 `
    -Pins @('1', '2') `
    -RootUuid $rootUuid))
Add-LabelBlock -Name 'GEO_IN_P' -X 20.32 -Y 147.32 -Justify 'right' -Key 'J4:pin1'
Add-LabelBlock -Name 'GEO_IN_N' -X 20.32 -Y 149.86 -Justify 'right' -Key 'J4:pin2'

$instances.Add((New-SymbolInstance `
    -LibraryId 'Connector_Generic:Conn_01x06' `
    -Reference 'J5' `
    -Value 'MICROSD_5V' `
    -Footprint 'Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical' `
    -Description 'Header for a 5 V-compatible microSD SPI module; do not fit a raw 3.3 V card socket here.' `
    -X 375.92 `
    -Y 60.96 `
    -Rotation 0 `
    -Pins @('1', '2', '3', '4', '5', '6') `
    -RootUuid $rootUuid))
Add-LabelBlock -Name 'PSOC_VDD_5V' -X 370.84 -Y 55.88 -Justify 'right' -Key 'J5:pin1'
Add-LabelBlock -Name 'GND' -X 370.84 -Y 58.42 -Justify 'right' -Key 'J5:pin2'
Add-LabelBlock -Name 'SD_CS' -X 370.84 -Y 60.96 -Justify 'right' -Key 'J5:pin3'
Add-LabelBlock -Name 'SD_SCK' -X 370.84 -Y 63.5 -Justify 'right' -Key 'J5:pin4'
Add-LabelBlock -Name 'SD_MOSI' -X 370.84 -Y 66.04 -Justify 'right' -Key 'J5:pin5'
Add-LabelBlock -Name 'SD_MISO' -X 370.84 -Y 68.58 -Justify 'right' -Key 'J5:pin6'

# These flags state the intended power source model for ERC: both development
# kits are USB-powered, while the carrier only consumes their exported rails.
$powerFlags = @(
    @{
        Reference = '#FLG01'
        Net = 'GND'
        X = 223.52
        Y = 50.8
    },
    @{
        Reference = '#FLG02'
        Net = '+3V3_ESP'
        X = 223.52
        Y = 58.42
    },
    @{
        Reference = '#FLG03'
        Net = 'PSOC_VDD_5V'
        X = 223.52
        Y = 66.04
    }
)

foreach ($flag in $powerFlags) {
    $instances.Add((New-SymbolInstance `
        -LibraryId 'power:PWR_FLAG' `
        -Reference $flag.Reference `
        -Value 'PWR_FLAG' `
        -Footprint '' `
        -Description 'ERC declaration for a rail exported by a USB-powered development kit.' `
        -X $flag.X `
        -Y $flag.Y `
        -Rotation 0 `
        -Pins @('1') `
        -RootUuid $rootUuid `
        -InBom $false `
        -OnBoard $false `
        -InPosFiles $false))
    Add-LabelBlock `
        -Name $flag.Net `
        -X $flag.X `
        -Y $flag.Y `
        -Justify 'left' `
        -Key "$($flag.Reference):pin1"
}

$notes.Add((New-TextNote `
    -Text 'CARRIER INTERMEDIA — CY8CKIT-059 + ESP32 DevKitC' `
    -X 20 `
    -Y 20 `
    -Size 2 `
    -Key 'title'))
$notes.Add((New-TextNote `
    -Text 'Sólo GND y señales unen los kits; no unir 5 V del PSoC con 3.3 V del ESP32.' `
    -X 20 `
    -Y 25 `
    -Size 1.27 `
    -Key 'power-domain-warning'))
$notes.Add((New-TextNote `
    -Text 'PSoC TX es open-drain y R1 lo eleva a +3V3_ESP. UART: GPIO25 RX / GPIO26 TX; SYNC: GPIO27; externo: GPIO32.' `
    -X 20 `
    -Y 29 `
    -Size 1.27 `
    -Key 'esp-interface'))
$notes.Add((New-TextNote `
    -Text 'Pinout PSoC bloqueado y compilado: SPI P2[3..6] = CS/SCK/MOSI/MISO en J1.4..J1.7.' `
    -X 20 `
    -Y 33 `
    -Size 1.27 `
    -Key 'sck-warning'))
$notes.Add((New-TextNote `
    -Text 'Se evitan LED/SW y bypass onboard salvo LPm=P0.3/J2.8, requerido por el ruteo analógico del fitter.' `
    -X 20 `
    -Y 37 `
    -Size 1.1 `
    -Key 'onboard-passives-warning'))
$notes.Add((New-TextNote `
    -Text 'ENTRADA Y ACONDICIONAMIENTO ANALÓGICO EXTERNO (TopDesign actual)' `
    -X 20 `
    -Y 128 `
    -Size 1.6 `
    -Key 'analog-title'))
$notes.Add((New-TextNote `
    -Text 'Los PGA, OPAbp, OPAsum, OPAlp, IDAC, AMux, LPF, ADC, DMA, DFB, temporizadores y debouncer son internos al PSoC y no forman parte de la BOM.' `
    -X 20 `
    -Y 132 `
    -Size 1.1 `
    -Key 'internal-blocks'))
$notes.Add((New-TextNote `
    -Text 'Interno PSoC: AMux(PGA/BP/SUM/LP) → LPF 15 kHz → ADC DelSig 18-bit; OPAref acondiciona VREF.' `
    -X 20 `
    -Y 116 `
    -Size 1.05 `
    -Key 'internal-analog-flow'))
$notes.Add((New-TextNote `
    -Text 'Gestión interna: SignalController + DFB + DMA DelSig→RAM / Filter→RAM + EEPROM + watchdog.' `
    -X 20 `
    -Y 120 `
    -Size 1.05 `
    -Key 'internal-management-flow'))
$notes.Add((New-TextNote `
    -Text 'Periféricos internos: UART 115200, EdgeDetector/Sync a 24 MHz, SPI Master, timers y debouncer.' `
    -X 20 `
    -Y 124 `
    -Size 1.05 `
    -Key 'internal-peripheral-flow'))
$notes.Add((New-TextNote `
    -Text 'Entrada diferencial y sesgo' `
    -X 20 `
    -Y 137 `
    -Size 1.27 `
    -Key 'section-input'))
$notes.Add((New-TextNote `
    -Text 'Banda pasante (OPAbp interno)' `
    -X 125 `
    -Y 137 `
    -Size 1.27 `
    -Key 'section-bp'))
$notes.Add((New-TextNote `
    -Text 'Sumador (OPAsum interno)' `
    -X 20 `
    -Y 165 `
    -Size 1.27 `
    -Key 'section-sum'))
$notes.Add((New-TextNote `
    -Text 'Pasa-bajos (OPAlp interno)' `
    -X 250 `
    -Y 165 `
    -Size 1.27 `
    -Key 'section-lp'))
$notes.Add((New-TextNote `
    -Text 'REFERENCIAS ANALÓGICAS Y DESACOPLOS EXTERNOS' `
    -X 20 `
    -Y 205 `
    -Size 1.6 `
    -Key 'references-title'))
$notes.Add((New-TextNote `
    -Text 'VREF principal' `
    -X 30 `
    -Y 218 `
    -Size 1.1 `
    -Key 'main-vref'))
$notes.Add((New-TextNote `
    -Text 'Cada rama: VREF → 30 k → VREF_x, con 1 uF || 100 nF a GND.' `
    -X 100 `
    -Y 210 `
    -Size 1.1 `
    -Key 'branch-note'))
$notes.Add((New-TextNote `
    -Text 'PERIFÉRICOS EXTERNOS' `
    -X 260 `
    -Y 42 `
    -Size 1.6 `
    -Key 'peripherals-title'))
$notes.Add((New-TextNote `
    -Text 'J5 requiere un módulo microSD que acepte 5 V y adapte niveles; una tarjeta/socket crudo es sólo 3.3 V.' `
    -X 260 `
    -Y 95 `
    -Size 1.1 `
    -Key 'sd-warning'))

$rootSymbolMarker = "`t(symbol`r`n`t`t(lib_id "
$firstRootSymbol = $text.IndexOf($rootSymbolMarker, [System.StringComparison]::Ordinal)
if ($firstRootSymbol -lt 0) {
    $rootSymbolMarker = "`t(symbol`n`t`t(lib_id "
    $firstRootSymbol = $text.IndexOf($rootSymbolMarker, [System.StringComparison]::Ordinal)
}
if ($firstRootSymbol -lt 0) {
    throw 'No se encontró la primera instancia raíz del esquema.'
}

$annotationText =
    ($notes -join "`r`n") + "`r`n" +
    ($labels -join "`r`n") + "`r`n" +
    ($noConnects -join "`r`n") + "`r`n"
$text = $text.Substring(0, $firstRootSymbol) +
    $annotationText +
    $text.Substring($firstRootSymbol)

$sheetMarker = "`t(sheet_instances"
$sheetIndex = $text.IndexOf($sheetMarker, [System.StringComparison]::Ordinal)
if ($sheetIndex -lt 0) {
    throw 'No se encontró sheet_instances en el esquema.'
}

$instanceText = ($instances -join "`r`n") + "`r`n"
$text = $text.Substring(0, $sheetIndex) +
    $instanceText +
    $text.Substring($sheetIndex)

$outputDirectory = Split-Path -Parent $OutputPath
if (-not (Test-Path -LiteralPath $outputDirectory)) {
    throw "No existe el directorio de salida: $outputDirectory"
}

[System.IO.File]::WriteAllText(
    $OutputPath,
    $text,
    [System.Text.UTF8Encoding]::new($false)
)

if (Test-Path -LiteralPath $BaseProjectPath -PathType Leaf) {
    $projectText = [System.IO.File]::ReadAllText($BaseProjectPath)
    [System.IO.File]::WriteAllText(
        $OutputProjectPath,
        $projectText,
        [System.Text.UTF8Encoding]::new($false)
    )
}

Write-Output "Esquema generado: $OutputPath"
if (Test-Path -LiteralPath $OutputProjectPath -PathType Leaf) {
    Write-Output "Configuración de proyecto: $OutputProjectPath"
}
Write-Output "Instancias físicas nuevas: $($instances.Count)"
Write-Output "Etiquetas nuevas: $($labels.Count)"
Write-Output "No conectados explícitos: $($noConnects.Count)"
Write-Output "Notas nuevas: $($notes.Count)"
