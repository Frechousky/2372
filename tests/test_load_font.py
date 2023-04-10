import pygame
import pytest

from graphics import load_font
from settings import BLANKA_FONT


@pytest.fixture
def init_pygamefont():
    pygame.font.init()
    yield
    pygame.font.quit()


def test_load_existing_font(init_pygamefont):
    f = load_font(BLANKA_FONT, 30)
    assert f is not None, 'font is not None'
    assert isinstance(
        f, pygame.font.Font), 'font is pygame.font.Font'


def test_load_non_existing_font(init_pygamefont):
    with pytest.raises(FileNotFoundError):
        load_font('thisisnotafont.otf', 30)
