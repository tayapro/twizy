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
    mock_on_load_login_screen.return_value = screens.HOME_SCREEN
    mock_on_load_home_screen.return_value = screens.GAME_SCREEN
    mock_on_load_game_screen.return_value = screens.OUTCOME_SCREEN
    mock_on_load_outcome_screen.return_value = screens.CHAMPIONS_SCREEN

    # Call the main function
    main()

    # Check that every screen is called once during the flow
    mock_on_load_login_screen.assert_called_once()
    mock_on_load_home_screen.assert_called_once()
    mock_on_load_game_screen.assert_called_once()
    mock_on_load_outcome_screen.assert_called_once()
    mock_on_load_champions_screen.assert_called_once()

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
    mock_on_load_login_screen.return_value = screens.HOME_SCREEN
    mock_on_load_home_screen.side_effect = Exception("Home screen error")
    mock_on_load_error_screen.side_effect = [screens.LOGIN_SCREEN, None]  # Go back to login, then exit

    # Call the main function
    main()

    # Verify that the error screen was displayed after an exception in the home screen
    # Expected flow: 
    # login -> home -> error (user is not set) -> login -> home -> error (None) -> quit
    assert mock_on_load_login_screen.call_count == 2
    assert mock_on_load_error_screen.call_count == 2
    assert mock_on_load_home_screen.call_count == 2
