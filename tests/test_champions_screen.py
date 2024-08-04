from unittest.mock import MagicMock, patch
import pytest

from screens import champions_screen  # Adjust this based on your actual path


# Mock configurations for layout, palette, and screens
class MockLayout:
    FRAME_PADDING_TOP = 6
    FRAME_PADDING_LEFT = 5
    FRAME_PADDING_BOTTOM = 3
    FRAME_PADDING_RIGHT = 5
    MAIN_TEXT_MARGIN_X = 20


class MockPalette:
    MAIN_COLOR = 1


class MockScreens:
    HOME_SCREEN = 0
    GAME_SCREEN = 1
    CHAMPIONS_SCREEN = 2
    OUTCOME_SCREEN = 3


# Updated mock data for champions
mock_champion_data = [
    ("Katya", 991, 1722270826),
    ("John", 895, 1722271509),
    ("Mark", 824, 1722292632),
    ("Alice", 783, 1722262478),
    ("Orla", 777, 1722267286)
]


# Mocking the necessary imports and configurations
@pytest.fixture(autouse=True)
def mock_imports_and_configs(monkeypatch):
    """
    This fixture automatically patches configuration settings, champion data
    retrieval, and spreadsheet storage interactions. It also mocks the SHEET
    object used in the `lib.spreadsheet_storage` module.
    """

    monkeypatch.setattr('config.layout', MockLayout)
    monkeypatch.setattr('config.palette', MockPalette)
    monkeypatch.setattr('config.screens', MockScreens)
    monkeypatch.setattr('components.champions.fetch_champions',
                        lambda: mock_champion_data)
    monkeypatch.setattr('screens.champions_screen.curses.color_pair',
                        lambda x: x)

    # Mock the SHEET object and the worksheet method
    mock_sheet = MagicMock()
    mock_worksheet = MagicMock()
    mock_worksheet.get_all_values.return_value = [
        ["name", "score", "timestamp"],  # Headers
        ["Katya", "991", 1722270826],
        ["John", "895", 1722271509],
        ["Mark", "824", 1722292632],
        ["Alice", "783", 1722262478],
        ["Orla", "777", 1722267286]
    ]
    mock_sheet.worksheet.return_value = mock_worksheet

    monkeypatch.setattr('lib.spreadsheet_storage.SHEET', mock_sheet)


def test_content_screen_handler():
    """
    The test verifies that `content_screen_handler` correctly handles user
    input and updates the screen. Specifically, it tests that pressing 'q' to
    quit results in the expected behavior.
    """

    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)
    stdscr.getch.side_effect = [ord('q')]  # Simulate pressing 'q' to quit

    navbar = MagicMock()
    navbar.update.return_value = (True, None)

    elements = [MagicMock()]
    data = mock_champion_data

    screen = champions_screen.content_screen_handler(stdscr, navbar,
                                                     elements, data)
    # Check that addstr was called (output is drawn)
    stdscr.addstr.assert_called()
    assert screen is None  # As 'q' returns None screen


def test_skeleton_screen_handler():
    """
    The test verifies that `skeleton_screen_handler` correctly retrieves and
    returns champion data for the screen. It ensures that the function returns
    the mock data and that the screen is refreshed.
    """

    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)

    navbar = MagicMock()
    elements = [MagicMock()]

    result = champions_screen.skeleton_screen_handler(stdscr, navbar, elements)
    assert result == mock_champion_data
    # Check that refresh was called (output is drawn)
    stdscr.refresh.assert_called()


@patch('screens.champions_screen.skeleton_screen_handler',
       return_value=mock_champion_data)
def test_champions_screen_handler(mock_skeleton_handler):
    """
    The test verifies that `champions_screen_handler` correctly handles
    user input and returns the expected result. Specifically, it checks that
    pressing 'q' results in quitting the screen.
    """

    stdscr = MagicMock()
    stdscr.getmaxyx.return_value = (20, 40)
    stdscr.getch.side_effect = [ord('q')]  # Simulate pressing 'q' to quit

    result = champions_screen.champions_screen_handler(stdscr)
    assert result is None  # Should return None when quitting


def test_on_load_champions_screen():
    """
    The test verifies that `on_load_champions_screen` correctly sets up
    the handler for the champions screen.
    """

    mock_w = MagicMock()
    mock_handler = MagicMock()

    # Ensure on_load_champions_screen sets the handler correctly
    wrapped_handler = champions_screen.on_load_champions_screen(mock_w)
    wrapped_handler(mock_handler)

    mock_w.assert_called_once_with(champions_screen.champions_screen_handler)
