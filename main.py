#!/usr/bin/env python3

# Description:
#   The following class Main is used as the main application class.
#   It isn't really needed, but I like it.
#
# OOP Principles Used:
#   Abstraction and Encapsulation
#
# Reasoning:
#   This class uses encapsulation because it contains both game variables and functions.
#   This class uses abstraction because running the game is as easy as calling Main.run().

import sys
from datetime import datetime
from pathlib import Path

import pygame as pg
from pygame.math import Vector2

import bitfont as bf

from simulation import Simulation, vec_to_tuple, PLAYER_TILES, GRID_TILES
from inventory import *


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
        # Create the lake.
        points = bf.draw_circle((self.cell_screen.width / 2, self.cell_screen.height / 2), 10.5)
        for point in points:
            if self.cell_screen.cell_in_bounds(point):
                self.simulation.grid[point[0]][point[1]] = 0

        # Create the player.
        self.player_dir = (1, 0)
        self.player_pos = Vector2(self.cell_screen.width // 2, self.cell_screen.height // 2)
        self.player_inventory: list[Item] = [Item(HOE), Item(WATERING_CAN_EMPTY)]
        for seed_data in ALL_SEEDS:
            self.player_inventory.append(Seed(*seed_data, count=10))
        self.current_item = 0

        # Draw everything for the first time.
        self.draw_play()

        # Create other variables.
        self.inventory = False
        self.colors = False
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
                if event.key == pg.K_F1:
                    self.debug = not self.debug
                elif event.key == pg.K_F2:
                    self.screenshot()

                elif event.key == pg.K_SPACE:
                    # Advance time.
                    self.simulation.update_ticks()

                elif event.key == pg.K_UP:
                    self.movement_key((0, -1), -1)
                elif event.key == pg.K_DOWN:
                    self.movement_key((0, 1), 1)
                elif event.key == pg.K_LEFT:
                    self.movement_key((-1, 0), -1)
                elif event.key == pg.K_RIGHT:
                    self.movement_key((1, 0), 1)

                elif event.key == pg.K_z:
                    self.handle_action_key()

                elif event.key == pg.K_x:
                    # Open and close the inventory.
                    self.inventory = not self.inventory

                    if self.inventory:
                        self.draw_inventory()
                    else:
                        self.draw_play()

                elif event.key == pg.K_c:
                    # Toggle showing the plant statuses.
                    self.colors = not self.colors
                    # Mark all plants for update.
                    for pos in self.simulation.plants:
                        self.simulation.updates.add(pos)

    def handle_action_key(self):
        """Handles all the action key logic."""
        # If in the inventory screen, exit it.
        if self.inventory:
            self.inventory = False
            self.draw_play()
        # Use the currently selected item.
        else:
            # Get the affected tile's position.
            tile_pos = vec_to_tuple(self.player_pos + Vector2(self.player_dir))
            # Only perform an action if the position is on the screen.
            if not self.cell_screen.cell_in_bounds(tile_pos):
                return

            item = self.player_inventory[self.current_item]

            if isinstance(item, Seed):
                # Make sure the space is clear.
                if not self.simulation.plants.get(tile_pos, None):
                    # Make sure the plant can be placed here.
                    if self.simulation.grid[tile_pos[0]][tile_pos[1]] in item.valid_tiles:
                        # Create a new plant.
                        self.simulation.add_plant(tile_pos, *item)
                        # Redraw the tiles that were covered by the previous display.
                        self.clear_current_item()
                        # Decrement the seed count.
                        item.count -= 1
                        # Delete the stack.
                        if item.count == 0:
                            del self.player_inventory[self.current_item]
                            self.current_item = 0

            elif item.name == HOE:
                # Harvest the plant.
                if plant := self.simulation.plants.get(tile_pos, None):
                    # Make the stacks stack nicely.
                    for item in self.player_inventory:
                        if item.name == plant.name:
                            item.count += 4 if plant.done_growing else 1
                            break
                    else:
                        self.player_inventory.append(Seed(*plant, count=4 if plant.done_growing else 1))
                    # Remove the plant.
                    self.simulation.remove_plant(plant)
                # Toggle dirt and farmland.
                else:
                    tile = self.simulation.grid[tile_pos[0]][tile_pos[1]]
                    if tile == 1:
                        self.simulation.grid[tile_pos[0]][tile_pos[1]] = 2
                    elif tile == 2:
                        self.simulation.grid[tile_pos[0]][tile_pos[1]] = 1
                    # Update the position.
                    self.simulation.updates.add(tile_pos)

            elif item.name == WATERING_CAN_EMPTY:
                # Fill the bucket.
                if self.simulation.grid[tile_pos[0]][tile_pos[1]] == 0:
                    # Redraw the tiles that were covered by the previous display.
                    self.clear_current_item()
                    # Remove the empty watering can.
                    del self.player_inventory[self.current_item]
                    # Add the full watering can.
                    self.player_inventory.insert(self.current_item, Item(WATERING_CAN_FULL))

            elif item.name == WATERING_CAN_FULL:
                # Water plants.
                if plant := self.simulation.plants.get(tile_pos, None):
                    # Free the plant to continue growing.
                    plant.needs_water = False
                    # Redraw the tiles that were covered by the previous display.
                    self.clear_current_item()
                    # Update for color status.
                    self.simulation.updates.add(tile_pos)
                    # Remove the full watering can.
                    del self.player_inventory[self.current_item]
                    # Add the empty watering can.
                    self.player_inventory.insert(self.current_item, Item(WATERING_CAN_EMPTY))

            # Advance time.
            self.simulation.update_ticks()

    def movement_key(self, pos_dir: tuple[int, int], inv_dir: int):
        """Handle the movement keys."""
        if self.inventory:
            self.move_inventory(inv_dir)
        else:
            self.move_player(pos_dir)

    def move_player(self, direction: tuple[int, int]):
        """Move the player in the given direction, staying on the screen."""
        # Calculate the new position.
        new_pos = vec_to_tuple(self.player_pos + Vector2(direction))

        # Only update if the position is on the screen.
        if self.cell_screen.cell_in_bounds(new_pos):
            # Update the old position.
            self.simulation.updates.add(vec_to_tuple(self.player_pos))
            # Save the new position and direction.
            self.player_pos = Vector2(new_pos)
            self.player_dir = direction
            # Draw the player.
            self.cell_screen.draw_cell(new_pos, PLAYER_TILES[self.player_dir])
            # Advance time.
            self.simulation.update_ticks()

    def move_inventory(self, direction: int):
        """Move the inventory cursor up and down, wrapping around."""
        self.current_item += direction
        self.current_item %= len(self.player_inventory)
        self.draw_inventory()

    def update(self):
        """Update all structures and variables."""

    def draw_play(self):
        """Draw the whole playing scene."""
        # Draw the world.
        for x in range(self.simulation.size[0]):
            for y in range(self.simulation.size[1]):
                self.cell_screen.draw_cell((x, y), GRID_TILES[self.simulation.grid[x][y]])
        # Draw the plants.
        for pos, plant in self.simulation.plants.items():
            status = None
            if self.colors:
                if plant.needs_water:
                    status = (0, 0, 255)
                if plant.done_growing:
                    status = (0, 255, 0)
            self.cell_screen.draw_cell(pos, (plant.tile[0], plant.tile[1], status))
        # Draw the player.
        self.cell_screen.draw_cell(vec_to_tuple(self.player_pos), PLAYER_TILES[self.player_dir])

    def clear_current_item(self):
        """Redraws the cells under the current item display."""
        # Redraw the tiles that were covered by the previous display.
        for x in range(len(self.player_inventory[self.current_item])):
            self.simulation.updates.add((x, 0))

    def draw_current_item(self):
        """Draw the currently selected item."""
        self.cell_screen.write_cells(bytes(self.player_inventory[self.current_item].get_name(), "utf8"),
                                     (0, 0), (None, (255, 255, 255), (0, 0, 0)))

    def draw_inventory(self):
        """Draw the inventory."""
        # Draw a black box sized for the inventory screen.
        points = bf.draw.draw_rect((0, 0, len(max(self.player_inventory, key=lambda x: len(x))) + 2,
                                    len(self.player_inventory)), True)
        self.cell_screen.draw_cells(points, (0, None, (0, 0, 0)))
        # Draw all the items.
        for index, item in enumerate(self.player_inventory):
            color = (128, 128, 128)
            if index == self.current_item:
                color = (255, 255, 255)
            self.cell_screen.write_cells(bytes(f"  {item.get_name()}", "utf8"),
                                         (0, index), (0, color, None))
        # Draw the currently selected item.
        self.cell_screen.draw_cell((0, self.current_item), (0x10, (255, 255, 255), None))

    def draw_simulation_cell(self, point: tuple[int, int]):
        """Draw a single cell from the simulation to the screen."""
        # Draw the plant if present.
        if plant := self.simulation.plants.get(point, None):
            status = (0, 0, 0)
            if self.colors:
                if plant.needs_water:
                    status = (0, 0, 255)
                if plant.done_growing:
                    status = (0, 255, 0)
            self.cell_screen.draw_cell(point, (plant.tile[0], plant.tile[1], status))
        # Draw the cell.
        else:
            self.cell_screen.draw_cell(point, GRID_TILES[self.simulation.grid[point[0]][point[1]]])

    def draw(self):
        """Draw the main display surface."""
        # Draw the simulation.
        for point in self.simulation.updates:
            self.draw_simulation_cell(point)
        # Clear the simulation update list.
        self.simulation.updates = set()

        # Draw the windows.
        if not self.inventory:
            self.draw_current_item()

        # Update the surf.
        self.cell_screen.update(self.screen)
        # Show FPS.
        if self.debug:
            self.screen.blit(self.debug_font.render(f'{self.clock.get_fps():.2f}',
                                                    False, (255, 255, 255), (0, 0, 0)), (750, 585))
            self.screen.blit(self.debug_font.render(f'T: {self.simulation.global_time}',
                                                    False, (255, 255, 255), (0, 0, 0)), (0, 585))
            self.screen.blit(self.debug_font.render(f'C: {int(self.colors)}',
                                                    False, (255, 255, 255), (0, 0, 0)), (0, 570))
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
