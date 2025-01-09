 # CATERING PROJECT

 ```python
import queue
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading

STORAGE = {
    "users": [],
    "dishes": [
        {"id": 1, "name": "pizza", "price": 1099},
        {
            "id": 2,
            "name": "soda",
            "price": 199,
        },
        {
            "id": 3,
            "name": "salad",
            "price": 599,
        },
    ],
    # ...
}


@dataclass
class DishRequest:
    name: str
    amount: str


@dataclass
class OrderRequestBody:
    id: int
    dishes: list[DishRequest]
    delivery_time: datetime
    created_at: datetime

    def __str__(self):
        if self.delivery_time == self.created_at:
            eta = "IMMIDIATLY"
        else:
            eta = f"at {self.delivery_time.strftime("%Y-%m-%d %H:%M")}"

        return f"[{self.id}] ORDER. TOTAL: {len(self.dishes)}. ORDER AT {eta}"


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()

    def add_order(self, order: OrderRequestBody):
        self.orders.put(order)
        print(f"ORDER {order} IS SCHEDULED")

    def process_orders(self):
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get()

            time_to_wait = order.delivery_time - datetime.now()
            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                continue
            else:
                print(f"{order} SENT TO SHIPPING DEPARTMENT")


def main():
    right_now = datetime.now()
    eta = right_now + timedelta(seconds=5)

    # order_request_body = OrderRequestBody(
    #     id=1,
    #     dishes=[
    #         DishRequest(name="pizza", amount="2"),
    #         DishRequest(name="soda", amount="1"),
    #         DishRequest(name="salad", amount="1"),
    #         DishRequest(name="dessert", amount="1"),
    #     ],
    #     created_at=right_now,
    #     delivery_time=eta,
    # )

    # order_request_body_2 = OrderRequestBody(
    #     id=2,
    #     dishes=[
    #         DishRequest(name="pizza", amount="2"),
    #         DishRequest(name="soda", amount="1"),
    #         DishRequest(name="salad", amount="1"),
    #         DishRequest(name="dessert", amount="1"),
    #     ],
    #     created_at=right_now,
    #     delivery_time=right_now,
    # )

    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread.start()

    # user input
    scheduler.add_order(order_request_body)
    scheduler.add_order(order_request_body_2)

    # end
    thread.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)


 ```

# REQUESTS

1. If order is outdated for 2 days - ignore on processing
