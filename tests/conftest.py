import pytest
from unittest.mock import MagicMock

from config import screens
from screens.home_screen import home_screen_handler


# Mock data for the logo
mock_logo = """
  +---------+
  | tWIZY   |
  +---------+
"""


@pytest.fixture
def mock_twizy_logo():
    """
    Fixture to provide a mock representation of the tWIZY logo.
    """
    return mock_logo


# Including headers
mock_table = [
    ("name", "score", "timestamp"),
    ("Katya", 991, 1722270826),
    ("John", 895, 1722271509),
    ("Mark", 824, 1722292632),
    ("Alice", 783, 1722262478),
    ("Orla", 777, 1722267286)
]


@pytest.fixture
def mock_champion_table():
    """
    Fixture to provide a mock champions table.
    """
    return mock_table


@pytest.fixture
def mock_init_colors(monkeypatch):
    """
    Fixture to mock the `init_colors` function from `palette`.
    """
    mock = MagicMock()
    monkeypatch.setattr('config.palette.init_colors', mock)
    return mock


@pytest.fixture
def mock_color_pair(monkeypatch):
    """
    Fixture to mock the `curses.color_pair` function.
    """
    mock_color = MagicMock(side_effect=lambda x: x)
    monkeypatch.setattr('curses.color_pair', mock_color)
    return mock_color


@pytest.fixture
def mock_stdscr():
    """
    Fixture to provide a mock `stdscr` object.
    """
    mock = MagicMock()
    mock.getmaxyx.return_value = (20, 40)
    return mock


@pytest.fixture
def mock_navbar():
    """
    Fixture to provide a mock navbar object.
    """
    mock = MagicMock()
    mock.update.return_value = (True, None)
    return mock


@pytest.fixture
def mock_screen_elements():
    """
    Fixture to provide a mock for screen elements.
    """
    return MagicMock()


@pytest.fixture
def mock_skeleton_handler():
    """
    Fixture to provide a mock skeleton handler function.
    """
    return MagicMock(return_value=mock_table[1:])


@pytest.fixture
def mock_init_storage(monkeypatch):
    """
    Fixture to mock the `init_storage` function from `spreadsheet_storage`.
    """
    mock = MagicMock()
    monkeypatch.setattr('lib.spreadsheet_storage.init_storage', mock)
    return mock


@pytest.fixture
def mock_get_table(monkeypatch):
    """
    Fixture to mock the `get_table` function from `spreadsheet_storage`
    to return a predefined champions table.
    """
    mock = MagicMock(return_value=mock_table)
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


@pytest.fixture
def mock_localstorage_get_item(monkeypatch):
    """
    Fixture to mock the `get_item` function from `local_storage`.
    """
    mock = MagicMock(return_value="TestUser")
    monkeypatch.setattr('lib.local_storage.get_item', mock)
    return mock


@pytest.fixture
def mock_localstorage_set_item(monkeypatch):
    """
    Fixture to mock the `set_item` function from `local_storage`.
    """
    mock = MagicMock()
    monkeypatch.setattr('lib.local_storage.set_item', mock)
    return mock


@pytest.fixture
def mock_localstorage_clear(monkeypatch):
    """
    Fixture to mock the `clear` function from `local_storage`.
    """
    mock = MagicMock()
    monkeypatch.setattr('lib.local_storage.clear', mock)
    return mock
