# Summer Photo Postcards

This example shows an end-to-end FastAPI service that turns uploaded photos into
stylized postcards. Images are sent to an AI art API, printed via a
print-on-demand service, charged through Stripe, stored in SQLite and confirmed
by email.

## Environment Setup

Create a `.env` file based on `.env.example` and provide credentials for:

- MidJourney or Stable Diffusion
- Printful/Printify
- Stripe
- SMTP or SendGrid
- Database path

Install requirements and run the API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Placing an Order

Example `curl` request using HTTPie-style syntax:

```bash
http -f POST http://localhost:8000/order \
  name='Alice Smith' \
  email='alice@example.com' \
  line1='123 Main St' city=Lethbridge postal_code=T1K0A1 country=CA \
  style_prompt='vibrant summer watercolor seaside scene' \
  quantity:=20 payment_token='tok_test' \
  photo@./beach.jpg
```

Successful responses include the print order ID and estimated ship date.

## Viewing Logs and Orders

Logs are written to `postcard.log` with rotation. View saved orders using the
SQLite database defined by `DB_PATH`:

```bash
sqlite3 orders.db 'SELECT * FROM orders;'
```
