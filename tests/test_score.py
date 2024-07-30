import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from components.score import get_score, get_score_and_tier

# Mocking the game settings
class MockGame:
    TOTAL_QUESTIONS = 10
    MAX_TIME = 60
    SCORE_1_STAR_CUTOFF = 300
    SCORE_2_STAR_CUTOFF = 700

@patch('config.game', MockGame)
def test_get_score():
    # Test case 1: No mistakes, minimal time
    assert get_score(total_mistakes=0, max_mistakes=10, total_time=0, max_time=60) == 1000

    # Test case 2: Maximum mistakes, maximum time
    assert get_score(total_mistakes=10, max_mistakes=10, total_time=60, max_time=60) == 0

    # Test case 3: Some mistakes and some time
    assert get_score(total_mistakes=5, max_mistakes=10, total_time=30, max_time=60) == 750

    # Test case 4: Edge cases
    assert get_score(total_mistakes=10, max_mistakes=5, total_time=60, max_time=30) == 0
    assert get_score(total_mistakes=0, max_mistakes=10, total_time=60, max_time=0) == 0

@patch('config.game', MockGame)
def test_get_score_and_tier():
    # Test case 1: Score above 700 should be 3-star
    assert get_score_and_tier(total_mistakes=0, total_time=10) == (1000, 3)

    # Test case 2: Score between 300 and 700 should be 2-star
    assert get_score_and_tier(total_mistakes=5, total_time=30) == (750, 2)

    # Test case 3: Score below 300 should be 1-star
    assert get_score_and_tier(total_mistakes=10, total_time=60) == (0, 1)

    # Test case 4: Edge cases
    assert get_score_and_tier(total_mistakes=10, total_time=0) == (0, 1)
    assert get_score_and_tier(total_mistakes=0, total_time=0) == (1000, 3)

