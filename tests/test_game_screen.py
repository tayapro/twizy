import pytest
from unittest.mock import MagicMock, patch
from screens import game_screen

# Mock configurations for layout, palette, game, and screens
class MockLayout:
    FRAME_PADDING_TOP = 6
    FRAME_PADDING_LEFT = 5
    FRAME_PADDING_BOTTOM = 3
    FRAME_PADDING_RIGHT = 5
    MAIN_TEXT_MARGIN_X = 20

class MockPalette:
    MAIN_COLOR = 1

class MockGame:
    TOTAL_QUESTIONS = 10

class MockScreens:
    HOME_SCREEN = 0
    GAME_SCREEN = 1
    OUTCOME_SCREEN = 3

# Mock data for quiz questions
mock_quiz_table = [
    ("question", "correct option", "option_0", "option_1", "option_2", "option_3"),
    ("What is 2+2?", "0", "3", "4", "5", "6"),
    ("What is the capital of France?", "0", "Berlin", "Madrid", "Paris", "Rome"),
    ("What is the boiling point of water?", "1", "90", "100", "80", "110"),
]

mock_quiz_data = mock_quiz_table[1:]
mock_quiz_data.sort(key=lambda x: x[0])

# Mock fixture to patch configurations and data
@pytest.fixture(autouse=True)
def mock_imports_and_configs(monkeypatch):
    monkeypatch.setattr('config.layout', MockLayout)
    monkeypatch.setattr('config.palette', MockPalette)
    monkeypatch.setattr('config.game', MockGame)
    monkeypatch.setattr('config.screens', MockScreens)
    monkeypatch.setattr('lib.spreadsheet_storage.get_table', lambda x: mock_quiz_table)
    monkeypatch.setattr('lib.local_storage.get_item', lambda x: "Test User" if x == "user" else None)
    monkeypatch.setattr('lib.local_storage.set_item', lambda x, y: None)
    monkeypatch.setattr('screens.game_screen.curses.color_pair', lambda x: x)

def test_content_screen_handler():
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)
    stdscr.getch.side_effect = [ord('a')]  # Simulate pressing 'a' to quit

    navbar = MagicMock()
    navbar.update.return_value = (True, 0)  # Mock update returning a screen switch

    elements = [MagicMock()]
    data = mock_quiz_data

    # Call the content screen handler
    screen = game_screen.content_screen_handler(stdscr, navbar, elements, data)
    
    # Ensure it returns the outcome screen
    assert screen == MockScreens.HOME_SCREEN
    # Check that addstr was called to ensure drawing operations
    stdscr.addstr.assert_called()

def test_skeleton_screen_handler():
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)

    navbar = MagicMock()
    elements = [MagicMock()]

    # Call the skeleton screen handler
    result = game_screen.skeleton_screen_handler(stdscr, navbar, elements)
    
    # Ensure the returned quiz data matches mock data
    # Sort to overcome shuffle
    result.sort(key=lambda x: x[0])
    assert result == mock_quiz_data

    # Check that refresh was called to ensure drawing operations
    stdscr.refresh.assert_called()

@patch('screens.game_screen.skeleton_screen_handler', return_value=mock_quiz_data)
def test_game_screen_handler(mock_skeleton_handler):
    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)
    stdscr.getch.side_effect = [ord('q')]  # Simulate pressing 'q' to quit

    # Call the game screen handler
    result = game_screen.game_screen_handler(stdscr)
    
    # Ensure it returns the None value which indicates quit
    assert result == None

def test_on_load_game_screen():
    mock_w = MagicMock()
    mock_handler = MagicMock()

    # Ensure on_load_game_screen sets the handler correctly
    wrapped_handler = game_screen.on_load_game_screen(mock_w)
    wrapped_handler(mock_handler)

    mock_w.assert_called_once_with(game_screen.game_screen_handler)
