import pytest
from unittest.mock import MagicMock, patch
import curses

from components.navbar import Navbar, NavAction
from screens.error_screen import error_screen_handler
from config import screens, palette, layout, logo


def test_error_screen_handler(mock_stdscr, mock_color_pair,
                              mock_localstorage_get_item,
                              mock_localstorage_set_item,
                              mock_localstorage_clear):
    """
    The test verifies that the `error_screen_handler` function correctly:
    1. Interacts with local storage to get and set user information.
    2. Clears and refreshes the screen.
    3. Transitions to the home screen based on user input.
    """

    # Any key to home screen
    mock_stdscr.getch.return_value = ord('i')

    result = error_screen_handler(mock_stdscr)

    mock_localstorage_get_item.assert_called_with("user")
    mock_localstorage_clear.assert_called_once()
    mock_localstorage_set_item.assert_called_once_with("user", "TestUser")

    mock_stdscr.clear.assert_called_once()
    mock_stdscr.refresh.assert_called_once()

    assert result == screens.HOME_SCREEN
