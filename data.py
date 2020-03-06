# Created on 27 January 2020
# Created by Nerd

import math
import pygame as pg
from pygame.locals import RESIZABLE

TWO_PI = 2 * math.pi

MIN_W = screen_w = 500
LEVELS = "saves/levels.bin"
WAVES = "saves/waves.bin"
# Offsets needed to keep the game screen square
off_x, off_y = 0, 0
lvlDriver = None
enemies, towers = {}, {}
shoot_audio = hit_audio = music_audio = None


def init():
    from inspect import getmembers, isclass
    from Game.LevelDriver import LevelDriver
    global lvlDriver
    lvlDriver = LevelDriver()

    global enemies, towers
    # Compile a list of enemies and towers
    enemies.clear()
    towers.clear()
    from Game import Enemy
    from Game import Tower
    for name, obj in getmembers(Enemy):
        if isclass(obj):
            if "Enemy." in str(obj):
                inst = obj()
                enemies[inst.idx] = inst
    for name, obj in getmembers(Tower):
        if isclass(obj):
            if "Tower." in str(obj):
                inst = obj()
                towers[inst.idx] = inst

    global shoot_audio, hit_audio, music_audio
    shoot_audio = pg.mixer.Sound("res/laser.wav")
    hit_audio = pg.mixer.Sound("res/hit.wav")
    music_audio = pg.mixer.Sound("res/duck_song.wav")


# Resizes screen
# playing tells whether we are playing the game or not
def resize(w, h, playing):
    global screen_w, off_x, off_y
    if w >= h:
        off_x = (w - h) // 2
        off_y = 0
    else:
        off_x = 0
        off_y = (h - w) // 2
    w, h = max(w, 500), max(h, 500)
    pg.display.set_mode((w, h), RESIZABLE)
    calculate_dimensions(playing)


# Calculates screen offsets and width based on if we are playing or not
def calculate_dimensions(playing):
    global screen_w, off_x, off_y
    w, h = pg.display.get_surface().get_size()
    if not playing:
        screen_w = min(w, h)
        off_x = (w - screen_w) // 2
        off_y = (h - screen_w) // 2
    else:
        if w * 5 // 6 >= h:
            screen_w = h
            off_x = (w - screen_w * 6 / 5) // 2
            off_y = 0
        else:
            screen_w = w * 5 // 6
            off_x = 0
            off_y = (h - screen_w) // 2


# Resizes surface to fit within desired dimensions, keeping surface's w:h ratio
def scale_to_fit(s, w=-1, h=-1):
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


# Breaks text into the minimum number of lines needed to display it
# Divides text into words with ' ' delimiter
def wrap_text(string, font, w):
    words = string.split(" ")
    strs = []
    line = ""
    i = 0
    # Go through each word
    while i < len(words):
        # Get the new line and check its width
        temp = line + (" " if line != "" else "") + words[i]
        # If it fits, go to the next word
        if font.size(temp)[0] < w:
            line = temp
            i += 1
        # If it doesn't and our line has other words, add the line
        elif line != "":
            strs.append(line)
            line = ""
        # Otherwise the word doesn't fit in one line so break it up
        else:
            wrap = wrap_string(temp, font, w)
            for text in wrap[:-1]:
                strs.append(text)
            if i < len(words) - 1:
                line = wrap[len(wrap) - 1]
            else:
                strs.append(wrap[len(wrap) - 1])
            i += 1
    strs.append(line)
    return strs


def wrap_string(string, font, w):
    strs = []
    text = ""
    for char in string:
        if font.size(text + char)[0] >= w:
            strs.append(text)
            text = ""
        text += char
    return strs
