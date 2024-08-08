import pytest
from unittest.mock import MagicMock, patch

from config import screens, layout, palette
from screens.home_screen import home_screen_handler


def test_home_screen_handler(mock_stdscr, mock_color_pair,
                             mock_localstorage_get_item):
    """
    The test verifies that `home_screen_handler` navigates to the game screen
    when the 'g' key is pressed.
    """
    mock_stdscr.getch.side_effect = [ord('g')]

    next_screen = home_screen_handler(mock_stdscr)

    assert next_screen == screens.GAME_SCREEN

    mock_localstorage_get_item.assert_called_once_with("user")

    mock_stdscr.clear.assert_called()
    mock_stdscr.refresh.assert_called()

    mock_stdscr.getmaxyx.assert_called()
    mock_stdscr.addch.assert_called()


def test_home_screen_handler_no_user(mock_stdscr, mock_color_pair,
                                     mock_localstorage_get_item):
    """
    Test `home_screen_handler` to verify that an exception is raised if no user
    name is set in local storage.
    """
    mock_localstorage_get_item.side_effect = [None]

    with pytest.raises(Exception, match="User name is not set"):
        home_screen_handler(mock_stdscr)
