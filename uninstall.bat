@echo off
setlocal

cd /d "%~dp0"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0uninstall.ps1"
if errorlevel 1 (
    echo.
    echo Odinstalowanie nie powiodlo sie.
    pause
    exit /b 1
)

echo.
echo Odinstalowanie zakonczone pomyslnie.
pause
exit /b 0