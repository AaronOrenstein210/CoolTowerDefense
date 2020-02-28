from os.path import isfile
import pygame
import math
import data
from Game.collision import Polygon

WINDOW = data.screen_w


class Sprite:
    def __init__(self, pos=(0, 0), dim=(.1, .1), angle=0, img=""):
        self.pos = pos
        self.dim = dim
        self.polygon = None
        self.angle = angle

        img_dim = (int(dim[0] * data.screen_w), int(dim[1] * data.screen_w))
        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.img = data.scale_to_fit(pygame.image.load(img), w=img_dim[0], h=img_dim[1])
        else:
            self.img = pygame.Surface(img_dim)
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
        self.blit_img = pygame.transform.rotate(self.img, self.angle + 90)


class Tower(Sprite):
    def __init__(self, idx, cooldown=1000, cost=10, **kwargs):
        super().__init__(**kwargs)
        self.idx = idx
        self.cooldown = cooldown
        self.cost = cost
        self.timer = 0

    def shoot(self, enemy):  # given an enemy, shoots at them
        return []

    def within_range(self, x, y, r):
        xval = self.pos[0] - x
        yval = self.pos[1] - y
        dist = (xval ** 2 + yval ** 2) ** 0.5
        return dist <= r

    def tick(self, dt):
        self.timer += dt
        while self.timer >= self.cooldown:
            self.timer -= self.cooldown
            if len(data.lvlDriver.enemies) > 0:
                for projectile in self.shoot(data.lvlDriver.enemies[0]):
                    data.lvlDriver.projectiles.append(projectile)


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
