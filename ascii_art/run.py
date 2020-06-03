from ascii_art.ascii_art import ASCIIArt
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert an image to ASCII')
    parser.add_argument('imagePath', type=str, help='path to image file that will be converted')
    parser.add_argument('-i', '--inverted', help='invert the generated ASCII',
                        action="store_true")
    parser.add_argument('-c', '--copy', help='copy the generated ASCII to clipboard',
                        action="store_true")
    parser.add_argument('--choice', help='pick what type of algorithm to use',
                        nargs=1, default="average", choices=('luminosity', 'brightness', 'average'))
    parser.add_argument('-p', '--print', help='print the generated ASCII with specified color if provided',
                        nargs='?', const=1, choices=('red', 'blue', 'yellow', 'green', 'cyan', 'magenta'))
    parser.add_argument('-w', '--write', help='write the generated ASCII to specified file if provided or default file',
                        nargs='?', const=1)
    args = parser.parse_args()

    monkeyText = ASCIIArt(args.imagePath, inverted=args.inverted, choice=args.choice)
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
