# Created on 27 January 2020
# Created by Isabelle Early

from Abstract import Projectile
import pygame
import data
from Abstract import Tower

TOWER_1, TOWER_2, BALLISTA, AAGUN = range(4)
WINDOW = data.screen_w


# Defines a tower

class DuckTower(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_1, pos=pos, dim=(.05, .05), img='res/duckTower1.png')
        # radius
        self.range = 0.29 * WINDOW
        self.countdown = 1000

    def shoot(self, enemy):
        proj = self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))
        data.lvlDriver.projectiles.append(proj)

    def restartCount(self):
        self.countdown = 1000

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed= 2.5, dim=(.05, .05), damage=1, img="res/baseProj.png")


class DuckTower2(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_2, pos=pos, dim=(.20, .20), img="res/duckTower2.png")
        # radius
        self.range = 0.29 * WINDOW
        self.countdown = 500

    def shoot(self, enemy):
        proj = self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))
        data.lvlDriver.projectiles.append(proj)

    def restartCount(self):
        self.countdown = 250

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed= 1, dim=(.025, .025), damage=.25, img="res/smallProj.png")


class DuckTowerAA(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(AAGUN, pos=pos, dim=(.09, .1), img="res/duckAAGun.png")
        # radius
        self.range = 0.7 * WINDOW
        self.countdown = 2130

    def shoot(self, enemy):
        proj = self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))
        data.lvlDriver.projectiles.append(proj)

    def restartCount(self):
        self.countdown = 2130

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=4, dim=(.05, .05), damage=4, img="res/baseProj.png")


class DuckTowerBallista(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BALLISTA, pos=pos, dim=(.1, .1), img="res/duckTowerBallista.png")
        # radius
        self.range = 0.43 * WINDOW
        self.countdown = 1220

    def shoot(self, enemy):
        proj = self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))
        data.lvlDriver.projectiles.append(proj)

    def restartCount(self):
        self.countdown = 1220

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.77, dim=(.05, .05), damage=3, img="res/baseProj.png")
