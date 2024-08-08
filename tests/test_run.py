import pytest
from unittest.mock import patch, MagicMock
from run import main
from screens.login_screen import on_load_login_screen
from screens.home_screen import on_load_home_screen
from screens.game_screen import on_load_game_screen
from screens.champions_screen import on_load_champions_screen
from screens.outcome_screen import on_load_outcome_screen
from screens.error_screen import on_load_error_screen


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
def test_main_flow(mock_curses_wrapper,
                   mock_on_load_error_screen,
                   mock_on_load_outcome_screen,
                   mock_on_load_champions_screen,
                   mock_on_load_game_screen,
                   mock_on_load_home_screen,
                   mock_on_load_login_screen,
                   mock_init_colors,
                   mock_init_storage):
    """
    The test simulates a sequence of screens transitions:
    - From login to home
    - From home to game
    - From game to outcome
    - From outcome to champions

    It verifies that:
    - Each screen function is called once.
    - Initialization functions `init_storage` and `init_colors`
      are called once.
    """
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
                                mock_on_load_login_screen, mock_init_colors,
                                mock_init_storage):
    """
    The test simulates an exception during the login screen loading:
    - It ensures that the error screen is displayed.
    - It verifies that the main function handles the exception and
      exits correctly.

    It also simulates that the error screen will cause the program to exit
    by returning `None`.
    """
    # Simulate an exception in the login screen
    mock_on_load_login_screen.side_effect = Exception("Login error")
    mock_on_load_error_screen.side_effect = [None]

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
def test_home_screen_exception(mock_curses_wrapper,
                               mock_on_load_error_screen,
                               mock_on_load_home_screen,
                               mock_on_load_login_screen,
                               mock_init_colors,
                               mock_init_storage):
    """
    The test simulates an exception occurring while loading the home screen,
    and verifies that:
    - The error screen is displayed after the exception.
    - The main function handles the exception and retries as expected.
    """
    # Set up the screens to transition from login to home
    mock_on_load_login_screen.return_value = screens.HOME_SCREEN
    mock_on_load_home_screen.side_effect = Exception("Home screen error")
    # Go back to login, then exit
    mock_on_load_error_screen.side_effect = [screens.LOGIN_SCREEN, None]

    # Call the main function
    main()

    # Verify that the error screen was displayed after an exception in
    # the home screen
    # Expected flow:
    # login -> home -> error (user is not set) -> login ->
    # -> home -> error (None) -> quit
    assert mock_on_load_login_screen.call_count == 2
    assert mock_on_load_error_screen.call_count == 2
    assert mock_on_load_home_screen.call_count == 2
