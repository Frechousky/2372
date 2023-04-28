import queue

import i18n
import pygame

from core import InputHandler, Renderer, Scene, SelectionViewModel
from graphics import FontSprite
from scenes.level_scene import LevelScene
from settings import BLANKA_FONT, GAME_NAME, WINDOW_SIZE


class MenuInputHandler(InputHandler):
    def __init__(self, model: SelectionViewModel, scene_queue: queue.Queue):
        super().__init__()
        self._model = model
        self._scene_queue = scene_queue
        self._key_down_callbacks = {
            pygame.K_KP_ENTER: self._select_menu,
            pygame.K_RETURN: self._select_menu,
        }

    @property
    def key_down_callbacks(self) -> dict:
        return self._key_down_callbacks

    def _select_menu(self, *args, **kwargs):
        # update game scene to level scene
        self._scene_queue.put(LevelScene())


class MenuRenderer(Renderer):
    def __init__(self, model: SelectionViewModel):
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

    def render(self, screen: pygame.surface.Surface):
        screen.fill((0, 0, 0))
        screen.blit(self._banner_sprite.image, self._banner_sprite.rect)
        self._menus_sprite.draw(screen)
        self._draw_selection_cursor(screen)
        pygame.display.update()

    def _draw_selection_cursor(self, screen: pygame.surface.Surface):
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
    def __init__(self, scene_queue: queue.Queue):
        super().__init__()
        self._model = SelectionViewModel(collection=[i18n.t("new_game")])
        self._input_handler = MenuInputHandler(self._model, scene_queue)
        self._renderer = MenuRenderer(self._model)

    def handle_inputs(self):
        self._input_handler.handle_inputs()

    def render(self, screen: pygame.Surface):
        self._renderer.render(screen)
