# Created on 27 January 2020
# Created by Kyle Doster
from LevelReader import *
import pygame as pg
from pygame.locals import *
from Tower import *
from random import uniform
import data

TOWER_ORDER = [TOWER_1, TOWER_2, BALLISTA, AAGUN]


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    TOWER_COLUMNS = 2

    def __init__(self):
        self.data = data
        self.enemies = []
        self.towers = []
        self.projectiles = []

        self.hp = self.money = 0

        # Menu and menu tower scroll surfaces
        self.menu = self.menu_towers = None
        # Menu rectangles
        self.menu_rects = {"menu": pg.Rect(0, 0, 0, 0),
                           "hp": pg.Rect(0, 0, 0, 0),
                           "money": pg.Rect(0, 0, 0, 0),
                           "towers": pg.Rect(0, 0, 0, 0)}
        # Menu x offset (0 to 1 * screen width)
        self.menu_x = 0
        # Scroll amount of menu tower list, <= 0
        self.towers_scroll = 0
        # Width of a tower sprite in the menu
        self.menu_tower_w = 0
        # Menu text font
        self.menu_font = None
        # Boolean telling if we are moving the menu
        self.moving_menu = False

        self.time = 0
        self.paths = []
        self.spawn_list = []

        # Background surface
        self.background = None

    # Called every iteration of the while loop
    def tick(self, dt):
        # Move all enemies, and update towers/projectiles
        for i in self.enemies:
            if not self.move_enemy(i, dt):
                self.damage(1)
                self.enemies.remove(i)
        for i in self.towers:
            i.tick(dt)
        for i in self.projectiles:
            if not i.tick(dt):
                self.projectiles.remove(i)
            else:
                for j in self.enemies:
                    if i.polygon.collides_polygon(j.polygon):
                        self.add_money(1)
                        self.projectiles.remove(i)
                        self.enemies.remove(j)
                        break
        # Get all enemy spawns
        self.spawn_enemies(dt)
        self.time += dt
        # Get change in mouse position every time so that it can update the last mouse position
        mouse_delta = pg.mouse.get_rel()
        # Check if we have moved the menu
        if self.moving_menu:
            self.menu_x += mouse_delta[0] / data.screen_w
            if self.menu_x < 0:
                self.menu_x = 0
            elif self.menu_x > 1 - self.menu_rects["menu"].w / data.screen_w:
                self.menu_x = 1 - self.menu_rects["menu"].w / data.screen_w
            self.menu_rects["menu"].x = self.menu_x * data.screen_w + data.off_x
        # Redraw the screen
        self.draw()

    # Returns the starting position of the enemy path
    def get_start(self):
        if len(self.paths) > 0:
            return self.paths[0].get_start()
        else:
            return [0, 0]

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
    def move_enemy(self, enemy, dt):
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
            # TODO: Optimize this
            img_rect = i.blit_img.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                   int(i.pos[1] * data.screen_w) + data.off_y))
            d.blit(i.blit_img, img_rect)
        d.blit(self.menu, self.menu_rects["menu"])

    # Draws menu surface
    def draw_menu(self):
        # Establish rectangles
        self.menu_rects["menu"] = pg.Rect(self.menu_x * data.screen_w + data.off_x, data.off_y,
                                          data.screen_w // 5, data.screen_w)
        r = self.menu_rects["menu"]
        img_w = r.h // 20
        self.menu_rects["hp"] = pg.Rect(img_w, 0, r.w - img_w, img_w)
        self.menu_rects["money"] = self.menu_rects["hp"].move(0, self.menu_rects["hp"].h)
        self.menu_rects["towers"] = pg.Rect(0, self.menu_rects["money"].bottom, r.w,
                                            r.h - self.menu_rects["money"].bottom)
        self.menu_tower_w = r.w // self.TOWER_COLUMNS

        # Create surface
        self.menu = pg.Surface(r.size)

        # Draw money and hp text
        self.menu_font = data.get_scaled_font(*self.menu_rects["hp"].size, "999")
        self.add_money(0)
        self.damage(0)

        # Draw money and hp icons
        rect = self.menu_rects["money"]
        img = data.scale_to_fit(pg.image.load("res/money.png"), w=img_w, h=img_w)
        img_rect = img.get_rect(center=(rect.x - img_w // 2, rect.centery))
        self.menu.blit(img, img_rect)
        rect = self.menu_rects["hp"]
        img = data.scale_to_fit(pg.image.load("res/heart.png"), w=img_w, h=img_w)
        img_rect = img.get_rect(center=(rect.x - img_w // 2, rect.centery))
        self.menu.blit(img, img_rect)

        # display towers
        self.menu_towers = pg.Surface((r.w, self.menu_tower_w * (math.ceil(len(TOWER_ORDER) / 2) + 1)))
        for idx in TOWER_ORDER:
            col, row = idx % self.TOWER_COLUMNS, idx // self.TOWER_COLUMNS
            img = data.scale_to_fit(data.tower_images[idx], w=self.menu_tower_w, h=self.menu_tower_w)
            img_rect = img.get_rect(center=(int((col + .5) * self.menu_tower_w), int((row + .5) * self.menu_tower_w)))
            self.menu_towers.blit(img, img_rect)
        self.towers_scroll = 0
        self.menu.blit(self.menu_towers, self.menu_rects["towers"],
                       area=((0, self.towers_scroll), self.menu_rects["towers"].size))

    # Draws the enemy path
    def draw_background(self):
        self.background = pg.Surface((data.screen_w, data.screen_w))
        self.background.fill((0, 175, 0))
        self.background.blit(draw_paths(data.screen_w, self.paths), (0, 0))

    # Resizes display
    def resize(self):
        self.draw_background()
        # Get a list of objects to resize
        objects = self.enemies + self.towers + self.projectiles
        # Redraw objects
        for obj in objects:
            img_dim = (int(obj.dim[0] * data.screen_w), int(obj.dim[1] * data.screen_w))
            obj.img = pg.transform.scale(obj.img, img_dim)
            obj.blit_img = pg.transform.rotate(obj.img, obj.angle)

        self.draw_menu()

    # Checks input events
    def input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                pos = pg.mouse.get_pos()
                m_rect = self.menu_rects["menu"]
                if m_rect.collidepoint(*pos):
                    pos = [pos[0] - m_rect.x, pos[1] - m_rect.y]
                    t_rect = self.menu_rects["towers"]
                    if t_rect.collidepoint(*pos):
                        pos = [pos[0] - t_rect.x, pos[1] - t_rect.y + self.towers_scroll]
                        col, row = pos[0] // self.menu_tower_w, pos[1] // self.menu_tower_w
                        idx = row * self.TOWER_COLUMNS + col
                        if idx < len(TOWER_ORDER):
                            self.towers.append(data.towers[idx](pos=rand_pos()))
                        else:
                            self.moving_menu = True
                    else:
                        self.moving_menu = True
            elif event.button == BUTTON_WHEELUP or event.button == BUTTON_WHEELDOWN:
                rect = self.menu_rects["towers"]
                if event.button == BUTTON_WHEELUP:
                    self.towers_scroll -= 2
                    if self.towers_scroll < 0:
                        self.towers_scroll = 0
                else:
                    self.towers_scroll += 2
                    max_scroll = max(0, self.menu_towers.get_size()[1] - rect.h)
                    if self.towers_scroll > max_scroll:
                        self.towers_scroll = max_scroll
                self.menu.fill((0, 0, 0), rect)
                self.menu.blit(self.menu_towers, rect, area=((0, self.towers_scroll), rect.size))
        if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT:
            self.moving_menu = False

    # Adds input to money
    def add_money(self, amnt):
        self.money += amnt
        rect = self.menu_rects["money"]
        self.menu.fill((0, 0, 0), rect)
        text = self.menu_font.render(str(self.money), 1, (255, 255, 255))
        text_rect = text.get_rect(centery=rect.centery, left=rect.left)
        self.menu.blit(text, text_rect)

    # Subtracts input from hp
    def damage(self, amnt):
        self.hp -= amnt
        rect = self.menu_rects["hp"]
        self.menu.fill((0, 0, 0), rect)
        text = self.menu_font.render(str(self.hp), 1, (255, 255, 255))
        text_rect = text.get_rect(centery=rect.centery, left=rect.left)
        self.menu.blit(text, text_rect)

    def reset(self):
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        self.time = 0
        self.hp = self.money = 100
        self.resize()

    # Sets level data
    def set_level(self, paths, spawn_list):
        self.reset()
        self.paths = paths
        self.spawn_list = spawn_list
        self.draw_background()
