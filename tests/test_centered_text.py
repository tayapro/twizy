import pytest
from unittest.mock import MagicMock
from components import centered_text


@pytest.fixture
def mock_stdscr():
    """
    Fixture to create a mocked `stdscr` object for testing.
    """

    # Create a mock stdscr object
    mock = MagicMock()
    mock.getmaxyx.return_value = (10, 40)  # Mock screen height and width
    return mock


def test_centered_text_draw(mock_stdscr):
    """
    The test verifies that the `draw` method correctly calculates the position
    of the text to be centered horizontally on the screen at the specified
    vertical position (`y`), and then calls `addstr` with the correct
    parameters.
    """

    # Instantiate CenteredText
    message = "Hello"
    y = 5
    text = centered_text.CenteredText(message, y)

    # Call the draw method
    text.draw(mock_stdscr)

    # Assert getmaxyx was called to get screen size
    mock_stdscr.getmaxyx.assert_called_once()

    # Calculate expected x position
    expected_x = 40 // 2 - len(message) // 2

    # Assert addstr was called with correct parameters
    mock_stdscr.addstr.assert_called_once_with(y, expected_x, message)
