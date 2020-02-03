# Created on 27 January 2020
# Created by Nicole Brown

import pygame
import data


#  Defines an enemy
class Enemy:
    def __init__(self, x, y, strength):
        self.x = x   # x position
        self.y = y   # y position
        self.strength = strength
        if self.strength == 1:
            self.image = data.resize(pygame.image.load("enemy1.png"))
        elif self.strength == 2:
            self.image = data.resize(pygame.image.load("enemy2.png"))
        elif self.strength == 3:
            self.image = data.resize(pygame.image.load("enemy3.png"))

    #  This method reduces the strength by the damage amount
    def hit(self, damage):
        self.strength = self.strength - damage
        if self.strength < 0:
            self.strength = 0

    #   Move
    def move(self, x, y):
        self.x = x   # x position
        self.y = y   # y position

    # Gets position
    def getpos(self):
        return self.x, self.y

    # Returns image
    def return_image(self):
        return self.image
