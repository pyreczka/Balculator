@echo off
if exist "dist\BetterCalculator.exe" (
	start "" "dist\BetterCalculator.exe"
) else (
	python calculator.py
)
