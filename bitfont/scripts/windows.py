#!/usr/bin/env python3

"""Window classes."""

from pathlib import Path

from surface import Surface


class WindowManager:
    def __init__(self, app):
        self.app = app
        self.windows = []

    def draw(self):
        for window in self.windows:
            window.draw(self.app.cell_screen)

    def mouse_over(self, pos):
        for window in self.windows:
            window.mouse_over(pos)

    def click(self):
        for window in self.windows:
            window.click()


class MenuBar:
    def __init__(self, master, buttons):
        self.master = master
        self.menu_bar_buttons = []
        button_pos = 0
        for text in buttons:
            self.menu_bar_buttons.append(Button((button_pos, 0), text))
            button_pos += len(text) + 1

    def draw(self, screen):
        screen.fill((None, None, (64, 64, 64)), (0, 0, screen.width, 1))
        for button in self.menu_bar_buttons:
            button.draw(screen)

    def mouse_over(self, pos):
        for button in self.menu_bar_buttons:
            button.mouse_over(pos)

    def click(self):
        pass


class MenuDropDown:
    def __init__(self, master, buttons):
        self.master = master
        self.buttons = []
        button_pos = 1
        for text in buttons:
            self.buttons.append(Button((0, button_pos), text))
            button_pos += 1

    def draw(self, screen):
        screen.fill((None, None, (64, 64, 64)), (0, 1, 14, len(self.buttons)))
        for button in self.buttons:
            button.draw(screen)

    def mouse_over(self, pos):
        for button in self.buttons:
            button.mouse_over(pos)

    def click(self):
        for button in self.buttons:
            button.click()


class Button:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
        self.hovered = False
        self.cell = (None, None, (64, 64, 64))

    def draw(self, screen):
        screen.write_cells(bytes(self.text, 'utf-8'), self.pos, self.cell)

    def mouse_over(self, pos):
        self.hovered = self.pos[0] <= pos[0] < self.pos[0] + len(self.text) and self.pos[1] <= pos[1] < self.pos[1] + 1
        if self.hovered:
            self.cell = (None, None, (170, 170, 170))
        else:
            self.cell = (None, None, (64, 64, 64))

    def click(self):
        if self.hovered:
            print(self.text)


class Tab:
    def __init__(self, path: Path = None):
        self.path = path
        size = (32, 32)
        if self.path is None:
            size = (32, 32)
        self.surface = Surface(size)
        self.surface.fill((0x23, None, None))
        self.offset = (0, 0)

    def draw(self, screen):
        screen.blit(self.surface, (0, 2))
