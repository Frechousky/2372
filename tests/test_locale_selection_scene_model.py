from typing import List

import pytest

from scenes.locale_selection_scene import LocaleSelectionSceneModel

test_init_data = [
    (0, ["en", "fr", "de"], 0),
    (1, ["en", "fr", "de"], 1),
    (2, ["en", "fr", "de"], 2),
    (-1, ["en", "fr", "de"], 0),
    (-55, ["en", "fr", "de"], 0),
    (3, ["en", "fr", "de"], 2),
    (99, ["en", "fr", "de"], 2),
]

test_decrement_cursor_pos_data = [
    (0, ["en", "fr", "de"], 2),
    (1, ["en", "fr", "de"], 0),
    (2, ["en", "fr", "de"], 1),
]
test_increment_cursor_pos_data = [
    (0, ["en", "fr", "de"], 1),
    (1, ["en", "fr", "de"], 2),
    (2, ["en", "fr", "de"], 0),
]


@pytest.mark.parametrize("cursor_pos,locales,expected", test_init_data)
def test_init(cursor_pos: int, locales: List[str], expected: int):
    tested = LocaleSelectionSceneModel(locales, cursor_pos)
    assert (
        tested._selection_cursor_pos == expected
    ), "cursor pos should be in range [0, len(locales)["


@pytest.mark.parametrize("cursor_pos,locales,expected", test_decrement_cursor_pos_data)
def test_decrement_cursor_pos(cursor_pos: int, locales: List[str], expected: int):
    tested = LocaleSelectionSceneModel(locales, cursor_pos)
    tested.decrement_cursor_pos()
    assert tested._selection_cursor_pos == expected, "cursor pos is updated correctly"


@pytest.mark.parametrize("cursor_pos,locales,expected", test_increment_cursor_pos_data)
def test_increment_cursor_pos(cursor_pos: int, locales: List[str], expected: int):
    tested = LocaleSelectionSceneModel(locales, cursor_pos)
    tested.increment_cursor_pos()
    assert tested._selection_cursor_pos == expected, "cursor pos is updated correctly"
