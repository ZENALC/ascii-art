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



        
        


