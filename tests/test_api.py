"""Tests for the FastAPI application endpoints."""
from datetime import date
import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.main as main_module


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

    def test_redoc_uses_self_hosted_js(self):
        # ReDoc must load the bundle from our /redoc.js proxy, not the CDN,
        # otherwise the page stays blank in MIME-restricted environments.
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "/redoc.js" in response.text
        assert "cdn.jsdelivr.net" not in response.text

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
        # Without inkl_sonntage the no-region path must NOT include Sundays.
        response = client.get("/api/feiertage?year=2016")
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 69

    def test_all_2016_inkl_sonntage(self):
        # inkl_sonntage must be honoured on the no-region path.
        response = client.get("/api/feiertage?year=2016&inkl_sonntage=true")
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


class TestApiIsFeiertag:
    def test_neujahr_no_region(self):
        response = client.get("/api/isFeiertag?date=2026-01-01")
        assert response.status_code == 200
        data = response.json()
        assert data["is_feiertag"] is True
        names = [f["name"] for f in data["feiertage"]]
        assert "Neujahr" in names

    def test_neujahr_with_region(self):
        response = client.get("/api/isFeiertag?date=2026-01-01&region=Bayern")
        assert response.status_code == 200
        data = response.json()
        assert data["is_feiertag"] is True
        assert len(data["feiertage"]) == 1
        assert data["feiertage"][0]["name"] == "Neujahr"
        assert data["feiertage"][0]["region"] == "Bayern"

    def test_not_a_feiertag(self):
        response = client.get("/api/isFeiertag?date=2026-07-03")
        assert response.status_code == 200
        data = response.json()
        assert data["is_feiertag"] is False
        assert len(data["feiertage"]) == 0

    def test_niederoesterreich_feiertag(self):
        response = client.get("/api/isFeiertag?date=2026-11-15&region=Niederösterreich")
        assert response.status_code == 200
        data = response.json()
        assert data["is_feiertag"] is True
        names = [f["name"] for f in data["feiertage"]]
        assert "Leopolditag" in names

    def test_invalid_region(self):
        response = client.get("/api/isFeiertag?date=2026-01-01&region=InvalidRegion")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data

    def test_invalid_date(self):
        response = client.get("/api/isFeiertag?date=not-a-date")
        assert response.status_code == 400

    def test_with_sundays(self):
        response = client.get("/api/isFeiertag?date=2026-04-05&region=Brandenburg&inkl_sonntage=true")
        assert response.status_code == 200
        data = response.json()
        assert data["is_feiertag"] is True

    def test_format_xml(self):
        response = client.get("/api/isFeiertag?date=2026-01-01&format=xml")
        assert response.status_code == 200
        assert "Neujahr" in response.text

    def test_format_csv(self):
        response = client.get("/api/isFeiertag?date=2026-01-01&format=csv")
        assert response.status_code == 200
        assert "Neujahr" in response.text


class TestYearDefaults:
    """Year is optional and defaults to the current year."""

    def test_regions_defaults_to_current_year(self):
        response = client.get("/api/regions")
        assert response.status_code == 200
        assert response.json()["year"] == date.today().year

    def test_region_defaults_to_current_year(self):
        response = client.get("/api/region/Bayern")
        assert response.status_code == 200
        assert response.json()["year"] == date.today().year

    def test_feiertage_defaults_to_current_year(self):
        response = client.get("/api/feiertage")
        assert response.status_code == 200
        assert response.json()["year"] == date.today().year

    def test_easter_defaults_to_current_year(self):
        response = client.get("/api/easter")
        assert response.status_code == 200
        assert response.json()["date"].startswith(str(date.today().year))


class TestUnifiedSchema:
    """The /api/feiertage response carries the unified region envelope."""

    def test_feiertage_includes_shortname(self):
        response = client.get("/api/feiertage?year=2026&region=Bayern")
        assert response.status_code == 200
        data = response.json()
        assert set(["year", "region", "shortname", "count", "feiertage"]).issubset(data.keys())
        assert data["shortname"] == "BY"

    def test_feiertage_no_region_has_shortname(self):
        response = client.get("/api/feiertage?year=2026")
        assert response.status_code == 200
        assert "shortname" in response.json()

    def test_openapi_exposes_response_schemas(self):
        data = client.get("/openapi.json").json()
        schemas = data["components"]["schemas"]
        for name in ["RegionsResponse", "RegionResponse", "DateFeiertageResponse",
                     "EasterResponse", "IsFeiertagResponse", "Feiertag"]:
            assert name in schemas
        ref = data["paths"]["/api/regions"]["get"]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
        assert ref.endswith("RegionsResponse")


class TestHealth:
    def test_health_ok(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestRedocJsProxy:
    def test_redoc_js_fetches_and_caches(self, monkeypatch):
        main_module._redoc_js_cache = None
        calls = {"n": 0}

        class FakeResp:
            text = "/* fake redoc bundle */"

            def raise_for_status(self):
                return None

        class FakeClient:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                return False

            async def get(self, url, timeout=None):
                calls["n"] += 1
                return FakeResp()

        monkeypatch.setattr(main_module.httpx, "AsyncClient", FakeClient)

        first = client.get("/redoc.js")
        assert first.status_code == 200
        assert "fake redoc bundle" in first.text
        assert "javascript" in first.headers["content-type"]

        # Second call is served from cache without another fetch.
        second = client.get("/redoc.js")
        assert second.status_code == 200
        assert calls["n"] == 1

        main_module._redoc_js_cache = None
