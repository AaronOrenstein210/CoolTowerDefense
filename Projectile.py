# Created on 27 January 2020
# Created by Isabelle Early
# Defines a projectile
import pygame
import data

WINDOW = data.screen_w


class Projectile:
    def __init__(self, t):  # t determines type of projectile
        self.type = t
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

    def getDamage(self):
        return self.damage

    def animate(self, startPos, endPos):
        pass

    def tick(self, dt):
        pass