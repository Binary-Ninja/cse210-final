#!/usr/bin/env python3

"""Contains Font class for loading of tile sheets and bitmap fonts."""

import re
from pathlib import Path

import pygame as pg

# RegEx for checking file name for name, width, and height of font.
# Group 0 is the font name, 1 & 2 are the width and height.
valid_font_regex = re.compile(r"(.+_|_)?(\d+)x(\d+)\.\w{3,4}$")


class Font:
    """Class for loading and parsing images into tile sheets and bitmap fonts."""
    def __init__(self, font_path: Path):
        """Given a path to the font image, returns a Font object with correct tile size.
        The tile size is parsed from the image name with a RegEx, and defaults to (8, 8).
        The main pygame display surface must already be created with pygame.display.set_mode."""
        # Load image from given Path object and convert to display format.
        self.image = pg.image.load(str(font_path)).convert()
        # Search file name for name, width, and height of font.
        if mo := valid_font_regex.search(font_path.name):
            self.name, self.pixel_width, self.pixel_height = mo.groups()
            # If no name supplied, default to empty string.
            self.name = '' if self.name is None else self.name
            # Strip the ending underscore from the name.
            self.name.rstrip('_')
            # Get valid font size in pixels.
            self.pixel_size = self.pixel_width, self.pixel_height = int(self.pixel_width), int(self.pixel_height)
        else:
            # Default to blank name, (8, 8) size.
            self.name = ''
            self.pixel_size = self.pixel_width, self.pixel_height = (8, 8)
        # Get the cell dimensions of the image, cutting off extra pixels at the edges.
        self.width = self.image.get_width() // self.pixel_width
        self.height = self.image.get_height() // self.pixel_height
        self.size = self.width, self.height

    def get_tile(self, tile_id: int) -> pg.Surface:
        """Given a tile ID, returns a pygame.Surface with dimensions of self.size.
        Invalid tile IDs will raise an IndexError."""
        # Raise IndexError if tile ID is out of range.
        if not (0 <= tile_id < self.width * self.height):
            raise IndexError(f"Tile ID out of range: {tile_id}")
        # Create tile Surface with same format as main font image.
        tile = pg.Surface(self.pixel_size)
        # Get x and y coordinates for the blit.
        x = tile_id % self.width
        y = (tile_id - x) // self.width
        # Blit correct tile from font image onto the tile Surface.
        tile.blit(self.image, (0, 0), (x * self.pixel_width, y * self.pixel_height, *self.pixel_size))
        return tile
