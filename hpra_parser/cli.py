"""Command-line utilities for running the HPRA XML parser."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List
from xml.etree import ElementTree as ET

from .converter import convert_xml_to_json


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

    failures = 0
    for xml_file in targets:
        output_file = output_dir / f"{xml_file.stem}.json"
        print(f"Processing {xml_file.name} -> {output_file.name} (flatten={args.flatten})")
        try:
            convert_xml_to_json(xml_file, output_file, flatten=args.flatten)
        except ET.ParseError as parse_error:
            failures += 1
            print(f"Failed to parse {xml_file.name}: {parse_error}.")
        except Exception as exc:  # pragma: no cover - defensive guard for unforeseen issues.
            failures += 1
            print(f"Unexpected error while processing {xml_file.name}: {exc}.")

    successful = len(targets) - failures
    print(
        f"Completed conversion for {successful} of {len(targets)} file(s). "
        f"Output directory: {output_dir}"
    )
    return 0 if failures == 0 else 1


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
