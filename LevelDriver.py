# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import *
import pygame as pg
from pygame.locals import *
from Abstract import Tower
from Enemy import Enemy1
from Tower import *
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
        self.menuRects = {"menu": pg.Rect(0, 0, 0, 0),
                          "health": pg.Rect(0, 0, 0, 0),
                          "money": pg.Rect(0, 0, 0, 0),
                          "towers": pg.Rect(0, 0, 0, 0)
                          }
        # Nicole Rectangle Start
        self.menuRectLeft = data.screen_w * 0.7
        self.menuRectTop = data.screen_w * 0.1
        self.boxTop = data.screen_w * 0.65  # top of box with all of the towers
        self.menuRectWidth = data.screen_w * 0.25
        self.menuRectHeight = data.screen_w * 0.8
        self.menuRect = (self.menuRectLeft, self.menuRectTop, self.menuRectWidth, self.menuRectHeight)

        self.time = 0
        self.paths = []
        self.spawn_list = []

        # Background surface
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

       # self.draw_menu(d, self.menuRect)

    # draws menu
    def draw_menu (self, d, menu_rect):
        blue = (0, 0, 255)
        pg.draw.rect(d, blue, menu_rect)
        font = pg.font.Font('freesansbold.ttf', 15)
        menu_text = font.render("MENU", 1, (255, 255, 255))
        menu_box = menu_text.get_rect()
        d.blit(menu_text, (self.menuRect[0] + (self.menuRect[2] - menu_box[2]) / 2, self.menuRect[1] + menu_box[3] / 2))
        money_text = font.render("Money:", 1, (255, 255, 255))
        lives_text = font.render("Lives:", 1, (255, 255, 255))
        buy_text = font.render("Buy Stuff:", 1, (255, 255, 255))
        close_text = font.render("Close", 1, (255, 255, 255))
        menu_box = money_text.get_rect()
        d.blit(money_text, (self.menuRect[0] + self.menuRect[2]/10, self.menuRect[1] + menu_box[3] * 2))
        d.blit(lives_text, (self.menuRect[0] + self.menuRect[2] / 10, self.menuRect[1] + menu_box[3] * 3))
        d.blit(buy_text, (self.menuRect[0] + self.menuRect[2] / 10, self.menuRect[1] + menu_box[3] * 4))
        d.blit(close_text, (self.menuRect[0] + self.menuRect[2] / 10, self.menuRect[1] + menu_box[3] * 5))

        # display towers
        x = self.menuRectLeft + data.screen_w * 0.06
        y = self.boxTop
        inc = self.menuRectWidth/3 + data.screen_w * 0.05
        for i in data.tower_images.values():
            i = pygame.transform.scale(i, (int(data.screen_w * 0.1), int(data.screen_w * 0.1)))
            rect = i.get_rect()
            rect.center = (x, y)
            d.blit(i, rect)
            x += inc
            if x >= self.menuRectLeft + self.menuRectWidth:
                x = self.menuRectLeft + data.screen_w * 0.06
                y += inc

            if y == self.menuRectTop + self.menuRectHeight:
                y = self.boxTop

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

        self.draw_menu(pg.display.get_surface(), self.menuRect)

    def input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if self.menuRectLeft <= pos[0] <= (self.menuRectLeft + self.menuRectWidth) \
                    and self.boxTop <= pos[1] <= (self.boxTop + self.menuRectHeight):
                self.click(pos[0], pos[1])

    def click(self, x, y):  # probably include this in the input method
        half_x = self.menuRectLeft + (self.menuRectWidth/2)
        half_y = self.boxTop + (self.menuRectHeight - self.boxTop)/2
        if self.menuRectLeft <= x <= half_x and self.boxTop <= y <= half_y:  # top left
            print("Duck Tower 1")
            self.set_tower(1)
        elif half_x <= x <= self.menuRectLeft + self.menuRectWidth and self.boxTop <= y <= half_y:  # top right
            print("Duck Tower 2")
            self.set_tower(2)
        elif self.menuRectLeft <= x <= half_x and half_y <= y <= self.menuRectTop + self.menuRectHeight:  # bottom left
            print("Duck Tower AA Gun")
            self.set_tower(3)
        elif half_x <= x <= self.menuRectLeft + self.menuRectWidth \
                and half_y <= y <= self.menuRectTop + self.menuRectHeight:  # bottom right
            print("Duck Tower Ballista")
            self.set_tower(4)

    def set_tower(self, type): # probably change the input
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN :
                pos = pg.mouse.get_pos()
                if type == 1:
                    tower = DuckTower(pos[0], pos[1])
                elif type == 2:
                    tower = DuckTower2(pos[0], pos[1])
                elif type == 3:
                    tower = DuckTowerAA(pos[0], pos[1])
                elif type == 4:
                    tower = DuckTowerBallista(pos[0], pos[1])
                self.towers.append(tower)



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
