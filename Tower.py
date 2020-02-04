# Created on 27 January 2020
# Created by Isabelle Early

import Projectile
from Enemy import Enemy
import pygame
import math
import data

WINDOW = data.screen_w
# Defines a tower


class Tower:
    def __init__(self, t, x, y):  # t is a variable determining the type of tower
        self.type = t
        self.pos = (x, y)

        if self.type == 1:
            self.IMG = pygame.transform.scale(pygame.image.load('duckTower1.png'), (WINDOW*0.05, WINDOW*0.05))
            # radius
            self.range = 0.29*WINDOW
            self.countdown = 1000
        elif self.type == 2:
            self.IMG = pygame.transform.scale(pygame.image.load('duckTower2.png'), (WINDOW*0.05, WINDOW*0.05))
            # radius
            self.range = 0.29*WINDOW
            self.countdown = 500
        elif self.type == 3:
            self.IMG = pygame.transform.scale(pygame.image.load('duckTowerBallista.png'), (WINDOW*0.05, WINDOW*0.05))
            # radius
            self.range = 0.43*WINDOW
            self.countdown = 3000
        elif self.type == 4:
            self.IMG = pygame.transform.scale(pygame.image.load('duckAAGun.png'), (WINDOW*0.05, WINDOW*0.05))
            # radius
            self.range = 0.7*WINDOW
            self.countdown = 2130

    def shoot(self, enemy):  # given an enemy, shoots at them
        proj = Projectile.Projectile(self.type)
        pos = enemy.getpos()
        if self.withinRange(pos[0], pos[1]):
            enemy.hit(proj.getDamage())
            proj.animate(self.pos, pos)

    def getIMG(self):
        return self.IMG

    def getAngle(self, x, y):
        ratio = (self.pos[y] - y) / (self.pos[0] - x)
        return math.atan(ratio)

    def withinRange(self, x, y):  # given a position, returns whether that position is within range
        xVal = self.pos[0] - x
        yVal = self.pos[1] - y
        dist = (xVal**2 + yVal**2)**0.5
        if dist <= self.range:
            return True
        return False

    def tick(self, dt):
        self.countdown -= 1
        en = Enemy(0, 0, 1)  # get nearby enemy somehow
        if self.countdown == 0:
            self.shoot(en)
        data.lvlDriver.tick()  # ?