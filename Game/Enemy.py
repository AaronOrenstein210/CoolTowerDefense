# Created on 27 January 2020
# Created by Nicole Brown

import data
from Game.Abstract import Enemy

WINDOW = data.screen_w

ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5 = range(5)
ENEMY_ORDER = [ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5]


class Enemy1(Enemy):
    def __init__(self):
        super().__init__(ENEMY_1, dim=(.1, .1), velocity=.25, img="res/enemy1.png", strength=1)


class Enemy2(Enemy):
    def __init__(self):
        super().__init__(ENEMY_2, dim=(.1, .1), velocity=.375, img="res/enemy2.png", strength=2)


class Enemy3(Enemy):
    def __init__(self):
        super().__init__(ENEMY_3, dim=(.1, .1), velocity=.5, img="res/enemy3.png", strength=3)


class Enemy4(Enemy):
    def __init__(self):
        super().__init__(ENEMY_4, dim=(.1, .1), velocity=.75, img="res/enemy4.png", strength=4)


class Enemy5(Enemy):
    def __init__(self):
        super().__init__(ENEMY_5, dim=(.1, .1), velocity=1, img="res/enemy5.png", strength=5)
