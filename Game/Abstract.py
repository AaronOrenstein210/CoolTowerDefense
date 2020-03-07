from os.path import isfile
import pygame as pg
import math
import data
from Game.collision import Polygon


class Sprite:
    def __init__(self, pos=(0, 0), w=.1, angle=0, img=""):
        self.pos = pos
        self.polygon = None
        self.angle = angle

        w_ = int(w * data.screen_w)
        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.img = data.scale_to_fit(pg.image.load(img), w=w_)
        else:
            self.img = pg.Surface((w_, w_))
        self.dim = [w, self.img.get_size()[1] / data.screen_w]
        # Just blit this surface, not self.img
        self.blit_img = self.img

        self.set_pos(pos)

    def set_pos(self, pos):
        self.pos = pos
        half_w, half_h = self.dim[0] / 2, self.dim[1] / 2
        points = []
        for signs in [[-1, 1], [1, 1], [1, -1], [-1, -1]]:
            points.append(rotate_point([pos[0] + signs[0] * half_w, pos[1] + signs[1] * half_h], pos, self.angle))
        self.polygon = Polygon(points)

    def set_angle(self, angle):
        self.angle = angle
        # Recalculate polygon
        self.set_pos(self.pos)
        self.blit_img = pg.transform.rotate(self.img, self.angle - 90)

    def set_img(self, img):
        w = self.dim[0] * data.screen_w
        self.img = data.scale_to_fit(img, w=w)
        self.dim[1] = self.img.get_size()[1] / data.screen_w
        # Recalculate polygon and blit image
        self.set_angle(self.angle)

    def resize(self):
        img_dim = [int(d * data.screen_w) for d in self.dim]
        self.img = pg.transform.scale(self.img, img_dim)
        self.blit_img = pg.transform.rotate(self.img, self.angle)


targeting_names = ["First", "Closest", "Strongest"]


class Tower(Sprite):
    def __init__(self, idx, cooldown=1000, cost=10, shoot_range=.1, **kwargs):
        super().__init__(**kwargs)
        self.idx = idx
        self.cooldown = cooldown
        self.cost = cost
        self.timer = 0
        self.range = shoot_range
        # Index of current upgrade
        self.upgrade_lvl = -1
        # Surface and rectangle of upgrade menu
        self.upgrade_s = None
        self.upgrade_r = pg.Rect(0, 0, 0, 0)
        # Surface and rectangle for top of upgrade menu (tower info)
        self.tower_s = self.tower_font = None
        self.tower_r = pg.Rect(0, 0, 0, 0)
        # Menu scroll
        self.scroll = 0
        # Determines how to pick enemy targets
        self.targeting = targeting_names[0]

    @property
    def upgrade_w(self):
        return data.screen_w // 5

    @property
    def text_h(self):
        return self.tower_r.h // 3

    def set_img(self, img):
        super().set_img(img)
        self.draw_upgrade_top()

    # Returns the array of upgrades for this tower
    # At run time, this will be called and the result stored
    # For every unique tower type
    def get_upgrades(self):
        return []

    def resize(self):
        super().resize()
        self.set_up_upgrades()

    # Draws range, upgrade menu, and any upgrade descriptions to screen
    def draw(self):
        pos = pg.mouse.get_pos()
        d = pg.display.get_surface()
        # Draw tower range
        r = int(self.range * data.screen_w)
        s = pg.Surface((r * 2, r * 2))
        pg.draw.circle(s, (0, 0, 255), (r, r), r)
        s.set_alpha(64)
        s.set_colorkey((0, 0, 0))
        d.blit(s, (int(self.pos[0] * data.screen_w - r + data.off_x),
                   int(self.pos[1] * data.screen_w - r + data.off_y)))
        # Draw upgrade menu
        d.fill((0, 0, 0), self.tower_r)
        d.blit(self.tower_s, self.tower_r)
        d.fill((0, 0, 0), self.upgrade_r)
        d.blit(self.upgrade_s, self.upgrade_r, area=((0, self.scroll), self.upgrade_r.size))
        # Draw upgrade description if hovering over it
        if self.upgrade_r.collidepoint(*pos):
            idx = (pos[1] - self.upgrade_r.y + self.scroll) // self.upgrade_w
            if idx < len(data.upgrades[self.idx]):
                topleft = [self.upgrade_r.x, self.upgrade_r.y + idx * self.upgrade_w + self.scroll]
                topleft[0] += self.upgrade_w if self.pos[0] >= .5 else -2 * self.upgrade_w
                d.blit(data.upgrades[self.idx][idx].description_s, topleft)

    # Draws the top of the upgrade menu
    def draw_upgrade_top(self):
        text_h, w = self.text_h, self.upgrade_w
        # Draw tower info surface menu surface
        self.tower_r = pg.Rect(data.off_x, data.off_y, w, w * 2 // 3)
        self.tower_s = pg.Surface((w, w * self.tower_r.h))
        # Draw tower image
        text_h = self.text_h
        img = data.scale_to_fit(self.img, w=w, h=self.tower_r.h - text_h)
        self.tower_s.blit(img, img.get_rect(center=(w // 2, (self.tower_r.h - text_h) // 2)))
        # Draw tower targeting type
        self.tower_font = data.get_scaled_font(w, text_h, "Targeting: " + data.get_widest_string(targeting_names))
        text = self.tower_font.render("Targeting: " + self.targeting, 1, (255, 255, 255))
        self.tower_s.blit(text, text.get_rect(center=(w // 2, self.tower_r.h - text_h // 2)))
        # Check which side to draw the upgrade menu
        if self.pos[0] < .5:
            self.tower_r.move_ip(data.screen_w - w, 0)

    # Draws the surface containing this tower's upgrades
    def set_up_upgrades(self):
        w = self.upgrade_w
        self.draw_upgrade_top()
        # Draw upgrade menu surface
        self.upgrade_s = pg.Surface((w, w * len(data.upgrades[self.idx])))
        for i, upgrade in enumerate(data.upgrades[self.idx]):
            upgrade.draw_img(self.upgrade_s, pg.Rect(0, i * w, w, w), i <= self.upgrade_lvl)
        self.upgrade_r = pg.Rect(data.off_x, self.tower_r.bottom, w, data.screen_w)
        # Check if the rectangles should be on the other side of the screen
        if self.pos[0] < .5:
            self.upgrade_r.move_ip(data.screen_w - w, 0)

    # Changes upgrade surfcae scroll
    def scroll_upgrades(self, up):
        amnt = self.upgrade_r.h // 20
        if up:
            self.scroll -= amnt
            if self.scroll < 0:
                self.scroll = 0
        else:
            self.scroll += amnt
            max_scroll = max(0, self.upgrade_s.get_size()[1] - self.upgrade_r.h)
            if self.scroll > max_scroll:
                self.scroll = max_scroll

    # Checks for clicks on the upgrade ui, returns whether we clicked the menu or not
    def click(self):
        pos = pg.mouse.get_pos()
        if self.tower_r.collidepoint(*pos):
            text_h = self.text_h
            if pos[1] - self.tower_r.y >= self.tower_r.h - text_h:
                idx = (targeting_names.index(self.targeting) + 1) % len(targeting_names)
                self.targeting = targeting_names[idx]
                rect = pg.Rect(0, self.tower_r.h - text_h, self.tower_r.w, text_h)
                self.tower_s.fill((0, 0, 0), rect)
                text = self.tower_font.render("Targeting: " + self.targeting, 1, (255, 255, 255))
                self.tower_s.blit(text, text.get_rect(center=rect.center))
        elif self.upgrade_r.collidepoint(*pos):
            idx = (pos[1] - self.upgrade_r.y + self.scroll) // self.upgrade_w
            upgrades = data.upgrades[self.idx]
            if idx < len(upgrades) and idx == self.upgrade_lvl + 1 and \
                    upgrades[idx].cost <= data.lvlDriver.money:
                upgrades[idx].draw_img(self.upgrade_s,
                                       pg.Rect(0, idx * self.upgrade_w, self.upgrade_w, self.upgrade_w), True)
                self.upgrade()
                data.lvlDriver.add_money(-upgrades[idx].cost)
        else:
            return False
        return True

    # Performs an upgrade
    def upgrade(self):
        self.upgrade_lvl += 1
        self.set_img(data.upgrades[self.idx][self.upgrade_lvl].img)

    # Return a list of projectiles to shoot at the given enemy
    def shoot(self, enemy):
        return []

    # Place any modifications to projectiles here (e.g. from upgrades)
    def modify_projectile(self, projectile):
        pass

    # Called every unpaused game tick TODO: Base in range on whole enemy, not just center
    def tick(self, dt):
        self.timer += dt
        while self.timer >= self.cooldown:
            self.timer -= self.cooldown
            # Get all enemies in range
            in_range = [e for e in data.lvlDriver.enemies if data.get_distance(self.pos, e.pos) < self.range]
            # Shoot the enemies based on shooting ai
            if len(in_range) > 0:
                # Get target enemy based on targeting method
                if self.targeting == "First":
                    enemy = first_enemy(in_range)
                elif self.targeting == "Closest":
                    enemy = closest_enemy(in_range, self.pos)
                elif self.targeting == "Strongest":
                    enemy = strongest_enemy(in_range)
                else:
                    continue
                # Shoot the projectile(s)
                arr = self.shoot(enemy)
                if arr:
                    pg.mixer.Channel(1).play(data.shoot_audio)
                for projectile in arr:
                    self.modify_projectile(projectile)
                    data.lvlDriver.projectiles.append(projectile)
                # Rotate to face the enemy
                self.set_angle(data.get_angle_pixels(self.pos, enemy.pos) * 360 // data.TWO_PI)


class Upgrade:
    def __init__(self, description="No Description", cost=0, img=""):
        # Save cost
        self.cost = cost
        # Break up description by "\n"'s
        self.description = description.split("\n")

        self.img = None
        if isfile(img) and (img.endswith(".png") or img.endswith(".jpg")):
            self.img = pg.image.load(img)

        self.description_s = None

    def draw_img(self, s, rect, bought):
        # Draw background
        back = data.scale_to_fit(pg.image.load("res/upgrade_back.png"), w=rect.w, h=rect.h)
        s.blit(back, back.get_rect(center=rect.center))
        # Draw cost text
        text_h = rect.h // 5
        font = data.get_scaled_font(rect.w, text_h, "Bought")
        string = "Bought" if bought else "${}".format(self.cost)
        text = font.render(string, 1, (255, 255, 255))
        s.blit(text, text.get_rect(center=(rect.centerx, rect.bottom - text_h // 2)))
        # Scale and draw the image
        img = data.scale_to_fit(self.img, w=rect.w, h=rect.h - text_h)
        s.blit(img, img.get_rect(center=(rect.centerx, rect.centery - text_h // 2)))
        if not bought:
            img = data.scale_to_fit(pg.image.load("res/lock.png"), w=rect.w, h=rect.h - text_h)
            s.blit(img, img.get_rect(center=(rect.centerx, rect.centery - text_h // 2)))
        # Draw description
        self.description_s = pg.Surface((rect.w * 2, rect.h))
        dim = self.description_s.get_size()
        text_h = dim[1] // 6
        font = data.get_scaled_font(dim[0], text_h, "")
        i = 0
        for line in self.description:
            for string in data.wrap_text(line, font, dim[0]):
                text = font.render(string, 1, (255, 255, 255))
                text_rect = text.get_rect(center=(dim[0] // 2, int(text_h * (i + .5))))
                self.description_s.blit(text, text_rect)
                i += 1


def first_enemy(arr):
    return max(arr, key=lambda e: e.path + e.progress)


def closest_enemy(arr, pos):
    return min(arr, key=lambda e: data.get_distance(pos, e.pos))


def strongest_enemy(arr):
    return max(arr, key=lambda e: e.strength)


class Projectile(Sprite):
    def __init__(self, damage=1, speed=.5, **kwargs):
        super().__init__(**kwargs)
        self.damage = damage
        self.speed = speed

    def tick(self, dt):
        d = (self.speed * dt) / 1000
        dx = d * math.cos(self.angle)
        # Flip y for pixel coords
        dy = -d * math.sin(self.angle)
        self.set_pos((self.pos[0] + dx, self.pos[1] + dy))
        return 0 <= self.pos[0] <= 1 and 0 <= self.pos[1] <= 1


class Enemy(Sprite):
    def __init__(self, idx, hp=1, velocity=.1, **kwargs):
        super().__init__(**kwargs)
        if data.lvlDriver is not None:
            self.set_pos(data.lvlDriver.get_start())
        self.idx = idx
        self.hp = hp
        self.path = 0
        self.progress = 0
        self.v = velocity
        self.color = (0, 0, 0, 0)

    def set_progress(self, path, progress):
        self.path = path
        self.progress = progress

    # Get what enemies to spawn when this enemy dies
    def die(self):
        from Game.Enemy import ENEMY_ORDER
        idx = ENEMY_ORDER.index(self.idx)
        return [idx - 1]


def rotate_point(p, center, dtheta):
    dx, dy = p[0] - center[0], p[1] - center[1]
    radius = math.sqrt(dx * dx + dy * dy)
    angle = math.asin(dy / radius)
    if dx < 0:
        angle = math.pi - angle
    angle += dtheta
    return center[0] + radius * math.cos(angle), center[1] + radius * math.sin(angle)
