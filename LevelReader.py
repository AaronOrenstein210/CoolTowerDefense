# Created on 27 January 2020
# Created by

from struct import pack, unpack
from sys import byteorder
import math
import pygame as pg
import data


# Reads a level file and compiles the enemy path
class LevelReader:
    def __init__(self):
        self.surface = None
        self.paths = []

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
                    print("Lost a Life")
                    return False
            else:
                enemy.progress += d / self.paths[enemy.path].length
            d -= to_end
        enemy.pos = self.paths[enemy.path].get_pos(enemy.progress)
        return True

    def draw_surface(self):
        from data import off_x, off_y, screen_w
        self.surface = draw_paths(pg.Rect(off_x, off_y, screen_w, screen_w), self.paths)

    # Loads a level from bytes
    def load_from_bytes(self, file_data):
        self.paths.clear()
        while len(file_data) > 0:
            # Get the path type and initialize its object
            idx = int.from_bytes(file_data[:1], byteorder)
            if idx in constructors.keys():
                self.paths.append(constructors[idx]())
            else:
                print("Unknown path type")
                break
            # Read path path_data
            file_data = file_data[1:]
            num_bytes = self.paths[-1].num_bytes
            if len(file_data) < num_bytes:
                print("Expected {} bytes, found {} bytes".format(num_bytes, len(file_data)))
                break
            else:
                self.paths[-1].from_bytes(file_data[:num_bytes])
                file_data = file_data[num_bytes:]
        self.draw_surface()


def draw_paths(rect, paths):
    s = pg.Surface(rect.size)
    s.fill((0, 175, 0))
    w = rect.w // 40
    for p in paths:
        if p.idx == LINE:
            pos_i = [int(p.start[0] * rect.w), int(p.start[1] * rect.h)]
            pos_f = [int(p.end[0] * rect.w), int(p.end[1] * rect.h)]
            pg.draw.line(s, (255, 255, 255), pos_i, pos_f, w)
            for pos in [pos_i, pos_f]:
                pg.draw.circle(s, (255, 255, 255), pos, w * 3 // 4)
        elif p.idx == CIRCLE:
            from data import TWO_PI
            c = [int(p.center[0] * rect.w), int(p.center[1] * rect.h)]
            rad = int(p.radius * rect.w)
            # Get theta range
            d_theta = p.theta_f - p.theta_i
            sign = math.copysign(1, d_theta)
            d_theta = abs(d_theta)
            # Break theta range into full circles
            loop = -1
            while d_theta >= TWO_PI:
                loop += 1
                d_theta -= TWO_PI
            # Draw the highest full circle
            if loop >= 0:
                pg.draw.circle(s, p.COLORS[loop], c, rad, min(w, rad))
            # Draw the other sections
            if d_theta > 0 and loop < len(p.COLORS) - 1:
                top_left = [c[0] - rad, c[1] - rad]
                thetas = [p.theta_i, p.theta_i + d_theta * sign]
                theta_min, theta_max = min(thetas), max(thetas)
                pg.draw.arc(s, p.COLORS[loop + 1], (*top_left, rad * 2, rad * 2), theta_min,
                            theta_max, min(w, rad))
        elif p.idx == START:
            pos = [int(p.pos[0] * rect.w), int(p.pos[1] * rect.h)]
            pg.draw.circle(s, (0, 200, 200), pos, w)
    return s


START, LINE, CIRCLE = range(3)


# Stores path_data for a specific segment of the enemy path
class Path:
    def __init__(self):
        self.idx = 0
        self.num_bytes = 0
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
        pass


class Line(Path):
    def __init__(self, start=(0, 0), end=(0, 0)):
        super().__init__()
        self.idx = LINE
        self.num_bytes = 16
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
        self.end = unpack('f' * 2, path_data[8:])
        self.length = data.get_distance(self.start, self.end)


class Circle(Path):
    COLORS = ((255, 255, 255), (175, 175, 0), (200, 0, 0), (0, 200, 0), (0, 0, 200))

    def __init__(self):
        super().__init__()
        self.idx = CIRCLE
        self.num_bytes = 20
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
        self.radius, self.theta_i, self.theta_f = unpack('f' * 3, path_data[8:])
        self.length = abs((self.theta_f - self.theta_i) * self.radius)


class Start(Path):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.idx = START
        self.num_bytes = 8
        self.pos = pos

    def get_start(self):
        return self.pos

    def get_end(self):
        return self.pos

    def to_bytes(self):
        return super().to_bytes() + pack('f' * 2, *self.pos)

    def from_bytes(self, path_data):
        self.pos = unpack('f' * 2, path_data)


constructors = {START: Start, LINE: Line, CIRCLE: Circle}
