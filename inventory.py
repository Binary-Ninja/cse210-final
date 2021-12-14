"""This file holds the item classes."""

__all__ = [
    "Item",
    "Seed",

    "HOE",
    "WATERING_CAN_EMPTY",
    "WATERING_CAN_FULL",
]

HOE = "Hoe"
WATERING_CAN_EMPTY = "Empty Watering Can"
WATERING_CAN_FULL = "Full Watering Can"


class Item:
    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        """Return the text to display the item in the inventory."""
        return self.name

    def __len__(self):
        """Convenience method for returning length of item name."""
        return len(self.get_name())


class Seed(Item):
    def __init__(self, name: str, count: int):
        super().__init__(name)
        self.count = count

    def get_name(self):
        return f"{self.count} {self.name} seeds"
