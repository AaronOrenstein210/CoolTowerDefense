# Created on 27 January 2020
# Created by

import math
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
                    draw()
        pg.display.flip()


# Opens choose level screen
def choose_level():
    print("Choose Level")


# TODO: Close & save level
# Opens create a level screen
def new_level():
    # Start with spots for start and end
    paths = []
    selected, current = "Start", reader.Start()
    types = ["Start", "Line", "Circle", "Save & Exit"]
    rect = pg.Rect(0, 0, 0, 0)

    def draw():
        pg.display.get_surface().fill((0, 0, 0))
        side_w = data.screen_w // 5
        rect.topleft = [side_w, side_w // 2]
        rect.size = [data.screen_w - side_w] * 2
        draw_editor()
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

    def draw_editor():
        d = pg.display.get_surface()
        s = pg.Surface(rect.size)
        s.fill((0, 175, 0))
        w = rect.w // 40
        for p in paths + [current]:
            if p.idx == reader.LINE:
                pos_i = [int(p.start[0] * rect.w), int(p.start[1] * rect.h)]
                pos_f = [int(p.end[0] * rect.w), int(p.end[1] * rect.h)]
                pg.draw.line(s, (255, 255, 255), pos_i, pos_f, w)
                pg.draw.rect(s, (255, 255, 255), (pos_i[0] - w / 2, pos_i[1] - w // 2, w, w))
                pg.draw.rect(s, (255, 255, 255), (pos_f[0] - w / 2, pos_f[1] - w // 2, w, w))
            elif p.idx == reader.CIRCLE:
                c = [int(p.center[0] * rect.w), int(p.center[1] * rect.h)]
                rad = int(p.radius * rect.w)
                # Get theta range
                d_theta = p.theta_f - p.theta_i
                sign = math.copysign(1, d_theta)
                d_theta = abs(d_theta)
                # Break theta range into full circles
                loop = -1
                while d_theta >= data.TWO_PI:
                    loop += 1
                    d_theta -= data.TWO_PI
                # Draw the highest full circle
                if loop >= 0:
                    pg.draw.circle(s, p.COLORS[loop], c, rad, min(w, rad))
                # Draw the other sections
                if d_theta > 0 and loop < len(p.COLORS) - 1:
                    top_left = [c[0] - rad, c[1] - rad]
                    thetas = [p.theta_i, p.theta_i + d_theta * sign]
                    theta_min, theta_max = min(thetas), max(thetas)
                    pg.draw.arc(s, p.COLORS[loop + 1], (*top_left, rad * 2, rad * 2), theta_min,
                                theta_max, min(w, rad))
            elif p.idx == reader.START:
                pos = [int(p.pos[0] * rect.w), int(p.pos[1] * rect.h)]
                pg.draw.circle(s, (0, 200, 200), pos, w)
        d.blit(s, (rect.x + data.off_x, rect.y + data.off_y))

    draw()

    mode = 0
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                exit(0)
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h)
                draw()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                pos = data.get_mouse_pos()
                if rect.collidepoint(*pos):
                    pos = [(pos[0] - rect.x) / rect.w, (pos[1] - rect.y) / rect.h]
                    if current.idx == reader.START:
                        current.pos = pos
                        paths = [current]
                        current = reader.Start()
                    elif current.idx == reader.LINE:
                        paths.append(current)
                        current = reader.Line(start=pos)
                    elif current.idx == reader.CIRCLE:
                        if mode == 0:
                            mode = 1
                        else:
                            paths.append(current)
                            current = reader.Circle()
                            mode = 0
                else:
                    idx = pos[1] * len(types) // data.screen_w
                    if idx >= len(types) - 1:
                        print("Save")
                        return
                    elif selected != types[idx] and len(paths) > 0:
                        selected = types[idx]
                        draw_options()
                        if selected == "Start":
                            current = reader.Start()
                        elif selected == "Line":
                            current = reader.Line(start=paths[-1].get_end())
                        elif selected == "Circle":
                            current = reader.Circle()
                        mode = 0
            elif e.type == MOUSEMOTION:
                pos = data.get_mouse_pos()
                pos = [(pos[0] - rect.x) / rect.w, (pos[1] - rect.y) / rect.h]
                pos_ = [min(max(i, 0), 1) for i in pos]
                if current.idx == reader.START:
                    current.pos = pos_
                elif current.idx == reader.LINE:
                    current.end = pos_
                    for i in range(2):
                        if abs(current.end[i] - current.start[i]) < .025:
                            current.end[i] = current.start[i]
                elif current.idx == reader.CIRCLE:
                    data.TWO_PI = 2 * math.pi
                    if mode == 0:
                        # Get end of last segment
                        end = paths[-1].get_end()
                        for i in range(2):
                            if abs(end[i] - pos[i]) < .025:
                                pos[i] = end[i]
                        # Calculate displacement
                        dx, dy = pos[0] - end[0], pos[1] - end[1]
                        # Circle radius
                        r = math.sqrt(dx * dx + dy * dy)
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
                        ten_pi = data.TWO_PI * 5
                        if current.theta_f > ten_pi + current.theta_i:
                            current.theta_f = ten_pi + current.theta_i
                        elif current.theta_f < -ten_pi + current.theta_i:
                            current.theta_f = -ten_pi + current.theta_i
                draw_editor()

        pg.display.flip()


main_screen()
