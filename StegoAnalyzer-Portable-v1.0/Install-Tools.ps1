# Tool Installation Helper
# Run this in PowerShell to help install common tools

Write-Host "Steganography Tool Installation Helper" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Check if tools are available
 = @{
    "exiftool" = "https://exiftool.org/"
    "binwalk" = "pip install binwalk"
    "zsteg" = "gem install zsteg (requires Ruby)"
    "steghide" = "http://steghide.sourceforge.net/"
    "outguess" = "https://github.com/resurrecting-open-source-projects/outguess"
    "foremost" = "Available in Kali Linux repositories"
    "strings" = "Part of GNU binutils"
}

Write-Host "
Checking tool availability..." -ForegroundColor Yellow

foreach ( in .Keys) {
    try {
         = Get-Command  -ErrorAction Stop
        Write-Host "вњ“  - Available" -ForegroundColor Green
    } catch {
        Write-Host "вњ—  - Not found" -ForegroundColor Red
        Write-Host "  Install: " -ForegroundColor Gray
    }
}

Write-Host "
Recommended installation methods:" -ForegroundColor Yellow
Write-Host "- Use Windows Subsystem for Linux (WSL)" -ForegroundColor White
Write-Host "- Use Chocolatey package manager" -ForegroundColor White  
Write-Host "- Download portable versions to tools/ folder" -ForegroundColor White

pause
