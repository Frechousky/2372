import logging
import queue

import pygame

from locale_selection_scene import LocaleSelectionScene
from settings import FPS, LOGS_FILE, WINDOW_SIZE


class Game:

    def __init__(self):
        logging.basicConfig(filename=LOGS_FILE, level=logging.DEBUG, format='{asctime} {filename:>15s}:{lineno:<3d} {levelname:>8s} {message}',
                            datefmt='%Y-%m-%d %H:%M:%S', style='{')
        pygame.init()
        pygame.mouse.set_visible(0)
        self._screen = pygame.surface.Surface(WINDOW_SIZE)
        self._scene_queue = queue.Queue()
        self._scene = LocaleSelectionScene(self._scene_queue)
        self._clock = pygame.time.Clock()

    def run(self):
        logging.debug('Run the game')
        while 1:
            current_fps = self._clock.tick(FPS)
            if not self._scene_queue.empty():
                # update scene
                self._scene = self._scene_queue.get()
            self._scene.handle_inputs()
            self._scene.update(current_fps)
            self._scene.render(self._screen)


if __name__ == '__main__':
    game = Game()
    game.run()