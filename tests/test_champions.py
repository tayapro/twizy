import pytest
from unittest.mock import patch
from components import champions

# Patching lib.spreadsheet_storage functions for testing
@patch('lib.spreadsheet_storage.get_table')
@patch('lib.spreadsheet_storage.set_table')
def test_fetch_champions(mock_set_table, mock_get_table):
    # Setup the mock to return a specific table structure
    mock_get_table.return_value = [
        ['name', 'score', 'timestamp'],
        ['Bob', '900', 1722262477],
        ['Dave', '800', 1722262475],
        ['Alice', '780', 1722262478],
        ['Charlie', '767', 1722262476],
        ['Eve', '720', 1722262474],
    ]

    # Call the function to test
    c = champions.fetch_champions()

    # Expected result
    expected_champions = [
        ('Bob', 900, 1722262477),
        ('Dave', 800, 1722262475),
        ('Alice', 780, 1722262478),
        ('Charlie', 767, 1722262476),
        ('Eve', 720, 1722262474),
    ]

    # Assert that the function returns the expected result
    assert c == expected_champions


@patch('lib.spreadsheet_storage.set_table')
def test_update_champions(mock_set_table):
    # Define the new champions data
    new_champions = [
        ('Bob', 900, 1722262477),
        ('Frank', 850, 1722262480),
        ('Dave', 800, 1722262475),
        ('Alice', 780, 1722262478),
        ('Charlie', 767, 1722262476),
    ]

    # Call the function to test
    champions.update_champions(new_champions)

    # Assert that set_table was called with correct arguments
    mock_set_table.assert_called_once_with('champions', new_champions)


def test_turn_index_into_place():
    # Test various indices
    assert champions.turn_index_into_place(0) == 1
    assert champions.turn_index_into_place(1) == 2
    assert champions.turn_index_into_place(-1) == -1


@patch('lib.spreadsheet_storage.get_table')
@patch('lib.spreadsheet_storage.set_table')
def test_record_user_score(mock_set_table, mock_get_table):
    # Mock data setup: Initially, the leaderboard has 5 players.
    mock_get_table.return_value = [
        ['name', 'score', 'timestamp'],
        ['Bob', '900', 1722262477],
        ['Dave', '800', 1722262475],
        ['Alice', '780', 1722262478],
        ['Charlie', '767', 1722262476],
        ['Eve', '720', 1722262474],
    ]

    # New score to be added
    new_user = ('Frank', 850, 1722262480)
    result = champions.record_user_score(*new_user)

    # Expected champions after adding new user (keeping max 5 and score < 1000)
    expected_champions = [
        ('Bob', 900, 1722262477),
        ('Frank', 850, 1722262480),
        ('Dave', 800, 1722262475),
        ('Alice', 780, 1722262478),
        ('Charlie', 767, 1722262476)
    ]

    # Verify set_table was called correctly
    mock_set_table.assert_called_once_with('champions', expected_champions)

    # Verify the new user's rank (1-based index)
    assert result == 2  # "Frank" should be 2nd on the leaderboard

