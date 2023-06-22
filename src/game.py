import logging
import queue

import pygame

from scenes.locale_selection_scene import LocaleSelectionScene
from settings import FPS, GAME_NAME, LOCALES, LOGS_FILE, WINDOW_SIZE


class Game:
    def __init__(self):
        logging.basicConfig(
            filename=LOGS_FILE,
            level=logging.DEBUG,
            format="{asctime} {filename:<15s} l{lineno:<4d} {levelname:<8s} {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{",
        )
        pygame.init()
        pygame.mouse.set_visible(0)
        self._screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(GAME_NAME)
        self._scene_queue = queue.Queue()
        self._scene = LocaleSelectionScene(LOCALES, self._scene_queue)
        self._clock = pygame.time.Clock()

    def run(self):
        logging.debug("Run the game")
        while 1:
            dt = self._clock.tick(FPS)  # delta time in milliseconds
            if not self._scene_queue.empty():
                # update scene
                self._scene = self._scene_queue.get()
            self._scene.handle_inputs()
            self._scene.update(dt)
            self._scene.render(self._screen)


if __name__ == "__main__":
    game = Game()
    game.run()
