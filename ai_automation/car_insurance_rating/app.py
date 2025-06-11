"""FastAPI application for car insurance rating."""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from .clients import VINClient, RecordClient, LocationClient
from .rating import calculate_premium
from .utils import ExternalAPIError, logger

app = FastAPI()


class Applicant(BaseModel):
    dob: str
    license_years: int = Field(ge=0)
    claims_last_5_years: int = Field(ge=0)


class Vehicle(BaseModel):
    vin: str


class Location(BaseModel):
    postal_code: str


class QuoteRequest(BaseModel):
    applicant: Applicant
    vehicle: Vehicle
    location: Location


# Dependency providers

def get_vin_client() -> VINClient:
    return VINClient()


def get_record_client() -> RecordClient:
    return RecordClient()


def get_location_client() -> LocationClient:
    return LocationClient()


@app.post("/quote")
def quote(
    data: QuoteRequest,
    vin_client: VINClient = Depends(get_vin_client),
    record_client: RecordClient = Depends(get_record_client),
    location_client: LocationClient = Depends(get_location_client),
):
    logger.info("Received quote request")
    try:
        vin_data = vin_client.decode(data.vehicle.vin)
        record_data = record_client.check_history(
            data.applicant.license_years, data.applicant.claims_last_5_years
        )
        location_data = location_client.risk_for_postal(data.location.postal_code)
    except ExternalAPIError as exc:
        logger.error("External API failure: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc))

    result = calculate_premium(
        dob=data.applicant.dob,
        license_years=data.applicant.license_years,
        claims_last_5_years=data.applicant.claims_last_5_years,
        safety_rating=float(vin_data.get("safety_rating", 3)),
        accident_rate=float(location_data.get("accident_rate", 0)),
    )
    return result
