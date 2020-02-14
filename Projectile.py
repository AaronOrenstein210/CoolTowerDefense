# Created on 27 January 2020
# Created by Isabelle Early
# Defines a projectile
import pygame
import data
import math
from Abstract import Projectile

WINDOW = data.screen_w


class Projectile1(Projectile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 0.3
        self.IMG = pygame.transform.scale(pygame.image.load('res/baseProj.png'),
                                            (int(WINDOW * 0.01), int(WINDOW * 0.01)))
        self.damage = 1


class Projectile2(Projectile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 0.3
        self.IMG = pygame.transform.scale(pygame.image.load('res/baseProj.png'), (WINDOW * 0.01, WINDOW * 0.01))
        self.damage = 2


class Projectile3(Projectile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 0.3
        self.IMG = pygame.transform.scale(pygame.image.load('res/smallProj.png'), (WINDOW * 0.01, WINDOW * 0.01))
        self.damage = 3


class Projectile4(Projectile):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 0.3
        self.IMG = pygame.transform.scale(pygame.image.load('smallProj.png'), (WINDOW * 0.01, WINDOW * 0.01))
        self.damage = 5

