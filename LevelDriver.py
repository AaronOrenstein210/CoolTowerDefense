# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import LevelReader as Read
from Read import surface as bg
import pygame as pg


# Runs the level
class LevelDriver:
    def __init__(self):
        self.enemies = self.towers = self.projectiles = []
        self.lr = Read()
        self.mainSurface = pg.display.get_surface()

    # Called every iteration of the while loop
    def tick(self, dt):
        # Move all enemies, and update towers/projectiles
        for i in self.enemies:
            i.pos = self.lr.move(i.pos, i.d)
        for i in self.towers:
            i.tick()
        for i in self.projectiles:
            i.tick()
        # Redraw the screen
        self.draw()

    # Draw the screen
    def draw(self):
        self.mainSurface.blit(bg, (0, 0))
        for i in self.enemies:
            self.mainSurface.blit(i.image, (i.pos[0], i.pos[1]))
        for i in self.towers:
            self.mainSurface.blit(i.IMG, (i.pos[0], i.pos[1]))
        for i in self.projectiles:
            self.mainSurface.blit(i.IMG, (i.pos[0], i.pos[1]))
