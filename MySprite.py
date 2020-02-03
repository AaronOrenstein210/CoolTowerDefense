from os.path import isfile
import pygame as pg
import data


class Sprite:
    def __init__(self, pos, dim=(.1, .1), img=""):
        self.pos = pos
        self.dim = dim

        img_dim = (int(dim[0] * data.screen_w), int(dim[1] * data.screen_w))
        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.image = pg.transform.scale(pg.image.load(img), (img_dim))
        else:
            self.image = pg.Surface(img_dim)
