# Export all 139 slides as PNG images from Java_Advanced_Topics.pptx
# Run this script to replace the SVG placeholders with real slide images

$ErrorActionPreference = 'Stop'
$base = 'D:\WorkBuddy\ThinkingInJava\Java_OOP_Foundations'
$outDir = "$base\courseware_advanced\img"

# Create output directory if it doesn't exist
if (!(Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

$pp = New-Object -ComObject PowerPoint.Application
$pres = $pp.Presentations.Open("$base\Java_Advanced_Topics.pptx", $true, $false, $false)
$count = $pres.Slides.Count
Write-Host "Exporting $count slides to $outDir ..." -ForegroundColor Cyan

for ($i = 1; $i -le $count; $i++) {
    $f = "{0}\{1:d3}.png" -f $outDir, $i
    $pres.Slides.Item($i).Export($f, 'PNG', 1600, 900)
    if ($i % 20 -eq 0) {
        Write-Host "  Exported $i / $count" -ForegroundColor Green
    }
}

$pres.Close()
$pp.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($pp) | Out-Null
Write-Host "DONE - exported all $count slides" -ForegroundColor Green
Write-Host "Run: python build_all.py && python build_course_menu.py to refresh players"