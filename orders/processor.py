from datetime import date, timedelta
from threading import Thread
from time import sleep
import json
from django.db.models import QuerySet
from redis import Redis
from products.models import Order, DishOrderItem
from products.enums import OrderStatus


class Processor:
    EXCLUDE_STATUSES = (
        OrderStatus.DELIVERED,
        OrderStatus.NOT_DELIVERED,
    )
    CACHE_KEY = "order"

    def __init__(self):
        self.cache = Redis()
        self._cache_thread = Thread(target=self.cache_updater, daemon=True)
        self._processing_thread = Thread(target=self.orders_processor, daemon=True)
        self._database_thread = Thread(target=self.orders_to_database, daemon=True)
        print("Orders Processor is created")

    @property
    def today(self):
        return date.today()

    def start(self):
        """Initiate threads for caching, processing, and database syncing."""
        self._cache_thread.start()
        self._processing_thread.start()
        self._database_thread.start()
        print("Orders Processor started:")

    def _save_order_to_database(self, order_data):
        """
        Save the order along with its associated dishes into the database.
        """
        try:
            # First, create the main order instance
            order = Order.objects.create(
                id=order_data["id"],
                status=order_data["status"],
                eta=date.fromisoformat(order_data["eta"]),
                user_id=order_data["user_id"],
            )

            # Then, prepare and save the related DishOrderItem instances
            if "food" in order_data:
                dish_order_items = [
                    DishOrderItem(
                        order=order,
                        dish_id=food_item["dish_id"],
                        quantity=food_item["quantity"],
                    )
                    for food_item in order_data["food"]
                ]
                DishOrderItem.objects.bulk_create(dish_order_items)  # Save all items at once

            print(f"Order {order.id} and associated dishes saved to database.")

        except Exception as e:
            print(f"Error while saving order to database: {e}")

    def _order_exists_in_database(self, order_id):
        """
        Check if an order already exists in the database.
        """
        from products.models import Order
        return Order.objects.filter(id=order_id).exists()

    def orders_processor(self):
        """
        Process today's orders directly from Redis.
        """
        while True:
            # print('work orders')
            try:
                self._process_today_orders()
            except Exception as e:
                print(f"Error while processing today's orders: {e}")
            sleep(5)  # Process every 10 seconds

    def cache_updater(self):
        """
        Thread to monitor Redis and perform actions based on ETA.
        """
        while True:
            # print( 'Work cashe')
            redis_keys = self.cache.keys(pattern="order:*")

            for redis_key in redis_keys:
                order_data_json = self.cache.get(redis_key)
                if not order_data_json:
                    continue

                order_data = json.loads(order_data_json)
                eta = date.fromisoformat(order_data["eta"])

                if eta < self.today:
                    # Reject orders with outdated ETA
                    self.cache.delete(redis_key)
                    print(f"Outdated order removed from cache: {order_data}")

                elif eta == self.today:
                    # Ensure today's orders stay in cache, ready for immediate processing
                    print(f"Valid order for today remains in cache: {order_data}")

                else:
                    # Leave future orders untouched for future sync
                    print(f"Future order remains in cache: {order_data}")

            sleep(5)  # Adjusted to poll and refresh data every 30 seconds

    def orders_to_database(self):
        """
        Sync future orders from Redis to the database every 10 minutes.
        """
        while True:
            # print('work base')
            try:
                redis_keys = self.cache.keys(pattern="order:*")

                for redis_key in redis_keys:
                    order_data_json = self.cache.get(redis_key)
                    if not order_data_json:
                        continue

                    order_data = json.loads(order_data_json)
                    eta = date.fromisoformat(order_data["eta"])

                    if eta > self.today:
                        # Save future orders to the database
                        self._save_order_to_database(order_data)
                        print(f"Future order synced to database: {order_data}")
                        self.cache.delete(redis_key)  # Remove successfully synced order

                    elif eta == self.today:
                        # Ensure today's orders remain in the database
                        if not self._order_exists_in_database(order_data["id"]):
                            self._save_order_to_database(order_data)
                        else:
                            print(f"Order {order_data['id']} already exists in the database. Skipping save.")


            except Exception as e:
                print(f"Error during syncing future orders to database: {e}")
            sleep(30)  # Run every 10 minutes

    def _process_today_orders(self):
        """
        Process orders for today directly from Redis.
        """
        redis_keys = self.cache.keys(pattern="order:*")
        for redis_key in redis_keys:
            order_data_json = self.cache.get(redis_key)
            if not order_data_json:
                continue

            order_data = json.loads(order_data_json)
            eta = date.fromisoformat(order_data["eta"])

            if eta == self.today:
                # Process today's orders
                if order_data["status"] == OrderStatus.NOT_STARTED:
                    self._process_not_started(order_data)
                elif order_data["status"] == OrderStatus.COOKING_REJECTED:
                    self._process_cooking_rejected(order_data)
                else:
                    print(f"Unknown order status: {order_data['status']}. Skipping.")

    def _process_not_started(self, order_data):
        """
            Update NOT_STARTED orders to a new status (e.g., COOKING) directly in Redis.
            """
        try:

            order_id = order_data["id"]


            redis_key = f"order:{order_id}"
            cached_order = self.cache.get(redis_key)
            if not cached_order:
                print(f"Order with ID {order_id} not found in cache.")
                return


            order_data["status"] = OrderStatus.COOKING
            self.cache.set(redis_key, json.dumps(order_data))

            print(f"Order {order_id} updated to status 'COOKING' in cache.")
        except Exception as e:
            print(f"Error while processing NOT_STARTED order: {e}")

    def _process_cooking_rejected(self, order_data):
        """
        Handle orders with COOKING_REJECTED status.
        """
        print(f"Order {order_data['id']} status is COOKING_REJECTED.")






