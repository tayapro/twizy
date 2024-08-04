import pytest
from unittest.mock import MagicMock, patch
from components.text import Text


def test_text_draw():
    """
    The test creates an instance of the Text class and a mock stdscr object.
    It then calls the draw method and asserts that stdscr.addstr was called
    with the correct arguments (message, y, x).
    """

    # Create an instance of the Text class
    message = "Hello, World!"
    y = 5
    x = 10
    text = Text(message, y, x)

    # Create a mock stdscr object
    mock_stdscr = MagicMock()

    # Call the draw method
    text.draw(mock_stdscr)

    # Assert that stdscr.addstr was called with the correct arguments
    mock_stdscr.addstr.assert_called_once_with(y, x, message)


def test_text_draw_with_attributes():
    """
    The test creates an instance of the Text class with an extra attribute
    (attr), and a mock stdscr object. It then calls the draw method and
    asserts that stdscr.addstr was called with the correct arguments
    (message, y, x, attr).
    """

    # Create an instance of the Text class with additional attributes
    message = "Hello, World!"
    y = 5
    x = 10
    attr = 1  # Example attribute (e.g., curses.A_BOLD)
    text = Text(message, y, x, attr)

    # Create a mock stdscr object
    mock_stdscr = MagicMock()

    # Call the draw method
    text.draw(mock_stdscr)

    # Assert that stdscr.addstr was called with the correct arguments
    mock_stdscr.addstr.assert_called_once_with(y, x, message, attr)
