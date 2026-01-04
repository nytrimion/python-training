"""
Exercise 03: FastAPI async endpoints and Background Tasks.

This module demonstrates:
- async vs sync endpoints in FastAPI
- BackgroundTasks for fire-and-forget operations
"""

import asyncio
import time
from datetime import datetime
from typing import Any

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

app = FastAPI(title="Async Demo API")


# --- Models ---


class OrderCreate(BaseModel):
    """Request model for creating an order."""

    customer_email: str
    product: str
    quantity: int


class OrderResponse(BaseModel):
    """Response model for order creation."""

    order_id: str
    status: str
    message: str


# --- Simulated services ---


async def save_order_to_db(order: OrderCreate) -> str:
    """Simulate saving an order to database (async I/O)."""
    print(f"[DB] Saving order for {order.customer_email}...")
    await asyncio.sleep(0.1)  # Simulate DB latency
    order_id = f"ORD-{int(time.time() * 1000)}"
    print(f"[DB] Order {order_id} saved")
    return order_id


def send_confirmation_email(email: str, order_id: str) -> None:
    """
    Simulate sending a confirmation email (slow operation).

    Note: This is a SYNC function - it blocks during execution.
    In production, you'd use an async email library or a task queue.
    """
    print(f"[EMAIL] Sending confirmation to {email}...")
    time.sleep(1)  # Simulate slow email sending
    print(f"[EMAIL] Confirmation sent for order {order_id}")


def log_order_analytics(order_id: str, product: str, quantity: int) -> None:
    """Simulate logging analytics (another background operation)."""
    print(f"[ANALYTICS] Logging order {order_id}: {quantity}x {product}")
    time.sleep(0.2)
    print(f"[ANALYTICS] Done logging {order_id}")


# --- Endpoints ---


@app.post("/orders/sync", response_model=OrderResponse)
def create_order_sync(order: OrderCreate) -> OrderResponse:
    """
    Create an order SYNCHRONOUSLY.

    The client waits for everything to complete, including the email.
    Total response time: ~1.3s (DB + email + analytics)
    """
    print(f"\n{'=' * 50}")
    print(f"[SYNC] Request received at {datetime.now():%H:%M:%S}")

    # Save to DB
    order_id = asyncio.run(save_order_to_db(order))

    # Send email (blocking!)
    send_confirmation_email(order.customer_email, order_id)

    # Log analytics (blocking!)
    log_order_analytics(order_id, order.product, order.quantity)

    print(f"[SYNC] Response sent at {datetime.now():%H:%M:%S}")
    return OrderResponse(
        order_id=order_id,
        status="completed",
        message="Order created and confirmation sent",
    )


# TODO(human): Implement create_order_async
# This endpoint should:
# 1. Save the order to DB (await save_order_to_db)
# 2. Add email sending as a background task (background_tasks.add_task)
# 3. Add analytics logging as a background task
# 4. Return immediately with status="processing"
#
# The BackgroundTasks parameter is injected by FastAPI:
#   async def create_order_async(order: OrderCreate, background_tasks: BackgroundTasks)
#
# To add a background task:
#   background_tasks.add_task(function_name, arg1, arg2, ...)
#
# Expected behavior:
# - Response returns in ~0.1s (just DB save)
# - Email and analytics run AFTER the response is sent


@app.post("/orders/async", response_model=OrderResponse)
async def create_order_async(
        order: OrderCreate,
        background_tasks: BackgroundTasks,
) -> OrderResponse:
    """
    Create an order ASYNCHRONOUSLY with background tasks.

    The client gets a response immediately after DB save.
    Email and analytics run in the background.
    Total response time: ~0.1s (just DB)
    """
    print(f"\n{'=' * 50}")
    print(f"[ASYNC] Request received at {datetime.now():%H:%M:%S}")

    # Save to DB (non-blocking)
    order_id = await save_order_to_db(order)

    # Send email (non-blocking)
    background_tasks.add_task(send_confirmation_email, order.customer_email, order_id)

    # Log analytics (non-blocking)
    background_tasks.add_task(
        log_order_analytics, order_id, order.product, order.quantity
    )

    print(f"[ASYNC] Response sent at {datetime.now():%H:%M:%S}")
    return OrderResponse(
        order_id=order_id,
        status="processing",
        message="Order created and confirmation scheduled",
    )


# --- Health check ---


@app.get("/health")
async def health_check() -> dict[str, Any]:
    """Simple health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
