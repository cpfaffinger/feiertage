from datetime import date
from dataclasses import dataclass, field
from typing import Callable, Optional
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


@dataclass
class Region:
    name: str
    shortname: str
    feiertage: list = field(default_factory=list)


def _create_common_feiertags_list() -> list:
    return [neujahr, ostermontag, christi_himmelfahrt, pfingstmontag]


def _create_uniq_austrian_feiertags_list() -> list:
    return [heilige_drei_koenige, staatsfeiertag, fronleichnam, mariae_himmelfahrt,
            nationalfeiertag, allerheiligen, mariae_empfaengnis, christtag, stefanitag]


def _create_uniq_german_feiertags_list(year: int) -> list:
    feiern = [karfreitag, tag_der_arbeit, tag_der_deutschen_einheit,
              weihnachten, zweiter_weihnachtsfeiertag]
    if year == 2017:
        feiern.insert(0, reformationstag)
    return feiern


def _feiertags_function_list_to_feiertag_list(ffun: list, y: int) -> list:
    result = []
    for f in ffun:
        ft = f(y)
        if ft is not None:
            result.append(ft)
    return result


def _create_feiertags_list(year: int, country: str, ffun: list) -> list:
    feiern: list = _create_common_feiertags_list()

    if country == "AT":
        nfeiern = _create_uniq_austrian_feiertags_list()
    else:
        nfeiern = _create_uniq_german_feiertags_list(year)

    feiern.extend(nfeiern)

    for f in ffun:
        ft = f(year)
        if ft is None:
            continue
        if year == 2017 and ft.datum == reformationstag(year).datum:
            continue
        feiern.append(f)

    feiertermine = _feiertags_function_list_to_feiertag_list(feiern, year)
    feiertermine.sort(key=lambda x: x.datum)
    return feiertermine


# ── German regions ──

def baden_wuerttemberg(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [epiphanias, fronleichnam, allerheiligen]
    return Region(name="Baden-Württemberg", shortname="BW",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def bayern(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [epiphanias, fronleichnam, allerheiligen]
    return Region(name="Bayern", shortname="BY",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def berlin(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = []
    if year >= 2019:
        ffun.append(internationaler_frauentag)
    if year == 2020 or year == 2025:
        ffun.append(tag_der_befreiung)
    return Region(name="Berlin", shortname="BE",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def brandenburg(year: int, inkl_sonntage: bool = False) -> Region:
    if not inkl_sonntage:
        ffun = [reformationstag]
    else:
        ffun = [ostern, pfingsten, reformationstag]
    return Region(name="Brandenburg", shortname="BB",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def bremen(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = []
    if year >= 2018:
        ffun.append(reformationstag)
    return Region(name="Bremen", shortname="HB",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def hamburg(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = []
    if year >= 2018:
        ffun.append(reformationstag)
    return Region(name="Hamburg", shortname="HH",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def hessen(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [fronleichnam]
    return Region(name="Hessen", shortname="HE",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def mecklenburg_vorpommern(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [reformationstag]
    if year >= 2023:
        ffun.append(internationaler_frauentag)
    return Region(name="Mecklenburg-Vorpommern", shortname="MV",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def niedersachsen(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = []
    if year >= 2018:
        ffun.append(reformationstag)
    return Region(name="Niedersachsen", shortname="NI",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def nordrhein_westfalen(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [fronleichnam, allerheiligen]
    return Region(name="Nordrhein-Westfalen", shortname="NW",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def rheinland_pfalz(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [fronleichnam, allerheiligen]
    return Region(name="Rheinland-Pfalz", shortname="RP",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def saarland(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [fronleichnam, mariae_himmelfahrt, allerheiligen]
    return Region(name="Saarland", shortname="SL",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def sachsen(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [reformationstag, buss_und_bettag]
    return Region(name="Sachsen", shortname="SN",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def sachsen_anhalt(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [epiphanias, reformationstag]
    return Region(name="Sachsen-Anhalt", shortname="ST",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def schleswig_holstein(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = []
    if year >= 2018:
        ffun.append(reformationstag)
    return Region(name="Schleswig-Holstein", shortname="SH",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def thueringen(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [reformationstag]
    if year >= 2019:
        ffun.append(weltkindertag)
    return Region(name="Thüringen", shortname="TH",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


def deutschland(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = []
    return Region(name="Deutschland", shortname="DE",
                  feiertage=_create_feiertags_list(year, "DE", ffun))


# ── Austrian regions ──

def burgenland(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [martinstag]
    return Region(name="Burgenland", shortname="Bgld",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def kaernten(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [josefitag, tag_der_volksabstimmung]
    return Region(name="Kärnten", shortname="Ktn",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def niederoesterreich(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [leopolditag]
    return Region(name="Niederösterreich", shortname="NÖ",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def oberoesterreich(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [florianitag]
    return Region(name="Oberösterreich", shortname="OÖ",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def salzburg(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [rupertitag]
    return Region(name="Salzburg", shortname="Sbg",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def steiermark(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [josefitag]
    return Region(name="Steiermark", shortname="Stmk",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def tirol(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [josefitag]
    return Region(name="Tirol", shortname="T",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def vorarlberg(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [josefitag]
    return Region(name="Vorarlberg", shortname="Vbg",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def wien(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = [leopolditag]
    return Region(name="Wien", shortname="W",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


def oesterreich(year: int, inkl_sonntage: bool = False) -> Region:
    ffun = []
    return Region(name="Österreich", shortname="AT",
                  feiertage=_create_feiertags_list(year, "AT", ffun))


# ── All holidays ──

def all_holidays(year: int, inkl_sonntage: bool = False) -> Region:
    feiern = [epiphanias, valentinstag, internationaler_tag_des_gedenkens_an_die_opfer_des_holocaust,
              josefitag, weiberfastnacht, rosenmontag, fastnacht, aschermittwoch,
              gruendonnerstag, internationaler_kindertag, tag_des_meeres,
              weltfluechtlingstag, beginn_sommerzeit, walpurgisnacht,
              internationaler_tag_der_pressefreiheit, tag_der_erde,
              internationaler_tag_gegen_drogenmissbrauch, fete_de_la_musique,
              florianitag, tag_der_befreiung, muttertag, vatertag, handtuchtag,
              towel_day, system_administrator_appreciation_day, rupertitag,
              tag_der_volksabstimmung, halloween, beginn_winterzeit, allerseelen,
              weltmaennertag, martinstag, karnevalsbeginn, leopolditag,
              weltumwelttag, weltspieltag, weltblutspendetag,
              internationaler_maennertag, star_wars_day, weltknuddeltag,
              weltkindertag, buss_und_bettag, thanksgiving, blackfriday,
              nikolaus, mariae_unbefleckte_empfaengnis, heiligabend,
              silvester, antikriegstag]

    if year != 2017:
        feiern.append(reformationstag)
    if year >= 2019:
        feiern.append(internationaler_frauentag)
    if year >= 1978:
        feiern.append(hobbit_day)

    feiern.extend(_create_common_feiertags_list())
    feiern.extend(_create_uniq_austrian_feiertags_list())
    feiern.extend(_create_uniq_german_feiertags_list(year))

    if inkl_sonntage:
        feiern.extend([karnevalssonntag, palmasonntag, ostern, pfingsten,
                       dreifaltigkeitssonntag, erntedankfest, volkstrauertag,
                       totensonntag, erster_advent, zweiter_advent, dritter_advent,
                       vierter_advent])

    feiertermine = _feiertags_function_list_to_feiertag_list(feiern, year)
    feiertermine.sort(key=lambda x: x.datum)
    return Region(name="Alle", shortname="All", feiertage=feiertermine)


# ── Region lookup ──

_ALL_REGIONS = {
    # German
    "Baden-Württemberg": baden_wuerttemberg,
    "Bayern": bayern,
    "Berlin": berlin,
    "Brandenburg": brandenburg,
    "Bremen": bremen,
    "Hamburg": hamburg,
    "Hessen": hessen,
    "Mecklenburg-Vorpommern": mecklenburg_vorpommern,
    "Niedersachsen": niedersachsen,
    "Nordrhein-Westfalen": nordrhein_westfalen,
    "Rheinland-Pfalz": rheinland_pfalz,
    "Saarland": saarland,
    "Sachsen": sachsen,
    "Sachsen-Anhalt": sachsen_anhalt,
    "Schleswig-Holstein": schleswig_holstein,
    "Thüringen": thueringen,
    "Deutschland": deutschland,
    # Austrian
    "Burgenland": burgenland,
    "Kärnten": kaernten,
    "Niederösterreich": niederoesterreich,
    "Oberösterreich": oberoesterreich,
    "Salzburg": salzburg,
    "Steiermark": steiermark,
    "Tirol": tirol,
    "Vorarlberg": vorarlberg,
    "Wien": wien,
    "Österreich": oesterreich,
    # All
    "Alle": all_holidays,
}

_SHORTNAME_MAP = {r(2020, False).shortname: r for r in _ALL_REGIONS.values()}
_SHORTNAME_MAP["DE"] = deutschland
_SHORTNAME_MAP["AT"] = oesterreich
_SHORTNAME_MAP["All"] = all_holidays


def _canonicalize(s: str) -> str:
    return s.lower().replace("-", "").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")


def get_region(name: str, year: int, inkl_sonntage: bool = False) -> Optional[Region]:
    c = _canonicalize(name)
    for rname, rfn in _ALL_REGIONS.items():
        if _canonicalize(rname) == c or _canonicalize(rfn(year, inkl_sonntage).shortname) == c:
            return rfn(year, inkl_sonntage)
    return None


def get_all_regions(year: int, inkl_sonntage: bool = False, country: str = None) -> list:
    german_regions = [baden_wuerttemberg, bayern, berlin, brandenburg, bremen,
                      hamburg, hessen, mecklenburg_vorpommern, niedersachsen,
                      nordrhein_westfalen, rheinland_pfalz, saarland, sachsen,
                      sachsen_anhalt, schleswig_holstein, thueringen, deutschland]

    austrian_regions = [burgenland, kaernten, niederoesterreich, oberoesterreich,
                        salzburg, steiermark, tirol, vorarlberg, wien, oesterreich]

    if country:
        c = country.lower()
        if c == "de":
            funcs = german_regions
        elif c == "at":
            funcs = austrian_regions
        else:
            funcs = []
        return [f(year, inkl_sonntage) for f in funcs]
    else:
        return [f(year, inkl_sonntage) for f in german_regions] + \
               [f(year, inkl_sonntage) for f in austrian_regions] + \
               [all_holidays(year, inkl_sonntage)]


def get_feiertage_for_date_in_region(d: date, region_fn, inkl_sonntage: bool = False) -> list:
    r = region_fn(d.year, inkl_sonntage)
    result = []
    for f in r.feiertage:
        if f.datum == d:
            result.append(f)
    return result


def get_feiertage_for_date(d: date) -> list:
    r = all_holidays(d.year, True)
    result = []
    for f in r.feiertage:
        if f.datum == d:
            result.append(f)
    return result


def is_feiertag(d: date, region_name: str = None, inkl_sonntage: bool = False) -> dict:
    """Check whether a date is a holiday, optionally filtered by region.

    Returns a dict with keys: date, is_feiertag, feiertage (list of {name, region}).
    If region_name is given, feiertage are specific to that region.
    Otherwise checks all regions.
    """
    if region_name:
        r = get_region(region_name, d.year, inkl_sonntage)
        if r is None:
            return {"date": d.isoformat(), "is_feiertag": False, "feiertage": [], "error": f"Region '{region_name}' not found"}
        matching = [f for f in r.feiertage if f.datum == d]
        return {
            "date": d.isoformat(),
            "is_feiertag": len(matching) > 0,
            "feiertage": [{"name": f.name, "region": r.name, "region_short": r.shortname} for f in matching],
        }

    all_regions = get_all_regions(d.year, inkl_sonntage)
    results = []
    for reg in all_regions:
        for f in reg.feiertage:
            if f.datum == d and f.name not in [x["name"] for x in results]:
                results.append({
                    "name": f.name,
                    "region": reg.name,
                    "region_short": reg.shortname,
                })

    return {
        "date": d.isoformat(),
        "is_feiertag": len(results) > 0,
        "feiertage": results,
    }
