from django.db import models
from users.models import Order

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


class Restaurant(models.Model):
    """ Restaurant model"""
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Dish(models.Model):
    """ Dish model"""
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='dishes'
    )

    def __str__(self):
        return self.name


class DishOrder(models.Model):
    """
     Intermediate model representing an ordered dish and its quantity.
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
    Logs delivery details for internal or external services.
    """

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

