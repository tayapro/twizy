import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from run import main
from config import screens

# Mock initialization functions and screen loading functions
@patch('run.init_storage')
@patch('run.palette.init_colors')
@patch('run.on_load_login_screen')
@patch('run.on_load_home_screen')
@patch('run.on_load_game_screen')
@patch('run.on_load_champions_screen')
@patch('run.on_load_outcome_screen')
@patch('run.on_load_error_screen')
@patch('run.curses.wrapper')
def test_main_flow(mock_curses_wrapper, mock_on_load_error_screen, mock_on_load_outcome_screen,
                   mock_on_load_champions_screen, mock_on_load_game_screen, mock_on_load_home_screen,
                   mock_on_load_login_screen, mock_init_colors, mock_init_storage):
    # Simulate the sequence of screens
    # mock_on_load_login_screen.side_effect = [None]  # Login screen loads once
    mock_on_load_home_screen.side_effect = [screens.HOME_SCREEN]
    mock_on_load_game_screen.side_effect = [screens.GAME_SCREEN]
    mock_on_load_champions_screen.side_effect = [screens.CHAMPIONS_SCREEN]
    mock_on_load_outcome_screen.side_effect = [screens.OUTCOME_SCREEN]
    # mock_on_load_error_screen.side_effect = [None]

    # Call the main function
    main()

    # Check that the screens were loaded in the correct order
    # assert mock_on_load_login_screen.call_count == 1
    assert mock_on_load_home_screen.call_count == 0
    assert mock_on_load_game_screen.call_count == 1
    assert mock_on_load_champions_screen.call_count == 2
    assert mock_on_load_outcome_screen.call_count == 3

    # Check that init_storage and init_colors were called
    mock_init_storage.assert_called_once()
    mock_init_colors.assert_called_once()

@patch('run.init_storage')
@patch('run.palette.init_colors')
@patch('run.on_load_login_screen')
@patch('run.on_load_error_screen')
@patch('run.curses.wrapper')
def test_login_screen_exception(mock_curses_wrapper, mock_on_load_error_screen, 
                                mock_on_load_login_screen, mock_init_colors, mock_init_storage):
    # Simulate an exception in the login screen
    mock_on_load_login_screen.side_effect = Exception("Login error")
    mock_on_load_error_screen.side_effect = [None]  # Simulate exiting after error screen

    # Call the main function
    main()

    # Verify the error handling and that the error screen was called
    mock_on_load_error_screen.assert_called_once()

@patch('run.init_storage')
@patch('run.palette.init_colors')
@patch('run.on_load_login_screen')
@patch('run.on_load_home_screen')
@patch('run.on_load_error_screen')
@patch('run.curses.wrapper')
def test_home_screen_exception(mock_curses_wrapper, mock_on_load_error_screen, 
                               mock_on_load_home_screen, mock_on_load_login_screen, 
                               mock_init_colors, mock_init_storage):
    # Set up the screens to transition from login to home
    mock_on_load_login_screen.return_value = None
    mock_on_load_home_screen.side_effect = Exception("Home screen error")
    mock_on_load_error_screen.side_effect = [screens.HOME_SCREEN, None]  # Go back to home, then exit

    # Call the main function
    main()

    # Verify that the error screen was displayed after an exception in the home screen
    assert mock_on_load_error_screen.call_count == 1
    assert mock_on_load_home_screen.call_count == 1
