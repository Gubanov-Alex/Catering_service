from django.contrib import admin
from django.http.response import HttpResponseRedirect

from .models import Dish, DishOrderItem, Order, Restaurant

admin.site.register(Restaurant)


def import_csv(self, request, queryset):
    print("testing import CSV custom action")
    return HttpResponseRedirect("/import-dishes")


# admin.site.register(Dish)
@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "restaurant")
    search_fields = ("name",)
    list_filter = ("name", "restaurant")
    actionss = ["import_csv"]


# admin.site.register(DishOrderItem)
class DishOrderItemInline(admin.TabularInline):
    model = DishOrderItem


@admin.register(Order)
class DishesOrderAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id", "status","external_order_id_melange", "external_order_id_bueno")
    inlines = (DishOrderItemInline,)


admin.site.add_action(import_csv)