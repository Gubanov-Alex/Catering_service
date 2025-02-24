from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status, viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Dish, DishOrderItem, Order, Restaurant
from .serializers import DishSerializer, OrderSerializer, RestaurantSerializer, RestaurantWithoutDishesSerializer
from .enums import OrderStatus

# ========== Food =======================
class FoodAPIViewSet(viewsets.GenericViewSet):
    # HTTP GET /food/dishes
    @action(methods=["get"], detail=False)
    def dishes(self, request):
        dishes = Dish.objects.all()
        serializer = DishSerializer(dishes, many=True)

        return Response(data=serializer.data)

    # HTTP POST /food/orders
    @action(methods=["post"], detail=False)
    def orders(self, request: WSGIRequest):
        """create new order for food.

        HTTP REQUEST EXAMPLE
        {
            "food": {
                1: 3  // id: quantity
                2: 1  // id: quantity
            }
        }

        WORKFLOW
        1. validate the input
        2. create ``
        """

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not isinstance(serializer.validated_data, dict):
            raise ValueError(...)

        # alternatives
        # -------------
        # assert isinstance(serializer.validated_data, dict)

        # from typing import cast
        # response = cast(dict, serializer.validated_data) | {}

        # ACTIVE RECORD
        # =======================
        # order = Order(status=OrderStatus.NOT_STARTED, provider=None)
        # order.save()

        # ORM
        # ======================
        order = Order.objects.create(status=OrderStatus.NOT_STARTED, user=request.user)
        print(f"New Food Order is created: {order.pk}")

        try:
            dishes_order = serializer.validated_data["food"]
        except KeyError as error:
            raise ValueError("Food order is not properly built")

        for dish_order in dishes_order:
            instance = DishOrderItem.objects.create(
                dish=dish_order["dish"], quantity=dish_order["quantity"], order=order
            )
            print(f"New Dish Order Item is created: {instance.pk}")

        return Response(
            data={"order_id": order.pk, "message": "Order is created"},
            status=status.HTTP_201_CREATED,
        )
# =========================================================

# ================== Restaurants ==========================

class RestaurantsAPIViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    # HTTP GET /restaurants/ID
    @action(methods=["get"], detail=True)
    def details(self, request, pk=None):
        """
        Returns details about the restaurant with the given ID.
        """
        try:
            restaurant = self.get_object()
            serializer = self.get_serializer(restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

    # HTTP GET /restaurants
    def list(self, request, *args, **kwargs):
        """
        Returns a list of all restaurants.
        """
        queryset = self.get_queryset()
        serializer = RestaurantWithoutDishesSerializer(queryset, many=True)
        return Response(serializer.data)

    # HTTP POST /restaurants
    def create(self, request, *args, **kwargs):
        """
        Creates a new restaurant.

        HTTP REQUEST EXAMPLE
        {
            "name": "restaurant",
            "address": "address",
            "dishes": [
                {"name": "Dish 1", "price": 10},
                {"name": "Dish 2", "price": 20}
            ]
        }

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ====================================================================

router = routers.DefaultRouter()
router.register(
    prefix="food",
    viewset=FoodAPIViewSet,
    basename="food",
)
router.register(
    prefix="restaurants",
    viewset=RestaurantsAPIViewSet,
    basename="restaurants",
)
