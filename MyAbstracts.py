from os.path import isfile
import pygame as pg
import math
import data
from collision import Polygon


class Sprite:
    def __init__(self, pos, dim=(.1, .1), img="", angle=0):
        self.pos = [0, 0]
        self.polygon = None
        self.dim = dim
        self.angle = angle

        img = "res/" + img
        img_dim = (int(dim[0] * data.screen_w), int(dim[1] * data.screen_w))
        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.img = pg.transform.scale(pg.image.load(img), img_dim)
        else:
            self.img = pg.Surface(img_dim)
        # This is the surface that is blitted, img is just a copy of the surface for rotating purposes
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


class Projectile(Sprite):
    def __init__(self, pos, angle, v=.1, dim=(.1, .1), img=""):
        super().__init__(pos, dim, img)

        self.v = v

        self.set_angle(angle)

    def tick(self, dt):
        d = self.v * dt / 1000
        dx, dy = d * math.cos(self.angle), d * math.sin(self.angle)
        self.set_pos([self.pos[0] + dx, self.pos[1] - dy])
        return 0 <= self.pos[0] <= 1 and 0 <= self.pos[1] <= 1


class Enemy(Sprite):
    def __init__(self, idx, strength=1, v=.25, dim=(.1, .1), img=""):
        if data.lvlDriver is not None:
            super().__init__(data.lvlDriver.get_start(), dim, img)
        else:
            super().__init__([0, 0], dim, img)

        self.idx = idx

        self.strength = strength
        self.path = self.progress = 0
        self.v = v

        data.enemies[idx] = self


class Tower(Sprite):
    def __init__(self, idx, pos, dim=(.1, .1), cooldown=1000, img=""):
        super().__init__(pos, dim, img)

        self.cooldown = cooldown
        self.timer = 0

        data.towers[idx] = self

    def tick(self, dt):
        projectiles = []
        self.timer += dt
        while self.timer > self.cooldown:
            self.timer -= self.cooldown
            if len(data.lvlDriver.enemies) > 0:
                projectiles += self.on_shoot(data.lvlDriver.enemies[0].pos)
        return projectiles

    def on_shoot(self, enemy_pos):
        pass


def rotate_point(p, center, dtheta):
    dx, dy = p[0] - center[0], p[1] - center[1]
    radius = math.sqrt(dx * dx + dy * dy)
    angle = math.asin(dy / radius)
    if dx < 0:
        angle = math.pi - angle
    angle += dtheta
    return center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)
