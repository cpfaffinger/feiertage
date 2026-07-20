"""Tests for region.py - region logic.

These tests validate against the Go reference implementation.
"""
import pytest
from app.region import (
    get_all_regions, get_region, get_feiertage_for_date,
    get_feiertage_for_date_in_region, Region,
    baden_wuerttemberg, bayern, berlin, brandenburg, bremen,
    hamburg, hessen, mecklenburg_vorpommern, niedersachsen,
    nordrhein_westfalen, rheinland_pfalz, saarland, sachsen,
    sachsen_anhalt, schleswig_holstein, thueringen, deutschland,
    burgenland, kaernten, niederoesterreich, oberoesterreich,
    salzburg, steiermark, tirol, vorarlberg, wien, oesterreich,
    all_holidays,
)
import datetime


# ── Region basic tests ──

class TestRegionBasics:
    def test_region_creation(self):
        r = Region(name="Test", shortname="T")
        assert r.name == "Test"
        assert r.shortname == "T"

    def test_all_2016_with_sunday(self):
        r = all_holidays(2016, True)
        assert len(r.feiertage) > 0
        assert r.name == "Alle"

    def test_deutschland_2016(self):
        r = deutschland(2016, False)
        assert len(r.feiertage) > 0
        assert r.name == "Deutschland"

    def test_brandenburg_2016_with_sunday(self):
        r = brandenburg(2016, True)
        assert len(r.feiertage) > 0

    def test_brandenburg_2016_no_sunday(self):
        r = brandenburg(2016, False)
        assert len(r.feiertage) > 0


# ── Region counts - verified against Go reference ──

class TestRegionCounts:
    @pytest.mark.parametrize("region_fn, year, inkl_sonntage, expected_count", [
        (baden_wuerttemberg, 2016, False, 12),
        (bayern, 2016, False, 12),
        (berlin, 2016, False, 9),
        (berlin, 2019, False, 10),
        (berlin, 2020, False, 11),
        (brandenburg, 2020, True, 12),
        (brandenburg, 2017, True, 12),
        (brandenburg, 2020, False, 10),
        (bremen, 2016, False, 9),
        (bremen, 2016, False, 9),
        (hamburg, 2016, False, 9),
        (hessen, 2016, False, 10),
        (mecklenburg_vorpommern, 2016, False, 10),
        (niedersachsen, 2016, False, 9),
        (nordrhein_westfalen, 2016, False, 11),
        (rheinland_pfalz, 2016, False, 11),
        (saarland, 2016, False, 12),
        (sachsen, 2016, False, 11),
        (sachsen_anhalt, 2016, False, 11),
        (schleswig_holstein, 2016, False, 9),
        (thueringen, 2016, False, 10),
        (deutschland, 2016, False, 9),
        (deutschland, 2017, False, 10),
        (burgenland, 2016, False, 14),
        (kaernten, 2016, False, 15),
        (niederoesterreich, 2016, False, 14),
        (oberoesterreich, 2016, False, 14),
        (salzburg, 2016, False, 14),
        (steiermark, 2016, False, 14),
        (tirol, 2016, False, 14),
        (vorarlberg, 2016, False, 14),
        (wien, 2016, False, 14),
        (oesterreich, 2016, False, 13),
        (all_holidays, 2016, True, 81),
        (all_holidays, 2016, False, 69),
        (baden_wuerttemberg, 2017, False, 13),
        (bayern, 2017, False, 13),
        (deutschland, 2017, False, 10),
    ])
    def test_region_counts(self, region_fn, year, inkl_sonntage, expected_count):
        r = region_fn(year, inkl_sonntage)
        assert len(r.feiertage) == expected_count, \
            f"{region_fn.__name__}({year}, {inkl_sonntage}): got {len(r.feiertage)}, expected {expected_count}"


# ── Brandenburg 2017 specific ──

class TestBrandenburg2017:
    def test_count(self):
        r = brandenburg(2017, True)
        assert len(r.feiertage) == 12


# ── GetAllRegions counts ──

class TestGetAllRegions:
    def test_germany_count(self):
        r = get_all_regions(2020, False, "de")
        assert len(r) == 17  # 16 Bundesländer + Deutschland

    def test_austria_count(self):
        r = get_all_regions(2020, False, "at")
        assert len(r) == 10  # 9 Bundesländer + Österreich

    def test_all_count(self):
        r = get_all_regions(2020, False)
        assert len(r) == 28  # 16 DE + 9 AT + DE + AT + Alle = 28


# ── get_region lookup ──

class TestGetRegion:
    def test_bayern(self):
        r = get_region("Bayern", 2016, True)
        assert r is not None
        assert r.name == "Bayern"
        assert r.feiertage[7].datum.strftime("%d.%m.%Y") == "26.05.2016"

    def test_brandenburg_ostern(self):
        r = get_region("Brandenburg", 2016, True)
        assert r is not None
        assert r.feiertage[2].datum.strftime("%d.%m.%Y") == "27.03.2016"

    def test_case_insensitive(self):
        r = get_region("bayern", 2016, False)
        assert r is not None
        assert r.name == "Bayern"

    def test_oesterreich(self):
        r = get_region("Österreich", 2016, False)
        assert r is not None
        assert r.name == "Österreich"

    def test_alle(self):
        r = get_region("Alle", 2016, True)
        assert r is not None
        assert r.name == "Alle"

    def test_unknown_region(self):
        r = get_region("InvalidRegion", 2016, False)
        assert r is None

    def test_shortname_bw(self):
        r = get_region("BW", 2016, False)
        assert r is not None
        assert r.shortname == "BW"

    def test_shortname_by(self):
        r = get_region("BY", 2016, False)
        assert r is not None
        assert r.shortname == "BY"


# ── get_feiertage_for_date_in_region ──

class TestFeiertageForDateInRegion:
    import datetime

    def test_weihnachten_in_bayern(self):
        d = datetime.date(2025, 12, 25)
        result = get_feiertage_for_date_in_region(d, bayern, False)
        assert len(result) == 1
        assert result[0].name == "Weihnachten"

    def test_not_a_holiday(self):
        d = datetime.date(2025, 3, 3)
        result = get_feiertage_for_date_in_region(d, bayern, False)
        assert len(result) == 0


# ── get_feiertage_for_date ──

class TestFeiertageForDate:
    import datetime

    def test_ostern(self):
        d = datetime.date(2025, 4, 20)
        result = get_feiertage_for_date(d)
        names = [f.name for f in result]
        assert "Ostern" in names

    def test_neujahr(self):
        d = datetime.date(2025, 1, 1)
        result = get_feiertage_for_date(d)
        names = [f.name for f in result]
        assert "Neujahr" in names

    def test_empty(self):
        d = datetime.date(2025, 7, 3)
        result = get_feiertage_for_date(d)
        assert len(result) == 0


# ── All regions sort feiertage by date ──

class TestRegionsSorted:
    @pytest.mark.parametrize("region_fn", [
        baden_wuerttemberg, bayern, berlin, brandenburg, bremen,
        hamburg, hessen, mecklenburg_vorpommern, niedersachsen,
        nordrhein_westfalen, rheinland_pfalz, saarland, sachsen,
        sachsen_anhalt, schleswig_holstein, thueringen, deutschland,
        burgenland, kaernten, niederoesterreich, oberoesterreich,
        salzburg, steiermark, tirol, vorarlberg, wien, oesterreich,
    ])
    def test_sorted_by_date(self, region_fn):
        r = region_fn(2026, False)
        dates = [f.datum for f in r.feiertage]
        assert dates == sorted(dates)


# ── Reformationstag 2017 edge case ──

class TestReformationstag2017:
    def test_deutschland_2017_includes(self):
        r = deutschland(2017, False)
        names = [f.name for f in r.feiertage]
        assert "Reformationstag" in names

    def test_deutschland_2016_excludes(self):
        r = deutschland(2016, False)
        names = [f.name for f in r.feiertage]
        assert "Reformationstag" not in names


# ── Internationaler Frauentag in Berlin from 2019 ──

class TestFrauentagBerlin:
    def test_2018_not_included(self):
        r = berlin(2018, False)
        names = [f.name for f in r.feiertage]
        assert "Internationaler Frauentag" not in names

    def test_2019_included(self):
        r = berlin(2019, False)
        names = [f.name for f in r.feiertage]
        assert "Internationaler Frauentag" in names


# ── Tag der Befreiung Berlin 2020 ──

class TestBefreiungBerlin:
    def test_2020_included(self):
        r = berlin(2020, False)
        names = [f.name for f in r.feiertage]
        assert "Tag der Befreiung" in names

    def test_2019_not_included(self):
        r = berlin(2019, False)
        names = [f.name for f in r.feiertage]
        assert "Tag der Befreiung" not in names


# ── Reformationstag for Bremen (from 2018) ──

class TestBremenReformationstag:
    def test_2018_included(self):
        r = bremen(2018, False)
        names = [f.name for f in r.feiertage]
        assert "Reformationstag" in names

    def test_2016_not_included(self):
        r = bremen(2016, False)
        names = [f.name for f in r.feiertage]
        assert "Reformationstag" not in names


# ── Mecklenburg-Vorpommern Frauentag from 2023 ──

class TestMVFrauentag:
    def test_2023_included(self):
        r = mecklenburg_vorpommern(2023, False)
        names = [f.name for f in r.feiertage]
        assert "Internationaler Frauentag" in names

    def test_2022_not_included(self):
        r = mecklenburg_vorpommern(2022, False)
        names = [f.name for f in r.feiertage]
        assert "Internationaler Frauentag" not in names


# ── Thüringen Weltkindertag from 2019 ──

class TestThueringenWeltkindertag:
    def test_2019_included(self):
        r = thueringen(2019, False)
        names = [f.name for f in r.feiertage]
        assert "Weltkindertag" in names

    def test_2018_not_included(self):
        r = thueringen(2018, False)
        names = [f.name for f in r.feiertage]
        assert "Weltkindertag" not in names


# ── Niedersachsen, Hamburg, Schleswig-Holstein Reformationstag from 2018 ──

class TestReformationstagFrom2018:
    @pytest.mark.parametrize("region_fn, name", [
        (niedersachsen, "Niedersachsen"),
        (hamburg, "Hamburg"),
        (schleswig_holstein, "Schleswig-Holstein"),
    ])
    def test_2018_included(self, region_fn, name):
        r = region_fn(2018, False)
        names = [f.name for f in r.feiertage]
        assert "Reformationstag" in names, f"{name} 2018 should include Reformationstag"

    @pytest.mark.parametrize("region_fn, name", [
        (niedersachsen, "Niedersachsen"),
        (hamburg, "Hamburg"),
        (schleswig_holstein, "Schleswig-Holstein"),
    ])
    def test_2016_not_included(self, region_fn, name):
        r = region_fn(2016, False)
        names = [f.name for f in r.feiertage]
        assert "Reformationstag" not in names, f"{name} 2016 should not include Reformationstag"


# ── Brandenburg with/without Sundays ──

class TestBrandenburgSunday:
    def test_with_sunday_includes_ostern(self):
        r = brandenburg(2026, True)
        names = [f.name for f in r.feiertage]
        assert "Ostern" in names
        assert "Pfingsten" in names

    def test_without_sunday_excludes_ostern(self):
        r = brandenburg(2026, False)
        names = [f.name for f in r.feiertage]
        assert "Ostern" not in names
        assert "Pfingsten" not in names


# ── canonalize function ──

class TestCanonicalize:
    def test_basic(self):
        from app.region import _canonicalize
        assert _canonicalize("Baden-Württemberg") == "badenwuerttemberg"

    def test_umlaut(self):
        from app.region import _canonicalize
        assert _canonicalize("Österreich") == "oesterreich"

    def test_case(self):
        from app.region import _canonicalize
        assert _canonicalize("BERLIN") == "berlin"


class TestGetAllRegionsEdgeCases:
    def test_invalid_country_returns_empty(self):
        from app.region import get_all_regions
        r = get_all_regions(2020, False, "fr")
        assert len(r) == 0


class TestFeiertagsFunctionListConversion:
    def test_hobbit_day_before_1978_returns_none(self):
        from app.region import _feiertags_function_list_to_feiertag_list
        from app.feiertage import hobbit_day
        result = _feiertags_function_list_to_feiertag_list([hobbit_day], 1977)
        assert len(result) == 0

    def test_hobbit_day_after_1978_included(self):
        from app.region import _feiertags_function_list_to_feiertag_list
        from app.feiertage import hobbit_day
        result = _feiertags_function_list_to_feiertag_list([hobbit_day], 1980)
        assert len(result) == 1
        assert result[0].name == "Hobbit Day"


class TestCreateFeiertagsListNoneHandling:
    def test_none_function_in_ffun(self):
        from app.region import _create_feiertags_list
        from app.feiertage import hobbit_day
        result = _create_feiertags_list(1977, "DE", [hobbit_day])
        assert isinstance(result, list)
