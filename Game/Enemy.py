# Created on 27 January 2020
# Created by Nicole Brown

import data
from Game.Abstract import Enemy

WINDOW = data.screen_w

ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5 = range(5)
ENEMY_ORDER = [ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5]


class Enemy1(Enemy):
    def __init__(self):
        super().__init__(ENEMY_1, dim=(.1, .1), velocity=.2, img="res/enemy1.png", strength=1)
        self.color = (255, 0, 0)


class Enemy2(Enemy):
    def __init__(self):
        super().__init__(ENEMY_2, dim=(.1, .1), velocity=.325, img="res/enemy2.png", strength=2)
        self.color = (0, 0, 255)


class Enemy3(Enemy):
    def __init__(self):
        super().__init__(ENEMY_3, dim=(.1, .1), velocity=.433, img="res/enemy3.png", strength=3)
        self.color = (0, 255, 0)


class Enemy4(Enemy):
    def __init__(self):
        super().__init__(ENEMY_4, dim=(.1, .1), velocity=.6, img="res/enemy4.png", strength=4)
        self.color = (255, 255, 0)


class Enemy5(Enemy):
    def __init__(self):
        super().__init__(ENEMY_5, dim=(.1, .1), velocity=1, img="res/enemy5.png", strength=5)
        self.color = (255, 150, 150)
