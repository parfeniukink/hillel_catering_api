from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status, viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Dish, DishOrderItem, Order
from .serializers import DishSerializer, OrderCreateSerializer
from .enums import OrderStatus


class FoodAPIViewSet(viewsets.GenericViewSet):
    # HTTP GET /food/dishes
    @action(methods=["get"], detail=False)
    def dishes(self, request):
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)

        return Response(data=serializer.data)

    # HTTP POST /food/orders
    @action(methods=["post"], detail=False)
    def orders(self, request: WSGIRequest):
        """create new order for food.

        HTTP REQUEST EXAMPLE
        {
            "food": {
                1: 3  // id: quantity
                2: 1  // id: quantity
            },
            "eta": TIMESTAMP
        }

        WORKFLOW
        1. validate the input
        2. create ``
        """

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not isinstance(serializer.validated_data, dict):
            raise ValueError(...)

        # alternatives
        # -------------
        # assert isinstance(serializer.validated_data, dict)

        # from typing import cast
        # response = cast(dict, serializer.validated_data) | {}

        # ACTIVE RECORD
        # =======================
        # order = Order(status=OrderStatus.NOT_STARTED, provider=None)
        # order.save()

        # ORM
        # ======================
        order = Order.objects.create(
            status=OrderStatus.NOT_STARTED,
            user=request.user,
            eta=serializer.validated_data["eta"],
        )
        print(f"New Food Order is created: {order.pk}.\nETA: {order.eta}")

        try:
            dishes_order = serializer.validated_data["food"]
        except KeyError as error:
            raise ValueError("Food order is not properly built")

        for dish_order in dishes_order:
            instance = DishOrderItem.objects.create(
                dish=dish_order["dish"], quantity=dish_order["quantity"], order=order
            )
            print(f"New Dish Order Item is created: {instance.pk}")

        return Response(
            data={
                "id": order.pk,
                "status": order.status,
                "eta": order.eta,
                "total": 9999,
            },
            status=status.HTTP_201_CREATED,
        )


router = routers.DefaultRouter()
router.register(
    prefix="food",
    viewset=FoodAPIViewSet,
    basename="food",
)
