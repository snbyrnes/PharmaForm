"""File integrity verification using SHA-256 hashes for audit trails."""

from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class FileChecksum:
    """Checksum information for a file."""
    filename: str
    file_type: str  # 'input' or 'output'
    sha256_hash: str
    file_size: int
    timestamp: datetime
    relative_path: Optional[str] = None


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file to hash
        
    Returns:
        Hexadecimal string representation of SHA-256 hash
    """
    sha256_hash = hashlib.sha256()
    
    with open(file_path, "rb") as f:
        # Read file in chunks to handle large files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


def create_checksum_record(
    file_path: Path,
    file_type: str,
    base_dir: Optional[Path] = None
) -> FileChecksum:
    """Create a checksum record for a file.
    
    Args:
        file_path: Path to the file
        file_type: Type of file ('input' or 'output')
        base_dir: Base directory for calculating relative path
        
    Returns:
        FileChecksum record with hash and metadata
    """
    sha256_hash = calculate_sha256(file_path)
    file_size = file_path.stat().st_size
    timestamp = datetime.now()
    
    relative_path = None
    if base_dir:
        try:
            relative_path = str(file_path.relative_to(base_dir))
        except ValueError:
            # File is not relative to base_dir
            relative_path = file_path.name
    
    return FileChecksum(
        filename=file_path.name,
        file_type=file_type,
        sha256_hash=sha256_hash,
        file_size=file_size,
        timestamp=timestamp,
        relative_path=relative_path
    )


def write_checksums_csv(
    checksums: List[FileChecksum],
    output_path: Path,
    append: bool = False
) -> None:
    """Write checksums to a CSV file.
    
    Args:
        checksums: List of FileChecksum records
        output_path: Path to the output CSV file
        append: If True, append to existing file; otherwise overwrite
    """
    mode = 'a' if append else 'w'
    file_exists = output_path.exists() and append
    
    with open(output_path, mode, newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'timestamp',
            'filename',
            'file_type',
            'sha256_hash',
            'file_size_bytes',
            'relative_path'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is new or being overwritten
        if not file_exists:
            writer.writeheader()
        
        for checksum in checksums:
            writer.writerow({
                'timestamp': checksum.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'filename': checksum.filename,
                'file_type': checksum.file_type,
                'sha256_hash': checksum.sha256_hash,
                'file_size_bytes': checksum.file_size,
                'relative_path': checksum.relative_path or checksum.filename
            })


def verify_file_integrity(file_path: Path, expected_hash: str) -> bool:
    """Verify a file's integrity by comparing its hash.
    
    Args:
        file_path: Path to the file to verify
        expected_hash: Expected SHA-256 hash (hex string)
        
    Returns:
        True if hash matches, False otherwise
    """
    actual_hash = calculate_sha256(file_path)
    return actual_hash.lower() == expected_hash.lower()


def load_checksums_from_csv(csv_path: Path) -> List[FileChecksum]:
    """Load checksum records from a CSV file.
    
    Args:
        csv_path: Path to the checksums CSV file
        
    Returns:
        List of FileChecksum records
    """
    checksums = []
    
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
            
            checksum = FileChecksum(
                filename=row['filename'],
                file_type=row['file_type'],
                sha256_hash=row['sha256_hash'],
                file_size=int(row['file_size_bytes']),
                timestamp=timestamp,
                relative_path=row.get('relative_path')
            )
            checksums.append(checksum)
    
    return checksums
