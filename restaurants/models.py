from django.db import models

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
