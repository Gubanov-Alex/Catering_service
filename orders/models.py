from django.db import models
from users.models import User
from restorants.models import Dish

class Order(models.Model):
    """
    This might represent one "order" of dishes from the user,
    sometimes called the 'cart' or 'basket' before finalization.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dish_orders'
    )
    external_order_id = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return f"DishOrder {self.id} by {self.user}"


class DishOrder(models.Model):
    """
    'Through' model for many dishes in a single DishOrder.
    """
    dish_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_dishes'
    )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"


class DeliveryOrder(models.Model):
    """
    Tracks deliveries from a 3rd party or internal delivery process.
    """
    PROVIDER_CHOICES = (
        ('Uber', 'Uber'),
        ('Uklon', 'Uklon'),
        # etc.
    )
    STATUS_CHOICES = (
        ('ready', 'Ready'),
        ('finished', 'Finished'),
        ('in_progress', 'In Progress'),
        # etc.
    )

    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_progress')
    addresses = models.TextField()
    external_order_id = models.CharField(max_length=100, unique=True)

    dish_order = models.ForeignKey(
        DishOrder,
        on_delete=models.CASCADE,
        related_name='delivery'
    )


    def __str__(self):
        return f"Delivery {self.id} [{self.provider}]"