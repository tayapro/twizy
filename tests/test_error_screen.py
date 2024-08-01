import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
import curses
from components.navbar import Navbar, NavAction
from screens.error_screen import error_screen_handler
from config import screens, palette, layout, logo


@patch('screens.error_screen.local_storage.get_item')
@patch('screens.error_screen.local_storage.clear')
@patch('screens.error_screen.local_storage.set_item')
@patch('screens.error_screen.curses.color_pair')
@patch('screens.error_screen.curses.initscr')
@patch('screens.error_screen.curses.start_color')
def test_error_screen_handler(
    mock_start_color, mock_initscr, mock_color_pair,
    mock_set_item, mock_clear, mock_get_item
):
    # Mock the standard screen and its methods
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)
    # Simulate pressing 'i' (any button) to home screen
    stdscr.getch.return_value = ord('i')

    # Set return values for mocked functions
    mock_color_pair.side_effect = lambda x: x
    mock_get_item.return_value = "TestUser"

    # Call the error_screen_handler function
    result = error_screen_handler(stdscr)

    # Verify that local storage was accessed correctly
    mock_get_item.assert_called_once_with("user")
    mock_clear.assert_called_once()
    mock_set_item.assert_called_once_with("user", "TestUser")

    # Check that curses functions were called
    mock_initscr.assert_called_once()
    mock_start_color.assert_called_once()

    # Verify the correct drawing actions were called
    stdscr.clear.assert_called_once()
    stdscr.refresh.assert_called_once()

    # Verify that the handler returns the home screen
    assert result == screens.HOME_SCREEN
