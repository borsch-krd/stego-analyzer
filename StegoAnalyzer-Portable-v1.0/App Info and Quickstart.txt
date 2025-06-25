Steganography Analyzer - Portable Version
=========================================

This is a portable version of the Steganography Analyzer tool that integrates
multiple steganography and forensic analysis tools.

Files and Folders:
------------------
- dist/                     : Contains the executable files
- tools/                    : Directory for external tools (see below)
- Launch-GUI.bat            : Start the GUI version
- Analyze-File.bat          : Drag & drop files here for CLI analysis
- CLI-Help.bat              : Shows CLI usage instructions
- stego_analyzer.py         : Source code (CLI)
- stego_gui.py              : Source code (GUI)

Quick Start:
------------
1. Double-click "Launch-GUI.bat" to start the graphical interface
2. Or drag and drop files onto "Analyze-File.bat" for command-line analysis

External Tools:
---------------
The analyzer can use these external tools if available:
- zsteg       : Ruby gem for PNG/BMP steganography detection
- steghide    : Hide/extract data in image/audio files
- outguess    : JPEG steganography tool
- exiftool    : Metadata extraction tool
- binwalk     : Firmware analysis and extraction
- foremost    : File carving tool
- strings     : Extract printable strings

Installing External Tools:
--------------------------
1. Download tools and place executables in the tools/ directory
2. Add tools/ directory to your system PATH, or
3. Copy tool executables to Windows\System32 directory

Tool Download Links:
-------------------
- ExifTool: https://exiftool.org/
- Binwalk:  pip install binwalk
- Zsteg:    gem install zsteg (requires Ruby)
- Steghide: http://steghide.sourceforge.net/
- Outguess: https://github.com/resurrecting-open-source-projects/outguess

For Windows users, consider using Windows Subsystem for Linux (WSL) 
for easier tool installation.

Version: 1.0
Built by: Claude 4 Sonnet
