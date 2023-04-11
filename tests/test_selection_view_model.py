from typing import List

import pytest

from core import SelectionViewModel

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

test_selected_data = [
    (0, ["en", "fr", "de"], "en"),
    (1, ["en", "fr", "de"], "fr"),
    (2, ["en", "fr", "de"], "de"),
]


@pytest.mark.parametrize("cursor_pos,collection,expected", test_init_data)
def test_init(cursor_pos: int, collection: List[str], expected: int):
    tested = SelectionViewModel(collection, cursor_pos)
    assert (
        tested._cursor_pos == expected
    ), "cursor_pos should be in range [0, len(collection)["


@pytest.mark.parametrize(
    "cursor_pos,collection,expected", test_decrement_cursor_pos_data
)
def test_decrement_cursor_pos(cursor_pos: int, collection: List[str], expected: int):
    tested = SelectionViewModel(collection, cursor_pos)
    tested.decrement_cursor_pos()
    assert tested._cursor_pos == expected, "cursor_pos is updated correctly"


@pytest.mark.parametrize(
    "cursor_pos,collection,expected", test_increment_cursor_pos_data
)
def test_increment_cursor_pos(cursor_pos: int, collection: List[str], expected: int):
    tested = SelectionViewModel(collection, cursor_pos)
    tested.increment_cursor_pos()
    assert tested._cursor_pos == expected, "cursor_pos is updated correctly"


@pytest.mark.parametrize("cursor_pos,collection,expected", test_selected_data)
def test_selected(cursor_pos: int, collection: List[str], expected: str):
    tested = SelectionViewModel(collection, cursor_pos)
    assert tested.selected == expected, "returns selected element"
