# Created on 27 January 2020
# Created by Nicole Brown

import data
from Game.Abstract import Enemy

WINDOW = data.screen_w

ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5, ENEMY_6 = range(6)
ENEMY_ORDER = [ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5, ENEMY_6]


class Enemy1(Enemy):
    def __init__(self):
        super().__init__(ENEMY_1, w=.1, velocity=.2, img="res/enemy1.png")
        self.color = (255, 0, 0)

    def die(self):
        return []


class Enemy2(Enemy):
    def __init__(self):
        super().__init__(ENEMY_2, w=.1, velocity=.325, img="res/enemy2.png")
        self.color = (0, 0, 255)


class Enemy3(Enemy):
    def __init__(self):
        super().__init__(ENEMY_3, w=.1, velocity=.433, img="res/enemy3.png")
        self.color = (0, 255, 0)


class Enemy4(Enemy):
    def __init__(self):
        super().__init__(ENEMY_4, w=.1, velocity=.6, img="res/enemy4.png")
        self.color = (255, 255, 0)


class Enemy5(Enemy):
    def __init__(self):
        super().__init__(ENEMY_5, w=.1, velocity=1, img="res/enemy5.png")
        self.color = (255, 150, 150)


class Enemy6(Enemy):
    def __init__(self):
        super().__init__(ENEMY_6, w=.1, velocity=.1, img="res/tankClass.png", hp=10)
        self.color = (0, 187, 212)

    def die(self):
        super().die()
        return [ENEMY_5] * 2
