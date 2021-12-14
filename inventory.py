"""This file holds the item classes."""

__all__ = [
    "Item",
    "Seed",

    "HOE",
    "WATERING_CAN_EMPTY",
    "WATERING_CAN_FULL",

    "PUMPKIN_DATA",
]

HOE = "Hoe"
WATERING_CAN_EMPTY = "Empty Watering Can"
WATERING_CAN_FULL = "Full Watering Can"

SEED_TYPE = tuple[str, tuple[int, ...], list[dict]]

PUMPKIN_DATA: SEED_TYPE = ("Pumpkin", (2,), [
    {"time": 20, "tile": (0xa2, (0, 255, 0), None)},
    {"time": 20, "tile": (0xa2, (0, 255, 0), None)},
    {"time": 20, "tile": (0x4f, (255, 128, 0), None)},
])


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

    def __repr__(self):
        return f"Seed({self.name}, {self.valid_tiles}, {self.stages}, {self.count})"
