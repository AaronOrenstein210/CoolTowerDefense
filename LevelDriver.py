# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import LevelReader as Read
from LevelReader import *
import pygame as pg
from pygame.locals import *
from Enemy import Enemy1
from Tower import DuckTower
from random import uniform
import data


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    def __init__(self):
        self.data = data
        self.lr = Read()
        rand = rand_pos()
        temp = rand_pos()
        # self.start = self.lr.paths[0].get_start()
        self.start = temp
        self.enemies = [Enemy1(self.start)]
        self.towers = [DuckTower(pos=(rand[0] * data.screen_w, rand[1] * data.screen_w))]
        self.projectiles = []


        # Nicole Rectangle Start
        self.menuRectLeft = data.screen_w * 0.7
        self.menuRectTop = data.screen_w * 0.1
        self.boxTop = data.screen_w * 0.65  # top of box with all of the towers
        self.menuRectWidth = data.screen_w * 0.25
        self.menuRectHeight = data.screen_w * 0.8
        self.menuRect = (self.menuRectLeft, self.menuRectTop, self.menuRectWidth, self.menuRectHeight)


    # Called every iteration of the while loop
    def tick(self, dt):
        # Move all enemies, and update towers/projectiles
        for i in self.enemies:
            if not self.lr.move(i, dt):
                self.enemies.remove(i)
        for i in self.towers:
            i.tick(dt)
        for i in self.projectiles:
            i.tick(dt)
        # Redraw the screen
        self.draw()

    # Draw the screen
    def draw(self):
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        d.blit(self.lr.surface, (data.off_x, data.off_y))
        for i in self.enemies + self.towers + self.projectiles:
            img_rect = i.blit_img.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                   int(i.pos[1] * data.screen_w) + data.off_y))

           #  Nicole start
            d.blit(i.blit_img, img_rect)
            self.draw_menu(d, self.menuRect)
        # draws menu
    def draw_menu (self, d, menu_rect):
        blue = (0, 0, 255)
        pg.draw.rect(d, blue, menu_rect, 2)
        font = pg.font.Font('freesansbold.ttf', 15)
        menu_text = font.render("MENU", 1, (255, 255, 255))
        menu_box = menu_text.get_rect()
        d.blit(menu_text, (self.menuRect[0] + (self.menuRect[2] - menu_box[2]) / 2, self.menuRect[1] + menu_box[3] / 2))
        font1 = pg.font.Font('freesansbold.ttf', 15)
        money_text = font.render("Money:", 1, (255, 255, 255))
        menu_box = money_text.get_rect()
        d.blit(money_text, (self.menuRect[0] + self.menuRect[2]/10, self.menuRect[1] + menu_box[3] * 2))





    def setStart(self, pos):
        self.start = pos

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
            pass  # set a tower
        elif half_x <= x <= self.menuRectLeft + self.menuRectWidth and self.boxTop <= y <= half_y:  # top right
            pass
        elif self.menuRectLeft <= x <= half_x and half_y <= y <= self.menuRectTop + self.menuRectHeight:  # bottom left
            pass
        elif half_x <= x <= self.menuRectLeft + self.menuRectWidth \
                and half_y <= y <= self.menuRectTop + self.menuRectHeight:  # bottom right
            pass

    def reset(self):
        pass
