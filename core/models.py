from django.db import models


class User(models.Model):
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)


class Dish(models.Model):
    name = models.CharField(max_length=50)

    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)


class Order(models.Model):
    external_order_id = models.CharField(max_length=255)

    user = models.ForeignKey("User", on_delete=models.CASCADE)


class DishOrder(models.Model):
    # class Meta:
    #     db_table = "custom_table_name"

    quantity = models.SmallIntegerField()

    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE)


class DeliveryOrder(models.Model):
    provider = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    addresses = models.TextField()
    external_order_id = models.CharField(max_length=255)

    order = models.ForeignKey("Order", on_delete=models.CASCADE)
