import pytest
from unittest.mock import patch, MagicMock
from components.score import get_score, get_score_and_tier


@pytest.fixture
def mock_game_consts(monkeypatch):
    """
    Fixture to mock the game constants for testing purposes.

    This fixture patches the game configuration constants to use fixed values:
    - TOTAL_QUESTIONS: Total number of questions in the game.
    - MAX_TIME: Maximum time allowed for the quiz.
    - SCORE_1_STAR_CUTOFF: Minimum score for 1 star.
    - SCORE_2_STAR_CUTOFF: Minimum score for 2 stars.
    """
    monkeypatch.setattr("config.game.TOTAL_QUESTIONS", 10)
    monkeypatch.setattr("config.game.MAX_TIME", 60)
    monkeypatch.setattr("config.game.SCORE_1_STAR_CUTOFF", 300)
    monkeypatch.setattr("config.game.SCORE_2_STAR_CUTOFF", 700)


def test_get_score(mock_game_consts):
    """
    Test the `get_score` function to ensure it calculates the score correctly.
    """
    assert get_score(total_mistakes=0, max_mistakes=10,
                     total_time=0, max_time=60) == 1000

    assert get_score(total_mistakes=10, max_mistakes=10,
                     total_time=60, max_time=60) == 0

    assert get_score(total_mistakes=5, max_mistakes=10,
                     total_time=30, max_time=60) == 500

    assert get_score(total_mistakes=10, max_mistakes=5,
                     total_time=60, max_time=30) == 0


def test_get_score_and_tier(mock_game_consts):
    """
    Test the `get_score_and_tier` function to ensure it calculates the score
    and tier correctly.
    """
    assert get_score_and_tier(total_mistakes=4, total_time=10) == (716, 3)

    assert get_score_and_tier(total_mistakes=5, total_time=10) == (666, 2)

    assert get_score_and_tier(total_mistakes=8, total_time=40) == (266, 1)

    assert get_score_and_tier(total_mistakes=10, total_time=60) == (0, 1)
    assert get_score_and_tier(total_mistakes=0, total_time=0) == (1000, 3)
