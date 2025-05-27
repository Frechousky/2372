import queue

import i18n
import pygame
import pytest

from src.core import SelectionViewModel
from src.scenes.locale_selection_scene import LocaleSelectionInputHandler

LOCALES = ["en", "fr", "de"]
CURSOR_POS_INIT = 1


@pytest.fixture
def tested() -> LocaleSelectionInputHandler:
    return LocaleSelectionInputHandler(
        SelectionViewModel(collection=LOCALES, cursor_pos=CURSOR_POS_INIT),
        queue.Queue(),
    )


def test_on_left_arrow_input_decrements_cursor_pos(
    mocker, tested: LocaleSelectionInputHandler
):
    mock_ret = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})]
    mocker.patch("pygame.event.get", return_value=mock_ret)

    assert (
        tested._model.cursor_pos == CURSOR_POS_INIT
    ), "cursor_pos has it's initial value"

    tested.handle_inputs()

    assert (
        tested._model.cursor_pos == CURSOR_POS_INIT - 1
    ), "cursor_pos value is updated"


def test_on_right_arrow_input_increments_cursor_pos(
    mocker, tested: LocaleSelectionInputHandler
):
    mock_ret = [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT})]
    mocker.patch("pygame.event.get", return_value=mock_ret)

    assert (
        tested._model.cursor_pos == CURSOR_POS_INIT
    ), "cursor_pos has it's initial value"

    tested.handle_inputs()

    assert (
        tested._model.cursor_pos == CURSOR_POS_INIT + 1
    ), "cursor_pos value is updated"


@pytest.mark.parametrize("key", [pygame.K_RETURN, pygame.K_KP_ENTER])
def test_on_enter_input_inits_i18n(
    mocker, tested: LocaleSelectionInputHandler, key: int
):
    mock_ret = [pygame.event.Event(pygame.KEYDOWN, {"key": key})]
    mocker.patch("pygame.event.get", return_value=mock_ret)
    mocker.patch("src.scenes.locale_selection_scene.MenuScene")
    i18n.set("locale", "en")

    assert (
        i18n.get("locale") != LOCALES[tested._model.cursor_pos]
    ), "locale is not set before pressing enter"

    tested.handle_inputs()

    assert (
        i18n.get("locale") == LOCALES[tested._model.cursor_pos]
    ), "locale is set after pressing enter"


@pytest.mark.parametrize("key", [pygame.K_RETURN, pygame.K_KP_ENTER])
def test_on_enter_input_posts_to_scene_queue(
    mocker, tested: LocaleSelectionInputHandler, key: int
):
    mock_ret = [pygame.event.Event(pygame.KEYDOWN, {"key": key})]
    mocker.patch("pygame.event.get", return_value=mock_ret)
    mocker.patch(
        "src.scenes.locale_selection_scene.MenuScene"
    )  # mock MenuScene creation because it requires pygame init

    assert tested._scene_queue.empty(), "scene_queue is empty"

    tested.handle_inputs()

    assert not tested._scene_queue.empty(), "scene_queue is not empty"
