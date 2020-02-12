# Created on 27 January 2020
# Created by Isabelle Early
# Defines a projectile
import pygame
import data
import math

WINDOW = data.screen_w


class Projectile:
    def __init__(self, x, y):  # t determines type of projectile
        self.pos = (x, y)

    def getIMG(self):
        pass

    def setAngle(self, ang):
        pass

    def getDamage(self):
        pass

    def tick(self, dt):
        pass


class Projectile1(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0.3
        self.angle = 0
        self.IMG = pygame.transform.scale(pygame.image.load('res/projectile1.png'), (int(WINDOW * 0.01), int(WINDOW * 0.01)))
        self.damage = 1

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


class Projectile2(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0.3
        self.angle = 0
        self.IMG = pygame.transform.scale(pygame.image.load('res/projectile2.png'), (WINDOW * 0.01, WINDOW * 0.01))
        self.damage = 2

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


class Projectile3(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0.3
        self.angle = 0
        self.IMG = pygame.transform.scale(pygame.image.load('res/projectile3.png'), (WINDOW * 0.01, WINDOW * 0.01))
        self.damage = 3

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


class Projectile4(Projectile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 0.3
        self.angle = 0
        self.IMG = pygame.transform.scale(pygame.image.load('projectile4.png'), (WINDOW * 0.01, WINDOW * 0.01))
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
