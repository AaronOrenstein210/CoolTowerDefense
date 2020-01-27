# Created on 27 January 2020
# Created by


# Runs the level
class LevelDriver:
    def __init__(self):
        self.enemies = self.towers = self.projectiles = []

    # Called every iteration of the while loop
    def tick(self, dt):
        self.draw()

    # Draw the screen
    def draw(self):
        pass
