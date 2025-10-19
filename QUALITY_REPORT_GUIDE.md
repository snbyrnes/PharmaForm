# Quality Summary Report Guide

## Overview

The HPRA Parser automatically generates comprehensive quality summary reports after each batch processing run. These reports are designed for audit dashboards, compliance tracking, and operational monitoring.

## Features

### Report Contents

- **Processing Counts**: Total files, successful conversions, skipped files, warnings, and failures
- **Detailed Results**: Per-file status with timestamps, record counts, and error messages
- **Frequent Issues**: Top issues encountered during processing for quick troubleshooting
- **Batch Metadata**: Start/end timestamps, duration, and success rate

### Report Formats

#### Excel Format (Default)
- **Filename**: `quality_report_YYYYMMDD_HHMMSS.xlsx`
- **Location**: Output directory (same as JSON files)
- **Sheets**:
  - **Summary**: High-level metrics and batch information
  - **Detailed Results**: Per-file processing details with color-coded status
  - **Frequent Issues**: Most common errors/warnings with occurrence counts

#### Text Format (Alternative)
- **Filename**: `quality_report_YYYYMMDD_HHMMSS.txt`
- **Location**: Output directory
- **Content**: Plain text summary suitable for logs or email

## Usage

### Basic Usage

By default, Excel reports are generated automatically:

```powershell
hpra-xml-parser
```

Or if running from source:

```powershell
python -m hpra_parser.cli
```

### Command-Line Options

#### Disable Report Generation

```powershell
hpra-xml-parser --no-report
```

#### Choose Report Format

```powershell
# Excel format (default)
hpra-xml-parser --report-format excel

# Text format
hpra-xml-parser --report-format text

# Generate both formats
hpra-xml-parser --report-format both
```

#### Combined with Other Options

```powershell
# Process with flattened JSON and text report
hpra-xml-parser --flatten --report-format text

# Process specific files with Excel report
hpra-xml-parser file1.xml file2.xml --report-format excel

# Custom directories with report
hpra-xml-parser --input C:\data\xml --output C:\data\json
```

## Excel Report Details

### Summary Sheet

| Metric | Description |
|--------|-------------|
| Start Time | When batch processing began |
| End Time | When batch processing completed |
| Duration | Total processing time in seconds |
| Total Files | Number of XML files encountered |
| Successfully Processed | Files converted without errors |
| Skipped | Files skipped (invalid format, etc.) |
| Warnings | Files processed but with warnings |
| Failures | Files that failed to process |
| Total Records | Total product records across all files |
| Success Rate | Percentage of successful conversions |

### Detailed Results Sheet

Color-coded per-file information:
- **Green**: Successful processing
- **Red**: Failed processing
- **Yellow**: Processed with warnings
- **Gray**: Skipped files

Columns:
- Filename
- Status
- Timestamp
- Records processed
- Error/Warning message

### Frequent Issues Sheet

Lists the most common issues with occurrence counts, helping identify:
- Recurring data quality problems
- Systemic parsing issues
- Files requiring manual intervention

## Integration with Audit Dashboards

### Excel Integration

1. **Power BI**: Import Excel files directly for automated dashboards
2. **Tableau**: Connect to Excel data source for visualization
3. **Excel Pivot Tables**: Use detailed results for custom analysis

### Programmatic Access

The quality report module can be used programmatically:

```python
from hpra_parser.quality_report import BatchMetrics, ProcessingResult, generate_excel_report
from datetime import datetime
from pathlib import Path

# Create metrics
metrics = BatchMetrics()

# Add results
result = ProcessingResult(
    filename="example.xml",
    status="success",
    timestamp=datetime.now(),
    records_processed=150
)
metrics.add_result(result)

# Finalize and generate report
metrics.finalize()
generate_excel_report(metrics, Path("output/report.xlsx"))
```

## Status Definitions

| Status | Description |
|--------|-------------|
| **success** | File processed successfully without issues |
| **warning** | File processed but with warnings (e.g., no products found) |
| **failure** | File failed to process due to errors |
| **skipped** | File skipped (not an XML file, doesn't exist, etc.) |

## Troubleshooting

### Excel Reports Not Generated

If you see: "Warning: openpyxl not available"

**Solution**: Install openpyxl dependency:

```powershell
pip install openpyxl
```

Or reinstall the package with dependencies:

```powershell
pip install -e .
```

### Report Files Not Found

Reports are saved in the output directory with timestamps. Check:

```powershell
ls data/output/quality_report_*.xlsx
```

### Permission Errors

If you get permission errors writing reports:
- Ensure the output directory is writable
- Close any open Excel files with the same name
- Check disk space

## Examples

### Example 1: Daily Batch Processing

```powershell
# Process all XML files and generate Excel report
hpra-xml-parser --flatten

# Check the report
ls data/output/quality_report_*.xlsx | select -First 1
```

### Example 2: Audit Trail

```powershell
# Generate both Excel and text reports for archive
hpra-xml-parser --report-format both

# Archive reports
mkdir archive\reports\2025-10-19
move data\output\quality_report_*.* archive\reports\2025-10-19\
```

### Example 3: Error Investigation

```powershell
# Process files
hpra-xml-parser

# Open Excel report
# Navigate to "Frequent Issues" sheet
# Identify top error patterns
# Fix source data and reprocess
```

## Best Practices

1. **Keep Reports**: Archive quality reports for compliance and audit trails
2. **Monitor Trends**: Track success rates over time to identify data quality issues
3. **Review Frequent Issues**: Regularly check the "Frequent Issues" sheet to identify recurring problems
4. **Automate Alerts**: Use report metrics to trigger alerts when success rate drops
5. **Document Actions**: Use reports to document remediation actions taken

## Report Retention

Recommended retention policies:
- **Daily Reports**: Keep for 90 days
- **Weekly Summaries**: Keep for 1 year
- **Monthly Archives**: Keep for 7 years (or per regulatory requirements)

## Support

For issues or questions about quality reports:
1. Check this guide for common solutions
2. Review the example reports in the output directory
3. Check error messages in the console output
