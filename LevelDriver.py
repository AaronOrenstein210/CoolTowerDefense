# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import *
import pygame as pg
from random import uniform
import data


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    def __init__(self):
        self.data = data
        self.enemies = []
        self.towers = []
        self.projectiles = []

        self.time = 0
        self.paths = []
        self.spawn_list = []

        self.background = None

    # Called every iteration of the while loop
    def tick(self, dt):
        # Move all enemies, and update towers/projectiles
        for i in self.enemies:
            if not self.move(i, dt):
                print("Lost a Life")
                self.enemies.remove(i)
        for i in self.towers:
            i.tick(dt)
        for i in self.projectiles:
            if not i.tick(dt):
                self.projectiles.remove(i)
            else:
                for j in self.enemies:
                    if i.polygon.collides_polygon(j.polygon):
                        self.projectiles.remove(i)
                        self.enemies.remove(j)
                        break
        # Get all enemy spawns
        self.spawn_enemies(dt)
        self.time += dt
        # Redraw the screen
        self.draw()

    # TODO: t_i
    # Spawns enemies based on the passage of time
    def spawn_enemies(self, dt):
        t_i = self.time
        t_f = self.time + dt
        for spawn in self.spawn_list:
            if spawn.duration < self.time:
                t_i -= spawn.duration
                t_f -= spawn.duration
            elif spawn.duration >= t_f:
                for i in range(abs(spawn.get_count(t_f) - spawn.get_count(self.time))):
                    num = uniform(0, sum(v for v in spawn.chances.values()))
                    for key in spawn.chances.keys():
                        val = spawn.chances[key]
                        if val < num:
                            num -= val
                        else:
                            self.enemies.append(data.enemies[key]())
                            break
                break
            else:
                for i in range(abs(spawn.get_count(spawn.duration) - spawn.get_count(self.time))):
                    num = uniform(0, sum(v for v in spawn.chances.values()))
                    for key in spawn.chances.keys():
                        val = spawn.chances[key]
                        if val < num:
                            num -= val
                        else:
                            self.enemies.append(data.enemies[key]())
                            break
                t_i = 0
                t_f -= spawn.duration

    # Updates an enemy's position along the path
    def move(self, enemy, dt):
        d = enemy.v * dt / 1000
        while d > 0:
            to_end = self.paths[enemy.path].length * (1 - enemy.progress)
            if d >= to_end:
                enemy.path += 1
                enemy.progress = 0
                if enemy.path >= len(self.paths):
                    return False
            else:
                enemy.progress += d / self.paths[enemy.path].length
            d -= to_end
        enemy.set_pos(self.paths[enemy.path].get_pos(enemy.progress))
        return True

    # Draw the screen
    def draw(self):
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        d.blit(self.background, (data.off_x, data.off_y))
        for i in self.enemies + self.towers + self.projectiles:
            img_rect = i.blit_img.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                   int(i.pos[1] * data.screen_w) + data.off_y))
            d.blit(i.blit_img, img_rect)

    # Draws the enemy path
    def draw_background(self):
        self.background = pg.Surface((data.screen_w, data.screen_w))
        self.background.fill((0, 175, 0))
        self.background.blit(draw_paths(data.screen_w, self.paths), (0, 0))

    def resize(self):
        self.draw_background()
        # Get a list of objects to resize
        objects = self.enemies + self.towers + self.projectiles
        # Redraw objects
        for obj in objects:
            img_dim = (int(obj.dim[0] * data.screen_w), int(obj.dim[1] * data.screen_w))
            obj.img = pg.transform.scale(obj.img, img_dim)
            obj.blit_img = pg.transform.rotate(obj.img, obj.angle)

    def reset(self):
        from Tower import TOWER_1
        self.enemies.clear()
        self.towers.clear()
        self.towers.append(data.towers[TOWER_1](pos=rand_pos()))
        self.projectiles.clear()
        self.time = 0

    # Sets level data
    def set_level(self, paths, spawn_list):
        self.reset()
        self.paths = paths
        self.spawn_list = spawn_list
        self.draw_background()
