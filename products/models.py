from django.db import models
from django.conf import settings


class Restaurant(models.Model):
    """ Restaurant model"""
    class Meta:
        db_table = 'restaurants'
        verbose_name_plural = 'Ресторан'

    name = models.CharField(max_length=100, blank=False, verbose_name= "Название")
    address = models.CharField(max_length=255, blank=False, verbose_name= "Адрес")

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name} {self.address}"


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

    def __str__(self) -> str:
        return f"{self.name} {self.price}  ({self.restaurant})"



class Order(models.Model):
    """
    This might represent one "order" of dishes from the user,
    sometimes called the 'cart' or 'basket' before finalization.
    """
    class Meta:
        db_table = 'orders'
        verbose_name_plural = 'Накладная заказа'

    status = models.CharField(max_length=20)
    provider = models.CharField(max_length=20, null=True, blank=True)
    eta = models.DateField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dish_orders',
        blank=False
    )
    # external_order_id = models.CharField(max_length=100,unique=True, verbose_name= "Номер Заказа")

    def __str__(self):
        return f"{self.pk} {self.status} for {self.user.email}"


class DishOrderItem(models.Model):
    """
    The instance of that class defines a DISH item that is related
    to an ORDER, that user has made.

     NOTES
    --------

    do we need user in relations?
    NOT! because we have it in the ``Order``
    """

    class Meta:
        db_table = 'dish_order_items'
        verbose_name_plural = 'Наименования заказа'


    # dish_order = models.ForeignKey(
    #     Order,
    #     on_delete=models.CASCADE,
    #     related_name='order_dishes',
    #     blank=False
    # )
    quantity = models.PositiveIntegerField(default=1, blank=False, verbose_name="Количество")
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, blank=False)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name='items')


    def __str__(self) -> str:
        return f"[{self.order.pk}] {self.dish.name}: {self.quantity}"



