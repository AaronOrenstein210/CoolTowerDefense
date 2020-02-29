from os.path import isfile
import pygame as pg
import math
import data
from Game.collision import Polygon


class Sprite:
    def __init__(self, pos=(0, 0), dim=(.1, .1), angle=0, img=""):
        self.pos = pos
        self.dim = dim
        self.polygon = None
        self.angle = angle

        img_dim = (int(dim[0] * data.screen_w), int(dim[1] * data.screen_w))
        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.img = data.scale_to_fit(pg.image.load(img), w=img_dim[0], h=img_dim[1])
        else:
            self.img = pg.Surface(img_dim)
        # Just blit this surface, not self.img
        self.blit_img = self.img

        self.set_pos(pos)

    def set_pos(self, pos):
        self.pos = pos
        half_w, half_h = self.dim[0] / 2, self.dim[1] / 2
        points = []
        for signs in [[-1, 1], [1, 1], [1, -1], [-1, -1]]:
            points.append(rotate_point([pos[0] + signs[0] * half_w, pos[1] + signs[1] * half_h], pos, self.angle))
        self.polygon = Polygon(points)

    def set_angle(self, angle):
        self.angle = angle
        half_w, half_h = self.dim[0] / 2, self.dim[1] / 2
        points = []
        for signs in [[-1, 1], [1, 1], [1, -1], [-1, -1]]:
            points.append(rotate_point([self.pos[0] + signs[0] * half_w,
                                        self.pos[1] + signs[1] * half_h], self.pos, angle))
        self.polygon = Polygon(points)
        self.blit_img = pg.transform.rotate(self.img, self.angle + 90)


class Tower(Sprite):
    upgrades = []

    def __init__(self, idx, cooldown=1000, cost=10, shoot_range=.1, **kwargs):
        super().__init__(**kwargs)
        self.idx = idx
        self.cooldown = cooldown
        self.cost = cost
        self.timer = 0
        self.range = shoot_range
        # Index of current upgrade
        self.upgrade_lvl = -1
        # Surface of all upgrades and rectangle
        self.upgrade_s = None
        self.upgrade_r = pg.Rect(0, 0, 0, 0)
        self.scroll = 0

    @property
    def upgrade_w(self):
        return data.screen_w // 5

    def draw_upgrades(self):
        w = self.upgrade_w
        self.upgrade_s = pg.Surface((w, w * len(self.upgrades)))
        for i, upgrade in enumerate(self.upgrades):
            upgrade.draw_img(self.upgrade_s, pg.Rect(0, i * w, w, w), i <= self.upgrade_lvl)
        self.upgrade_r = pg.Rect(data.off_x, data.off_y, w, data.screen_w)
        if self.pos[0] < .5:
            self.upgrade_r.move_ip(data.screen_w - w, 0)

    def clear_upgrades(self):
        del self.upgrade_s
        for upgrade in self.upgrades:
            upgrade.clear_surface()

    def scroll_upgrades(self, up):
        amnt = self.upgrade_r.h // 20
        if up:
            self.scroll -= amnt
            if self.scroll < 0:
                self.scroll = 0
        else:
            self.scroll += amnt
            max_scroll = max(0, self.upgrade_s.get_size()[1] - self.upgrade_r.h)
            if self.scroll > max_scroll:
                self.scroll = max_scroll

    def click_upgrades(self, money):
        pos = pg.mouse.get_pos()
        if self.upgrade_r.collidepoint(*pos):
            idx = (pos[1] - self.upgrade_r.y + self.scroll) // self.upgrade_w
            if idx < len(self.upgrades) and idx == self.upgrade_lvl + 1 and \
                    self.upgrades[idx].cost <= money:
                self.upgrades[idx].draw_img(self.upgrade_s,
                                            pg.Rect(0, idx * self.upgrade_w, self.upgrade_w, self.upgrade_w), True)
                self.upgrade()
                return self.upgrades[idx].cost
        return 0

    def check_hovering(self):
        pos = pg.mouse.get_pos()
        if self.upgrade_r.collidepoint(*pos):
            idx = (pos[1] - self.upgrade_r.y + self.scroll) // self.upgrade_w
            if idx < len(self.upgrades):
                topleft = [self.upgrade_r.x, self.upgrade_r.y + idx * self.upgrade_w + self.scroll]
                topleft[0] += self.upgrade_w if self.pos[0] >= .5 else -2 * self.upgrade_w
                pg.display.get_surface().blit(self.upgrades[idx].description_s, topleft)

    def upgrade(self):
        pass

    def shoot(self, enemy):  # given an enemy, shoots at them
        return []

    def modify_projectile(self, projectile):
        pass

    def draw_range(self):
        r = int(self.range * data.screen_w)
        s = pg.Surface((r * 2, r * 2))
        pg.draw.circle(s, (0, 0, 255), (r, r), r)
        s.set_alpha(64)
        s.set_colorkey((0, 0, 0))
        pg.display.get_surface().blit(s, (int(self.pos[0] * data.screen_w - r + data.off_x),
                                          int(self.pos[1] * data.screen_w - r + data.off_y)))

    def within_range(self, x, y):
        xval = self.pos[0] - x
        yval = self.pos[1] - y
        dist = (xval ** 2 + yval ** 2) ** 0.5
        return dist <= self.range

    def tick(self, dt):
        self.timer += dt
        while self.timer >= self.cooldown:
            self.timer -= self.cooldown
            # Get all enemies in range
            in_range = [e for e in data.lvlDriver.enemies if data.get_distance(self.pos, e.pos) < self.range]
            # Shoot the enemies based on shooting ai
            if len(in_range) > 0:
                for projectile in self.shoot(closest_enemy(in_range, self)):
                    self.modify_projectile(projectile)
                    data.lvlDriver.projectiles.append(projectile)


class Upgrade:
    def __init__(self, description="No Description", cost=0, img=""):
        # Save cost
        self.cost = cost
        # Break up description by "\n"'s
        self.description = description.split("\n")

        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.img = pg.image.load(img)
        else:
            self.img = pg.Surface((10, 10))
        self.description_s = None

    def draw_img(self, s, rect, bought):
        # Draw background
        back = data.scale_to_fit(pg.image.load("res/upgrade_back.png"), w=rect.w, h=rect.h)
        s.blit(back, back.get_rect(center=rect.center))
        # Draw cost text
        text_h = rect.h // 5
        font = data.get_scaled_font(rect.w, text_h, "Bought")
        string = "Bought" if bought else "${}".format(self.cost)
        text = font.render(string, 1, (255, 255, 255))
        s.blit(text, text.get_rect(center=(rect.centerx, rect.bottom - text_h // 2)))
        # Scale and draw the image
        img = data.scale_to_fit(self.img, w=rect.w, h=rect.h - text_h)
        s.blit(img, img.get_rect(center=(rect.centerx, rect.centery - text_h // 2)))
        if not bought:
            img = data.scale_to_fit(pg.image.load("res/lock.png"), w=rect.w, h=rect.h - text_h)
            s.blit(img, img.get_rect(center=(rect.centerx, rect.centery - text_h // 2)))
        # Draw description
        self.description_s = pg.Surface((rect.w * 2, rect.h))
        dim = self.description_s.get_size()
        text_h = dim[1] // 6
        font = data.get_scaled_font(dim[0], text_h, "")
        i = 0
        for line in self.description:
            for string in data.wrap_text(line, font, dim[0]):
                text = font.render(string, 1, (255, 255, 255))
                text_rect = text.get_rect(center=(dim[0] // 2, int(text_h * (i + .5))))
                self.description_s.blit(text, text_rect)
                i += 1

    def clear_surface(self):
        del self.description_s


def first_enemy(arr):
    return max(arr, key=lambda e: e.path + e.progress)


def closest_enemy(arr, tower):
    return min(arr, key=lambda e: data.get_distance(tower.pos, e.pos))


def strongest_enemy(arr):
    return max(arr, key=lambda e: e.strength)


class Projectile(Sprite):
    def __init__(self, damage=1, speed=.5, **kwargs):
        super().__init__(**kwargs)
        self.damage = damage
        self.speed = speed

    def tick(self, dt):
        d = (self.speed * dt) / 1000
        dx = d * math.cos(self.angle)
        # Flip y for pixel coords
        dy = -d * math.sin(self.angle)
        self.set_pos((self.pos[0] + dx, self.pos[1] + dy))
        return 0 <= self.pos[0] <= 1 and 0 <= self.pos[1] <= 1


class Enemy(Sprite):
    def __init__(self, idx, strength=1, velocity=.1, **kwargs):
        super().__init__(**kwargs)
        if data.lvlDriver is not None:
            self.set_pos(data.lvlDriver.get_start())
        self.idx = idx
        self.strength = strength
        self.path = 0
        self.progress = 0
        self.v = velocity

    #  This method reduces the strength by the damage amount
    def hit(self, damage):
        self.strength = self.strength - damage
        if self.strength < 0:
            self.strength = 0
        return self.strength

    def set_progress(self, path, progress):
        self.path = path
        self.progress = progress


def rotate_point(p, center, dtheta):
    dx, dy = p[0] - center[0], p[1] - center[1]
    radius = math.sqrt(dx * dx + dy * dy)
    angle = math.asin(dy / radius)
    if dx < 0:
        angle = math.pi - angle
    angle += dtheta
    return center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)
