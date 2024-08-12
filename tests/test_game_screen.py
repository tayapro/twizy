import pytest
from unittest.mock import MagicMock, ANY

from screens import game_screen
from config import screens


@pytest.fixture
def mock_quiz_table():
    header = [
        ("question", "correct option", "option_0", "option_1",
         "option_2", "option_3")
    ]
    table = [
        ("What is 2+2?", 0, "3", "4", "5", "6"),
        ("What is the capital of France?", 0, "Berlin", "Madrid",
         "Paris", "Rome"),
        ("What is the boiling point of water?", 1, "90", "100", "80", "110"),
    ]
    table.sort(key=lambda x: x[0])
    return header + table


@pytest.fixture
def mock_game_screen_navbar():
    def navbar_update(stdscr, c):
        if c == ord('a'):
            return (True, 0)
        else:
            raise Exception("test error")

    navbar = MagicMock()
    navbar.update.side_effect = navbar_update
    return navbar


@pytest.fixture
def mock_game_screen_get_table(monkeypatch, mock_quiz_table):
    mock = MagicMock(return_value=mock_quiz_table)
    monkeypatch.setattr('lib.spreadsheet_storage.get_table', mock)
    return mock


def test_content_screen_handler(mock_color_pair, mock_stdscr,
                                mock_screen_elements,
                                mock_quiz_table, mock_game_screen_navbar):
    """
    The test verifies that the `content_screen_handler` function properly
    handles transitions based on user input and updates the screen accordingly.
    """

    # Simulate pressing 'a' to abort
    mock_stdscr.getch.side_effect = [ord('a')]

    # Call the content screen handler
    screen = game_screen.content_screen_handler(mock_stdscr,
                                                mock_game_screen_navbar,
                                                mock_screen_elements,
                                                mock_quiz_table[1:])

    # Ensure it returns the outcome screen
    assert screen == screens.HOME_SCREEN
    # Check that addstr was called to ensure drawing operations
    mock_stdscr.addstr.assert_any_call(13, 20, ANY, ANY)
    mock_stdscr.addstr.assert_any_call(14, 20, ANY, ANY)
    mock_stdscr.addstr.assert_any_call(15, 20, ANY, ANY)
    mock_stdscr.addstr.assert_any_call(16, 20, ANY, ANY)
    mock_stdscr.addstr.assert_any_call(10, 14, ANY, ANY)


def test_skeleton_screen_handler(mock_color_pair, mock_stdscr, mock_quiz_table,
                                 mock_game_screen_get_table,
                                 mock_screen_elements,
                                 mock_game_screen_navbar):
    """
    The test verifies that the `skeleton_screen_handler` function correctly
    retrieves and returns quiz data. It also ensures that the screen was
    refreshed during the operation.
    """
    navbar = MagicMock()

    # Call the skeleton screen handler
    result = game_screen.skeleton_screen_handler(mock_stdscr, navbar,
                                                 mock_screen_elements)

    result.sort(key=lambda x: x[0])
    assert result == mock_quiz_table[1:]

    mock_stdscr.refresh.assert_called()


def test_game_screen_handler(mock_stdscr, mock_quiz_table, mock_color_pair,
                             mock_localstorage_get_item, mock_get_table):
    """
    The test verifies that the `game_screen_handler` function processes
    user input correctly and handles quitting operations as expected.
    """
    mock_get_table.side_effect = lambda x: mock_quiz_table
    # Simulate pressing 'q' to quit
    mock_stdscr.getch.side_effect = [ord('q')]

    result = game_screen.game_screen_handler(mock_stdscr)
    assert result is None


def test_on_load_game_screen():
    """
    The test verifies that the `on_load_game_screen` function correctly
    wraps the game screen handler and sets it up to be used with a provided
    wrapper function.
    """
    mock_w = MagicMock()
    mock_handler = MagicMock()

    # Ensure on_load_game_screen sets the handler correctly
    wrapped_handler = game_screen.on_load_game_screen(mock_w)
    wrapped_handler(mock_handler)

    mock_w.assert_called_once_with(game_screen.game_screen_handler)
