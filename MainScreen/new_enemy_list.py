from pygame.locals import *
from Game.LevelReader import *
import data

spawns = []
current = Spawn()

rects = {"Count": Rect(0, 0, 0, 0), "Time": Rect(0, 0, 0, 0),
         "Model": Rect(0, 0, 0, 0), "Flip": Rect(0, 0, 0, 0),
         "Add": Rect(0, 0, 0, 0), "Clear": Rect(0, 0, 0, 0),
         "Save": Rect(0, 0, 0, 0), "Enemies": Rect(0, 0, 0, 0),
         "Current": Rect(0, 0, 0, 0), "Timeline": Rect(0, 0, 0, 0),
         "SlideBar": Rect(0, 0, 0, 0), "Slider": Rect(0, 0, 0, 0)}
selected = "Count"
model_names = {LINEAR: "Linear", PARABOLIC: "Parabolic",
               EXPONENTIAL: "Exponential"}
models = list(model_names.keys())
model_idx = 0
surfaces = {"Enemies": pg.Surface((0, 0))}
slider_ends = [0, 0]
slider_selected = -1
slider_off = 0

show_cursor = True


def reset():
    spawns.clear()
    global current, selected, slider_off, slider_selected, model_idx
    current = Spawn()
    selected = "Count"
    slider_off = model_idx = 0
    slider_selected = -1

    resize()


def resize():
    w = data.screen_w
    fifteenth = w // 15
    # Define rectangles
    rects["Count"] = Rect(data.off_x, data.off_y, w // 4, fifteenth)
    rects["Time"] = rects["Count"].move(0, fifteenth)
    rects["Model"] = rects["Time"].move(0, fifteenth)
    rects["Flip"] = rects["Model"].move(0, fifteenth)
    rects["Current"] = Rect(rects["Count"].right + w // 16, data.off_y + fifteenth // 2, w * 5 // 8, fifteenth * 3)
    rects["Enemies"] = Rect(rects["Current"].x, rects["Flip"].bottom + fifteenth // 2, rects["Current"].w,
                            fifteenth * 5)
    rects["Add"] = Rect(data.off_x, rects["Enemies"].y + fifteenth // 2, rects["Flip"].w, fifteenth)
    rects["Clear"] = rects["Add"].move(0, fifteenth * 3 // 2)
    rects["Save"] = rects["Clear"].move(0, fifteenth * 3 // 2)
    rects["Timeline"] = Rect(data.off_x + fifteenth, w * 2 // 3 + data.off_y, fifteenth * 13,
                             fifteenth * 5)
    # Draw enemy sliders
    lineh = rects["Enemies"].h // 3
    linew = rects["Enemies"].w
    slider_ends[0] = (linew - lineh) // 20 + lineh
    slider_w = (linew - lineh) * 9 // 10
    slider_ends[1] = slider_ends[0] + slider_w
    rects["SlideBar"] = pg.Rect(slider_ends[0], 0, slider_ends[1] - slider_ends[0], lineh)
    rects["Slider"] = pg.Rect(0, 0, (linew - lineh) // 20, lineh * 9 // 10)
    rects["Slider"].centerx = slider_ends[0]
    s_ = pg.Surface((linew, lineh * len(current.chances.keys())))
    # Draw surface
    for i, k in enumerate(current.chances.keys()):
        rects["Slider"].top = i * lineh
        r_ = rects["Slider"].move(int(rects["SlideBar"].w * current.chances[k]), 0)
        # Draw enemy image
        img = data.scale_to_fit(data.enemies[k].img, lineh, lineh)
        img_rect = img.get_rect(center=(lineh // 2, r_.centery))
        s_.blit(img, img_rect)
        # Draw slider
        pg.draw.line(s_, (0, 255, 0), (slider_ends[0], r_.centery), r_.center, 2)
        pg.draw.rect(s_, (128, 128, 128), r_)
    surfaces["Enemies"] = s_
    draw()


def draw():
    d = pg.display.get_surface()
    d.fill((0, 0, 0))
    # Draw current timeline
    r_ = rects["Current"]
    d.blit(current.get_img(*r_.size), r_.topleft)
    # Draw entire timeline
    d.blit(draw_spawn_list(*rects["Timeline"].size, spawns), rects["Timeline"].topleft)
    # Draw text for number of spawns
    text = "Enemies: {}{}".format(current.num_enemies, "|" if selected == "Count" and show_cursor else "")
    color_ = (255, 255, 255) if current.num_enemies >= 1 else (255, 0, 0)
    draw_text(text, rects["Count"], d, text_color=color_)
    # Draw text for duration
    text = "Duration: {}{}ms".format(current.duration, "|" if selected == "Time" and show_cursor else "")
    color_ = (255, 255, 255) if current.duration >= 100 else (255, 0, 0)
    draw_text(text, rects["Time"], d, text_color=color_)
    # Outline either the enemy count or duration
    pg.draw.rect(d, (200, 200, 0), rects[selected], 2)
    # Draw text for model and flip button
    draw_text("Model: " + model_names[current.model], rects["Model"], d, text_color=(0, 0, 0),
              bkgrnd_color=(150, 150, 150))
    draw_text("Flip: " + str(current.flip), rects["Flip"], d, text_color=(0, 0, 0), bkgrnd_color=(150, 150, 150))
    # Draw add, delete, and save buttons
    for string in ["Add", "Clear", "Save"]:
        draw_text(string, rects[string], d)
    d.blit(surfaces["Enemies"], rects["Enemies"].topleft, area=((0, -slider_off), rects["Enemies"].size))


def draw_text(text, rect, surface, text_color=(255, 255, 255), bkgrnd_color=()):
    font = data.get_scaled_font(*rect.size, text)
    text_s = font.render(text, 1, text_color)
    text_rect = text_s.get_rect(center=rect.center)
    if len(bkgrnd_color) == 3:
        surface.fill(bkgrnd_color, rect)
    surface.blit(text_s, text_rect)


# Runs screen to set spawn order
def new_enemy_list():
    global show_cursor
    reset()
    while True:
        # Update whether to show the cursor or not
        temp = show_cursor
        show_cursor = (pg.time.get_ticks() // 400) % 2 == 0
        if temp != show_cursor:
            draw()
        for e in pg.event.get():
            if e.type == QUIT:
                return ""
            elif e.type == VIDEORESIZE:
                data.resize(e.w, e.h, False)
                resize()
            elif e.type == MOUSEBUTTONUP:
                if e.button == BUTTON_LEFT:
                    global slider_selected, current, selected
                    slider_selected = -1
                    # Offset is include in the rectangles
                    pos = pg.mouse.get_pos()
                    if rects["Count"].collidepoint(*pos):
                        selected = "Count"
                    elif rects["Time"].collidepoint(*pos):
                        selected = "Time"
                    elif rects["Model"].collidepoint(*pos):
                        global model_idx
                        model_idx = (model_idx + 1) % len(models)
                        current.model = models[model_idx]
                    elif rects["Flip"].collidepoint(*pos):
                        current.flip = not current.flip
                    elif rects["Add"].collidepoint(*pos):
                        if current.num_enemies >= 1 and current.duration >= 100:
                            spawns.append(current)
                            current = Spawn()
                    elif rects["Clear"].collidepoint(*pos):
                        current = Spawn()
                    elif rects["Save"].collidepoint(*pos):
                        if len(spawns) > 0:
                            byte_data = len(spawns).to_bytes(1, byteorder)
                            for s in spawns:
                                byte_data += s.to_bytes()
                            with open(data.SPAWNS, "ab+") as file:
                                file.write(byte_data)
                            return byte_data
                    else:
                        continue
                    draw()
                elif e.button == BUTTON_WHEELDOWN or e.button == BUTTON_WHEELUP:
                    if rects["Enemies"].collidepoint(*pg.mouse.get_pos()):
                        global slider_off
                        slider_off += rects["SlideBar"].h // 3 * (1 if e.button == BUTTON_WHEELUP else -1)
                        max_off = rects["Enemies"].h - surfaces["Enemies"].get_size()[1]
                        if slider_off < max_off:
                            slider_off = max_off
                        if slider_off > 0:
                            slider_off = 0
                        d = pg.display.get_surface()
                        d.fill((0, 0, 0), rects["Enemies"])
                        d.blit(surfaces["Enemies"], rects["Enemies"].topleft,
                               area=((0, -slider_off), rects["Enemies"].size))
            elif e.type == MOUSEBUTTONDOWN and e.button == BUTTON_LEFT:
                pos = pg.mouse.get_pos()
                if rects["Enemies"].collidepoint(*pos):
                    r = rects["Enemies"]
                    pos = [pos[0] - r.x, pos[1] - r.y - slider_off]
                    # Make sure we are clicking on the slider
                    if slider_ends[0] <= pos[0] <= slider_ends[1]:
                        idx = pos[1] // rects["SlideBar"].h
                        if idx < len(current.chances.keys()):
                            slider_selected = idx
            elif e.type == MOUSEMOTION and slider_selected != -1:
                pos = pg.mouse.get_pos()
                pos = [pos[0] - rects["Enemies"].x, pos[1] - rects["Enemies"].y + slider_off]
                # Get slider fractions
                frac = (pos[0] - slider_ends[0]) / rects["SlideBar"].w
                if frac < 0:
                    frac = 0
                elif frac > 1:
                    frac = 1
                idx = slider_selected
                current.chances[idx] = frac
                # Update slider
                line_h = rects["SlideBar"].h
                surfaces["Enemies"].fill((0, 0, 0), (line_h, idx * line_h, rects["Enemies"].w - line_h, line_h))
                rects["Slider"].top = idx * line_h
                r = rects["Slider"].move(int(rects["SlideBar"].w * frac), 0)
                pg.draw.line(surfaces["Enemies"], (0, 255, 0), (slider_ends[0], r.centery), r.center, 2)
                pg.draw.rect(surfaces["Enemies"], (128, 128, 128), r)
                pg.display.get_surface().blit(surfaces["Enemies"], rects["Enemies"].topleft,
                                              area=((0, -slider_off), rects["Enemies"].size))
            elif e.type == KEYUP:
                if e.key == K_BACKSPACE:
                    if selected == "Count":
                        current.num_enemies = current.num_enemies // 10
                    else:
                        current.duration = current.duration // 10
                elif pg.key.name(e.key).isnumeric():
                    val = int(pg.key.name(e.key))
                    if selected == "Count":
                        current.num_enemies = min(current.num_enemies * 10 + val, 99)
                    else:
                        current.duration = min(current.duration * 10 + val, 100000)
                else:
                    continue
                draw()
        pg.display.flip()
