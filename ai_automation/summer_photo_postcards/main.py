"""FastAPI entrypoint for the postcard service."""

import tempfile
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

from .config import logger
from .design import generate_art
from .print import create_postcard_order
from .payment import charge_customer
from .report import init_db, save_order
from .notifier import send_confirmation
from .utils import DesignError, PrintError, PaymentError, NotificationError

app = FastAPI(title="Summer Photo Postcards")

init_db()

@app.post("/order")
async def create_order(
    name: str = Form(...),
    email: str = Form(...),
    line1: str = Form(...),
    city: str = Form(...),
    postal_code: str = Form(...),
    country: str = Form(...),
    style_prompt: str = Form(...),
    quantity: int = Form(...),
    payment_token: str = Form(...),
    photo: UploadFile = File(...),
):
    customer = {
        "name": name,
        "email": email,
        "address": {
            "line1": line1,
            "city": city,
            "postal_code": postal_code,
            "country": country,
        },
    }

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await photo.read())
        photo_path = Path(tmp.name)
        design_url, image_bytes = generate_art(photo_path, style_prompt)
    except DesignError as exc:
        return JSONResponse(status_code=502, content={"error": str(exc)})
    finally:
        photo_path.unlink(missing_ok=True)

    try:
        print_info = create_postcard_order(design_url, quantity, customer)
    except PrintError as exc:
        return JSONResponse(status_code=502, content={"error": str(exc)})

    try:
        charge_id = charge_customer(payment_token, quantity)
    except PaymentError as exc:
        # cancel print order in real scenario
        return JSONResponse(status_code=402, content={"error": str(exc)})

    order_record: Dict[str, str] = {
        "customer_name": name,
        "customer_email": email,
        "address": f"{line1}, {city}, {postal_code}, {country}",
        "design_url": design_url,
        "print_order_id": print_info["order_id"],
        "charge_id": charge_id,
        "status": "processing",
    }
    save_order(order_record)

    try:
        send_confirmation(order_record)
    except NotificationError:
        pass  # already logged

    return {
        "order_id": print_info["order_id"],
        "ship_date": print_info["ship_date"],
    }
