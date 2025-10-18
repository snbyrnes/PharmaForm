# HPRA Parser Bundle

This folder contains a ready-to-run Windows executable for converting HPRA human medicines XML files to JSON.

## Quick Start
- Copy your HPRA XML files into `data\input`.
- Double-click `HPRAParser.exe` (or run it from PowerShell).
- Find the generated JSON files in `data\output`.

The executable already includes Python, so no additional software is required.

## Command-Line Options
Run from PowerShell if you need flags:
```powershell
.\HPRAParser.exe --flatten
.\HPRAParser.exe --input "D:/hpra/input" --output "D:/hpra/output"
```

## Support
For troubleshooting or to rebuild the bundle, see the project documentation at the repository root.
