"""Comparison tests: Python implementation vs Go reference implementation.

These tests verify that the Python holiday calculations produce identical results
to the Go reference implementation. All expected values are taken directly from
the Go test files (feiertage_test.go, region_test.go).
"""
import datetime
import pytest
from app.feiertage import (
    ostern, beginn_sommerzeit, beginn_winterzeit, buss_und_bettag,
    erntedankfest, muttertag, vierter_advent, dritter_advent,
    zweiter_advent, erster_advent, thanksgiving, neujahr, epiphanias,
    tag_der_arbeit, weihnachten, zweiter_weihnachtsfeiertag,
    tag_der_deutschen_einheit, karfreitag, ostermontag,
    christi_himmelfahrt, pfingstmontag,
)
from app.region import (
    baden_wuerttemberg, bayern, berlin, brandenburg, bremen,
    hamburg, hessen, mecklenburg_vorpommern, niedersachsen,
    nordrhein_westfalen, rheinland_pfalz, saarland, sachsen,
    sachsen_anhalt, schleswig_holstein, thueringen, deutschland,
    burgenland, kaernten, niederoesterreich, oberoesterreich,
    salzburg, steiermark, tirol, vorarlberg, wien, oesterreich,
    all_holidays, get_all_regions,
)


def fmt(d: datetime.date) -> str:
    return d.strftime("%d.%m.%Y")


# ═══════════════════════════════════════════════════════════════
# Ostern (Easter) comparison
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonOstern:
    """Verified against Go: feiertage_test.go TestOstern"""
    GoData = [
        (2015, "05.04.2015"),
        (2016, "27.03.2016"),
        (1954, "18.04.1954"),
        (1981, "19.04.1981"),
    ]

    @pytest.mark.parametrize("year,expected", GoData)
    def test_ostern_matches_go(self, year, expected):
        assert fmt(ostern(year).datum) == expected


# ═══════════════════════════════════════════════════════════════
# Sommerzeit / Winterzeit
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonSommerWinter:
    """Verified against Go: feiertage_test.go TestSommerWinterZeit"""
    def test_sommerzeit_2015(self):
        assert fmt(beginn_sommerzeit(2015).datum) == "29.03.2015"

    def test_winterzeit_2016(self):
        assert fmt(beginn_winterzeit(2016).datum) == "30.10.2016"


# ═══════════════════════════════════════════════════════════════
# Buß- und Bettag
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonBussUndBettag:
    """Verified against Go: feiertage_test.go TestBußUndBettag"""
    def test_2015(self):
        assert fmt(buss_und_bettag(2015).datum) == "18.11.2015"

    def test_2016(self):
        assert fmt(buss_und_bettag(2016).datum) == "16.11.2016"


# ═══════════════════════════════════════════════════════════════
# Erntedankfest / Muttertag
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonVorwaertssucher:
    """Verified against Go: feiertage_test.go TestVorwärtssucher"""
    def test_erntedankfest_2015(self):
        assert fmt(erntedankfest(2015).datum) == "04.10.2015"

    def test_erntedankfest_2016(self):
        assert fmt(erntedankfest(2016).datum) == "02.10.2016"

    def test_muttertag_2015(self):
        assert fmt(muttertag(2015).datum) == "10.05.2015"

    def test_muttertag_2016(self):
        assert fmt(muttertag(2016).datum) == "08.05.2016"


# ═══════════════════════════════════════════════════════════════
# Advent
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonAdvent:
    """Verified against Go: feiertage_test.go TestAdvent"""
    def test_vierter_advent_2016(self):
        assert fmt(vierter_advent(2016).datum) == "18.12.2016"

    def test_dritter_advent_2016(self):
        assert fmt(dritter_advent(2016).datum) == "11.12.2016"

    def test_zweiter_advent_2016(self):
        assert fmt(zweiter_advent(2016).datum) == "04.12.2016"

    def test_erster_advent_2016(self):
        assert fmt(erster_advent(2016).datum) == "27.11.2016"

    def test_vierter_advent_2006(self):
        assert fmt(vierter_advent(2006).datum) == "24.12.2006"


# ═══════════════════════════════════════════════════════════════
# Thanksgiving
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonThanksgiving:
    """Verified against Go: feiertage_test.go TestThanksgiving"""
    GoData = [
        (2010, "25.11.2010"),
        (2014, "27.11.2014"),
        (2015, "26.11.2015"),
        (2016, "24.11.2016"),
        (2017, "23.11.2017"),
        (2018, "22.11.2018"),
        (2019, "28.11.2019"),
        (2025, "27.11.2025"),
        (2028, "23.11.2028"),
        (2029, "22.11.2029"),
    ]

    @pytest.mark.parametrize("year,expected", GoData)
    def test_thanksgiving_matches_go(self, year, expected):
        assert fmt(thanksgiving(year).datum) == expected


# ═══════════════════════════════════════════════════════════════
# Region holiday counts (Deutschland + Österreich)
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonRegionCounts:
    """Verified against Go: region_test.go TestFeiertageZahl"""
    GoData = [
        ("Baden-Württemberg", baden_wuerttemberg, 2016, False, 12),
        ("Bayern", bayern, 2016, False, 12),
        ("Berlin", berlin, 2016, False, 9),
        ("Berlin", berlin, 2019, False, 10),
        ("Berlin", berlin, 2020, False, 11),
        ("Brandenburg", brandenburg, 2020, True, 12),
        ("Brandenburg", brandenburg, 2017, True, 12),
        ("Brandenburg", brandenburg, 2020, False, 10),
        ("Bremen", bremen, 2016, False, 9),
        ("Hamburg", hamburg, 2016, False, 9),
        ("Hessen", hessen, 2016, False, 10),
        ("Mecklenburg-Vorpommern", mecklenburg_vorpommern, 2016, False, 10),
        ("Niedersachsen", niedersachsen, 2016, False, 9),
        ("Nordrhein-Westfalen", nordrhein_westfalen, 2016, False, 11),
        ("Rheinland-Pfalz", rheinland_pfalz, 2016, False, 11),
        ("Saarland", saarland, 2016, False, 12),
        ("Sachsen", sachsen, 2016, False, 11),
        ("Sachsen-Anhalt", sachsen_anhalt, 2016, False, 11),
        ("Schleswig-Holstein", schleswig_holstein, 2016, False, 9),
        ("Thüringen", thueringen, 2016, False, 10),
        ("Deutschland", deutschland, 2016, False, 9),
        ("Deutschland", deutschland, 2017, False, 10),
        ("Burgenland", burgenland, 2016, False, 14),
        ("Kärnten", kaernten, 2016, False, 15),
        ("Niederösterreich", niederoesterreich, 2016, False, 14),
        ("Oberösterreich", oberoesterreich, 2016, False, 14),
        ("Salzburg", salzburg, 2016, False, 14),
        ("Steiermark", steiermark, 2016, False, 14),
        ("Tirol", tirol, 2016, False, 14),
        ("Vorarlberg", vorarlberg, 2016, False, 14),
        ("Wien", wien, 2016, False, 14),
        ("Österreich", oesterreich, 2016, False, 13),
        ("Alle", all_holidays, 2016, True, 81),
        ("Alle", all_holidays, 2016, False, 69),
        ("Baden-Württemberg", baden_wuerttemberg, 2017, False, 13),
        ("Bayern", bayern, 2017, False, 13),
        ("Deutschland", deutschland, 2017, False, 10),
    ]

    @pytest.mark.parametrize("name,region_fn,year,inkl_sonntage,expected", GoData)
    def test_region_count_matches_go(self, name, region_fn, year, inkl_sonntage, expected):
        r = region_fn(year, inkl_sonntage)
        assert len(r.feiertage) == expected, \
            f"{name}({year}, {inkl_sonntage}): Python={len(r.feiertage)}, Go={expected}"


# ═══════════════════════════════════════════════════════════════
# GetAllRegions counts
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonGetAllRegions:
    """Verified against Go: region_test.go TestRegionsInGermany, TestRegionsInAustria, TestRegionsAvailable"""
    def test_germany_2020(self):
        r = get_all_regions(2020, False, "de")
        assert len(r) == 17

    def test_austria_2020(self):
        r = get_all_regions(2020, False, "at")
        assert len(r) == 10

    def test_all_2020(self):
        r = get_all_regions(2020, False)
        assert len(r) == 28


# ═══════════════════════════════════════════════════════════════
# Brandenburg 2017
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonBrandenburg2017:
    """Verified against Go: region_test.go TestBrandenburg2017"""
    def test_count(self):
        r = brandenburg(2017, True)
        assert len(r.feiertage) == 12


# ═══════════════════════════════════════════════════════════════
# Fronleichnam in Bayern (index check)
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonFronleichnam:
    """Verified against Go: feiertagecmd_test.go TestGetRegion"""
    def test_bayern_fronleichnam_2016(self):
        r = bayern(2016, True)
        assert fmt(r.feiertage[7].datum) == "26.05.2016"

    def test_brandenburg_ostern_2016(self):
        r = brandenburg(2016, True)
        assert fmt(r.feiertage[2].datum) == "27.03.2016"


# ═══════════════════════════════════════════════════════════════
# Fixed date holidays (common across all DE)
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonFixedHolidays:
    """Common German holidays have fixed dates."""
    def test_neujahr(self):
        for y in [2015, 2016, 2020, 2026]:
            assert neujahr(y).datum == datetime.date(y, 1, 1)

    def test_tag_der_arbeit(self):
        for y in [2015, 2016, 2020, 2026]:
            assert tag_der_arbeit(y).datum == datetime.date(y, 5, 1)

    def test_tag_der_deutschen_einheit(self):
        for y in [2015, 2016, 2020, 2026]:
            assert tag_der_deutschen_einheit(y).datum == datetime.date(y, 10, 3)

    def test_weihnachten(self):
        for y in [2015, 2016, 2020, 2026]:
            assert weihnachten(y).datum == datetime.date(y, 12, 25)

    def test_zweiter_weihnachtsfeiertag(self):
        for y in [2015, 2016, 2020, 2026]:
            assert zweiter_weihnachtsfeiertag(y).datum == datetime.date(y, 12, 26)


# ═══════════════════════════════════════════════════════════════
# Easter-based offset verification
# ═══════════════════════════════════════════════════════════════

class TestGoComparisonEasterOffsets:
    """Verify Easter-based holidays have correct offsets."""
    def test_karfreitag_offset(self):
        for y in [2015, 2016, 2020]:
            o = ostern(y)
            assert karfreitag(y).datum == o.datum + datetime.timedelta(days=-2)

    def test_ostermontag_offset(self):
        for y in [2015, 2016, 2020]:
            o = ostern(y)
            assert ostermontag(y).datum == o.datum + datetime.timedelta(days=1)

    def test_christi_himmelfahrt_offset(self):
        for y in [2015, 2016, 2020]:
            o = ostern(y)
            assert christi_himmelfahrt(y).datum == o.datum + datetime.timedelta(days=39)

    def test_pfingstmontag_offset(self):
        for y in [2015, 2016, 2020]:
            o = ostern(y)
            assert pfingstmontag(y).datum == o.datum + datetime.timedelta(days=50)
