import math
from MySprite import Sprite


class Projectile(Sprite):
    def __init__(self, pos, angle, v=.1, dim=(.1, .1), img=""):
        super().__init__(pos, dim, img)

        self.angle = angle
        self.v = v

    def tick(self, dt):
        d = self.v * dt / 1000
        dx, dy = d * math.cos(self.angle), d * math.sin(self.angle)
        self.pos = [self.pos[0] + dx, self.pos[1] - dy]
        return 0 <= self.pos[0] <= 1 and 0 <= self.pos[1] <= 1
