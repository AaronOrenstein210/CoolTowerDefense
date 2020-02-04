from MySprite import Sprite


class Enemy(Sprite):
    def __init__(self, idx, pos, v=.25, dim=(.1, .1), img=""):
        super().__init__(pos, dim, img)

        self.idx = idx

        self.path = self.progress = 0
        self.v = v


class Enemy1(Enemy):
    def __init__(self, pos=(0, 0)):
        super().__init__(0, pos, img="duckBase.png")
