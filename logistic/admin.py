from django.contrib import admin
from .models import DeliveryDishesOrder




@admin.register(DeliveryDishesOrder)
class DeliveryDishesOrderAdmin(admin.ModelAdmin):
    list_display = ('external_order_id','provider','status','addresses','get_dish_order')
    search_fields = ('provider', 'status')

    def get_dish_order(self, obj):
        return obj.dish_order

    get_dish_order.short_description = 'Информация'
