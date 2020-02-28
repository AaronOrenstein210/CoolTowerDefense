# Created on 27 January 2020
# Created by Isabelle Early

from Game.Abstract import Projectile
import data
from Game.Abstract import Tower

TOWER_1, TOWER_2, BALLISTA, AAGUN = range(4)
TOWER_ORDER = [TOWER_1, TOWER_2, AAGUN, BALLISTA]


class DuckTower(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_1, pos=pos, dim=(.05, .05), img='res/duckTower1.png', cooldown=750, cost=25, range=.2)

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.5, dim=(.05, .05), damage=1, img="res/baseProj.png")


class DuckTower2(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_2, pos=pos, dim=(.05, .05), img="res/duckTower2.png", cooldown=400, cost=50, range=.25)

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1, dim=(.025, .025), damage=1, img="res/smallProj.png")


class DuckTowerAA(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(AAGUN, pos=pos, dim=(.1, .1), img="res/duckAAGun.png", cooldown=200, cost=100, range=.15)

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.33, dim=(.04, .04), damage=1, img="res/AAProj.png")


class DuckTowerBallista(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BALLISTA, pos=pos, dim=(.1, .1), img="res/duckTowerBallista.png", cooldown=1250, cost=175,
                         range=.3)

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.25, dim=(.05, .05), damage=2, img="res/ballistaProj.png")
