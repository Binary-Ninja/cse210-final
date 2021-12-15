"""This file holds the item classes."""

# Description:
#   The following class Item is the class for all inventory items.
#
# OOP Principles Used:
#   Inheritance and Polymorphism
#
# Reasoning:
#   This class uses inheritance because it is also used as a superclass for more specific item classes.
#   This class uses polymorphism because it and all its subclasses are valid inventory items.

# Description:
#   The following class Seed is used as a specific Item type that holds plant data.
#
# OOP Principles Used:
#   Inheritance and Polymorphism
#
# Reasoning:
#   This class uses inheritance because it is a subclass from Item.
#   This class uses polymorphism because it acts like a regular item in the player inventory.

__all__ = [
    "Item",
    "Seed",

    "HOE",
    "WATERING_CAN_EMPTY",
    "WATERING_CAN_FULL",

    "ALL_SEEDS",
]

HOE = "Hoe"
WATERING_CAN_EMPTY = "Empty Watering Can"
WATERING_CAN_FULL = "Full Watering Can"

SEED_TYPE = tuple[str, tuple[int, ...], list[dict]]

PUMPKIN_DATA: SEED_TYPE = ("Pumpkin", (2,), [
    {"time": 120, "tile": (0xa2, (0, 255, 0), None), "water": True},
    {"time": 120, "tile": (0xa2, (255, 128, 0), None), "water": True},
    {"tile": (0x4f, (255, 128, 0), None)},
])

WHEAT_DATA: SEED_TYPE = ("Wheat", (2,), [
    {"time": 100, "tile": (0xb0, (220, 220, 100), None), "water": True},
    {"time": 100, "tile": (0xb1, (220, 220, 100), None)},
    {"tile": (0xb2, (220, 220, 100), None)},
])

GRASS_DATA: SEED_TYPE = ("Grass", (1, 2), [
    {"time": 0, "tile": (0x22, (0, 128, 0), None)},
    {"tile": (0x22, (0, 128, 0), None)},
])

REED_DATA: SEED_TYPE = ("Reed", (0,), [
    {"time": 200, "tile": (0x7c, (0, 200, 0), None)},
    {"tile": (0xf4, (0, 200, 0), None)},
])

BERRY_DATA: SEED_TYPE = ("Berry Bush", (1, 2), [
    {"time": 200, "tile": (0x05, (0, 255, 0), None), "water": True},
    {"time": 200, "tile": (0x05, (0, 128, 0), None), "water": True},
    {"tile": (0x05, (110, 50, 150), None)},
])

LILY_DATA: SEED_TYPE = ("Water Lily", (0, ), [
    {"time": 50, "tile": (0x07, (0, 255, 0), None)},
    {"time": 100, "tile": (0x09, (0, 255, 0), None)},
    {"time": 100, "tile": (0x0f, (0, 255, 0), None)},
    {"tile": (0x0f, (255, 255, 255), None)},
])

MUSHROOM_DATA: SEED_TYPE = ("Mushroom", (1,), [
    {"time": 300, "tile": (0x18, (255, 128, 128), None)},
    {"tile": (0x06, (255, 0, 0), None)},
])

ALL_SEEDS = (
    PUMPKIN_DATA,
    WHEAT_DATA,
    GRASS_DATA,
    REED_DATA,
    LILY_DATA,
    BERRY_DATA,
    MUSHROOM_DATA,
)


class Item:
    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        """Return the text to display the item in the inventory."""
        return self.name

    def __len__(self):
        """Convenience method for returning length of item name."""
        return len(self.get_name())

    def __repr__(self):
        return f"Item({self.name})"


class Seed(Item):
    def __init__(self, name: str, valid_tiles: tuple[int, ...], stages: list[dict], count: int):
        super().__init__(name)
        self.valid_tiles = valid_tiles
        self.stages = stages
        self.count = count

    def get_name(self):
        return f"{self.count} {self.name} seeds"

    def __getitem__(self, item):
        """Convenience method for unpacking the data."""
        if item == 0:
            return self.name
        elif item == 1:
            return self.valid_tiles
        elif item == 2:
            return self.stages
        else:
            raise IndexError("Valid items are 0, 1, and 2.")

    def __repr__(self):
        return f"Seed({self.name}, {self.valid_tiles}, {self.stages}, {self.count})"
