# Created on 27 January 2020
# Created by

import pygame as pg
from pygame.locals import *
import data
import LevelReader as reader

pg.init()
pg.display.set_mode((data.MIN_W, data.MIN_W), RESIZABLE)


# Start playing a new level
def start_level():
    pass


# Opens main screen
def main_screen():
    new, choose = 1, 0
    rects = [None, None]

    def draw():
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        half_w = data.screen_w // 2
        text = ["Select a Level", "Create a new Level"]
        font = data.get_scaled_font(data.screen_w, half_w, data.get_widest_string(text, "Times New Roman"),
                                    "Times New Roman")
        text_s = font.render(text[0], 1, (255, 255, 255))
        rects[choose] = text_s.get_rect(centerx=half_w, bottom=half_w)
        d.blit(text_s, rects[choose])
        text_s = font.render(text[1], 1, (255, 255, 255))
        rects[new] = text_s.get_rect(centerx=half_w, top=half_w)
        d.blit(text_s, rects[new])

    draw()
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                exit(0)
            elif e.type == RESIZABLE:
                data.resize(e.w, e.h)
                draw()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                pos = pg.mouse.get_pos()
                if rects[choose].collidepoint(*pos):
                    return choose_level()
                elif rects[new].collidepoint(*pos):
                    new_level()
        pg.display.flip()


# Opens choose level screen
def choose_level():
    print("Choose Level")


# Opens create a level screen
def new_level():
    paths = [reader.Line()]
    paths[0].end = [1, 1]
    selected = ""
    types = ["Line", "Circle"]
    rects = {"Editor": None}
    for t in types:
        rects[t] = None

    def draw():
        draw_options()
        draw_editor()

    def draw_options():
        d = pg.display.get_surface()
        side_w = data.screen_w // 5
        item_h = data.screen_w // len(types)
        font = data.get_scaled_font(side_w, item_h, data.get_widest_string(types))
        d.fill((128, 128, 128), (0, 0, side_w, data.screen_w))
        for i, t_ in enumerate(types):
            rects[t_] = pg.Rect(0, i * item_h, side_w, item_h)
            text = font.render(t_, 1, (0, 0, 0))
            text_rect = text.get_rect(center=(side_w // 2, int(item_h * (i + .5))))
            d.blit(text, text_rect)
            if t_ == selected:
                pg.draw.rect(d, (175, 175, 0), (rects[t_]), 5)

    def draw_editor():
        d = pg.display.get_surface()
        off = data.screen_w // 5
        for p in paths:
            if p.idx == reader.LINE:
                start = [i * data.screen_w + off for i in p.start]
                end = [i * data.screen_w + off for i in p.end]
                pg.draw.line(d, (255, 255, 255), start, end, 5)
            elif p.idx == reader.CIRCLE:
                pg.draw.circle(d, (255, 255, 255), p.center, p.radius, 5)

    draw()

    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                exit(0)
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h)
                draw()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                pos = pg.mouse.get_pos()
        pg.display.flip()


main_screen()
