from colorama import init, Fore
from PIL import Image
import pyperclip
import os


class ASCIIArt:
    CONSTANT = 3.85  # constant we will use to determine which character to use
    characters = r"`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    inverseCharacters = characters[::-1]  # same array as above but in reverse

    def __init__(self, imagePath, choice='AVERAGE', inverted=False, dimension=(50, 50)):
        self.imagePath = imagePath
        self.choice = choice.upper()
        self.inverted = inverted
        self.dimension = dimension
        self.imageFile = os.path.basename(imagePath)
        self.image = self.get_image(imagePath, dimension)
        self.width, self.height = self.image.size
        self.matrix = self.get_image_matrix()
        self.renderedText = self.renderText()

    def get_image_matrix(self):
        """Helper function to get 2D array of RGB values"""
        imagePixels = self.get_image_pixels()
        return [[imagePixels[self.width * x + y] for y in range(self.width)] for x in range(self.height)]

    def get_image_pixels(self):
        """Helper function to get RGB tuples from an Image object"""
        return list(self.image.getdata())

    def get_character(self, brightness):
        """Helper function to get character depending on inverse values"""
        index = round(brightness / self.CONSTANT)
        if self.inverted:
            return self.inverseCharacters[index]
        else:
            return self.characters[index]

    def get_brightness_matrix(self):
        """Helper function to return brightness matrix of image"""
        if self.choice == 'AVERAGE':  # Use average formula to get brightness array
            return [[self.get_average(self.matrix[x][y]) for y in range(self.width)] for x in range(self.height)]
        elif self.choice == 'LIGHTNESS':  # Use lightness formula to get brightness array
            return [[self.get_lightness(self.matrix[x][y]) for y in range(self.width)] for x in range(self.height)]
        elif self.choice == 'LUMINOSITY':  # Use luminosity formula to get brightness array
            return [[self.get_luminosity(self.matrix[x][y]) for y in range(self.width)] for x in range(self.height)]
        else:
            raise ValueError("Invalid algorithm choice. Possible values are average, lightness, and luminosity.")

    def get_character_matrix(self):
        """Helper function to get character matrix depending on brightness and inverse values"""
        brightnessMatrix = self.get_brightness_matrix()
        if self.inverted:  # if inverted, get character from the reversed list
            return [[self.get_character(brightnessMatrix[x][y]) for y in range(self.width)] for x in range(self.height)]
        else:  # if not inverted, get character from the original list
            return [[self.get_character(brightnessMatrix[x][y]) for y in range(self.width)] for x in range(self.height)]

    def renderText(self):
        """Main function to return ASCII format of image"""
        characterMatrix = self.get_character_matrix()
        renderedText = ''
        for row in characterMatrix:
            renderedText += "".join(row) + '\n'

        return renderedText

    def copy_to_clipboard(self):
        """Helper function to copy to clipboard"""
        pyperclip.copy(self.renderedText)
        print("ASCII image copied to clipboard.")

    def print(self, color=None):
        """Helper function to print rendered text"""
        if color:
            init(convert=True)  # initialize colorama module
            color = color.upper()
            if color == "GREEN":
                print(Fore.GREEN + self.renderedText)
            elif color == "RED":
                print(Fore.RED + self.renderedText)
            elif color == "BLUE":
                print(Fore.BLUE + self.renderedText)
            elif color == "YELLOW":
                print(Fore.YELLOW + self.renderedText)
            elif color == "CYAN":
                print(Fore.CYAN + self.renderedText)
            elif color == "MAGENTA":
                print(Fore.MAGENTA + self.renderedText)
            else:
                print("Invalid color. Supported colors are green, red, blue, yellow, cyan, and magenta.")
        else:
            print(self.renderedText)

    def write_to_file(self, fileName=None):
        """Helper function to write to a txt file"""
        if not fileName:
            fileName = self.imageFile
        outputName, _ = os.path.splitext(fileName)
        outputFile = outputName + '.txt'
        folderName = 'ASCII Files'
        if not os.path.exists(folderName):
            os.mkdir(folderName)

        previousPath = os.getcwd()
        os.chdir(folderName)

        if os.path.exists(outputFile):
            counter = 0
            while os.path.exists(outputFile):
                outputFile = f'{outputName}{counter}.txt'
                counter += 1

        with open(outputFile, 'w') as f:
            f.write(self.renderedText)
            print(f"ASCII image saved to {os.path.abspath(outputFile)}.")

        os.chdir(previousPath)

    def __repr__(self):
        return f'ASCIIArt{self.imagePath, self.choice, self.inverted, self.dimension}'

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def get_image(path, dimension):
        """Helper function to retrieve an Image object"""
        with Image.open(path) as image:
            if image.mode == 'P':  # If transparent, convert to RGBA
                image = image.convert('RGBA')
            else:  # Else force convert to RGB
                image = image.convert('RGB')
            image.thumbnail(dimension)  # Resizing image
            return image

    @staticmethod
    def get_average(rgbTuple):
        """Helper function to get average value of an RGB tuple"""
        return sum(rgbTuple) / len(rgbTuple)

    @staticmethod
    def get_luminosity(rgbTuple):
        """Helper function to get luminosity value of an RGB tuple"""
        return rgbTuple[0] * .21 + rgbTuple[1] * .72 + rgbTuple[2] * .07

    @staticmethod
    def get_lightness(rgbTuple):
        """Helper function to get lightness of an RGB tuple"""
        return (max(rgbTuple) - min(rgbTuple)) / 2
