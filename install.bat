@echo off
setlocal

cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo Nie znaleziono Pythona 3.10 lub nowszego.
    echo Zainstaluj Python z https://www.python.org/downloads/windows/ i zaznacz opcje dodania do PATH.
    pause
    exit /b 1
)

echo Budowanie pliku EXE i instalowanie Better Calculator...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
if errorlevel 1 (
    echo.
    echo Instalacja nie powiodla sie.
    pause
    exit /b 1
)

echo.
echo Instalacja zakonczona pomyslnie.
pause
exit /b 0