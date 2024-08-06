import pytest
from unittest.mock import MagicMock
from components import centered_text


@pytest.fixture
def mock_stdscr():
    """
    Fixture to create a mocked `stdscr` object for testing.
    """
    mock = MagicMock()
    mock.getmaxyx.return_value = (10, 40)
    return mock


@pytest.fixture
def centered_text_instance():
    """
    Fixture to create an instance of `CenteredText` with a sample message 
    and vertical position for testing.
    """
    return centered_text.CenteredText("Hello", 5)


def test_centered_text_draw(mock_stdscr, centered_text_instance):
    """
    The test verifies that the `draw` method correctly calculates the position
    of the text to be centered horizontally on the screen at the specified
    vertical position (`y`), and then calls `addstr` with the correct
    parameters.
    """
    centered_text_instance.draw(mock_stdscr)

    mock_stdscr.getmaxyx.assert_called_once()

    expected_x = 40 // 2 - len("Hello") // 2
    mock_stdscr.addstr.assert_called_once_with(5, expected_x, "Hello")
