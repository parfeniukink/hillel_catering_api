from django.contrib import admin
from .models import Dish, Restaurant, DishesOrder, DishOrderItem

admin.site.register(Restaurant)


# admin.site.register(Dish)
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "restaurant")
    search_fields = ("name",)
    list_filter = ("name", "restaurant")


# admin.site.register(DishOrderItem)
class DishOrderItemInline(admin.TabularInline):
    model = DishOrderItem


@admin.register(DishesOrder)
class DishesOrderAdmin(admin.ModelAdmin):
    inlines = (DishOrderItemInline,)
