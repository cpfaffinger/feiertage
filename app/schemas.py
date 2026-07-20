"""Unified response schemas for the Feiertage API.

These Pydantic models are the single source of truth for the JSON response
shapes and drive the OpenAPI documentation shown in Swagger UI and ReDoc.

All endpoints also support the ``?format=`` query parameter (xml, csv, tsv,
txt). Those responses carry the same information as the JSON schema documented
here, serialized into the requested format.
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class Feiertag(BaseModel):
    """A single public holiday or special day."""
    date: str = Field(..., description="Date in ISO format (YYYY-MM-DD)", examples=["2026-01-01"])
    name: str = Field(..., description="Name of the holiday", examples=["Neujahr"])


class FeiertagInRegion(BaseModel):
    """A holiday together with the region it applies to."""
    name: str = Field(..., description="Name of the holiday", examples=["Leopolditag"])
    region: str = Field(..., description="Full region name", examples=["Niederösterreich"])
    region_short: str = Field(..., description="Region short code", examples=["NÖ"])


class RegionFeiertage(BaseModel):
    """Holidays of a single region, as nested in the /api/regions response."""
    name: str = Field(..., description="Full region name", examples=["Bayern"])
    shortname: str = Field(..., description="Region short code", examples=["BY"])
    count: int = Field(..., description="Number of holidays", examples=[12])
    feiertage: List[Feiertag] = Field(..., description="List of holidays")


class RegionsResponse(BaseModel):
    """Response of GET /api/regions."""
    year: int = Field(..., description="Queried year", examples=[2026])
    count: int = Field(..., description="Number of regions returned", examples=[27])
    regions: List[RegionFeiertage] = Field(..., description="Regions with their holidays")


class RegionResponse(BaseModel):
    """Response of GET /api/region/{name} and GET /api/feiertage."""
    year: int = Field(..., description="Queried year", examples=[2026])
    region: str = Field(..., description="Full region name", examples=["Bayern"])
    shortname: str = Field(..., description="Region short code", examples=["BY"])
    count: int = Field(..., description="Number of holidays", examples=[12])
    feiertage: List[Feiertag] = Field(..., description="List of holidays")


class DateFeiertageResponse(BaseModel):
    """Response of GET /api/feiertage/{datum}."""
    date: str = Field(..., description="Queried date (YYYY-MM-DD)", examples=["2026-12-25"])
    count: int = Field(..., description="Number of holidays on that date", examples=[1])
    feiertage: List[Feiertag] = Field(..., description="Holidays on that date")


class EasterResponse(BaseModel):
    """Response of GET /api/easter."""
    date: str = Field(..., description="Date of Easter Sunday (YYYY-MM-DD)", examples=["2026-04-05"])
    name: str = Field(..., description="Name of the holiday", examples=["Ostersonntag"])


class IsFeiertagResponse(BaseModel):
    """Response of GET /api/isFeiertag."""
    date: str = Field(..., description="Queried date (YYYY-MM-DD)", examples=["2026-11-15"])
    is_feiertag: bool = Field(..., description="Whether the date is a public holiday", examples=[True])
    feiertage: List[FeiertagInRegion] = Field(..., description="Matching holidays with their region")
    error: Optional[str] = Field(None, description="Error message, e.g. when the region is unknown")


class HealthResponse(BaseModel):
    """Response of GET /health."""
    status: str = Field(..., description="Service status", examples=["ok"])
