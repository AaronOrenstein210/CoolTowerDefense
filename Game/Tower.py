# Created on 27 January 2020
# Created by Isabelle Early

from Game.Abstract import Projectile
import data
from Game.Abstract import Tower

TOWER_1, TOWER_2, BALLISTA, AAGUN = range(4)
TOWER_ORDER = [TOWER_1, TOWER_2, BALLISTA, AAGUN]


class DuckTower(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_1, pos=pos, dim=(.05, .05), img='res/duckTower1.png', cooldown=1000, cost=25)
        # radius
        self.range = 0.29

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1.5, dim=(.05, .05), damage=1, img="res/baseProj.png")


class DuckTower2(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_2, pos=pos, dim=(.05, .05), img="res/duckTower2.png", cooldown=500, cost=50)
        # radius
        self.range = 0.29

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=2.5, dim=(.025, .025), damage=1, img="res/smallProj.png")


class DuckTowerAA(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(AAGUN, pos=pos, dim=(.1, .1), img="res/duckAAGun.png", cooldown=200, cost=100)
        # radius
        self.range = 0.7

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1, dim=(.04, .04), damage=1, img="res/AAProj.png")


class DuckTowerBallista(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BALLISTA, pos=pos, dim=(.1, .1), img="res/duckTowerBallista.png", cooldown=1500, cost=175)
        # radius
        self.range = 0.43

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.77, dim=(.05, .05), damage=2, img="res/ballistaProj.png")