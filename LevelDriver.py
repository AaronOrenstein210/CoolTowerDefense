# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import LevelReader as Read
from LevelReader import *
import pygame as pg
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
        self.enemies, self.towers, self.projectiles = [Enemy1(self.start)], [
            DuckTower(x=rand[0] * data.screen_w, y=rand[1] * data.screen_w)], []

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
        d.blit(self.lr.surface, (0, 0))
        for i in self.enemies:
            d.blit(i.image, (i.x, i.y))
        for i in self.towers:
            d.blit(i.IMG, (i.pos[0], i.pos[1]))
        for i in self.projectiles:
            d.blit(i.IMG, (i.pos[0], i.pos[1]))

    def setStart(self, pos):
        self.start = pos

    def reset(self):
        pass
