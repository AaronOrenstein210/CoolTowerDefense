# Created on 27 January 2020
# Created by

import math
import pygame as pg
from pygame.locals import RESIZABLE

TWO_PI = 2 * math.pi

MIN_W = screen_w = 500
LEVELS = "saves/levels.bin"
SPAWNS = "saves/spawn_lists.bin"
# Offsets needed to keep the game screen square
off_x, off_y = 0, 0
lvlDriver = None
enemies, towers = {}, {}


def init():
    from inspect import getmembers, isclass
    from LevelDriver import LevelDriver
    global lvlDriver
    lvlDriver = LevelDriver()

    if "MyLevelDriver.LevelDriver" in str(LevelDriver):
        import MyObjects
        global enemies, towers
        # Compile a list of enemies and towers
        enemies.clear()
        towers.clear()
        for name, obj in getmembers(MyObjects):
            if isclass(obj):
                if "MyObjects" in str(obj):
                    # Add Constructor to list
                    if "Enemy" in str(obj):
                        enemies[obj().idx] = obj
                    elif "Tower" in str(obj):
                        towers[obj().idx] = obj


# Resizes screen
# @param resize_driver boolean tells whether to resize the level driver or not
def resize(w, h, resize_driver):
    global screen_w, off_x, off_y
    if w >= h:
        screen_w = h
        off_x = (w - h) // 2
        off_y = 0
    else:
        screen_w = w
        off_x = 0
        off_y = (h - w) // 2
    pg.display.set_mode((w, h), RESIZABLE)
    if resize_driver:
        lvlDriver.lr.draw_surface()
        for i in lvlDriver.enemies + lvlDriver.towers + lvlDriver.projectiles:
            img_dim = (int(i.dim[0] * screen_w), int(i.dim[1] * screen_w))
            i.img = pg.transform.scale(i.img, img_dim)
            i.blit_img = pg.transform.rotate(i.img, i.angle)


# Resizes surface to fit within desired dimensions, keeping surface's w:h ratio
def scale_to_fit(s, w=-1, h=-1):
    import pygame as pg
    if w == -1 and h == -1:
        return s
    dim = s.get_size()
    if w == -1:
        frac = h / dim[1]
    elif h == -1:
        frac = w / dim[0]
    else:
        frac = min(w / dim[0], h / dim[1])
    return pg.transform.scale(s, (int(frac * dim[0]), int(frac * dim[1])))


# Returns mouse position in relation to the game screen
def get_mouse_pos():
    pos = pg.mouse.get_pos()
    return [pos[0] - off_x, pos[1] - off_y]


# Tools
# Gets the angle from p1 to p2, which are points in PIXEL coordinates
def get_angle_pixels(p1, p2):
    dx = p2[0] - p1[0]
    # Negative to account for flipped pixel coords
    dy = -(p2[1] - p1[1])
    r = math.sqrt(dx * dx + dy * dy)
    if r == 0:
        return 0
    theta = math.asin(dy / r)
    if dx < 0:
        theta = math.pi - theta
    return theta % TWO_PI


# Returns distance between two points
def get_distance(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)


# Gets the biggest font size that fits the text within max_w and max_h
def get_scaled_font(max_w, max_h, text, font_name="Times New Roman"):
    font_size = 1
    font = pg.font.SysFont(font_name, font_size)
    w, h = font.size(text)
    min_size = max_size = 1
    while (max_w == -1 or w < max_w) and (max_h == -1 or h < max_h):
        font_size *= 2
        min_size = max_size
        max_size = font_size
        font = pg.font.SysFont(font_name, font_size)
        w, h = font.size(text)
    if font_size == 1:
        return font
    while True:
        font_size = (max_size + min_size) // 2
        font = pg.font.SysFont(font_name, font_size)
        w, h = font.size(text)
        # Too small
        if (max_w == -1 or w < max_w) and (max_h == -1 or h < max_h):
            # Check if the next size is too big
            font_ = pg.font.SysFont(font_name, font_size + 1)
            w, h = font_.size(text)
            if (max_w == -1 or w < max_w) and (max_h == -1 or h < max_h):
                min_size = font_size + 1
            else:
                return font
        # Too big
        else:
            # Check if the previous size is too small
            font_ = pg.font.SysFont(font_name, font_size - 1)
            w, h = font_.size(text)
            if (max_w == -1 or w < max_w) and (max_h == -1 or h < max_h):
                return font
            else:
                max_size = font_size - 1


def get_widest_string(strs, font_type="Times New Roman"):
    biggest = ""
    last_w = 0
    font = pg.font.SysFont(font_type, 12)
    for s in strs:
        if font.size(s)[0] > last_w:
            biggest = s
            last_w = font.size(s)[0]
    return biggest
