from unittest.mock import MagicMock, patch, ANY
import pytest
import re

from screens import champions_screen

class ReMatcher(str):
    def __init__(self, s):
        self.regex = re.compile(s)

    def __eq__(self, other):
        return self.regex.match(other)


# Including headers
mock_champion_data = [
    ("name", "score", "timestamp"),
    ("Katya", 991, 1722270826),
    ("John", 895, 1722271509),
    ("Mark", 824, 1722292632),
    ("Alice", 783, 1722262478),
    ("Orla", 777, 1722267286)
]

# Excluding headers
mock_champion_table = mock_champion_data[1:]

@pytest.fixture
def mock_color_pair(monkeypatch):
    mock_color = MagicMock(side_effect=lambda x: x)
    monkeypatch.setattr('screens.home_screen.curses.color_pair', mock_color)
    return mock_color


@pytest.fixture
def mock_stdscr():
    mock = MagicMock()
    mock.getmaxyx.return_value = (20, 40)
    return mock

@pytest.fixture
def mock_navbar():
    mock = MagicMock()
    mock.update.return_value = (True, None)
    return mock


@pytest.fixture
def mock_screen_elements():
    return MagicMock()
    

@pytest.fixture
def mock_skeleton_handler():
    return MagicMock(return_value=mock_champion_table)


@pytest.fixture
def mock_get_table(monkeypatch):
    """
    Fixture to mock the `get_table` function from `spreadsheet_storage`
    to return a predefined champions table.
    """
    mock = MagicMock(return_value=mock_champion_data)
    monkeypatch.setattr('lib.spreadsheet_storage.get_table', mock)
    return mock


@pytest.fixture
def mock_set_table(monkeypatch):
    """
    Fixture to mock the `set_table` function from `spreadsheet_storage`
    to prevent actual updates to the champions table.
    """
    m = MagicMock()
    monkeypatch.setattr('lib.spreadsheet_storage.set_table', m)
    return m


def test_content_screen_handler(mock_stdscr, mock_navbar, mock_screen_elements):
    """
    The test verifies that `content_screen_handler` correctly handles user
    input and updates the screen. Specifically, it tests that pressing 'q' to
    quit results in the expected behavior.
    """
    screen = champions_screen.content_screen_handler(mock_stdscr, mock_navbar,
                                                     mock_screen_elements, mock_champion_table)

    mock_stdscr.addstr.assert_any_call(10, 5, ReMatcher("^Katya\s+991$"))
    mock_stdscr.addstr.assert_any_call(11, 5, ReMatcher("^John\s+895$"))
    mock_stdscr.addstr.assert_any_call(12, 5, ReMatcher("^Mark\s+824$"))
    mock_stdscr.addstr.assert_any_call(13, 5, ReMatcher("^Alice\s+783$"))
    mock_stdscr.addstr.assert_any_call(14, 5, ReMatcher("^Orla\s+777$"))

    assert screen is None


def test_skeleton_screen_handler(mock_stdscr, mock_navbar, mock_screen_elements, mock_color_pair, mock_get_table):
    """
    The test verifies that `skeleton_screen_handler` correctly retrieves and
    returns champion data for the screen. It ensures that the function returns
    the mock data and that the screen is refreshed.
    """

    result = champions_screen.skeleton_screen_handler(mock_stdscr, mock_navbar, mock_screen_elements)
    assert result == mock_champion_table
    mock_stdscr.refresh.assert_called()


def test_champions_screen_handler(mock_stdscr, mock_color_pair, mock_get_table):
    """
    The test verifies that `champions_screen_handler` correctly handles
    user input and returns the expected result. Specifically, it checks that
    pressing 'q' results in quitting the screen.
    """

    mock_stdscr.getch.side_effect = [ord('q')]
    result = champions_screen.champions_screen_handler(mock_stdscr)
    assert result is None 


def test_on_load_champions_screen():
    """
    The test verifies that `on_load_champions_screen` correctly sets up
    the handler for the champions screen.
    """
    mock_w = MagicMock()
    mock_handler = MagicMock()

    wrapped_handler = champions_screen.on_load_champions_screen(mock_w)
    wrapped_handler(mock_handler)

    mock_w.assert_called_once_with(champions_screen.champions_screen_handler)
