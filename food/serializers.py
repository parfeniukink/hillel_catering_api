from rest_framework import serializers

from .models import Dish, Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = Dish
        fields = "__all__"


class DishOrderSerializer(serializers.Serializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=20)


class OrderSerializer(serializers.Serializer):
    food = DishOrderSerializer(many=True)
    total = serializers.IntegerField(min_value=1, read_only=True)
    delivery = serializers.CharField(read_only=True)
    # status = serializers.CharField(read_only=True)


# alternative
# class OrderResponseSerializer(OrderCreateCreateRequestBodySerializer):
#     status = serializers.CharField()


"""
{
    'food': [
        {
            'dish': 1,
            'quantity': 2
        },
    ]
}
"""
