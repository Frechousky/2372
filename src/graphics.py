import functools
import logging
import os

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
