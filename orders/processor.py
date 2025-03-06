from datetime import date
from threading import Thread
from time import sleep

from django.db.models import QuerySet

from redis import Redis


import json

from products.models import Order
from products.enums import OrderStatus


# class Processor:
# 
#     EXCLUDE_STATUSES = (
#         OrderStatus.DELIVERED,
#         OrderStatus.NOT_DELIVERED,
#     )
# 
#     def __init__(self) -> None:
#         self._thread = Thread(target=self.process, daemon=True)
#         print(f"Orders Processor is created")
# 
#     @property
#     def today(self):
#         return date.today()
# 
#     def start(self):
#         self._thread.start()
#         print(f"Orders Processor started processing orders")
# 
#     def process(self):
#         """The processing of the orders entrypoint."""
# 
#         while True:
#             self._process()
#             sleep(2)  # delay
# 
#     def _process(self):
# 
#         orders: QuerySet[Order] = Order.objects.exclude(
#             status__in=self.EXCLUDE_STATUSES,
#         )
# 
#         for order in orders:
#             match order.status:
#                 case OrderStatus.NOT_STARTED:
#                     self._process_not_started(order)
#                 case OrderStatus.COOKING_REJECTED:
#                     self._process_cooking_rejected()
#                 case _:
#                     print(f"Unrecognized order status: {order.status}. passing")
# 
#     def _process_not_started(self, order: Order):
#         """
#         INPUT DATA
#         -------------
#         TODAY: 03.03.2025
#         ETA:   04.03.2025
# 
#         CONDITIONS
#         --------------
#         ETA1:   02.03.2025  -> CANCELLED (because deprecated/outdated)
#         ETA2:   03.03.2025  -> do nothing
#         ETA3:   04.03.2025  -> COOKING + send API call to restaurants
#         """
# 
#         if order.eta > self.today:
#             pass
#         elif order.eta < self.today:
#             order.status = OrderStatus.CANCELLED
#             order.save()
#             print(f"Cancelled order {order}")
#         else:
#             # today scenario
#             order.status = OrderStatus.COOKING
#             order.save()
# 
#             restaurants = set()
#             for item in order.items.all():
#                 restaurants.add(item.dish.restaurant)
# 
#             print(f"Finished preparing order. Restaurants: {restaurants}")
#             print(f"Order: {order}")
# 
#     def _process_cooking_rejected(self):
#         raise NotImplementedError

#

class Processor:
    EXCLUDE_STATUSES = (
        OrderStatus.DELIVERED,
        OrderStatus.NOT_DELIVERED,
    )

    # CACHE_KEY = "orders:today"
    CACHE_KEY = "orders_cache_key"

    def __init__(self) -> None:
        self.cache = Redis()  # Connection to Redis
        self._cache_thread = Thread(target=self.cache_updater, daemon=True)
        self._processing_thread = Thread(target=self.orders_processor, daemon=True)
        print("Orders Processor is created")

    @property
    def today(self):
        return date.today()

    def start(self):
        """Start both threads for caching and processing."""
        self._cache_thread.start()
        self._processing_thread.start()
        print("Orders Processor started:")

    def cache_updater(self):
        """Thread to update the orders cache every 15 minutes."""
        while True:
            self._fetch_orders_and_update_cache()
            sleep(5)  # 15 minutes (900 seconds)

    def orders_processor(self):
        """Thread to process orders every 10 seconds."""
        while True:
            try:
                self._process()
            except Exception as e:
                print(f"Error while processing orders: {e}")
            sleep(5)  # 10 seconds

    # def _fetch_orders_and_update_cache(self):
    #     """Fetch orders from the database and update them in the cache."""
    #     # Fetch orders excluding certain statuses
    #     orders: QuerySet[Order] = Order.objects.filter(
    #         eta=self.today
    #     ).exclude(
    #         status__in=self.EXCLUDE_STATUSES,
    #     )
    #
    #     # Convert orders into cache-compatible format (e.g., only ID and status)
    #     orders_data = [
    #         {"id": order.id, "status": order.status, "eta": str(order.eta)}
    #         for order in orders
    #     ]
    #
    #     # Save to Redis
    #     orders_data_json = json.dumps(orders_data)
    #     self.cache.set(self.CACHE_KEY, orders_data_json)
    #
    #     print(f"Cache updated {self.today}: {orders_data}")

    def _fetch_orders_and_update_cache(self):
        """
        Updates Redis cache for each individual order to avoid complete rewrites.
        """
        # Get today's orders
        orders: QuerySet[Order] = Order.objects.filter(
            eta=self.today
        ).exclude(
            status__in=self.EXCLUDE_STATUSES,
        )

        # Initialize Redis connection
        cache = self.cache

        # Collect all current order IDs
        current_order_ids = set()
        for order in orders:
            current_order_ids.add(order.id)

            # Redis key for this order
            redis_key = f"{self.CACHE_KEY}:{order.id}"

            # Store order data
            order_data = {"id": order.id, "status": order.status, "eta": str(order.eta)}
            cache.set(redis_key, json.dumps(order_data))

        # Identify stale orders (existing in Redis but not in the database)
        redis_keys = cache.keys(pattern=f"{self.CACHE_KEY}:*")
        for redis_key in redis_keys:
            order_id = int(redis_key.decode("utf-8").split(":")[-1])
            if order_id not in current_order_ids:
                cache.delete(redis_key)


    # def _process(self):
    #     """Process orders from the cache."""
    #     orders_data_json = self.cache.get(self.CACHE_KEY)  # Read data from Redis
    #
    #     if not orders_data_json:
    #         print("Cache is empty. No orders to process.")
    #         return
    #
    #     orders_data = json.loads(orders_data_json)
    #
    #     # Process each order based on its status
    #     for order_dict in orders_data:
    #         match order_dict["status"]:
    #             case OrderStatus.NOT_STARTED:
    #                 self._process_not_started(order_dict)
    #             case OrderStatus.COOKING_REJECTED:
    #                 self._process_cooking_rejected(order_dict)
    #             case _:
    #                 print(f"Unknown order status: {order_dict['status']}. Skipping.")

    def _process(self):
        """Process orders from the cache."""
        redis_keys = self.cache.keys(f"{self.CACHE_KEY}:*")  # Получаем все ключи

        if not redis_keys:
            print("Cache is empty. No orders to process.")
            return

        for redis_key in redis_keys:
            order_data_json = self.cache.get(redis_key)
            if not order_data_json:
                continue  # Пропускаем, если ключа нет
            order_dict = json.loads(order_data_json)

            match order_dict["status"]:
                case OrderStatus.NOT_STARTED:
                    self._process_not_started(order_dict)
                case OrderStatus.COOKING_REJECTED:
                    self._process_cooking_rejected(order_dict)
                case _:
                    print(f"Unknown order status: {order_dict['status']}. Skipping.")

    def _process_not_started(self, order_data):
        """
        Process an order with the status NOT_STARTED.
        """
        eta = date.fromisoformat(order_data["eta"])
        order = Order.objects.get(id=order_data["id"])  # Retrieve the order object from the database

        if eta > self.today:
            # Order is scheduled for a future date
            pass
        elif eta < self.today:
            # Cancel outdated orders
            order.status = OrderStatus.CANCELLED
            order.save()
            print(f"Cancelled order: {order}")
        else:
            # Scenario for today's date
            order.status = OrderStatus.COOKING
            order.save()

            # Notify restaurants about the order
            restaurants = set()
            for item in order.items.all():
                restaurants.add(item.dish.restaurant)

            print(f"Order preparation completed. Restaurants: {restaurants}")
            print(f"Order: {order}")

    def _process_cooking_rejected(self, order_data):
        """
        Process orders with the status COOKING_REJECTED.
        """
        print(f"Processing order with status: {OrderStatus.COOKING_REJECTED}.")
        pass








