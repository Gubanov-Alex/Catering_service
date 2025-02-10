from django.db import models
from django.conf import settings






class Restaurant(models.Model):
    """ Restaurant model"""
    class Meta:
        db_table = 'restaurants'
        verbose_name_plural = 'Ресторан'

    name = models.CharField(max_length=100, blank=False, verbose_name= "Название")
    address = models.CharField(max_length=255, blank=False, verbose_name= "Адрес")

    def __str__(self):
        return self.name


class Dish(models.Model):
    """ Dish model"""
    class Meta:
        db_table = 'dishes'
        verbose_name_plural = 'Ястие'

    name = models.CharField(max_length=100, verbose_name= "Наименование")
    price = models.IntegerField(verbose_name= "Цена")
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='dishes',
        blank=False,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/placeholder-url/"

class DishesOrder(models.Model):
    """
    This might represent one "order" of dishes from the user,
    sometimes called the 'cart' or 'basket' before finalization.
    """
    class Meta:
        db_table = 'dishes_orders'
        verbose_name_plural = 'Накладная заказа'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dish_orders',
        blank=False
    )
    external_order_id = models.CharField(max_length=100,unique=True, verbose_name= "Номер Заказа")

    def __str__(self):
        return f"Заказ № {self.external_order_id} ; Клиент: {self.user}"


class DishOrderItem(models.Model):
    """
     Intermediate model representing an ordered dish and its quantity.
    """
    class Meta:
        db_table = 'dish_order_items'
        verbose_name_plural = 'Наименования заказа'


    dish_order = models.ForeignKey(
        DishesOrder,
        on_delete=models.CASCADE,
        related_name='order_dishes',
        blank=False
    )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, blank=False)
    quantity = models.PositiveIntegerField(default=1, blank=False, verbose_name= "Количество")

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} ; Заказ №: {self.dish_order.external_order_id}"



