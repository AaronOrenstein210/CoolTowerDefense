# Created on 27 January 2020
# Created by Isabelle Early

from random import randint
from Game.Abstract import Projectile
import data
from Game.Abstract import Tower, Upgrade

TOWER_1, TOWER_2, BALLISTA, AAGUN, BFG = range(5)
TOWER_ORDER = [TOWER_1, TOWER_2, AAGUN, BALLISTA, BFG]


class DuckTower(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_1, pos=pos, w=.05, img='res/duckTower1.png', cooldown=750, cost=25,
                         shoot_range=.2)

    def get_upgrades(self):
        return [Upgrade(cost=30, img="res/duckTower1U1.png",
                        description="Sharper projectiles tear through multiple enemies\nIncreases damage by 1"),
                Upgrade(cost=50, img="",
                        description="Making the tower taller allows for more enemies to be seen\n"
                                    "Increases range by 20%"),
                Upgrade(cost=80, img="",
                        description="More efficient engines speed up fire rate appreciably\n"
                                    "Fire rate is increased by 50%"),
                Upgrade(cost=120, img="res/duckTower1U4.png",
                        description="Matter manipulation technology allows projectiles to be duplicated "
                                    "when shot\n50% chance to shoot two projectiles instead of one")]

    def upgrade(self):
        super().upgrade()
        if self.upgrade_lvl == 1:
            self.range *= 1.2
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.5

    def modify_projectile(self, projectile):
        if self.upgrade_lvl >= 0:
            projectile.damage += 1

    def shoot(self, enemy):
        result = [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]
        if self.upgrade_lvl >= 3 and randint(0, 1) == 0:
            result.append(self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos)))
        return result

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1, w=.05, damage=1, img="res/baseProj.png")


class DuckTower2(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_2, pos=pos, w=.05, img="res/duckTower2.png", cooldown=200, cost=50,
                         shoot_range=.25)

    def get_upgrades(self):
        return [Upgrade(cost=50, img="",
                        description="Put your duck through a strict training regimen, increasing its strength"
                                    "\nIncreases range by 20%"),
                Upgrade(cost=80, img="",
                        description="Making the tower taller allows for more enemies to be seen\n"
                                    "Increases range by 20%"),
                Upgrade(cost=100, img="res/duckTower2U3.png",
                        description="More efficient engines speed up fire rate appreciably\n"
                                    "Fire rate is increased by 50%"),
                Upgrade(cost=140, img="res/duckTower2U4.png",
                        description="Matter manipulation technology allows projectiles to be duplicated "
                                    "when shot\n50% chance to shoot two projectiles instead of one")]

    def upgrade(self):
        super().upgrade()
        if self.upgrade_lvl == 0 or self.upgrade_lvl == 1:
            self.range *= 1.2
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.5

    def modify_projectile(self, projectile):
        if self.upgrade_lvl >= 0:
            projectile.damage += 1

    def shoot(self, enemy):
        result = [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]
        if self.upgrade_lvl >= 3 and randint(0, 1) == 0:
            result.append(self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos)))
        return result

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1.5, w=.025, damage=1, img="res/smallProj.png")


class DuckTowerAA(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(AAGUN, pos=pos, w=.04, img="res/duckAAGun.png", cooldown=400, cost=100,
                         shoot_range=.3)

    def get_upgrades(self):
        return [Upgrade(cost=30, img="",
                        description="Microwaved grapes explode, damaging even more enemies\nIncreases damage by 1"),
                Upgrade(cost=50, img="",
                        description="Your duck suddenly and unexpectedly grows to monstrous heights\n"
                                    "Increases range by 20%"),
                Upgrade(cost=80, img="",
                        description="More efficient engines speed up fire rate appreciably\n"
                                    "Fire rate is increased by 50%"),
                Upgrade(cost=120, img="",
                        description="Matter manipulation technology allows projectiles to be duplicated "
                                    "when shot\n50% chance to shoot two projectiles instead of one")]

    def upgrade(self):
        super().upgrade()
        if self.upgrade_lvl == 1:
            self.range *= 1.2
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.5

    def modify_projectile(self, projectile):
        if self.upgrade_lvl >= 0:
            projectile.damage += 1

    def shoot(self, enemy):
        result = [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]
        if self.upgrade_lvl >= 3 and randint(0, 1) == 0:
            result.append(self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos)))
        return result

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.7, w=.04, damage=1, img="res/AAProj.png")


class DuckTowerBallista(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BALLISTA, pos=pos, w=.05, img="res/duckTowerBallista.png", cooldown=1250, cost=175,
                         shoot_range=.3)

    def get_upgrades(self):
        return [Upgrade(cost=120, img="",
                        description="A wormhole appears, allowing your duck to summon grapes at a higher rate\n "
                                    "Fire rate is increased by 30%"),
                Upgrade(cost=200, img="",
                        description="Frozen grapes tear through multiple enemies\nIncreases damage by 2"),
                Upgrade(cost=300, img="",
                        description="Your duck eats some radioactive grapes, and gains super speed\n"
                                    "Fire rate is increased by 50%")]

    def upgrade(self):
        super().upgrade()
        if self.upgrade_lvl == 0:
            self.cooldown //= 1.5
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.3

    def modify_projectile(self, projectile):
        if self.upgrade_lvl >= 1:
            projectile.damage += 2

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1, w=.08, damage=5, img="res/ballistaProj.png")


class DuckTowerBFG(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BFG, pos=pos, w=.1, img="res/bfgpixel.png", cooldown=1000, cost=1000,
                         shoot_range=.4)

    def get_upgrades(self):
        return [Upgrade(cost=100, img="",
                        description="2X fire rate"),
                Upgrade(cost=300, img="",
                        description="2X fire rate"),
                Upgrade(cost=1000, img="",
                        description="Range covers the whol screen")]

    def upgrade(self):
        super().upgrade()
        if self.upgrade_lvl == 0 or self.upgrade_lvl == 1:
            self.cooldown //= 2
        elif self.upgrade_lvl == 2:
            self.range = .75

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1, w=.09, damage=10, img="res/bfgProj.png")
