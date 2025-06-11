"""Premium calculation helpers."""

from __future__ import annotations

from datetime import date, datetime

from .config import BASE_RATE


def age_factor(dob: str) -> float:
    """Calculate a simple age factor from a YYYY-MM-DD date string."""
    birth = datetime.strptime(dob, "%Y-%m-%d").date()
    years = (date.today() - birth).days / 365.25
    if years < 25:
        return 1.5
    if years < 35:
        return 1.2
    if years < 60:
        return 1.0
    return 1.3


def history_factor(claims: int) -> float:
    return 1.0 + 0.1 * claims


def vehicle_factor(safety_rating: float) -> float:
    return 1.0 - safety_rating / 5.0


def location_factor(accident_rate: float) -> float:
    return 1.0 + accident_rate


def calculate_premium(
    dob: str,
    license_years: int,
    claims_last_5_years: int,
    safety_rating: float,
    accident_rate: float,
) -> dict:
    af = age_factor(dob)
    hf = history_factor(claims_last_5_years)
    vf = vehicle_factor(safety_rating)
    lf = location_factor(accident_rate)
    premium = BASE_RATE * af * hf * vf * lf
    return {
        "breakdown": {
            "base_rate": BASE_RATE,
            "age_factor": af,
            "history_factor": hf,
            "vehicle_factor": vf,
            "location_factor": lf,
        },
        "final_premium": round(premium, 2),
    }
