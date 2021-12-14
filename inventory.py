"""This file holds the item classes."""

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

ALL_SEEDS = (
    PUMPKIN_DATA,
    WHEAT_DATA,
    GRASS_DATA,
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
