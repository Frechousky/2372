import queue
from typing import List

import pygame
from menu_scene import MenuScene

from core import InputHandler, Renderer, Scene
from graphics import load_image
from settings import LOCALES, WINDOW_SIZE, init_i18n


class FlagSprite(pygame.sprite.Sprite):

    def __init__(self, imagepath: str, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        self.image = load_image(imagepath)
        self.rect = self.image.get_rect()


class LocaleSelectionSceneModel:

    def __init__(self) -> None:
        self.cursor_pos = 0
        self.flags = pygame.sprite.Group(
            [FlagSprite(f'flag_{locale}.png') for locale in LOCALES])


class LocaleSelectionInputHandler(InputHandler):

    def __init__(self, model: LocaleSelectionSceneModel, scene_queue: queue.Queue) -> None:
        self._model = model
        self._scene_queue = scene_queue
        self._key_down_callbacks = {
            pygame.K_LEFT: self._decrement_cursor_cb,
            pygame.K_RIGHT: self._increment_cursor_cb,
            pygame.K_KP_ENTER: self._select_locale,
            pygame.K_RETURN: self._select_locale,
        }

    @property
    def key_down_callbacks(self) -> dict:
        return self._key_down_callbacks

    def _decrement_cursor_cb(self, *args, **kwargs):
        self._model.cursor_pos -= 1
        self._model.cursor_pos = self._model.cursor_pos % len(LOCALES)

    def _increment_cursor_cb(self, *args, **kwargs):
        self._model.cursor_pos += 1
        self._model.cursor_pos = self._model.cursor_pos % len(LOCALES)

    def _select_locale(self, *args, **kwargs):
        init_i18n(LOCALES[self._model.cursor_pos])
        self._scene_queue.put(MenuScene(self._scene_queue))


class LocaleSelectionRenderer(Renderer):

    def __init__(self, model: LocaleSelectionSceneModel) -> None:
        self._model = model

        # update flags position
        for i, fs in enumerate(self._model.flags):
            v_offset = (WINDOW_SIZE[0] - len(LOCALES)
                        * fs.rect.width) / (len(LOCALES) + 1)
            fs.rect.left = v_offset * (i + 1) + fs.rect.width * i
            fs.rect.top = (WINDOW_SIZE[1] - fs.rect.height) / 2

    def render(self, screen: pygame.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        self._model.flags.draw(screen)
        self._draw_cursor(screen)

    def _draw_cursor(self, screen: pygame.surface.Surface) -> None:
        fs = self._model.flags.sprites()[self._model.cursor_pos]
        width = WINDOW_SIZE[0] // 400
        offset = WINDOW_SIZE[0] // 150
        rect = pygame.rect.Rect(fs.rect.left - offset, fs.rect.top -
                                offset, fs.rect.width + 2*offset, fs.rect.height + 2*offset)
        pygame.draw.rect(screen, (255, 0, 0), rect, width)
        pygame.display.update()


class LocaleSelectionScene(Scene):

    def __init__(self, scene_queue: queue.Queue) -> None:
        self._model = LocaleSelectionSceneModel()
        self._input_handler = LocaleSelectionInputHandler(
            self._model, scene_queue)
        self._renderer = LocaleSelectionRenderer(self._model)

    def handle_inputs(self) -> None:
        self._input_handler.handle_inputs()

    def render(self, screen: pygame.Surface) -> None:
        self._renderer.render(screen)
