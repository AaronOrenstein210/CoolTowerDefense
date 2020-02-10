# Created on 27 January 2020
# Created by Nicole Brown

import pygame


#  Defines an enemy
class Enemy:
    def __init__(self, pos, strength):
        self.pos = pos
        self.strength = strength
        if self.strength == 1:
            self.img = pygame.transform.scale(pygame.image.load("enemy1.png"))
            self.v = 5  # 5% of screen width per second (20 seconds to move across the screen)
        elif self.strength == 2:
            self.img = pygame.transform.scale(pygame.image.load("enemy2.png"))
            self.v = 10  # 10% of screen width per second (10 seconds to move across the screen)
        elif self.strength == 3:
            self.img = pygame.transform.scale(pygame.image.load("enemy3.png"))
            self.v = 20  # 20% of screen width per second (5 seconds to move across the screen)
        elif self.strength == 4:
            self.img = pygame.transform.scale(pygame.image.load("enemy4.png"))
            self.v = 30  # 30% of screen width per second
        elif self.strength == 5:
            self.img = pygame.transform.scale(pygame.image.load("enemy5.png"))
            self.v = 40  # 40% of screen width per second

    #  This method reduces the strength by the damage amount
    def hit(self, damage):
        self.strength = self.strength - damage
        if self.strength < 0:
            self.strength = 0
        return self.strength

    #   Move method
    def move(self, x, y):
        self.pos = (x, y)

    # Gets position
    def getpos(self):
        return self.pos

    # Returns image
    def return_image(self):
        return self.img

    # Gets Velocity
    def get_velocity(self):
        return self.v


class Enemy1(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos, 1)


class Enemy2(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos, 2)


class Enemy3(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos, 3)


class Enemy4(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos, 4)


class Enemy5(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(pos, 5)
