import pytest
from unittest.mock import patch, MagicMock
from components import champions
import logging


@pytest.fixture
def mock_get_table(monkeypatch):
    """
    Fixture to mock the `get_table` function from `spreadsheet_storage`
    to return a predefined champions table.
    """
    champions_table = [
        ['name', 'score', 'timestamp'],
        ['Bob', '900', 1722262477],
        ['Dave', '800', 1722262475],
        ['Alice', '780', 1722262478],
        ['Charlie', '767', 1722262476],
        ['Eve', '720', 1722262474],
    ]
    m = MagicMock(return_value=champions_table)
    monkeypatch.setattr('lib.spreadsheet_storage.get_table', m)
    return m


@pytest.fixture
def mock_set_table(monkeypatch):
    """
    Fixture to mock the `set_table` function from `spreadsheet_storage`
    to prevent actual updates to the champions table.
    """
    m = MagicMock()
    monkeypatch.setattr('lib.spreadsheet_storage.set_table', m)
    return m


def test_fetch_champions(mock_get_table):
    """
    The test verifies that `fetch_champions` correctly retrieves and formats
    champion data from the spreadsheet storage.
    """
    c = champions.fetch_champions()
    expected_champions = [
        ('Bob', 900, 1722262477),
        ('Dave', 800, 1722262475),
        ('Alice', 780, 1722262478),
        ('Charlie', 767, 1722262476),
        ('Eve', 720, 1722262474),
    ]
    assert c == expected_champions


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


def test_record_user_score(mock_set_table, mock_get_table):
    """
    The test verifies that `record_user_score` correctly records a new user
    score, updates the leaderboard, and returns the user's rank.
    """
    new_user = ('Frank', 850, 1722262480)
    result = champions.record_user_score(*new_user)

    expected_champions = [
        ('Bob', 900, 1722262477),
        ('Frank', 850, 1722262480),
        ('Dave', 800, 1722262475),
        ('Alice', 780, 1722262478),
        ('Charlie', 767, 1722262476)
    ]
    mock_set_table.assert_called_once_with('champions', expected_champions)
    assert result == 2
