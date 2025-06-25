# Steganography Analyzer - Quick Reference

## Launchers:
- **Launch-GUI.bat**         - Start graphical interface
- **Launch-CLI-Enhanced.bat** - CLI with PATH setup  
- **Analyze-File.bat**       - Drag & drop analysis
- **CLI-Help.bat**           - Show CLI help

## Executables (in dist/ folder):
- **StegoAnalyzer-CLI.exe**  - Command-line version
- **StegoAnalyzer-GUI.exe**  - GUI version (no console)

## Usage Examples:
`
# GUI mode
Launch-GUI.bat

# CLI mode - basic
StegoAnalyzer-CLI.exe image.jpg

# CLI mode - with password
StegoAnalyzer-CLI.exe image.jpg -p mypassword

# CLI mode - save results
StegoAnalyzer-CLI.exe image.jpg -o results.json

# Drag and drop
Drag file onto Analyze-File.bat
`

## Tool Installation:
Run Install-Tools.ps1 to check tool availability
Place external tools in tools/ directory
