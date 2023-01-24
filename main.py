import math
from typing import Callable
import random
import tkinter as tk
import sys
import glob

width, height, step = [int(i) for i in sys.argv[1:]]
max_hex = 16581375


def number_to_hex(n):
    n = hex(int(n)% max_hex)[2:]
    n = "0" * (6 - len(n)) + n
    return "#" + n


def progress_bar(percent):
    return "▒" * int(percent // step) + "░" * int(100 // step - percent // step)


root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, bg="black")

img = tk.PhotoImage(width=width, height=height)
canvas.create_image((width//2, height//2), image=img, state="normal")

canvas.pack()


def pure_random(*args):
    return random.randint(0, 255 ** 3)


def plot_multiplied(x, y):
    try:
        return max_hex/(x * y)
    except ZeroDivisionError:
        return max_hex


def plot_power(x, y):
    return x ** y


def thing(x, y):
    return (math.cos(x) + math.sin(y)) * max_hex


def zoom(x, y, z, f: Callable, *args, **kwargs):
    return f(x/z, y/z, *args, **kwargs)


def move_cam(x, y, x_m, y_m, f: Callable, *args, **kwargs):
    return f(x + x_m, y + y_m, *args, **kwargs)


def quadratic(x, y, a, b, c):
    return a * (x ** 2) + b * x + c


def plot_normalised_thing(x, y):
    return max_hex - max_hex / (math.cos(x) + math.sin(y))


def centre(x, y, f: Callable, *args, **kwargs):
    return f(x - width//2, y - height//2, *args, **kwargs)


def centre_x(x, y, f: Callable, *args, **kwargs):
    return f(x - width//2, y, *args, **kwargs)


def centre_y(x, y, f: Callable, *args, **kwargs):
    return f(x, y - height//2, *args, **kwargs)


def double_square(x, y):
    return max_hex / (x ** 2 + y ** 2)


def join(x, y, f: Callable, g: Callable, **kwargs):
    return f(x, y, *kwargs["f_args"]) + g(x, y, *kwargs["g_args"])


def magnify(x, y, f: Callable, z, *args, **kwargs):
    return f(x, y, *args, **kwargs) * z


def plot(f: Callable, *args, **kwargs):
    for x in range(width):
        for y in range(height):
            try:
                img.put(number_to_hex(f(x, y, *args, **kwargs)), (x, y))
            except ZeroDivisionError:
                img.put(number_to_hex(max_hex), (x, y))
            prog = (x*height + y) / width / height * 100
            print(f"{progress_bar(prog)} {str(int(prog))}%", end="\r")
    print("▓" * (100 // step) + " 100%")


plot(centre, zoom, 100, join, magnify, magnify, f_args=[double_square, 10], g_args=[quadratic, 4, 1, 2, 1])

img.write(f"{len(glob.glob('*render.png'))}render.png", format='png')

root.mainloop()

if __name__ == "__main__":
    pass
