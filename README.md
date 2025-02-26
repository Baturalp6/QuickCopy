# File Transfer Tool

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey.svg)]()
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/downloads/)
[![GitHub release](https://img.shields.io/badge/release-v1.0-blue.svg)](https://github.com/Baturalp6/QuickCopy)

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [Development](#development)
- [Important Notes](#important-notes)
- [Troubleshooting](#troubleshooting)
- [License & Rights](#license--rights)

## Overview
File Transfer Tool helps you automatically locate and copy files based on catalog numbers. Perfect for managing large file collections in business environments.

## Key Features
- 🔍 Smart file search using catalog numbers from Excel
- 📁 Recursive directory scanning
- 📊 Real-time progress tracking
- 📝 Detailed operation reports
- 🖥️ Cross-platform support (Windows & macOS)
- 🎯 User-friendly interface

## Getting Started

### Prerequisites
- Excel file with catalog numbers in column B
- Access to source files directory
- Sufficient storage space in target directory

### Installation Options

#### 1. Pre-built Executables (Recommended)
You can find pre-built executables in the [Releases section](https://github.com/Baturalp6/QuickCopy/releases/tag/v1.0.0):
- **Windows**: Download `FileCopier.exe`
- **macOS**: Download `FileCopier.app` (Note: Due to cross-platform compilation limitations, macOS users might need to build from source)

#### 2. Build from Source
```bash
# Clone repository
git clone https://github.com/Baturalp6/file-transfer-tool.git

# Install dependencies
pip install -r requirements.txt

# Run application
python src/QuickCopy.py
```

## Usage Guide

1. Launch the application
2. Select source directory containing your files
3. Choose Excel file with catalog numbers (column B)
4. Select target directory for copied files
5. Click "Start" to begin the process

## Development

### Development Environment Setup
1. Install Python 3.x (tested with Python 3.9+)
2. Install required dependencies:
```bash
pip install pandas pyinstaller tkinter
```

### Building from Source

#### Windows (.exe)
```bash
# Basic version
python -m PyInstaller --onefile --windowed --name "FileCopier" src/QuickCopy.py

# Advanced version with explicit dependencies
python -m PyInstaller --onefile --windowed --hidden-import pandas --hidden-import tkinter --name "FileCopier" src/QuickCopy.py
```

#### macOS (.app)
```bash
python -m PyInstaller --onefile --windowed --name "FileCopier" src/QuickCopy.py
```

### Project Structure
```
QuickCopy/
│
├── src/
│   └── QuickCopy.py      # Main program
├── README.md             # User guide and documentation
├── LICENSE              # MIT License
├── requirements.txt     # Dependencies
│
├── dist/               # Build output directory
│   ├── FileCopier.exe # Windows executable
│   └── FileCopier.app # macOS application
```

Note: The compiled .exe or .app can be copied anywhere and run directly, e.g. from the desktop.

### Contributing
Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

## Important Notes

### Antivirus Warning
Some antivirus programs (e.g., Avast) might flag this application as suspicious. This is a common false positive that occurs with PyInstaller-generated executables because:

1. PyInstaller packages Python programs into standalone executables
2. This packaging method is sometimes used by malware creators
3. Antivirus software often flags unknown packed executables as suspicious

This is completely normal for custom-built applications and you can:
- Add the application to your antivirus whitelist
- Verify the source code and build it yourself
- Download only from this official repository

### Security
- This program only reads Excel files and copies files
- No internet connection required
- All operations are local to your computer
- Source code is open and can be audited

### Build Information
The Windows executable (.exe) is built on Windows 10 and tested on Windows 10/11.
For macOS users, it's recommended to build from source due to potential compatibility issues with pre-built apps.

### Latest Release
Check the [Releases page](https://github.com/Baturalp6/QuickCopy/releases/tag/v1.0.0) for:
- Pre-compiled executables
- Version history
- Change logs
- Installation instructions

## Troubleshooting

### Common Issues
1. **Application won't start**
   - Verify admin privileges
   - Try restarting your system

2. **Excel file not recognized**
   - Ensure file format is .xlsx
   - Verify catalog numbers are in column B

3. **Files not found**
   - Check source directory
   - Verify file naming matches catalog numbers

## License & Rights
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This project is available under the MIT License, which means you can:
- ✅ Download and use the program for free
- ✅ Modify the source code
- ✅ Create your own version
- ✅ Use it in your own projects
- ✅ Share your modified version
- ✅ Use it commercially

If you create your own version, please:
- Fork this repository to your own GitHub account
- Make your modifications there
- Give credit by keeping the MIT License notice

## Acknowledgments
- Built with Python and Tkinter
- Uses pandas for Excel processing
- PyInstaller for creating standalone executables
