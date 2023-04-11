import queue
from typing import List, Tuple

import i18n
import pygame

from core import InputHandler, Renderer, Scene, SelectionViewModel
from graphics import FontSprite
from settings import BLANKA_FONT, GAME_NAME, WINDOW_SIZE


class MenuSceneModel(SelectionViewModel):
    def __init__(self, collection: List | Tuple, cursor_pos=0) -> None:
        super().__init__(collection, cursor_pos)


class MenuSceneInputHandler(InputHandler):
    def __init__(self, model: MenuSceneModel) -> None:
        super().__init__()
        self._model = model


class MenuSceneRenderer(Renderer):
    def __init__(self, model: MenuSceneModel) -> None:
        super().__init__()
        self._model = model
        self._banner_sprite = FontSprite(
            GAME_NAME, BLANKA_FONT, 100, pygame.Color(255, 0, 0)
        )
        self._banner_sprite.rect.top = WINDOW_SIZE[1] // 8
        self._banner_sprite.rect.centerx = WINDOW_SIZE[0] // 2
        self._menus_sprite = pygame.sprite.Group(
            [
                FontSprite(menu_name, BLANKA_FONT, 50, pygame.Color(255, 255, 255))
                for menu_name in self._model.collection
            ]
        )
        for menu_sprite in self._menus_sprite:
            menu_sprite.rect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)

    def render(self, screen: pygame.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        screen.blit(self._banner_sprite.image, self._banner_sprite.rect)
        self._menus_sprite.draw(screen)
        self._draw_selection_cursor(screen)
        pygame.display.update()

    def _draw_selection_cursor(self, screen: pygame.surface.Surface) -> None:
        fs = self._menus_sprite.sprites()[self._model.cursor_pos]
        width = WINDOW_SIZE[0] // 400
        offset = WINDOW_SIZE[0] // 150
        rect = pygame.rect.Rect(
            fs.rect.left - offset,
            fs.rect.top - offset,
            fs.rect.width + 2 * offset,
            fs.rect.height + 2 * offset,
        )
        pygame.draw.rect(surface=screen, color=(255, 0, 0), rect=rect, width=width)


class MenuScene(Scene):
    def __init__(self, scene_queue: queue.Queue) -> None:
        super().__init__()
        self._model = MenuSceneModel(collection=[i18n.t("new_game")])
        self._input_handler = MenuSceneInputHandler(self._model)
        self._renderer = MenuSceneRenderer(self._model)
        self._scene_queue = scene_queue

    def handle_inputs(self) -> None:
        self._input_handler.handle_inputs()

    def render(self, screen: pygame.Surface) -> None:
        self._renderer.render(screen)
