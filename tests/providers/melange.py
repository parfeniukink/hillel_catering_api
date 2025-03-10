from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import uuid
import asyncio
import httpx

app = FastAPI()
orders: dict[str, dict] = {}


class OrderItem(BaseModel):
    dish: str
    quantity: int


class OrderRequest(BaseModel):
    order: list[OrderItem]


STATUS_STAGES = ["not_started", "cooking", "cooked", "done"]

# note: this is configurable on their side
WEBHOOK_URL = "http://127.0.0.1:8000/hooks/melange"


async def update_order_status(order_id: str):
    for status in STATUS_STAGES:
        await asyncio.sleep(10)  # Simulate cooking time
        orders[order_id]["status"] = status

        # send the web api call...
        async with httpx.AsyncClient() as client:
            await client.post(
                url=WEBHOOK_URL, data={"order": {"id": order_id, "status": status}}
            )


@app.post("/")
def make_order(order: OrderRequest, background_tasks: BackgroundTasks):
    order_id = str(uuid.uuid4())
    orders[order_id] = {"status": "not_started"}  # skip adding order instance
    background_tasks.add_task(update_order_status, order_id)

    return {"order_id": order_id}


@app.get("/order/{order_id}")
def get_order_status(order_id: str):
    return orders.get(order_id, {"error": "Order not found"})
