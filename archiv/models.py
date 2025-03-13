from django.db import models
from food.models import DishesOrder

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


class DeliveryDishesOrder(models.Model):
    """
    Logs delivery details for internal or external services.
    """
    class Meta:
        db_table = 'dishes_orders_deliveries'
        verbose_name_plural = 'Товаро-транспортный документ'

    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, blank=False, verbose_name= "Провайдер" )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in_progress', blank=False, verbose_name="Статус")
    addresses = models.TextField(verbose_name = "Адрес доставки")
    external_order_id = models.CharField(max_length=100, unique=True, blank=False, verbose_name= "Маркер Доставки")

    dish_order = models.ForeignKey(
        DishesOrder,
        on_delete=models.CASCADE,
        related_name='delivery',
        blank=False
    )


    def __str__(self):
        return (f"Доставка № {self.id}; "
                f"Оператор:[{self.provider}],"
                f"Заказ №: {self.external_order_id}; "
                f"Статус:[{self.status}]")