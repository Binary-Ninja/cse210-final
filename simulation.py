"""The file that holds the simulation classes."""

from pygame.math import Vector2


class Actor:
    """The Actor superclass."""
    def __init__(self, time_units: int = 0):
        self.time_units = time_units

    def take_action(self):
        """Should be overridden in the child classes."""
        raise NotImplementedError("Actor.take_action should be overridden in the child class.")


class Turn(Actor):
    """The Turn counter class, handling things once per turn."""
    def __init__(self, simulation: "Simulation"):
        super().__init__()
        self.simulation = simulation

    def take_action(self):
        """Always spend 100tu, which is one turn."""
        self.time_units += 100


class Cell(Actor):
    """The Cell class for the creatures in the Cell Engine."""
    def __init__(self, simulation: "Simulation", pos: tuple[int, int]):
        super().__init__()
        self.simulation = simulation
        self.pos = Vector2(pos)

    def take_action(self):
        """Perform the cell's next action."""
        self.time_units += 100


class Simulation:
    """The simulation class for the Cell Engine."""
    def __init__(self, size: tuple[int, int]):
        """Create an empty simulation of a given size."""
        self.size = size
        # Store the cells in a list, ordered by time units.
        # There exists a sentinel Turn counter.
        self.cells: list[Actor] = [Turn(self)]
        # Store the grid data in a 2d list.
        # 0 is an empty cell.
        # 1 is a wall.
        self.grid = [[0 for y in range(size[1])] for x in range(size[0])]
        # Set of all cells that changed since last time.
        self.updates = set()

    def toggle_wall(self, pos: tuple[int, int]):
        """Toggle whether a wall exists at the given position."""
        self.grid[pos[0]][pos[1]] = not self.grid[pos[0]][pos[1]]
        self.updates.add(pos)

    def update_one_action(self):
        """Update the simulation by one actor's action."""

    def update_one_turn(self):
        """Update the simulation by one turn (100tu)."""
