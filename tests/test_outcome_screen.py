import pytest
from unittest.mock import MagicMock

from screens.outcome_screen import outcome_screen_handler
from config import screens


@pytest.fixture
def mock_data():
    """
    Fixture to create a mocked data object that simulates user data and quiz
    results. This includes information like the user's name, number of
    mistakes, correct answers, quiz time, end time, score, tier, and place.
    """
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


@pytest.fixture
def mock_get_score_and_tier(monkeypatch):
    """
    Fixture to mock the `get_score_and_tier` function from the
    `components.score` module. This allows testing of the outcome screen
    handler without relying on the actual implementation
    of `get_score_and_tier`.
    """
    mock = MagicMock()
    monkeypatch.setattr('components.score.get_score_and_tier', mock)

    return mock


@pytest.fixture
def mock_record_user_score(monkeypatch):
    """
    Fixture to mock the `record_user_score` function from the
    `components.champions` module.
    This allows testing of the outcome screen handler without relying on
    the actual implementation of `record_user_score`.
    """
    mock = MagicMock()
    monkeypatch.setattr('components.champions.record_user_score', mock)

    return mock


def test_outcome_screen_handler(mock_data, mock_record_user_score,
                                mock_get_score_and_tier, mock_champion_table,
                                mock_get_table, mock_set_table, mock_stdscr,
                                mock_localstorage_clear,
                                mock_localstorage_get_item, mock_color_pair):
    """
    Test for `outcome_screen_handler` that verifies:
    - The function correctly processes user data, calculates the score and
        tier, and determines the next screen.
    - Interactions with mocked functions are performed correctly.
    - Correct function calls to handle and display the outcome of the quiz.

    This test simulates user input and checks if the correct screen is returned
    after the outcome screen is processed.
    """
    mock_localstorage_get_item.side_effect = lambda key: {
        "user": mock_data.user(),
        "total_mistakes": mock_data.mistakes(),
        "correct_answers": mock_data.correct_answers(),
        "quiz_time": mock_data.quiz_time(),
        "end_time": mock_data.end_time()
    }.get(key)

    mock_get_score_and_tier.return_value = (mock_data.score(),
                                            mock_data.tier())
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
    mock_record_user_score.assert_called_once_with(mock_data.user(),
                                                   mock_data.score(),
                                                   mock_data.end_time())

    mock_stdscr.clear.assert_called()
    mock_stdscr.refresh.assert_called()
    mock_stdscr.getmaxyx.assert_called()


def test_outcome_screen_handler_no_user(mock_localstorage_get_item,
                                        mock_color_pair, mock_stdscr):
    """
    Test for `outcome_screen_handler` that verifies the behavior when no user
    data is set.
    If the user name is not present in the local storage, the function should
    raise an exception.
    """
    mock_localstorage_get_item.side_effect = [None]

    with pytest.raises(Exception, match="User name is not set"):
        outcome_screen_handler(mock_stdscr)
