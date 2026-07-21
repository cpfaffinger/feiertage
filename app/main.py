"""Feiertage API - German and Austrian Holiday API.

This API provides access to public holidays in all German federal states (Bundesländer)
and Austrian states, as well as various special days.

No authentication required - completely open and public.

Supported output formats: json, xml, csv, tsv, txt
"""
from datetime import date as Date
from typing import Optional
import httpx
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_redoc_html
from app.region import (
    get_all_regions,
    get_region,
    get_feiertage_for_date,
    get_holiday_status,
)
from app.formatter import format_response, AVAILABLE_FORMATS
from app.schemas import (
    RegionsResponse,
    RegionResponse,
    DateFeiertageResponse,
    EasterResponse,
    IsFeiertagResponse,
    HealthResponse,
)

_REDOC_JS_URL = "https://cdn.jsdelivr.net/npm/redoc@2.2.0/bundles/redoc.standalone.js"
_redoc_js_cache: Optional[str] = None

app = FastAPI(
    title="Feiertage API",
    description="Gesetzliche Feiertage in Deutschland und Österreich. "
                "Public holiday API for Germany and Austria - open and free for everyone.",
    version="3.0.1",
    contact={"name": "Feiertage API"},
    license_info={"name": "MIT"},
    openapi_url="/openapi.json",
    docs_url="/docs",
    # Default ReDoc route is disabled and replaced by a custom one below that
    # serves the JS bundle from our self-hosted /redoc.js proxy. FastAPI's
    # constructor has no redoc_js_url parameter (it is silently ignored via
    # **extra), so the default route would always load from the CDN.
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

FORMAT_DESCRIPTION = f"Output format: {', '.join(AVAILABLE_FORMATS)}"


@app.get("/redoc.js", include_in_schema=False)
async def redoc_js():
    """Proxy Redoc JS with correct MIME type to avoid browser blocking."""
    global _redoc_js_cache
    if _redoc_js_cache is None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(_REDOC_JS_URL, timeout=30)
            resp.raise_for_status()
            _redoc_js_cache = resp.text
    return Response(content=_redoc_js_cache, media_type="application/javascript")


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """Serve ReDoc using the self-hosted JS bundle instead of the CDN."""
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="Feiertage API - ReDoc",
        redoc_js_url="/redoc.js",
    )


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("app/static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/api/regions", response_model=RegionsResponse)
async def api_regions(
    year: Optional[int] = Query(None, description="Year to query (defaults to current year)"),
    include_sundays: bool = Query(False, alias="includeSundays", description="Include Sundays"),
    country: Optional[str] = Query(None, description="Filter by country: 'de' or 'at'"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get all regions with their holidays for a given year."""
    if year is None:
        year = Date.today().year
    regions = get_all_regions(year, include_sundays, country)
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


@app.get("/api/region/{regionName}", response_model=RegionResponse)
async def api_region(
    regionName: str,
    year: Optional[int] = Query(None, description="Year to query (defaults to current year)"),
    include_sundays: bool = Query(False, alias="includeSundays", description="Include Sundays"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get holidays for a specific region."""
    if year is None:
        year = Date.today().year
    r = get_region(regionName, year, include_sundays)
    if r is None:
        raise HTTPException(status_code=404, detail=f"Region '{regionName}' not found")
    data = {
        "year": year,
        "region": r.name,
        "shortname": r.shortname,
        "count": len(r.feiertage),
        "feiertage": [f.to_dict() for f in r.feiertage],
    }
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/feiertage", response_model=RegionResponse)
async def api_feiertage(
    year: Optional[int] = Query(None, description="Year to query (defaults to current year)"),
    region: Optional[str] = Query(None, description="Region name"),
    include_sundays: bool = Query(False, alias="includeSundays", description="Include Sundays"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get all holidays for a year, optionally filtered by region."""
    if year is None:
        year = Date.today().year
    if region:
        r = get_region(region, year, include_sundays)
        if r is None:
            raise HTTPException(status_code=404, detail=f"Region '{region}' not found")
    else:
        r = get_region("Alle", year, include_sundays)
    feiertage = r.feiertage

    data = {
        "year": year,
        "region": r.name,
        "shortname": r.shortname,
        "count": len(feiertage),
        "feiertage": [f.to_dict() for f in feiertage],
    }
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/feiertage/{date}", response_model=DateFeiertageResponse)
async def api_feiertage_by_date(
    date: str,
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get holidays for a specific date (YYYY-MM-DD)."""
    try:
        parts = date.split("-")
        d = Date(int(parts[0]), int(parts[1]), int(parts[2]))
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


@app.get("/api/easter", response_model=EasterResponse)
async def api_easter(
    year: Optional[int] = Query(None, description="Year to calculate Easter for (defaults to current year)"),
    fmt: str = Query("json", alias="format", description=FORMAT_DESCRIPTION),
):
    """Get the date of Easter (Ostersonntag) for a given year."""
    if year is None:
        year = Date.today().year
    from app.feiertage import ostern as calc_ostern
    o = calc_ostern(year)
    data = o.to_dict()
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/api/isFeiertag", response_model=IsFeiertagResponse)
async def api_is_feiertag(
    requested_date: str = Query(..., alias="date", description="Date in YYYY-MM-DD format"),
    region: Optional[str] = Query(None, description="Region name (optional, regions are unique across countries)"),
    include_sundays: bool = Query(False, alias="includeSundays", description="Include Sundays"),
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
        parts = requested_date.split("-")
        d = Date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    data = get_holiday_status(d, region, include_sundays)
    body, content_type = format_response(data, fmt)
    return Response(content=body, media_type=content_type)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
