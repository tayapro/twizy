import pytest
from unittest.mock import MagicMock, patch
from components.right_text import RightText

@patch('curses.initscr')
def test_right_text_draw(mock_initscr):
    # Mock stdscr
    mock_stdscr = MagicMock()
    mock_stdscr.getmaxyx.return_value = (20, 40)  # height = 20, width = 40

    # Create RightText instance
    message = "Hello"
    y = 5
    right_margin = 3
    right_text = RightText(message, y, right_margin)

    # Draw the text
    right_text.draw(mock_stdscr)

    # Expected position calculation
    expected_x = 40 - len(message) - right_margin

    # Assert addstr was called with correct parameters
    mock_stdscr.addstr.assert_called_once_with(y, expected_x, message)
