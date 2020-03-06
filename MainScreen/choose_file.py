# Created on 5 March 2020
from os import listdir, getcwd
from os.path import isfile, isdir
import pygame as pg
from pygame.locals import *
from data import get_scaled_font, get_widest_string, resize

path = "/"
surface = None
scroll = max_scroll = line_h = 0
selected = -1
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
    # Check if we are all the way to the top of the drive
    if path.endswith(":/"):
        files.clear()
    else:
        files = ["../"]
    # Get all files and directories
    for file in listdir(path):
        if isdir(path + file) and file[0] != '.':
            files.append(file + "/")
        elif isfile(path + file) and "." in file and file[file.rfind("."):] in file_types:
            files.append(file)
    global surface, line_h, scroll, max_scroll
    d = pg.display.get_surface()
    d.fill((0, 0, 0))
    dim = d.get_size()
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
    d.blit(surface, (0, 0))


def redraw():
    d = pg.display.get_surface()
    d.fill((0, 0, 0))
    d.blit(surface, (0, 0), area=((0, scroll), d.get_size()))


# TODO: hovering over shows image for .png/.jpg
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
                resize(e.w, e.h, False)
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
                                # Go back a folder
                                if files[idx] == "../":
                                    path = path[:path[:-1].rfind("/") + 1]
                                # Go forward a folder
                                else:
                                    path += files[idx]
                                selected = -1
                                draw()
                            else:
                                return path + files[idx]
                        else:
                            # Unselect and reselect
                            dim = pg.display.get_surface().get_size()
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
        pg.display.flip()
