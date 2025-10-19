# HPRA XML Parser# HPRA XML Parser# HPRA XML Parser



Convert HPRA human medicines XML exports into clean JSON for analysis and reporting.



## FeaturesConvert HPRA human medicines XML exports into clean JSON for analysis and reporting.Convert publicy available HPRA human medicines XML exports into clean JSON, ready for analysis.



- Namespace-free JSON output preserving attributes and text content

- Optional flattened format for spreadsheets and BI tools

- Batch processing mode for multiple files## Features## Features

- Automated quality summary reports with audit trail

- SHA-256 integrity checksums for input and output files- **Namespace-free JSON**: Removes XML namespaces while preserving attributes and text content.

- Standalone Windows executable (no Python installation required)

- Namespace-free JSON output preserving attributes and text content- **Flattened output**: Optional table-friendly JSON with dot-notation keys for BI tools like QuickSight or Excel.

## Quick Start (Non-Technical Users)

- Optional flattened format for spreadsheets and BI tools- **Batch mode**: Process every XML file dropped into the `data/input` directory with a single command.

### Windows Executable

- Batch processing mode for multiple files- **Quality Summary Reports**: Automatically generates Excel/text reports with processing counts, issue tracking, and audit-ready timestamps.

1. Download and extract the `HPRAParser-bundle` folder

2. Copy your HPRA XML files into the `data/input` folder- Automated quality summary reports with audit trail- **Zero dependencies**: Pure Python implementation using only the standard library (openpyxl required for Excel reports).

3. Double-click `HPRAParser.exe`

4. Find your converted JSON files in the `data/output` folder- Standalone Windows executable (no Python installation required)

5. Review the quality report Excel file for processing summary

6. Check `checksums.csv` for file integrity verification## Getting Started



### Advanced Options## Quick Start (Non-Technical Users)



Run the executable from PowerShell with additional options:### Option A: Zero-Dependency Bundle (Recommended)



```powershell### Windows Executable- Download or clone this repository and open the `dist/HPRAParser-bundle/` folder.

# Flatten JSON for easier spreadsheet import

.\HPRAParser.exe --flatten- Drop HPRA XML files into `dist/HPRAParser-bundle/data/input/`.



# Process files from custom locations1. Download and extract the `HPRAParser-bundle` folder- Double-click `dist/HPRAParser-bundle/HPRAParser.exe` (or run it from PowerShell to pass flags such as `--flatten`).

.\HPRAParser.exe --input "C:\MyData\XML" --output "C:\MyData\JSON"

2. Copy your HPRA XML files into the `data/input` folder- Converted JSON files appear in `dist/HPRAParser-bundle/data/output/` with matching filenames.

# Disable quality reports

.\HPRAParser.exe --no-report3. Double-click `HPRAParser.exe`



# Disable integrity checksums4. Find your converted JSON files in the `data/output` folderThe executable already embeds Python, so no additional runtime installs are required.

.\HPRAParser.exe --no-checksums

```5. Review the quality report Excel file for processing summary



## Installation (Technical Users)### Option B: Run with Local Python



### Requirements### Advanced Options



- Python 3.9 or higher### 1. Download the repository

- openpyxl (for Excel quality reports)

Run the executable from PowerShell with additional options:```bash

### Install from Repository

# HTTPS clone example

```bash

git clone https://github.com/snbyrnes/PharmaForm.git```powershellgit clone https://github.com/your-org/hpra-xml-parser.git

cd PharmaForm

python -m pip install -e .# Flatten JSON for easier spreadsheet importcd hpra-xml-parser

```

.\HPRAParser.exe --flatten```

### Basic Usage

Or download the ZIP from GitHub and extract it locally.

```bash

# Place XML files in data/input, then run:# Process files from custom locations

python -m hpra_parser.cli

.\HPRAParser.exe --input "C:\MyData\XML" --output "C:\MyData\JSON"### 2. Prepare a Python environment

# Or use the trigger script:

python trigger/run_parser.pyUse a recent Python 3.9+ interpreter. Optionally create a virtual environment:

```

# Disable quality reports```bash

## Command-Line Options

.\HPRAParser.exe --no-reportpython -m venv .venv

```

usage: hpra-xml-parser [-h] [--flatten] [--input INPUT] [--output OUTPUT]```.venv\Scripts\activate  # Windows PowerShell

                       [--no-report] [--report-format {excel,text,both}]

                       [--no-checksums] [files ...]# source .venv/bin/activate  # macOS / Linux



Options:## Installation (Technical Users)```

  files                 Specific XML files to process (optional)

  --flatten             Output flattened JSON for BI tools

  --input INPUT         Custom input directory

  --output OUTPUT       Custom output directory### Requirements### 3. Add HPRA XML files

  --no-report           Disable quality summary report

  --report-format       Report format: excel, text, or both (default: excel)Place the XML files you want to convert into:

  --no-checksums        Disable SHA-256 integrity checksums

```- Python 3.9 or higher```



## Advanced Usage for Analytics- openpyxl (for Excel quality reports)<repo-root>/data/input



### Flattened JSON for Business Intelligence```



The `--flatten` option produces table-friendly JSON optimized for tools like Power BI, Tableau, and Excel:### Install from RepositoryIf the `data` folders are missing, the parser will create them automatically when it runs.



```bash

python -m hpra_parser.cli --flatten

``````bash### 4. Run the parser



Output structure:git clone https://github.com/snbyrnes/PharmaForm.gitUse the trigger script to convert everything in `data/input` to JSON files in `data/output`:

- Nested objects become dot-notation keys (e.g., `Product.Name`)

- Arrays are indexed (e.g., `Ingredient[0].Name`)cd PharmaForm```bash

- Suitable for direct import into spreadsheets and databases

python -m pip install -e .python trigger/run_parser.py

### Batch Processing Multiple Files

``````

```bash

# Process all XML files in a directoryPass `--flatten` to emit flattened JSON records instead of the nested structure:

python -m hpra_parser.cli --input "/path/to/xml/files" --flatten

### Basic Usage```bash

# Process specific files only

python -m hpra_parser.cli file1.xml file2.xml --flattenpython trigger/run_parser.py --flatten

```

```bash```

### Quality Reports for Audit and Compliance

# Place XML files in data/input, then run:

Quality reports are automatically generated in the output directory:

python -m hpra_parser.cli### 5. Review results

**Excel Report Includes:**

- Summary metrics (success rate, file counts, processing time)The generated JSON files appear under `data/output` with the same base filenames as the inputs.

- Per-file detailed results with color-coded status

- Frequent issues analysis for troubleshooting# Or use the trigger script:



**Example:**python trigger/run_parser.py## Windows Bundle (No Python Required)

```bash

python -m hpra_parser.cli --flatten --report-format both```

# Creates: quality_report_YYYYMMDD_HHMMSS.xlsx

#          quality_report_YYYYMMDD_HHMMSS.txtCreate a standalone `HPRAParser.exe` that ships with its own Python runtime and ready-to-use `data` folders:

```

## Command-Line Options

### File Integrity Verification

1. On a Windows build machine with Python 3.9+ installed, open PowerShell, change into the repository, and run:

SHA-256 checksums are automatically generated for all input and output files:

```   ```powershell

**checksums.csv Format:**

```csvusage: hpra-xml-parser [-h] [--flatten] [--input INPUT] [--output OUTPUT]   powershell -ExecutionPolicy Bypass -File trigger/build_bundle.ps1

timestamp,filename,file_type,sha256_hash,file_size_bytes,relative_path

2025-10-19 19:05:55,sample.xml,input,e939047d...,720,sample.xml                       [--no-report] [--report-format {excel,text,both}]   ```

2025-10-19 19:05:55,sample.json,output,5c6f4ba7...,504,sample.json

```                       [files ...]   The script installs or upgrades PyInstaller automatically. Add `-Python "C:/Path/To/python.exe"` if you need a specific interpreter, or `-SkipInstall` to reuse an existing PyInstaller install.



**Verify File Integrity:**2. The script generates `dist/HPRAParser.exe` and assembles a shareable `dist/HPRAParser-bundle/` directory containing the executable plus ready-to-use `data/input` and `data/output` folders.

```powershell

# PowerShellOptions:3. Zip the `HPRAParser-bundle` directory and distribute it to end users.

Get-FileHash -Path "data\output\sample.json" -Algorithm SHA256

# Compare hash with value in checksums.csv  files                 Specific XML files to process (optional)4. End users unzip the bundle, drop XML files into `data/input`, and run `HPRAParser.exe` (pass flags such as `--flatten` the same way) — no Python installation needed.

```

  --flatten             Output flattened JSON for BI tools

**Use Cases:**

- Prove files weren't altered post-conversion  --input INPUT         Custom input directory## Advanced Usage

- Regulatory compliance and audit trails

- Chain of custody documentation  --output OUTPUT       Custom output directory- Process specific files only:

- Forensic analysis

  --no-report           Disable quality summary report  ```bash

For detailed documentation, see [FILE_INTEGRITY_GUIDE.md](FILE_INTEGRITY_GUIDE.md).

  --report-format       Report format: excel, text, or both (default: excel)  python trigger/run_parser.py latestHumanlist.xml another.xml

### Integration with BI Tools

```  ```

**Power BI:**

```- Override input/output directories:

Get Data → Excel → Select quality_report_*.xlsx

Load all sheets for complete dashboard## Advanced Usage for Analytics  ```bash



Import checksums.csv for integrity tracking  python trigger/run_parser.py --input "C:/data/hpra" --output "C:/data/hpra-json"

```

### Flattened JSON for Business Intelligence  ```

**Python Automation:**

```python- Generate quality summary reports (default: Excel format):

from hpra_parser.quality_report import BatchMetrics, generate_excel_report

from hpra_parser.integrity import verify_file_integrityThe `--flatten` option produces table-friendly JSON optimized for tools like Power BI, Tableau, and Excel:  ```bash

from pathlib import Path

  python trigger/run_parser.py --flatten

# Programmatic access to reporting

metrics = BatchMetrics()```bash  # Creates: data/output/quality_report_YYYYMMDD_HHMMSS.xlsx

# ... add results ...

generate_excel_report(metrics, Path("report.xlsx"))python -m hpra_parser.cli --flatten  ```



# Verify file integrity```- Disable quality reports:

is_valid = verify_file_integrity(Path("file.json"), "expected_hash")

```  ```bash



**Scheduled Processing:**Output structure:  python trigger/run_parser.py --no-report

```powershell

# Windows Task Scheduler script- Nested objects become dot-notation keys (e.g., `Product.Name`)  ```

cd C:\PharmaForm

python -m hpra_parser.cli --flatten --report-format both- Arrays are indexed (e.g., `Ingredient[0].Name`)- Generate text format reports:

# Archive reports and checksums as needed

```- Suitable for direct import into spreadsheets and databases  ```bash



## Quality Report Details  python trigger/run_parser.py --report-format text



Quality reports track:### Batch Processing Multiple Files  ```

- Total files processed vs. skipped/failed

- Processing duration and timestamps- The bundled executable accepts the same flags:

- Record counts per file

- Most frequent errors/warnings```bash  ```powershell

- Success rate percentage

# Process all XML files in a directory  .\HPRAParser.exe --flatten --input "D:/hpra/input" --output "D:/hpra/output"

Status codes:

- **success** - File processed without issuespython -m hpra_parser.cli --input "/path/to/xml/files" --flatten  ```

- **warning** - Processed with non-critical warnings

- **failure** - Processing failed due to errors- Install the package locally (optional):

- **skipped** - File skipped (invalid format, missing, etc.)

# Process specific files only  ```bash

For detailed documentation, see [QUALITY_REPORT_GUIDE.md](QUALITY_REPORT_GUIDE.md).

python -m hpra_parser.cli file1.xml file2.xml --flatten  python -m pip install -e .

## Building Standalone Executable

```  python -m hpra_parser.cli --flatten

Create a Windows executable bundle for distribution:

  ```

```powershell

# Build with PyInstaller### Quality Reports for Audit and Compliance

powershell -ExecutionPolicy Bypass -File trigger/build_bundle.ps1

## Quality Summary Reports

# Output: dist/HPRAParser-bundle/ (ready to zip and distribute)

```Quality reports are automatically generated in the output directory:



The bundle includes:After each batch, the parser generates comprehensive quality reports perfect for audit dashboards and compliance tracking:

- HPRAParser.exe (standalone executable)

- data/input and data/output folders**Excel Report Includes:**

- No Python installation required on target machine

- Summary metrics (success rate, file counts, processing time)- **Processing Counts**: Successful, skipped, warnings, failures

## Project Structure

- Per-file detailed results with color-coded status- **Detailed Results**: Per-file status with timestamps and error messages

```

PharmaForm/- Frequent issues analysis for troubleshooting- **Frequent Issues**: Top errors/warnings with occurrence counts

├── hpra_parser/              # Core library

│   ├── cli.py                # Command-line interface- **Excel Format**: Color-coded sheets with professional formatting

│   ├── converter.py          # XML to JSON conversion

│   ├── quality_report.py     # Report generation**Example:**- **Text Format**: Plain text alternative for logs and email

│   └── integrity.py          # SHA-256 checksums

├── data/```bash

│   ├── input/                # XML files (source)

│   └── output/               # JSON files, reports, checksumspython -m hpra_parser.cli --flatten --report-format bothFor detailed documentation, see [Quality Report Guide](QUALITY_REPORT_GUIDE.md).

├── trigger/

│   ├── run_parser.py         # Convenience script# Creates: quality_report_YYYYMMDD_HHMMSS.xlsx

│   └── build_bundle.ps1      # Executable builder

└── dist/#          quality_report_YYYYMMDD_HHMMSS.txt## Project Structure

    └── HPRAParser-bundle/    # Distributable package

`````````



## Noteshpra-xml-parser/



This tool is an independent utility and is not associated with or validated by the Health Products Regulatory Authority (HPRA).### Integration with BI Tools├─ hpra_parser/              # Reusable parsing library



For issues or feature requests, please use the GitHub issues tracker.│  ├─ __init__.py


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
