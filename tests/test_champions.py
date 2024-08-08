import pytest
from unittest.mock import patch, MagicMock

from components import champions


def test_fetch_champions(mock_get_table, mock_champion_table):
    """
    The test verifies that `fetch_champions` correctly retrieves and formats
    champion data from the spreadsheet storage.
    """
    actual_champions = champions.fetch_champions()
    assert actual_champions == mock_champion_table[1:]


def test_update_champions(mock_set_table):
    """
    The test verifies that `update_champions` correctly updates the champions
    data in the spreadsheet storage with new data.
    """
    new_champions = [
        ('Bob', 900, 1722262477),
        ('Frank', 850, 1722262480),
        ('Dave', 800, 1722262475),
        ('Alice', 780, 1722262478),
        ('Charlie', 767, 1722262476),
    ]
    champions.update_champions(new_champions)
    mock_set_table.assert_called_once_with('champions', new_champions)


def test_turn_index_into_place():
    """
    The test verifies that `turn_index_into_place` correctly converts index
    values to their corresponding 1-based place values.
    """
    assert champions.turn_index_into_place(0) == 1
    assert champions.turn_index_into_place(1) == 2
    assert champions.turn_index_into_place(-1) == -1


def test_record_user_score(mock_set_table, mock_get_table,
                           mock_champion_table):
    """
    The test verifies that `record_user_score` correctly records a new user
    score, updates the leaderboard, and returns the user's rank.
    """
    new_user = ('Frank', 850, 1722262480)
    result = champions.record_user_score(*new_user)

    expected_champions = mock_champion_table[1:]
    expected_champions.insert(2, new_user)
    expected_champions = expected_champions[:5]
    mock_set_table.assert_called_once_with('champions', expected_champions)
    assert result == 3
