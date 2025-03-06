from django.core.handlers.wsgi import WSGIRequest
from rest_framework import status, viewsets, routers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Dish, DishOrderItem, Order, Restaurant
from .serializers import DishSerializer, OrderCreateSerializer, RestaurantSerializer, RestaurantWithoutDishesSerializer
from .enums import OrderStatus

from django.utils.timezone import now
import json
from redis import Redis
from uuid import uuid4

redis_client = Redis()



# ========== Food =======================
class FoodAPIViewSet(viewsets.GenericViewSet):
    @action(methods=["post"], detail=False)
    def orders(self, request: WSGIRequest):
        """
        Creating a new order for food.
        """

        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        order_id = uuid4().int % (2 ** 31)

        order_data = {
            "id": order_id,
            "status": OrderStatus.NOT_STARTED,
            "eta": data["eta"],
            "user_id": request.user.id,
            "food": [
                {
                    "dish_id": item["dish"].id if isinstance(item["dish"], Dish) else item["dish"],
                    "quantity": item["quantity"]
                }
                for item in data["food"]
            ],
        }

        eta_date = data["eta"]
        today_date = now().date()

        if eta_date < today_date:
            return Response(
                {"error": "Date is out of range"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_data["eta"] = order_data["eta"].isoformat()


        redis_key = f"order:{order_id}"
        redis_client.set(redis_key, json.dumps(order_data))
        print(f"Order {order_id} saved in Redis")

        return Response(
            data={
                "message": "Order created",
                "id": order_id,
                "status": "NOT_STARTED",
            },
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
