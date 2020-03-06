# Created on 27 January 2020
# Created on 27 January 2020
# Created by Stinky

from pygame.locals import *
import pygame as pg
import data
from MainScreen.choose_level import choose_level

pg.init()
# Channels - 0 = game music, 1 = laser sound, 2 = enemy sound
pg.mixer.init()
data.init()
pg.display.set_mode((data.MIN_W, data.MIN_W), RESIZABLE)


# Main function which helps specific ui screens release their variables
def main():
    while choose_level():
        pg.mixer.Channel(0).play(data.music_audio, -1)
        run_level()
        for i in range(3):
            pg.mixer.Channel(i).stop()


# Runs current level
def run_level():
    time = pg.time.get_ticks()
    while True:
        dt = pg.time.get_ticks() - time
        time += dt
        dt = min(20, dt)
        for e in pg.event.get():
            if e.type == QUIT:
                data.calculate_dimensions(False)
                return
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, True)
                data.lvlDriver.resize()
            else:
                if not data.lvlDriver.input(e):
                    data.calculate_dimensions(False)
                    return
        data.lvlDriver.tick(dt)
        pg.display.flip()


main()
