import pytest
import curses
from unittest.mock import MagicMock, patch
from components.menu import Menu


def test_menu_draw(mock_color_pair, mock_stdscr):
    """
    The test verifies that the `draw` method correctly displays the menu title
    and options on the screen with appropriate formatting and color pairs.
    """
    mock_color_pair.side_effect = [10, 20]

    title = "Main Menu"
    options = ["Option 1", "Option 2", "Option 3"]
    show_numbers = True
    menu = Menu(5, 10, title, show_numbers, *options)
    menu.draw(mock_stdscr)

    mock_stdscr.addstr.assert_any_call(5, 10, title)

    expected_calls = [
        ((6, 10, "1. Option 1", 20),),
        ((7, 10, "2. Option 2", 10),),
        ((8, 10, "3. Option 3", 10),),
    ]
    mock_stdscr.addstr.assert_has_calls(expected_calls, any_order=False)


def test_menu_update():
    """
    The test checks that the `update` method correctly navigates through the
    menu options using up and down keys, wrapping around when necessary.
    """
    options = ["Option 1", "Option 2", "Option 3"]
    menu = Menu(5, 10, "", False, *options)

    assert menu.get_selection() == 0

    menu.update(curses.KEY_DOWN)
    assert menu.get_selection() == 1

    menu.update(curses.KEY_DOWN)
    assert menu.get_selection() == 2

    menu.update(curses.KEY_DOWN)
    assert menu.get_selection() == 0

    menu.update(curses.KEY_UP)
    assert menu.get_selection() == 2

    menu.update(curses.KEY_UP)
    assert menu.get_selection() == 1
