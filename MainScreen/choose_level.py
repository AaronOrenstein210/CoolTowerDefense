from sys import byteorder
from os.path import isfile
import pygame as pg
from pygame.locals import *
from Game.level_objects import draw_paths, draw_spawn_list, load_paths, load_spawn_list
from MainScreen.new_level import new_level
from MainScreen.new_wave import new_wave
import data

levels, spawns = 0, 1
# Load all levels and spawn lists
level_data = [[], []]
spawn_blacklist = []
# Stores which array, position, and value of deleted items
history = []
delete = False

# Surface and rectangle for all levels and waves
surfaces = [pg.Surface((0, 0))] * 2
rects = [pg.Rect(0, 0, 0, 0)] * 2
# Surface and rectangle for level/wave previews
previews = [pg.Surface((0, 0))] * 2
preview_rects = [pg.Rect(0, 0, 0, 0)] * 2
# Text, surfaces, and rectangles for top text
text = ["Select Level", "Select Waves", "Press Enter to Start"]
title_text = [pg.Surface((0, 0))] * 3
title_rects = [pg.Rect(0, 0, 0, 0)] * 3
# Misc buttons
button_order = ["new level", "edit", "delete", "undo", "new wave"]
button_imgs = ["res/{}.png".format(s) for s in ["add", "lock", "delete", "undo", "add"]]
button_rects = {s: pg.Rect(0, 0, 0, 0) for s in button_order}
# Other ui variables
off = [0, 0]
selected_lvl = -1
hovering = [-1, -1]

lvl_font = back_img = overlay = None

row_len = 5
margin = 10

item_w = 0


def reset():
    global delete
    delete = False
    history.clear()
    level_data[0].clear()
    level_data[1].clear()


def resize():
    global item_w, lvl_font, back_img, overlay
    # Get specific dimensions
    half_w = data.screen_w // 2
    eighth_w = data.screen_w // 8
    d = pg.display.get_surface()
    d.fill((0, 0, 0))
    # Draw middle line
    pg.draw.line(d, (200, 200, 0), [half_w + data.off_x, data.off_y],
                 [half_w + data.off_x, data.screen_w * 7 // 8 + data.off_y], int(margin * .9))
    # Title = w/8
    title_rects[2] = pg.Rect(data.off_x, data.off_y, data.screen_w, eighth_w)
    title_rects[levels] = pg.Rect(data.off_x, data.off_y, half_w - margin, eighth_w)
    title_rects[spawns] = title_rects[levels].move(half_w + margin, 0)
    # Scroll = w*4/8
    rects[levels] = pg.Rect(*title_rects[levels].bottomleft, title_rects[levels].w, half_w)
    rects[spawns] = rects[levels].move(half_w + margin, 0)
    # Level/Wave preview = w*2/8
    preview_rects[levels] = pg.Rect(data.off_x + half_w // 4, rects[levels].bottom, half_w // 2, half_w // 2)
    preview_rects[spawns] = pg.Rect(*rects[spawns].bottomleft, rects[spawns].w, half_w // 2)
    # Bottom buttons = w/8
    but_w = eighth_w * 9 // 10
    off_ = (eighth_w - but_w) // 2
    space = (data.screen_w - eighth_w) // (len(button_order) - 1)
    y = data.off_y + data.screen_w - off_ - but_w
    for i, string in enumerate(button_order):
        r = pg.Rect(data.off_x + off_ + space * i, y, but_w, but_w)
        img = data.scale_to_fit(pg.image.load(button_imgs[i]), w=but_w, h=but_w)
        d.blit(img, img.get_rect(center=r.center))
        button_rects[string] = r
    # Set up parts of the surfaces
    item_w = rects[levels].w // row_len
    back_img = pg.transform.scale(pg.image.load("res/back.png"), (item_w, item_w))
    lvl_font = data.get_scaled_font(item_w * 3 // 5, item_w * 3 // 5, "999")
    # Black overlay
    overlay = pg.Surface((item_w, item_w))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    # Draw levels and waves
    draw()
    # Set up title text
    font = data.get_scaled_font(half_w - margin, title_rects[levels].h, data.get_widest_string(text))
    for j in range(3):
        title_text[j] = font.render(text[j], 1, (255, 255, 255))
        title_rects[j] = title_text[j].get_rect(center=title_rects[j].center)
    update_title()


def draw():
    # Set up surfaces and rectangles
    for j, arr in enumerate(level_data):
        num_rows = len(arr) // row_len + 1
        surfaces[j] = pg.Surface((rects[j].w, item_w * num_rows))
        for k in range(len(arr)):
            row, col = k // row_len, k % row_len
            rect = pg.Rect(col * item_w, row * item_w, item_w, item_w)
            text_s = lvl_font.render(str(k + 1), 1, (255, 255, 255))
            text_rect = text_s.get_rect(center=rect.center)
            surfaces[j].blit(back_img, rect)
            surfaces[j].blit(text_s, text_rect)
            if j == levels and k == selected_lvl:
                pg.draw.rect(surfaces[j], (255, 255, 0), rect, 2)
            elif j == spawns and k in spawn_blacklist:
                surfaces[j].blit(overlay, rect)
                surfaces[j].fill((0, 0, 0), rect)
            if delete:
                pg.draw.rect(surfaces[j], (255, 0, 0), rect, 2)
        off[j] = 0
        pg.display.get_surface().fill((0, 0, 0), rects[j])
        pg.display.get_surface().blit(surfaces[j], rects[j].topleft, area=((0, off[j]), rects[j].size))
        # Draw preview for selected items
        hovering[j] = -1


def update_title():
    d = pg.display.get_surface()
    d.fill((0, 0, 0), title_rects[2])
    # Update title text
    if selected_lvl != -1:
        d.blit(title_text[2], title_rects[2])
    else:
        half_w = data.screen_w // 2
        # Draw middle line
        pg.draw.line(d, (200, 200, 0), [half_w + data.off_x, data.off_y],
                     [half_w + data.off_x, data.screen_w * 7 // 8 + data.off_y], int(margin * .9))
        for j in range(2):
            d.blit(title_text[j], title_rects[j])


def save_data():
    with open(data.LEVELS, "wb+") as file:
        for paths in level_data[levels]:
            byte_data = len(paths).to_bytes(1, byteorder)
            for p in paths:
                byte_data += p.to_bytes()
            file.write(byte_data)
    with open(data.WAVES, "wb+") as file:
        for wave in level_data[spawns]:
            byte_data = len(wave).to_bytes(1, byteorder)
            for s in wave:
                byte_data += s.to_bytes()
            file.write(byte_data)


# Runs level selection screen
def choose_level():
    reset()

    if isfile(data.LEVELS):
        with open(data.LEVELS, 'rb') as file:
            file_data = file.read()
        # Loop through the data
        while len(file_data) > 0:
            arr, file_data = load_paths(file_data)
            level_data[levels].append(arr)
    if isfile(data.WAVES):
        with open(data.WAVES, 'rb') as file:
            file_data = file.read()
        # Loop through data
        while len(file_data) > 0:
            arr, file_data = load_spawn_list(file_data)
            level_data[spawns].append(arr)
    spawn_blacklist.clear()

    resize()
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                save_data()
                return False
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, False)
                resize()
            elif e.type == MOUSEMOTION:
                pos = pg.mouse.get_pos()
                for i, array in enumerate(level_data):
                    if rects[i].collidepoint(*pos):
                        pos = [pos[0] - rects[i].x, pos[1] - rects[i].y]
                        idx = (pos[1] // item_w) * row_len + (pos[0] // item_w)
                        if idx > len(array):
                            idx = -1
                    else:
                        idx = -1
                    if 0 <= idx < len(array) and idx != hovering[i]:
                        hovering[i] = idx
                        if i == levels:
                            previews[i] = draw_paths(data.screen_w // 4, array[idx])
                        else:
                            previews[i] = draw_spawn_list(array[idx], data.screen_w // 4, w=rects[i].w - 1)
                        pg.display.get_surface().fill((0, 0, 0), preview_rects[i])
                        pg.display.get_surface().blit(previews[i], preview_rects[i])
            elif e.type == MOUSEBUTTONUP:
                if e.button == BUTTON_LEFT:
                    global delete
                    pos = pg.mouse.get_pos()
                    done = False
                    for i, r in enumerate(rects):
                        if r.collidepoint(*pos):
                            pos = [pos[0] - r.x, pos[1] - r.y]
                            row, col = pos[1] // item_w, pos[0] // item_w
                            idx = row * row_len + col
                            if idx < len(level_data[i]):
                                if delete:
                                    history.append([i, idx, level_data[i][idx]])
                                    del level_data[i][idx]
                                    draw()
                                else:
                                    item_r = pg.Rect(col * item_w, row * item_w, item_w, item_w)
                                    if i == levels:
                                        global selected_lvl
                                        # Remove yellow border
                                        if selected_lvl != -1:
                                            row, col = selected_lvl // row_len, selected_lvl % row_len
                                            pg.draw.rect(surfaces[i], (0, 0, 0),
                                                         (col * item_w, row * item_w, item_w, item_w), 2)
                                        selected_lvl = idx if idx != selected_lvl else -1
                                        # Draw yellow border
                                        if selected_lvl != -1:
                                            pg.draw.rect(surfaces[i], (255, 255, 0), item_r, 2)
                                    else:
                                        if idx in spawn_blacklist:
                                            spawn_blacklist.remove(idx)
                                            surfaces[i].fill((0, 0, 0), item_r)
                                            surfaces[i].blit(back_img, item_r)
                                            text_s = lvl_font.render(str(idx + 1), 1, (255, 255, 255))
                                            surfaces[i].blit(text_s, text_s.get_rect(center=item_r.center))
                                        else:
                                            spawn_blacklist.append(idx)
                                            surfaces[i].blit(overlay, item_r)
                                    update_title()
                                    d = pg.display.get_surface()
                                    d.fill((0, 0, 0), r)
                                    d.blit(surfaces[i], r.topleft, area=((0, -off[i]), r.size))
                            done = True
                            break
                    if not done:
                        for i, key in enumerate(button_order):
                            if button_rects[key].collidepoint(*pos):
                                if key == "new level":
                                    result = new_level()
                                    if result:
                                        level_data[levels].append(result)
                                    resize()
                                elif key == "new wave":
                                    result = new_wave()
                                    if result:
                                        level_data[spawns].append(result)
                                    resize()
                                elif key == "delete":
                                    delete = not delete
                                    draw()
                                elif key == "undo":
                                    if len(history) > 0:
                                        idx1, idx2, val = history[-1]
                                        level_data[idx1].insert(idx2, val)
                                        del history[-1]
                                    resize()
                                break
                elif e.button == BUTTON_WHEELUP or e.button == BUTTON_WHEELDOWN:
                    pos = pg.mouse.get_pos()
                    up = e.button == BUTTON_WHEELUP
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(*pos):
                            off[i] += (data.screen_w // (row_len * 6)) * (1 if up else -1)
                            max_off = rect.h - surfaces[i].get_size()[1]
                            if off[i] < max_off:
                                off[i] = max_off
                            if off[i] > 0:
                                off[i] = 0
                            d = pg.display.get_surface()
                            d.fill((0, 0, 0), rect)
                            d.blit(surfaces[i], rect.topleft, area=((0, -off[i]), rect.size))
                            break
            elif e.type == KEYUP and e.key == K_RETURN and selected_lvl != -1 and \
                    len(spawn_blacklist) != len(level_data[spawns]):
                save_data()
                data.calculate_dimensions(True)
                data.lvlDriver.set_level(level_data[levels][selected_lvl],
                                         [a for i, a in enumerate(level_data[spawns]) if i not in spawn_blacklist])
                return True
        pg.display.flip()
