import data
from MyProjectile import Projectile
from MySprite import Sprite

towers = {}


class Tower(Sprite):
    def __init__(self, idx, pos, dim=(.1, .1), cooldown=1000, img=""):
        super().__init__(pos, dim, img)

        self.idx = idx

        self.cooldown = cooldown
        self.timer = 0

    def set_pos(self, x, y):
        self.pos = [x, y]

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


class Tower1(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(0, pos, img="duckTower1.png")

    def on_shoot(self, enemy_pos):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy_pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.5, dim=(.03, .03), img="back.png")


class Tower2(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(0, pos, dim=(.07, .07), cooldown=750, img="duckTower2.png")

    def on_shoot(self, enemy_pos):
        pos1 = [self.pos[0] + .05, self.pos[1] + .05]
        pos2 = [self.pos[0] - .05, self.pos[1] - .05]
        return [self.P1(p, data.get_angle_pixels(p, enemy_pos)) for p in [pos1, pos2]]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.5, dim=(.03, .03), img="back.png")


class Ballista(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(0, pos, dim=(.125, .125), cooldown=2500, img="duckTowerBallista.png")

    def on_shoot(self, enemy_pos):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy_pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.25, dim=(.08, .08), img="back.png")


class AAGun(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(0, pos, dim=(.05, .1), cooldown=400, img="duckAAGun.png")

    def on_shoot(self, enemy_pos):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy_pos)),
                self.P2(self.pos, data.get_angle_pixels(self.pos, enemy_pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.75, dim=(.02, .02), img="back.png")

    class P2(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.4, dim=(.06, .06), img="back.png")
