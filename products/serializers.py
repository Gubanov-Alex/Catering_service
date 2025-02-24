from rest_framework import serializers
from .models import Dish, Restaurant



class DishSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Dish
        fields = "__all__"

class RestaurantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, write_only=True)

    class Meta:
        model = Restaurant
        fields = "__all__"

    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes', [])
        restaurant = Restaurant.objects.create(**validated_data)
        for dish_data in dishes_data:
            Dish.objects.create(restaurant=restaurant, **dish_data)
        return restaurant

class RestaurantWithoutDishesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address']

class DishOrderSerializer(serializers.Serializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    quantity = serializers.IntegerField(min_value=1, max_value=20)


class OrderSerializer(serializers.Serializer):
    food = DishOrderSerializer(many=True)
    total = serializers.IntegerField(min_value=1, read_only=True)
    delivery = serializers.CharField(read_only=True)
    # status = serializers.CharField(read_only=True)


# alternative
# class OrderResponseSerializer(OrderCreateCreateRequestBodySerializer):
#     status = serializers.CharField()


"""
{
    'food': [
        {
            'dish': 1,
            'quantity': 2
        },
    ]
}
"""