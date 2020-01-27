# Created on 27 January 2020
# Created by Isabelle Early

from Projectile import Projectile

WINDOW = 500  #this is temporary
# Defines a tower
class Tower:
    def __init__(self, t, x, y):  # t is a variable determining the type of tower
        self.type = t
        self.pos = (x, y)
        self.projectile = Projectile(self.type)
        if self.type == 1 :
            self.IMG = pygame.transform.scale(pygame.image.load('tower1.png'), (WINDOW*0.05, WINDOW*0.05 ))
            self.range = 0.1*WINDOW  # radius

    def withinRange(self, x, y):  # given a position, returns whether that position is within range
        xVal = self.pos[0] - x
        yVal = self.pos[1] - y
        dist = (xVal**2 + yVal**2)**0.5
        if dist <= self.range :
            return True
        return False

    def tick(self, dt):
        pass
