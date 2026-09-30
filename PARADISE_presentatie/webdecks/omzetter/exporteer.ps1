# Opent een pptx in PowerPoint (zonder venster) en exporteert elke dia als PNG van 1920 breed.
# Gebruik: powershell -File exporteer.ps1 <pptx> <uitmap> [dianummers, komma-gescheiden]
# PowerPoint weigert soms kort na een vorige export (COM-fout); dan tot drie keer opnieuw, met een pauze.
param([string]$Pptx, [string]$Uit, [string]$Dias = "")
New-Item -ItemType Directory -Force $Uit | Out-Null
for ($poging = 1; $poging -le 3; $poging++) {
    $ppt = $null
    try {
        $ppt = New-Object -ComObject PowerPoint.Application
        $pres = $ppt.Presentations.Open($Pptx, $true, $false, $false)
        $kies = if ($Dias) { $Dias.Split(",") | ForEach-Object { [int]$_ } } else { 1..$pres.Slides.Count }
        foreach ($i in $kies) {
            $pres.Slides.Item($i).Export((Join-Path $Uit ("dia{0:D2}.png" -f $i)), "PNG", 1920, 1080)
        }
        "geexporteerd: $($kies.Count) dia's van $($pres.Slides.Count)"
        $pres.Close()
        break
    } catch {
        "poging $poging mislukt: $($_.Exception.Message)"
        Start-Sleep -Seconds 10
    } finally {
        if ($ppt) {
            if ($ppt.Presentations.Count -eq 0) { $ppt.Quit() }
            [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
        }
    }
}
