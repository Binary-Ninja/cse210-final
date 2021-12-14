"""The file that holds the simulation classes."""

from pygame.math import Vector2

PLAYER_TILES = {
    (1, 0): (0x10, (255, 255, 255), None),
    (-1, 0): (0x11, (255, 255, 255), None),
    (0, -1): (0x1e, (255, 255, 255), None),
    (0, 1): (0x1f, (255, 255, 255), None),
}

WATER_TILE = (0xf7, (0, 0, 255), (0, 0, 0))
DIRT_TILE = (0xfa, (128, 64, 0), (0, 0, 0))
FARMLAND_TILE = (0xf7, (128, 64, 0), (0, 0, 0))

GRID_TILES = {
    0: WATER_TILE,
    1: DIRT_TILE,
    2: FARMLAND_TILE,
}


def vec_to_tuple(x: Vector2) -> tuple[int, int]:
    """Converts a Vector2 class to a tuple of integers."""
    return int(x[0]), int(x[1])


class Plant:
    def __init__(self, simulation: "Simulation", pos: tuple[int, int],
                 name: str, valid_tiles: tuple[int, ...], stages: list[dict]):
        self.simulation = simulation
        self.pos = pos

        # Seed data.
        self.name = name
        self.valid_tiles = valid_tiles
        self.stages = stages

        # Other instance variables.
        self.done_growing = False
        self.stage = 0
        self.tile = self.stages[self.stage]["tile"]
        self.last_time = self.simulation.global_time
        self.needs_water = self.stages[self.stage].get("water", False)

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

    def update(self):
        """Update the plant."""
        if self.done_growing:
            return

        if self.simulation.global_time - self.last_time >= self.stages[self.stage]["time"] and \
                not self.needs_water:
            # Update the simulation.
            self.simulation.updates.add(self.pos)
            # Update the variables.
            self.stage += 1
            self.tile = self.tile if (new_tile := self.stages[self.stage].get("tile", None)) is None \
                else new_tile
            self.last_time = self.simulation.global_time
            self.needs_water = self.stages[self.stage].get("water", False)

            # Make the plant stop growing.
            if self.stage == len(self.stages) - 1:
                self.done_growing = True
                return


class Simulation:
    """The simulation class for the Cell Engine."""
    def __init__(self, size: tuple[int, int]):
        """Create an empty simulation of a given size."""
        # The size of the simulation.
        self.size = size
        # Quick lookup of plants based on position.
        self.plants: dict[tuple[int, int], Plant] = {}
        # Store the grid data in a 2d list.
        self.grid = [[0 for _ in range(size[1])] for _ in range(size[0])]
        # Set of all cells that changed since last time.
        self.updates = set()
        # The global time.
        self.global_time = 0

    def add_plant(self, pos: tuple[int, int],
                  name: str, valid_tiles: tuple[int, ...], stages: list[dict]):
        """Add a plant to the world."""
        self.plants[pos] = Plant(self, pos, name, valid_tiles, stages)
        self.updates.add(pos)

    def remove_plant(self, plant: Plant):
        """Remove a plant from the world."""
        del self.plants[plant.pos]
        self.updates.add(plant.pos)

    def update_ticks(self, amount: int = 1):
        """Update the simulation by some amount of ticks."""
        self.global_time += amount
        # Update all the plants.
        for plant in self.plants.values():
            plant.update()
