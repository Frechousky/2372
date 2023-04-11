import queue
from typing import List

import pygame

from core import InputHandler, Renderer, Scene
from graphics import Sprite, load_image
from scenes.menu_scene import MenuScene
from settings import WINDOW_SIZE, init_i18n


class LocaleSelectionSceneModel:
    def __init__(self, locales: List[str], selection_cursor_pos=0) -> None:
        self._locales = locales
        self._selection_cursor_pos = max(0, min(selection_cursor_pos, len(locales) - 1))

    @property
    def locales(self):
        return self._locales

    def decrement_cursor_pos(self):
        self._selection_cursor_pos -= 1
        self._selection_cursor_pos = self._selection_cursor_pos % len(self._locales)

    def increment_cursor_pos(self):
        self._selection_cursor_pos += 1
        self._selection_cursor_pos = self._selection_cursor_pos % len(self._locales)


class LocaleSelectionInputHandler(InputHandler):
    def __init__(
        self, model: LocaleSelectionSceneModel, scene_queue: queue.Queue
    ) -> None:
        self._model = model
        self._scene_queue = scene_queue
        self._key_down_callbacks = {
            pygame.K_LEFT: self._decrement_cursor_pos,
            pygame.K_RIGHT: self._increment_cursor_pos,
            pygame.K_KP_ENTER: self._select_locale,
            pygame.K_RETURN: self._select_locale,
        }

    @property
    def key_down_callbacks(self) -> dict:
        return self._key_down_callbacks

    def _decrement_cursor_pos(self, *args, **kwargs):
        self._model.decrement_cursor_pos()

    def _increment_cursor_pos(self, *args, **kwargs):
        self._model.increment_cursor_pos()

    def _select_locale(self, *args, **kwargs):
        init_i18n(self._model.locales[self._model._selection_cursor_pos])
        self._scene_queue.put(MenuScene(scene_queue=self._scene_queue))


class LocaleSelectionRenderer(Renderer):
    def __init__(self, model: LocaleSelectionSceneModel) -> None:
        self._model = model
        self._flags = pygame.sprite.Group(
            [Sprite(load_image(f"flag_{locale}.png")) for locale in self._model.locales]
        )
        # update flags position
        for i, fs in enumerate(self._flags):
            v_offset = (WINDOW_SIZE[0] - len(self._model.locales) * fs.rect.width) / (
                len(self._model.locales) + 1
            )
            fs.rect.left = v_offset * (i + 1) + fs.rect.width * i
            fs.rect.top = (WINDOW_SIZE[1] - fs.rect.height) / 2

    def render(self, screen: pygame.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        self._flags.draw(surface=screen)
        self._draw_selection_cursor(screen=screen)
        pygame.display.update()

    def _draw_selection_cursor(self, screen: pygame.surface.Surface) -> None:
        fs = self._flags.sprites()[self._model._selection_cursor_pos]
        width = WINDOW_SIZE[0] // 400
        offset = WINDOW_SIZE[0] // 150
        rect = pygame.rect.Rect(
            fs.rect.left - offset,
            fs.rect.top - offset,
            fs.rect.width + 2 * offset,
            fs.rect.height + 2 * offset,
        )
        pygame.draw.rect(surface=screen, color=(255, 0, 0), rect=rect, width=width)


class LocaleSelectionScene(Scene):
    def __init__(self, locales: List[str], scene_queue: queue.Queue) -> None:
        self._model = LocaleSelectionSceneModel(locales=locales)
        self._input_handler = LocaleSelectionInputHandler(
            model=self._model, scene_queue=scene_queue
        )
        self._renderer = LocaleSelectionRenderer(model=self._model)

    def handle_inputs(self) -> None:
        self._input_handler.handle_inputs()

    def render(self, screen: pygame.Surface) -> None:
        self._renderer.render(screen=screen)
