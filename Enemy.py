# Created on 27 January 2020
# Created by Nicole Brown

import data
from Abstract import Enemy

WINDOW = data.screen_w

ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5 = range(5)


class Enemy1(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_1, pos=pos, dim=(.1, .1), velocity=.25, img="res/enemy1.png")


class Enemy2(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_2, pos=pos, dim=(.1, .1), velocity=.375, img="res/enemy2.png")


class Enemy3(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_3, pos=pos, dim=(.1, .1), velocity=.5, img="res/enemy3.png")


class Enemy4(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_4, pos=pos, dim=(.1, .1), velocity=.75, img="res/enemy4.png")


class Enemy5(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_5, pos=pos, dim=(.1, .1), velocity=1, img="res/enemy5.png")
