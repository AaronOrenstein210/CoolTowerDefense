# Created on 27 January 2020
# Created by

# Defines a projectile
import pygame, sys, random

WINDOW = 500  # this is temporary


class Projectile:
    def __init__(self, t):  # t determines type of projectile
        self.type = t
        if self.type == 1:
            self.IMG = pygame.transform.scale(pygame.image.load('projectile1.png'), (WINDOW * 0.01, WINDOW * 0.01))
            self.damage = 3

    def getIMG(self):
        return self.IMG

    def get_damage(self):
        return self.damage

    def tick(self, dt):
        pass