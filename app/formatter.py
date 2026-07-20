"""Output formatter supporting JSON, XML, CSV, TSV and TXT formats."""
import csv
import io
import json
import xml.dom.minidom
from typing import Any
from xml.etree.ElementTree import Element, SubElement, tostring


def _normalize(name: str) -> str:
    """Make tag names XML-safe."""
    return name.lower().replace(" ", "_").replace("-", "_")


def _build_xml_element(parent: Element, key: str, value: Any) -> Element:
    """Recursively build XML elements from dict/list structures."""
    tag = _normalize(key)
    elem = SubElement(parent, tag)
    if isinstance(value, dict):
        for k, v in value.items():
            _build_xml_element(elem, k, v)
    elif isinstance(value, list):
        for item in value:
            item_elem = SubElement(elem, _normalize(tag.rstrip("s")) if key.endswith("s") else "item")
            if isinstance(item, dict):
                for k, v in item.items():
                    _build_xml_element(item_elem, k, v)
            else:
                item_elem.text = str(item)
    else:
        elem.text = str(value)
    return elem


def to_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def to_xml(data: dict) -> str:
    root = Element("response")
    for key, value in data.items():
        _build_xml_element(root, key, value)
    raw = tostring(root, encoding="unicode")
    dom = xml.dom.minidom.parseString(raw)
    body = dom.toprettyxml(indent="  ")
    body = body.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8"?>')
    return body


def to_csv(data: dict) -> str:
    output = io.StringIO()
    flat = _flatten_for_tabular(data)
    if not flat:
        return ""
    writer = csv.DictWriter(output, fieldnames=flat[0].keys(), delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(flat)
    return output.getvalue()


def to_tsv(data: dict) -> str:
    output = io.StringIO()
    flat = _flatten_for_tabular(data)
    if not flat:
        return ""
    writer = csv.DictWriter(output, fieldnames=flat[0].keys(), delimiter="\t", quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(flat)
    return output.getvalue()


def to_txt(data: dict) -> str:
    lines = []
    _build_txt_lines(data, lines, 0)
    return "\n".join(lines)


def _build_txt_lines(data: dict, lines: list, indent: int) -> None:
    prefix = "  " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            _build_txt_lines(value, lines, indent + 1)
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}:")
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    lines.append(f"{prefix}  [{i}]:")
                    _build_txt_lines(item, lines, indent + 2)
                else:
                    lines.append(f"{prefix}  - {item}")
        else:
            lines.append(f"{prefix}{key}: {value}")


def _flatten_for_tabular(data: dict) -> list:
    """Extract feiertage entries into a flat list for CSV/TSV output."""
    entries = []

    feiertage = data.get("feiertage", [])
    if feiertage:
        for f in feiertage:
            row = {"date": f.get("date", ""), "name": f.get("name", "")}
            entries.append(row)
        return entries

    regions = data.get("regions", [])
    if regions:
        for r in regions:
            for f in r.get("feiertage", []):
                row = {
                    "region": r.get("name", ""),
                    "region_short": r.get("shortname", ""),
                    "date": f.get("date", ""),
                    "name": f.get("name", ""),
                }
                entries.append(row)
        return entries

    if "date" in data and "name" in data:
        return [{"date": data["date"], "name": data["name"]}]

    return []


FORMATTERS = {
    "json": ("application/json; charset=utf-8", to_json),
    "xml": ("application/xml; charset=utf-8", to_xml),
    "csv": ("text/csv; charset=utf-8", to_csv),
    "tsv": ("text/tab-separated-values; charset=utf-8", to_tsv),
    "txt": ("text/plain; charset=utf-8", to_txt),
}

AVAILABLE_FORMATS = list(FORMATTERS.keys())


def format_response(data: dict, fmt: str) -> tuple[str, str]:
    """Return (formatted_string, content_type) for the given format."""
    if fmt not in FORMATTERS:
        fmt = "json"
    content_type, converter = FORMATTERS[fmt]
    return converter(data), content_type
