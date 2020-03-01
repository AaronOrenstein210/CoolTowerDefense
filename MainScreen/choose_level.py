from os.path import isfile
import pygame as pg
from pygame.locals import *
from Game.level_objects import draw_paths, draw_spawn_list, load_paths, load_spawn_list
from MainScreen.new_level import new_level
from MainScreen.new_enemy_list import new_enemy_list
import data

levels, spawns = 0, 1
# Load all levels and spawn lists
level_data = [[], []]
spawn_blacklist = []

surfaces = [pg.Surface] * 2
rects = [pg.Rect(0, 0, 0, 0)] * 2
previews = [None] * 2
preview_rects = [pg.Rect(0, 0, 0, 0)] * 2
text = ["Select Map", "Select Levels", "Press Enter to Start"]
title_text = [None] * 3
title_rects = [pg.Rect(0, 0, 0, 0)] * 3
off = [0, 0]
selected_lvl = -1
hovering = [-1, -1]

lvl_font = back_img = overlay = None

row_len = 5
margin = 10

item_w = 0


def resize():
    global item_w, lvl_font, back_img, overlay
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
    item_w = rects[levels].w // row_len
    back_img = pg.transform.scale(pg.image.load("res/back.png"), (item_w, item_w))
    lvl_font = data.get_scaled_font(item_w * 3 // 5, item_w * 3 // 5, "999")
    # Black overlay
    overlay = pg.Surface((item_w, item_w))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    # Set up surfaces and rectangles
    for j, arr in enumerate(level_data):
        num_rows = (len(arr) + 1) // row_len + 1
        surfaces[j] = pg.Surface((rects[j].w, item_w * num_rows))
        for k in range(len(arr)):
            row, col = k // row_len, k % row_len
            text_s = lvl_font.render(str(k + 1), 1, (255, 255, 255))
            text_rect = text_s.get_rect(center=(int((col + .5) * item_w), int((row + .5) * item_w)))
            surfaces[j].blit(back_img, (col * item_w, row * item_w))
            surfaces[j].blit(text_s, text_rect)
            if j == levels and k == selected_lvl:
                pg.draw.rect(surfaces[j], (255, 255, 0), (col * item_w, row * item_w, item_w, item_w), 2)
            elif j == spawns and k in spawn_blacklist:
                surfaces[j].blit(overlay, (col * item_w, row * item_w))
                surfaces[j].fill((0, 0, 0), (col * item_w, row * item_w, item_w, item_w))
        # Add plus sign at the end
        row, col = len(arr) // row_len, len(arr) % row_len
        plus = pg.transform.scale(pg.image.load("res/add.png"), (int(item_w * .9), int(item_w * .9)))
        plus_rect = plus.get_rect(center=(int((col + .5) * item_w), int((row + .5) * item_w)))
        surfaces[j].blit(plus, plus_rect)
        off[j] = 0
        d.blit(surfaces[j], rects[j].topleft, area=((0, off[j]), rects[j].size))
        # Draw preview for selected items
        hovering[j] = -1
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
    if selected_lvl != -1:
        d.blit(title_text[2], title_rects[2])
    else:
        half_w = data.screen_w // 2
        pg.draw.line(d, (200, 200, 0), [half_w + data.off_x, data.off_y],
                     [half_w + data.off_x, data.screen_w + data.off_y], int(margin * .9))
        for j in range(2):
            d.blit(title_text[j], title_rects[j])


# Runs level selection screen
def choose_level():
    for arr in level_data:
        arr.clear()
    if isfile(data.LEVELS):
        with open(data.LEVELS, 'rb') as file:
            file_data = file.read()
        # Loop through the data
        while len(file_data) > 0:
            arr, file_data = load_paths(file_data)
            level_data[levels].append(arr)
    if isfile(data.SPAWNS):
        with open(data.SPAWNS, 'rb') as file:
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
                            previews[i] = draw_spawn_list(rects[i].w - 1, data.screen_w // 4, array[idx])
                        pg.display.get_surface().fill((0, 0, 0), preview_rects[i])
                        pg.display.get_surface().blit(previews[i], preview_rects[i])
            elif e.type == MOUSEBUTTONUP:
                if e.button == BUTTON_LEFT:
                    pos = pg.mouse.get_pos()
                    for i, r in enumerate(rects):
                        if r.collidepoint(*pos):
                            pos = [pos[0] - r.x, pos[1] - r.y]
                            row, col = pos[1] // item_w, pos[0] // item_w
                            idx = row * row_len + col
                            if idx < len(level_data[i]):
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
                            elif idx == len(level_data[i]):
                                result = new_level() if i == levels else new_enemy_list()
                                if result != "":
                                    obj, result = load_paths(result) if i == levels else load_spawn_list(result)
                                    level_data[i].append(obj)
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
                data.calculate_dimensions(True)
                data.lvlDriver.set_level(level_data[levels][selected_lvl],
                                         [a for i, a in enumerate(level_data[spawns]) if i not in spawn_blacklist])
                return True
        pg.display.flip()
