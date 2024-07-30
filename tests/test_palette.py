import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest import mock
import curses
import sys

from config import palette

@pytest.fixture
def mock_curses():
    """Fixture to mock curses module functions."""
    with mock.patch('curses.init_pair') as mock_init_pair, \
         mock.patch('curses.COLOR_WHITE', new=15), \
         mock.patch('curses.COLOR_BLACK', new=0), \
         mock.patch('curses.COLOR_YELLOW', new=3), \
         mock.patch('curses.wrapper') as mock_wrapper:

        yield {
            'init_pair': mock_init_pair,
            'wrapper': mock_wrapper
        }


def test_init_colors(mock_curses):
    # Mock stdscr
    mock_stdscr = mock.Mock()

    # Call the function
    palette.init_colors()

    # Check if `curses.wrapper` was called with a function
    mock_curses['wrapper'].assert_called_once()
    handle_colors_func = mock_curses['wrapper'].call_args[0][0]

    # Call the passed function with a mock stdscr
    handle_colors_func(mock_stdscr)

    # Verify that init_pair is called with the expected color pairs
    mock_curses['init_pair'].assert_any_call(palette.MAIN_COLOR, 15, 0)
    mock_curses['init_pair'].assert_any_call(palette.MAIN_COLOR_INV, 0, 15)
    mock_curses['init_pair'].assert_any_call(palette.ACCENT_COLOR, 0, 3)
    mock_curses['init_pair'].assert_any_call(palette.ACCENT_COLOR_INV, 3, 0)
