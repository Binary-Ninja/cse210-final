"""Contains the different organelles for the simulation."""


class Organelle:
    """The superclass Organelle that contains basic functionality."""
    # The upkeep required per turn.
    # Negative upkeep adds energy.
    upkeep = 0

    # The actions the organelle can take.
    # Keys: name of the action
    # Values: tuple of energy cost and time cost
    actions: dict[str, tuple[int, int]] = {}

    def __init__(self, cell):
        self.cell = cell

    def take_action(self, action: str):
        """Perform a given action, costing energy and time."""
        pass


class Chloroplast(Organelle):
    """Produces energy passively."""
    upkeep = -10
