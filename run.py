from ascii_art import ASCIIArt
import argparse


def main():
    parser = argparse.ArgumentParser(description='Convert an image to ASCII')
    parser.add_argument('imagePath', type=str, help='path to image file that will be converted.')
    parser.add_argument('-c', '--copy', help='copy the generated ASCII to clipboard',
                        action="store_true")
    parser.add_argument('-p', '--print', help='print the generated ASCII with specified color',
                        action="store_true", nargs='?')
    parser.add_argument('-w', '--write', help='write the generated ASCII to specified file',
                        action="store_true", nargs='?')
    args = parser.parse_args()

    monkeyText = ASCIIArt(args.imagePath)
    if args.copy:
        monkeyText.copy_to_clipboard()
    if args.print:
        monkeyText.print()
    # monkeyText.print()


if __name__ == '__main__':
    main()
