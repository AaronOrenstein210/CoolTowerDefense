# Created on 5 March 2020
from os import listdir, getcwd
from os.path import isfile, isdir
import pygame as pg
from pygame.locals import *
from data import get_scaled_font, get_widest_string, scale_to_fit

path = "/"
surface = hover_img = None
scroll = max_scroll = line_h = 0
selected = hover = -1
files = []
file_types = []


def reset():
    global path, selected
    selected = -1
    path = getcwd().replace("\\", "/") + "/"
    file_types.clear()
    files.clear()


def draw():
    global files
    try:
        contents = listdir(path)
        # Check if we are all the way to the top of the drive
        if path.endswith(":/"):
            files.clear()
        else:
            files = ["../"]
        # Get all files and directories
        for file in contents:
            if isdir(path + file) and file[0] != '.':
                files.append(file + "/")
            elif isfile(path + file) and "." in file and file[file.rfind("."):] in file_types:
                files.append(file)
        # Update ui
        global surface, line_h, scroll, max_scroll
        dim = pg.display.get_surface().get_size()
        line_h = max(50, dim[1] // 10)
        scroll = 0
        max_scroll = max(0, line_h * len(files) - dim[1])
        surface = pg.Surface((dim[0], line_h * len(files)))
        font = get_scaled_font(dim[0], line_h, get_widest_string(files))
        for i, name in enumerate(files):
            text = font.render(name, 1, (255, 255, 255))
            surface.blit(text, text.get_rect(center=(dim[0] // 2, int((i + .5) * line_h))))
            if i == selected:
                pg.draw.rect(surface, (200, 200, 0), (0, i * line_h, dim[0], line_h), 2)
        redraw()
        return True
    except PermissionError:
        if selected != -1:
            w = pg.display.get_surface().get_size()[0]
            pg.draw.rect(surface, (255, 0, 0), (0, selected * line_h, w, line_h), 2)
            redraw()
        return False


def redraw():
    d = pg.display.get_surface()
    dim = d.get_size()
    d.fill((0, 0, 0))
    d.blit(surface, (0, 0), area=((0, scroll), d.get_size()))
    if hover != -1:
        pos = pg.mouse.get_pos()
        img_dim = hover_img.get_size()
        d.blit(hover_img, [pos[i] if pos[i] < dim[i] // 2 else pos[i] - img_dim[i] for i in range(2)])


def choose_file(types=()):
    reset()

    global file_types
    file_types = types

    draw()
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                return
            elif e.type == VIDEORESIZE:
                pg.display.set_mode((e.w, e.h), RESIZABLE)
                draw()
            elif e.type == MOUSEBUTTONUP:
                global scroll
                if e.button == BUTTON_LEFT:
                    idx = (pg.mouse.get_pos()[1] + scroll) // line_h
                    if idx < len(files):
                        global selected
                        if idx == selected:
                            # Check if it is a folder
                            if files[idx][-1] == '/':
                                global path
                                temp = path
                                # Go back a folder
                                if files[idx] == "../":
                                    path = path[:path[:-1].rfind("/") + 1]
                                # Go forward a folder
                                else:
                                    path += files[idx]
                                if draw():
                                    w = pg.display.get_surface().get_size()[0]
                                    pg.draw.rect(surface, (0, 0, 0), (0, line_h * selected, w, line_h), 2)
                                    selected = -1
                                else:
                                    path = temp
                            else:
                                return path + files[idx]
                        else:
                            # Unselect and reselect
                            dim = pg.display.get_surface().get_size()
                            if selected != -1:
                                pg.draw.rect(surface, (0, 0, 0), (0, line_h * selected, dim[0], line_h), 2)
                            selected = idx
                            pg.draw.rect(surface, (200, 200, 0), (0, line_h * selected, dim[0], line_h), 2)
                            redraw()
                elif e.button == BUTTON_WHEELDOWN:
                    scroll += line_h // 2
                    if scroll > max_scroll:
                        scroll = max_scroll
                    redraw()
                elif e.button == BUTTON_WHEELUP:
                    scroll -= line_h // 2
                    if scroll < 0:
                        scroll = 0
                    redraw()
            elif e.type == MOUSEMOTION:
                global hover, hover_img
                pos = pg.mouse.get_pos()
                idx = (pos[1] + scroll) // line_h
                if idx != hover:
                    if 0 <= idx < len(files) and (files[idx].endswith(".png") or files[idx].endswith(".jpg")):
                        hover = idx
                        img_w = min(pg.display.get_surface().get_size()) // 5
                        hover_img = scale_to_fit(pg.image.load(path + files[idx]), w=img_w, h=img_w)
                    else:
                        hover = -1
                elif idx != -1:
                    redraw()
        pg.display.flip()
