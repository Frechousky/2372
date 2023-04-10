import pygame
import pytest

from graphics import load_sound
from settings import CLICK_SOUND


@pytest.fixture
def init_pygamemixer():
    pygame.mixer.init()
    yield
    pygame.mixer.quit()


def test_load_existing_sound(init_pygamemixer):
    f = load_sound(CLICK_SOUND)
    assert f is not None, 'font is not None'
    assert isinstance(
        f, pygame.mixer.Sound), 'font is pygame.mixer.Sound'


def test_load_non_existing_sound(init_pygamemixer):
    with pytest.raises(FileNotFoundError):
        load_sound('thisisnotasound.wav')
