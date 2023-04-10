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

    def _on_quit(self, event: pygame.event.Event) -> None:
        pygame.quit()
        quit()


class Renderer:
    """handle rendering"""

    def render(self, screen: pygame.surface.Surface) -> None:
        pass


class Updater:
    """handle updates"""

    def update(self, fps: int) -> None:
        pass


class Scene:
    """handle user inputs, rendering and update (may delegate to InputHandler, Renderer and Updater)"""

    def handle_inputs(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass

    def update(self, fps: int) -> None:
        pass
