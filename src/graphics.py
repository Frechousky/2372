import functools
import logging
import os
from typing import List

import pygame

from settings import FONTS_DIR, IMAGES_DIR, SOUNDS_DIR


def load_font(filename: str, size: int) -> pygame.font.Font:
    """Load font from file"""
    fullpath = os.path.join(FONTS_DIR, filename)
    logging.info(f"Load font '{fullpath}' with size {size}")
    return pygame.font.Font(fullpath, size)


@functools.lru_cache(256)
def load_image(filename: str) -> pygame.Surface:
    """Load an image from filesystem"""
    fullpath = os.path.join(IMAGES_DIR, filename)
    logging.info(f"Load image '{fullpath}'")
    return pygame.image.load(fullpath).convert_alpha()


def load_sound(filename: str) -> pygame.mixer.Sound:
    """Load sound from filesystem"""
    fullpath = os.path.join(SOUNDS_DIR, filename)
    logging.info(f"Load sound '{fullpath}'")
    return pygame.mixer.Sound(fullpath)


class Sprite(pygame.sprite.Sprite):
    def __init__(
        self, image: pygame.Surface, *groups: List[pygame.sprite.Group]
    ) -> None:
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_rect()


class FontSprite(Sprite):
    def __init__(
        self,
        text: str,
        font_name: str,
        font_size: int,
        color: pygame.Color,
        *groups: List[pygame.sprite.Group],
    ) -> None:
        font = load_font(font_name, font_size)
        image = font.render(text, True, color)
        super().__init__(image, *groups)
