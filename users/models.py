from django.db import models

class User(models.Model):
    """ User model"""
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"


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

