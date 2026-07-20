"""Tests for the FastAPI application endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestRootEndpoint:
    def test_root_returns_html(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_root_contains_title(self):
        response = client.get("/")
        assert "Feiertage API" in response.text

    def test_root_contains_swagger_link(self):
        response = client.get("/")
        assert "/docs" in response.text


class TestDocsEndpoints:
    def test_swagger_ui(self):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc(self):
        response = client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_json(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "Feiertage API" in data["info"]["title"]


class TestApiRegions:
    def test_all_regions_2020(self):
        response = client.get("/api/regions?year=2020")
        assert response.status_code == 200
        data = response.json()
        assert data["year"] == 2020
        assert "regions" in data
        assert len(data["regions"]) == 28

    def test_regions_de(self):
        response = client.get("/api/regions?year=2020&country=de")
        assert response.status_code == 200
        data = response.json()
        assert len(data["regions"]) == 17

    def test_regions_at(self):
        response = client.get("/api/regions?year=2020&country=at")
        assert response.status_code == 200
        data = response.json()
        assert len(data["regions"]) == 10

    def test_regions_with_sundays(self):
        response = client.get("/api/regions?year=2020&inkl_sonntage=true")
        assert response.status_code == 200

    def test_regions_structure(self):
        response = client.get("/api/regions?year=2020&country=de")
        data = response.json()
        region = data["regions"][0]
        assert "name" in region
        assert "shortname" in region
        assert "count" in region
        assert "feiertage" in region
        feiertag = region["feiertage"][0]
        assert "date" in feiertag
        assert "name" in feiertag


class TestApiRegion:
    def test_bayern_2016(self):
        response = client.get("/api/region/Bayern?year=2016")
        assert response.status_code == 200
        data = response.json()
        assert data["region"] == "Bayern"
        assert len(data["feiertage"]) == 12

    def test_berlin_2019(self):
        response = client.get("/api/region/Berlin?year=2019")
        assert response.status_code == 200
        data = response.json()
        assert len(data["feiertage"]) == 10

    def test_berlin_2020(self):
        response = client.get("/api/region/Berlin?year=2020")
        assert response.status_code == 200
        data = response.json()
        assert len(data["feiertage"]) == 11

    def test_burgenland_2016(self):
        response = client.get("/api/region/Burgenland?year=2016")
        assert response.status_code == 200
        data = response.json()
        assert len(data["feiertage"]) == 14

    def test_invalid_region(self):
        response = client.get("/api/region/InvalidRegion?year=2016")
        assert response.status_code == 404

    def test_alle_2016(self):
        response = client.get("/api/region/Alle?year=2016&inkl_sonntage=true")
        assert response.status_code == 200
        data = response.json()
        assert len(data["feiertage"]) == 81


class TestApiFeiertage:
    def test_all_2016(self):
        response = client.get("/api/feiertage?year=2016")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 81

    def test_with_region(self):
        response = client.get("/api/feiertage?year=2016&region=Bayern")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 12

    def test_invalid_region(self):
        response = client.get("/api/feiertage?year=2016&region=Invalid")
        assert response.status_code == 404


class TestApiFeiertageByDate:
    def test_neujahr(self):
        response = client.get("/api/feiertage/2026-01-01")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 1
        names = [f["name"] for f in data["feiertage"]]
        assert "Neujahr" in names

    def test_weihnachten(self):
        response = client.get("/api/feiertage/2026-12-25")
        assert response.status_code == 200
        data = response.json()
        names = [f["name"] for f in data["feiertage"]]
        assert "Weihnachten" in names or "Christtag" in names

    def test_no_holiday(self):
        response = client.get("/api/feiertage/2026-03-03")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0

    def test_invalid_date(self):
        response = client.get("/api/feiertage/not-a-date")
        assert response.status_code == 400

    def test_bad_format(self):
        response = client.get("/api/feiertage/01-01-2026")
        assert response.status_code == 400


class TestApiEaster:
    def test_easter_2015(self):
        response = client.get("/api/easter?year=2015")
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == "2015-04-05"

    def test_easter_2016(self):
        response = client.get("/api/easter?year=2016")
        assert response.status_code == 200
        data = response.json()
        assert data["date"] == "2016-03-27"

    def test_easter_2026(self):
        response = client.get("/api/easter?year=2026")
        assert response.status_code == 200
        data = response.json()
        assert "date" in data
        assert "name" in data
        assert data["name"] == "Ostern"
