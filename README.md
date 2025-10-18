# HPRA XML Parser

Convert HPRA human medicines XML exports into clean JSON, ready for analysis.

## Features
- **Namespace-free JSON**: Removes XML namespaces while preserving attributes and text content.
- **Flattened output**: Optional table-friendly JSON with dot-notation keys for BI tools like QuickSight or Excel.
- **Batch mode**: Process every XML file dropped into the `data/input` directory with a single command.
- **Zero dependencies**: Pure Python implementation using only the standard library.

## Getting Started

### Option A: Zero-Dependency Bundle (Recommended)
- Download or clone this repository and open the `dist/HPRAParser-bundle/` folder.
- Drop HPRA XML files into `dist/HPRAParser-bundle/data/input/`.
- Double-click `dist/HPRAParser-bundle/HPRAParser.exe` (or run it from PowerShell to pass flags such as `--flatten`).
- Converted JSON files appear in `dist/HPRAParser-bundle/data/output/` with matching filenames.

The executable already embeds Python, so no additional runtime installs are required.

### Option B: Run with Local Python

### 1. Download the repository
```bash
# HTTPS clone example
git clone https://github.com/your-org/hpra-xml-parser.git
cd hpra-xml-parser
```
Or download the ZIP from GitHub and extract it locally.

### 2. Prepare a Python environment
Use a recent Python 3.9+ interpreter. Optionally create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell
# source .venv/bin/activate  # macOS / Linux
```

### 3. Add HPRA XML files
Place the XML files you want to convert into:
```
<repo-root>/data/input
```
If the `data` folders are missing, the parser will create them automatically when it runs.

### 4. Run the parser
Use the trigger script to convert everything in `data/input` to JSON files in `data/output`:
```bash
python trigger/run_parser.py
```
Pass `--flatten` to emit flattened JSON records instead of the nested structure:
```bash
python trigger/run_parser.py --flatten
```

### 5. Review results
The generated JSON files appear under `data/output` with the same base filenames as the inputs.

## Windows Bundle (No Python Required)

Create a standalone `HPRAParser.exe` that ships with its own Python runtime and ready-to-use `data` folders:

1. On a Windows build machine with Python 3.9+ installed, open PowerShell, change into the repository, and run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File trigger/build_bundle.ps1
   ```
   The script installs or upgrades PyInstaller automatically. Add `-Python "C:/Path/To/python.exe"` if you need a specific interpreter, or `-SkipInstall` to reuse an existing PyInstaller install.
2. The script generates `dist/HPRAParser.exe` and assembles a shareable `dist/HPRAParser-bundle/` directory containing the executable plus ready-to-use `data/input` and `data/output` folders.
3. Zip the `HPRAParser-bundle` directory and distribute it to end users.
4. End users unzip the bundle, drop XML files into `data/input`, and run `HPRAParser.exe` (pass flags such as `--flatten` the same way) — no Python installation needed.

## Advanced Usage
- Process specific files only:
  ```bash
  python trigger/run_parser.py latestHumanlist.xml another.xml
  ```
- Override input/output directories:
  ```bash
  python trigger/run_parser.py --input "C:/data/hpra" --output "C:/data/hpra-json"
  ```
- The bundled executable accepts the same flags:
  ```powershell
  .\HPRAParser.exe --flatten --input "D:/hpra/input" --output "D:/hpra/output"
  ```
- Install the package locally (optional):
  ```bash
  python -m pip install -e .
  python -m hpra_parser.cli --flatten
  ```

## Project Structure
```
hpra-xml-parser/
├─ hpra_parser/           # Reusable parsing library
│  ├─ __init__.py
│  ├─ cli.py              # Command-line interface
│  └─ converter.py        # XML → JSON conversion helpers
├─ dist/
│  ├─ HPRAParser-bundle/  # Prebuilt executable and data folders (zero-dependency)
│  └─ HPRAParser.exe      # Raw PyInstaller output (copied into the bundle)
├─ trigger/
│  └─ run_parser.py       # Desktop-friendly entrypoint
├─ data/
│  ├─ input/              # Drop XML files here
│  └─ output/             # JSON output appears here
└─ README.md
```