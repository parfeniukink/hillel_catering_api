import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from shared.cache import CacheService

from .enums import OrderStatus
from .models import Dish, DishOrderItem, Order
from .serializers import DishSerializer, OrderCreateSerializer
from .services import schedule_order


@csrf_exempt
def bueno_webhook(request):
    data: dict = json.loads(json.dumps(request.POST))
    print(
        "getting the bueno order from the cache and update the database instance"
    )

    return JsonResponse({"message": "ok"})


class FoodAPIViewSet(viewsets.GenericViewSet):
    # HTTP GET /food/dishes
    @action(methods=["get"], detail=False, url_path="dishes")
    def dishes(self, request):
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)

        return Response(data=serializer.data)

    # HTTP POST /food/orders
    @action(
        methods=["post"],
        detail=False,
        url_path="orders",
        url_name="create_order",
    )
    def orders(self, request: WSGIRequest):
        """create new order for food.

        HTTP REQUEST EXAMPLE
        {
            "food": {
                1: 3  // id: quantity
                2: 1  // id: quantity
            },
            "eta": DATE
        }

        WORKFLOW
        1. validate the input
        2. create ``
        """

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not isinstance(serializer.validated_data, dict):
            raise ValueError(...)

        order: Order = Order.objects.create(
            status=OrderStatus.NOT_STARTED,
            user=request.user,
            eta=serializer.validated_data["eta"],
        )

        try:
            dishes_order = serializer.validated_data["food"]
        except KeyError as error:
            raise ValueError("Food order is not properly built")

        for dish_order in dishes_order:
            instance = DishOrderItem.objects.create(
                dish=dish_order["dish"],
                quantity=dish_order["quantity"],
                order=order,
            )
            print(f"New Dish Order Item is created: {instance.pk}")

        schedule_order(order=order)
        print(f"New Food Order is created: {order.pk}.\nETA: {order.eta}")

        return Response(
            data={
                "id": order.pk,
                "status": order.status,
                "eta": order.eta,
                "total": 9999,
            },
            status=status.HTTP_201_CREATED,
        )

    # HTTP GET /food/orders/ID
    # note: mention that ``detail=True`` will generate <int:pk> for `/food/<...>/orders`
    #       instead of `/food/orders/<...>`
    @action(methods=["get"], detail=False, url_path=r"orders/(?P<id>\d+)")
    def order_retrieve(self, request: WSGIRequest, id=None):
        order: Order = Order.objects.get(id=id)
        order_in_cache = CacheService().get("orders", order.pk)

        # todo: create another serializer for OrderResponse
        return Response(
            data={
                "id": order.pk,
                "status": order.status,
                "eta": order.eta,
                "total": 9999,
                "location": order_in_cache["location"],
            },
            status=status.HTTP_200_OK,
        )


router = routers.DefaultRouter()
router.register(prefix="food", viewset=FoodAPIViewSet, basename="food")
