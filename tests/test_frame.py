import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock, patch
from ..components import frame
# from components.frame import Frame, rectangle, safe_acs_vline, safe_acs_hline
import curses

@patch('components.frame.curses.ACS_VLINE', '|')
@patch('components.frame.curses.ACS_HLINE', '-')
@patch('components.frame.rectangle', side_effect=frame.rectangle)
def test_frame_draw(mock_rectangle):
    # Mocking stdscr to return specific dimensions
    mock_stdscr = MagicMock()
    mock_stdscr.getmaxyx.return_value = (20, 40)  # height = 20, width = 40

    # Create a Frame instance
    f = frame.Frame(padding_top_y=2, padding_top_x=3,
                  padding_bottom_y=4, padding_bottom_x=5)

    # Call the draw method
    f.draw(mock_stdscr)

    # Assert rectangle was called with the correct parameters
    mock_rectangle.assert_called_once_with(mock_stdscr, 2, 3, 16, 35)

def test_safe_acs_vline():
    assert frame.safe_acs_vline() == '|'

def test_safe_acs_hline():
    assert frame.safe_acs_hline() == '-'
