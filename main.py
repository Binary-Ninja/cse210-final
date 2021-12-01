#!/usr/bin/env python3

import sys
from datetime import datetime
from pathlib import Path

import pygame as pg

import bitfont as bf

from simulation import Simulation


class Main:
    def __init__(self):
        """Initialize the application."""
        # Create main screen.
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Cell Engine")
        # Create main cell screen.
        self.font = bf.Font(Path() / 'bitfont' / 'fonts' / 'CP437_8x8.png')
        self.cell_screen = bf.PygameSurface.refactor_size((800, 600), self.font)
        # Create the cell simulation.
        self.simulation = Simulation(self.cell_screen.size)
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
                elif event.key == pg.K_SPACE:
                    self.simulation.update_one_action()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.simulation.toggle_wall(self.cell_screen.get_cell_pos(event.pos))
            elif event.type == pg.MOUSEMOTION:
                if pg.mouse.get_pressed()[0]:
                    self.simulation.toggle_wall(self.cell_screen.get_cell_pos(event.pos))

    def update(self):
        """Update all structures and variables."""

    def draw_simulation_cell(self, point: tuple[int, int]):
        """Draw a single cell from the simulation to the screen."""
        if self.simulation.grid[point[0]][point[1]]:
            self.cell_screen.draw_cell(point, (None, None, (128, 128, 128)))
        else:
            self.cell_screen.draw_cell(point, (None, None, (0, 0, 0)))

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
    Main().run()


if __name__ == "__main__":
    main()
