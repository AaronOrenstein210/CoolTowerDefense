# Created on 27 January 2020
# Created by Nicole Brown

import data
from Abstract import Enemy

WINDOW = data.screen_w

ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5 = range(5)

class Enemy1(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_1, *pos, 1)


class Enemy2(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_2, *pos, 2)


class Enemy3(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_3, *pos, 3)


class Enemy4(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_4, *pos, 4)


class Enemy5(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_5, *pos, 5)
