# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import LevelReader as Read
import pygame as pg
from Enemy import Enemy
from Tower import Tower, DuckTower
from random import uniform
import data


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    def __init__(self):
        self.data = data
        rand1 = rand_pos()
        rand2 = rand_pos()
        self.enemies, self.towers, self.projectiles = [Enemy(rand1[0] * data.screen_w, rand1[1] * data.screen_w, 1)], [DuckTower(rand2[0] * data.screen_w, rand2[1] * data.screen_w)], []
        self.lr = Read()

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
