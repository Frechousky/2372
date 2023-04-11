import queue
from ast import Tuple
from typing import List

import pygame

from core import InputHandler, Renderer, Scene, SelectionViewModel
from graphics import Sprite, load_image
from scenes.menu_scene import MenuScene
from settings import WINDOW_SIZE, init_i18n


class LocaleSelectionSceneModel(SelectionViewModel):
    def __init__(self, collection: List | Tuple, cursor_pos=0) -> None:
        super().__init__(collection, cursor_pos)


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
        self._model.decrement_cursor()

    def _increment_cursor_pos(self, *args, **kwargs):
        self._model.increment_cursor()

    def _select_locale(self, *args, **kwargs):
        init_i18n(self._model.selected)
        self._scene_queue.put(MenuScene(scene_queue=self._scene_queue))


class LocaleSelectionRenderer(Renderer):
    def __init__(self, model: LocaleSelectionSceneModel) -> None:
        self._model = model
        self._flags = pygame.sprite.Group(
            [
                Sprite(load_image(f"flag_{locale}.png"))
                for locale in self._model.collection
            ]
        )
        # update flags position
        for i, fs in enumerate(self._flags):
            v_offset = (
                WINDOW_SIZE[0] - len(self._model.collection) * fs.rect.width
            ) / (len(self._model.collection) + 1)
            fs.rect.left = v_offset * (i + 1) + fs.rect.width * i
            fs.rect.top = (WINDOW_SIZE[1] - fs.rect.height) / 2

    def render(self, screen: pygame.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        self._flags.draw(surface=screen)
        self._draw_selection_cursor(screen=screen)
        pygame.display.update()

    def _draw_selection_cursor(self, screen: pygame.surface.Surface) -> None:
        fs = self._flags.sprites()[self._model.cursor_pos]
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
        self._model = LocaleSelectionSceneModel(collection=locales)
        self._input_handler = LocaleSelectionInputHandler(
            model=self._model, scene_queue=scene_queue
        )
        self._renderer = LocaleSelectionRenderer(model=self._model)

    def handle_inputs(self) -> None:
        self._input_handler.handle_inputs()

    def render(self, screen: pygame.Surface) -> None:
        self._renderer.render(screen=screen)
