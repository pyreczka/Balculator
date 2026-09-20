Add-Type -AssemblyName System.Drawing

$size = 256
$bitmap = New-Object System.Drawing.Bitmap $size, $size
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

function New-RoundedPath($x, $y, $width, $height, $radius) {
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $diameter = $radius * 2
    $path.AddArc($x, $y, $diameter, $diameter, 180, 90)
    $path.AddArc($x + $width - $diameter, $y, $diameter, $diameter, 270, 90)
    $path.AddArc($x + $width - $diameter, $y + $height - $diameter, $diameter, $diameter, 0, 90)
    $path.AddArc($x, $y + $height - $diameter, $diameter, $diameter, 90, 90)
    $path.CloseFigure()
    return $path
}

$graphics.Clear([System.Drawing.Color]::Transparent)
$backgroundPath = New-RoundedPath 12 12 232 232 54
$backgroundBrush = New-Object System.Drawing.Drawing2D.LinearGradientBrush(
    [System.Drawing.Rectangle]::new(12, 12, 232, 232),
    [System.Drawing.Color]::FromArgb(38, 121, 238),
    [System.Drawing.Color]::FromArgb(12, 75, 174),
    135
)
$graphics.FillPath($backgroundBrush, $backgroundPath)

$shadowPath = New-RoundedPath 60 38 136 184 25
$shadowBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(55, 0, 27, 72))
$graphics.FillPath($shadowBrush, $shadowPath)

$bodyPath = New-RoundedPath 56 30 136 184 25
$bodyBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(250, 255, 255, 255))
$graphics.FillPath($bodyBrush, $bodyPath)

$displayPath = New-RoundedPath 72 52 104 39 11
$displayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(27, 39, 57))
$graphics.FillPath($displayBrush, $displayPath)
$displayLine = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(102, 170, 255))
$graphics.FillRectangle($displayLine, 145, 76, 17, 3)

$keyBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(226, 237, 250))
$operatorBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(48, 126, 232))
foreach ($row in 0..3) {
    foreach ($column in 0..3) {
        $x = 72 + ($column * 27)
        $y = 105 + ($row * 24)
        $path = New-RoundedPath $x $y 20 16 5
        $graphics.FillPath($(if ($column -eq 3) { $operatorBrush } else { $keyBrush }), $path)
        $path.Dispose()
    }
}

$outputPath = Join-Path $PSScriptRoot 'better_calculator.ico'
$icon = [System.Drawing.Icon]::FromHandle($bitmap.GetHicon())
$stream = [System.IO.File]::Create($outputPath)
$icon.Save($stream)
$stream.Dispose()
$icon.Dispose()
$backgroundBrush.Dispose()
$shadowBrush.Dispose()
$bodyBrush.Dispose()
$displayBrush.Dispose()
$displayLine.Dispose()
$keyBrush.Dispose()
$operatorBrush.Dispose()
$backgroundPath.Dispose()
$shadowPath.Dispose()
$bodyPath.Dispose()
$displayPath.Dispose()
$graphics.Dispose()
$bitmap.Dispose()

Write-Host "Icon generated: $outputPath"