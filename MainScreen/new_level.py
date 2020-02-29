from pygame.locals import *
from Game.level_objects import *
import data

paths = []
selected = "Start"
current = Start()
last_paths = []
types = ["Start", "Line", "Circle", "Undo", "Save & Exit"]
rect = pg.Rect(0, 0, 0, 0)

# Width of side bar and height of each option text box
side_w = item_h = 0


def reset():
    paths.clear()
    last_paths.clear()
    global selected, current
    selected, current = "Start", Start()


def draw():
    global rect, side_w
    pg.display.get_surface().fill((0, 0, 0))
    side_w = data.screen_w // 5
    rect = pg.Rect(side_w + data.off_x, side_w // 2 + data.off_y, data.screen_w - side_w, data.screen_w - side_w)
    draw_level()
    draw_options()


def draw_level():
    pg.display.get_surface().fill((0, 200, 0), rect)
    pg.display.get_surface().blit(draw_paths(rect.w, paths + [current]), rect)


def draw_options():
    global item_h
    d = pg.display.get_surface()
    item_h = data.screen_w // len(types)
    font = data.get_scaled_font(side_w, item_h, data.get_widest_string(types))
    d.fill((128, 128, 128), (data.off_x, data.off_y, side_w, data.screen_w))
    for i, t_ in enumerate(types):
        text = font.render(t_, 1, (0, 0, 0))
        text_rect = text.get_rect(center=(side_w // 2 + data.off_x, int(item_h * (i + .5)) + data.off_y))
        d.blit(text, text_rect)
        if t_ == selected:
            pg.draw.rect(d, (175, 175, 0), (data.off_x, i * item_h + data.off_y, side_w, item_h), 5)


# Runs level creator
def new_level():
    reset()
    draw()

    mode = 0
    while True:
        for e in pg.event.get():
            if e.type == QUIT:
                return ""
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, False)
                draw()
            elif e.type == MOUSEBUTTONUP and e.button == BUTTON_LEFT:
                global selected, paths, last_paths, current
                pos = pg.mouse.get_pos()
                if rect.collidepoint(*pos):
                    temp = paths.copy()
                    pos = [(pos[0] - rect.x) / rect.w, (pos[1] - rect.y) / rect.h]
                    if current.idx == START:
                        current.pos = pos
                        paths = [current]
                        current = Start()
                    elif current.idx == LINE:
                        paths.append(current)
                        current = Line(start=paths[-1].get_end())
                    elif current.idx == CIRCLE:
                        if mode == 0:
                            mode = 1
                        else:
                            paths.append(current)
                            current = Circle()
                            mode = 0
                    # If we added a path, update saves
                    if temp != paths:
                        last_paths = temp
                elif pos[0] - data.off_x < side_w:
                    idx = (pos[1] - data.off_y) * len(types) // data.screen_w
                    # Clicked save, make sure we have at least one non-start path
                    if idx == len(types) - 1 and len(paths) >= 2:
                        byte_data = len(paths).to_bytes(1, byteorder)
                        for p in paths:
                            byte_data += p.to_bytes()
                        with open(data.LEVELS, "ab+") as file:
                            file.write(byte_data)
                        return byte_data
                    # Clicked undo
                    elif idx == len(types) - 2 and len(paths) >= 1:
                        paths = last_paths
                        last_paths = last_paths[:-1]
                        # Change the index so that it recreates the current path object
                        if len(paths) == 0:
                            current = Start()
                        else:
                            if selected == "Start":
                                current = Start()
                            elif selected == "Line":
                                current = Line(start=paths[-1].get_end())
                            elif selected == "Circle":
                                current = Circle()
                            mode = 0
                        draw_level()
                    elif selected != types[idx] and len(paths) > 0:
                        selected = types[idx]
                        draw_options()
                        if selected == "Start":
                            current = Start()
                        elif selected == "Line":
                            current = Line(start=paths[-1].get_end())
                        elif selected == "Circle":
                            current = Circle()
                        mode = 0
            elif e.type == MOUSEMOTION:
                pos = pg.mouse.get_pos()
                pos = [(pos[0] - rect.x) / rect.w, (pos[1] - rect.y) / rect.h]
                pos_ = [min(max(i, 0.), 1.) for i in pos]
                if current.idx == START:
                    current.pos = pos_
                    for i in range(2):
                        if abs(.5 - current.pos[i]) < .025:
                            current.pos[i] = .5
                elif current.idx == LINE:
                    current.end = pos_
                    dx, dy = current.end[0] - current.start[0], current.end[1] - current.start[1]
                    if abs(dx) < .025:
                        current.end[0] = current.start[0]
                    if abs(dy) < .025:
                        current.end[1] = current.start[1]
                    if abs(abs(dx) - abs(dy)) < .025:
                        r = math.sqrt(dx * dx + dy * dy)
                        delta = r * math.sqrt(2) / 2
                        current.end[0] = current.start[0] + math.copysign(delta, dx)
                        current.end[1] = current.start[1] + math.copysign(delta, dy)
                elif current.idx == CIRCLE:
                    if mode == 0:
                        # Get end of last segment
                        end = paths[-1].get_end()
                        for i in range(2):
                            if abs(end[i] - pos[i]) < .025:
                                pos[i] = end[i]
                        r = data.get_distance(end, pos)
                        # Set initial circle angle
                        current.theta_i = data.get_angle_pixels(pos, end)
                        current.theta_f = current.theta_i + data.TWO_PI
                        if pos[0] - r >= 0 and pos[0] + r <= 1 and pos[1] - r >= 0 and pos[1] + r <= 1:
                            current.center = pos
                            current.radius = r
                        else:
                            trig = [math.cos(current.theta_i), -math.sin(current.theta_i)]
                            diameter = 1
                            for i in range(2):
                                # Distance to negative edge
                                d = end[i]
                                # Number of diameters from starting point to negative edge
                                v = .5 + trig[i] / 2
                                if v > 0 and d / v < diameter:
                                    diameter = d / v
                                # Same for positive edge
                                d = 1 - d
                                v = 1 - v
                                if v > 0 and d / v < diameter:
                                    diameter = d / v
                            radius = diameter / 2
                            # Set center position and radius
                            current.center = [end[i] - radius * trig[i] for i in range(2)]
                            current.radius = radius
                    else:
                        # Calculate change in angle
                        dtheta = data.get_angle_pixels(current.center, pos) - (current.theta_f % data.TWO_PI)
                        # Make sure we are going in the correct direction
                        if dtheta > math.pi:
                            dtheta -= data.TWO_PI
                        elif dtheta < -math.pi:
                            dtheta += data.TWO_PI
                        current.theta_f += dtheta
                        diff = current.theta_f - current.theta_i
                        ten_pi = data.TWO_PI * 5
                        if diff > ten_pi:
                            current.theta_f = ten_pi + current.theta_i
                        elif diff < -ten_pi:
                            current.theta_f = -ten_pi + current.theta_i
                        half_pi, quarter_pi = math.pi / 2, math.pi / 4
                        factor = (diff + quarter_pi) // half_pi
                        if abs(diff - half_pi * factor) < half_pi / 10:
                            current.theta_f = factor * half_pi + current.theta_i
                draw_level()
        pg.display.flip()
