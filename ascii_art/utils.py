import os
from PIL import Image
from colorama import init, Fore

RED, GREEN, BLUE, YELLOW, MAGENTA, CYAN = "RED", "GREEN", "BLUE", "YELLOW", "MAGENTA", "CYAN"
AVERAGE, LIGHTNESS, LUMINOSITY = 'AVERAGE', 'LIGHTNESS', 'LUMINOSITY'


# characters that range from least to most visible
characters = r"`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
inverseCharacters = characters[::-1]  # same array as above but in reverse
CONSTANT = 3.85  # constant we will use to determine which character to use


# helper function to parse arguments given through terminal
def parse_args(args):
    imagePath = args[1]
    if not any(x in imagePath for x in ["jpg", "jpeg", "png"]):
        raise ValueError("Please provide an image in a jpg, jpeg, or png format.")

    additionalFlags = args[2:]
    copy, inverted, printScreen, colorPrint, choice = False, False, False, None, AVERAGE

    if '-c' in additionalFlags:
        copy = True
    if '-i' in additionalFlags:
        inverted = True
    if '-p' in additionalFlags:
        printScreen = True
        if '-green' in additionalFlags:
            colorPrint = GREEN
        if '-red' in additionalFlags:
            colorPrint = RED
        if '-yellow' in additionalFlags:
            colorPrint = YELLOW
        if '-blue' in additionalFlags:
            colorPrint = BLUE
        if '-magenta' in additionalFlags:
            colorPrint = MAGENTA
        if '-cyan' in additionalFlags:
            colorPrint = CYAN

    if '-lum' in additionalFlags or '-luminosity' in additionalFlags:
        choice = LUMINOSITY
    if '-avg' in additionalFlags or '-average' in additionalFlags:
        choice = AVERAGE
    if '-light' in additionalFlags or '-lightness' in additionalFlags:
        choice = LIGHTNESS

    return imagePath, copy, inverted, printScreen, colorPrint, choice


# helper function to get average of an RGB tuple
def get_average(rgbTuple):
    return sum(rgbTuple) / len(rgbTuple)


# helper function to get lightness of an RGB tuple
def get_lightness(rgbTuple):
    return (max(rgbTuple) - min(rgbTuple)) / 2


# helper function to get luminosity of an RGB tuple
def get_luminosity(rgbTuple):
    return rgbTuple[0] * .21 + rgbTuple[1] * .72 + rgbTuple[2] * .07


# helper function to get a brightness matrix
def get_brightnessMatrix(matrix, width, height, choice):
    if choice == AVERAGE:  # use average formula to get brightness array
        return [[get_average(matrix[x][y]) for y in range(width)] for x in range(height)]
    elif choice == LIGHTNESS:  # use lightness formula to get brightness array
        return [[get_lightness(matrix[x][y]) for y in range(width)] for x in range(height)]
    else:  # use luminosity formula to get brightness array
        return [[get_luminosity(matrix[x][y]) for y in range(width)] for x in range(height)]


# helper function to get character depending on brightness and inverse values
def get_character(brightness, inverse):
    index = round(brightness / CONSTANT)
    if inverse:
        return inverseCharacters[index]
    else:
        return characters[index]


# helper function to get Image object
def get_image(path, maxWidth, maxHeight):
    image = Image.open(path)  # open the image
    if image.mode == 'P':  # if transparent, convert to RGBA
        image = image.convert('RGBA')
    else:
        image = image.convert('RGB')  # else force convert to RGB

    image.thumbnail((maxWidth, maxHeight))  # Resizing image
    return image


# helper function to get image name and filename
def get_name_and_filename(choice, imagePath, inverted):
    baseFile = os.path.basename(imagePath)  # get base name of the image file
    name, extension = baseFile.split('.')  # get name and extension of image
    if inverted:
        name += '-inverted'  # add inverted to file name
    name += f'-{choice.lower()}'  # add choice name to file name
    fileName = f'{name}.txt'  # file name we will save ascii image as

    return name, fileName


# helper function to write to a txt file
def write_to_file(fileName, imageName, text, folderName):
    os.chdir('../')
    if not os.path.exists(folderName):
        os.mkdir(folderName)

    os.chdir(folderName)

    if os.path.exists(fileName):
        counter = 0
        while os.path.exists(fileName):
            fileName = f'{imageName}{counter}.txt'
            counter += 1

    with open(fileName, 'w') as f:
        f.write(text)
        print(f"ASCII image saved to {os.path.abspath(fileName)}.")
        
        
# helper function to print in color
def color_print(totalString, colorPrint):
    init(convert=True)  # initialize
    if colorPrint is GREEN:
        print(Fore.GREEN + totalString)
    elif colorPrint is RED:
        print(Fore.RED + totalString)
    elif colorPrint is BLUE:
        print(Fore.BLUE + totalString)
    elif colorPrint is YELLOW:
        print(Fore.YELLOW + totalString)
    elif colorPrint is CYAN:
        print(Fore.CYAN + totalString)
    elif colorPrint is MAGENTA:
        print(Fore.MAGENTA + totalString)

