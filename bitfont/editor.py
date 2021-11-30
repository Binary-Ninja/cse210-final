#!/usr/bin/env python3

"""Editor for the bitfont module."""

# Standard library imports.
import sys
from datetime import datetime
from pathlib import Path

# Third party imports.
import pygame as pg

# Local library imports.
from font import Font
from surface import PygameSurface, Surface
from scripts import *


class Main:
    def __init__(self):
        """Initializes the application, creates display, loads files, etc."""
        # Load in the preferences.
        self.preferences = PreferenceManager()
        # Create main display surface.
        self.screen = pg.display.set_mode(self.preferences["Resolution"], pg.RESIZABLE)
        pg.display.set_caption(f"Bitfont Editor v{self.preferences['Version']}")
        # Load and create cell font.
        font_dir = Path() / "fonts"
        if not font_dir.exists():
            raise FileNotFoundError("No 'fonts' directory found.")
        self.cell_font = Font(font_dir / self.preferences["Font"])
        # Create the main cell surface.
        self.cell_screen = PygameSurface.refactor_size(pg.display.get_window_size(), self.cell_font)
        # Make menu bar.
        self.menu_buttons = []
        button_pos = 0
        for text in self.preferences["MenuBar"]:
            self.menu_buttons.append(Button((button_pos, 0), text))
            button_pos += len(text) + 1
        # Draw menu bar.
        self.cell_screen.fill((None, None, (64, 64, 64)), (0, 0, self.cell_screen.width, 1))
        for button in self.menu_buttons:
            button.draw(self.cell_screen)
        # Create new tab.
        self.tab = Tab()
        self.tab_surface = Surface((16, self.cell_screen.height - 2))
        self.draw_tab()
        # Create the debug font.
        self.font = pg.font.Font(None, 24)
        # Create clock for timings.
        self.clock = pg.time.Clock()
        # Create log.
        self.log = [datetime.now().strftime("Program started: %a %b %d %Y %I.%M.%S %p.\n")]
        # Other variables.
        self.debug = True

    def update_size(self, size):
        """Resize the main cell screen to fit in new pixel dimensions."""
        # Resize the screen.
        self.cell_screen = PygameSurface.refactor_size(size, self.cell_font)
        # Redraw everything.
        self.cell_screen.fill((None, None, (64, 64, 64)), (0, 0, self.cell_screen.width, 1))
        for button in self.menu_buttons:
            button.draw(self.cell_screen)

    def draw_tab(self):
        self.tab_surface.fill((0x0, (255, 255, 255), (0, 0, 0)))
        self.cell_screen.fill((0xBA, None, None), (16, 0, 1, self.cell_screen.height))
        self.tab_surface.blit(self.tab.surface, self.tab.offset)
        self.cell_screen.blit(self.tab_surface, (0, 2))

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
        self.log.append(f'Saved screenshot: {name}')
        print(f'Saved screenshot: {name}')

    def log_data(self):
        """Open or create the log file and log all program data."""
        # Log the end of the program.
        self.log.append(datetime.now().strftime("\nProgram ended: %a %b %d %Y %I.%M.%S %p."))
        # Write each log line to the log.
        with open('log.txt', 'w') as file:
            for line in self.log:
                file.write(line + '\n')

    def terminate(self):
        """Quit pygame to be IDLE friendly, log data, and exit the program."""
        pg.quit()
        self.log_data()
        sys.exit()

    def events(self):
        """Capture all events and handle them properly."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.terminate()
            elif event.type == pg.VIDEORESIZE:
                self.update_size(event.size)
            elif event.type == pg.MOUSEMOTION:
                cell_pos = self.cell_screen.get_cell_pos(event.pos)
                self.cell_screen.fill((None, None, (64, 64, 64)), (0, 0, self.cell_screen.width, 1))
                for button in self.menu_buttons:
                    button.mouse_over(cell_pos)
                    button.draw(self.cell_screen)
            elif event.type == pg.MOUSEBUTTONDOWN:
                for button in self.menu_buttons:
                    if button.hovered:
                        print(button.text)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_F2:
                    self.screenshot()

    def update(self):
        """Update all structures and variables."""

    def draw(self):
        """Draw the main display surface."""
        # Draw all changed cells to main screen.
        self.cell_screen.update(self.screen)
        # Draw the debug.
        if self.debug:
            self.screen.blit(self.font.render(f"{self.clock.get_fps():.2f}", False, (255, 255, 255), (0, 0, 0)),
                             (0, self.screen.get_height() - 20))
        # Tick the clock and flip the display.
        self.clock.tick(self.preferences["FPS"])
        pg.display.flip()

    def run(self):
        """The function with the main loop of the application."""
        while True:
            self.events()
            self.update()
            self.draw()


def main():
    """Main function for the program, runs the editor and catches crashes."""
    pg.init()
    m = Main()
    try:
        m.run()
    except Exception as ex:
        m.log.append(f'FATAL ERROR: {ex}')
        m.log_data()
        raise ex


# Run the editor.
if __name__ == '__main__':
    main()
