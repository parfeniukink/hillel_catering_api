from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, time
from time import sleep
from typing import Any

from config import celery_app
from shared.cache import CacheService

from .enums import OrderStatus, Restaurant
from .models import DishOrderItem, Order
from .providers import bueno, melange, uklon


# note: move to dataclasses since Celery does not serialize
#       class instances (https://docs.celeryq.dev/en/stable/userguide/calling.html#serializers)
@dataclass
class OrderInCache:
    restaurants: dict = field(default_factory=defaultdict)
    location: tuple[float, float] | None = None

    def append(self, restaurant: str, item: DishOrderItem):
        if not self.restaurants.get(restaurant):
            self.restaurants[restaurant] = {
                "external_id": None,
                "address": item.dish.restaurant.address,
                "status": "not started",
                "dishes": [
                    {
                        "dish": item.dish.name,
                        "quantity": item.quantity,
                    }
                ],
            }
        else:
            self.restaurants[restaurant]["dishes"].append(
                {
                    "dish": item.dish.name,
                    "quantity": item.quantity,
                }
            )


def validate_all_orders_cooked(order: OrderInCache) -> bool:
    flag = False

    for rest, _order in order.restaurants.items():
        if rest == Restaurant.MELANGE:
            if _order["status"] in (
                melange.OrderStatus.COOKED,
                melange.OrderStatus.FINISHED,
            ):
                flag = True
                break
        elif rest == Restaurant.BUENO:
            if _order["status"] in [
                bueno.OrderStatus.COOKED,
                bueno.OrderStatus.FINISHED,
            ]:
                flag = True
                break

    # note: this is not a part of a validation function!
    # todo: remove, since moved to concrete provider implementation
    # todo: implement in melange_order_processing and bueno_order_processing
    # if flag is True:
    #     Order.update_from_restaurant_status(
    #         id_=order.internal_order_id, status="finished"
    #     )

    return flag


# ==================================================
# RESTAURANTS
# ==================================================
@celery_app.task
def melange_order_processing(internal_order_id: int):
    cache = CacheService()
    provider = melange.Provider()

    # get item from the cache instead of having it as a constant variable
    cooked = False
    while not cooked:
        sleep(1)
        cached_order: OrderInCache = OrderInCache(
            **cache.get(namespace="orders", key=internal_order_id)
        )
        melange_order: dict[str, Any] = cached_order.restaurants[Restaurant.MELANGE]

        print(f"MELANGE ORDER STATUS: {melange_order['status']}")
        if melange_order["status"] == "not started":
            # create or get the order depending on the cache
            if not melange_order.get("external_id"):
                response: melange.OrderResponse = provider.create_order(
                    melange.OrderRequestBody(
                        order=[
                            melange.OrderItem(**item)
                            for item in melange_order["dishes"]
                        ]
                    )
                )
                # update cache
                cached_order.restaurants[Restaurant.MELANGE][
                    "external_id"
                ] = response.id
                cache.set(
                    namespace="orders",
                    key=internal_order_id,
                    instance=asdict(cached_order),
                )
                # note: skip database update, since "not started" is default value
            else:
                external_order_id: str = melange_order["external_id"]
                response: melange.OrderResponse = provider.get_order(
                    order_id=external_order_id
                )

                if melange_order["status"] != response.status:  # status changed
                    # update cache
                    cached_order.restaurants[Restaurant.MELANGE][
                        "status"
                    ] = response.status
                    cache.set(
                        namespace="orders",
                        key=internal_order_id,
                        instance=asdict(cached_order),
                    )
                sleep(1)
        elif melange_order["status"] == "cooking":
            external_order_id = melange_order["external_id"]
            response = provider.get_order(order_id=external_order_id)

            if melange_order["status"] != response.status:  # if status changed
                cached_order.restaurants[Restaurant.MELANGE]["status"] = response.status
                cache.set(
                    namespace="orders",
                    key=internal_order_id,
                    instance=asdict(cached_order),
                )

            sleep(3)
        elif melange_order["status"] in ["cooked", "finished"]:
            cooked = True
            cached_order.restaurants[Restaurant.MELANGE]["status"] = "cooked"
            cache.set(
                namespace="orders",
                key=internal_order_id,
                instance=asdict(cached_order),
            )
            if validate_all_orders_cooked(cached_order):
                # note: instead of doing this through the provider mapping
                Order.objects.filter(id=internal_order_id).update(
                    status=OrderStatus.COOKED
                )
                print("🍲😋 UPDATED ORDER IN DATABASE TO ``COOKED``")


@celery_app.task
def bueno_order_processing(internal_order_id: int):
    provider = bueno.Provider()

    # response: bueno.OrderResponse = provider.create_order(
    #     bueno.OrderRequestBody(
    #         order=[
    #             bueno.OrderItem(**item)
    #             for item in cached_order.restaurants[Restaurant.BUENO]["dishes"]
    #         ]
    #     )
    # )
    # # update cache representation
    # cached_order.restaurants[Restaurant.BUENO]["external_id"] = response.id

    print("BUENO ORDER PROCESSED")
    return


# ==================================================
# DELIVERY
# ==================================================
def _delivery_order_task(internal_order_id: int):
    """Using random provider - start processing delivery orders."""

    # todo: select provider randomly
    provider = uklon.Provider()
    cache = CacheService()
    addresses: list[str] = []
    comments: list[str] = []
    order_in_cache = OrderInCache(**cache.get("orders", internal_order_id))

    # todo: select restaurants by nearest location
    for restaurant in order_in_cache.restaurants.values():
        addresses.append(restaurant["address"])
        comments.append(f"ORDER: {restaurant['external_id']}")

    _response: uklon.OrderResponse = provider.create_order(
        uklon.OrderRequestBody(addresses=addresses, comments=comments)
    )

    current_status = uklon.OrderStatus.NOT_STARTED
    while current_status != uklon.OrderStatus.DELIVERED:
        response: uklon.OrderResponse = provider.get_order(_response.id)
        current_status = response.status
        print(f"🚙 DRIVER LOCATION: {response.location}")
        order_in_cache.location = response.location
        cache.set("orders", internal_order_id, asdict(order_in_cache))

        if current_status == response.status:
            sleep(1)
            continue

        current_status = response.status  # DELIVERY, DELIVERED
        print(f"\tCHANGED DELIVERY STATUS TO: {current_status.upper()}")

    Order.objects.filter(id=internal_order_id).update(status=OrderStatus.DELIVERED)


@celery_app.task
def delivery_order(internal_order_id: int):
    """Using random provider - start processing delivery orders."""

    print(f"🚚 DELIVERY PROCESSING STARTED")

    cache = CacheService()
    # checking orders in background
    # note: always reaches ``break`` when we comment Celery
    while True:
        order_in_cache: OrderInCache = OrderInCache(
            **cache.get(
                namespace="orders",
                key=internal_order_id,
            )
        )

        if validate_all_orders_cooked(order_in_cache):
            break
        else:
            sleep(3)
            print(f"WAITING FOR ORDERS TO BE COOKED")
            print(order_in_cache.restaurants["melange"]["status"])

    _delivery_order_task(internal_order_id)

    print(f"🚚 DELIVERED all the orders...")


# ==================================================
# ORDERS
# ==================================================
@celery_app.task
def _schedule_order(order: Order):
    """Start processing restaurants orders.

    WORKFLOW:
    1. create temporary orders
    2. call restaurants APIs
    3. process orders in background


    NOTES
    - [order: Order] includes all restaurantes
    - each provider task will run ``validate_external_orders_ready(order)``
        and the last one will update the status to ``DRIVER_LOOKUP``
    """

    print("#" * 30)
    print("# 🤖 STARTED WORKING PROCESSING CLIENT ORDER")
    print("#" * 30)

    order_in_cache = OrderInCache()

    for item in order.items.all():
        if (restaurant := item.dish.restaurant.name.lower()) == Restaurant.MELANGE:
            order_in_cache.append(restaurant, item)
        elif item.dish.restaurant.name.lower() == Restaurant.BUENO:
            order_in_cache.append(restaurant, item)
        else:
            raise ValueError(
                f"Can not create order for {item.dish.restaurant.name} restaurant"
            )

    # initialize data in cache
    cache = CacheService()
    cache.set(namespace="orders", key=order.pk, instance=asdict(order_in_cache))

    # add restaurants and delivery processing
    melange_order_processing.delay(order.pk)
    delivery_order.delay(order.pk)

    # note:won't change the value due to the webhook is not finished bueno_order_processing.delay(order_in_cache)


def schedule_order(order: Order):
    """Add the task to the queue for the future processing."""

    assert type(order.eta) is date

    # 2025-03-06  -> 2025-03-06-00:00:00 UTC
    if order.eta == date.today():
        print(f"The order will be started processing now")
        return _schedule_order.delay(order)
    else:
        # ETA: 3:00AM will be sent to restaurant APIs
        eta = datetime.combine(order.eta, time(hour=3))
        print(f"The order will be started processing {eta}")
        return _schedule_order.apply_async(args=(order,), eta=eta)
