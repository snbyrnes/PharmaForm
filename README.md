# PharmaForm - XML to JSON Parser optimised for medicinal product information



Convert HPRA human medicines XML public exports into clean JSON for analysis and reporting.



## Features## Features

- **Namespace-free JSON**: Removes XML namespaces while preserving attributes and text content.

- Namespace-free JSON output preserving attributes and text content- **Flattened output**: Optional table-friendly JSON with dot-notation keys for BI tools like QuickSight or Excel.

- Optional flattened format for spreadsheets and BI tools- **Batch mode**: Process every XML file dropped into the `data/input` directory with a single command.

- Batch processing mode for multiple files- **Quality Summary Reports**: Automatically generates Excel/text reports with processing counts, issue tracking, and audit-ready timestamps.

- Automated quality summary reports with audit trail- **Zero dependencies**: Pure Python implementation using only the standard library (openpyxl required for Excel reports).

- Standalone Windows executable (no Python installation required)

## Getting Started

## Quick Start (Non-Technical Users)

### Option A: Zero-Dependency Bundle (Recommended)

### Windows Executable- Download or clone this repository and open the `dist/HPRAParser-bundle/` folder.

- Drop HPRA XML files into `dist/HPRAParser-bundle/data/input/`.

1. Download and extract the `HPRAParser-bundle` folder- Double-click `dist/HPRAParser-bundle/HPRAParser.exe` (or run it from PowerShell to pass flags such as `--flatten`).

2. Copy your HPRA XML files into the `data/input` folder- Converted JSON files appear in `dist/HPRAParser-bundle/data/output/` with matching filenames.

3. Double-click `HPRAParser.exe`

4. Find your converted JSON files in the `data/output` folderThe executable already embeds Python, so no additional runtime installs are required.

5. Review the quality report Excel file for processing summary

### Option B: Run with Local Python

### Advanced Options

### 1. Download the repository

Run the executable from PowerShell with additional options:```bash

# HTTPS clone example

```powershellgit clone https://github.com/your-org/hpra-xml-parser.git

# Flatten JSON for easier spreadsheet importcd hpra-xml-parser

.\HPRAParser.exe --flatten```

Or download the ZIP from GitHub and extract it locally.

# Process files from custom locations

.\HPRAParser.exe --input "C:\MyData\XML" --output "C:\MyData\JSON"### 2. Prepare a Python environment

Use a recent Python 3.9+ interpreter. Optionally create a virtual environment:

# Disable quality reports```bash

.\HPRAParser.exe --no-reportpython -m venv .venv

```.venv\Scripts\activate  # Windows PowerShell

# source .venv/bin/activate  # macOS / Linux

## Installation (Technical Users)```



### Requirements### 3. Add HPRA XML files

Place the XML files you want to convert into:

- Python 3.9 or higher```

- openpyxl (for Excel quality reports)<repo-root>/data/input

```

### Install from RepositoryIf the `data` folders are missing, the parser will create them automatically when it runs.



```bash### 4. Run the parser

git clone https://github.com/snbyrnes/PharmaForm.gitUse the trigger script to convert everything in `data/input` to JSON files in `data/output`:

cd PharmaForm```bash

python -m pip install -e .python trigger/run_parser.py

``````

Pass `--flatten` to emit flattened JSON records instead of the nested structure:

### Basic Usage```bash

python trigger/run_parser.py --flatten

```bash```

# Place XML files in data/input, then run:

python -m hpra_parser.cli### 5. Review results

The generated JSON files appear under `data/output` with the same base filenames as the inputs.

# Or use the trigger script:

python trigger/run_parser.py## Windows Bundle (No Python Required)

```

Create a standalone `HPRAParser.exe` that ships with its own Python runtime and ready-to-use `data` folders:

## Command-Line Options

1. On a Windows build machine with Python 3.9+ installed, open PowerShell, change into the repository, and run:

```   ```powershell

usage: hpra-xml-parser [-h] [--flatten] [--input INPUT] [--output OUTPUT]   powershell -ExecutionPolicy Bypass -File trigger/build_bundle.ps1

                       [--no-report] [--report-format {excel,text,both}]   ```

                       [files ...]   The script installs or upgrades PyInstaller automatically. Add `-Python "C:/Path/To/python.exe"` if you need a specific interpreter, or `-SkipInstall` to reuse an existing PyInstaller install.

2. The script generates `dist/HPRAParser.exe` and assembles a shareable `dist/HPRAParser-bundle/` directory containing the executable plus ready-to-use `data/input` and `data/output` folders.

Options:3. Zip the `HPRAParser-bundle` directory and distribute it to end users.

  files                 Specific XML files to process (optional)4. End users unzip the bundle, drop XML files into `data/input`, and run `HPRAParser.exe` (pass flags such as `--flatten` the same way) — no Python installation needed.

  --flatten             Output flattened JSON for BI tools

  --input INPUT         Custom input directory## Advanced Usage

  --output OUTPUT       Custom output directory- Process specific files only:

  --no-report           Disable quality summary report  ```bash

  --report-format       Report format: excel, text, or both (default: excel)  python trigger/run_parser.py latestHumanlist.xml another.xml

```  ```

- Override input/output directories:

## Advanced Usage for Analytics  ```bash

  python trigger/run_parser.py --input "C:/data/hpra" --output "C:/data/hpra-json"

### Flattened JSON for Business Intelligence  ```

- Generate quality summary reports (default: Excel format):

The `--flatten` option produces table-friendly JSON optimized for tools like Power BI, Tableau, and Excel:  ```bash

  python trigger/run_parser.py --flatten

```bash  # Creates: data/output/quality_report_YYYYMMDD_HHMMSS.xlsx

python -m hpra_parser.cli --flatten  ```

```- Disable quality reports:

  ```bash

Output structure:  python trigger/run_parser.py --no-report

- Nested objects become dot-notation keys (e.g., `Product.Name`)  ```

- Arrays are indexed (e.g., `Ingredient[0].Name`)- Generate text format reports:

- Suitable for direct import into spreadsheets and databases  ```bash

  python trigger/run_parser.py --report-format text

### Batch Processing Multiple Files  ```

- The bundled executable accepts the same flags:

```bash  ```powershell

# Process all XML files in a directory  .\HPRAParser.exe --flatten --input "D:/hpra/input" --output "D:/hpra/output"

python -m hpra_parser.cli --input "/path/to/xml/files" --flatten  ```

- Install the package locally (optional):

# Process specific files only  ```bash

python -m hpra_parser.cli file1.xml file2.xml --flatten  python -m pip install -e .

```  python -m hpra_parser.cli --flatten

  ```

### Quality Reports for Audit and Compliance

## Quality Summary Reports

Quality reports are automatically generated in the output directory:

After each batch, the parser generates comprehensive quality reports perfect for audit dashboards and compliance tracking:

**Excel Report Includes:**

- Summary metrics (success rate, file counts, processing time)- **Processing Counts**: Successful, skipped, warnings, failures

- Per-file detailed results with color-coded status- **Detailed Results**: Per-file status with timestamps and error messages

- Frequent issues analysis for troubleshooting- **Frequent Issues**: Top errors/warnings with occurrence counts

- **Excel Format**: Color-coded sheets with professional formatting

**Example:**- **Text Format**: Plain text alternative for logs and email

```bash

python -m hpra_parser.cli --flatten --report-format bothFor detailed documentation, see [Quality Report Guide](QUALITY_REPORT_GUIDE.md).

# Creates: quality_report_YYYYMMDD_HHMMSS.xlsx

#          quality_report_YYYYMMDD_HHMMSS.txt## Project Structure

``````

hpra-xml-parser/

### Integration with BI Tools├─ hpra_parser/              # Reusable parsing library

│  ├─ __init__.py

**Power BI:**│  ├─ cli.py                 # Command-line interface

```│  ├─ converter.py           # XML → JSON conversion helpers

Get Data → Excel → Select quality_report_*.xlsx│  └─ quality_report.py      # Quality summary report generation

Load all sheets for complete dashboard├─ dist/

```│  ├─ HPRAParser-bundle/     # Prebuilt executable and data folders (zero-dependency)

│  └─ HPRAParser.exe         # Raw PyInstaller output (copied into the bundle)

**Python Automation:**├─ trigger/

```python│  └─ run_parser.py          # Desktop-friendly entrypoint

from hpra_parser.quality_report import BatchMetrics, generate_excel_report├─ data/

from pathlib import Path│  ├─ input/                 # Drop XML files here

│  └─ output/                # JSON output and quality reports appear here

# Programmatic access to reporting├─ QUALITY_REPORT_GUIDE.md   # Detailed quality report documentation

metrics = BatchMetrics()└─ README.md

# ... add results ...```

generate_excel_report(metrics, Path("report.xlsx"))

```## Notes



**Scheduled Processing:**1. This tool is not associated with, or validated by the HPRA.

```powershell2. Please contribute by using the issues function to report bugs and suggest enhancements.

# Windows Task Scheduler script   

cd C:\PharmaForm
python -m hpra_parser.cli --flatten --report-format both
# Archive reports as needed
```

## Quality Report Details

Quality reports track:
- Total files processed vs. skipped/failed
- Processing duration and timestamps
- Record counts per file
- Most frequent errors/warnings
- Success rate percentage

Status codes:
- **success** - File processed without issues
- **warning** - Processed with non-critical warnings
- **failure** - Processing failed due to errors
- **skipped** - File skipped (invalid format, missing, etc.)

For detailed documentation, see [QUALITY_REPORT_GUIDE.md](QUALITY_REPORT_GUIDE.md).

## Building Standalone Executable

Create a Windows executable bundle for distribution:

```powershell
# Build with PyInstaller
powershell -ExecutionPolicy Bypass -File trigger/build_bundle.ps1

# Output: dist/HPRAParser-bundle/ (ready to zip and distribute)
```

The bundle includes:
- HPRAParser.exe (standalone executable)
- data/input and data/output folders
- No Python installation required on target machine

## Project Structure

```
PharmaForm/
├── hpra_parser/              # Core library
│   ├── cli.py                # Command-line interface
│   ├── converter.py          # XML to JSON conversion
│   └── quality_report.py     # Report generation
├── data/
│   ├── input/                # XML files (source)
│   └── output/               # JSON files and reports
├── trigger/
│   ├── run_parser.py         # Convenience script
│   └── build_bundle.ps1      # Executable builder
└── dist/
    └── HPRAParser-bundle/    # Distributable package
```

## Notes

This tool is an independent utility and is not associated with or validated by the Health Products Regulatory Authority (HPRA).

For issues or feature requests, please use the GitHub issues tracker.
