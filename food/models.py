from typing import Literal

from django.conf import settings
from django.db import models

from .constants import RESTAURANT_TO_INTERNAL_STATUSES
from .enums import OrderStatus
from .enums import Restaurant as RestaurantEnum


class Restaurant(models.Model):
    class Meta:
        db_table = "restaurants"

    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.name}"


class Dish(models.Model):
    class Meta:
        db_table = "dishes"
        verbose_name_plural = "dishes"

    name = models.CharField(max_length=50, null=True)
    price = models.IntegerField()
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} {self.price}  ({self.restaurant})"


class Order(models.Model):
    """the instance of that class defines the order of dishes from
    external restaurant that is available in the system.

    dishes in plural.

    ARGS
    -- Idea:
    restaurants_meta: dict = {
        "provider": {
            "order_id": string,
            "order_status": string,
            "dishes": [
                {
                    "dish": string,
                    "quantity": number,
                }, ...
            ]
        }

    }
    """

    class Meta:
        db_table = "orders"

    status = models.CharField(max_length=20)
    provider = models.CharField(max_length=20, null=True, blank=True)
    eta = models.DateField()
    external_order_id_melange = models.CharField(max_length=100, null=True, blank=True)
    external_order_id_bueno = models.CharField(max_length=100, null=True, blank=True)

    # restaurants_meta = models.JSONField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.status} for {self.user.email}"

    def __repr__(self) -> str:
        return super().__str__()

    @classmethod
    def update_from_provider_status(cls, id_: int, status: str, delivery=False) -> None:
        if delivery is False:
            if status == "finished":
                cls.objects.filter(id=id_).update(status=OrderStatus.DRIVER_LOOKUP)
            else:
                cls.objects.filter(id=id_).update(
                    status=RESTAURANT_TO_INTERNAL_STATUSES[RestaurantEnum.MELANGE][
                        status
                    ]
                )
        else:
            if status == "delivered":
                cls.objects.filter(id=id_).update(status=OrderStatus.DELIVERED)
            elif status == "delivery":
                cls.objects.filter(id=id_).update(status=OrderStatus.DELIVERY)
            elif status == "delivered":
                cls.objects.filter(id=id_).update(status=OrderStatus.DELIVERED)
            else:
                raise ValueError(f"Status {status} is not supported")


class DishOrderItem(models.Model):
    """the instance of that class defines a DISH item that is related
    to an ORDER, that user has made.


    NOTES
    --------

    do we need user in relations?
    NOT! because we have it in the ``Order``
    """

    class Meta:
        db_table = "dish_order_items"

    quantity = models.SmallIntegerField()

    dish = models.ForeignKey("Dish", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return f"[{self.order.pk}] {self.dish.name}: {self.quantity}"
