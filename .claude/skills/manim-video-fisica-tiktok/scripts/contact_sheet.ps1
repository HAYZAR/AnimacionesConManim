<#
.SYNOPSIS
    Genera una "hoja de contacto" (contact sheet) de un video de Manim: un
    fotograma por segundo, en una sola imagen en cuadricula, para revisar
    visualmente toda la linea de tiempo sin tener que abrir el video.

.DESCRIPTION
    Un video de Manim puede verse perfecto en el codigo y seguir teniendo
    texto cortado en los bordes, vectores mal orientados, o elementos que
    nunca se borran de la escena. La unica forma confiable de detectarlo es
    mirando los fotogramas reales. Este script hace eso automaticamente:
    extrae 1 fotograma por segundo con ffmpeg y arma una cuadricula con
    todos ellos en una sola imagen, lista para revisar (por ejemplo, con la
    herramienta de lectura de imagenes de Claude Code).

.PARAMETER Video
    Ruta al archivo .mp4 ya renderizado.

.PARAMETER OutDir
    Carpeta donde se guardan los fotogramas individuales y la(s) hoja(s) de
    contacto. Por defecto, una subcarpeta "contact_sheet" junto al video.

.PARAMETER FramesPerSheet
    Cuantos fotogramas caben en cada imagen de cuadricula antes de empezar
    una hoja nueva (por defecto 30, es decir ~30 segundos de video por hoja).

.EXAMPLE
    .\contact_sheet.ps1 -Video "Español\extras\mi_video\media\videos\mi_video\1920p30\MiEscena.mp4"
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Video,

    [string]$OutDir,

    [int]$FramesPerSheet = 30
)

if (-not (Test-Path $Video)) {
    Write-Error "No se encontro el video: $Video"
    exit 1
}

if (-not $OutDir) {
    $videoDir = Split-Path -Parent (Resolve-Path $Video)
    $OutDir = Join-Path $videoDir "contact_sheet"
}
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

Write-Host "Extrayendo 1 fotograma por segundo..."
$framePattern = Join-Path $OutDir "frame%03d.png"
ffmpeg -y -i $Video -vf "fps=1" $framePattern 2>&1 | Select-Object -Last 3

$frames = Get-ChildItem -Path $OutDir -Filter "frame*.png" | Sort-Object Name
if ($frames.Count -eq 0) {
    Write-Error "ffmpeg no genero fotogramas. Revisa que ffmpeg este instalado y en el PATH (ver SKILL.md seccion 1)."
    exit 1
}
Write-Host "Se extrajeron $($frames.Count) fotogramas (~$($frames.Count)s de video)."

# Divide los fotogramas en lotes de $FramesPerSheet y arma una cuadricula por lote
$batches = [System.Collections.Generic.List[Object]]::new()
for ($i = 0; $i -lt $frames.Count; $i += $FramesPerSheet) {
    $endIdx = [Math]::Min($i + $FramesPerSheet - 1, $frames.Count - 1)
    $batches.Add($frames[$i..$endIdx])
}

$cols = 6
$sheetPaths = @()
for ($b = 0; $b -lt $batches.Count; $b++) {
    $batch = $batches[$b]
    $rows = [Math]::Ceiling($batch.Count / $cols)
    $sheetPath = Join-Path $OutDir "contact_sheet_$b.png"
    $startNum = $b * $FramesPerSheet + 1

    ffmpeg -y -start_number $startNum -i (Join-Path $OutDir "frame%03d.png") -frames:v $batch.Count `
        -vf "scale=220:390,tile=${cols}x${rows}" $sheetPath 2>&1 | Select-Object -Last 3

    $sheetPaths += $sheetPath
}

Write-Host ""
Write-Host "Listo. Hoja(s) de contacto generada(s):"
$sheetPaths | ForEach-Object { Write-Host "  $_" }
Write-Host ""
Write-Host "Pidele a Claude Code que lea estas imagenes (Read tool) para revisar" -ForegroundColor Yellow
Write-Host "toda la linea de tiempo del video de una sola vez." -ForegroundColor Yellow
