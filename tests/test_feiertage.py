"""Tests for feiertage.py - holiday calculation logic.

These tests validate against the Go reference implementation.
"""
import datetime
import pytest
from app.feiertage import (
    Feiertag, neujahr, epiphanias, heilige_drei_koenige, internationaler_frauentag,
    josefitag, karfreitag, ostern, ostermontag, tag_der_arbeit, staatsfeiertag,
    florianitag, tag_der_befreiung, christi_himmelfahrt, pfingsten, pfingstmontag,
    fronleichnam, mariae_himmelfahrt, rupertitag, tag_der_deutschen_einheit,
    tag_der_volksabstimmung, nationalfeiertag, reformationstag, allerheiligen,
    martinstag, leopolditag, weltkindertag, buss_und_bettag, mariae_empfaengnis,
    mariae_unbefleckte_empfaengnis, weihnachten, christtag, zweiter_weihnachtsfeiertag,
    stefanitag, valentinstag, internationaler_tag_des_gedenkens_an_die_opfer_des_holocaust,
    weiberfastnacht, karnevalssonntag, rosenmontag, fastnacht, aschermittwoch,
    palmasonntag, gruendonnerstag, beginn_sommerzeit, tag_der_erde, walpurgisnacht,
    internationaler_tag_der_pressefreiheit, muttertag, vatertag, dreifaltigkeitssonntag,
    internationaler_kindertag, tag_des_meeres, weltfluechtlingstag, antikriegstag,
    halloween, beginn_winterzeit, allerseelen, weltmaennertag, erntedankfest,
    nikolaus, erster_advent, zweiter_advent, dritter_advent, vierter_advent,
    volkstrauertag, totensonntag, heiligabend, silvester, weltknuddeltag,
    star_wars_day, handtuchtag, towel_day, weltumwelttag, weltspieltag,
    weltblutspendetag, fete_de_la_musique, internationaler_tag_gegen_drogenmissbrauch,
    system_administrator_appreciation_day, hobbit_day, internationaler_maennertag,
    karnevalsbeginn, thanksgiving, blackfriday,
)


# ── Easter (Ostern) tests - verified against Go reference ──

class TestOstern:
    def test_2015(self):
        assert ostern(2015).datum == datetime.date(2015, 4, 5)

    def test_2016(self):
        assert ostern(2016).datum == datetime.date(2016, 3, 27)

    def test_1954(self):
        assert ostern(1954).datum == datetime.date(1954, 4, 18)

    def test_1981(self):
        assert ostern(1981).datum == datetime.date(1981, 4, 19)

    def test_name(self):
        assert ostern(2020).name == "Ostern"


class TestOsternFormat:
    def test_2015_formatted(self):
        assert ostern(2015).datum.strftime("%d.%m.%Y") == "05.04.2015"

    def test_2016_formatted(self):
        assert ostern(2016).datum.strftime("%d.%m.%Y") == "27.03.2016"


# ── Sommerzeit / Winterzeit - verified against Go reference ──

class TestSommerWinterZeit:
    def test_sommerzeit_2015(self):
        assert beginn_sommerzeit(2015).datum.strftime("%d.%m.%Y") == "29.03.2015"

    def test_winterzeit_2016(self):
        assert beginn_winterzeit(2016).datum.strftime("%d.%m.%Y") == "30.10.2016"


# ── Buß- und Bettag - verified against Go reference ──

class TestBussUndBettag:
    def test_2015(self):
        assert buss_und_bettag(2015).datum.strftime("%d.%m.%Y") == "18.11.2015"

    def test_2016(self):
        assert buss_und_bettag(2016).datum.strftime("%d.%m.%Y") == "16.11.2016"


# ── Vorwärtssucher (forward-looking holidays) - verified against Go reference ──

class TestVorwaertssucher:
    def test_erntedankfest_2015(self):
        assert erntedankfest(2015).datum.strftime("%d.%m.%Y") == "04.10.2015"

    def test_erntedankfest_2016(self):
        assert erntedankfest(2016).datum.strftime("%d.%m.%Y") == "02.10.2016"

    def test_muttertag_2015(self):
        assert muttertag(2015).datum.strftime("%d.%m.%Y") == "10.05.2015"

    def test_muttertag_2016(self):
        assert muttertag(2016).datum.strftime("%d.%m.%Y") == "08.05.2016"


# ── Advent - verified against Go reference ──

class TestAdvent:
    def test_vierter_advent_2016(self):
        assert vierter_advent(2016).datum.strftime("%d.%m.%Y") == "18.12.2016"

    def test_dritter_advent_2016(self):
        assert dritter_advent(2016).datum.strftime("%d.%m.%Y") == "11.12.2016"

    def test_zweiter_advent_2016(self):
        assert zweiter_advent(2016).datum.strftime("%d.%m.%Y") == "04.12.2016"

    def test_erster_advent_2016(self):
        assert erster_advent(2016).datum.strftime("%d.%m.%Y") == "27.11.2016"

    def test_vierter_advent_2006(self):
        assert vierter_advent(2006).datum.strftime("%d.%m.%Y") == "24.12.2006"


# ── Thanksgiving - verified against Go reference ──

class TestThanksgiving:
    @pytest.mark.parametrize("year,expected", [
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
    ])
    def test_thanksgiving_dates(self, year, expected):
        assert thanksgiving(year).datum.strftime("%d.%m.%Y") == expected


# ── Black Friday is day after Thanksgiving ──

class TestBlackFriday:
    def test_2018(self):
        t = thanksgiving(2018)
        bf = blackfriday(2018)
        assert bf.datum == t.datum + datetime.timedelta(days=1)
    def test_2019(self):
        t = thanksgiving(2019)
        bf = blackfriday(2019)
        assert bf.datum == t.datum + datetime.timedelta(days=1)


# ── Feiertag class ──

class TestFeiertag:
    def test_to_dict(self):
        f = neujahr(2026)
        d = f.to_dict()
        assert d["date"] == "2026-01-01"
        assert d["name"] == "Neujahr"

    def test_feiertag_creation(self):
        f = Feiertag(datum=datetime.date(2025, 12, 25), name="Test")
        assert f.datum.year == 2025
        assert f.name == "Test"


# ── Fixed-date holidays ──

class TestFixedDateHolidays:
    def test_neujahr(self):
        assert neujahr(2026).datum == datetime.date(2026, 1, 1)
        assert neujahr(2026).name == "Neujahr"

    def test_epiphanias(self):
        assert epiphanias(2026).datum == datetime.date(2026, 1, 6)

    def test_heilige_drei_koenige(self):
        assert heilige_drei_koenige(2026).datum == datetime.date(2026, 1, 6)
        assert heilige_drei_koenige(2026).name == "Heilige drei Könige"

    def test_internationaler_frauentag(self):
        assert internationaler_frauentag(2026).datum == datetime.date(2026, 3, 8)

    def test_josefitag(self):
        assert josefitag(2026).datum == datetime.date(2026, 3, 19)

    def test_tag_der_arbeit(self):
        assert tag_der_arbeit(2026).datum == datetime.date(2026, 5, 1)

    def test_staatsfeiertag(self):
        assert staatsfeiertag(2026).datum == datetime.date(2026, 5, 1)
        assert staatsfeiertag(2026).name == "Staatsfeiertag"

    def test_florianitag(self):
        assert florianitag(2026).datum == datetime.date(2026, 5, 4)

    def test_tag_der_befreiung(self):
        assert tag_der_befreiung(2026).datum == datetime.date(2026, 5, 8)

    def test_mariae_himmelfahrt(self):
        assert mariae_himmelfahrt(2026).datum == datetime.date(2026, 8, 15)

    def test_rupertitag(self):
        assert rupertitag(2026).datum == datetime.date(2026, 9, 24)

    def test_weltkindertag(self):
        assert weltkindertag(2026).datum == datetime.date(2026, 9, 20)

    def test_tag_der_deutschen_einheit(self):
        assert tag_der_deutschen_einheit(2026).datum == datetime.date(2026, 10, 3)

    def test_tag_der_volksabstimmung(self):
        assert tag_der_volksabstimmung(2026).datum == datetime.date(2026, 10, 10)

    def test_nationalfeiertag(self):
        assert nationalfeiertag(2026).datum == datetime.date(2026, 10, 26)

    def test_reformationstag(self):
        assert reformationstag(2026).datum == datetime.date(2026, 10, 31)

    def test_allerheiligen(self):
        assert allerheiligen(2026).datum == datetime.date(2026, 11, 1)

    def test_martinstag(self):
        assert martinstag(2026).datum == datetime.date(2026, 11, 11)

    def test_leopolditag(self):
        assert leopolditag(2026).datum == datetime.date(2026, 11, 15)

    def test_mariae_unbefleckte_empfaengnis(self):
        assert mariae_unbefleckte_empfaengnis(2026).datum == datetime.date(2026, 12, 8)
        assert "unbefleckte" in mariae_unbefleckte_empfaengnis(2026).name

    def test_mariae_empfaengnis(self):
        assert mariae_empfaengnis(2026).datum == datetime.date(2026, 12, 8)
        assert mariae_empfaengnis(2026).name == "Mariä Empfängnis"

    def test_weihnachten(self):
        assert weihnachten(2026).datum == datetime.date(2026, 12, 25)

    def test_christtag(self):
        assert christtag(2026).datum == datetime.date(2026, 12, 25)
        assert christtag(2026).name == "Christtag"

    def test_zweiter_weihnachtsfeiertag(self):
        assert zweiter_weihnachtsfeiertag(2026).datum == datetime.date(2026, 12, 26)

    def test_stefanitag(self):
        assert stefanitag(2026).datum == datetime.date(2026, 12, 26)
        assert stefanitag(2026).name == "Stefanitag"


# ── Easter-based movable holidays ──

class TestEasterBasedHolidays:
    def test_karfreitag(self):
        o = ostern(2026)
        assert karfreitag(2026).datum == o.datum + datetime.timedelta(days=-2)

    def test_ostermontag(self):
        o = ostern(2026)
        assert ostermontag(2026).datum == o.datum + datetime.timedelta(days=1)

    def test_christi_himmelfahrt(self):
        o = ostern(2026)
        assert christi_himmelfahrt(2026).datum == o.datum + datetime.timedelta(days=39)

    def test_pfingsten(self):
        o = ostern(2026)
        assert pfingsten(2026).datum == o.datum + datetime.timedelta(days=49)

    def test_pfingstmontag(self):
        o = ostern(2026)
        assert pfingstmontag(2026).datum == o.datum + datetime.timedelta(days=50)

    def test_fronleichnam(self):
        o = ostern(2026)
        assert fronleichnam(2026).datum == o.datum + datetime.timedelta(days=60)

    def test_vatertag(self):
        assert vatertag(2026).datum == christi_himmelfahrt(2026).datum
        assert vatertag(2026).name == "Vatertag"
        assert isinstance(vatertag(2026), Feiertag)


# ── Carnival / Karneval holidays ──

class TestCarnival:
    def test_weiberfastnacht(self):
        o = ostern(2026)
        assert weiberfastnacht(2026).datum == o.datum + datetime.timedelta(days=-52)

    def test_karnevalssonntag(self):
        o = ostern(2026)
        assert karnevalssonntag(2026).datum == o.datum + datetime.timedelta(days=-49)

    def test_rosenmontag(self):
        o = ostern(2026)
        assert rosenmontag(2026).datum == o.datum + datetime.timedelta(days=-48)

    def test_fastnacht(self):
        o = ostern(2026)
        assert fastnacht(2026).datum == o.datum + datetime.timedelta(days=-47)

    def test_aschermittwoch(self):
        o = ostern(2026)
        assert aschermittwoch(2026).datum == o.datum + datetime.timedelta(days=-46)

    def test_karnevalsbeginn(self):
        assert karnevalsbeginn(2026).datum == datetime.date(2026, 11, 11)


# ── Other movable holidays ──

class TestOtherMovableHolidays:
    def test_palmasonntag(self):
        o = ostern(2026)
        assert palmasonntag(2026).datum == o.datum + datetime.timedelta(days=-7)

    def test_gruendonnerstag(self):
        o = ostern(2026)
        assert gruendonnerstag(2026).datum == o.datum + datetime.timedelta(days=-3)

    def test_dreifaltigkeitssonntag(self):
        o = ostern(2026)
        assert dreifaltigkeitssonntag(2026).datum == o.datum + datetime.timedelta(days=56)


# ── Special days ──

class TestSpecialDays:
    def test_valentinstag(self):
        assert valentinstag(2026).datum == datetime.date(2026, 2, 14)

    def test_holocaust_remembrance(self):
        f = internationaler_tag_des_gedenkens_an_die_opfer_des_holocaust(2026)
        assert f.datum == datetime.date(2026, 1, 27)
        assert "Holocaust" in f.name

    def test_weltknuddeltag(self):
        assert weltknuddeltag(2026).datum == datetime.date(2026, 1, 21)

    def test_star_wars_day(self):
        assert star_wars_day(2026).datum == datetime.date(2026, 5, 4)

    def test_handtuchtag(self):
        assert handtuchtag(2026).datum == datetime.date(2026, 5, 25)

    def test_towel_day(self):
        assert towel_day(2026).datum == datetime.date(2026, 5, 25)
        assert towel_day(2026).name == "Towel Day"

    def test_weltumwelttag(self):
        assert weltumwelttag(2026).datum == datetime.date(2026, 6, 5)

    def test_weltspieltag(self):
        assert weltspieltag(2026).datum == datetime.date(2026, 6, 11)

    def test_weltblutspendetag(self):
        assert weltblutspendetag(2026).datum == datetime.date(2026, 6, 14)

    def test_fete_de_la_musique(self):
        assert fete_de_la_musique(2026).datum == datetime.date(2026, 6, 21)

    def test_drogenmissbrauch(self):
        f = internationaler_tag_gegen_drogenmissbrauch(2026)
        assert f.datum == datetime.date(2026, 6, 26)

    def test_system_admin_day(self):
        f = system_administrator_appreciation_day(2025)
        assert f.datum.weekday() == 4  # Friday
        assert f.datum.month == 7  # July
        assert 25 <= f.datum.day <= 31  # Last Friday

    def test_system_admin_day_2026(self):
        f = system_administrator_appreciation_day(2026)
        assert f.datum.weekday() == 4  # Friday
        assert f.datum.month == 7
        assert f.datum == datetime.date(2026, 7, 31)

    def test_hobbit_day(self):
        assert hobbit_day(2020).datum == datetime.date(2020, 9, 22)

    def test_hobbit_day_before_1978(self):
        assert hobbit_day(1977) is None

    def test_internationaler_maennertag(self):
        assert internationaler_maennertag(2026).datum == datetime.date(2026, 11, 19)

    def test_tag_der_erde(self):
        assert tag_der_erde(2026).datum == datetime.date(2026, 4, 22)

    def test_walpurgisnacht(self):
        assert walpurgisnacht(2026).datum == datetime.date(2026, 4, 30)

    def test_pressefreiheit(self):
        f = internationaler_tag_der_pressefreiheit(2026)
        assert f.datum == datetime.date(2026, 5, 3)

    def test_internationaler_kindertag(self):
        assert internationaler_kindertag(2026).datum == datetime.date(2026, 6, 1)

    def test_tag_des_meeres(self):
        assert tag_des_meeres(2026).datum == datetime.date(2026, 6, 8)

    def test_weltfluechtlingstag(self):
        assert weltfluechtlingstag(2026).datum == datetime.date(2026, 6, 20)

    def test_antikriegstag(self):
        assert antikriegstag(2026).datum == datetime.date(2026, 9, 1)

    def test_halloween(self):
        assert halloween(2026).datum == datetime.date(2026, 10, 31)

    def test_allerseelen(self):
        assert allerseelen(2026).datum == datetime.date(2026, 11, 2)

    def test_weltmaennertag(self):
        assert weltmaennertag(2026).datum == datetime.date(2026, 11, 3)

    def test_nikolaus(self):
        assert nikolaus(2026).datum == datetime.date(2026, 12, 6)

    def test_heiligabend(self):
        assert heiligabend(2026).datum == datetime.date(2026, 12, 24)

    def test_silvester(self):
        assert silvester(2026).datum == datetime.date(2026, 12, 31)


# ── Volkstrauertag and Totensonntag ──

class TestVolkstrauertag:
    def test_volkstrauertag_offset(self):
        e = erster_advent(2026)
        assert volkstrauertag(2026).datum == e.datum + datetime.timedelta(days=-14)
        assert volkstrauertag(2026).datum.weekday() == 6  # Sunday

    def test_totensonntag_offset(self):
        v = vierter_advent(2026)
        assert totensonntag(2026).datum == v.datum + datetime.timedelta(days=-28)
        assert totensonntag(2026).datum.weekday() == 6  # Sunday


# ── Erntedankfest ──

class TestErntedankfest:
    def test_first_sunday_of_october(self):
        for year in range(2015, 2031):
            f = erntedankfest(year)
            assert f.datum.month == 10
            assert f.datum.weekday() == 6  # Sunday
            assert 1 <= f.datum.day <= 7  # First Sunday


# ── All holiday functions return valid dates ──

class TestAllHolidayFunctions:
    ALL_FUNCTIONS = [
        neujahr, epiphanias, heilige_drei_koenige, valentinstag,
        internationaler_tag_des_gedenkens_an_die_opfer_des_holocaust, josefitag,
        weiberfastnacht, karnevalssonntag, rosenmontag, fastnacht, aschermittwoch,
        internationaler_frauentag, palmasonntag, gruendonnerstag, karfreitag,
        ostern, beginn_sommerzeit, ostermontag, walpurgisnacht, tag_der_arbeit,
        tag_der_befreiung, staatsfeiertag, internationaler_tag_der_pressefreiheit,
        florianitag, muttertag, christi_himmelfahrt, vatertag, pfingsten,
        pfingstmontag, dreifaltigkeitssonntag, fronleichnam, tag_des_meeres,
        mariae_himmelfahrt, rupertitag, internationaler_kindertag,
        weltfluechtlingstag, tag_der_deutschen_einheit,
        tag_der_volksabstimmung, nationalfeiertag, erntedankfest,
        reformationstag, halloween, beginn_winterzeit, allerheiligen,
        allerseelen, martinstag, karnevalsbeginn, leopolditag, weltkindertag,
        buss_und_bettag, thanksgiving, blackfriday, volkstrauertag, nikolaus,
        mariae_unbefleckte_empfaengnis, mariae_empfaengnis, totensonntag,
        erster_advent, zweiter_advent, dritter_advent, vierter_advent,
        heiligabend, weihnachten, christtag, stefanitag,
        zweiter_weihnachtsfeiertag, silvester,
        # Special days
        weltknuddeltag, star_wars_day, handtuchtag, towel_day,
        weltumwelttag, weltspieltag, weltblutspendetag, fete_de_la_musique,
        internationaler_tag_gegen_drogenmissbrauch,
        system_administrator_appreciation_day, internationaler_maennertag,
        antikriegstag,
    ]

    @pytest.mark.parametrize("year", [2015, 2016])
    @pytest.mark.parametrize("f", ALL_FUNCTIONS)
    def test_valid_dates(self, f, year):
        result = f(year)
        if result is not None:  # hobbit_day returns None for year < 1978
            assert result.datum.year == year
            assert isinstance(result.datum, datetime.date)
            assert isinstance(result.name, str)
            assert len(result.name) > 0

    @pytest.mark.parametrize("year", [2020, 2024, 2026])
    @pytest.mark.parametrize("f", ALL_FUNCTIONS)
    def test_valid_dates_extended(self, f, year):
        result = f(year)
        if result is not None:
            assert result.datum.year == year
            assert isinstance(result.datum, datetime.date)
            assert isinstance(result.name, str)


class TestNthWeekdayOfMonth:
    def test_nth_weekday(self):
        from app.feiertage import _nth_weekday_of_month
        result = _nth_weekday_of_month(2026, 11, 3, 4)
        assert result.day == 26
        assert result.month == 11
        assert result.year == 2026
        assert result.weekday() == 3
