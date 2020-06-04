import pytest
import os


@pytest.fixture
def asciiObject():
    from ascii_art import ASCIIArt as Art
    return Art('Images/python.png')


def test_matrix(asciiObject):
    assert asciiObject.get_image_matrix() is not None
    assert asciiObject.matrix[0][0] is not None


def test_image_pixels(asciiObject):
    assert asciiObject.get_image_pixels() is not None
    assert asciiObject.get_image_pixels()[0] is not None


def test_get_brightness(asciiObject):
    asciiObject.inverted = True
    assert asciiObject.get_character(0) == '$'

    asciiObject.inverted = False
    assert asciiObject.get_character(0) == '`'


def test_get_average(asciiObject):
    rgbTuple = (1, 2, 3)
    assert asciiObject.get_average(rgbTuple) == 2


def test_get_lightness(asciiObject):
    rgbTuple = (1, 2, 3)
    assert asciiObject.get_lightness(rgbTuple) == 1


def test_get_luminosity(asciiObject):
    rgbTuple = (1, 2, 3)
    assert round(asciiObject.get_luminosity(rgbTuple), 2) == 1.86


def test_renderText(asciiObject):
    os.chdir(os.path.join('ascii_art', 'Text Files'))
    with open('python.txt', 'r') as f:
        assert asciiObject.renderText() == f.read()

    with open('pythonInverted.txt', 'r') as f:
        asciiObject.inverted = True
        assert asciiObject.renderText() == f.read()