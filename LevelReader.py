# Created on 27 January 2020
# Created by Poopy

from struct import pack, unpack
from sys import byteorder
from random import uniform
import math
import pygame as pg
import data


# Reads a level file and compiles the enemy path
class LevelReader:
    def __init__(self):
        self.surface = None
        self.paths = []
        self.spawn_list = []

    def get_enemy_spawns(self, t_i, t_f):
        spawns = []
        for spawn in self.spawn_list:
            if spawn.duration < t_i:
                t_i -= spawn.duration
                t_f -= spawn.duration
            elif spawn.duration >= t_f:
                for i in range(abs(spawn.get_count(t_f) - spawn.get_count(t_i))):
                    num = uniform(0, sum(v for v in spawn.chances.values()))
                    for key in spawn.chances.keys():
                        val = spawn.chances[key]
                        if val < num:
                            num -= val
                        else:
                            spawns.append(data.enemies[key]())
                            break
                break
            else:
                for i in range(abs(spawn.get_count(spawn.duration) - spawn.get_count(t_i))):
                    num = uniform(0, sum(v for v in spawn.chances.values()))
                    for key in spawn.chances.keys():
                        val = spawn.chances[key]
                        if val < num:
                            num -= val
                        else:
                            spawns.append(data.enemies[key]())
                            break
                t_i = 0
                t_f -= spawn.duration
        return spawns

    # Return a new position for the enemy
    # Moves an enemy given its position and distance to be travelled
    # Mostly just coordinates the path's various segments
    def move(self, enemy, dt):
        d = enemy.velocity * dt / 1000
        while d > 0:
            to_end = self.paths[enemy.path].length * (1 - enemy.progress)
            if d >= to_end:
                enemy.path += 1
                enemy.progress = 0
                if enemy.path >= len(self.paths):
                    return False
            else:
                enemy.progress += d / self.paths[enemy.path].length
            d -= to_end
        enemy.set_pos(*self.paths[enemy.path].get_pos(enemy.progress))
        return True

    def draw_surface(self):
        from data import screen_w
        self.surface = draw_paths(screen_w, self.paths)

    def set_level(self, paths, spawn_list):
        self.paths = paths
        self.spawn_list = spawn_list
        self.draw_surface()


# Loads a level from bytes
def load_paths(file_data):
    paths = []
    num = int.from_bytes(file_data[:1], byteorder)
    file_data = file_data[1:]
    for i in range(num):
        if len(file_data) == 0:
            print("Missing bytes")
            break
        # Get the path type and initialize its object
        idx = int.from_bytes(file_data[:1], byteorder)
        if idx in constructors.keys():
            paths.append(constructors[idx]())
        else:
            print("Unknown path type")
            break
        # Read path data
        file_data = file_data[1:]
        try:
            file_data = paths[-1].from_bytes(file_data)
        except IndexError:
            print("Missing Bytes")
            break
    return paths, file_data


# Draws a list of paths
def draw_paths(w, paths):
    s = pg.Surface((w, w), pg.SRCALPHA)
    line_w = w // 40
    for p in paths:
        if p.idx == LINE:
            pos_i = [int(p.start[0] * w), int(p.start[1] * w)]
            pos_f = [int(p.end[0] * w), int(p.end[1] * w)]
            pg.draw.line(s, (255, 255, 255), pos_i, pos_f, line_w)
            for pos in [pos_i, pos_f]:
                pg.draw.circle(s, (255, 255, 255), pos, line_w * 3 // 4)
        elif p.idx == CIRCLE:
            from data import TWO_PI
            c = [int(p.center[0] * w), int(p.center[1] * w)]
            rad = int(p.radius * w)
            # Get theta range
            d_theta = p.theta_f - p.theta_i
            sign = math.copysign(1, d_theta)
            d_theta = abs(d_theta)
            # Break theta range into full circles
            loop = -1
            while d_theta >= TWO_PI and loop < len(p.COLORS) - 1:
                loop += 1
                d_theta -= TWO_PI
            # Draw the highest full circle
            if loop >= 0:
                pg.draw.circle(s, p.COLORS[loop], c, rad, min(line_w, rad))
            # Draw the other sections
            if d_theta > 0 and loop < len(p.COLORS) - 1:
                top_left = [c[0] - rad, c[1] - rad]
                thetas = [p.theta_i, p.theta_i + d_theta * sign]
                theta_min, theta_max = min(thetas), max(thetas)
                pg.draw.arc(s, p.COLORS[loop + 1], (*top_left, rad * 2, rad * 2), theta_min,
                            theta_max, min(line_w, rad))
        elif p.idx == START:
            pos = [int(p.pos[0] * w), int(p.pos[1] * w)]
            pg.draw.circle(s, (0, 200, 200), pos, line_w)
    return s


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
def draw_spawn_list(w, h, spawn_list):
    s = pg.Surface((w, h))
    max_time = sum(i.duration for i in spawn_list)
    start_time = 0
    for i in spawn_list:
        w_ = w * i.duration // max_time
        x = w * start_time // max_time
        s.blit(i.get_img(w_, h), (x, 0))
        start_time += i.duration
    return s


START, LINE, CIRCLE = range(3)


# Stores path_data for a specific segment of the enemy path
class Path:
    def __init__(self):
        self.idx = 0
        self.length = 0

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
    COLORS = ((255, 255, 255), (175, 175, 0), (200, 0, 0), (0, 200, 0), (0, 0, 200))

    def __init__(self):
        super().__init__()
        self.idx = CIRCLE
        self.center, self.radius = [0, 0], 0
        self.theta_i, self.theta_f = 0, 2 * math.pi

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

    def get_start(self):
        return self.pos

    def get_end(self):
        return self.pos

    def to_bytes(self):
        return super().to_bytes() + pack('f' * 2, *self.pos)

    def from_bytes(self, path_data):
        self.pos = unpack('f' * 2, path_data[:8])
        return path_data[8:]


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
        for key in data.enemies.keys():
            self.chances[key] = 0
        from MyObjects import ENEMY_1
        self.chances[ENEMY_1] = 1

    @property
    def y_to_count(self):
        # Gets the conversion from model function value to enemy count
        return self.num_enemies / get_y[self.model](1)

    def get_img(self, w, h):
        s = pg.Surface((w, h))
        # Draw some pretty lines
        pg.draw.line(s, (255, 255, 255), (0, h // 2), (w - 1, h // 2))
        pg.draw.line(s, (255, 255, 255), (0, 0), (0, h - 1))
        pg.draw.line(s, (255, 255, 255), (w - 1, 0), (w - 1, h - 1))
        # Draw each enemy spawn time
        y_i, y_f = h // 4, h * 3 // 4
        for i in range(self.num_enemies):
            dx = int((w - 1) * self.get_time(i + 1))
            pg.draw.line(s, (0, 200, 0), (dx, y_i), (dx, y_f))
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


constructors = {START: Start, LINE: Line, CIRCLE: Circle}
