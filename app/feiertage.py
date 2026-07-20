from datetime import date, timedelta
from dataclasses import dataclass, field
from typing import Callable, Optional
import json


@dataclass
class Feiertag:
    datum: date
    name: str
    regions: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"date": self.datum.isoformat(), "name": self.name}


_default_time_format = "%d.%m.%Y"


def _go_weekday(d: date) -> int:
    """Convert Python weekday (Mon=0) to Go weekday (Sun=0)."""
    return d.isoweekday() % 7


def _ostern(year: int) -> Feiertag:
    """Extended Gauss algorithm for Easter."""
    k = year // 100
    m = 15 + (3 * k + 3) // 4 - (8 * k + 13) // 25
    s = 2 - (3 * k + 3) // 4
    a = year % 19
    d = (19 * a + m) % 30
    r = (d + a // 11) // 29
    og = 21 + d - r
    sz = 7 - (year + year // 4 + s) % 7
    oe = 7 - (og - sz) % 7
    os = og + oe

    day = os % 31
    if day == 0:
        day = 31
        month = os // 31 + 2
    else:
        month = os // 31 + 3

    return Feiertag(datum=date(year, month, day), name="Ostern")


# ── Fixed-date holidays ──

def neujahr(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 1, 1), name="Neujahr")


def epiphanias(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 1, 6), name="Epiphanias")


def heilige_drei_koenige(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 1, 6), name="Heilige drei Könige")


def internationaler_frauentag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 3, 8), name="Internationaler Frauentag")


def josefitag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 3, 19), name="Josefitag")


def tag_der_arbeit(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 1), name="Tag der Arbeit")


def staatsfeiertag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 1), name="Staatsfeiertag")


def florianitag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 4), name="Florianitag")


def tag_der_befreiung(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 8), name="Tag der Befreiung")


def mariae_himmelfahrt(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 8, 15), name="Mariä Himmelfahrt")


def rupertitag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 9, 24), name="Rupertitag")


def weltkindertag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 9, 20), name="Weltkindertag")


def tag_der_deutschen_einheit(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 10, 3), name="Tag der deutschen Einheit")


def tag_der_volksabstimmung(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 10, 10), name="Tag der Volksabstimmung")


def nationalfeiertag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 10, 26), name="Nationalfeiertag")


def reformationstag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 10, 31), name="Reformationstag")


def allerheiligen(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 11, 1), name="Allerheiligen")


def martinstag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 11, 11), name="Martinstag")


def leopolditag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 11, 15), name="Leopolditag")


def mariae_unbefleckte_empfaengnis(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 8), name="Mariä unbefleckte Empfängnis")


def mariae_empfaengnis(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 8), name="Mariä Empfängnis")


def weihnachten(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 25), name="Weihnachten")


def christtag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 25), name="Christtag")


def zweiter_weihnachtsfeiertag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 26), name="Zweiter Weihnachtsfeiertag")


def stefanitag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 26), name="Stefanitag")


# ── Easter-based movable holidays ──

def karfreitag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-2), name="Karfreitag")


def ostern(year: int) -> Feiertag:
    return _ostern(year)


def ostermontag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=1), name="Ostermontag")


def christi_himmelfahrt(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=39), name="Christi Himmelfahrt")


def pfingsten(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=49), name="Pfingsten")


def pfingstmontag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=50), name="Pfingstmontag")


def fronleichnam(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=60), name="Fronleichnam")


# ── Special calculated holidays ──

def _last_sunday_of_month(year: int, month: int) -> date:
    d = date(year, month, 1)
    last_day = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    days_since_sunday = (last_day.weekday() + 1) % 7
    return last_day - timedelta(days=days_since_sunday)


def _first_sunday_of_month(year: int, month: int) -> date:
    d = date(year, month, 1)
    days_until_sunday = (6 - d.weekday()) % 7
    return d + timedelta(days=days_until_sunday)


def _nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    first = date(year, month, 1)
    first_wday = first.weekday()
    days_until = (weekday - first_wday) % 7
    return first + timedelta(days=days_until + 7 * (n - 1))


def buss_und_bettag(year: int) -> Feiertag:
    o = date(year, 11, 22)
    d = (4 + _go_weekday(o)) % 7
    return Feiertag(datum=o + timedelta(days=-d), name="Buß- und Bettag")


# ── Special days ──

def weltknuddeltag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 1, 21), name="Weltknuddeltag")


def star_wars_day(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 4), name="Star Wars Day")


def handtuchtag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 25), name="Handtuchtag")


def towel_day(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 25), name="Towel Day")


def weltumwelttag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 5), name="Weltumwelttag")


def weltspieltag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 11), name="Weltspieltag")


def weltblutspendetag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 14), name="Weltblutspendetag")


def fete_de_la_musique(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 21), name="Fête de la Musique")


def internationaler_tag_gegen_drogenmissbrauch(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 26), name="Internationaler Tag gegen Drogenmissbrauch")


def system_administrator_appreciation_day(year: int) -> Feiertag:
    o = date(year, 7, 31)
    d = (2 + _go_weekday(o)) % 7
    return Feiertag(datum=o + timedelta(days=-d), name="System Administrator Appreciation Day")


def hobbit_day(year: int) -> Feiertag:
    if year >= 1978:
        return Feiertag(datum=date(year, 9, 22), name="Hobbit Day")
    return None


def internationaler_maennertag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 11, 19), name="Internationaler Männertag")


def karnevalsbeginn(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 11, 11), name="Karnevalsbeginn")


def thanksgiving(year: int) -> Feiertag:
    o = date(year, 11, 1)
    d = (11 - _go_weekday(o)) % 7
    return Feiertag(datum=o + timedelta(days=21 + d), name="Thanksgiving (US)")


def blackfriday(year: int) -> Feiertag:
    t = thanksgiving(year)
    return Feiertag(datum=t.datum + timedelta(days=1), name="Blackfriday")


def valentinstag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 2, 14), name="Valentinstag")


def internationaler_tag_des_gedenkens_an_die_opfer_des_holocaust(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 1, 27), name="Internationaler Tag des Gedenkens an die Opfer des Holocaust")


def weiberfastnacht(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-52), name="Weiberfastnacht")


def karnevalssonntag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-49), name="Karnevalssonntag")


def rosenmontag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-48), name="Rosenmontag")


def fastnacht(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-47), name="Fastnacht")


def aschermittwoch(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-46), name="Aschermittwoch")


def palmasonntag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-7), name="Palmsonntag")


def gruendonnerstag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=-3), name="Gründonnerstag")


def beginn_sommerzeit(year: int) -> Feiertag:
    return Feiertag(datum=_last_sunday_of_month(year, 3), name="Beginn Sommerzeit")


def tag_der_erde(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 4, 22), name="Tag der Erde")


def walpurgisnacht(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 4, 30), name="Walpurgisnacht")


def internationaler_tag_der_pressefreiheit(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 5, 3), name="Internationaler Tag der Pressefreiheit")


def muttertag(year: int) -> Feiertag:
    o = date(year, 5, 1)
    d = (7 - _go_weekday(o)) % 7
    return Feiertag(datum=o + timedelta(days=d + 7), name="Muttertag")


def vatertag(year: int) -> Feiertag:
    e = christi_himmelfahrt(year)
    return Feiertag(datum=e.datum, name="Vatertag")


def dreifaltigkeitssonntag(year: int) -> Feiertag:
    o = _ostern(year)
    return Feiertag(datum=o.datum + timedelta(days=56), name="Dreifaltigkeitssonntag")


def internationaler_kindertag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 1), name="Internationaler Kindertag")


def tag_des_meeres(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 8), name="Tag des Meeres")


def weltfluechtlingstag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 6, 20), name="Weltflüchtlingstag")


def antikriegstag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 9, 1), name="Antikriegstag")


def halloween(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 10, 31), name="Halloween")


def beginn_winterzeit(year: int) -> Feiertag:
    return Feiertag(datum=_last_sunday_of_month(year, 10), name="Beginn Winterzeit")


def allerseelen(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 11, 2), name="Allerseelen")


def weltmaennertag(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 11, 3), name="Weltmännertag")


def erntedankfest(year: int) -> Feiertag:
    return Feiertag(datum=_first_sunday_of_month(year, 10), name="Erntedankfest")


def nikolaus(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 6), name="Nikolaus")


def vierter_advent(year: int) -> Feiertag:
    o = date(year, 12, 24)
    d = (7 + _go_weekday(o)) % 7
    return Feiertag(datum=o + timedelta(days=-d), name="Vierter Advent")


def dritter_advent(year: int) -> Feiertag:
    o = vierter_advent(year)
    return Feiertag(datum=o.datum + timedelta(days=-7), name="Dritter Advent")


def zweiter_advent(year: int) -> Feiertag:
    o = vierter_advent(year)
    return Feiertag(datum=o.datum + timedelta(days=-14), name="Zweiter Advent")


def erster_advent(year: int) -> Feiertag:
    o = vierter_advent(year)
    return Feiertag(datum=o.datum + timedelta(days=-21), name="Erster Advent")


def volkstrauertag(year: int) -> Feiertag:
    o = erster_advent(year)
    return Feiertag(datum=o.datum + timedelta(days=-14), name="Volkstrauertag")


def totensonntag(year: int) -> Feiertag:
    o = vierter_advent(year)
    return Feiertag(datum=o.datum + timedelta(days=-28), name="Totensonntag")


def heiligabend(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 24), name="Heiligabend")


def silvester(year: int) -> Feiertag:
    return Feiertag(datum=date(year, 12, 31), name="Silvester")
