# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import LevelReader as Read
import pygame as pg
from pygame.locals import *
from random import uniform, randint
from MyObjects import *
import data


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    def __init__(self):
        self.enemies = []
        self.towers = []  # [Tower1(rand_pos()), Tower2(rand_pos()), Ballista(rand_pos()), AAGun(rand_pos())]
        self.projectiles = []
        self.lr = Read()
        self.time = 0

        # Called every iteration of the while loop

    # Returns the starting position for new enemies
    def get_start(self):
        if len(self.lr.paths) > 0:
            return self.lr.paths[0].get_start()
        else:
            return [0, 0]

    def tick(self, dt):
        # Move all enemies, and update towers/projectiles
        for i in self.enemies:
            if not self.lr.move(i, dt):
                self.enemies.remove(i)
        for i in self.towers:
            self.projectiles += i.tick(dt)
        for i in self.projectiles:
            if not i.tick(dt):
                self.projectiles.remove(i)
            for j in self.enemies:
                if i.polygon.collides_polygon(j.polygon):
                    self.projectiles.remove(i)
                    self.enemies.remove(j)
                    break
        # Get all enemy spawns
        self.enemies += self.lr.get_enemy_spawns(self.time, self.time + dt)
        self.time += dt
        # Redraw the screen
        self.draw()

    def handle_event(self, e):
        if e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
            pos = data.get_mouse_pos()
            pos = [p / data.screen_w for p in pos]
            num = randint(1, 10)
            if num > 6:
                self.towers.append(Tower1(pos=pos))
            elif num > 3:
                self.towers.append(Tower2(pos=pos))
            elif num > 1:
                self.towers.append(Ballista(pos=pos))
            else:
                self.towers.append(AAGun(pos=pos))

    def reset(self):
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        self.time = 0

    # Draw the screen
    def draw(self):
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        d.blit(self.lr.surface, (data.off_x, data.off_y))
        # TODO: The img rect will probably just be replaced by a rectangle in the object itself
        for i in self.enemies + self.towers + self.projectiles:
            img_rect = i.blit_img.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                   int(i.pos[1] * data.screen_w) + data.off_y))
            d.blit(i.blit_img, img_rect)
