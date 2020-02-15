# Created on 27 January 2020
# Created by 

from pygame.locals import *
from random import uniform, randint
from MyObjects import *
from LevelReader import draw_paths
import data


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    def __init__(self):
        # Lists of objects
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.background = None
        self.paths = []
        self.spawn_list = []
        # Time since start of game, not including paused sections
        self.time = 0
        # If we are paused or not
        self.paused = False
        # Test enemy used to show enemy path
        self.test_enemy = None

    # Returns the starting position for new enemies
    def get_start(self):
        if len(self.paths) > 0:
            return self.paths[0].get_start()
        else:
            return [0, 0]

    # Updates game
    def tick(self, dt):
        if not self.paused:
            # Move all enemies, and update towers/projectiles
            for i in self.enemies:
                if not self.move(i, dt):
                    if i.idx != TEST_ENEMY:
                        print("Lost a Life")
                    self.enemies.remove(i)
            for i in self.towers:
                self.projectiles += i.tick(dt)
            for i in self.projectiles:
                if not i.tick(dt):
                    self.projectiles.remove(i)
                else:
                    for j in self.enemies:
                        if i.polygon.collides_polygon(j.polygon):
                            self.projectiles.remove(i)
                            self.enemies.remove(j)
                            break
            # Get all enemy spawns
            self.spawn_enemies(dt)
            self.time += dt
        if self.test_enemy is not None and not self.move(self.test_enemy, dt):
            self.test_enemy = None
        # Redraw the screen
        self.draw()

    # Spawns enemies based on the passage of time
    def spawn_enemies(self, dt):
        t_f = self.time + dt
        for spawn in self.spawn_list:
            if spawn.duration < self.time:
                self.time -= spawn.duration
                t_f -= spawn.duration
            elif spawn.duration >= t_f:
                for i in range(abs(spawn.get_count(t_f) - spawn.get_count(self.time))):
                    num = uniform(0, sum(v for v in spawn.chances.values()))
                    for key in spawn.chances.keys():
                        val = spawn.chances[key]
                        if val < num:
                            num -= val
                        else:
                            self.enemies.append(data.enemies[key]())
                            break
                break
            else:
                for i in range(abs(spawn.get_count(spawn.duration) - spawn.get_count(self.time))):
                    num = uniform(0, sum(v for v in spawn.chances.values()))
                    for key in spawn.chances.keys():
                        val = spawn.chances[key]
                        if val < num:
                            num -= val
                        else:
                            self.enemies.append(data.enemies[key]())
                            break
                self.time = 0
                t_f -= spawn.duration

    # Updates an enemy's position along the path
    def move(self, enemy, dt):
        d = enemy.v * dt / 1000
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
        enemy.set_pos(self.paths[enemy.path].get_pos(enemy.progress))
        return True

    # Handles a UI event
    def handle_event(self, e):
        if e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
            pos = data.get_mouse_pos()
            pos = [p / data.screen_w for p in pos]
            num = randint(1, 10)
            if num > 6:
                self.towers.append(Tower1(pos=pos))
            elif num > 3:
                self.towers.append(Tower2(pos=pos))
            elif num > 1:
                self.towers.append(Ballista(pos=pos))
            else:
                self.towers.append(AAGun(pos=pos))
            self.paused = not self.paused
            if self.paused:
                self.test_enemy = TestEnemy()

    # Draws the screen
    def draw(self):
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        d.blit(self.background, (data.off_x, data.off_y))
        # Get a list of objects to draw
        objects = self.enemies + self.towers + self.projectiles
        if self.test_enemy is not None:
            objects.append(self.test_enemy)
        # Draw the objects
        for obj in objects:
            img_rect = obj.blit_img.get_rect(center=(int(obj.pos[0] * data.screen_w) + data.off_x,
                                                     int(obj.pos[1] * data.screen_w) + data.off_y))
            d.blit(obj.blit_img, img_rect)

    # Draws the background
    def draw_background(self):
        from data import screen_w
        self.background = draw_paths(screen_w, self.paths)

    def resize(self):
        self.draw_background()
        # Get a list of objects to resize
        objects = self.enemies + self.towers + self.projectiles
        if self.test_enemy is not None:
            objects.append(self.test_enemy)
        # Redraw objects
        for obj in objects:
            img_dim = (int(obj.dim[0] * data.screen_w), int(obj.dim[1] * data.screen_w))
            obj.img = pg.transform.scale(obj.img, img_dim)
            obj.blit_img = pg.transform.rotate(obj.img, obj.angle)

    # Resets data
    def reset(self):
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        self.time = 0

    # Sets level data
    def set_level(self, paths, spawn_list):
        self.reset()
        self.paths = paths
        self.spawn_list = spawn_list
        self.draw_background()
