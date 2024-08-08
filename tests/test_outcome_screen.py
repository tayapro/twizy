import pytest
from unittest.mock import MagicMock, patch
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


@patch('screens.outcome_screen.get_score_and_tier')
@patch('screens.outcome_screen.record_user_score')
def test_outcome_screen_handler(
    mock_record_user_score,
    mock_get_score_and_tier,
    mock_stdscr, mock_localstorage_clear, mock_localstorage_get_item
):
    """
    The test verifies that the `outcome_screen_handler` function correctly
    processes user data, calculates the score and tier, and determines the next
    screen. It also checks interactions with mocked functions and verifies
    correct function calls.
    """
    mock_localstorage_get_item.side_effect = lambda key: {
        "user": mock_user,
        "total_mistakes": mock_mistakes,
        "correct_answers": mock_correct_answers,
        "quiz_time": mock_quiz_time,
        "end_time": mock_end_time
    }.get(key)

    mock_get_score_and_tier.return_value = (mock_score, mock_tier)
    mock_record_user_score.return_value = mock_place

    mock_stdscr.getch.side_effect = [ord('h')]

    next_screen = outcome_screen_handler(mock_stdscr)

    assert next_screen == screens.HOME_SCREEN

    mock_localstorage_get_item.assert_any_call("user")
    mock_localstorage_get_item.assert_any_call("total_mistakes")
    mock_localstorage_get_item.assert_any_call("correct_answers")
    mock_localstorage_get_item.assert_any_call("quiz_time")
    mock_localstorage_get_item.assert_any_call("end_time")

    mock_get_score_and_tier.assert_called_once_with(mock_mistakes,
                                                    mock_quiz_time)
    mock_record_user_score.assert_called_once_with(mock_user, mock_score,
                                                   mock_end_time)

    mock_stdscr.clear.assert_called()
    mock_stdscr.refresh.assert_called()
    mock_stdscr.getmaxyx.assert_called()


def test_outcome_screen_handler_no_user(mock_localstorage_clear, mock_localstorage_get_item, mock_stdscr):
    mock_localstorage_get_item.return_value = None

    with pytest.raises(Exception, match="User name is not set"):
        outcome_screen_handler(mock_stdscr)
