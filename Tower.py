# Created on 27 January 2020
# Created by Isabelle Early

from Projectile import Projectile
from Enemy import Enemy
import pygame, sys, random
import math
import data

WINDOW = 500  # this is temporary
# Defines a tower

class Tower:
    def __init__(self, t, x, y):  # t is a variable determining the type of tower
        self.type = t
        self.pos = (x, y)
        if self.type == 1:
            self.IMG = data.resize(pygame.image.load('tower1.png'))
            self.range = 0.1*WINDOW  # radius

    def shoot(self, enemy):  # given an enemy, shoots at them
        projectile = Projectile(self.type)
        pos = enemy.getPos()
        if self.withinRange(pos[0], pos[1]):
            enemy.hit(projectile.getDamage())
            # probably add animation later

    def getIMG(self):
        return self.IMG

    def getAngle(self, x, y):
        ratio = (self.pos[y] - y) / (self.pos[0] - x)
        return math.atan(ratio)

    def withinRange(self, x, y):  # given a position, returns whether that position is within range
        xVal = self.pos[0] - x
        yVal = self.pos[1] - y
        dist = (xVal**2 + yVal**2)**0.5
        if dist <= self.range :
            return True
        return False

    def tick(self, dt):
        pass
