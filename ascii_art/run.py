from ascii_art import ASCIIArt
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert an image to ASCII')
    parser.add_argument('imagePath', type=str, help='path to image file that will be converted')
    parser.add_argument('--inverted', help='invert the generated ASCII',
                        action="store_true")
    parser.add_argument('--copy', help='copy the generated ASCII to clipboard',
                        action="store_true")
    parser.add_argument('--choice', help='pick what type of algorithm to use',
                        nargs=1, default=["average"], choices=('luminosity', 'lightness', 'average'))
    parser.add_argument('--height', help='specify height for generated ascii text',
                        nargs=1, default=[50], type=int)
    parser.add_argument('--width', help='specify width for generated ascii text',
                        nargs=1, default=[50], type=int)
    parser.add_argument('--print', help='print the generated ASCII with specified color if provided',
                        nargs='?', const=1, choices=('red', 'blue', 'yellow', 'green', 'cyan', 'magenta'))
    parser.add_argument('--write', help='write the generated ASCII to specified filename if provided',
                        nargs='?', const=1)
    args = parser.parse_args()

    dimension = (args.width[0], args.height[0])
    monkeyText = ASCIIArt(args.imagePath, inverted=args.inverted, choice=args.choice[0], dimension=dimension)
    if args.copy:
        monkeyText.copy_to_clipboard()
    if args.print:
        if args.print != 1:
            monkeyText.print(args.print)
        else:
            monkeyText.print()
    if args.write:
        if args.write != 1:
            monkeyText.write_to_file(args.write)
        else:
            monkeyText.write_to_file()


if __name__ == '__main__':
    main()
