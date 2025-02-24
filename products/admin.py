from django.contrib import admin
from django.http.response import HttpResponseRedirect
from .models import Restaurant,Order,DishOrderItem,Dish


class DishInline(admin.TabularInline):
    model = Dish
    extra = 5


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name','address',)
    search_fields = ('name',)
    inlines = [DishInline]


def import_csv(self, request, queryset):
    print("testing import CSV custom action")
    return HttpResponseRedirect("/import-dishes")


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','get_restaurant_name')
    search_fields = ('name',)
    list_filter = ("name", "restaurant")
    actions = ["import_csv"]

    def get_restaurant_name(self, obj):
        return obj.restaurant.name
    get_restaurant_name.short_description = 'Ресторан'


# admin.site.register(DishOrderItem)
class DishOrderItemInline(admin.TabularInline):
    model = DishOrderItem


@admin.register(Order)
class DishesOrderAdmin(admin.ModelAdmin):
    inlines = (DishOrderItemInline,)



admin.site.add_action(import_csv)


# @admin.register(DishOrderItem)
# class DishOrderItemAdmin(admin.ModelAdmin):
#     list_display = ('get_dish_order_id','get_dish_name', 'quantity')
#     search_fields = ('dish__name',)
#
#     def get_dish_name(self, obj):
#         return obj.dish.name
#     get_dish_name.short_description = 'Ястие'
#
#     def get_dish_order_id(self, obj):
#         return obj.dish_order.external_order_id
#     get_dish_order_id.short_description = 'Номер Заказа'




# @admin.register(DishesOrder)
# class DishesOrderAdmin(admin.ModelAdmin):
#     list_display = ('get_user', 'external_order_id')
#
#     def get_user(self, obj):
#         return obj.user.username
#
#     get_user.short_description = 'Клиент'
#
#
#
# @admin.register(Restaurant)
# class RestaurantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'address')
#     search_fields = ('name',)