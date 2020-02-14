# Created on 27 January 2020
# Created by Isabelle Early

import Projectile
import pygame
import data
from Abstract import Tower

TOWER_1, TOWER_2, BALLISTA, AAGUN = range(4)
WINDOW = data.screen_w


# Defines a tower

class DuckTower(Tower):
    def __init__(self, **kwargs):
        super().__init__(TOWER_1, **kwargs)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckTower1.png'),
                                          (int(WINDOW * 0.05), int(WINDOW * 0.05)))
        # radius
        self.range = 0.29 * WINDOW
        self.countdown = 1000

    def shoot(self, enemy):
        proj = Projectile.Projectile1(self.pos[0], self.pos[1])
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        proj.tick()
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def restartCount(self):
        self.countdown = 1000

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]  # change this
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)


class DuckTower2(Tower):
    def __init__(self, **kwargs):
        super().__init__(TOWER_2, **kwargs)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckTower2.png'), (WINDOW * 0.05, WINDOW * 0.05))
        # radius
        self.range = 0.29 * WINDOW
        self.countdown = 500

    def shoot(self, enemy):
        proj = Projectile.Projectile2(self.pos[0], self.pos[1])
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        proj.tick()
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def restartCount(self):
        self.countdown = 500

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)


class DuckTowerAA(Tower):
    def __init__(self, **kwargs):
        super().__init__(AAGUN, **kwargs)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckAAGun.png'), (WINDOW * 0.05, WINDOW * 0.05))
        # radius
        self.range = 0.7 * WINDOW
        self.countdown = 2130

    def shoot(self, enemy):
        proj = Projectile.Projectile3(self.pos[0], self.pos[1])
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        proj.tick()
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def restartCount(self):
        self.countdown = 2130

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)


class DuckTowerBallista(Tower):
    def __init__(self, **kwargs):
        super().__init__(BALLISTA, **kwargs)
        self.IMG = pygame.transform.scale(pygame.image.load('res/duckTowerBallista.png'),
                                          (WINDOW * 0.05, WINDOW * 0.05))
        # radius
        self.range = 0.43 * WINDOW
        self.countdown = 1220

    def shoot(self, enemy):
        proj = Projectile.Projectile4(self.pos[0], self.pos[1])
        epos = enemy.getpos()
        proj.setAngle(self.getAngle(epos[0], epos[1]))
        proj.tick()
        if self.withinRange(epos[0], epos[1]):
            enemy.hit(proj.getDamage())

    def restartCount(self):
        self.countdown = 1220

    def tick(self, dt):
        self.countdown -= dt
        if len(data.lvlDriver.enemies) > 0:
            en = data.lvlDriver.enemies[0]
            if self.countdown <= 0:
                self.restartCount()
                self.shoot(en)
