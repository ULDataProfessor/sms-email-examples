"""FastAPI application entry point."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from . import design, payment, production, shipping, report
from .config import logger
from .utils import DesignError, PaymentError, ProductionError, ShippingError

app = FastAPI(title="T-Shirt Ecommerce Store")

class Address(BaseModel):
    line1: str
    city: str
    postal_code: str
    country: str

class Customer(BaseModel):
    name: str
    email: EmailStr
    address: Address

class Tshirt(BaseModel):
    size: str
    color: str

class OrderRequest(BaseModel):
    customer: Customer
    design_prompt: str
    tshirt: Tshirt
    payment_token: str

@app.post("/order")
def create_order(order: OrderRequest):
    try:
        design_url = design.generate_design(order.design_prompt)
        charge_id = payment.process_payment(order.payment_token)
        production_id, _ = production.create_order(order.customer.dict(), order.tshirt.dict(), design_url)
        tracking_url = shipping.wait_for_tracking(production_id)
        report.init_db()
        order_id = report.save_order(order.customer.dict(), design_url, charge_id, production_id, tracking_url)
        return {
            "order_id": order_id,
            "design_url": design_url,
            "charge_id": charge_id,
            "production_id": production_id,
            "tracking_url": tracking_url,
        }
    except (DesignError, PaymentError, ProductionError, ShippingError) as exc:
        logger.error("Order failed: %s", exc)
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Internal server error")
