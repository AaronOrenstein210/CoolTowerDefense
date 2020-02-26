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
        super().__init__(TOWER_1, pos=pos, dim=(.05, .05), img='res/duckTower1.png', cooldown=1000)
        # radius
        self.range = 0.29 * WINDOW

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.3, dim=(.05, .05), damage=1, img="res/baseProj.png")


class DuckTower2(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_2, pos=pos, dim=(.05, .05), img="res/duckTower2.png", cooldown=500)
        # radius
        self.range = 0.29 * WINDOW

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.3, dim=(.05, .05), damage=1, img="res/baseProj.png")


class DuckTowerAA(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(AAGUN, pos=pos, dim=(.05, .1), img="res/duckAAGun.png", cooldown=2000)
        # radius
        self.range = 0.7 * WINDOW

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.3, dim=(.05, .05), damage=1, img="res/baseProj.png")


class DuckTowerBallista(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BALLISTA, pos=pos, dim=(.1, .1), img="res/duckTowerBallista.png", cooldown=1500)
        # radius
        self.range = 0.43 * WINDOW

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.3, dim=(.05, .05), damage=1, img="res/baseProj.png")
