#!/usr/bin/env python3

import sys
from datetime import datetime
from pathlib import Path

import pygame as pg
from pygame.math import Vector2

import bitfont as bf

from simulation import Simulation, vec_to_tuple, PLAYER_TILES, WATER_TILE, DIRT_TILE


class Main:
    def __init__(self):
        """Initialize the application."""
        # Create main screen.
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Final Project")
        # Create main cell screen.
        self.font = bf.Font(Path() / 'bitfont' / 'fonts' / 'CP437_12x12.png')
        self.cell_screen = bf.PygameSurface.refactor_size((800, 600), self.font)
        # Create the cell simulation.
        self.simulation = Simulation(self.cell_screen.size)
        # Create the island.
        points = bf.draw_circle((self.cell_screen.width / 2, self.cell_screen.height / 2), 24.5)
        for point in points:
            if self.cell_screen.cell_in_bounds(point):
                self.simulation.grid[point[0]][point[1]] = 1
        # Create the player.
        self.player_dir = (1, 0)
        self.player_pos = Vector2(self.cell_screen.width // 2, self.cell_screen.height // 2)
        # Draw everything for the first time.
        for x in range(self.simulation.size[0]):
            for y in range(self.simulation.size[1]):
                cell = self.simulation.grid[x][y]
                if cell == 0:
                    tile = WATER_TILE
                else:
                    tile = DIRT_TILE
                self.cell_screen.draw_cell((x, y), tile)
        self.cell_screen.draw_cell(vec_to_tuple(self.player_pos), PLAYER_TILES[self.player_dir])
        # Create other variables.
        self.clock = pg.time.Clock()
        self.debug = True
        self.debug_font = pg.font.Font(None, 24)

    def screenshot(self):
        """Save the main display surface to the screenshots folder."""
        # Get the name of the screenshot by current time.
        name = datetime.now().strftime("%a %b %d %Y %I.%M.%S %p.png")
        # Create path to screenshots directory.
        screenshot_path = Path() / 'screenshots'
        # If there is no screenshots directory, make it.
        if not screenshot_path.exists():
            screenshot_path.mkdir()
        # Save the main display surface to the screenshots directory.
        pg.image.save(self.screen, screenshot_path / name)
        # Record the screenshot.
        print(f'Saved screenshot: {name}')

    @staticmethod
    def terminate():
        """Quit pygame to be IDLE friendly and exit the program."""
        pg.quit()
        sys.exit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminate()

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F2:
                    self.screenshot()

                elif event.key == pg.K_UP:
                    self.move_player((0, -1))
                elif event.key == pg.K_DOWN:
                    self.move_player((0, 1))
                elif event.key == pg.K_LEFT:
                    self.move_player((-1, 0))
                elif event.key == pg.K_RIGHT:
                    self.move_player((1, 0))

                elif event.key == pg.K_z:
                    # Use the currently selected item.
                    pass
                elif event.key == pg.K_x:
                    # Open and close the inventory.
                    pass

    def move_player(self, direction: tuple[int, int]):
        """Move the player in the given direction, staying on the screen."""
        # Calculate the new position.
        new_pos = vec_to_tuple(self.player_pos + Vector2(direction))

        # Only update if the position is still on the screen.
        if self.cell_screen.cell_in_bounds(new_pos):
            # Update the old position.
            self.simulation.updates.add(vec_to_tuple(self.player_pos))
            # Save the new position and direction.
            self.player_pos = Vector2(new_pos)
            self.player_dir = direction
            # Draw the player.
            self.cell_screen.draw_cell(new_pos, PLAYER_TILES[self.player_dir])

    def update(self):
        """Update all structures and variables."""

    def draw_simulation_cell(self, point: tuple[int, int]):
        """Draw a single cell from the simulation to the screen."""
        # Draw the plant if present.
        if plant := self.simulation.pos_2_plant.get(point, False):
            self.cell_screen.draw_cell(point, plant.tile)
        # Draw the cell.
        else:
            cell = self.simulation.grid[point[0]][point[1]]
            if cell == 0:
                self.cell_screen.draw_cell(point, WATER_TILE)
            else:
                self.cell_screen.draw_cell(point, DIRT_TILE)

    def draw(self):
        """Draw the main display surface."""
        # Draw the simulation.
        for point in self.simulation.updates:
            self.draw_simulation_cell(point)
        # Clear the simulation update list.
        self.simulation.updates = set()

        # Update the surf.
        self.cell_screen.update(self.screen)
        # Show FPS.
        if self.debug:
            self.screen.blit(self.debug_font.render(f'{self.clock.get_fps():.2f}',
                                                    False, (255, 255, 255), (0, 0, 0)), (750, 580))
        # Tick clock for timing and flip the display.
        pg.display.flip()
        self.clock.tick()

    def run(self):
        """The function with the main loop of the application."""
        while True:
            self.events()
            self.update()
            self.draw()


def main():
    pg.init()
    pg.key.set_repeat(500, 100)
    Main().run()


if __name__ == "__main__":
    main()
