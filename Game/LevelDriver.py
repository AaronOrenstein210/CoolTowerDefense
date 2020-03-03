# Created on 27 January 2020
# Created by Kyle Doster
from random import randint
from pygame.locals import *
from Game.level_objects import *
from Game.Tower import TOWER_ORDER
from Game.Enemy import ENEMY_ORDER, Enemy
from random import uniform
import data

LOST, PLAYING, WON = -1, 0, 1


# Used to show the level path when paused
class TestEnemy(Enemy):
    def __init__(self):
        super().__init__(-1, strength=0, velocity=3, dim=(.05, .05), img="res/test_enemy.png")

    def reset(self, pos):
        self.path = 0
        self.progress = 0
        self.set_pos(pos)


def rand_pos():
    return uniform(.1, .9), uniform(.1, .9)


# Runs the level
class LevelDriver:
    TOWER_COLUMNS = 2
    tower_imgs = {idx: None for idx in TOWER_ORDER}

    def __init__(self):
        self.data = data
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.test_enemy = TestEnemy()

        self.hp = self.money = 0

        # Wave progress and spawn chances
        self.progression = self.wave_chances = None
        # Menu and menu tower scroll surfaces
        self.menu = self.menu_towers = None
        # Tower being dragged to place
        self.drag_tower = DragObject()
        # Menu rectangles
        self.rects = {"menu": pg.Rect(0, 0, 0, 0),
                      "hp": pg.Rect(0, 0, 0, 0),
                      "money": pg.Rect(0, 0, 0, 0),
                      "towers": pg.Rect(0, 0, 0, 0),
                      "pause": pg.Rect(0, 0, 0, 0),
                      "progress": pg.Rect(0, 0, 0, 0),
                      "chances": pg.Rect(0, 0, 0, 0)}
        # Scroll amount of menu tower list, <= 0
        self.towers_scroll = 0
        # Width of a tower sprite in the menu
        self.menu_tower_w = 0
        # Menu text font
        self.menu_font = None
        # Type of tower being dragged
        self.drag_tower_idx = -1
        # Tower currently being clicked on
        self.selected_tower = None

        self.time = 0
        self.paths = []
        self.waves = []
        self.wave_num = 0
        self.finished_lvl = False

        self.paused = False
        self.game_status = PLAYING

        # Background surface
        self.background = None

    # Called every iteration of the while loop
    def tick(self, dt):
        if self.game_status == PLAYING:
            if self.paused:
                if not self.move_enemy(self.test_enemy, dt):
                    self.test_enemy.reset(self.get_start())
            else:
                # Update towers/projectiles and move enemies
                for i in self.towers:
                    i.tick(dt)
                for i in self.projectiles:
                    if not i.tick(dt):
                        self.projectiles.remove(i)
                    else:
                        for j in self.enemies:
                            if i.polygon.collides_polygon(j.polygon):
                                self.enemies.remove(j)
                                strength = ENEMY_ORDER.index(j.idx) + 1
                                # If projectile damage equals enemy strength, delete the projectile
                                if strength == i.damage:
                                    self.projectiles.remove(i)
                                    self.add_money(strength)
                                # If the projectile damage is less than enemy strength, delete the projectile
                                # and create a new enemy of appropriate strength
                                elif strength > i.damage:
                                    self.projectiles.remove(i)
                                    new_enemy = type(data.enemies[ENEMY_ORDER[strength - i.damage - 1]])()
                                    new_enemy.set_progress(j.path, j.progress)
                                    self.enemies.append(new_enemy)
                                    self.add_money(i.damage)
                                # If the projectile damage is greater than enemy strength,
                                # lower its damage appropriately
                                else:
                                    i.damage -= strength
                                    self.add_money(strength)
                                break
                for i in self.enemies:
                    if not self.move_enemy(i, dt):
                        self.damage(i.strength)
                        self.enemies.remove(i)
                        # Check lost
                        if self.hp <= 0:
                            self.end(False)
                            return
                # Spawn enemies
                if not self.finished_lvl:
                    self.spawn_enemies(dt)
                # Move to the next wave or win the game
                elif len(self.enemies) == 0:
                    self.time = 0
                    self.finished_lvl = False
                    self.wave_num += 1
                    if self.wave_num >= len(self.waves):
                        self.end(True)
                        return
                        # Get change in mouse position every time so that it can update the last mouse position
            mouse_delta = pg.mouse.get_rel()
            # Check if we are dragging a tower
            if self.drag_tower.dragging:
                self.drag_tower.drag(mouse_delta)
        # Redraw the screen
        self.draw()

    # Gets the start of the enemy path
    def get_start(self):
        if len(self.paths) == 0:
            return [0, 0]
        else:
            return self.paths[0].get_start()

    # Spawns enemies based on the passage of time
    def spawn_enemies(self, dt):
        t_i = self.time
        t_f = self.time + dt
        wave = self.waves[self.wave_num]
        for idx, spawn in enumerate(wave):
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
                            self.enemies.append(type(data.enemies[key])())
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
                            self.enemies.append(type(data.enemies[key])())
                            break
                t_i = 0
                t_f -= spawn.duration
                if idx == len(wave) - 1:
                    self.finished_lvl = True
                # Update wave chances
                else:
                    r = self.rects["chances"]
                    self.wave_chances = wave[idx + 1].draw_chances(*r.size)
                    self.menu.fill((0, 0, 0), r)
                    self.menu.blit(self.wave_chances, r)
        # If time is 0, draw the new wave
        if self.time == 0:
            self.draw_wave()
        else:
            # Update wave progression
            r = self.rects["progress"]
            off_x = int(self.progression.get_size()[0] * self.time / sum([i.duration for i in wave]))
            self.menu.fill((0, 0, 0), r)
            self.menu.blit(self.progression, r, area=((off_x, 0), r.size))
        # Increment timer
        self.time += dt

    # Updates an enemy's position along the path
    def move_enemy(self, enemy, dt):
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

    # Draw the screen
    def draw(self):
        d = pg.display.get_surface()
        d.fill((0, 0, 0))
        d.blit(self.background, (data.off_x, data.off_y))
        # Draw enemies, towers, and projectiles
        for i in self.enemies + self.towers + self.projectiles:
            img_rect = i.blit_img.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                   int(i.pos[1] * data.screen_w) + data.off_y))
            d.blit(i.blit_img, img_rect)
        # If paused, draw the test enemy
        if self.paused:
            i = self.test_enemy
            img_rect = i.blit_img.get_rect(center=(int(i.pos[0] * data.screen_w) + data.off_x,
                                                   int(i.pos[1] * data.screen_w) + data.off_y))
            d.blit(i.blit_img, img_rect)
        # Draw selected tower range
        if self.selected_tower:
            self.selected_tower.draw()
        # Draw the menu
        d.blit(self.menu, self.rects["menu"])
        # Draw the tower being placed
        if self.drag_tower.dragging:
            self.drag_tower.draw()
        # Draw won and lose messages
        if self.game_status != PLAYING:
            dim = d.get_size()
            # Draw black overlay
            s = pg.Surface(dim)
            s.fill((0, 0, 0))
            s.set_alpha(128)
            d.blit(s, (0, 0))
            # Draw lost or won text
            text = "You Lost" if self.game_status == LOST else "You Won!"
            font = data.get_scaled_font(data.screen_w // 2, data.screen_w // 5, text)
            text_s = font.render(text, 1, (255, 255, 255))
            d.blit(text_s, text_s.get_rect(centerx=dim[0] // 2, bottom=dim[1] // 2))
            # Draw return to main screen text
            text = "Click to return to main screen"
            font = data.get_scaled_font(data.screen_w // 2, data.screen_w // 5, text)
            text_s = font.render(text, 1, (255, 255, 255))
            d.blit(text_s, text_s.get_rect(centerx=dim[0] // 2, top=dim[1] // 2))

    # Draws menu surface
    def draw_menu(self):
        w, h = data.screen_w // 5, data.screen_w
        img_w = h // 20

        # Establish rectangles
        self.rects["menu"] = pg.Rect(data.off_x + data.screen_w, data.off_y, w, h)
        # Top
        self.rects["hp"] = pg.Rect(img_w, 0, w - img_w, img_w)
        self.rects["money"] = self.rects["hp"].move(0, img_w)
        # Bottom
        self.rects["pause"] = pg.Rect((w - img_w) // 2, h - img_w, img_w, img_w)
        self.rects["chances"] = pg.Rect(0, self.rects["pause"].top - img_w * 3 // 4, w, img_w // 2)
        self.rects["progress"] = pg.Rect(0, self.rects["chances"].top - img_w * 9 // 4, w, img_w * 2)
        # Middle
        self.rects["towers"] = pg.Rect(0, self.rects["money"].bottom, w,
                                       self.rects["progress"].top - self.rects["money"].bottom)
        self.menu_tower_w = w // self.TOWER_COLUMNS

        # Create surface
        self.menu = pg.Surface((w, h))

        # Draw money and hp text
        self.menu_font = data.get_scaled_font(*self.rects["hp"].size, "999")
        self.add_money(0)
        self.damage(0)

        # Draw money and hp icons
        rect = self.rects["money"]
        img = data.scale_to_fit(pg.image.load("res/money.png"), w=img_w, h=img_w)
        img_rect = img.get_rect(center=(rect.x - img_w // 2, rect.centery))
        self.menu.blit(img, img_rect)
        rect = self.rects["hp"]
        img = data.scale_to_fit(pg.image.load("res/heart.png"), w=img_w, h=img_w)
        img_rect = img.get_rect(center=(rect.x - img_w // 2, rect.centery))
        self.menu.blit(img, img_rect)

        # Draw pause button
        path = "res/{}.png".format("play" if self.paused else "pause")
        img = data.scale_to_fit(pg.image.load(path), w=img_w, h=img_w)
        self.menu.blit(img, img.get_rect(center=self.rects["pause"].center))

        # Display towers
        cost_font = data.get_scaled_font(self.menu_tower_w, self.menu_tower_w // 3, "9999")
        self.menu_towers = pg.Surface((w, self.menu_tower_w * (math.ceil(len(TOWER_ORDER) / 2) + 1)))
        for idx in TOWER_ORDER:
            tower = data.towers[idx]
            col, row = idx % self.TOWER_COLUMNS, idx // self.TOWER_COLUMNS
            rect = pg.Rect(col * self.menu_tower_w, row * self.menu_tower_w, self.menu_tower_w, self.menu_tower_w)
            img = data.scale_to_fit(tower.img, w=self.menu_tower_w, h=self.menu_tower_w)
            self.menu_towers.blit(img, img.get_rect(center=rect.center))
            text = cost_font.render(str(tower.cost), 1, (128, 128, 128))
            self.menu_towers.blit(text, text.get_rect(bottomright=rect.bottomright))
            self.tower_imgs[idx] = img
        self.towers_scroll = 0
        self.menu.blit(self.menu_towers, self.rects["towers"],
                       area=((0, self.towers_scroll), self.rects["towers"].size))

        self.draw_wave()

    # Draws progression and chances for current wave
    def draw_wave(self):
        wave = self.waves[self.wave_num]
        # Draw the wave progression
        r = self.rects["progress"]
        self.progression = draw_spawn_list(wave, r.h, draw_chances=False)
        off_x = int(self.progression.get_size()[0] * self.time / sum([i.duration for i in wave]))
        self.menu.fill((0, 0, 0), r)
        self.menu.blit(self.progression, r, area=((off_x, 0), r.size))
        # Draw wave chances
        time = self.time
        for part in wave:
            time -= part.duration
            if time <= 0:
                r = self.rects["chances"]
                self.wave_chances = wave[0].draw_chances(*r.size)
                self.menu.fill((0, 0, 0), r)
                self.menu.blit(self.wave_chances, r)
                break

    # Draws the enemy path
    def draw_background(self):
        self.background = pg.Surface((data.screen_w, data.screen_w))
        # Fill the screen randomly with grass texture
        img_w = data.screen_w // 5
        img = pg.transform.scale(pg.image.load("res/grassblock.png"), (img_w, img_w))
        y_pos = 0
        while y_pos < data.screen_w:
            x_pos = 0
            while x_pos < data.screen_w:
                self.background.blit(img, (x_pos, y_pos))
                x_pos += randint(img_w // 2, img_w)
            y_pos += randint(img_w // 2, img_w)
        self.background.blit(draw_paths(data.screen_w, self.paths), (0, 0))

    def resize(self):
        self.background = pg.transform.scale(self.background, (data.screen_w, data.screen_w))
        # Get a list of objects to resize
        objects = self.enemies + self.towers + self.projectiles
        # Redraw objects
        for obj in objects:
            obj.resize()
        self.draw_menu()

    def select_tower(self, tower):
        self.selected_tower = None if self.selected_tower is tower else tower

    # Handles and event
    def input(self, event):
        if self.game_status == PLAYING:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    pos = pg.mouse.get_pos()
                    m_rect = self.rects["menu"]
                    if m_rect.collidepoint(*pos):
                        pos = [pos[0] - m_rect.x, pos[1] - m_rect.y]
                        t_rect = self.rects["towers"]
                        if t_rect.collidepoint(*pos):
                            pos = [pos[0] - t_rect.x, pos[1] - t_rect.y + self.towers_scroll]
                            col, row = pos[0] // self.menu_tower_w, pos[1] // self.menu_tower_w
                            idx = row * self.TOWER_COLUMNS + col
                            if idx < len(TOWER_ORDER):
                                if self.money >= data.towers[idx].cost:
                                    self.drag_tower_idx = idx
                                    dim = [int(d * data.screen_w) for d in data.towers[idx].dim]
                                    img = pg.transform.scale(data.towers[idx].img, dim)
                                    self.drag_tower.set_surface(img,
                                                                pos=[p / data.screen_w for p in data.get_mouse_pos()])
                                    self.drag_tower.dragging = True
                elif event.button == BUTTON_WHEELUP or event.button == BUTTON_WHEELDOWN:
                    pos = pg.mouse.get_pos()
                    if self.rects["menu"].collidepoint(*pos):
                        pos = [pos[0] - self.rects["menu"].x, pos[1] - self.rects["menu"].y]
                        rect = self.rects["towers"]
                        if rect.collidepoint(*pos):
                            if event.button == BUTTON_WHEELUP:
                                self.towers_scroll -= 2
                                if self.towers_scroll < 0:
                                    self.towers_scroll = 0
                            else:
                                self.towers_scroll += 2
                                max_scroll = max(0, self.menu_towers.get_size()[1] - rect.h)
                                if self.towers_scroll > max_scroll:
                                    self.towers_scroll = max_scroll
                            self.menu.fill((0, 0, 0), rect)
                            self.menu.blit(self.menu_towers, rect, area=((0, self.towers_scroll), rect.size))
                    elif self.selected_tower and self.selected_tower.upgrade_r.collidepoint(*pos):
                        self.selected_tower.scroll_upgrades(event.button == BUTTON_WHEELUP)
            if event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT:
                pos = pg.mouse.get_pos()
                # Check if we finished dragging a tower
                if self.drag_tower.dragging:
                    half_w = [w / 2 / data.screen_w for w in self.drag_tower.rect.size]
                    if all([w <= p <= 1 - w for p, w in zip(self.drag_tower.pos, half_w)]):
                        self.towers.append(type(data.towers[self.drag_tower_idx])(pos=self.drag_tower.pos))
                        self.add_money(-self.towers[-1].cost)
                        self.select_tower(self.towers[-1])
                    self.drag_tower.dragging = False
                else:
                    # Clicked the menu
                    if self.rects["menu"].collidepoint(*pos):
                        pos = [pos[0] - self.rects["menu"].x, pos[1] - self.rects["menu"].y]
                        if self.rects["pause"].collidepoint(*pos):
                            self.paused = not self.paused
                            # Reset test enemy
                            if self.paused:
                                self.test_enemy.reset(self.get_start())
                            # Update paused button
                            img_w = self.rects["pause"].w
                            path = "res/{}.png".format("play" if self.paused else "pause")
                            img = data.scale_to_fit(pg.image.load(path), w=img_w, h=img_w)
                            self.menu.fill((0, 0, 0, 0), self.rects["pause"])
                            self.menu.blit(img, img.get_rect(center=self.rects["pause"].center))
                    # Check clicking tower upgrades
                    elif not self.selected_tower or not self.selected_tower.click():
                        pos = [(pos[0] - data.off_x) / data.screen_w, (pos[1] - data.off_y) / data.screen_w]
                        # Check if we clicked a tower
                        for i in self.towers:
                            if i.polygon.collides_point(pos):
                                self.select_tower(i)
                                break
            return True
        else:
            return not (event.type == MOUSEBUTTONUP and event.button == BUTTON_LEFT)

    def end(self, won):
        self.game_status = WON if won else LOST
        self.drag_tower.dragging = False
        self.draw()

    # Adds input to money
    def add_money(self, amnt):
        self.money += amnt
        rect = self.rects["money"]
        self.menu.fill((0, 0, 0), rect)
        text = self.menu_font.render(str(self.money), 1, (255, 255, 255))
        text_rect = text.get_rect(centery=rect.centery, left=rect.left)
        self.menu.blit(text, text_rect)

    # Subtracts input from hp
    def damage(self, amnt):
        self.hp -= amnt
        rect = self.rects["hp"]
        self.menu.fill((0, 0, 0), rect)
        text = self.menu_font.render(str(self.hp), 1, (255, 255, 255))
        text_rect = text.get_rect(centery=rect.centery, left=rect.left)
        self.menu.blit(text, text_rect)

    def reset(self):
        # Reset object arrays
        self.enemies.clear()
        self.towers.clear()
        self.projectiles.clear()
        # Reset spawning variables
        self.time = self.wave_num = 0
        self.finished_lvl = False
        # Reset money and hp
        self.hp = self.money = 10000
        # Reset game status
        self.game_status = PLAYING
        # Reset ui variables
        self.paused = True
        self.test_enemy.reset(self.get_start())
        self.selected_tower = None
        # Call resize
        self.resize()

    # Sets level data
    def set_level(self, paths, waves):
        self.paths = paths
        self.waves = waves
        self.draw_background()
        self.reset()


class DragObject:
    def __init__(self):
        self.rect = pg.Rect(0, 0, 0, 0)
        self.surface = pg.Surface((0, 0))
        self.pos = [0, 0]
        self.dragging = False

    def set_pos(self, pos):
        self.pos = pos
        self.drag([0, 0])

    def set_surface(self, surface, pos=None):
        self.surface = surface
        self.rect = self.surface.get_rect()
        if pos:
            self.pos = pos
        self.drag([0, 0])

    def drag(self, dmouse):
        dmouse = [d / data.screen_w for d in dmouse]
        self.pos = [p + d for p, d in zip(self.pos, dmouse)]
        self.rect.center = [self.pos[0] * data.screen_w + data.off_x,
                            self.pos[1] * data.screen_w + data.off_y]

    def draw(self):
        pg.display.get_surface().blit(self.surface, self.rect)
