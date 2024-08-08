from unittest.mock import MagicMock, patch, ANY
import pytest
import re

from screens import champions_screen

class ReMatcher(str):
    """
    A helper class to enable regular expression matching in assertions.
    """
    def __init__(self, s):
        self.regex = re.compile(s)

    def __eq__(self, other):
        return self.regex.match(other)


def test_content_screen_handler(mock_stdscr, mock_navbar, mock_screen_elements, 
                                mock_champion_table):
    """
    The test verifies that `content_screen_handler` correctly displays the
    champion data on the screen.
    """
    screen = champions_screen.content_screen_handler(mock_stdscr, mock_navbar,
                                                     mock_screen_elements, mock_champion_table)

    mock_stdscr.addstr.assert_any_call(10, 5, ReMatcher("^Katya\s+991 $"))
    mock_stdscr.addstr.assert_any_call(11, 5, ReMatcher("^John\s+895 $"))
    mock_stdscr.addstr.assert_any_call(12, 5, ReMatcher("^Mark\s+824 $"))
    mock_stdscr.addstr.assert_any_call(13, 5, ReMatcher("^Alice\s+783 $"))
    mock_stdscr.addstr.assert_any_call(14, 5, ReMatcher("^Orla\s+777 $"))

    assert screen is None


def test_skeleton_screen_handler(mock_stdscr, mock_navbar, mock_screen_elements, 
                                 mock_color_pair, mock_get_table, mock_champion_table):
    """
    The test verifies that `skeleton_screen_handler` correctly retrieves and
    returns champion data for the screen. It ensures that the function returns
    the mock data and that the screen is refreshed.
    """

    result = champions_screen.skeleton_screen_handler(mock_stdscr, mock_navbar, mock_screen_elements)
    assert result == mock_champion_table[1:]
    mock_stdscr.refresh.assert_called()


def test_champions_screen_handler(mock_stdscr, mock_color_pair, mock_get_table):
    """
    The test verifies that `champions_screen_handler` correctly handles
    user input and returns the expected result. Specifically, it checks that
    pressing 'q' results in quitting the screen.
    """

    mock_stdscr.getch.side_effect = [ord('q')]
    result = champions_screen.champions_screen_handler(mock_stdscr)
    assert result is None 


def test_on_load_champions_screen():
    """
    The test verifies that `on_load_champions_screen` correctly sets up
    the handler for the champions screen.
    """
    mock_w = MagicMock()
    mock_handler = MagicMock()

    wrapped_handler = champions_screen.on_load_champions_screen(mock_w)
    wrapped_handler(mock_handler)

    mock_w.assert_called_once_with(champions_screen.champions_screen_handler)
