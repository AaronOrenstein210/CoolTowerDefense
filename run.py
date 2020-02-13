# Created on 27 January 2020
# Created by

from os.path import isfile
import math
import pygame as pg
from pygame.locals import *
import data
from LevelReader import *

pg.init()
data.init()
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


# Main function which helps specific ui screens release their variables
def main():
    while choose_level():
        run_level()


# Runs level selection screen
def choose_level():
    levels, spawns = 0, 1
    # Load all levels and spawn lists
    level_data = [[], []]
    if isfile(data.LEVELS):
        with open(data.LEVELS, 'rb') as file:
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
                    file_data = ""
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
                        file_data = ""
                        break
            level_data[levels].append(file_data[:byte_pos])
            file_data = file_data[byte_pos:]
    if isfile(data.SPAWNS):
        with open(data.SPAWNS, 'rb') as file:
            file_data = file.read()
        # Loop through data
        while len(file_data) > 0:
            num_spawns = int.from_bytes(file_data[0:1], byteorder)
            num_bytes = num_spawns * 5 + 1
            if len(file_data) < num_bytes:
                print("Missing Bytes")
                file_data = ""
            else:
                level_data[spawns].append(file_data[:num_bytes])
                file_data = file_data[num_bytes:]

    surfaces = [pg.Surface] * 2
    rects = [pg.Rect(0, 0, 0, 0)] * 2
    previews = [None] * 2
    preview_rects = [pg.Rect(0, 0, 0, 0)] * 2
    text = ["Select Level", "Select Enemies", "Press Enter to Start"]
    title_text = [pg.Surface] * 3
    title_rects = [pg.Rect(0, 0, 0, 0)] * 3
    off = [0, 0]
    selected = [-1, -1]
    hovering = [-1, -1]

    row_len = 5
    margin = 10

    def resize():
        half_w = data.screen_w // 2
        # Draw middle line
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        pg.draw.line(d, (200, 200, 0), [half_w + data.off_x, data.off_y],
                     [half_w + data.off_x, data.screen_w + data.off_y], int(margin * .9))
        # Define rectangles
        title_rects[2] = pg.Rect(data.off_x, data.off_y, data.screen_w, half_w // 4)
        title_rects[levels] = pg.Rect(data.off_x, data.off_y, half_w - margin, half_w // 4)
        title_rects[spawns] = title_rects[levels].move(half_w + margin, 0)
        rects[levels] = pg.Rect(*title_rects[levels].bottomleft, title_rects[levels].w, half_w * 5 // 4)
        rects[spawns] = rects[levels].move(half_w + margin, 0)
        preview_rects[levels] = pg.Rect(data.off_x + half_w // 4, rects[levels].bottom, half_w // 2, half_w // 2)
        preview_rects[spawns] = pg.Rect(*rects[spawns].bottomleft, rects[spawns].w, half_w // 2)
        # Set up parts of the surfaces
        lvl_w = rects[levels].w // row_len
        back_img = pg.transform.scale(pg.image.load("res/back.png"), (lvl_w, lvl_w))
        font = data.get_scaled_font(lvl_w * 3 // 5, lvl_w * 3 // 5, "999")
        # Set up surfaces and rectangles
        for j, arr in enumerate(level_data):
            num_rows = (len(arr) + 1) // row_len + 1
            surfaces[j] = pg.Surface((rects[j].w, lvl_w * num_rows))
            for k in range(len(arr)):
                row, col = k // row_len, k % row_len
                text_s = font.render(str(k + 1), 1, (255, 255, 255))
                text_rect = text_s.get_rect(center=(int((col + .5) * lvl_w), int((row + .5) * lvl_w)))
                surfaces[j].blit(back_img, (col * lvl_w, row * lvl_w))
                surfaces[j].blit(text_s, text_rect)
            # Add plus sign at the end
            row, col = len(arr) // row_len, len(arr) % row_len
            plus = pg.transform.scale(pg.image.load("res/add.png"), (int(lvl_w * .9), int(lvl_w * .9)))
            plus_rect = plus.get_rect(center=(int((col + .5) * lvl_w), int((row + .5) * lvl_w)))
            surfaces[j].blit(plus, plus_rect)
            off[j] = 0
            d.blit(surfaces[j], rects[j].topleft, area=((0, off[j]), rects[j].size))
            # Draw preview for selected items
            hovering[j] = -1
            if selected[j] != -1:
                if j == levels:
                    previews[j] = draw_paths(data.screen_w // 4, load_paths(arr[selected[j]]))
                else:
                    previews[j] = draw_spawn_list(rects[j].w - 1, data.screen_w // 4,
                                                  load_spawn_list(arr[selected[j]]))
                d.blit(previews[j], preview_rects[j])
        # Set up title text
        font = data.get_scaled_font(half_w - margin, title_rects[levels].h, data.get_widest_string(text))
        for j in range(3):
            title_text[j] = font.render(text[j], 1, (255, 255, 255))
            title_rects[j] = title_text[j].get_rect(center=title_rects[j].center)
        update_title()

    def update_title():
        d = pg.display.get_surface()
        d.fill((0, 0, 0), (data.off_x, data.off_y, data.screen_w, rects[0].y - data.off_y))
        # Update title text
        if -1 not in selected:
            d.blit(title_text[2], title_rects[2])
        else:
            half_w = data.screen_w // 2
            pg.draw.line(d, (200, 200, 0), [half_w + data.off_x, data.off_y],
                         [half_w + data.off_x, data.screen_w + data.off_y], int(margin * .9))
            for j in range(2):
                d.blit(title_text[j], title_rects[j])

    resize()
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                return False
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, False)
                resize()
            elif e.type == MOUSEMOTION:
                pos = pg.mouse.get_pos()
                for i, array in enumerate(level_data):
                    if rects[i].collidepoint(*pos):
                        pos = [pos[0] - rects[i].x, pos[1] - rects[i].y]
                        item_w = rects[i].w // row_len
                        idx = (pos[1] // item_w) * row_len + (pos[0] // item_w)
                        if idx > len(array):
                            idx = selected[i]
                    else:
                        idx = selected[i]
                    if 0 <= idx < len(array) and idx != hovering[i]:
                        hovering[i] = idx
                        if i == levels:
                            previews[i] = draw_paths(data.screen_w // 4, load_paths(array[idx]))
                        else:
                            previews[i] = draw_spawn_list(rects[i].w - 1, data.screen_w // 4,
                                                          load_spawn_list(array[idx]))
                        pg.display.get_surface().fill((0, 0, 0), preview_rects[i])
                        pg.display.get_surface().blit(previews[i], preview_rects[i])
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                pos = pg.mouse.get_pos()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(*pos):
                        pos = [pos[0] - rect.x, pos[1] - rect.y]
                        item_w = rect.w // row_len
                        row, col = pos[1] // item_w, pos[0] // item_w
                        idx = row * row_len + col
                        if idx < len(level_data[i]):
                            if selected[i] != -1:
                                row_, col_ = selected[i] // row_len, selected[i] % row_len
                                pg.draw.rect(pg.display.get_surface(), (0, 0, 0),
                                             (rect.x + col_ * item_w, rect.y + row_ * item_w, item_w, item_w), 2)
                            selected[i] = idx if idx != selected[i] else -1
                            if selected[i] != -1:
                                pg.draw.rect(pg.display.get_surface(), (255, 255, 0),
                                             (rect.x + col * item_w, rect.y + row * item_w, item_w, item_w), 2)
                            update_title()
                        elif idx == len(level_data[i]):
                            result = new_level() if i == levels else new_enemy_list()
                            if result != "":
                                level_data[i].append(result)
                            resize()
                        break
            elif e.type == KEYUP and e.key == K_RETURN and -1 not in selected:
                data.lvlDriver.reset()
                data.lvlDriver.lr.load(*[level_data[i][selected[i]] for i in range(2)])
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
        pg.display.get_surface().blit(draw_paths(rect.w, paths + [current]),
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
                return ""
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
                        byte_data = len(paths).to_bytes(1, byteorder)
                        for p in paths:
                            byte_data += p.to_bytes()
                        with open(data.LEVELS, "ab+") as file:
                            file.write(byte_data)
                        return byte_data
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
                pg.display.get_surface().blit(draw_paths(rect.w, paths + [current]),
                                              (rect.x + data.off_x, rect.y + data.off_y))
        pg.display.flip()


# Runs screen to set spawn order
def new_enemy_list():
    spawns = []
    current = Spawn()

    rects = {"Count": Rect(0, 0, 0, 0), "Time": Rect(0, 0, 0, 0),
             "Model": Rect(0, 0, 0, 0), "Flip": Rect(0, 0, 0, 0),
             "Add": Rect(0, 0, 0, 0), "Delete": Rect(0, 0, 0, 0), "Save": Rect(0, 0, 0, 0),
             "Current": Rect(0, 0, 0, 0), "Timeline": Rect(0, 0, 0, 0)}
    selected = "Count"
    model_names = {LINEAR: "Linear", PARABOLIC: "Parabolic",
                   EXPONENTIAL: "Exponential"}
    models = list(model_names.keys())
    model_idx = 0

    show_cursor = True

    def resize():
        w = data.screen_w
        rects["Current"] = Rect(w // 20 + data.off_x, w * 3 // 8 + data.off_y, w * 9 // 10, w // 4)
        rects["Timeline"] = Rect(w // 20 + data.off_x, w * 17 // 24 + data.off_y, w * 9 // 10, w // 4)
        # TODO: set rect dims
        fifteenth = w // 15
        twentieth = w // 20
        rects["Count"] = Rect(twentieth * 2 + data.off_x, fifteenth + data.off_y, twentieth * 7, fifteenth)
        rects["Time"] = rects["Count"].move(twentieth * 9, 0)
        rects["Model"] = rects["Count"].move(0, fifteenth)
        rects["Flip"] = rects["Model"].move(twentieth * 9, 0)
        rects["Add"] = Rect(twentieth * 2 + data.off_x, fifteenth * 4 + data.off_y, twentieth * 4, fifteenth)
        rects["Delete"] = rects["Add"].move(twentieth * 6, 0)
        rects["Save"] = rects["Delete"].move(twentieth * 6, 0)
        draw()

    def draw():
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        # Draw current timeline
        r = rects["Current"]
        d.blit(current.get_img(*r.size), r.topleft)
        # Draw entire timeline
        d.blit(draw_spawn_list(*rects["Timeline"].size, spawns), rects["Timeline"].topleft)
        # Draw text for number of spawns
        text = "{}{} Enemies".format(current.num_enemies, "|" if selected == "Count" and show_cursor else "")
        color_ = (255, 255, 255) if current.num_enemies >= 1 else (255, 0, 0)
        draw_text(text, rects["Count"], d, color_=color_)
        # Draw text for duration
        text = "Over {}{}ms".format(current.duration, "|" if selected == "Time" and show_cursor else "")
        color_ = (255, 255, 255) if current.duration >= 100 else (255, 0, 0)
        draw_text(text, rects["Time"], d, color_=color_)
        # Outline either the enemy count or duration
        pg.draw.rect(d, (200, 200, 0), rects[selected], 2)
        # Draw text for model and flip button
        draw_text(model_names[current.model], rects["Model"], d)
        draw_text("Reverse", rects["Flip"], d)
        # Draw add, delete, and save buttons
        for string in ["Add", "Delete", "Save"]:
            draw_text(string, rects[string], d)

    def draw_text(text, rect, surface, color_=(255, 255, 255)):
        font = data.get_scaled_font(*rect.size, text)
        text_s = font.render(text, 1, color_)
        text_rect = text_s.get_rect(center=rect.center)
        surface.blit(text_s, text_rect)

    resize()
    while True:
        # Update whether to show the cursor or not
        temp = show_cursor
        show_cursor = (pg.time.get_ticks() // 400) % 2 == 0
        if temp != show_cursor:
            draw()
        for e in pg.event.get():
            if e.type == QUIT:
                return ""
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, False)
                resize()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                # Offset is include in the rectangles
                pos = pg.mouse.get_pos()
                if rects["Count"].collidepoint(*pos):
                    selected = "Count"
                elif rects["Time"].collidepoint(*pos):
                    selected = "Time"
                elif rects["Model"].collidepoint(*pos):
                    model_idx = (model_idx + 1) % len(models)
                    current.model = models[model_idx]
                elif rects["Flip"].collidepoint(*pos):
                    current.flip = not current.flip
                elif rects["Add"].collidepoint(*pos):
                    if current.num_enemies >= 1 and current.duration >= 100:
                        spawns.append(current)
                        current = Spawn()
                elif rects["Delete"].collidepoint(*pos):
                    print("Delete")
                elif rects["Save"].collidepoint(*pos):
                    if len(spawns) > 0:
                        byte_data = len(spawns).to_bytes(1, byteorder)
                        for s in spawns:
                            byte_data += s.to_bytes()
                        with open(data.SPAWNS, "ab+") as file:
                            file.write(byte_data)
                        return byte_data
                else:
                    continue
                draw()
            elif e.type == KEYUP:
                if e.key == K_BACKSPACE:
                    if selected == "Count":
                        current.num_enemies = current.num_enemies // 10
                    else:
                        current.duration = current.duration // 10
                elif pg.key.name(e.key).isnumeric():
                    val = int(pg.key.name(e.key))
                    if selected == "Count":
                        current.num_enemies = min(current.num_enemies * 10 + val, 99)
                    else:
                        current.duration = min(current.duration * 10 + val, 10000)
                else:
                    continue
                draw()
        pg.display.flip()


main()
