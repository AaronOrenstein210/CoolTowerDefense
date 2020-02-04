# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import LevelReader as Read
import pygame as pg
from random import uniform
from MyTower import Tower1, Tower2, Ballista, AAGun
from MyEnemy import Enemy1
import data


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    def __init__(self):
        self.enemies = [Enemy1(rand_pos())]
        self.towers = [Tower1(rand_pos()), Tower2(rand_pos()), Ballista(rand_pos()), AAGun(rand_pos())]
        self.projectiles = []
        self.lr = Read()

        # Called every iteration of the while loop

    def tick(self, dt):
        # Move all enemies, and update towers/projectiles
        for i in self.enemies:
            if not self.lr.move(i, dt):
                self.enemies.remove(i)
        for i in self.towers:
            self.projectiles += i.tick(dt)
        for i in self.projectiles:
            if not i.tick(dt):
                self.projectiles.remove(i)
        # Redraw the screen
        self.draw()

    # Draw the screen
    def draw(self):
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        d.blit(self.lr.surface, (data.off_x, data.off_y))
        # TODO: The img rect will probably just be replaced by a rectangle in the object itself
        for i in self.enemies + self.towers + self.projectiles:
            img_rect = i.image.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                int(i.pos[1] * data.screen_w) + data.off_y))
            d.blit(i.image, img_rect)
