import queue

import pygame
import pytest

from core import SelectionViewModel
from scenes.menu_scene import MenuInputHandler

MENUS = ["menu1"]
CURSOR_POS_INIT = 0


@pytest.fixture
def tested() -> MenuInputHandler:
    return MenuInputHandler(
        SelectionViewModel(collection=MENUS, cursor_pos=CURSOR_POS_INIT),
        queue.Queue(),
    )


@pytest.mark.parametrize("key", [pygame.K_RETURN, pygame.K_KP_ENTER])
def test_on_enter_input_posts_to_scene_queue(
    mocker, tested: MenuInputHandler, key: int
):
    mock_ret = [pygame.event.Event(pygame.KEYDOWN, {"key": key})]
    mocker.patch("pygame.event.get", return_value=mock_ret)

    assert tested._scene_queue.empty(), "scene_queue is empty"

    tested.handle_inputs()

    assert not tested._scene_queue.empty(), "scene_queue is not empty"
