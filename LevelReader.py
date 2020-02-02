# Created on 27 January 2020
# Created by

import math


# Reads a level file and compiles the enemy path
class LevelReader:
    def __init__(self):
        self.surface = None

    # Return a new position for the enemy
    # Moves an enemy given its position and distance to be travelled
    # Mostly just coordinates the path's various segments
    def move(self, pos, d):
        pass

    # Loads a level from a file
    def load_file(self, name):
        pass


START, LINE, CIRCLE = range(3)


# Stores data for a specific segment of the enemy path
class Path:
    def __init__(self):
        self.idx = 0

    # Move an enemy along this path segment
    def move(self, pos, d):
        pass

    def get_start(self):
        pass

    def get_end(self):
        pass


class Line(Path):
    def __init__(self, start=(0, 0), end=(0, 0)):
        Path.__init__(self)
        self.idx = LINE
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end


class Circle(Path):
    COLORS = ((255, 255, 255), (175, 175, 0), (200, 0, 0), (0, 200, 0), (0, 0, 200))

    def __init__(self):
        Path.__init__(self)
        self.idx = CIRCLE
        self.center, self.radius = [0, 0], 0
        self.theta_i, self.theta_f = 0, 2 * math.pi

    def get_start(self):
        return [self.center[0] + self.radius * math.cos(self.theta_i),
                self.center[1] - self.radius * math.sin(self.theta_i)]

    def get_end(self):
        return [self.center[0] + self.radius * math.cos(self.theta_f),
                self.center[1] - self.radius * math.sin(self.theta_f)]


class Start(Path):
    def __init__(self, pos=(0, 0)):
        Path.__init__(self)
        self.pos = pos
        self.idx = START

    def get_start(self):
        return self.pos

    def get_end(self):
        return self.pos
