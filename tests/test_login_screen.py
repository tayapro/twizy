import pytest

from screens.login_screen import login_screen_handler


def test_login_screen_handler(mock_twizy_logo, mock_stdscr, mock_color_pair,
                              mock_localstorage_set_item,
                              mock_localstorage_clear):
    """
    The test verifies that the `login_screen_handler` function:
    - Clears local storage at the beginning of the function.
    - Correctly saves the username entered by the user to local storage.
    - Clears and refreshes the screen.
    """
    mock_stdscr.getch.side_effect = [ord('T'), ord('e'), ord('s'), ord('t'),
                                     ord('\n')]
    login_screen_handler(mock_stdscr)

    mock_localstorage_clear.assert_called_once()

    mock_localstorage_set_item.assert_called_once_with("user", "Test")

    mock_stdscr.clear.assert_called()
    mock_stdscr.refresh.assert_called()
