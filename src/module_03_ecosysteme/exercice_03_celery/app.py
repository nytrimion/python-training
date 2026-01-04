"""
FastAPI application with Celery integration.

This is a refactored version of the Module 2 exercise,
replacing BackgroundTasks with Celery for robust email sending.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from .tasks import send_confirmation_email

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Orders API with Celery")


class OrderCreate(BaseModel):
    """Order creation request."""

    product: str
    quantity: int
    customer_email: str


class OrderResponse(BaseModel):
    """Order creation response."""

    order_id: str
    status: str
    message: str
    email_task_id: str | None = None


async def save_order_to_db(_order: OrderCreate) -> str:
    """Simulate saving order to database."""
    await asyncio.sleep(0.1)  # Simulate DB latency
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    logger.info(f"Order {order_id} saved to database")
    return order_id


@app.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderCreate) -> OrderResponse:
    """
    Create a new order and send confirmation email via Celery.

    The email is sent asynchronously by a Celery worker.
    If the email fails, Celery will retry automatically.
    """
    order_id = await save_order_to_db(order)
    email_task = send_confirmation_email.delay(order.customer_email, order_id)

    return OrderResponse(
        order_id=order_id,
        status="success",
        message="Order created successfully",
        email_task_id=email_task.id,
    )


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str) -> dict[str, Any]:
    """
    Check the status of a Celery task.

    This endpoint allows checking if an email was sent successfully.
    """
    from .celery_app import app as celery_app

    result = celery_app.AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": result.status,
    }

    if result.ready():
        if result.successful():
            response["result"] = result.result  # type: ignore[assignment]
        else:
            response["error"] = str(result.result)

    return response
