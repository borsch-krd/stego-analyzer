@echo off
title Steganography Analyzer - Enhanced CLI
echo Steganography Analyzer - Enhanced CLI
echo ====================================

REM Add tools directory to PATH for this session
set "TOOLS_DIR=%~dp0tools"
set "PATH=%TOOLS_DIR%;%PATH%"

echo Tools directory added to PATH: %TOOLS_DIR%
echo.

REM Change to dist directory
cd /d "%~dp0dist"

REM Check if a file was passed as argument
if "%~1"=="" (
    echo Usage: %~nx0 [file_to_analyze] [options]
    echo.
    echo Examples:
    echo   %~nx0 image.jpg
    echo   %~nx0 document.pdf -p password
    echo   %~nx0 audio.wav -o results.json
    echo.
    echo Or drag and drop a file onto this script
    echo.
    pause
    exit /b 1
)

echo Analyzing file: %~1
echo.
"StegoAnalyzer-CLI.exe" %*
echo.
pause
