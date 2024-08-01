import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
import curses
from config import layout, palette
from screens.login_screen import login_screen_handler
from lib import local_storage

# Mock data for the logo
mock_logo = """ 
  +---------+
  | tWIZY   |
  +---------+
"""

# Mock the logo constant in the module where it's used
@patch('screens.login_screen.logo.LOGO', mock_logo)
@patch('screens.login_screen.local_storage.clear')
@patch('screens.login_screen.local_storage.set_item')
@patch('screens.login_screen.curses.color_pair')
@patch('screens.login_screen.curses.initscr')
@patch('screens.login_screen.curses.start_color')
def test_login_screen_handler(
    mock_start_color, mock_initscr, mock_color_pair,
    mock_set_item, mock_clear
):
    # Mock the standard screen and its methods
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)  # Mock screen dimensions

    # Setting the color pair returns based on palette colors
    mock_color_pair.side_effect = lambda x: x

    # Simulate user input by defining a sequence of getch() return values
    stdscr.getch.side_effect = [ord('T'), ord('e'), ord('s'), ord('t'), ord('\n')]

    # Call the login_screen_handler function
    login_screen_handler(stdscr)

    # Verify that local storage was cleared at the beginning
    mock_clear.assert_called_once()

    # Verify that the set_item was called with the correct username
    mock_set_item.assert_called_once_with("user", "Test")

    # Check that curses functions were called for initialization
    mock_initscr.assert_called_once()
    mock_start_color.assert_called_once()

    # Verify that the screen was cleared and refreshed
    stdscr.clear.assert_called()
    stdscr.refresh.assert_called()
