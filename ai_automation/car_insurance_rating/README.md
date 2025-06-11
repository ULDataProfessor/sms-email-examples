# Car Insurance Rating API

This example demonstrates a minimal car insurance rating service built with **FastAPI**. The `/quote` endpoint accepts basic applicant, vehicle and location data then calls several external services to calculate a premium.

## Files

- `app.py` – FastAPI application with the `/quote` route
- `clients/` – Simple HTTP clients for external APIs
- `rating.py` – Functions to convert API responses into rating factors and compute the premium
- `config.py` – Loads environment variables from `.env`
- `utils.py` – Logging configuration and custom exceptions
- `requirements.txt` – Required Python packages
- `.env.example` – Template for API keys and `BASE_RATE`

## Endpoint

```
POST /quote
Content-Type: application/json
{
  "applicant": {
    "dob": "YYYY-MM-DD",
    "license_years": 5,
    "claims_last_5_years": 1
  },
  "vehicle": { "vin": "1HGCM82633A004352" },
  "location": { "postal_code": "T1K0A1" }
}
```

Sample response:

```
{
  "breakdown": {
    "base_rate": 500,
    "age_factor": 1.2,
    "history_factor": 1.1,
    "vehicle_factor": 0.8,
    "location_factor": 1.3
  },
  "final_premium": 686
}
```

## External APIs

The service expects three external APIs:

1. **VIN Decoder API** – returns `make`, `model`, `year` and `safety_rating` for a VIN.
2. **Driving Record API** – verifies prior claims or infractions.
3. **Location Risk API** – returns `accident_rate` for a postal code.

Provide your credentials in a `.env` file (see `.env.example`).

## Rating Formula

```
final_premium = BASE_RATE × age_factor × history_factor × vehicle_factor × location_factor
```

- `age_factor` – derived from the applicant's age
- `history_factor` – based on number of claims in the last five years
- `vehicle_factor` – `1 - (safety_rating / 5)`
- `location_factor` – normalised accident rate from the location service

Adjust `BASE_RATE` or modify the factor formulas in `rating.py` as needed.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys and `BASE_RATE`.
3. Run the server:
   ```bash
   uvicorn app:app --reload
   ```
4. Test with `curl` or Postman using the JSON structure shown above.
