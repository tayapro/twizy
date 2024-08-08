import pytest
from unittest.mock import MagicMock, patch
from screens.outcome_screen import outcome_screen_handler
from config import screens
# from components import score, champions
# from components.score import get_score_and_tier
# from components.champions import record_user_score

# Mock data for local_storage
# mock_user = "TestUser"
# mock_mistakes = 3
# mock_correct_answers = 7
# mock_quiz_time = 120  # in seconds
# mock_end_time = "2023-01-01T12:00:00Z"

# # Mock data for get_score_and_tier and record_user_score
# mock_score = 850
# mock_tier = 3
# mock_place = 3

@pytest.fixture
def mock_data():
    mock = MagicMock()
    mock.user.return_value = "TestUser"
    mock.mistakes.return_value = 3
    mock.correct_answers.return_value = 7
    mock.quiz_time.return_value = 120
    mock.end_time.return_value = "2024-07-01T12:00:00Z"
    mock.score.return_value = 850
    mock.tier.return_value = 3
    mock.place.return_value = 3
    return mock

# mock_data.user()

@pytest.fixture
def mock_get_score_and_tier(monkeypatch):
  mock = MagicMock()
  monkeypatch.setattr('components.score.get_score_and_tier', mock)
  return mock

@pytest.fixture
def mock_record_user_score(monkeypatch):
  mock = MagicMock()
  monkeypatch.setattr('components.champions.record_user_score', mock)
  return mock

# @pytest.fixture
# def mock_outcome_screen_get_table(monkeypatch, mock_champions_table):
#     mock = MagicMock(return_value=mock_champions_table)
#     monkeypatch.setattr('lib.spreadsheet_storage.get_table', mock)
#     return mock

# @patch('screens.outcome_screen.get_score_and_tier')
# @patch('screens.outcome_screen.record_user_score')
def test_outcome_screen_handler(
    mock_data,
    mock_record_user_score,
    mock_get_score_and_tier,
    mock_champion_table,
    mock_stdscr, mock_localstorage_clear, mock_localstorage_get_item, mock_color_pair):
    """
    The test verifies that the `outcome_screen_handler` function correctly
    processes user data, calculates the score and tier, and determines the next
    screen. It also checks interactions with mocked functions and verifies
    correct function calls.
    """
    mock_localstorage_get_item.side_effect = lambda key: {
        "user": mock_data.user(),
        "total_mistakes": mock_data.mistakes(),
        "correct_answers": mock_data.correct_answers(),
        "quiz_time": mock_data.quiz_time(),
        "end_time": mock_data.end_time()
    }.get(key)

    mock_get_score_and_tier.return_value = (mock_data.score(), mock_data.tier())
    mock_record_user_score.return_value = mock_data.place()

    mock_stdscr.getch.side_effect = [ord('h')]
    next_screen = outcome_screen_handler(mock_stdscr)
    assert next_screen == screens.HOME_SCREEN

    mock_localstorage_get_item.assert_any_call("user")
    mock_localstorage_get_item.assert_any_call("total_mistakes")
    mock_localstorage_get_item.assert_any_call("correct_answers")
    mock_localstorage_get_item.assert_any_call("quiz_time")
    mock_localstorage_get_item.assert_any_call("end_time")

    mock_get_score_and_tier.assert_called_once_with(mock_data.mistakes(),
                                                    mock_data.quiz_time())
    mock_record_user_score.assert_called_once_with(mock_data.user(), mock_data.score(),
                                                   mock_data.end_time())

    mock_stdscr.clear.assert_called()
    mock_stdscr.refresh.assert_called()
    mock_stdscr.getmaxyx.assert_called()


def test_outcome_screen_handler_no_user(mock_localstorage_get_item, mock_color_pair, mock_stdscr):
    mock_localstorage_get_item.side_effect = [None]

    with pytest.raises(Exception, match="User name is not set"):
        outcome_screen_handler(mock_stdscr)
