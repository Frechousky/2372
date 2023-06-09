import abc
from typing import Any, List, Tuple

import pygame


class InputHandler:
    """handle user inputs"""

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self._on_quit(event)
            callbacks = None
            if event.type == pygame.KEYUP:
                callbacks = self.get_key_up_callbacks()
            elif event.type == pygame.KEYDOWN:
                callbacks = self.get_key_down_callbacks()
            callback = callbacks.get(event.key, None) if callbacks is not None else None
            if callback is not None:
                return callback(event)

    def get_key_down_callbacks(self) -> dict | None:
        return None

    def get_key_up_callbacks(self) -> dict | None:
        return None

    def _on_quit(self, event: pygame.event.Event):
        pygame.quit()
        quit()


class Renderer(abc.ABC):
    """handle rendering"""

    @abc.abstractmethod
    def render(self, screen: pygame.surface.Surface):
        pass


class Updater(abc.ABC):
    """handle updates"""

    @abc.abstractmethod
    def update(self, dt: int):
        pass


class Scene:
    """handle user inputs, rendering and update (may delegate to InputHandler, Renderer and Updater)"""

    def handle_inputs(self):
        pass

    def render(self, screen: pygame.Surface):
        pass

    def update(self, dt: int):
        pass


class SelectionViewModel:
    """view model for selection with cursor screen"""

    def __init__(self, collection: List[Any] | Tuple[Any], cursor_pos=0):
        self._collection = (
            collection if isinstance(collection, tuple.__class__) else tuple(collection)
        )
        # make sure cursor is in range [0, len(collections)[
        self._cursor_pos = max(0, min(cursor_pos, len(collection) - 1))

    @property
    def collection(self) -> Tuple[Any]:
        return self._collection

    @property
    def cursor_pos(self) -> int:
        return self._cursor_pos

    @property
    def selected(self) -> Any:
        return self._collection[self._cursor_pos]

    def decrement_cursor_pos(self):
        self._cursor_pos -= 1
        self._cursor_pos = self._cursor_pos % len(self._collection)

    def increment_cursor_pos(self):
        self._cursor_pos += 1
        self._cursor_pos = self._cursor_pos % len(self._collection)
