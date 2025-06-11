# T-Shirt Ecommerce Store

This example demonstrates a simplified end-to-end workflow for a print-on-demand T‑shirt business. The FastAPI service exposes a single `/order` endpoint that accepts a design prompt and payment token and coordinates design generation, payment, production, and shipping.

## Environment Variables
Create a `.env` file based on `.env.example` and set the following keys:

- `MIDJOURNEY_API_URL` – image generation endpoint
- `S3_BUCKET_URL` – storage upload URL
- `STRIPE_API_KEY` – Stripe secret key
- `PRINTFUL_URL` and `PRINTFUL_TOKEN` – print-on-demand API credentials
- `SHIPPING_URL_TEMPLATE` – URL to check order shipping status
- `DB_PATH` – path to SQLite DB (e.g. `orders.db`)
- `TSHIRT_PRICE_CENTS` – price charged in cents

## Running
Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Example Order Request
```bash
curl -X POST http://localhost:8000/order \
  -H "Content-Type: application/json" \
  -d '{"customer": {"name": "Jane Doe", "email": "jane@example.com", "address": {"line1": "123 Main St", "city": "Toronto", "postal_code": "A1A1A1", "country": "CA"}}, "design_prompt": "a minimalist mountain scene in pastel colors", "tshirt": {"size": "L", "color": "white"}, "payment_token": "tok_test"}'
```

## Logs and Orders
Logs are written to `store.log` in this folder. Order records are saved to the SQLite database specified by `DB_PATH`. Use any SQLite browser or the `sqlite3` CLI to inspect the `orders` table.
