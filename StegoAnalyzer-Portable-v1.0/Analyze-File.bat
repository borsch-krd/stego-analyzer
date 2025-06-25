@echo off
title Steganography Analyzer - CLI
cd /d "%~dp0\dist"
if "%~1"=="" (
    echo Please drag and drop a file onto this script or provide a file path
    pause
    exit /b 1
)
echo Analyzing file: %~1
echo.
"StegoAnalyzer-CLI.exe" "%~1"
pause
