from simpleimage import SimpleImage
from karel.stanfordkarel import *
import math
import time

IMAGE_PATH = "images/"
DEFAULT_FILE = "kayaking_doggo.JPG"
CANVAS_SIZE = 40
COLOR_CHART = {
    "BLACK": (0, 0, 0),
    "BLUE": (0, 0, 255),
    "CYAN": (0, 255, 255),
    "DARK_GRAY": (77, 77, 77),
    "GRAY": (140, 140, 140),
    "GREEN": (0, 255, 0),
    "LIGHT_GRAY": (204, 204, 204),
    "MAGENTA": (205, 0, 205),
    "ORANGE": 	(255, 165, 0),
    "PINK": (255, 192, 203),
    "RED": (255, 0, 0),
    "WHITE": (255, 250, 250),
    "YELLOW": (255, 255, 0),
}


def rgb_to_lab(rgb):
    return xyz_to_lab(*rgb_to_xyz(rgb))


def rgb_to_xyz(rgb):
    values = []
    for value in rgb:
        value = value / 255
        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value /= 12.92
        value *= 100
        values.append(value)
    x = values[0] * 0.4124 + values[1] * 0.3576 + values[2] * 0.1805
    y = values[0] * 0.2126 + values[1] * 0.7152 + values[2] * 0.0722
    z = values[0] * 0.0193 + values[1] * 0.1192 + values[2] * 0.9505
    return (x, y, z)


def xyz_to_lab(x, y, z):
    x = x / 95.047         # ref_x =  95.047
    y = y / 100.000        # ref_y = 100.000
    z = z / 108.883        # ref_z = 108.883

    if (x > 0.008856):
        x = x ** (1.0 / 3.0)
    else:
        x = (7.787 * x) + (16.0 / 116.0)
    if (y > 0.008856):
        y = y ** (1.0 / 3.0)
    else:
        y = (7.787 * y) + (16.0 / 116.0)
    if (z > 0.008856):
        z = z ** (1.0 / 3.0)
    else:
        z = (7.787 * z) + (16.0 / 116.0)

    CIE_L = (116.0 * y) - 16.0
    CIE_a = 500.0 * (x - y)
    CIE_b = 200.0 * (y - z)
    return (CIE_L, CIE_a, CIE_b)


LAB = {color: rgb_to_lab(rgb) for color, rgb in COLOR_CHART.items()}


def main():
    image = SimpleImage(get_file())
    cropped_image = crop_image(image)
    colors = get_colors(cropped_image)
    draw_on_cavas(colors)
    time.sleep(5)
    image.show()


def get_file():
    file_name = input("Enter file name or press enter to use default image: ")
    if not file_name:
        file_name = DEFAULT_FILE
    return IMAGE_PATH + file_name


def crop_image(image):
    """
    make the image square
    """
    width = image.width
    height = image.height
    size = min(width, height)
    new_image = SimpleImage.blank(size, size)
    for y in range(size):
        for x in range(size):
            px = image.get_pixel(x+(width-size)//2,
                                 y+(height-size)//2)
            new_image.set_pixel(x, y, px)
    return new_image


def get_colors(img):
    skip_size = math.ceil(img.height/CANVAS_SIZE)
    colors = [[] for i in range(CANVAS_SIZE)]
    for y in range(0, img.height, skip_size):
        for x in range(0, img.width, skip_size):
            color = convert(img.get_pixel(x, y))
            colors[y//skip_size].append(color)
    return colors


def convert(px):
    min_distance = 765
    closest_color = ""
    lab = rgb_to_lab((px.red, px.green, px.blue))
    for color, (L, a, b) in LAB.items():
        distance = math.sqrt(
            (lab[0] - L)**2 + (lab[1] - a)**2 + (lab[2] - b) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color


def draw_on_cavas(colors):
    for i, row in enumerate(colors):
        for j, cell_color in enumerate(row):
            paint(cell_color)
            if j == len(colors) - 1:
                continue
            move()
        if i == len(colors) - 1:
            break
        move_to_next_row()


def paint(color):
    if color == "BLACK":
        paint_corner(BLACK)
    elif color == "BLUE":
        paint_corner(BLUE)
    elif color == "CYAN":
        paint_corner(CYAN)
    elif color == "DARK_GRAY":
        paint_corner(DARK_GRAY)
    elif color == "GRAY":
        paint_corner(GRAY)
    elif color == "GREEN":
        paint_corner(GREEN)
    elif color == "LIGHT_GRAY":
        paint_corner(LIGHT_GRAY)
    elif color == "MAGENTA":
        paint_corner(MAGENTA)
    elif color == "ORANGE":
        paint_corner(ORANGE)
    elif color == "PINK":
        paint_corner(PINK)
    elif color == "RED":
        paint_corner(RED)
    elif color == "WHITE":
        paint_corner(WHITE)
    elif color == "YELLOW":
        paint_corner(YELLOW)


# Karel's move

def move_to_next_row():
    """
    pre-condition: Karel is next to the right wall facing East.
    post_condition: Kare is at one row below and next to the left wall facing East.
    """
    turn_around()
    move_to_wall()
    turn_left()
    move()
    turn_left()


def turn_around():
    turn_left()
    turn_left()


def move_to_wall():
    while front_is_clear():
        move()


# main()
if __name__ == "__main__":
    run_karel_program('canvas.w')
