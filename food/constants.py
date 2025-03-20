"""
{
    "melange": {
        "not started": "not_started",
        "cooking": "cooking",
        "cooked": "cooked",
        "finished": "DRIVER_LOOKUP",
    },
    "bueno": {
        "not started": "not_started",
        "cooking": "cooking",
        "cooked": "cooked",
        "finished": "DRIVER_LOOKUP",
    },
}
"""

from .enums import OrderStatus, Provider, Restaurant
from .providers import bueno, melange, uklon

EXCLUDE_STATUSES = (
    OrderStatus.DELIVERED,
    OrderStatus.NOT_DELIVERED,
    OrderStatus.CANCELLED,
)


# note: after ``validate_all_external_orders_are_cooked`` is implemented
#       we can start moving from these statuses
RESTAURANT_TO_INTERNAL_STATUSES: dict[Restaurant, dict[str, OrderStatus]] = {
    Restaurant.MELANGE: {
        melange.OrderStatus.NOT_STARTED: OrderStatus.NOT_STARTED,
        melange.OrderStatus.COOKING: OrderStatus.COOKING,
        melange.OrderStatus.COOKED: OrderStatus.COOKED,
        melange.OrderStatus.FINISHED: OrderStatus.DRIVER_LOOKUP,
    },
    Restaurant.BUENO: {
        bueno.OrderStatus.NOT_STARTED: OrderStatus.NOT_STARTED,
        bueno.OrderStatus.COOKING: OrderStatus.COOKING,
        bueno.OrderStatus.COOKED: OrderStatus.COOKED,
        bueno.OrderStatus.FINISHED: OrderStatus.DRIVER_LOOKUP,
    },
}


PROVIDER_TO_INTERNAL_STATUSES: dict[Provider, dict[str, OrderStatus]] = {
    Provider.UKLON: {
        uklon.OrderStatus.NOT_STARTED: OrderStatus.NOT_STARTED,
        uklon.OrderStatus.DELIVERY: OrderStatus.DELIVERY,
        uklon.OrderStatus.DELIVERED: OrderStatus.DELIVERED,
    }
}
