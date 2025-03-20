import enum
from dataclasses import asdict, dataclass

import httpx
from django.conf import settings


class OrderStatus(enum.StrEnum):
    NOT_STARTED = "not started"
    COOKING = "cooking"
    COOKED = "cooked"
    FINISHED = "finished"


@dataclass
class OrderItem:
    dish: str
    quantity: int


@dataclass
class OrderRequestBody:
    order: list[OrderItem]


@dataclass
class OrderResponse:
    id: str
    status: OrderStatus


class Provider:
    @classmethod
    def create_order(cls, order: OrderRequestBody):
        response: httpx.Response = httpx.post(
            settings.BUENO_BASE_URL, json=asdict(order)
        )
        response.raise_for_status()

        return OrderResponse(**response.json())

    @classmethod
    def get_order(cls, order_id: str):
        response: httpx.Response = httpx.get(f"{settings.BUENO_BASE_URL}/{order_id}")
        response.raise_for_status()

        return OrderResponse(**response.json())
