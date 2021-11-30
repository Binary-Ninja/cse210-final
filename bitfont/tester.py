#!/usr/bin/env python3

"""Script for testing various features of the bitfont module."""

import sys
from pathlib import Path

import pygame as pg

from font import Font
from surface import PygameSurface, Surface
from draw import *


def main():
    pg.init()
    screen = pg.display.set_mode((256, 256), pg.RESIZABLE)
    fonts = (Font(Path() / 'fonts' / 'CP437_8x8.png'),
             Font(Path() / 'fonts' / 'CP437_12x12.png'))
    font_index = 0
    bfont = fonts[font_index]
    pgsurf = PygameSurface.refactor_size((256, 256), bfont)
    # testing stuff
    # surf 1
    surf1 = Surface((8, 8))
    surf1.fill((0xb0, None, None))
    # surf 2
    surf2 = Surface((4, 4))
    surf2.fill((0xb1, None, None))
    surf2.draw_cell((0, 0), (None, (255, 0, 0), None))
    surf2.draw_cell((0, 3), (None, (255, 255, 0), None))
    surf2.draw_cell((3, 0), (None, (0, 0, 255), None))
    surf2.draw_cell((3, 3), (None, (0, 255, 0), None))
    # the blitting
    surf1.blit2(surf2, (0, 0), (2, 2, 2, 2))
    pgsurf.blit(surf1, (0, 0))
    # surf2.blit(surf1, (1, 1))
    # pgsurf.blit(surf2, (0, 0))
    # points = set()
    clock = pg.time.Clock()
    font = pg.font.Font(None, 24)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_SPACE:
                    font_index += 1
                    font_index %= len(fonts)
                    bfont = fonts[font_index]
                    pgsurf = pgsurf.refactor_size(screen.get_size(), bfont)
            elif event.type == pg.MOUSEMOTION:
                pass
                # pgsurf.draw_cells(points, (0x0, (255, 255, 255), (0, 0, 0)))
                # points = dda_line((0, 0), pgsurf.get_cell_pos(event.pos))
                # pgsurf.draw_cells(points, (0x26, (2, 2, 2), (128, 128, 128)))
            elif event.type == pg.VIDEORESIZE:
                pgsurf = pgsurf.refactor_size(event.size, bfont)
        # Update the surf.
        pgsurf.update(screen)
        # Show FPS.
        screen.blit(font.render(f'{clock.get_fps():.2f}', False, (255, 255, 255), (0, 0, 0)), (0, 128))
        # Tick clock for timing and flip the display.
        clock.tick()
        pg.display.flip()


main()
