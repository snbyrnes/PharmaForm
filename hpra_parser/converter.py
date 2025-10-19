"""Core parsing utilities for transforming HPRA XML into JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from xml.etree import ElementTree as ET

from .integrity import calculate_sha256


@dataclass
class ConversionResult:
    """Result of converting an XML file to JSON."""
    success: bool
    records_processed: int = 0
    warning_message: Optional[str] = None
    error_message: Optional[str] = None
    input_sha256: Optional[str] = None
    output_sha256: Optional[str] = None


def strip_namespace(tag: str) -> str:
    """Return the local part of an XML tag (drop the namespace URI)."""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def etree_to_dict(node: ET.Element) -> Any:
    """Recursively convert an ElementTree node into nested dictionaries/lists."""
    tag = strip_namespace(node.tag)
    children = list(node)
    text = (node.text or "").strip()

    if not children and not node.attrib:
        return text or None

    result: Dict[str, Any] = {}

    if node.attrib:
        result["attributes"] = {strip_namespace(key): value for key, value in node.attrib.items()}

    if children:
        grouped_children: Dict[str, List[Any]] = {}
        for child in children:
            key = strip_namespace(child.tag)
            value = etree_to_dict(child)
            if value is None:
                continue
            grouped_children.setdefault(key, []).append(value)

        for key, values in grouped_children.items():
            result[key] = values[0] if len(values) == 1 else values

    if text:
        if result:
            result["value"] = text
        else:
            return text

    if not result:
        return text or None

    if "attributes" not in result and "value" not in result and len(result) == 1:
        sole_key, sole_value = next(iter(result.items()))
        if sole_key == tag:
            return sole_value

    return result


def flatten_dict(value: Any, parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dictionaries/lists into a single dictionary."""
    items: Dict[str, Any] = {}

    if isinstance(value, dict):
        for key, val in value.items():
            if key == "attributes" and isinstance(val, dict):
                attr_prefix = f"{parent_key}{sep}attributes" if parent_key else "attributes"
                for attr_key, attr_val in val.items():
                    combined_key = f"{attr_prefix}{sep}{attr_key}" if attr_prefix else attr_key
                    items[combined_key] = attr_val
                continue

            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            items.update(flatten_dict(val, new_key, sep))
    elif isinstance(value, list):
        if not parent_key:
            for index, item in enumerate(value):
                indexed_key = f"[{index}]"
                items.update(flatten_dict(item, indexed_key, sep))
        elif all(not isinstance(item, (dict, list)) for item in value):
            items[parent_key] = value
        else:
            for index, item in enumerate(value):
                indexed_key = f"{parent_key}[{index}]"
                items.update(flatten_dict(item, indexed_key, sep))
    else:
        if parent_key:
            items[parent_key] = value

    return items


def flatten_data(data: Dict[str, Any]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Flatten the nested product-focused JSON into table-friendly records."""
    products_section = data.get("Products")
    if isinstance(products_section, dict) and "Product" in products_section:
        products_raw = products_section.get("Product", [])
        if not isinstance(products_raw, list):
            products_raw = [products_raw] if products_raw is not None else []

        flattened_products: List[Dict[str, Any]] = []
        root_attrs = products_section.get("attributes")
        for product in products_raw:
            flattened = flatten_dict(product)
            if isinstance(root_attrs, dict):
                for attr_key, attr_val in root_attrs.items():
                    flattened[f"Products.attributes.{attr_key}"] = attr_val
            flattened_products.append(flattened)
        return flattened_products

    return flatten_dict(data)


def parse_xml(xml_path: Path) -> Dict[str, Any]:
    """Parse a HPRA XML file into the nested dictionary representation."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return {strip_namespace(root.tag): etree_to_dict(root)}


def convert_xml_to_json(input_path: Path, output_path: Path, flatten: bool = False, calculate_checksums: bool = True) -> ConversionResult:
    """Convert a HPRA XML file to JSON, optionally flattening the structure.
    
    Args:
        input_path: Path to input XML file
        output_path: Path to output JSON file
        flatten: If True, flatten the JSON structure
        calculate_checksums: If True, calculate SHA-256 hashes for integrity verification
    
    Returns:
        ConversionResult with success status, record count, hashes, and any warnings/errors.
    """
    input_hash = None
    output_hash = None
    
    try:
        # Calculate input file hash before processing
        if calculate_checksums:
            input_hash = calculate_sha256(input_path)
        
        data = parse_xml(input_path)
        records_count = 0
        warning = None
        
        if flatten:
            flattened_data = flatten_data(data)
            if isinstance(flattened_data, list):
                records_count = len(flattened_data)
            else:
                records_count = 1
            data = flattened_data
        else:
            # Count records in nested structure
            products_section = data.get("Products", {})
            if isinstance(products_section, dict):
                products = products_section.get("Product", [])
                if isinstance(products, list):
                    records_count = len(products)
                elif products is not None:
                    records_count = 1
        
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        
        # Calculate output file hash after writing
        if calculate_checksums:
            output_hash = calculate_sha256(output_path)
        
        # Add warning if no records found
        if records_count == 0:
            warning = "No products found in XML file"
        
        return ConversionResult(
            success=True,
            records_processed=records_count,
            warning_message=warning,
            input_sha256=input_hash,
            output_sha256=output_hash
        )
    except ET.ParseError as e:
        return ConversionResult(
            success=False,
            error_message=f"XML parse error: {str(e)}"
        )
    except Exception as e:
        return ConversionResult(
            success=False,
            error_message=f"Unexpected error: {str(e)}"
        )
