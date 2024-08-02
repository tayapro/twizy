import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
import curses
from config import screens, layout, palette
from screens.home_screen import home_screen_handler

# Sample user name for testing
mock_user_name = "TestUser"

@patch('screens.home_screen.local_storage.get_item')
@patch('screens.home_screen.curses.color_pair')
def test_home_screen_handler(mock_color_pair, mock_get_item):
    # Mock the standard screen and its methods
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (24, 80)  # Mock screen dimensions

    # Set the color pair return values based on palette colors
    mock_color_pair.side_effect = lambda x: x

    # Mock the return value of local_storage.get_item to provide a username
    mock_get_item.return_value = mock_user_name

    # Simulate user input for the 'g' key to navigate to the game screen
    stdscr.getch.side_effect = [ord('g')]

    # Call the home_screen_handler function
    next_screen = home_screen_handler(stdscr)

    # Verify that the correct screen was returned
    assert next_screen == screens.GAME_SCREEN

    # Verify that the username was fetched
    mock_get_item.assert_called_once_with("user")

    # Verify that the screen was cleared and refreshed
    stdscr.clear.assert_called()
    stdscr.refresh.assert_called()

    # Check if navbar and elements were drawn correctly
    stdscr.getmaxyx.assert_called()
    stdscr.addch.assert_called()  # to verify any character drawing


@patch('screens.home_screen.local_storage.get_item', return_value=None)
@patch('screens.home_screen.curses.color_pair')
def test_home_screen_handler_no_user(mock_color_pair, mock_get_item):
    # Mock the standard screen and its methods
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (24, 80)  # Mock screen dimensions

    # Set the color pair return values based on palette colors
    mock_color_pair.side_effect = lambda x: x


    # Simulate the scenario where no username is set
    with pytest.raises(Exception, match="User name is not set"):
        home_screen_handler(stdscr)
