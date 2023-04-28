from typing import Any, List, Tuple

import pygame


class InputHandler:
    """handle user inputs"""

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self._on_quit(event)
            cb = None
            if event.type == pygame.KEYDOWN:
                if self.key_down_callbacks is not None:
                    cb = self.key_down_callbacks.get(event.key, None)
            if event.type == pygame.KEYUP:
                if self.key_up_callbacks is not None:
                    cb = self.key_up_callbacks.get(event.key, None)
            if cb is not None:
                return cb(event)

    @property
    def key_down_callbacks(self) -> dict:
        return None

    @property
    def key_up_callbacks(self) -> dict:
        return None

    def _on_quit(self, event: pygame.event.Event):
        pygame.quit()
        quit()


class Renderer:
    """handle rendering"""

    def render(self, screen: pygame.surface.Surface):
        pass


class Updater:
    """handle updates"""

    def update(self, fps: int):
        pass


class Scene:
    """handle user inputs, rendering and update (may delegate to InputHandler, Renderer and Updater)"""

    def handle_inputs(self):
        pass

    def render(self, screen: pygame.Surface):
        pass

    def update(self, fps: int):
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
