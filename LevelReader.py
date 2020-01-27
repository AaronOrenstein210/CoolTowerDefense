# Created on 27 January 2020
# Created by


# Reads a level file and compiles the enemy path
class LevelReader:
    def __init__(self):
        pass

    # Moves an enemy given its position and distance to be travelled
    # Mostly just coordinates the path's various segments
    def move(self, pos, d):
        pass

    # Loads a level from a file
    def load_file(self, name):
        pass


# Stores data for a specific segment of the enemy path
class Path:
    def __init__(self):
        pass

    # Move an enemy along this path segment
    def move(self, pos, d):
        pass


class Line(Path):
    def __init__(self):
        pass


class Circle(Path):
    def __init__(self):
        pass
