# Created on 27 January 2020
# Created by

import pygame as pg
from pygame.locals import RESIZABLE

MIN_W = screen_w = 500
lvlDriver = None


def resize(w, h):
    global screen_w
    dw, dh = abs(w - screen_w), abs(h - screen_w)
    if dw >= dh:
        screen_w = min(w, MIN_W)
    else:
        screen_w = min(h, MIN_W)
    pg.display.set_mode((screen_w, screen_w), RESIZABLE)
    # TODO: resize towers, enemies, projectile, and screen


# Gets the biggest font that fits the text within max_w and max_h
def get_scaled_font(max_w, max_h, text, font_name="Times New Roman"):
    font_size = 0
    font = pg.font.SysFont(font_name, font_size)
    w, h = font.size(text)
    while (max_w == -1 or w < max_w) and (max_h == -1 or h < max_h):
        font_size += 1
        font = pg.font.SysFont(font_name, font_size)
        w, h = font.size(text)
    return pg.font.SysFont(font_name, font_size - 1)


def get_widest_string(strs, font_type="Times New Roman"):
    biggest = ""
    last_w = 0
    font = pg.font.SysFont(font_type, 12)
    for s in strs:
        if font.size(s)[0] > last_w:
            biggest = s
            last_w = font.size(s)[0]
    return biggest
