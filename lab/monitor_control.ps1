param(
    [string]$Port = 'COM8',
    [int]$Seconds = 1250,
    [switch]$StartLearning,
    [switch]$Raw,
    [string]$Command = '',
    [switch]$ResetEsp
)

$sp = [System.IO.Ports.SerialPort]::new($Port, 115200, 'None', 8, 'one')
$sp.NewLine = "`n"
$sp.ReadTimeout = 1200
$sp.DtrEnable = $false
$sp.RtsEnable = $false
$values = @{}
$lastPrint = [DateTime]::MinValue
$sp.Open()
try {
    if ($ResetEsp) {
        $sp.RtsEnable = $true
        Start-Sleep -Milliseconds 150
        $sp.RtsEnable = $false
        Start-Sleep -Milliseconds 800
    } else {
        Start-Sleep -Milliseconds 700
        $sp.DiscardInBuffer()
    }
    if ($StartLearning) { $sp.Write("ctl learn`n") }
    if ($Command) { $sp.Write("$Command`n") }
    $deadline = [DateTime]::UtcNow.AddSeconds($Seconds)
    while ([DateTime]::UtcNow -lt $deadline) {
        try {
            $line = $sp.ReadLine().Trim()
            if ($Raw) { $line }
            if ($line -match '^#CTL_ACK') { $line }
            if ($line -match '^#CTL 0 (256|257|258|264|272|273|274|275|300|301|304|305) (-?\d+)') {
                $key = [int]$matches[1]
                $value = [int64]$matches[2]
                $changed = (-not $values.ContainsKey($key)) -or $values[$key] -ne $value
                $values[$key] = $value
                if ($changed -and $key -in 256,257,258,264,272,273,274,275) {
                    "CHANGE key=$key value=$value"
                }
                if (([DateTime]::UtcNow - $lastPrint).TotalSeconds -ge 10 -and
                    $values.ContainsKey(256) -and $values.ContainsKey(300) -and $values.ContainsKey(304)) {
                    "SNAP state=$($values[256]) profile=$($values[257]) band=$($values[258]) " +
                    "idac=($($values[272]),$($values[273]),$($values[274]),$($values[275])) " +
                    "SUM=$($values[300])/$($values[301]) LP=$($values[304])/$($values[305])"
                    $lastPrint = [DateTime]::UtcNow
                }
            }
        } catch [System.TimeoutException] {
        }
    }
} finally {
    $sp.Close()
}
