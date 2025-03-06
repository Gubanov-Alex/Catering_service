from enum import StrEnum


class OrderStatus(StrEnum):
    NOT_STARTED = "not_started"
    COOKING_REJECTED = "cooking_rejected"
    COOKING = "cooking"
    COOKED = "cooked"
    DRIVER_LOOKUP = "driver_lookup"
    DRIVER_WAITING = "driver_waiting"
    DELIVERED = "delivered"
    NOT_DELIVERED = "not_delivered"
    CANCELLED = "cancelled"


    @classmethod
    def choices(cls):
        results = []

        for element in cls:
            _element = (element.value, element.name.lower().capitalize())
            results.append(_element)

        return results