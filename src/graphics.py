import functools
import logging
import pathlib
from enum import Enum
from typing import List

import pygame

from src.settings import FONTS_DIR, IMAGES_DIR, SOUNDS_DIR


def load_font(filename: str | pathlib.Path, size: int) -> pygame.font.Font:
    """Load font from file"""
    fullpath = FONTS_DIR / filename
    logging.info(f"Load font '{fullpath}' with size {size}")
    return pygame.font.Font(fullpath, size)


@functools.lru_cache(256)
def load_image(filename: str | pathlib.Path) -> pygame.Surface:
    """Load an image from filesystem"""
    fullpath = IMAGES_DIR / filename
    logging.info(f"Load image '{fullpath}'")
    return pygame.image.load(fullpath).convert_alpha()


def load_sound(filename: str | pathlib.Path) -> pygame.mixer.Sound:
    """Load sound from filesystem"""
    fullpath = SOUNDS_DIR / filename
    logging.info(f"Load sound '{fullpath}'")
    return pygame.mixer.Sound(fullpath)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, *groups: List[pygame.sprite.Group]):
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
    ):
        font = load_font(font_name, font_size)
        image = font.render(text, True, color)
        super().__init__(image, *groups)


class Direction(Enum):
    LEFT = 0
    RIGHT = 1


class PlayerState(Enum):
    IDLE = 0
    RUN = 1
    JUMP = 2


class PlayerAnimationHandler:
    # animations per second depending on player state
    ANIMATIONS_FQ_STATE = {
        PlayerState.IDLE.value: 10,
        PlayerState.JUMP.value: 18,
        PlayerState.RUN.value: 12,
    }

    def __init__(
        self, state=PlayerState.IDLE, direction=Direction.RIGHT, animation_time=0
    ) -> None:
        self._state_direction_images = [None] * len(PlayerState)
        # contains 2 list of images for each PlayerState, one for left and one for right direction
        self._state_direction_images[PlayerState.IDLE.value] = [
            [
                load_image(filename)
                for filename in [
                    pathlib.Path("player", "idle", f"idle-left-{i+1}.png")
                    for i in range(4)
                ]
            ],
            [
                load_image(filename)
                for filename in [
                    pathlib.Path("player", "idle", f"idle-right-{i+1}.png")
                    for i in range(4)
                ]
            ],
        ]
        self._state_direction_images[PlayerState.RUN.value] = [
            [
                load_image(filename)
                for filename in [
                    pathlib.Path("player", "run", f"run-left-{i+1}.png")
                    for i in range(8)
                ]
            ],
            [
                load_image(filename)
                for filename in [
                    pathlib.Path("player", "run", f"run-right-{i+1}.png")
                    for i in range(8)
                ]
            ],
        ]
        self._state_direction_images[PlayerState.JUMP.value] = [
            [
                load_image(filename)
                for filename in [
                    pathlib.Path("player", "jump", f"jump-left-{i + 1}.png")
                    for i in range(4)
                ]
            ],
            [
                load_image(filename)
                for filename in [
                    pathlib.Path("player", "jump", f"jump-right-{i + 1}.png")
                    for i in range(4)
                ]
            ],
        ]
        self._state = state
        self._direction = direction
        self._animation_time = animation_time  # in milliseconds

    def update(self, new_state: PlayerState, new_direction: Direction, dt: int):
        if self._state != new_state or self._direction != new_direction:
            # player animation update
            self._animation_time = 0
            self._state = new_state
            self._direction = new_direction
        else:
            self._animation_time += dt

    @property
    def image(self) -> pygame.Surface:
        images = self._state_direction_images[self._state.value][self._direction.value]
        animation_fq = self.ANIMATIONS_FQ_STATE[self._state.value]
        return images[int(self._animation_time * animation_fq / 1000) % len(images)]


class PlayerSprite(Sprite):
    jump_vy = -500  # pixels per second
    max_available_jumps = 2
    max_vx_speed = 500  # pixels per second
    weight = 1500  # pixels per second squared

    def __init__(
        self,
        vx: int = 0,
        vy: int = 0,
        available_jumps: int = max_available_jumps,
        direction=Direction.RIGHT,
        *groups: List[pygame.sprite.Group],
    ):
        self._vx = vx
        self._vy = vy
        self._available_jumps = available_jumps
        self._sprite_sheet = PlayerAnimationHandler(self.state)
        self._direction = direction
        super().__init__(self._sprite_sheet.image, *groups)

    def jump(self):
        if self._available_jumps <= 0:
            return
        self._available_jumps -= 1
        self._vy = self.jump_vy

    def move_right(self):
        self._vx = self.max_vx_speed
        self._direction = Direction.RIGHT

    def move_left(self):
        self._vx = -self.max_vx_speed
        self._direction = Direction.LEFT

    def stop_horizontal_movement(self):
        self._vx = 0

    def update_horizontal_pos(self, dt: int):
        self.rect.centerx += self._vx * dt / 1000

    def update_vertical_pos(self, dt: int):
        self.rect.centery += self._vy * dt / 1000

    def apply_gravity(self, dt: int):
        self._vy += self.weight * dt / 1000

    def hit_ground(self):
        self._available_jumps = self.max_available_jumps
        self._vy = 0

    def hit_roof(self):
        self._vy = 0

    @property
    def state(self) -> PlayerState:
        if self._vy != 0:
            return PlayerState.JUMP
        elif self._vx == self._vy == 0:
            return PlayerState.IDLE
        else:
            return PlayerState.RUN

    def update_image(self, dt: int):
        self._sprite_sheet.update(self.state, self._direction, dt)
        self.image = self._sprite_sheet.image
