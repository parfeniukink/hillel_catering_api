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

from django.contrib import admin
from django.urls import path
from users.api import router as users_router
from food.api import router as food_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # token_obtain_pair,
)  # noqa


urlpatterns = (
    [
        # USERS MANAGEMENT
        # ==================
        path("admin/", admin.site.urls),
        # ---------------------------------
        # FIRST ITERATION BEFORE APIViewSets
        # using Class-Based-Views
        # path("users/", UserRetrieveCreateAPI.as_view()),
        # path("users/activation/resendActivation", resend_activation_mail),
        # using SimpleRouter
        # won't work
        # path("users/", users_router.urls),
        # ---------------------------------
        # ==================
        # HOMEWORK
        # ==================
        # path("import-dishes/", import_dishes),
        # path(
        #     "users/<id:int>", user_update_delete
        # ),  # PUT to updaste user, DELETE to remove user
        # path("users/password/forgot", password_forgot),  # POST to generate temp UUID key
        # path(
        #     "users/password/change", password_change
        # ),  # POST, receive key and new password
        # AUTHENTICATION
        # ==================
        # path("auth/token/", token_obtain_pair),  # using function
        path("auth/token/", TokenObtainPairView.as_view()),
        # BASKET & ORDERS
        # ==================
        # path("basket/", basket_create),  # POST  -> return ID
        # path("basket/<id:int>", basket_retrieve),  # GET to see all details
        # path(
        #     "basket/<id:int>/dishes/<id:int>", basket_dish_add_update_delete
        # ),  # PUT (change quantity), DELETE, POST (add dish)
        # path("basket/<id:int>/order", order_from_basket),  # POST -> [Order] with ID
        # path(
        #     "orders/<id:int>", order_details
        # ),  # GET (owner, support), PUT (only by SUPPORT)
    ]
    + users_router.urls
    + food_router.urls
)
