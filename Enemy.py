# Created on 27 January 2020
# Created by Nicole Brown

import pygame
import data


#  Defines an enemy
class Enemy:
    def __init__(self, x, y, strength):
        self.x = x  # x position
        self.y = y  # y position
        self.path = 0
        self.progress = 0
        self.strength = strength
        if self.strength == 1:
            self.image = pygame.transform.scale(pygame.image.load("enemy1.png"), (int(data.screen_w * .05), int(data.screen_w * .05)))
        elif self.strength == 2:
            self.image = pygame.transform.scale(pygame.image.load("enemy2.png"), (int(data.screen_w * .05), int(data.screen_w * .05)))
        elif self.strength == 3:
            self.image = pygame.transform.scale(pygame.image.load("enemy3.png"), (int(data.screen_w * .05), int(data.screen_w * .05)))
        if self.strength == 1:
            self.velocity = 5    # 5% of screen width per second (20 seconds to move across the screen)
        elif self.strength == 2:
            self.velocity = 10   # 10% of screen width per second (10 seconds to move across the screen)
        elif self.strength == 3:
            self.velocity = 20   # 20% of screen width per second (5 seconds to move across the screen)

    #  This method reduces the strength by the damage amount
    def hit(self, damage):
        self.strength = self.strength - damage
        if self.strength < 0:
            self.strength = 0

    #   Move
    def move(self, x, y):
        self.x = x  # x position
        self.y = y  # y position

    # Gets position
    def getpos(self):
        return self.x, self.y

    # Returns image
    def return_image(self):
        return self.image

    # Gets Velocity
    def get_velocity(self):
        return self.velocity
