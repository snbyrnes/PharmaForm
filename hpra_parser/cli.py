"""Command-line utilities for running the HPRA XML parser."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List
from xml.etree import ElementTree as ET

from .converter import convert_xml_to_json
from .quality_report import (
    BatchMetrics,
    ProcessingResult,
    generate_excel_report,
    generate_text_report,
    OPENPYXL_AVAILABLE,
)


def get_runtime_root() -> Path:
    """Return the directory that should be treated as the project root."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def default_input_dir() -> Path:
    return get_runtime_root() / "data" / "input"


def default_output_dir() -> Path:
    return get_runtime_root() / "data" / "output"


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert HPRA XML files placed in data/input into JSON files under data/output."
    )
    parser.add_argument(
        "--flatten",
        action="store_true",
        help="Emit flattened JSON suitable for spreadsheets/BI tools.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Override the input directory containing XML files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Override the output directory for JSON files.",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Disable generation of quality summary report.",
    )
    parser.add_argument(
        "--report-format",
        choices=["excel", "text", "both"],
        default="excel",
        help="Format for quality summary report (default: excel).",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Optional specific XML files to process (relative to the input directory unless absolute).",
    )
    return parser.parse_args(argv)


def resolve_targets(input_dir: Path, selected_files: List[Path]) -> List[Path]:
    input_dir = input_dir.resolve()
    if selected_files:
        targets: List[Path] = []
        for file_path in selected_files:
            candidate = file_path if file_path.is_absolute() else input_dir / file_path
            if candidate.is_file() and candidate.suffix.lower() == ".xml":
                targets.append(candidate)
            else:
                print(f"Skipping {candidate}: not an XML file.")
        return targets

    return sorted(input_dir.glob("*.xml"))


def generate_quality_report(metrics: BatchMetrics, output_dir: Path, report_format: str) -> None:
    """Generate quality summary report in the requested format(s)."""
    timestamp = metrics.start_time.strftime("%Y%m%d_%H%M%S")
    
    if report_format in ("excel", "both"):
        if OPENPYXL_AVAILABLE:
            excel_path = output_dir / f"quality_report_{timestamp}.xlsx"
            try:
                generate_excel_report(metrics, excel_path)
                print(f"Quality report (Excel): {excel_path}")
            except Exception as e:
                print(f"Warning: Failed to generate Excel report: {e}")
                # Fallback to text if Excel fails
                if report_format == "excel":
                    report_format = "text"
        else:
            print("Warning: openpyxl not available. Install with: pip install openpyxl")
            # Fallback to text if Excel not available
            if report_format == "excel":
                report_format = "text"
    
    if report_format in ("text", "both"):
        text_path = output_dir / f"quality_report_{timestamp}.txt"
        text_report = generate_text_report(metrics)
        text_path.write_text(text_report, encoding="utf-8")
        print(f"Quality report (Text): {text_path}")


def run(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    input_dir: Path = (args.input or default_input_dir()).resolve()
    output_dir: Path = (args.output or default_output_dir()).resolve()

    # Ensure directories exist so a freshly unpacked bundle is ready to use.
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    targets = resolve_targets(input_dir, args.files or [])
    if not targets:
        print("No XML files found to process. Ensure files are placed in the input directory.")
        return 1

    # Initialize batch metrics
    metrics = BatchMetrics()
    
    for xml_file in targets:
        output_file = output_dir / f"{xml_file.stem}.json"
        print(f"Processing {xml_file.name} -> {output_file.name} (flatten={args.flatten})")
        
        timestamp = datetime.now()
        
        # Check if file should be skipped (you can add custom skip logic here)
        if not xml_file.exists():
            result = ProcessingResult(
                filename=xml_file.name,
                status="skipped",
                timestamp=timestamp,
                error_message="File does not exist"
            )
            metrics.add_result(result)
            continue
        
        # Process the file
        try:
            conversion_result = convert_xml_to_json(xml_file, output_file, flatten=args.flatten)
            
            if conversion_result.success:
                if conversion_result.warning_message:
                    status = "warning"
                else:
                    status = "success"
                
                result = ProcessingResult(
                    filename=xml_file.name,
                    status=status,
                    timestamp=timestamp,
                    records_processed=conversion_result.records_processed,
                    warning_message=conversion_result.warning_message
                )
            else:
                result = ProcessingResult(
                    filename=xml_file.name,
                    status="failure",
                    timestamp=timestamp,
                    error_message=conversion_result.error_message
                )
                print(f"Failed to process {xml_file.name}: {conversion_result.error_message}")
            
            metrics.add_result(result)
            
        except Exception as exc:
            result = ProcessingResult(
                filename=xml_file.name,
                status="failure",
                timestamp=timestamp,
                error_message=f"Unexpected error: {str(exc)}"
            )
            metrics.add_result(result)
            print(f"Unexpected error while processing {xml_file.name}: {exc}.")

    # Finalize metrics
    metrics.finalize()
    
    # Print summary
    print(
        f"\nCompleted conversion for {metrics.total_processed} of {metrics.total_files} file(s). "
        f"Warnings: {metrics.total_warnings}, Failures: {metrics.total_failures}"
    )
    print(f"Output directory: {output_dir}")
    
    # Generate quality report
    if not args.no_report:
        print("\nGenerating quality summary report...")
        generate_quality_report(metrics, output_dir, args.report_format)
    
    return 0 if metrics.total_failures == 0 else 1


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
