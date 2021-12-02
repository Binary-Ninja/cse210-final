"""The file that holds the simulation classes."""

import heapq

from pygame.math import Vector2


def vec_to_tuple(x: Vector2) -> tuple[int, int]:
    """Converts a Vector2 class to a tuple of integers."""
    return int(x[0]), int(x[1])


class Actor:
    """The Actor superclass."""
    def __init__(self, time_units: int = 0):
        self.time_units = time_units
        self.dead = False

    def __lt__(self, other):
        """Overload '<' for heapq sorting."""
        return self.time_units < other.time_units

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
    def __init__(self, simulation: "Simulation", pos: tuple[int, int], time_units: int = 0):
        super().__init__(time_units)
        self.simulation = simulation
        self.pos = Vector2(pos)
        self.tile = (0x40, (255, 128, 0), (128, 255, 0))

    def move(self, new_pos: tuple[int, int]):
        """Move the cell to a new position.

        Assume valid position.
        """
        # Update old position.
        self.simulation.updates.add(vec_to_tuple(self.pos))
        # Remove old quick lookup.
        del self.simulation.pos_2_actor[vec_to_tuple(self.pos)]
        # Modify position.
        self.pos = Vector2(new_pos)
        # Add new quick lookup.
        self.simulation.pos_2_actor[new_pos] = self
        # Update new position.
        self.simulation.updates.add(vec_to_tuple(self.pos))

    def take_action(self):
        """Perform the cell's next action."""
        self.move(vec_to_tuple(self.pos + Vector2(1, 0)))
        self.time_units += 100


class Simulation:
    """The simulation class for the Cell Engine."""
    def __init__(self, size: tuple[int, int]):
        """Create an empty simulation of a given size."""
        self.size = size
        # There exists a sentinel Turn counter.
        self.turn_counter = Turn(self)
        # Store the cells in a list, ordered by time units.
        self.cells: list[Actor] = [self.turn_counter]
        # Store the grid data in a 2d list.
        # 0 is an empty cell.
        # 1 is a wall.
        self.grid = [[0 for y in range(size[1])] for x in range(size[0])]
        # Set of all cells that changed since last time.
        self.updates = set()
        # Dictionary of keys: pos to value: Actor.
        self.pos_2_actor = {}

    def toggle_cell(self, pos: tuple[int, int]):
        """Add or remove a cell at the given position.

        Assume the position is valid.
        """
        if self.pos_2_actor.get(pos, False):
            # Remove cell.
            self.remove_cell(pos)
        else:
            # Add cell.
            self.add_cell(pos)

    def remove_cell(self, pos: tuple[int, int]):
        """Remove a Cell from the given position.

        Assume the position is valid.
        """
        cell = self.pos_2_actor[pos]
        # Remove cell from turn order by marking it dead.
        cell.dead = True
        # Update the quick lookup dictionary.
        del self.pos_2_actor[pos]
        # Mark the position for updates.
        self.updates.add(pos)

    def add_cell(self, pos: tuple[int, int]):
        """Add a Cell to the given position.

        Assume the position is valid.
        """
        # Create new Cell from information.
        # Give time units so it has the proper global time.
        cell = Cell(self, pos, time_units=self.cells[0].time_units)
        # Insert the cell at the front of the turn order.
        self.cells.insert(0, cell)
        # Update the quick lookup dictionary.
        self.pos_2_actor[pos] = cell
        # Mark the position for updates.
        self.updates.add(pos)

    def toggle_wall(self, pos: tuple[int, int]):
        """Toggle whether a wall exists at the given position."""
        # Toggle the wall.
        self.grid[pos[0]][pos[1]] = not self.grid[pos[0]][pos[1]]
        # Mark the position for updates.
        self.updates.add(pos)

    def update_one_action(self) -> Actor:
        """Update the simulation by one actor's action.

        Returns the actor that took an action.
        """
        # Get the next actor.
        actor = heapq.heappop(self.cells)
        # Take action if not dead.
        if actor.dead:
            return actor
        else:
            actor.take_action()
        # Resort the turn order.
        heapq.heappush(self.cells, actor)
        # Return the actor to take an action.
        return actor

    def update_one_turn(self):
        """Update the simulation by one turn (100tu)."""
        while True:
            if self.update_one_action() is self.turn_counter:
                break