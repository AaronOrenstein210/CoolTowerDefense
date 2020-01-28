# Created on 27 January 2020
# Created by Nicole Brown

import pygame


#  Defines an enemy
class Enemy:
    def __init__(self, image, x, y, strength):
        self.x = x   # x position
        self.y = y   # y position
        self.strength = strength
        self.image = pygame.image.load(image)

    #  This method reduces the strength by the damage amount
    def hit(self, damage):
        self.strength = self.strength - damage
        if self.strength < 0:
            self.strength = 0

    #   Move
    def move(self, x, y):
        self.x = x   # x position
        self.y = y   # y position

    # Draw
    def draw(self, display, w, h):
        if self.strength > 0:
            pass
            resize_image = pygame.transform.scale(self.image, (w, h))
            display.blit(resize_image, (self.x, self.y))

    # Gets position
    def getpos(self):
        return self.x, self.y