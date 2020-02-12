# Created on 27 January 2020
# Created by Isabelle Early

import Projectile
import pygame
import math
import data

WINDOW = data.screen_w
# Defines a tower


class Tower:
    def __init__(self, x, y):  # t is a variable determining the type of tower
        self.pos = (x, y)
        self.IMG = None

    def shoot(self, enemy):  # given an enemy, shoots at them
        pass

    def getIMG(self):
        pass

    def getAngle(self, x, y):
        ratio = (self.pos[1] - y) / (self.pos[0] - x)
        return math.atan(ratio)

    def withinRange(self, x, y, r):
        xval = self.pos[0] - x
        yval = self.pos[1] - y
        dist = (xval**2 + yval**2)**0.5
        if dist <= r:
            return True
        return False

    def restartCount(self):
        pass

    def tick(self, dt):
        pass


class DuckTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckTower1.png'), (int(WINDOW * 0.05), int(WINDOW * 0.05)))
        # radius
        self.range = 0.29 * WINDOW
        self.countdown = 1000

    def shoot(self, enemy):
        proj = Projectile.Projectile1(self.pos[0], self.pos[1])
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def getIMG(self):
        return self.IMG

    def getAngle(self, x, y):
        super().getAngle(x, y)

    def withinRange(self, x, y):
        super().withinRange(x, y, self.range)

    def restartCount(self):
        self.countdown = 1000

    def tick(self, dt):
        self.countdown -= dt
        en = None
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]  # change this
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)


class DuckTower2(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckTower2.png'), (WINDOW * 0.05, WINDOW * 0.05))
        # radius
        self.range = 0.29 * WINDOW
        self.countdown = 500

    def shoot(self, enemy):
        proj = Projectile.Projectile2(self.pos[0], self.pos[1])  # change
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def getIMG(self):
        return self.IMG

    def getAngle(self, x, y):
        super().getAngle(x, y)

    def withinRange(self, x, y):
        super().withinRange(x, y, self.range)

    def restartCount(self):
        self.countdown = 500

    def tick(self, dt):
        self.countdown -= dt
        en = data.lvlDriver.enemies[0]
        if self.countdown <= 0:
            self.restartCount()
            self.shoot(en)


class DuckTowerAA(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckAAGun.png'), (WINDOW * 0.05, WINDOW * 0.05))
        # radius
        self.range = 0.7 * WINDOW
        self.countdown = 2130

    def shoot(self, enemy):
        proj = Projectile.Projectile3(self.pos[0], self.pos[1])  # change
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def getIMG(self):
        return self.IMG

    def getAngle(self, x, y):
        super().getAngle(x, y)

    def withinRange(self, x, y):
        super().withinRange(x, y, self.range)

    def restartCount(self):
        self.countdown = 2130

    def tick(self, dt):
        self.countdown -= dt
        en = data.lvlDriver.enemies[0]
        if self.countdown <= 0:
            self.restartCount()
            self.shoot(en)


class DuckTowerBallista(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckTowerBallista.png'), (WINDOW * 0.05, WINDOW * 0.05))
        # radius
        self.range = 0.43 * WINDOW
        self.countdown = 1220

    def shoot(self, enemy):
        proj = Projectile.Projectile4(self.pos[0], self.pos[1])  # change
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def getIMG(self):
        return self.IMG

    def getAngle(self, x, y):
        super().getAngle(x, y)

    def withinRange(self, x, y):
        super().withinRange(x, y, self.range)

    def restartCount(self):
        self.countdown = 1220

    def tick(self, dt):
        self.countdown -= dt
        en = data.lvlDriver.enemies[0]
        if self.countdown <= 0:
            self.restartCount()
            self.shoot(en)
