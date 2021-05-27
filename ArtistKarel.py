from simpleimage import SimpleImage
from karel.stanfordkarel import *
import math

IMAGE_PATH = "images/"
DEFAULT_FILE = "baby_koi.JPG"
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


def main():
    image = SimpleImage(get_file())
    image = crop_image(image)
    image.show()
    colors = get_colors(image)
    draw_on_cavas(colors)


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
            px = image.get_pixel(x+round((width-size)/2),
                                 y+round((height-size)/2))
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


def test():
    img = SimpleImage(DEFAULT_FILE)
    px = img.get_pixel(450, 300)
    color = convert(px)
    print(color)


def convert(px):
    min_distance = float("inf")
    closest_color = ""
    for color, values in COLOR_CHART.items():
        # distance = math.sqrt((values[0]-px.red)**2 +
        #                      (values[1]-px.green)**2+(values[2]-px.blue)**2)
        distance = abs(
            values[0]-px.red)+abs(values[1]-px.green)+abs(values[2]-px.blue)
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
