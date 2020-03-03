# Created on 27 January 2020
# Created by Isabelle Early

from random import randint
from Game.Abstract import Projectile
import data
from Game.Abstract import Tower, Upgrade

TOWER_1, TOWER_2, BALLISTA, AAGUN, BFG = range(5)
TOWER_ORDER = [TOWER_1, TOWER_2, AAGUN, BALLISTA, BFG]


class DuckTower(Tower):
    upgrades = [Upgrade(cost=30, img="",
                        description="Sharper projectiles tear through multiple enemies\nIncreases damage by 1"),
                Upgrade(cost=50, img="",
                        description="Making the tower taller allows for more enemies to be seen\n"
                                    "Increases range by 20%"),
                Upgrade(cost=80, img="",
                        description="More efficient engines speed up fire rate appreciably\n"
                                    "Fire rate is increased by 50%"),
                Upgrade(cost=120, img="",
                        description="Matter manipulation technology allows projectiles to be duplicated "
                                    "when shot\n50% chance to shoot two projectiles instead of one")]

    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_1, pos=pos, dim=(.05, .05), img='res/duckTower1.png', cooldown=750, cost=25,
                         shoot_range=.2)

    def upgrade(self):
        self.upgrade_lvl += 1
        if self.upgrade_lvl == 0:
            # self.modify_projectile(self.result)
            self.P1.addDamage()
        elif self.upgrade_lvl == 1:
            self.range *= 1.2
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.5
        elif self.upgrade_lvl == 3:
            ran = randint(0, 2)
            if ran == 0:
                self.P1.addDamage()

    def modify_projectile(self, projectile):
        if self.upgrade_lvl >= 0:
            projectile.damage += 1

    def shoot(self, enemy):
        self.result = [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]
        if self.upgrade_lvl >= 3 and randint(0, 1) == 0:
            self.result.append(self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos)))
        return self.result

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.5, dim=(.05, .05), damage=1, img="res/baseProj.png")

        def addDamage(self):
            self.damage += 1


class DuckTower2(Tower):
    upgrades = [Upgrade(cost=50, img="",
                        description="Put your duck through a strict training regimen, increasing its strength"
                                    "\nIncreases range by 20%"),
                Upgrade(cost=80, img="",
                        description="Making the tower taller allows for more enemies to be seen\n"
                                    "Increases range by 20%"),
                Upgrade(cost=100, img="",
                        description="More efficient engines speed up fire rate appreciably\n"
                                    "Fire rate is increased by 50%"),
                Upgrade(cost=140, img="",
                        description="Matter manipulation technology allows projectiles to be duplicated "
                                    "when shot\n50% chance to shoot two projectiles instead of one")]

    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_2, pos=pos, dim=(.05, .05), img="res/duckTower2.png", cooldown=400, cost=50,
                         shoot_range=.25)

    def upgrade(self):
        self.upgrade_lvl += 1
        if self.upgrade_lvl == 0:
            # self.modify_projectile(self.result)
            self.P1.addDamage()
        elif self.upgrade_lvl == 1:
            self.range *= 1.2
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.5
        elif self.upgrade_lvl == 3:
            ran = randint(0, 2)
            if ran == 0:
                self.P1.addDamage()

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=1, dim=(.025, .025), damage=1, img="res/smallProj.png")

        def addDamage(self):
            self.damage += 1


class DuckTowerAA(Tower):
    upgrades = [Upgrade(cost=30, img="",
                        description="Microwaved grapes explode, damaging even more enemies\nIncreases damage by 3"),
                Upgrade(cost=50, img="",
                        description="Your duck suddenly and unexpectedly grows to monstrous heights\n"
                                    "Increases range by 20%"),
                Upgrade(cost=80, img="",
                        description="More efficient engines speed up fire rate appreciably\n"
                                    "Fire rate is increased by 50%"),
                Upgrade(cost=120, img="",
                        description="Matter manipulation technology allows projectiles to be duplicated "
                                    "when shot\n50% chance to shoot two projectiles instead of one")]

    def __init__(self, pos=(0, 0)):
        super().__init__(AAGUN, pos=pos, dim=(.04, .04), img="res/duckAAGun.png", cooldown=200, cost=100,
                         shoot_range=.15)

    def upgrade(self):
        self.upgrade_lvl += 1
        if self.upgrade_lvl == 0:
            # self.modify_projectile(self.result)
            self.P1.addDamage()
        elif self.upgrade_lvl == 1:
            self.range *= 1.2
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.5
        elif self.upgrade_lvl == 3:
            ran = randint(0, 2)
            if ran == 0:
                self.P1.addDamage()

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.33, dim=(.04, .04), damage=1, img="res/AAProj.png")

        def addDamage(self):
            self.damage += 1


class DuckTowerBallista(Tower):
    upgrades = [Upgrade(cost=200, img="",
                        description="Frozen grapes tear through multiple enemies\nIncreases damage by 5"),
                Upgrade(cost=500, img="",
                        description="You get in good standing with your weapon dealership\n"
                                    "Additional towers will be 50 coins cheaper"),
                Upgrade(cost=300, img="",
                        description="Your duck eats some radioactive grapes, and gains super speed\n"
                                    "Fire rate is increased by 50%"),
                Upgrade(cost=120, img="",
                        description="A wormhole appears, allowing your duck to summon grapes at a higher rate\n "
                                    "Fire rate is increased even more")]

    def __init__(self, pos=(0, 0)):
        super().__init__(BALLISTA, pos=pos, dim=(.1, .1), img="res/duckTowerBallista.png", cooldown=1250, cost=175,
                         shoot_range=.3)

    def upgrade(self):
        self.upgrade_lvl += 1
        if self.upgrade_lvl == 0:
            # self.modify_projectile(self.result)
            self.P1.addDamage(5)
        elif self.upgrade_lvl == 1:
            self.cost -= 50
        elif self.upgrade_lvl == 2:
            self.cooldown //= 1.5
        elif self.upgrade_lvl == 3:
            self.cooldown //= 1.3

    def shoot(self, enemy):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.25, dim=(.05, .05), damage=2, img="res/ballistaProj.png")

        def addDamage(self, num):
            self.damage += num

class DuckTowerBFG(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BFG, pos=pos, dim=(.1,.1), img="res/bfgpixel.png", cooldown=1000, cost=1,
                         shoot_range=.4)

    def shoot(self, enemy):
        return [self.P1(self.pos,data.get_angle_pixels(self.pos, enemy.pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos=pos, angle=angle, speed=.4, dim=(.1, .1), damage=50000, img="res/bfgProj.png")