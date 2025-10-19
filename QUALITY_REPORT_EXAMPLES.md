# Quality Report Examples

This document shows examples of running the HPRA parser with different quality report options.

## Example 1: Default Excel Report

```powershell
# Process all XML files and generate Excel quality report
python -m hpra_parser.cli --flatten

# Output includes:
# - JSON files in data/output/
# - Excel report: data/output/quality_report_YYYYMMDD_HHMMSS.xlsx
```

**Console Output:**
```
Processing sample_medicines.xml -> sample_medicines.json (flatten=True)

Completed conversion for 1 of 1 file(s). Warnings: 0, Failures: 0
Output directory: C:\...\data\output

Generating quality summary report...
Quality report (Excel): C:\...\data\output\quality_report_20251019_183627.xlsx
```

## Example 2: Text Report Only

```powershell
# Generate text report instead of Excel
python -m hpra_parser.cli --report-format text
```

## Example 3: Both Excel and Text Reports

```powershell
# Generate both formats for maximum compatibility
python -m hpra_parser.cli --report-format both
```

## Example 4: Disable Reports

```powershell
# Process without generating quality reports
python -m hpra_parser.cli --no-report
```

## Example 5: Custom Directories with Reports

```powershell
# Process from custom locations and generate report
python -m hpra_parser.cli --input "C:\hpra\xml" --output "C:\hpra\json" --flatten
```

## Example Report Contents

### Excel Report Structure

The generated Excel file contains three sheets:

#### 1. Summary Sheet
- Batch start/end times
- Total duration
- File counts (total, successful, skipped, warnings, failures)
- Total records processed
- Success rate percentage

#### 2. Detailed Results Sheet
- Per-file processing details
- Color-coded status (green=success, red=failure, yellow=warning, gray=skipped)
- Timestamps for each file
- Record counts
- Error/warning messages

#### 3. Frequent Issues Sheet
- Most common errors and warnings
- Occurrence counts for each issue
- Useful for identifying systemic problems

### Text Report Example

```
======================================================================
HPRA Parser - Quality Summary Report
======================================================================

Batch Information:
  Start Time: 2025-10-19 18:35:46
  End Time: 2025-10-19 18:35:46
  Duration: 0.50 seconds

Processing Counts:
  Total Files: 10
  Successfully Processed: 8
  Skipped: 0
  Warnings: 1
  Failures: 1
  Total Records: 1250

Success Rate: 80.00%

Most Frequent Issues:

  [5x] XML parse error: mismatched tag
  [3x] No products found in XML file
  [1x] File does not exist
======================================================================
```

## Integration with Audit Systems

### Power BI Integration

1. Open Power BI Desktop
2. Get Data → Excel → Browse to quality report
3. Select all three sheets
4. Create dashboard with:
   - Success rate gauge
   - File status breakdown (pie chart)
   - Timeline of processing (if multiple reports)
   - Top issues table

### Excel Pivot Table Analysis

1. Open quality report in Excel
2. Go to "Detailed Results" sheet
3. Insert → PivotTable
4. Drag "Status" to Rows
5. Drag "Filename" to Values (Count)
6. Analyze processing patterns

### Python Automation

```python
import pandas as pd
from pathlib import Path

# Read quality report
excel_file = "data/output/quality_report_20251019_183627.xlsx"

# Load summary data
summary = pd.read_excel(excel_file, sheet_name="Summary")
details = pd.read_excel(excel_file, sheet_name="Detailed Results")
issues = pd.read_excel(excel_file, sheet_name="Frequent Issues")

# Calculate metrics
success_rate = details[details['Status'] == 'SUCCESS'].shape[0] / len(details)

# Send alert if success rate drops
if success_rate < 0.9:
    print(f"ALERT: Success rate dropped to {success_rate:.1%}")
```

## Archiving Reports

### Daily Archive Script

```powershell
# archive_reports.ps1
$today = Get-Date -Format "yyyy-MM-dd"
$archiveDir = "archive\reports\$today"

# Create archive directory
New-Item -ItemType Directory -Force -Path $archiveDir

# Move today's reports
Move-Item -Path "data\output\quality_report_*.xlsx" -Destination $archiveDir
Move-Item -Path "data\output\quality_report_*.txt" -Destination $archiveDir

Write-Host "Reports archived to: $archiveDir"
```

## Troubleshooting

### Excel File Won't Open

- Check if file is already open in Excel
- Ensure sufficient permissions
- Verify disk space

### No Records Counted

If all files show 0 records:
- Verify XML structure matches expected format
- Check for Products/Product elements in XML
- Review the JSON output to confirm data was parsed

### Large Number of Failures

If you see many failures:
1. Open Excel report
2. Go to "Frequent Issues" sheet
3. Identify the most common error
4. Fix source data or XML structure
5. Reprocess files

## Best Practices

1. **Run with Reports**: Always generate reports for audit trails
2. **Archive Regularly**: Keep reports for compliance (90 days minimum)
3. **Monitor Success Rate**: Investigate if it drops below 95%
4. **Review Issues Weekly**: Check "Frequent Issues" to catch patterns
5. **Use Both Formats**: Excel for analysis, text for automation
