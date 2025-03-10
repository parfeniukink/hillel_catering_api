import random
import asyncio
import uuid
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

STORAGE: dict[str, dict] = {}
ORDER_STATUSES = ("not started", "cooking", "cooked", "finished")


app = FastAPI()


class OrderItem(BaseModel):
    dish: str
    quantity: int


class OrderRequestBody(BaseModel):
    order: list[OrderItem]


# business model of the application
async def update_order_status(order_id: str):
    for status in ORDER_STATUSES[1:]:
        await asyncio.sleep(random.randint(5, 10))
        STORAGE[order_id]["status"] = status
        print(f"MELANGE [{order_id}] --> {status}")


@app.post("/api/orders")
async def make_order(order: OrderRequestBody, background_tasks: BackgroundTasks):
    print(order)
    order_id = str(uuid.uuid4())
    STORAGE[order_id] = {"status": "not_started"}
    background_tasks.add_task(update_order_status, order_id)
    return {"id": order_id, "status": "not_started"}


@app.get("/api/orders/{order_id}")
async def retrieve_order(order_id: str):
    return STORAGE.get(order_id, {"error": "No such order"})
