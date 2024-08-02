import pytest
from unittest.mock import MagicMock, patch
from components.text import Text

def test_text_draw():
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

