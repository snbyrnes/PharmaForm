# Changelog

All notable changes to the HPRA XML Parser project are documented in this file.

## [0.3.0] - 2025-10-19

### Added

- File integrity verification using SHA-256 checksums
- Automatic generation of `checksums.csv` with input and output file hashes
- Command-line option `--no-checksums` to disable checksum generation
- Hash tracking for audit trails and regulatory compliance
- File size and timestamp metadata in checksum records
- Programmatic verification functions in `integrity.py` module

### Changed

- `ConversionResult` now includes `input_sha256` and `output_sha256` fields
- `convert_xml_to_json()` accepts `calculate_checksums` parameter
- CLI displays checksum file location and count after processing

## [0.2.0] - 2025-10-19

### Added

- Automatic quality summary report generation after batch processing
- Excel format reports with professional formatting and color-coded status
- Text format reports for logging and automation
- Command-line options: `--no-report` and `--report-format`
- Comprehensive metrics tracking (counts, success rates, timestamps)
- Per-file processing details with record counts
- Frequent issues analysis for troubleshooting
- Enhanced error and warning detection

### Changed

- `convert_xml_to_json()` now returns detailed conversion results
- CLI tracks metrics during processing and generates reports
- Added openpyxl as a dependency for Excel report generation

## [0.1.0] - Initial Release

### Added

- XML to JSON conversion for HPRA human medicines data
- Namespace removal and attribute preservation
- Optional flattened output for BI tools
- Batch processing mode
- Command-line interface
- PyInstaller bundling support for standalone distribution
