# Created on 27 January 2020
# Created by Isabelle Early
# Defines a projectile
import pygame
import data
import math

WINDOW = data.screen_w


class Projectile:
    def __init__(self, t, x, y):  # t determines type of projectile
        self.type = t
        self.speed = 0.3
        self.angle = 0
        self.pos = (x, y)
        if self.type == 1:
            self.IMG = pygame.transform.scale(pygame.image.load('projectile1.png'), (WINDOW*0.01, WINDOW*0.01))
            self.damage = 1
        elif self.type == 2:
            self.IMG = pygame.transform.scale(pygame.image.load('projectile2.png'), (WINDOW*0.01, WINDOW*0.01))
            self.damage = 2
        elif self.type == 3:
            self.IMG = pygame.transform.scale(pygame.image.load('projectile3.png'), (WINDOW*0.01, WINDOW*0.01))
            self.damage = 3
        elif self.type == 4:
            self.IMG = pygame.transform.scale(pygame.image.load('projectile4.png'), (WINDOW*0.01, WINDOW*0.01))
            self.damage = 5

    def getIMG(self):
        return self.IMG

    def setAngle(self, ang):
        self.angle = ang

    def getDamage(self):
        return self.damage

    def tick(self, dt):
        d = (self.speed * dt) / 1000
        dx = d * math.cos(self.angle)
        dy = d * math.sin(self.angle)
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        return 0 <= self.pos[0] <= 1 and 0 <= self.pos[1] <= 1