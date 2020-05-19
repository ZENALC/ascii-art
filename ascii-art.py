from PIL import Image
from colorama import Fore, init
from pyperclip import copy
import os
import sys

AVERAGE, LIGHTNESS, LUMINOSITY = 'AVERAGE', 'LIGHTNESS', 'LUMINOSITY'
RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN = "RED", "GREEN", "BLUE", "YELLOW", "MAGENTA", "CYAN"
MAX_HEIGHT = 150  # maximum height image will be resized to
MAX_WIDTH = 150  # maximum width image will be resized to
IMAGE_NAME = 'python.png'  # image name we will convert to ascii
IMAGE_PATH = os.path.join('Images', IMAGE_NAME)  # image path that you want to open
FOLDER_NAME = 'ASCII Files'  # folder we will save images to
CHOICE = AVERAGE  # AVERAGE, LIGHTNESS, AND LUMINOSITY are possible choices
WRITE_TO_FILE = True  # setting to write to file
COPY_TO_CLIPBOARD = False  # setting to copy to clipboard
PRINT_TO_SCREEN = False  # setting to print to screen
INVERTED = False  # setting to invert ascii-txt
COLOR_PRINT = None

# characters that range from least to most visible
characters = r"`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
inverseCharacters = characters[::-1]  # same array as above but in reverse
CONSTANT = 3.85  # constant we will use to determine which character to use

# if run from terminal, accept the arguments
if len(sys.argv) > 1:
    IMAGE_PATH = sys.argv[1]
    additionalFlags = sys.argv[2:]

    if '-c' in additionalFlags:
        COPY_TO_CLIPBOARD = True
    if '-i' in additionalFlags:
        INVERTED = True
    if '-p' in additionalFlags:
        PRINT_TO_SCREEN = True
        if '-green' in additionalFlags:
            COLOR_PRINT = GREEN
        if '-red' in additionalFlags:
            COLOR_PRINT = RED
        if '-yellow' in additionalFlags:
            COLOR_PRINT = YELLOW
        if '-blue' in additionalFlags:
            COLOR_PRINT = BLUE
        if '-magenta' in additionalFlags:
            COLOR_PRINT = MAGENTA
        if '-cyan' in additionalFlags:
            COLOR_PRINT = CYAN

    if '-lum' in additionalFlags:
        CHOICE = LUMINOSITY
    if '-avg' in additionalFlags:
        CHOICE = AVERAGE
    if '-light' in additionalFlags:
        CHOICE = LIGHTNESS


def main():
    baseFile = os.path.basename(IMAGE_PATH)  # get base name of the image file
    name, extension = baseFile.split('.')  # get name and extension of image
    if INVERTED:
        name += '-inverted'  # add inverted to file name
    name += f'-{CHOICE.lower()}'  # add choice name to file name
    FILE_NAME = f'{name}.txt'  # file name we will save ascii image as

    image = Image.open(IMAGE_PATH)  # open the image
    if image.mode == 'P':  # if transparent, convert to RGBA
        image = image.convert('RGBA')
    else:
        image = image.convert('RGB')   # else force convert to RGB
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))  # Resizing image
    width, height = image.size  # get width and height of image

    pixels = list(image.getdata())  # get list of RGB values from image
    matrix = [[pixels[width * x + y] for y in range(width)] for x in range(height)]  # get 2D array of RGB values

    if CHOICE == "AVERAGE":  # use average formula to get brightness array
        brightnessMatrix = [[get_average(matrix[x][y]) for y in range(width)] for x in range(height)]
    elif CHOICE == "LIGHTNESS":  # use lightness formula to get brightness array
        brightnessMatrix = [[get_lightness(matrix[x][y]) for y in range(width)] for x in range(height)]
    else:  # use luminosity formula to get brightness array
        brightnessMatrix = [[get_luminosity(matrix[x][y]) for y in range(width)] for x in range(height)]

    if INVERTED:  # if inverted, get character from the reversed list
        characterMatrix = [[get_character(brightnessMatrix[x][y], True) for y in range(width)] for x in range(height)]
    else:  # if not inverted, get character from the original list
        characterMatrix = [[get_character(brightnessMatrix[x][y], False) for y in range(width)] for x in range(height)]

    totalString = ''

    for row in characterMatrix:
        totalString += "".join(row) + '\n'  # get each row of 2D array and append to string

    if COPY_TO_CLIPBOARD:
        copy(totalString)  # copy ascii-string to clipboard
        print("ASCII image copied to clipboard.")

    if WRITE_TO_FILE:  # write to a file
        if not os.path.exists(FOLDER_NAME):
            os.mkdir(FOLDER_NAME)

        os.chdir(FOLDER_NAME)

        if os.path.exists(FILE_NAME):
            counter = 0
            while os.path.exists(FILE_NAME):
                FILE_NAME = f'{name}{counter}.txt'
                counter += 1

        with open(FILE_NAME, 'w') as f:
            f.write(totalString)
            print(f"ASCII image saved to {os.path.abspath(FILE_NAME)}.")

    if PRINT_TO_SCREEN:  # print to screen
        if not COLOR_PRINT:
            print(totalString)
        else:
            init(convert=True)  # initialize colorama
            if COLOR_PRINT is GREEN:
                print(Fore.GREEN + totalString)
            elif COLOR_PRINT is RED:
                print(Fore.RED + totalString)
            elif COLOR_PRINT is BLUE:
                print(Fore.BLUE + totalString)
            elif COLOR_PRINT is YELLOW:
                print(Fore.YELLOW + totalString)
            elif COLOR_PRINT is CYAN:
                print(Fore.CYAN + totalString)
            elif COLOR_PRINT is MAGENTA:
                print(Fore.MAGENTA + totalString)


# helper function to get average of an RGB tuple
def get_average(rgbTuple):
    return sum(rgbTuple) / len(rgbTuple)


# helper function to get lightness of an RGB tuple
def get_lightness(rgbTuple):
    return (max(rgbTuple) - min(rgbTuple)) / 2


# helper function to get luminosity of an RGB tuple
def get_luminosity(rgbTuple):
    return rgbTuple[0] * .21 + rgbTuple[1] * .72 + rgbTuple[2] * .07


# helper function to get character depending on brightness and inverse values
def get_character(brightness, inverse):
    index = round(brightness / CONSTANT)
    if inverse:
        return inverseCharacters[index]
    else:
        return characters[index]


if __name__ == "__main__":
    main()
