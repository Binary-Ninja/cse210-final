"""The file that holds the simulation classes."""

from pygame.math import Vector2

PLAYER_TILES = {
    (1, 0): (0x10, (255, 255, 255), None),
    (-1, 0): (0x11, (255, 255, 255), None),
    (0, -1): (0x1e, (255, 255, 255), None),
    (0, 1): (0x1f, (255, 255, 255), None),
}

WATER_TILE = (0xf7, (0, 0, 255), None)
DIRT_TILE = (0xfa, (128, 64, 0), None)
FARMLAND_TILE = (0xf7, (128, 64, 0), None)

GRID_TILES = {
    0: WATER_TILE,
    1: DIRT_TILE,
    2: FARMLAND_TILE,
}


def vec_to_tuple(x: Vector2) -> tuple[int, int]:
    """Converts a Vector2 class to a tuple of integers."""
    return int(x[0]), int(x[1])


class Plant:
    def __init__(self, pos: tuple[int, int]):
        self.pos = Vector2(pos)
        self.tile = (0x06, (0, 255, 0), None)


class Simulation:
    """The simulation class for the Cell Engine."""
    def __init__(self, size: tuple[int, int]):
        """Create an empty simulation of a given size."""
        # The size of the simulation.
        self.size = size
        # Store the plants in a list.
        self.plants: list[Plant] = []
        # Dictionary of keys: pos to value: Plant.
        self.pos_2_plant: dict[tuple[int, int], Plant] = {}
        # Store the grid data in a 2d list.
        self.grid = [[0 for _ in range(size[1])] for _ in range(size[0])]
        # Set of all cells that changed since last time.
        self.updates = set()
        # The global time.
        self.global_time = 0

    def update_one_turn(self, amount: int = 100):
        """Update the simulation by one turn (100tu)."""
        self.global_time += amount
