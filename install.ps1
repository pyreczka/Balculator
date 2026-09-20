$ErrorActionPreference = 'Stop'

$installDir = Join-Path $env:LOCALAPPDATA 'Programs\Better Calculator'
$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Test-Path (Join-Path $sourceDir 'dist\BetterCalculator.exe'))) {
    Write-Host 'Nie znaleziono dist\BetterCalculator.exe. Najpierw uruchom: .\build.ps1' -ForegroundColor Red
    exit 1
}

New-Item -ItemType Directory -Force -Path $installDir | Out-Null
Copy-Item (Join-Path $sourceDir 'dist\BetterCalculator.exe') (Join-Path $installDir 'BetterCalculator.exe') -Force

$launcher = Join-Path $installDir 'better-calculator.cmd'
Set-Content -Path $launcher -Encoding ASCII -Value @('@echo off', 'start "" "%~dp0BetterCalculator.exe"')

$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$pathEntries = @($userPath -split ';' | Where-Object { $_ -and $_.Trim() -ne '' })
if ($pathEntries -notcontains $installDir) {
    [Environment]::SetEnvironmentVariable('Path', (($pathEntries + $installDir) -join ';'), 'User')
}

$startMenu = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPaths = @(
    (Join-Path $startMenu 'Better Calculator.lnk'),
    (Join-Path $desktop 'Better Calculator.lnk')
)
$wsh = New-Object -ComObject WScript.Shell
foreach ($shortcutPath in $shortcutPaths) {
    $shortcut = $wsh.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = (Join-Path $installDir 'BetterCalculator.exe')
    $shortcut.WorkingDirectory = $installDir
    $shortcut.Description = 'Better Calculator'
    $shortcut.Save()
}

Write-Host ''
Write-Host 'Better Calculator zostal zainstalowany.' -ForegroundColor Green
Write-Host "Lokalizacja: $installDir"
Write-Host 'Skrot zostal dodany na pulpit i do menu Start.'
Write-Host 'Otworz nowe okno CMD lub PowerShell i wpisz: better-calculator'
