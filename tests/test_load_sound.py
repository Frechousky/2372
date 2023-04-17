import pygame
import pytest

from graphics import load_sound
from settings import CLICK_SOUND


@pytest.fixture
def init_pygamemixer():
    pygame.mixer.init()
    yield
    pygame.mixer.quit()


@pytest.skip(reason="pygame.mixer.init fails on github action", allow_module_level=True)
def test_load_existing_sound(init_pygamemixer):
    s = load_sound(CLICK_SOUND)

    assert s is not None, "sound is not None"
    assert isinstance(s, pygame.mixer.Sound), "sound is pygame.mixer.Sound"


@pytest.skip(reason="pygame.mixer.init fails on github action", allow_module_level=True)
def test_load_non_existing_sound(init_pygamemixer):
    with pytest.raises(FileNotFoundError):
        load_sound("thisisnotasound.wav")
