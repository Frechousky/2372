import queue
from typing import List

import i18n
import pygame

from core import InputHandler, Renderer, Scene, Updater
from graphics import load_font
from settings import BLANKA_FONT


class StartMenuEntrySprite(pygame.sprite.Sprite):
    def __init__(self, *groups: List[pygame.sprite.Group]) -> None:
        super().__init__(*groups)
        font = load_font(BLANKA_FONT, 50)
        self.image = font.render(i18n.t("new_game"), False, (255, 255, 255))
        self.rect = self.image.get_rect()


class MenuSceneModel:
    def __init__(self) -> None:
        self.cursor_pos = 0
        self.menu_entries = pygame.sprite.Group(StartMenuEntrySprite())


class MenuSceneInputHandler(InputHandler):
    def __init__(self, model: MenuSceneModel) -> None:
        super().__init__()
        self._model = model

    def _on_key_down(self, event: pygame.event.Event) -> None:
        pass

    def _on_key_up(self, event: pygame.event.Event) -> None:
        pass


class MenuSceneRenderer(Renderer):
    def __init__(self, model: MenuSceneModel) -> None:
        super().__init__()
        self._model = model

    def render(self, screen: pygame.surface.Surface) -> None:
        screen.fill((0, 0, 0))
        self._model.menu_entries.draw(screen)
        pygame.display.update()


class MenuSceneUpdater(Updater):
    def __init__(self, model: MenuSceneModel) -> None:
        super().__init__()
        self._model = model

    def update(self, fps: int) -> None:
        pass


class MenuScene(Scene):
    def __init__(self, scene_queue: queue.Queue) -> None:
        super().__init__()
        self._model = MenuSceneModel()
        self._input_handler = MenuSceneInputHandler(self._model)
        self._renderer = MenuSceneRenderer(self._model)
        self._updater = MenuSceneUpdater(self._model)
        self._scene_queue = scene_queue

    def handle_inputs(self) -> None:
        self._input_handler.handle_inputs()

    def render(self, screen: pygame.Surface) -> None:
        self._renderer.render(screen)

    def update(self, fps: int) -> None:
        self._updater.update(fps)
