from os.path import isfile
import pygame
import math
import data
from collision import Polygon

WINDOW = data.screen_w


class Sprite:
    def __init__(self, pos=(0, 0), dim=(.1, .1), img=""):
        self.pos = pos
        self.dim = dim
        self.polygon = None
        self.angle = 0

        img_dim = (int(dim[0] * data.screen_w), int(dim[1] * data.screen_w))
        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.img = data.scale_to_fit(pygame.image.load(img), *img_dim)
        else:
            self.img = pygame.Surface(img_dim)
        # Just blit this surface, not self.img
        self.blit_img = self.img

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
        self.blit_img = pygame.transform.rotate(self.img, self.angle + 90)


class Tower(Sprite):
    def __init__(self, idx, **kwargs):
        super().__init__(**kwargs)
        self.idx = idx

    def shoot(self, enemy):  # given an enemy, shoots at them
        pass

    def withinRange(self, x, y, r):
        xval = self.pos[0] - x
        yval = self.pos[1] - y
        dist = (xval ** 2 + yval ** 2) ** 0.5
        return dist <= r

    def restartCount(self):
        pass

    def tick(self, dt):
        pass


class Projectile(Sprite):
    def __init__(self, pos, angle, damage=1, speed=.5, dim=(.05, .05), img=""):
        super().__init__(pos=pos, dim=dim, img=img)
        self.set_angle(angle)
        self.damage = damage
        self.speed = speed

    def getDamage(self):
        return self.damage

    def tick(self, dt):
        d = (self.speed * dt) / 1000
        dx = d * math.cos(self.angle)
        dy = d * math.sin(self.angle)
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)
        return 0 <= self.pos[0] <= 1 and 0 <= self.pos[1] <= 1


class Enemy(Sprite):
    def __init__(self, idx, strength=1, velocity=.1, **kwargs):
        super().__init__(**kwargs)
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


def rotate_point(p, center, dtheta):
    dx, dy = p[0] - center[0], p[1] - center[1]
    radius = math.sqrt(dx * dx + dy * dy)
    angle = math.asin(dy / radius)
    if dx < 0:
        angle = math.pi - angle
    angle += dtheta
    return center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)
