# Created on 27 January 2020
# Created by Poopy

from os.path import isfile
from struct import pack, unpack
from sys import byteorder
import math
import pygame as pg
import data
from Game.Enemy import ENEMY_ORDER


# Loads a spawn list from bytes
def load_spawn_list(file_data):
    spawn_list = []
    num = int.from_bytes(file_data[0:1], byteorder)
    file_data = file_data[1:]
    for i in range(num):
        if len(file_data) == 0:
            print("Missing Bytes")
            break
        try:
            temp = Spawn()
            file_data = temp.from_bytes(file_data)
            spawn_list.append(temp)
        except IndexError:
            print("Missing Bytes")
            break
    return spawn_list, file_data


# Draws a spawn list
# If no width is given, 1 second is represented by h pixels
# Chances determines whether to draw enemy spawn chances or not
def draw_spawn_list(spawn_list, h, w=-1, draw_chances=True):
    max_time = sum(i.duration for i in spawn_list)
    if w == -1:
        w = max(h * max_time // 1000, h + h)
    s = pg.Surface((w, h))
    start_time = 0
    for i in spawn_list:
        w_ = w * i.duration // max_time
        x = w * start_time // max_time
        s.blit(i.draw_img(w_, h, draw_chances), (x, 0))
        start_time += i.duration
    return s


START, LINE, CIRCLE = range(3)


class Level:
    def __init__(self):
        self.img = ""
        self.paths = []

    @property
    def start(self):
        return self.paths[0].get_start() if self.paths else [0, 0]

    @property
    def end(self):
        return self.paths[-1].get_end() if self.paths else [0, 0]

    @property
    def len(self):
        return len(self.paths)

    # Draws this level
    def draw(self, w):
        s = pg.Surface((w, w), pg.SRCALPHA)
        if isfile(self.img) and (self.img.endswith(".png") or self.img.endswith(".jpg")):
            img = data.scale_to_fit(pg.image.load(self.img), w=w, h=w)
            s.blit(img, img.get_rect(center=(w // 2, w // 2)))
        line_w = w // 40
        for p in self.paths:
            p.draw(s, line_w)
        return s

    def add(self, path):
        self.paths.append(path)

    def to_bytes(self):
        result = bytearray()
        result.extend(len(self.img).to_bytes(1, byteorder))
        result.extend(self.img.encode('ascii'))
        result.extend(len(self.paths).to_bytes(1, byteorder))
        for p in self.paths:
            result.extend(p.to_bytes())
        return result

    # Loads from bytes, returns remaining bytes
    def from_bytes(self, file_data):
        # Reset variables
        self.img = ""
        self.paths.clear()
        # Load background image
        if len(file_data) == 0:
            print("No data")
            return ""
        str_len = int.from_bytes(file_data[:1], byteorder)
        if len(file_data) < str_len:
                print("Missing src image string")
                return ""
        self.img = file_data[1:str_len + 1].decode("ascii")
        file_data = file_data[str_len + 1:]
        # Load paths
        if len(file_data) == 0:
            print("No path data")
            return ""
        num = int.from_bytes(file_data[:1], byteorder)
        file_data = file_data[1:]
        for i in range(num):
            if len(file_data) == 0:
                print("Missing data for path {} / {}".format(i + 1, num))
                return ""
            # Get the path type and initialize its object
            idx = int.from_bytes(file_data[:1], byteorder)
            if idx in constructors.keys():
                self.paths.append(constructors[idx]())
            else:
                print("Unknown path type")
                return ""
                # Read path data
            file_data = file_data[1:]
            try:
                file_data = self.paths[-1].from_bytes(file_data)
            except Exception:
                print("Incomplete data for path {} / {}".format(i + 1, num))
                return ""
        return file_data


# Stores path data for a specific segment of the enemy path
class Path:
    def __init__(self):
        self.idx = 0
        self.length = 0

    def draw(self, surface, line_w):
        pass

    def get_pos(self, progress):
        return [0, 0]

    def get_start(self):
        pass

    def get_end(self):
        pass

    def to_bytes(self):
        return self.idx.to_bytes(1, byteorder)

    def from_bytes(self, path_data):
        return ""


class Line(Path):
    def __init__(self, start=(0, 0), end=(0, 0)):
        super().__init__()
        self.idx = LINE
        self.start = start
        self.end = end

    def draw(self, surface, line_w):
        w = surface.get_size()[0]
        pos_i = [int(self.start[0] * w), int(self.start[1] * w)]
        pos_f = [int(self.end[0] * w), int(self.end[1] * w)]
        pg.draw.line(surface, (255, 255, 255), pos_i, pos_f, line_w)
        for pos in [pos_i, pos_f]:
            pg.draw.circle(surface, (255, 255, 255), pos, line_w * 3 // 4)

    def get_pos(self, progress):
        dx, dy = self.end[0] - self.start[0], self.end[1] - self.start[1]
        return [self.start[0] + dx * progress, self.start[1] + dy * progress]

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def to_bytes(self):
        return super().to_bytes() + pack('f' * 4, *self.start, *self.end)

    def from_bytes(self, path_data):
        self.start = unpack('f' * 2, path_data[:8])
        self.end = unpack('f' * 2, path_data[8:16])
        self.length = data.get_distance(self.start, self.end)
        return path_data[16:]


class Circle(Path):
    COLORS = ((140, 255, 117), (169, 221, 123), (198, 186, 130), (226, 152, 136), (255, 117, 142))

    def __init__(self):
        super().__init__()
        self.idx = CIRCLE
        self.center, self.radius = [0, 0], 0
        self.theta_i, self.theta_f = 0, 2 * math.pi

    def draw(self, surface, line_w):
        from data import TWO_PI
        w = surface.get_size()[0]
        c = [int(self.center[0] * w), int(self.center[1] * w)]
        rad = int(self.radius * w)
        # Get theta range
        d_theta = self.theta_f - self.theta_i
        sign = math.copysign(1, d_theta)
        d_theta = abs(d_theta)
        # Break theta range into full circles
        loop = -1
        while d_theta >= TWO_PI and loop < len(self.COLORS) - 1:
            loop += 1
            d_theta -= TWO_PI
        # Draw the highest full circle
        if loop >= 0:
            pg.draw.circle(surface, self.COLORS[loop], c, rad, min(line_w, rad))
        # Draw the other sections
        if d_theta > 0 and loop < len(self.COLORS) - 1:
            top_left = [c[0] - rad, c[1] - rad]
            thetas = [self.theta_i, self.theta_i + d_theta * sign]
            theta_min, theta_max = min(thetas), max(thetas)
            pg.draw.arc(surface, self.COLORS[loop + 1], (*top_left, rad * 2, rad * 2), theta_min,
                        theta_max, min(line_w, rad))

    def get_pos(self, progress):
        theta = self.theta_i + (self.theta_f - self.theta_i) * progress
        return [self.center[0] + self.radius * math.cos(theta), self.center[1] - self.radius * math.sin(theta)]

    def get_start(self):
        return [self.center[0] + self.radius * math.cos(self.theta_i),
                self.center[1] - self.radius * math.sin(self.theta_i)]

    def get_end(self):
        return [self.center[0] + self.radius * math.cos(self.theta_f),
                self.center[1] - self.radius * math.sin(self.theta_f)]

    def to_bytes(self):
        return super().to_bytes() + pack('f' * 5, *self.center, self.radius, self.theta_i, self.theta_f)

    def from_bytes(self, path_data):
        self.center = unpack('f' * 2, path_data[:8])
        self.radius, self.theta_i, self.theta_f = unpack('f' * 3, path_data[8:20])
        self.length = abs((self.theta_f - self.theta_i) * self.radius)
        return path_data[20:]


class Start(Path):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.idx = START
        self.pos = pos

    def draw(self, surface, line_w):
        w = surface.get_size()[0]
        pos = [int(self.pos[0] * w), int(self.pos[1] * w)]
        pg.draw.circle(surface, (0, 200, 200), pos, line_w)

    def get_start(self):
        return self.pos

    def get_end(self):
        return self.pos

    def to_bytes(self):
        return super().to_bytes() + pack('f' * 2, *self.pos)

    def from_bytes(self, path_data):
        self.pos = unpack('f' * 2, path_data[:8])
        return path_data[8:]


constructors = {START: Start, LINE: Line, CIRCLE: Circle}

# Stores enemy data for spawning enemies
LINEAR, PARABOLIC, EXPONENTIAL = range(3)
# Input fraction between 0 and 1
get_y = {LINEAR: lambda t: t,
         PARABOLIC: lambda t: t * t,
         EXPONENTIAL: lambda t: math.exp(t) - 1}
# Return fraction between 0 and 1
get_t = {LINEAR: lambda y: y,
         PARABOLIC: lambda y: math.sqrt(y),
         EXPONENTIAL: lambda y: math.log(y + 1)}


class Spawn:
    def __init__(self, enemy_count=1, duration=1000, model=LINEAR, flip=False):
        self.num_enemies = enemy_count
        # Length of spawn sections in milliseconds
        self.duration = duration
        self.model = model
        self.flip = flip
        # Dictionary containing chances to spawn each enemy type
        self.chances = {}
        for key in ENEMY_ORDER:
            self.chances[key] = 0
        from Game.Enemy import ENEMY_1
        self.chances[ENEMY_1] = 1

    @property
    def y_to_count(self):
        # Gets the conversion from model function value to enemy count
        return self.num_enemies / get_y[self.model](1)

    def draw_img(self, w, h, draw_chances):
        if w == -1:
            w = h * self.duration // 1000
        s = pg.Surface((w, h))
        # Draw some pretty lines
        pg.draw.line(s, (255, 255, 255), (0, h // 2), (w - 1, h // 2))
        pg.draw.line(s, (255, 255, 255), (0, 0), (0, h - 1))
        pg.draw.line(s, (255, 255, 255), (w - 1, 0), (w - 1, h - 1))
        # Draw each enemy at its spawn time
        y_i, y_f = h // 4, h * 3 // 4
        for i in range(self.num_enemies):
            dx = int((w - 1) * self.get_time(i + 1))
            pg.draw.line(s, (0, 200, 0), (dx, y_i), (dx, y_f))
        # Check if we show draw enemy frequencies
        if draw_chances:
            s.blit(self.draw_chances(w * 3 // 4, h // 8), (w // 8, h // 16))
        return s

    def draw_chances(self, w, h):
        total = sum(self.chances.values())
        x = 0
        s = pg.Surface((w, h))
        for key in ENEMY_ORDER:
            if self.chances[key] > 0:
                dx = int(w * self.chances[key] / total)
                s.fill(data.enemies[key].color, (x, 0, dx, h))
                x += dx
        return s

    def get_count(self, t):
        t /= self.duration
        if self.flip:
            t = 1 - t
        return int(get_y[self.model](t) * self.y_to_count + 1)

    def get_time(self, count):
        y = (count - 1) / self.y_to_count
        t = get_t[self.model](y)
        return t if not self.flip else 1 - t

    def to_bytes(self):
        result = self.num_enemies.to_bytes(1, byteorder) + self.duration.to_bytes(2, byteorder)
        result += self.model.to_bytes(1, byteorder) + self.flip.to_bytes(1, byteorder)
        result += len(self.chances.keys()).to_bytes(1, byteorder)
        for key in self.chances.keys():
            result += key.to_bytes(1, byteorder)
            result += pack('f', self.chances[key])
        return result

    def from_bytes(self, enemy_data):
        if len(enemy_data) < 6:
            print("Missing Bytes")
            return ""
        self.num_enemies = int.from_bytes(enemy_data[0:1], byteorder)
        self.duration = int.from_bytes(enemy_data[1:3], byteorder)
        self.model = int.from_bytes(enemy_data[3:4], byteorder)
        self.flip = bool.from_bytes(enemy_data[4:5], byteorder)
        dict_len = int.from_bytes(enemy_data[5:6], byteorder)
        enemy_data = enemy_data[6:]
        for i in range(dict_len):
            if len(enemy_data) < 5:
                print("Missing Bytes")
                return ""
            else:
                key = int.from_bytes(enemy_data[:1], byteorder)
                val = unpack('f', enemy_data[1:5])
                self.chances[key] = val[0]
                enemy_data = enemy_data[5:]
        return enemy_data
