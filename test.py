import queue
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading


OrderRequestBody = tuple[str, datetime]


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()

    def add_order(self, order: OrderRequestBody):
        self.orders.put(order)
        print(f"ORDER {order[0]} IS SCHEDULED")

    def process_orders(self):
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(False)
            print("...")

            time_to_wait = order[1] - datetime.now()
            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                print(f"{order[0]} SENT TO SHIPPING DEPARTMENT")


def main():
    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread.start()

    # user input
    # A 5
    # B 3
    while True:
        if order_details := input("Enter order details: "):
            data = order_details.split(" ")
            order_name, delay = data[0], int(data[1])
            scheduler.add_order(
                (
                    order_name,
                    datetime.now() + timedelta(seconds=delay),
                )
            )

    # end
    thread.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        raise SystemExit(0)
