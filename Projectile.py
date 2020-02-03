# Created on 27 January 2020
# Created by Isabelle Early
# Defines a projectile
import pygame, sys, random
import data

WINDOW = 500  # this is temporary


class Projectile:
    def __init__(self, t):  # t determines type of projectile
        self.type = t
        if self.type == 1:
            self.IMG = data.resize(pygame.image.load('projectile1.png'))
            self.damage = 1
        elif self.type == 2:
            self.IMG = data.resize(pygame.image.load('projectile2.png'))
            self.damage = 2
        elif self.type == 3:
            self.IMG = data.resize(pygame.image.load('projectile3.png'))
            self.damage = 3
        elif self.type == 4:
            self.IMG = data.resize(pygame.image.load('projectile4.png'))
            self.damage = 4

    def getIMG(self):
        return self.IMG

    def getDamage(self):
        return self.damage

    def tick(self, dt):
        pass
