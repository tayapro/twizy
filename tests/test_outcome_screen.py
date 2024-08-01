import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
import curses
from screens.outcome_screen import outcome_screen_handler
from config import screens

# Mock data for local_storage
mock_user = "TestUser"
mock_mistakes = 3
mock_correct_answers = 7
mock_quiz_time = 120  # in seconds
mock_end_time = "2023-01-01T12:00:00Z"

# Mock data for get_score_and_tier and record_user_score
mock_score = 850
mock_tier = 3
mock_place = 3

@patch('screens.outcome_screen.local_storage.get_item')
@patch('screens.outcome_screen.local_storage.clear')
@patch('screens.outcome_screen.get_score_and_tier')
@patch('screens.outcome_screen.record_user_score')
@patch('screens.outcome_screen.curses.color_pair')
@patch('screens.outcome_screen.curses.initscr')
@patch('screens.outcome_screen.curses.start_color')
def test_outcome_screen_handler(
    mock_start_color, mock_initscr, mock_color_pair, mock_record_user_score,
    mock_get_score_and_tier, mock_clear, mock_get_item
):
    # Mock the standard screen and its methods
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (24, 80)  # Mock screen dimensions

    # Set the color pair return values based on palette colors
    mock_color_pair.side_effect = lambda x: x

    # Mock the return values of local_storage.get_item
    mock_get_item.side_effect = lambda key: {
        "user": mock_user,
        "total_mistakes": mock_mistakes,
        "correct_answers": mock_correct_answers,
        "quiz_time": mock_quiz_time,
        "end_time": mock_end_time
    }.get(key)

    # Mock the return values of get_score_and_tier and record_user_score
    mock_get_score_and_tier.return_value = (mock_score, mock_tier)
    mock_record_user_score.return_value = mock_place

    # Simulate user input for the 'h' key to navigate to the home screen
    stdscr.getch.side_effect = [ord('h')]

    # Call the outcome_screen_handler function
    next_screen = outcome_screen_handler(stdscr)

    # Verify that the correct screen was returned
    assert next_screen == screens.HOME_SCREEN

    # Verify that local_storage.get_item was called for required items
    mock_get_item.assert_any_call("user")
    mock_get_item.assert_any_call("total_mistakes")
    mock_get_item.assert_any_call("correct_answers")
    mock_get_item.assert_any_call("quiz_time")
    mock_get_item.assert_any_call("end_time")

    # Verify that get_score_and_tier and record_user_score were called correctly
    mock_get_score_and_tier.assert_called_once_with(mock_mistakes, mock_quiz_time)
    mock_record_user_score.assert_called_once_with(mock_user, mock_score, mock_end_time)

    # Check that curses functions were called for initialization
    mock_initscr.assert_called_once()
    mock_start_color.assert_called_once()

    # Verify that the screen was cleared and refreshed
    stdscr.clear.assert_called()
    stdscr.refresh.assert_called()

    # Check if navbar and elements were drawn correctly
    stdscr.getmaxyx.assert_called()

@patch('screens.outcome_screen.local_storage.get_item')
@patch('screens.outcome_screen.local_storage.clear')
def test_outcome_screen_handler_no_user(mock_clear, mock_get_item):
    # Mock the standard screen and its methods
    stdscr = MagicMock()

    # Simulate the scenario where no username is set
    mock_get_item.return_value = None

    # Expect an exception to be raised due to missing user name
    with pytest.raises(Exception, match="User name is not set"):
        outcome_screen_handler(stdscr)
