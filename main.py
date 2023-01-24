import math
from typing import Callable
import random
import tkinter as tk
import sys
import glob

width, height, step = [int(i) for i in sys.argv[1:]]
max_hex = 16581375


def number_to_hex(n: int):
    n = hex(n % max_hex)[2:]
    n = "0" * (6 - len(n)) + n
    return "#" + n


def progress_bar(percent, step):
    return "▒" * int(percent // step) + "░" * int(100 // step - percent // step)


root = tk.Tk()
canvas = tk.Canvas(root, width=width, height=height, bg="black")

img = tk.PhotoImage(width=width, height=height)
canvas.create_image((width//2, height//2), image=img, state="normal")

canvas.pack()


def pure_random(*args):
    return number_to_hex(random.randint(0, 255 ** 3))


def plot_multiplied(x, y):
    return number_to_hex(x * y)


def plot_power(x, y):
    return number_to_hex(x ** y)


def thing(x, y):
    return number_to_hex(int((math.cos(x) + math.sin(y)) * max_hex))


def zoom(x, y, z, f: Callable, *args):
    return f(x/z, y/z, *args)


def move_cam(x, y, x_m, y_m, f: Callable, *args):
    return f(x + x_m, y + y_m, *args)


def quadratic(x, y, a, b, c):
    return number_to_hex(a * (x ** 2) + b * x + c)


def plot(f: Callable, *args):
    for x in range(width):
        for y in range(height):
            img.put(f(x, y, *args), (x, y))
            print(f"{progress_bar((x*height + y) / width / height * 100, step)} {str(int((x*height + y) / width / height * 100))}%", end="\r")
    print("▓" * (100 // step) + " 100%")


plot(zoom, 100, thing)

img.write(f"{len(glob.glob('*render.png'))}render.png", format='png')

root.mainloop()

if __name__ == "__main__":
    pass
