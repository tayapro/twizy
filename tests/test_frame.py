import sys
import os

# Ensure the correct path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
from components.frame import Frame
import curses

# # Define box-drawing characters for curses
setattr(curses, "ACS_VLINE", "|")
setattr(curses, "ACS_HLINE", "-")
setattr(curses, "ACS_ULCORNER", "+")
setattr(curses, "ACS_URCORNER", "+")
setattr(curses, "ACS_LRCORNER", "+")
setattr(curses, "ACS_LLCORNER", "+")

@patch('curses.textpad.rectangle')
def test_frame_draw(mock_rectangle):
    """
    Test that Frame.draw correctly draws a frame on the screen.

    This test verifies that the draw method of the Frame class uses
    the curses library to draw a rectangle with the expected dimensions
    and at the expected screen coordinates.
    """
    # Mock the stdscr object to simulate curses screen
    mock_stdscr = MagicMock()
    mock_stdscr.getmaxyx.return_value = (20, 40)  # Mock screen dimensions

    # Create a Frame instance with specific padding
    frame = Frame(padding_top_y=2, padding_top_x=3,
                  padding_bottom_y=4, padding_bottom_x=5)

    # Call the draw method, which should invoke curses methods
    frame.draw(mock_stdscr)

    # Verify that vertical and horizontal lines are drawn correctly
    mock_stdscr.vline.assert_any_call(3, 35, "|", 13)
    mock_stdscr.vline.assert_any_call(3, 3, "|", 13)
    mock_stdscr.hline.assert_any_call(16, 4, "-", 31)
    mock_stdscr.hline.assert_any_call(2, 4, "-", 31)

    # Verify that corners are drawn correctly
    mock_stdscr.addch.assert_any_call(2, 3, "+")
    mock_stdscr.addch.assert_any_call(2, 35, "+")
    mock_stdscr.addch.assert_any_call(16, 35, "+")
    mock_stdscr.addch.assert_any_call(16, 3, "+")
    
    # Verify that the rectangle function is called once with correct parameters
    mock_rectangle.assert_called_once_with(mock_stdscr, 2, 3, 16, 35)
