# Created on 27 January 2020
# Created by

import pygame as pg
from pygame.locals import RESIZABLE

MIN_W = 500
lvlDriver = None


def resize(w, h):
    w_ = pg.display.get_surface().get_size()[0]
    dw, dh = abs(w - w_), abs(h - w_)
    if dw >= dh:
        w_ = min(w, MIN_W)
    else:
        w_ = min(h, MIN_W)
    pg.display.set_mode((w_, w_), RESIZABLE)
    # TODO: resize towers, enemies, projectile, and screen
