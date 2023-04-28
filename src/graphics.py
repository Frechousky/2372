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


class PlayerSprite(Sprite):
    jump_speed_init = 300
    max_available_jumps = 2
    max_vx_speed = 120
    weight = 300

    def __init__(
        self,
        vx: int = 0,
        vy: int = 0,
        available_jumps: int = max_available_jumps,
        *groups: List[pygame.sprite.Group],
    ) -> None:
        image = pygame.surface.Surface(size=(32, 32))
        image.fill((255, 0, 0))
        super().__init__(image, *groups)
        self._vx = vx
        self._vy = vy
        self._available_jumps = available_jumps

    def jump(self):
        if self._available_jumps <= 0:
            return
        self._available_jumps -= 1
        self._vy = -self.jump_speed_init

    def move_right(self):
        self._vx = self.max_vx_speed

    def move_left(self):
        self._vx = -self.max_vx_speed

    def stop_horizontal_movement(self):
        self._vx = 0

    def update_position(self, fps: float):
        self.rect.centerx += self._vx // int(max(fps, 1))
        self.rect.centery += self._vy // int(max(fps, 1))

    def apply_gravity(self, fps: float):
        self._vy += self.weight // int(max(fps, 1))

    def hit_ground(self):
        self._available_jumps = self.max_available_jumps
        self._vy = 0.0
