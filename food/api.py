from django.core.handlers.wsgi import WSGIRequest
from rest_framework import routers, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Dish, DishesOrder, Restaurant

# note: to debug settings
# from rest_framework.settings import api_settings


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Dish
        fields = "__all__"


class DishesOrderCreateRequestBodySerializer(serializers.Serializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    quantity = serializers.IntegerField(max_value=20)


class FoodOrderCreateRequestBodySerializer(serializers.Serializer):
    order = DishesOrderCreateRequestBodySerializer(many=True, min_length=1)


class DishesOrderSerializer(DishesOrderCreateRequestBodySerializer):
    """output public data structure."""

    dish = DishSerializer()


class FoodOrderSerializer(serializers.Serializer):
    order = DishesOrderSerializer(many=True, read_only=True)


class FoodViewSet(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False)
    def restaurants(self, request: WSGIRequest):
        """retrieve all the restaurants."""

        insatnces = Restaurant.objects.all()
        serializer = RestaurantSerializer(insatnces, many=True)

        return Response(data=serializer.data)

    @action(methods=["get"], detail=False)
    def dishes(self, request: WSGIRequest):
        """retrieve all the dishes."""

        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)

        return Response(data=serializer.data)

    @action(methods=["get", "post"], detail=False)
    def orders(self, request: WSGIRequest):
        """create a new order for dishes.

        HTTP REQUEST EXAMPLE:
        {
            "dishes_order": {
                1: 3,  // id: quantity
                2: 1
            }
        }


        WORKFLOW:
        1. validate the input
        2. create `food.DishesOrder`


        NOTES:

        HOW ARE WE GONIG TO DEAL WITH MULTIPLE RESTAURANTS?
        let's parse the information and create 2 SEPARATE ORDERS
        for separate restaurants. Then we will check all of them separately.

        why such a solution?
        actually in one day we can combibe (aggregate) those orders into
        a single data structure, called `UserOrder` / etc...
        """

        if request.method == "GET":
            raise NotImplementedError
        else:
            serializer = FoodOrderCreateRequestBodySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            return Response(
                data=FoodOrderSerializer(serializer.validated_data).data,
            )


router = routers.DefaultRouter()
router.register(prefix="food", viewset=FoodViewSet, basename="food")
