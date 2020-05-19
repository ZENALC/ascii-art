from PIL import Image
from pyperclip import copy
import os
import sys

MAX_HEIGHT = 100
MAX_WIDTH = 300
IMAGE_NAME = 'dog.png'
IMAGE_PATH = os.path.join('Images', IMAGE_NAME)  # image path that you want to open
FOLDER_NAME = 'ASCII Files'  # folder we will save images to
CHOICE = "LUMINOSITY"  # AVERAGE, LIGHTNESS, AND LUMINOSITY are possible choices
WRITE_TO_FILE = True  # setting to write to file
COPY_TO_CLIPBOARD = False  # setting to copy to clipboard
PRINT_TO_SCREEN = False
INVERTED = False  # setting to invert ascii-txt

characters = r"`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
inverseCharacters = characters[::-1]  # same array as above but in reverse
CONSTANT = 3.85  # constant we will use to determine which character to use

if len(sys.argv) > 1:
    IMAGE_PATH = sys.argv[1]
    additionalFlags = sys.argv[2:]

    if '-c' in additionalFlags:
        COPY_TO_CLIPBOARD = True
    if '-i' in additionalFlags:
        INVERTED = True
    if '-p' in additionalFlags:
        PRINT_TO_SCREEN = True


def main():
    baseFile = os.path.basename(IMAGE_PATH)
    name, extension = baseFile.split('.')  # get name and extension of image
    if INVERTED:
        name += '-inverted'  # add inverted
    name += f'-{CHOICE.lower()}'  # add choice name to name
    FILE_NAME = f'{name}.txt'  # file name we will save ascii image as

    image = Image.open(IMAGE_PATH)  # open the image
    if image.mode == 'P':  # if transparent, convert to RGBA
        image = image.convert('RGBA')
    else:
        image = image.convert('RGB')   # force convert to RGB
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT))  # Resizing image
    width, height = image.size  # get width and height of image

    pixels = list(image.getdata())  # get list of RGB values from image
    matrix = [[pixels[width * x + y] for y in range(width)] for x in range(height)]  # get 2D array of RGB values

    if CHOICE == "AVERAGE":
        brightnessMatrix = [[get_average(matrix[x][y]) for y in range(width)] for x in range(height)]
    elif CHOICE == "LIGHTNESS":
        brightnessMatrix = [[get_lightness(matrix[x][y]) for y in range(width)] for x in range(height)]
    else:
        brightnessMatrix = [[get_luminosity(matrix[x][y]) for y in range(width)] for x in range(height)]

    if INVERTED:
        characterMatrix = [[get_characterIndex(brightnessMatrix[x][y], True) for y in range(width)] for x in range(height)]
    else:
        characterMatrix = [[get_characterIndex(brightnessMatrix[x][y], False) for y in range(width)] for x in range(height)]

    totalString = ''

    for row in characterMatrix:
        totalString += "".join(row) + '\n'  # get each row of 2D array and append to string

    if COPY_TO_CLIPBOARD:
        copy(totalString)  # copy ascii-string to clipboard
        print("ASCII image copied to clipboard.")

    if WRITE_TO_FILE:
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

    if PRINT_TO_SCREEN:
        print(totalString)


# helper function to get average of an RGB tuple
def get_average(rgbTuple):
    return sum(rgbTuple) / len(rgbTuple)


# helper function to get lightness of an RGB tuple
def get_lightness(rgbTuple):
    return (max(rgbTuple) - min(rgbTuple)) / 2


# helper function to get luminosity of an RGB tuple
def get_luminosity(rgbTuple):
    return rgbTuple[0] * .21 + rgbTuple[1] * .72 + rgbTuple[2] * .07


def get_characterIndex(brightness, inverse):
    index = round(brightness / CONSTANT)
    if inverse:
        return inverseCharacters[index]
    else:
        return characters[index]


if __name__ == "__main__":
    main()
