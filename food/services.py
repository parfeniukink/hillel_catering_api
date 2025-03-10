from datetime import datetime, date, time
import uuid
from django.conf import settings

from celery.result import AsyncResult

from shared.cache import CacheService
from .models import Order, DishOrderItem
from .enums import Provider
from config import celery_app


# note: TASK: how to change the status in order to start the delivery?
#       SOLUTION: run the background task to track it all the time
#       SOLUTION: run this checker in each provider. If it can see that
#                 all statuses are finished - run the delivery task then.


def bueno_webhook_handler(): ...


@celery_app.task
def melange_get_status_in_loop(order_key: str): ...


# todo: uncomment
# @celery_app.task
def _schedule_order(order: Order):
    """Start processing restaurant order.

    0. Call the Restaurant API but first create them...
    1. Depending on the restaurant provide the order to each one
    """

    melange_order: list[DishOrderItem] = []
    bueno_order: list[DishOrderItem] = []

    for item in order.items.all():
        if item.provider == Provider.BUENO:
            bueno_order.append(item)
        elif item.provider == Provider.MELANGE:
            melange_order.append(item)
        else:
            raise ValueError("Can NOT process order")

    # note: in case with BUENO we have webhooks, when with MELANGE we have to provide background processing on our side
    # todo: this about how better to solve that task. where collect order statuses??

    # note: solution
    # todo: save temporary key of Restaurants gathered order
    order_key = uuid.uuid4()

    cache = CacheService()
    cache.set(namespace="restaurants_order", key=str(order_key), instance={})

    melange_get_status_in_loop.delay(order_key)


def schedule_order(order: Order) -> None:
    """Depending on `eta` process order immediately or in specified time"""

    assert type(order.eta) is date

    # todo: remove
    _schedule_order(order)
    return None

    # 2025-03-06  -> 2025-03-06-00:00:00 UTC
    if order.eta == date.today():
        print(f"The order will be started processing now")
        return _schedule_order.delay(order)
    else:
        # 3:00AM -> create the order to the RESTAURANT API
        eta = datetime.combine(order.eta, time(hour=3))
        print(f"The order will be started processing {eta}")
        return _schedule_order.apply_async(args=(order,), eta=eta)
