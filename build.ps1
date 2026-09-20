$ErrorActionPreference = 'Stop'

$sourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $sourceDir

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host 'Nie znaleziono Pythona. Zainstaluj Python 3.10+.' -ForegroundColor Red
    exit 1
}

cmd /c "python -m pip show pyinstaller >nul 2>nul"
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Instaluje PyInstaller...' -ForegroundColor Yellow
    python -m pip install pyinstaller
}

if (Test-Path 'build') { Remove-Item 'build' -Recurse -Force }
if (Test-Path 'dist') { Remove-Item 'dist' -Recurse -Force }
if (Test-Path 'BetterCalculator.spec') { Remove-Item 'BetterCalculator.spec' -Force }

powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $sourceDir 'generate-icon.ps1')
if ($LASTEXITCODE -ne 0) { throw 'Icon generation failed.' }

python -m PyInstaller --onefile --windowed --name BetterCalculator --icon better_calculator.ico calculator.py
if ($LASTEXITCODE -ne 0) { throw 'EXE build failed.' }

Write-Host ''
Write-Host 'EXE ready: dist\BetterCalculator.exe' -ForegroundColor Green
Write-Host 'Installing and creating a desktop shortcut...' -ForegroundColor Cyan
& (Join-Path $sourceDir 'install.ps1')