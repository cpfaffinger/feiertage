"""Feiertage API - German and Austrian Holiday API.

This API provides access to public holidays in all German federal states (Bundesländer)
and Austrian states, as well as various special days.

No authentication required - completely open and public.

Supported output formats: json, xml, csv, tsv, txt
"""
from datetime import date
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from app.region import (
    get_all_regions,
    get_region,
    get_feiertage_for_date_in_region,
    get_feiertage_for_date,
    is_feiertag,
)
from app.feiertage import Feiertag
from app.formatter import format_response, AVAILABLE_FORMATS

app = FastAPI(
    title="Feiertage API",
    description="Gesetzliche Feiertage in Deutschland und Österreich. "
                "Public holiday API for Germany and Austria - open and free for everyone.",
    version="1.0.0",
    contact={"name": "Feiertage API"},
    license_info={"name": "MIT"},
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

FORMAT_DESCRIPTION = f"Output format: {', '.join(AVAILABLE_FORMATS)}"


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/api/regions")
async def api_regions(
    year: int = Query(..., description="Year to query"),
    inkl_sonntage: bool = Query(False, description="Include Sundays"),
    country: Optional[str] = Query(None, description="Filter by country: 'de' or 'at'"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get all regions with their holidays for a given year."""
    regions = get_all_regions(year, inkl_sonntage, country)
    data = {
        "year": year,
        "count": len(regions),
        "regions": [
            {
                "name": r.name,
                "shortname": r.shortname,
                "count": len(r.feiertage),
                "feiertage": [f.to_dict() for f in r.feiertage],
            }
            for r in regions
        ],
    }
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/region/{region_name}")
async def api_region(
    region_name: str,
    year: int = Query(..., description="Year to query"),
    inkl_sonntage: bool = Query(False, description="Include Sundays"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get holidays for a specific region."""
    r = get_region(region_name, year, inkl_sonntage)
    if r is None:
        raise HTTPException(status_code=404, detail=f"Region '{region_name}' not found")
    data = {
        "year": year,
        "region": r.name,
        "shortname": r.shortname,
        "count": len(r.feiertage),
        "feiertage": [f.to_dict() for f in r.feiertage],
    }
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/feiertage")
async def api_feiertage(
    year: int = Query(..., description="Year to query"),
    region: Optional[str] = Query(None, description="Region name"),
    inkl_sonntage: bool = Query(False, description="Include Sundays"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get all holidays for a year, optionally filtered by region."""
    if region:
        r = get_region(region, year, inkl_sonntage)
        if r is None:
            raise HTTPException(status_code=404, detail=f"Region '{region}' not found")
        feiertage = r.feiertage
        region_name = r.name
    else:
        r = get_region("Alle", year, True)
        feiertage = r.feiertage
        region_name = "Alle"

    data = {
        "year": year,
        "region": region_name,
        "count": len(feiertage),
        "feiertage": [f.to_dict() for f in feiertage],
    }
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/feiertage/{datum}")
async def api_feiertage_by_date(
    datum: str,
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get holidays for a specific date (YYYY-MM-DD)."""
    try:
        parts = datum.split("-")
        d = date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    result = get_feiertage_for_date(d)
    data = {
        "date": d.isoformat(),
        "count": len(result),
        "feiertage": [f.to_dict() for f in result],
    }
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/easter")
async def api_easter(
    year: int = Query(..., description="Year to calculate Easter for"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get the date of Easter (Ostersonntag) for a given year."""
    from app.feiertage import ostern as calc_ostern
    o = calc_ostern(year)
    data = o.to_dict()
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/isFeiertag")
async def api_is_feiertag(
    datum: str = Query(..., alias="date", description="Date in YYYY-MM-DD format"),
    region: Optional[str] = Query(None, description="Region name (optional, regions are unique across countries)"),
    inkl_sonntage: bool = Query(False, description="Include Sundays"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Check whether a given date is a public holiday.

    Can optionally filter by region. Regions are unique across Germany and Austria,
    so the country parameter is not needed.

    Examples:
    - /api/isFeiertag?date=2026-04-06
    - /api/isFeiertag?date=2026-04-06&region=Niederösterreich
    """
    try:
        parts = datum.split("-")
        d = date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    data = is_feiertag(d, region, inkl_sonntage)
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)
