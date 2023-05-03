import functools
import logging
import os
from enum import Enum
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
    run_offset = 10
    jump_offset = 15
    idle_offset = 8

    def __init__(
        self, state=PlayerState.IDLE, direction=Direction.RIGHT, idx=0.0
    ) -> None:
        self._state_direction_images = [None] * len(PlayerState)
        # contains 2 list of images for each PlayerState, one for left and one for right direction
        self._state_direction_images[PlayerState.IDLE.value] = [
            [
                load_image(filename)
                for filename in [f"player/idle/idle-left-{i+1}.png" for i in range(4)]
            ],
            [
                load_image(filename)
                for filename in [f"player/idle/idle-right-{i+1}.png" for i in range(4)]
            ],
        ]
        self._state_direction_images[PlayerState.RUN.value] = [
            [
                load_image(filename)
                for filename in [f"player/run/run-left-{i+1}.png" for i in range(8)]
            ],
            [
                load_image(filename)
                for filename in [f"player/run/run-right-{i+1}.png" for i in range(8)]
            ],
        ]
        self._state_direction_images[PlayerState.JUMP.value] = [
            [
                load_image(filename)
                for filename in [f"player/jump/jump-left-{i+1}.png" for i in range(4)]
            ],
            [
                load_image(filename)
                for filename in [f"player/jump/jump-right-{i+1}.png" for i in range(4)]
            ],
        ]
        self._state = state
        self._direction = direction
        self._idx = idx

    def update(self, new_state: PlayerState, new_direction: Direction, fps: float):
        if self._state != new_state:
            # player state updated
            self._idx = 0.0
            self._state = new_state
        else:
            offset = self.idle_offset
            if new_state is PlayerState.RUN:
                offset = self.run_offset
            elif new_state is PlayerState.JUMP:
                offset = self.jump_offset
            self._idx += offset / max(fps, 1.0)
        self._direction = new_direction

    @property
    def image(self) -> pygame.Surface:
        images = self._state_direction_images[self._state.value][self._direction.value]
        return images[int(self._idx) % len(images)]


class PlayerSprite(Sprite):
    jump_speed_init = 1000
    max_available_jumps = 2
    max_vx_speed = 1000
    weight = 2500

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
        self._vy = -self.jump_speed_init

    def move_right(self):
        self._vx = self.max_vx_speed
        self._direction = Direction.RIGHT

    def move_left(self):
        self._vx = -self.max_vx_speed
        self._direction = Direction.LEFT

    def stop_horizontal_movement(self):
        self._vx = 0

    def update_horizontal_pos(self, fps: float):
        self.rect.centerx += self._vx // int(max(fps, 1))

    def update_vertical_pos(self, fps: float):
        self.rect.centery += self._vy // int(max(fps, 1))

    def apply_gravity(self, fps: float):
        self._vy += self.weight // int(max(fps, 1))

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

    def update_image(self, fps: float):
        self._sprite_sheet.update(self.state, self._direction, fps)
        self.image = self._sprite_sheet.image

