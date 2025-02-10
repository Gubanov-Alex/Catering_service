from django.contrib import admin
from .models import Restaurant,DishesOrder,DishOrderItem,Dish





@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price','get_restaurant_name')
    search_fields = ('name',)

    def get_restaurant_name(self, obj):
        return obj.restaurant.name
    get_restaurant_name.short_description = 'Ресторан'


@admin.register(DishOrderItem)
class DishOrderItemAdmin(admin.ModelAdmin):
    list_display = ('get_dish_order_id','get_dish_name', 'quantity')
    search_fields = ('dish__name',)

    def get_dish_name(self, obj):
        return obj.dish.name
    get_dish_name.short_description = 'Ястие'

    def get_dish_order_id(self, obj):
        return obj.dish_order.external_order_id
    get_dish_order_id.short_description = 'Номер Заказа'




@admin.register(DishesOrder)
class DishesOrderAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'external_order_id')

    def get_user(self, obj):
        return obj.user.username

    get_user.short_description = 'Клиент'



@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)