"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import operator
from django.contrib import admin
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest
from django.urls import path
from food.views import import_dishes
from django.views.decorators.csrf import csrf_exempt

from dataclasses import dataclass, asdict


@dataclass
class Dish:
    id: int
    name: str
    price: int
    restaurant: int


@dataclass
class Basket:
    id: int


@dataclass
class BasketItem:
    id: int


storage = {
    "dishes": [
        Dish(id=1, name="salad", price=100, restaurant=1),
        Dish(id=2, name="pizza", price=200, restaurant=2),
        Dish(id=3, name="juice", price=300, restaurant=1),
    ],
    "baskets": [
        # BasketCreateRequestBody(id=1),
    ],
    "basket_items": [
        # BasketItem(id=1, basket_id=1, dish_id=1, quantity=2),
        # BasketItem(id=2, basket_id=1, dish_id=3, quantity=1),
    ],
}


@csrf_exempt
def basket_create(request: WSGIRequest):
    if request.method != "POST":
        raise ValueError(f"Method {request.method} is not allowed on this resource")
    else:
        try:
            last_basket: Basket = sorted(
                storage["baskets"], key=operator.attrgetter("id")
            )[-1]
        except IndexError:
            last_id = 0
        else:
            last_id = last_basket.id

        instance = Basket(id=last_id + 1)
        storage["baskets"].append(instance)

        print(storage["baskets"])
        return JsonResponse(asdict(instance))


urlpatterns = [
    # USERS MANAGEMENT
    # ==================
    path("admin/", admin.site.urls),
    path("import-dishes/", import_dishes),
    # path("users/", user_create_retrieve),  # GET to retrieve user, POST to create user
    # path(
    #     "users/<id:int>", user_update_delete
    # ),  # PUT to updaste user, DELETE to remove user
    # path("users/password/forgot", password_forgot),  # POST to generate temp UUID key
    # path(
    #     "users/passwordt/change", password_change
    # ),  # POST, receive key and new password
    # AUTH
    # ==================
    # path("auth/token", access_token),  # POST
    # BASKET & ORDERS
    # ==================
    path("basket/", basket_create),  # POST  -> return ID
    # path("basket/<id:int>", basket_retrieve),  # GET to see all details
    # path(
    #     "basket/<id:int>/dishes/<id:int>", basket_dish_add_update_delete
    # ),  # PUT (change quantity), DELETE, POST (add dish)
    # path("basket/<id:int>/order", order_from_basket),  # POST -> [Order] with ID
    # path(
    #     "orders/<id:int>", order_details
    # ),  # GET (owner, support), PUT (only by SUPPORT)
]
