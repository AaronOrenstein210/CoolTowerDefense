# Created on 27 January 2020
# Created by

from os.path import isfile
import math
import pygame as pg
from pygame.locals import *
import data
from LevelReader import *
from MyLevelDriver import LevelDriver

pg.init()
data.lvlDriver = LevelDriver()
pg.display.set_mode((data.MIN_W, data.MIN_W), RESIZABLE)


# Runs current level
def run_level():
    time = pg.time.get_ticks()
    while True:
        dt = pg.time.get_ticks() - time
        time += dt
        for e in pg.event.get():
            if e.type == QUIT:
                return
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, True)
        data.lvlDriver.tick(dt)
        pg.display.flip()


# Runs main screen
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
        rects[choose] = text_s.get_rect(centerx=half_w + data.off_x, bottom=half_w + data.off_y)
        d.blit(text_s, rects[choose])
        text_s = font.render(text[1], 1, (255, 255, 255))
        rects[new] = text_s.get_rect(centerx=half_w + data.off_x, top=half_w + data.off_y)
        d.blit(text_s, rects[new])

    draw()
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                return
            elif e.type == RESIZABLE:
                data.resize(e.w, e.h, False)
                draw()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                pos = pg.mouse.get_pos()
                if rects[choose].collidepoint(*pos):
                    while choose_level():
                        run_level()
                    draw()
                elif rects[new].collidepoint(*pos):
                    new_level()
                    draw()
        pg.display.flip()


# Runs level selection screen
def choose_level():
    # Load all levels
    levels = []
    if isfile("custom_levels.bin"):
        with open("custom_levels.bin", 'rb') as file:
            file_data = file.read()
        # Loop through the data
        while len(file_data) > 0:
            # Get the number of paths for this level
            num_paths = int.from_bytes(file_data[0:1], byteorder)
            byte_pos = 1
            # Get data for each path
            for i in range(num_paths):
                # Make sure the path data is there
                if len(file_data) == 0:
                    print("Missing path data")
                    break
                else:
                    # Get path type
                    path_type = int.from_bytes(file_data[byte_pos:byte_pos + 1], byteorder)
                    byte_pos += 1
                    # Make sure path type is valid
                    if path_type in constructors.keys():
                        # Get path data and make sure it exists
                        num_bytes = constructors[path_type]().num_bytes
                        if len(file_data) < num_bytes:
                            print("Missing path data")
                            break
                        else:
                            byte_pos += num_bytes
                    else:
                        print("Unknown path type")
                        break
            levels.append(file_data[1:byte_pos])
            file_data = file_data[byte_pos:]

    row_len = 10

    def draw():
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        lvl_w = data.screen_w // row_len
        back_img = pg.transform.scale(pg.image.load("back.png"), (lvl_w, lvl_w))
        digit_w = lvl_w // 5
        font = data.get_scaled_font(digit_w * 3, digit_w * 3, "0")
        numbers = []
        for num in range(9):
            numbers.append(font.render(str(num), 1, (255, 255, 255)))
        for j in range(len(levels)):
            row, col = j // row_len, j % row_len
            d.blit(back_img, (col * lvl_w + data.off_x, row * lvl_w + data.off_y, row_len, row_len))
            j += 1
            digits = len(str(j))
            for k, val in enumerate(str(j)):
                center = [int(lvl_w * (col + .5)) + data.off_x, int(lvl_w * (row + .5)) + data.off_y]
                if digits == 2:
                    center[0] += k - 1.5
                elif digits == 3:
                    center[0] += (k - 2) * 1.5
                d.blit(numbers[int(val)], numbers[int(val)].get_rect(center=center))

    draw()
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                return False
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, False)
                draw()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                pos = data.get_mouse_pos()
                item_w = data.screen_w // row_len
                idx = (pos[0] // item_w) + (pos[1] // item_w) * 10
                if idx < len(levels):
                    data.lvlDriver.lr.load_from_bytes(levels[idx])
                    return True
        pg.display.flip()


# Runs level creator
def new_level():
    # Start with spots for start and end
    paths = []
    selected, current = "Start", Start()
    types = ["Start", "Line", "Circle", "Save & Exit"]
    rect = pg.Rect(0, 0, 0, 0)

    def draw():
        pg.display.get_surface().fill((0, 0, 0))
        side_w = data.screen_w // 5
        rect.topleft = [side_w, side_w // 2]
        rect.size = [data.screen_w - side_w] * 2
        pg.display.get_surface().blit(draw_paths(rect, paths + [current]),
                                      (rect.x + data.off_x, rect.y + data.off_y))
        draw_options()

    def draw_options():
        d = pg.display.get_surface()
        side_w = data.screen_w // 5
        item_h = data.screen_w // len(types)
        font = data.get_scaled_font(side_w, item_h, data.get_widest_string(types))
        d.fill((128, 128, 128), (data.off_x, data.off_y, side_w, data.screen_w))
        for i, t_ in enumerate(types):
            text = font.render(t_, 1, (0, 0, 0))
            text_rect = text.get_rect(center=(side_w // 2 + data.off_x, int(item_h * (i + .5)) + data.off_y))
            d.blit(text, text_rect)
            if t_ == selected:
                pg.draw.rect(d, (175, 175, 0), (data.off_x, i * item_h + data.off_y, side_w, item_h), 5)

    draw()

    mode = 0
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                return
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, False)
                draw()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                pos = data.get_mouse_pos()
                if rect.collidepoint(*pos):
                    pos = [(pos[0] - rect.x) / rect.w, (pos[1] - rect.y) / rect.h]
                    if current.idx == START:
                        current.pos = pos
                        paths = [current]
                        current = Start()
                    elif current.idx == LINE:
                        paths.append(current)
                        current = Line(start=pos)
                    elif current.idx == CIRCLE:
                        if mode == 0:
                            mode = 1
                        else:
                            paths.append(current)
                            current = Circle()
                            mode = 0
                else:
                    idx = pos[1] * len(types) // data.screen_w
                    if idx >= len(types) - 1:
                        with open("custom_levels.bin", "ab+") as file:
                            file.write(len(paths).to_bytes(1, byteorder))
                            for p in paths:
                                file.write(p.to_bytes())
                        return
                    elif selected != types[idx] and len(paths) > 0:
                        selected = types[idx]
                        draw_options()
                        if selected == "Start":
                            current = Start()
                        elif selected == "Line":
                            current = Line(start=paths[-1].get_end())
                        elif selected == "Circle":
                            current = Circle()
                        mode = 0
            elif e.type == MOUSEMOTION:
                pos = data.get_mouse_pos()
                pos = [(pos[0] - rect.x) / rect.w, (pos[1] - rect.y) / rect.h]
                pos_ = [min(max(i, 0), 1) for i in pos]
                if current.idx == START:
                    current.pos = pos_
                    for i in range(2):
                        if abs(.5 - current.pos[i]) < .025:
                            current.pos[i] = .5
                elif current.idx == LINE:
                    current.end = pos_
                    dx, dy = current.end[0] - current.start[0], current.end[1] - current.start[1]
                    if abs(dx) < .025:
                        current.end[0] = current.start[0]
                    if abs(dy) < .025:
                        current.end[1] = current.start[1]
                    if abs(abs(dx) - abs(dy)) < .025:
                        r = math.sqrt(dx * dx + dy * dy)
                        delta = r * math.sqrt(2) / 2
                        current.end[0] = current.start[0] + math.copysign(delta, dx)
                        current.end[1] = current.start[1] + math.copysign(delta, dy)
                elif current.idx == CIRCLE:
                    data.TWO_PI = 2 * math.pi
                    if mode == 0:
                        # Get end of last segment
                        end = paths[-1].get_end()
                        for i in range(2):
                            if abs(end[i] - pos[i]) < .025:
                                pos[i] = end[i]
                        r = data.get_distance(end, pos)
                        # Set initial circle angle
                        current.theta_i = data.get_angle_pixels(pos, end)
                        current.theta_f = current.theta_i + data.TWO_PI
                        if pos[0] - r >= 0 and pos[0] + r <= 1 and pos[1] - r >= 0 and pos[1] + r <= 1:
                            current.center = pos
                            current.radius = r
                        else:
                            trig = [math.cos(current.theta_i), -math.sin(current.theta_i)]
                            diameter = 1
                            for i in range(2):
                                # Distance to negative edge
                                d = end[i]
                                # Number of diameters from starting point to negative edge
                                v = .5 + trig[i] / 2
                                if v > 0 and d / v < diameter:
                                    diameter = d / v
                                # Same for positive edge
                                d = 1 - d
                                v = 1 - v
                                if v > 0 and d / v < diameter:
                                    diameter = d / v
                            radius = diameter / 2
                            # Set center position and radius
                            current.center = [end[i] - radius * trig[i] for i in range(2)]
                            current.radius = radius
                    else:
                        # Calculate change in angle
                        dtheta = data.get_angle_pixels(current.center, pos) - (current.theta_f % data.TWO_PI)
                        # Make sure we are going in the correct direction
                        if dtheta > math.pi:
                            dtheta -= data.TWO_PI
                        elif dtheta < -math.pi:
                            dtheta += data.TWO_PI
                        current.theta_f += dtheta
                        diff = current.theta_f - current.theta_i
                        ten_pi = data.TWO_PI * 5
                        if diff > ten_pi:
                            current.theta_f = ten_pi + current.theta_i
                        elif diff < -ten_pi:
                            current.theta_f = -ten_pi + current.theta_i
                        half_pi, quarter_pi = math.pi / 2, math.pi / 4
                        factor = (diff + quarter_pi) // half_pi
                        if abs(diff - half_pi * factor) < half_pi / 10:
                            current.theta_f = factor * half_pi + current.theta_i
                pg.display.get_surface().blit(draw_paths(rect, paths + [current]),
                                              (rect.x + data.off_x, rect.y + data.off_y))
        pg.display.flip()


main_screen()
