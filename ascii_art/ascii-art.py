from utils import (write_to_file, color_print, get_brightnessMatrix,
                   get_character, get_image, get_name_and_filename, parse_args)
from pyperclip import copy
import os
import sys

AVERAGE, LIGHTNESS, LUMINOSITY = 'AVERAGE', 'LIGHTNESS', 'LUMINOSITY'
MAX_HEIGHT = 50  # maximum height image will be resized to
MAX_WIDTH = 50  # maximum width image will be resized to
IMAGE_NAME = 'python.png'  # image name we will convert to ascii
IMAGE_PATH = os.path.join('../Images', IMAGE_NAME)  # image path that you want to open
FOLDER_NAME = 'ASCII Files'  # folder we will save images to
CHOICE = AVERAGE  # AVERAGE, LIGHTNESS, AND LUMINOSITY are possible choices
WRITE_TO_FILE = True  # setting to write to file
COPY_TO_CLIPBOARD = False  # setting to copy to clipboard
PRINT_TO_SCREEN = False  # setting to print to screen
INVERTED = False  # setting to invert ascii-txt
COLOR_PRINT = None  # setting to turn colored printing on


# if run from terminal, accept the arguments
if len(sys.argv) > 1:
    IMAGE_PATH, COPY_TO_CLIPBOARD, INVERTED, PRINT_TO_SCREEN, COLOR_PRINT, CHOICE = parse_args(sys.argv)


def main():
    name, FILE_NAME = get_name_and_filename(CHOICE, IMAGE_PATH, INVERTED)
    image = get_image(IMAGE_PATH, maxHeight=MAX_HEIGHT, maxWidth=MAX_WIDTH)
    width, height = image.size  # get width and height of image

    pixels = list(image.getdata())  # get list of RGB values from image
    matrix = [[pixels[width * x + y] for y in range(width)] for x in range(height)]  # get 2D array of RGB values

    brightnessMatrix = get_brightnessMatrix(matrix, width, height, CHOICE)

    if INVERTED:  # if inverted, get character from the reversed list
        characterMatrix = [[get_character(brightnessMatrix[x][y], True) for y in range(width)] for x in range(height)]
    else:  # if not inverted, get character from the original list
        characterMatrix = [[get_character(brightnessMatrix[x][y], False) for y in range(width)] for x in range(height)]

    totalString = ''

    for row in characterMatrix:
        totalString += "".join(row) + '\n'  # get each row of 2D array and append to string

    if PRINT_TO_SCREEN:  # print to screen
        if not COLOR_PRINT:
            print(totalString)
        else:
            color_print(totalString, COLOR_PRINT)

    if COPY_TO_CLIPBOARD:
        copy(totalString)  # copy ascii-string to clipboard
        print("ASCII image copied to clipboard.")

    if WRITE_TO_FILE:
        write_to_file(FILE_NAME, name, totalString, FOLDER_NAME)  # write to a file


if __name__ == "__main__":
    main()
