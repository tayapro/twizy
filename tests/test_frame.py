import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch, call
from components.frame import Frame
import curses
from curses import textpad

setattr(curses, "ACS_VLINE", "|")
setattr(curses, "ACS_HLINE", "-")
setattr(curses, "ACS_ULCORNER", "+")
setattr(curses, "ACS_URCORNER", "+")
setattr(curses, "ACS_LRCORNER", "+")
setattr(curses, "ACS_LLCORNER", "+")


@patch('curses.textpad.rectangle')
def test_frame_draw(mock_rectangle):
    # Mocking stdscr to return specific dimensions
    mock_stdscr = MagicMock()
    mock_stdscr.getmaxyx.return_value = (20, 40)  # height = 20, width = 40

    # Create a Frame instance
    frame = Frame(padding_top_y=2, padding_top_x=3,
                  padding_bottom_y=4, padding_bottom_x=5)

    # Call the draw method
    frame.draw(mock_stdscr)

    mock_stdscr.vline.assert_any_call(3, 35, "|", 13)
    mock_stdscr.vline.assert_any_call(3, 3, "|", 13)
    mock_stdscr.hline.assert_any_call(16, 4, "-", 31)
    mock_stdscr.hline.assert_any_call(2, 4, "-", 31)
    mock_stdscr.addch.assert_any_call(2, 3, "+")
    mock_stdscr.addch.assert_any_call(2, 35, "+")
    mock_stdscr.addch.assert_any_call(16, 35, "+")
    mock_stdscr.addch.assert_any_call(16, 3, "+")


    





    # mock_stdscr.hline.assert_called_with(3, 35, "|", 13)
    # mock_stdscr.vline.assert_called_with(3, 3, "|", 13)
    # mock_rectangle.assert_called_once_with(mock_stdscr, 2, 3, 16, 35)
