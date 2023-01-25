import math
from typing import Callable
import random
import tkinter as tk
import sys
import os

width, height, step = [float(i) for i in sys.argv[1:4]]
width, height = int(width), int(height)
max_hex = 256**3


def number_to_hex(n):
    n = hex(int(n)% max_hex)[2:]
    n = "0" * (6 - len(n)) + n
    return "#" + n


def progress_bar(percent):
    return "▒" * int(percent // step) + "░" * int(100 // step - percent // step)


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


def quadratic_y(x, y, a, b, c):
    return a * (y ** 2) + b * y + c


def plot_normalised_thing(x, y):
    return max_hex - max_hex / (math.cos(x) + math.sin(y))


def centre(x, y, f: Callable, *args, **kwargs):
    return f(x - width//2, y - height//2, *args, **kwargs)


def centre_x(x, y, f: Callable, *args, **kwargs):
    return f(x - width//2, y, *args, **kwargs)


def centre_y(x, y, f: Callable, *args, **kwargs):
    return f(x, y - height//2, *args, **kwargs)


def quadratic_s(x, y, a, b, c):
    return a * (x ** 2) + b * x + c + y


def quadratic_p(*args):
    return (quadratic_s(*args) == 0) * (max_hex - 1)


def flip_y(x, y, f: Callable, *args, **kwargs):
    return f(x, -y, *args, **kwargs)


def double_square(x, y):
    return max_hex / (x ** 2 + y ** 2)


def join(x, y, f: Callable, g: Callable, **kwargs):
    return f(x, y, *kwargs["f_args"]) + g(x, y, *kwargs["g_args"])


def multiply(x, y, f: Callable, z, *args, **kwargs):
    return f(x, y, *args, **kwargs) * z


def normalise_y(x, y, f: Callable, *args, **kwargs):
    pass


def sine(x, y, g):
    if math.sin(x) - y in range(-g, g):
        return max_hex - 1
    else:
        return 0


def grayscale(x, y, f: Callable, *args, **kwargs):
    a = number_to_hex(f(x, y, *args, **kwargs))
    r, g, b = a[1:3], a[3:5], a[5:7]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)
    return int(hex(min(255, (r+g+b)//3 + 1))[2:] * 3, 16)


def circle(x, y, r, w):
    if x**2 + y**2 in range(r**2 - w, r**2 + w):
        return max_hex - 1
    else:
        return 0


def plot(f: Callable, *args, **kwargs):
    for x in range(width):
        for y in range(height):
            try:
                img.put(number_to_hex(f(x, y, *args, **kwargs)), (x, y))
            except ZeroDivisionError:
                img.put(number_to_hex(max_hex - 1), (x, y))
            prog = (x*height + y) / width / height * 100
            print(f"{progress_bar(prog)} {str(int(prog))}%", end="\r")
    print("▓" * int(100 // step) + " 100%")


def unpack_args(iterable):
    name = ""
    if isinstance(iterable, str):
        return iterable
    if isinstance(iterable, list):
        name += "["
    for arg in iterable:
        match arg:
            case list():
                name += "["
                name += unpack_args(arg)
                name += "]"
            case dict():
                name += "{"
                for k, v in arg.items():
                    name += f"{unpack_args(k)} : {unpack_args(v)}"
                name += "}"
            case _:
                if callable(arg):
                    name += arg.__name__
                else:
                    name += repr(arg)
        name += ", "
    if isinstance(iterable, list):
        name += "]"

    name += f" {width}px x {height}px"
    return name


def log_plot(*args, **kwargs):
    global img
    t_args = args
    args = list(args)
    args.append(kwargs)
    name = unpack_args(args)
    path = f"{os.path.dirname(os.path.abspath(__file__))}\\{name}.png"
    if os.path.isfile(path):
        img = tk.PhotoImage(file=path)
        canvas.create_image((width // 2, height // 2), image=img, state="normal")
        canvas.pack()
    else:
        plot(*t_args, **kwargs)
        img.write(f"{name}.png", format='png')


if __name__ == "__main__":
    root = tk.Tk()
    canvas = tk.Canvas(root, width=width, height=height, bg="black")

    img = tk.PhotoImage(width=width, height=height)
    canvas.create_image((width // 2, height // 2), image=img, state="normal")
    canvas.pack()

    exec(f"log_plot({','.join(sys.argv[4:])})")

    root.mainloop()
