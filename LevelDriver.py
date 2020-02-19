# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import LevelReader as Read
from LevelReader import *
import pygame as pg
from pygame.locals import *
from Enemy import Enemy1
from Tower import DuckTower
from random import uniform
import data


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    def __init__(self):
        self.data = data
        self.lr = Read()
        rand = rand_pos()
        temp = rand_pos()
        # self.start = self.lr.paths[0].get_start()
        self.start = temp
        self.enemies = [Enemy1(self.start)]
        self.towers = [DuckTower(pos=(rand[0] * data.screen_w, rand[1] * data.screen_w))]
        self.projectiles = []

    # Called every iteration of the while loop
    def tick(self, dt):
        # Move all enemies, and update towers/projectiles
        for i in self.enemies:
            if not self.lr.move(i, dt):
                self.enemies.remove(i)
        for i in self.towers:
            i.tick(dt)
        for i in self.projectiles:
            i.tick(dt)
        # Redraw the screen
        self.draw()

    # Draw the screen
    def draw(self):
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        d.blit(self.lr.surface, (data.off_x, data.off_y))
        for i in self.enemies + self.towers + self.projectiles:
            img_rect = i.blit_img.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                   int(i.pos[1] * data.screen_w) + data.off_y))
            d.blit(i.blit_img, img_rect)

    def setStart(self, pos):
        self.start = pos

    def input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            if pos[0] >= self.rectX and pos[1] >= self.rectY and pos[1]:  # other edges of the box will be the side and bottom of the screen
                self.click(pos[0], pos[1])

    def click(self, x, y):  # probably include this in the input method
        if x > self.rectX and y > self.rectY :  # replace with a bunch of different conditionals describing which box the mouse is over
            pass  # set a tower


    def reset(self):
        pass
