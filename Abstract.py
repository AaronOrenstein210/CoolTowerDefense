import pygame
import math
import data

WINDOW = data.screen_w


class Tower:
    def __init__(self, idx, x=0, y=0):  # t is a variable determining the type of tower
        self.idx = idx
        self.pos = (x, y)
        self.IMG = None

    def shoot(self, enemy):  # given an enemy, shoots at them
        pass

    def getIMG(self):
        return self.IMG

    def getAngle(self, x, y):
        ratio = (self.pos[1] - y) / (self.pos[0] - x)
        return math.atan(ratio)

    def withinRange(self, x, y, r):
        xval = self.pos[0] - x
        yval = self.pos[1] - y
        dist = (xval ** 2 + yval ** 2) ** 0.5
        if dist <= r:
            return True
        return False

    def restartCount(self):
        pass

    def tick(self, dt):
        pass


class Projectile:
    def __init__(self, x=0, y=0):  # t determines type of projectile
        self.pos = (x, y)
        self.IMG = None
        self.angle = 0  # default values
        self.damage = 0
        self.speed = 1

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


class Enemy:
    def __init__(self, idx, x, y, strength):
        self.idx = idx
        self.pos = (x, y)
        self.x = x
        self.y = y
        self.strength = strength
        self.path = 0
        self.progress = 0

        if self.strength == 1:
            self.image = pygame.transform.scale(pygame.image.load("res/enemy1.png"),
                                                (int(WINDOW * 0.05), int(WINDOW * 0.05)))
            self.velocity = 5  # 5% of screen width per second (20 seconds to move across the screen)
        elif self.strength == 2:
            self.image = pygame.transform.scale(pygame.image.load("res/enemy2.png"),
                                                (int(WINDOW * 0.05), int(WINDOW * 0.05)))
            self.velocity = 10  # 10% of screen width per second (10 seconds to move across the screen)
        elif self.strength == 3:
            self.image = pygame.transform.scale(pygame.image.load("res/enemy3.png"),
                                                (int(WINDOW * 0.05), int(WINDOW * 0.05)))
            self.velocity = 20  # 20% of screen width per second (5 seconds to move across the screen)
        elif self.strength == 4:
            self.image = pygame.transform.scale(pygame.image.load("res/enemy4.png"),
                                                (int(WINDOW * 0.05), int(WINDOW * 0.05)))
            self.velocity = 30  # 30% of screen width per second
        elif self.strength == 5:
            self.image = pygame.transform.scale(pygame.image.load("res/enemy5.png"),
                                                (int(WINDOW * 0.05), int(WINDOW * 0.05)))
            self.velocity = 40  # 40% of screen width per second

    #  This method reduces the strength by the damage amount
    def hit(self, damage):
        self.strength = self.strength - damage
        if self.strength < 0:
            self.strength = 0
        return self.strength

    def set_pos(self, x, y):
        self.pos = (x, y)

    # Gets position
    def getpos(self):
        return self.pos

    # Returns image
    def return_image(self):
        return self.image

    # Gets Velocity
    def get_velocity(self):
        return self.velocity
