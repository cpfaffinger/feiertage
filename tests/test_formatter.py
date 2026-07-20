"""Tests for the format converter module."""
import pytest
from app.formatter import (
    to_json, to_xml, to_csv, to_tsv, to_txt,
    format_response, FORMATTERS, AVAILABLE_FORMATS,
    _normalize, _flatten_for_tabular,
)


SIMPLE_DATA = {"date": "2026-01-01", "name": "Neujahr"}
FEIERTAGE_DATA = {
    "year": 2026,
    "region": "Bayern",
    "count": 2,
    "feiertage": [
        {"date": "2026-01-01", "name": "Neujahr"},
        {"date": "2026-01-06", "name": "Epiphanias"},
    ],
}
REGIONS_DATA = {
    "year": 2026,
    "count": 1,
    "regions": [
        {
            "name": "Bayern",
            "shortname": "BY",
            "count": 2,
            "feiertage": [
                {"date": "2026-01-01", "name": "Neujahr"},
                {"date": "2026-01-06", "name": "Epiphanias"},
            ],
        }
    ],
}


class TestNormalize:
    def test_basic(self):
        assert _normalize("Hello World") == "hello_world"

    def test_umlaut_preserved(self):
        assert _normalize("Österreich") == "österreich"

    def test_hyphens(self):
        assert _normalize("Baden-Württemberg") == "baden_württemberg"


class TestToJson:
    def test_simple(self):
        result = to_json(SIMPLE_DATA)
        assert '"date": "2026-01-01"' in result
        assert '"name": "Neujahr"' in result

    def test_feiertage_list(self):
        result = to_json(FEIERTAGE_DATA)
        assert '"feiertage"' in result
        assert '"Neujahr"' in result

    def test_regions(self):
        result = to_json(REGIONS_DATA)
        assert '"regions"' in result
        assert '"Bayern"' in result


class TestToXml:
    def test_simple(self):
        result = to_xml(SIMPLE_DATA)
        assert "<date>2026-01-01</date>" in result
        assert "<name>Neujahr</name>" in result
        assert "<response>" in result

    def test_feiertage_list(self):
        result = to_xml(FEIERTAGE_DATA)
        assert "<year>2026</year>" in result
        assert "<region>Bayern</region>" in result
        assert "Neujahr" in result
        assert "Epiphanias" in result

    def test_regions(self):
        result = to_xml(REGIONS_DATA)
        assert "Bayern" in result
        assert "BY" in result

    def test_xml_well_formed(self):
        result = to_xml(FEIERTAGE_DATA)
        assert result.startswith("<?xml")

    def test_xml_nested_lists(self):
        data = {"items": [{"a": 1}, {"a": 2}]}
        result = to_xml(data)
        assert result.count("<a>") == 2

    def test_xml_nested_dicts(self):
        data = {"address": {"street": "Hauptstr", "number": 42}}
        result = to_xml(data)
        assert "Hauptstr" in result
        assert "42" in result

    def test_xml_list_of_primitives(self):
        data = {"tags": ["foo", "bar", "baz"]}
        result = to_xml(data)
        assert "foo" in result
        assert "bar" in result


class TestToCsv:
    def test_feiertage(self):
        result = to_csv(FEIERTAGE_DATA)
        lines = result.strip().split("\r\n")
        assert len(lines) >= 3  # header + 2 rows
        assert "date" in lines[0]
        assert "2026-01-01" in result
        assert "Neujahr" in result

    def test_regions(self):
        result = to_csv(REGIONS_DATA)
        lines = result.strip().split("\r\n")
        assert len(lines) >= 3
        assert "region" in lines[0]

    def test_simple_date(self):
        result = to_csv(SIMPLE_DATA)
        assert "date" in result
        assert "2026-01-01" in result

    def test_empty(self):
        result = to_csv({})
        assert result == ""


class TestToTsv:
    def test_feiertage(self):
        result = to_tsv(FEIERTAGE_DATA)
        assert "\t" in result
        assert "2026-01-01" in result

    def test_regions(self):
        result = to_tsv(REGIONS_DATA)
        assert "\t" in result
        assert "Bayern" in result

    def test_empty(self):
        result = to_tsv({})
        assert result == ""


class TestToTxt:
    def test_simple(self):
        result = to_txt(SIMPLE_DATA)
        assert "date:" in result
        assert "2026-01-01" in result
        assert "Neujahr" in result

    def test_feiertage_list(self):
        result = to_txt(FEIERTAGE_DATA)
        assert "year:" in result
        assert "2026" in result
        assert "region:" in result
        assert "Neujahr" in result

    def test_regions(self):
        result = to_txt(REGIONS_DATA)
        assert "count:" in result
        assert "Bayern" in result

    def test_nested_output(self):
        result = to_txt(FEIERTAGE_DATA)
        assert "feiertage:" in result

    def test_nested_dicts(self):
        data = {"address": {"street": "Main", "number": 42}}
        result = to_txt(data)
        assert "address:" in result
        assert "street:" in result
        assert "Main" in result

    def test_list_of_primitives(self):
        data = {"tags": ["foo", "bar"]}
        result = to_txt(data)
        assert "- foo" in result
        assert "- bar" in result


class TestFormatResponse:
    def test_json(self):
        body, ct = format_response(SIMPLE_DATA, "json")
        assert "json" in ct
        assert "Neujahr" in body

    def test_xml(self):
        body, ct = format_response(SIMPLE_DATA, "xml")
        assert "xml" in ct
        assert "<name>Neujahr</name>" in body

    def test_csv(self):
        body, ct = format_response(FEIERTAGE_DATA, "csv")
        assert "csv" in ct

    def test_tsv(self):
        body, ct = format_response(FEIERTAGE_DATA, "tsv")
        assert "tab-separated" in ct

    def test_txt(self):
        body, ct = format_response(SIMPLE_DATA, "txt")
        assert "plain" in ct
        assert "Neujahr" in body

    def test_invalid_format_falls_back_to_json(self):
        body, ct = format_response(SIMPLE_DATA, "yaml")
        assert "json" in ct

    def test_unknown_format_returns_json(self):
        body, ct = format_response(SIMPLE_DATA, "html")
        assert "Neujahr" in body


class TestAvailableFormats:
    def test_all_formats_registered(self):
        assert "json" in FORMATTERS
        assert "xml" in FORMATTERS
        assert "csv" in FORMATTERS
        assert "tsv" in FORMATTERS
        assert "txt" in FORMATTERS

    def test_available_formats_list(self):
        assert AVAILABLE_FORMATS == ["json", "xml", "csv", "tsv", "txt"]


class TestFlattenForTabular:
    def test_feiertage_list(self):
        result = _flatten_for_tabular(FEIERTAGE_DATA)
        assert len(result) == 2
        assert result[0]["date"] == "2026-01-01"
        assert result[1]["name"] == "Epiphanias"

    def test_regions_list(self):
        result = _flatten_for_tabular(REGIONS_DATA)
        assert len(result) == 2
        assert result[0]["region"] == "Bayern"
        assert result[0]["region_short"] == "BY"

    def test_simple_data(self):
        result = _flatten_for_tabular(SIMPLE_DATA)
        assert len(result) == 1
        assert result[0]["name"] == "Neujahr"

    def test_empty(self):
        result = _flatten_for_tabular({})
        assert result == []
