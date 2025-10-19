# File Integrity Verification Guide

## Overview

The HPRA Parser automatically generates SHA-256 checksums for all input XML files and output JSON files, creating an audit trail that proves files weren't altered post-conversion.

## Features

- **SHA-256 Hashing**: Industry-standard cryptographic hash for file integrity
- **Automatic Generation**: Checksums calculated during processing without manual intervention
- **CSV Export**: All checksums stored in `checksums.csv` for easy auditing
- **Bidirectional Verification**: Tracks both input (XML) and output (JSON) files
- **Timestamp Recording**: Each hash includes generation timestamp
- **File Metadata**: Includes file size for additional verification

## Generated Files

### checksums.csv

Location: Output directory (same as JSON files)

Format:
```csv
timestamp,filename,file_type,sha256_hash,file_size_bytes,relative_path
2025-10-19 19:05:55,sample.xml,input,e939047d...,720,sample.xml
2025-10-19 19:05:55,sample.json,output,5c6f4ba7...,504,sample.json
```

**Columns:**
- `timestamp`: When the hash was generated (YYYY-MM-DD HH:MM:SS)
- `filename`: Name of the file
- `file_type`: Either "input" or "output"
- `sha256_hash`: 64-character hexadecimal SHA-256 hash
- `file_size_bytes`: File size in bytes
- `relative_path`: File path relative to the processing directory

## Usage

### Default Behavior (Checksums Enabled)

```powershell
# Checksums generated automatically
python -m hpra_parser.cli --flatten
```

Output:
```
Processing sample.xml -> sample.json (flatten=True)

Completed conversion for 1 of 1 file(s). Warnings: 0, Failures: 0
Output directory: C:\...\data\output

Integrity checksums: C:\...\data\output\checksums.csv
  Total files hashed: 1 pairs (input + output)
```

### Disable Checksums

```powershell
# Skip checksum generation
python -m hpra_parser.cli --no-checksums
```

## Verification Process

### Manual Verification

To verify a file hasn't been altered:

1. Locate the file's hash in `checksums.csv`
2. Recalculate the hash using any SHA-256 tool
3. Compare the hashes - they must match exactly

**PowerShell Example:**
```powershell
# Get hash of a file
Get-FileHash -Path "data\output\sample.json" -Algorithm SHA256

# Output will show:
# Algorithm       Hash                                                              Path
# ---------       ----                                                              ----
# SHA256          5C6F4BA7AA8BD5268329727F330703A72C3AA1044839161798B4071B80752D99      ...
```

**Python Example:**
```python
import hashlib
from pathlib import Path

def verify_file(filepath, expected_hash):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    
    actual_hash = sha256.hexdigest()
    return actual_hash.lower() == expected_hash.lower()

# Verify a file
result = verify_file("data/output/sample.json", "5c6f4ba7...")
print(f"Integrity verified: {result}")
```

### Automated Verification Script

```python
from hpra_parser.integrity import load_checksums_from_csv, verify_file_integrity
from pathlib import Path

# Load checksums
checksums_file = Path("data/output/checksums.csv")
checksums = load_checksums_from_csv(checksums_file)

# Verify each file
for checksum in checksums:
    file_path = Path("data") / checksum.file_type / checksum.filename
    
    if file_path.exists():
        is_valid = verify_file_integrity(file_path, checksum.sha256_hash)
        status = "✓ VALID" if is_valid else "✗ ALTERED"
        print(f"{status}: {checksum.filename}")
    else:
        print(f"✗ MISSING: {checksum.filename}")
```

## Audit Trail Benefits

### Regulatory Compliance

The checksums.csv file provides:
- **Non-repudiation**: Proves files haven't been modified since conversion
- **Chain of custody**: Timestamps show when processing occurred
- **Data integrity**: Ensures accuracy of converted data
- **Audit evidence**: Verifiable proof for regulatory inspections

### Use Cases

1. **Pharmaceutical Compliance**: Prove data integrity for regulatory submissions
2. **Quality Assurance**: Verify conversions haven't been tampered with
3. **Forensic Analysis**: Investigate suspected data alterations
4. **Archive Verification**: Confirm archived files match originals
5. **Third-party Validation**: Allow auditors to independently verify files

## Integration Examples

### Power BI Dashboard

Import `checksums.csv` to create integrity dashboards:

```
Get Data → Text/CSV → Select checksums.csv
```

Create visuals for:
- Files processed by date
- Input vs output file sizes
- Verification status tracking

### Database Import

```sql
-- Create table
CREATE TABLE file_checksums (
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME,
    filename VARCHAR(255),
    file_type VARCHAR(10),
    sha256_hash CHAR(64),
    file_size_bytes BIGINT,
    relative_path VARCHAR(500)
);

-- Import CSV
LOAD DATA INFILE 'checksums.csv'
INTO TABLE file_checksums
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

### Blockchain Integration

For maximum security, SHA-256 hashes can be stored on blockchain:

```python
# Example: Store hash on blockchain for immutable audit trail
from web3 import Web3

def store_hash_on_blockchain(filename, sha256_hash, timestamp):
    # Connect to blockchain
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    
    # Store hash in smart contract
    # This creates an immutable record that files existed
    # with specific hashes at specific times
    contract.functions.storeHash(
        filename,
        sha256_hash,
        timestamp
    ).transact()
```

## Best Practices

1. **Archive checksums.csv**: Keep checksum files with the processed data
2. **Version Control**: Track checksum files in version control systems
3. **Regular Verification**: Periodically verify file integrity
4. **Backup**: Store checksums separately from data files
5. **Documentation**: Include checksums in data lineage documentation

## Checksum File Management

### Appending vs Overwriting

By default, each run overwrites `checksums.csv`. To maintain history:

```python
from hpra_parser.integrity import write_checksums_csv
from pathlib import Path

# Append to existing file
write_checksums_csv(checksums, Path("checksums.csv"), append=True)
```

### Archiving Checksums

```powershell
# Archive checksums with timestamp
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item "data\output\checksums.csv" "archive\checksums_$timestamp.csv"
```

## Security Considerations

### SHA-256 Properties

- **Collision Resistant**: Virtually impossible to find two files with same hash
- **One-way Function**: Cannot reverse hash to get original file
- **Avalanche Effect**: Small file change produces completely different hash
- **Industry Standard**: NIST-approved, FIPS 180-4 compliant

### Tamper Detection

If a file is modified after hashing:
- Hash verification will fail
- Even one byte change produces different hash
- Modification is immediately detectable

### Limitations

- Checksums don't prevent tampering, only detect it
- Both files and checksums can be altered together (store separately)
- Hash alone doesn't prove file authenticity (use digital signatures for that)

## Troubleshooting

### Checksums Not Generated

**Problem**: No `checksums.csv` file created

**Solutions**:
1. Check you're not using `--no-checksums` flag
2. Verify files were successfully processed
3. Check output directory permissions

### Hash Mismatch

**Problem**: Verification shows hash doesn't match

**Causes**:
1. File was modified after conversion
2. File corruption during transfer
3. Different file with same name

**Action**: Re-process the original XML file

### Missing Checksum Records

**Problem**: Some files missing from `checksums.csv`

**Causes**:
1. Files failed processing (check quality report)
2. Files were skipped (check console output)
3. Checksums disabled for that run

## Command-Line Reference

```
Options:
  --no-checksums    Disable generation of SHA-256 integrity checksums
  
Examples:
  # Generate checksums (default)
  python -m hpra_parser.cli --flatten
  
  # Skip checksums
  python -m hpra_parser.cli --no-checksums
  
  # Process with both quality reports and checksums
  python -m hpra_parser.cli --flatten --report-format both
```

## Programmatic Access

```python
from hpra_parser.integrity import (
    calculate_sha256,
    create_checksum_record,
    write_checksums_csv,
    verify_file_integrity,
    load_checksums_from_csv
)
from pathlib import Path

# Calculate hash for a single file
hash_value = calculate_sha256(Path("myfile.xml"))
print(f"SHA-256: {hash_value}")

# Create checksum record
checksum = create_checksum_record(
    Path("myfile.xml"),
    file_type="input",
    base_dir=Path("data/input")
)

# Verify integrity
is_valid = verify_file_integrity(Path("myfile.xml"), expected_hash)
```

## Summary

The integrity verification feature provides:
- Automatic SHA-256 hash generation for all files
- CSV export for easy auditing and integration
- Tools for verification and validation
- Compliance-ready audit trail
- Protection against undetected file alterations

For audit purposes, always retain `checksums.csv` files alongside your processed data.
