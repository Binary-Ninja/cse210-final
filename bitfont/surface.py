#!/usr/bin/env python3

"""Contains Surface classes for holding and rendering tiles."""

from typing import Union, Sequence

import numpy as np
import pygame as pg

# For type hints only.
from .font import Font

# Cell type for type hints. A cell is a tuple of tile, fg, bg, but any of its elements may be None.
CellType = tuple[Union[int, None], Union[Sequence[int], pg.Color, None], Union[Sequence[int], pg.Color, None]]


class Surface:
    """Class for representing a rectangular area of cells."""

    def __init__(self, size: Sequence[int]):
        """Given a size, returns a Surface object filled with default cells.
        The default cell has ID 0, foreground white, and background black."""
        # Raise ValueError on invalid size argument.
        if len(size) != 2:
            raise ValueError("Size must be of length two; (width, height).")
        # Create width, height, size, and rect attributes.
        self.width, self.height = self.size = size
        self.rect = pg.Rect(0, 0, *self.size)
        # Create arrays of cell attributes.
        self.tile_array = np.full(self.size, 0, np.uint8)
        self.fg_array = np.full((*self.size, 3), 255, np.uint8)
        self.bg_array = np.full((*self.size, 3), 0, np.uint8)
        # Variables for updating, needed for PygameSurface.
        self.points = set()
        self.flip = False

    def copy(self):
        """Returns a Surface copy of self."""
        # Create the copy.
        copy_surface = Surface(self.size)
        # Copy the arrays.
        copy_surface.tile_array = self.tile_array.copy()
        copy_surface.fg_array = self.fg_array.copy()
        copy_surface.bg_array = self.bg_array.copy()
        # Return the copied surface.
        return copy_surface

    @staticmethod
    def bound_rect(surf, rect: Sequence[int] = None) -> Sequence[int]:
        """Given a Surface and a rect, converts rect into a rect for slicing on the Surface."""
        # Get the rect and convert it to a list.
        rect = [0, 0, *surf.size] if rect is None else list(rect)
        # If the draw starts out of bounds, just return an empty rect.
        if rect[0] > surf.width or rect[1] > surf.height:
            return 0, 0, 0, 0
        # Clip negative positions to zero.
        rect[0] = 0 if rect[0] < 0 else rect[0]
        rect[1] = 0 if rect[1] < 0 else rect[1]
        # Add width and height to position to find slicing indices.
        rect[2] += rect[0]
        rect[3] += rect[1]
        # Clip width and height of rect to the bounds of the Surface.
        if rect[2] > surf.width:
            rect[2] = surf.width
        if rect[3] > surf.height:
            rect[3] = surf.height
        # Return the clipped rect.
        return tuple(rect)

    def cell_in_bounds(self, coordinates: Sequence[int]):
        return 0 <= coordinates[0] < self.width and 0 <= coordinates[1] < self.height

    def fill(self, cell: CellType, rect: Sequence[int] = None):
        """Fills the Surface with a given cell. The rect argument limits the fill to a given area."""
        # Don't bother doing anything if we aren't drawing anything.
        if cell == (None, None, None):
            return
        # Bound the rect to the array sizes for slicing.
        rect = Surface.bound_rect(self, rect)
        # Update arrays from cell.
        if cell[0] is not None:
            self.tile_array[rect[0]:rect[2], rect[1]:rect[3]] = cell[0]
        if cell[1] is not None:
            self.fg_array[rect[0]:rect[2], rect[1]:rect[3]] = cell[1]
        if cell[2] is not None:
            self.bg_array[rect[0]:rect[2], rect[1]:rect[3]] = cell[2]
        # Update the Surface.
        for w, h in np.ndindex((rect[2], rect[3])):
            self.points.add((rect[0] + w, rect[1] + h))

    def blit(self, source, pos: Sequence[int], rect: Sequence[int] = None,
             apply: Sequence[bool] = (True, True, True)):
        """DO NOT USE. Please use function blit2 instead. This one does not work in all cases.
        This function may be faster however, though that is not confirmed. USE AT OWN RISK.
        Copies cells from source onto this Surface. The draw starts at pos.
        The optional rect represents a smaller portion of the source surface to draw."""
        # Don't bother doing anything if we aren't drawing anything.
        if apply == (None, None, None):
            return
        # Bound the rect to the source surface for source slicing.
        rect = Surface.bound_rect(source, rect)
        # Bound the rect to the master surface to clip in bounds.
        rect = Surface.bound_rect(self, rect)
        # Bound the rect to self for self slicing.
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        source_rect = Surface.bound_rect(self, (*pos, w, h))
        # Change the rect dimensions to clip in bounds.
        rect = list(rect)
        rect[2] = source_rect[2] - source_rect[0]
        rect[3] = source_rect[3] - source_rect[1]
        # Blit the source material onto self.
        if apply[0]:
            self.tile_array[source_rect[0]:source_rect[2], source_rect[1]:source_rect[3]] = \
                source.tile_array[rect[0]:rect[2], rect[1]:rect[3]]
        if apply[1]:
            self.fg_array[source_rect[0]:source_rect[2], source_rect[1]:source_rect[3]] = \
                source.fg_array[rect[0]:rect[2], rect[1]:rect[3]]
        if apply[2]:
            self.bg_array[source_rect[0]:source_rect[2], source_rect[1]:source_rect[3]] = \
                source.bg_array[rect[0]:rect[2], rect[1]:rect[3]]
        # Update the surface.
        for w, h in np.ndindex((source_rect[2], source_rect[3])):
            if self.cell_in_bounds((source_rect[0] + w, source_rect[1] + h)):
                self.points.add((source_rect[0] + w, source_rect[1] + h))

    def blit2(self, source, pos: Sequence[int], rect: Union[Sequence[int], pg.Rect] = None,
              apply: Sequence[bool] = (True, True, True)) -> Union[Sequence[int], pg.Rect]:
        """Copies cells from source surface onto this Surface. The draw starts at pos.
        The optional rect represents a smaller portion of the source surface to draw.
        The rect is assumed to be completely inside the source surface. Errors occur otherwise.
        The apply mode states whether to blit only the tiles, colors, etc.
        It is a sequence of booleans (tile, fg, bg).
        Returns the rectangular area of affected cells."""
        # Return if we aren't drawing anything.
        if apply == (False, False, False):
            return 0, 0, 0, 0
        # Return if drawing position is out of bounds.
        if pos[0] >= self.width or pos[1] >= self.height:
            return 0, 0, 0, 0
        # Get the rect used to pull cells from the source surface.
        source_rect = source.rect if rect is None else rect
        # Get the intersection of affected cells.
        drawing_rect = pg.Rect(pos[0], pos[1], source_rect[2], source_rect[3]).clip(self.rect)
        # Return if rect does not overlap with the surface.
        if drawing_rect.size == (0, 0):
            return 0, 0, 0, 0
        # Loop and blit source onto self and update the points.
        for x, y in np.ndindex((source_rect[2], source_rect[3])):
            # Save cells into temporary variables to avoid lots of math.
            dest_cell = (pos[0] + x, pos[1] + y)
            source_cell = (source_rect[0] + x, source_rect[1] + y)
            # Only draw if cell is in bounds.
            if self.cell_in_bounds(dest_cell):
                # Only draw when applicable.
                if apply[0]:
                    self.tile_array[dest_cell] = source.tile_array[source_cell]
                if apply[1]:
                    self.fg_array[dest_cell] = source.fg_array[source_cell]
                if apply[2]:
                    self.bg_array[dest_cell] = source.bg_array[source_cell]
                # Update the points.
                self.points.add(dest_cell)
        # Return the area of affected cells.
        # print(drawing_rect)
        return drawing_rect

    def draw_cell(self, point: tuple[int, int], cell: CellType):
        """Draws a single cell CellType at position point."""
        # Make sure the point is in bounds.
        if self.cell_in_bounds(point):
            # Draw point according to cell given.
            if cell[0] is not None:
                self.tile_array[point] = cell[0]
            if cell[1] is not None:
                self.fg_array[point] = cell[1]
            if cell[2] is not None:
                self.bg_array[point] = cell[2]
            # Update the surface.
            self.points.add(point)

    def draw_cells(self, points: Sequence[tuple[int, int]], cell: CellType):
        """Given a list of points and a cell, colors in all those points with that cell."""
        # Don't bother doing anything if we aren't drawing anything.
        if cell == (None, None, None):
            return
        # For each point, draw the point.
        for point in points:
            self.draw_cell(point, cell)

    def write_cells(self, tiles: Union[Sequence[int], bytes], start_pos: tuple[int, int],
                    cell: CellType = (None, None, None), direction: tuple[int, int] = (1, 0)):
        """Given a sequence of tiles, writes those tiles to start_pos, moving along direction given.
        Direction defaults to positive x by 1 cell, ideal for printing text.
        An optional cell for foreground / background colors can also be provided."""
        # The current position we are writing to.
        current_pos = start_pos
        # Loop through the tiles to draw.
        for tile in tiles:
            # Draw the tile.
            self.draw_cell(current_pos, (tile, cell[1], cell[2]))
            # Update the current position from the direction vector.
            current_pos = current_pos[0] + direction[0], current_pos[1] + direction[1]

    def update(self):
        """This function is overridden in PygameSurface."""
        # After updating, refresh the update variables.
        self.points = set()
        self.flip = False


class PygameSurface(Surface):
    """Child class of Surface that actually renders its cells to a pygame surface."""

    def __init__(self, size: Sequence[int], font: Font):
        """Given a size and a font object, returns a PygameSurface object filled with default cells.
        The default cell has ID 0, foreground white, and background black.
        The main pygame display surface must already be created with pygame.display.set_mode."""
        # Initialize parent class.
        super().__init__(size)
        # Create buffer arrays.
        self.tile_buffer = self.tile_array.copy()
        self.fg_buffer = self.fg_array.copy()
        self.bg_buffer = self.bg_array.copy()
        # Get font and size attributes.
        self.font = font
        self.pixel_width, self.pixel_height = self.width * self.font.pixel_width, self.height * self.font.pixel_height
        self.pixel_size = self.pixel_width, self.pixel_height
        # Create main render surface.
        self.image = pg.Surface(self.pixel_size).convert()
        # Draw all cells to the main render surface on next update call.
        self.flip = True

    def change_font(self, font: Font):
        """Change the font of the PygameSurface, but keep its cell dimensions the same."""
        # Get font and size attributes.
        self.font = font
        self.pixel_width, self.pixel_height = self.width * self.font.pixel_width, self.height * self.font.pixel_height
        self.pixel_size = self.pixel_width, self.pixel_height
        # Create main render surface.
        self.image = pg.Surface(self.pixel_size).convert()
        # Draw all cells to the main render surface on next update call.
        self.flip = True

    @staticmethod
    def refactor_size(size: tuple[int, int], font: Font):
        """Returns a new PygameSurface that will fit inside the given pixel dimensions."""
        w = size[0] // font.pixel_width
        h = size[1] // font.pixel_height
        return PygameSurface((w, h), font)

    def get_pixel_pos(self, pos: tuple[int, int], clamp: bool = True):
        """Given cell coordinates, translate to the top left pixel coordinates of that cell.
        Optionally clamps result to inside the surface, defaults to True."""
        # Multiply cell by font dimensions.
        x = pos[0] * self.font.pixel_width
        y = pos[1] * self.font.pixel_height
        # Clamp the resulting point to inside the surface.
        if clamp:
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x > self.pixel_width - 1:
                x = self.pixel_width - 1
            if y > self.pixel_height - 1:
                y = self.pixel_height - 1
        # Return that point.
        return x, y

    def get_cell_pos(self, pos: tuple[int, int], clamp: bool = True):
        """Given pixel coordinates, translate to cell coordinates.
        Optionally clamps result to inside the surface, defaults to True."""
        # Floor divide point by surface size.
        x = pos[0] // self.font.pixel_width
        y = pos[1] // self.font.pixel_height
        # Clamp the resulting cell to inside the surface.
        if clamp:
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x > self.width - 1:
                x = self.width - 1
            if y > self.height - 1:
                y = self.height - 1
        # Return that cell.
        return x, y

    def _draw_cell(self, pos: Sequence[int], surf: pg.Surface = None):
        """Given a cell position, draws tile in correct colors on given surface."""
        # Default to drawing on own surface.
        if surf is None:
            surf = self.image
        # Fill the cell with the background color.
        surf.fill(self.bg_array[pos], (pos[0] * self.font.pixel_width, pos[1] * self.font.pixel_height,
                                       *self.font.pixel_size))
        # Load in tile image from the Font.
        fg_surf = self.font.get_tile(self.tile_array[pos])
        # Color in the image with the foreground color.
        fg_surf.fill(self.fg_array[pos], None, pg.BLEND_RGB_MULT)
        # Set the key color to black for transparency.
        fg_surf.set_colorkey((0, 0, 0))
        # Blit foreground onto cell on image.
        surf.blit(fg_surf, (pos[0] * self.font.pixel_width, pos[1] * self.font.pixel_height))

    def update(self, surf: pg.Surface = None):
        """Actually render the cells on the given surface, defaults to its own surface."""
        # Actually draw the required cells.
        if self.flip:
            # Redraw the whole surface.
            for x, y in np.ndindex(self.size):
                self._draw_cell((x, y), surf)
        elif self.points:
            # Redraw only the points that have changed.
            for p in self.points:
                if not (self.tile_buffer[p] == self.tile_array[p] and
                        (self.bg_buffer[p] == self.bg_array[p]).all() and
                        (self.fg_buffer[p] == self.fg_array[p]).all()):
                    self._draw_cell(p, surf)
        # Only bother updating buffers and clearing data if cells have changed.
        if self.flip or self.points:
            # Update buffer arrays.
            self.tile_buffer = self.tile_array.copy()
            self.fg_buffer = self.fg_array.copy()
            self.bg_buffer = self.bg_array.copy()
            # Clear the update variables through super().
            super().update()
