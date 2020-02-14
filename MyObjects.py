from MyAbstracts import Enemy, Tower, Projectile
import data

# Enemies
ENEMY_1, ENEMY_2, ENEMY_3, ENEMY_4, ENEMY_5 = range(5)


class Enemy1(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_1, pos, v=.25, img="enemy1.png")


class Enemy2(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_2, pos, v=.3, img="enemy2.png")


class Enemy3(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_3, pos, v=.4, img="enemy3.png")


class Enemy4(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_4, pos, v=.55, img="enemy4.png")


class Enemy5(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(ENEMY_5, pos, v=.75, img="enemy5.png")


# Towers
TOWER_1, TOWER_2, BALLISTA, AAGUN = range(4)


class Tower1(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_1, pos, img="duckTower1.png")

    def on_shoot(self, enemy_pos):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy_pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.5, dim=(.03, .03), img="back.png")


class Tower2(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(TOWER_2, pos, dim=(.07, .07), cooldown=750, img="duckTower2.png")

    def on_shoot(self, enemy_pos):
        pos1 = [self.pos[0] + .05, self.pos[1] + .05]
        pos2 = [self.pos[0] - .05, self.pos[1] - .05]
        return [self.P1(p, data.get_angle_pixels(p, enemy_pos)) for p in [pos1, pos2]]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.5, dim=(.03, .03), img="back.png")


class Ballista(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(BALLISTA, pos, dim=(.125, .125), cooldown=2500, img="duckTowerBallista.png")

    def on_shoot(self, enemy_pos):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy_pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.25, dim=(.08, .08), img="back.png")


class AAGun(Tower):
    def __init__(self, pos=(0, 0)):
        super().__init__(AAGUN, pos, dim=(.05, .1), cooldown=400, img="duckAAGun.png")

    def on_shoot(self, enemy_pos):
        return [self.P1(self.pos, data.get_angle_pixels(self.pos, enemy_pos)),
                self.P2(self.pos, data.get_angle_pixels(self.pos, enemy_pos))]

    class P1(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.75, dim=(.02, .02), img="back.png")

    class P2(Projectile):
        def __init__(self, pos, angle):
            super().__init__(pos, angle, v=.4, dim=(.06, .06), img="back.png")
