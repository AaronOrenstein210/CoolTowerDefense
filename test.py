from data import get_scaled_font, get_scaled_font_log
import pygame as pg
import time

pg.init()


def time_func(w, h, string):
    print("Normal Method: ", end="")
    start = time.time()
    get_scaled_font(w, h, string)
    print(time.time() - start)
    print("Log Method: ", end="")
    start = time.time()
    get_scaled_font_log(w, h, string)
    print(time.time() - start)


dims = [(100, 100), (200, 50), (50, 200), (10, 10), (1000, 1000)]
strings = ["Helow World", "Short", "Looooonnnnngggg"]

for string in strings:
    for dim in dims:
        print("\nFit {} into {}X{}".format(string, *dim))
        for i in range(3):
            time_func(*dim, string)
