import pytest

from components.frame import Frame


def test_frame_draw(mock_stdscr):
    """
    Test that the `draw` method of the `Frame` class correctly draws a frame
    on the provided `stdscr` mock object. The test verifies that the frame's
    border lines and corners are drawn with the correct characters at the
    appropriate positions.
    """
    frame = Frame(padding_top_y=2, padding_top_x=3,
                  padding_bottom_y=4, padding_bottom_x=5)

    frame.draw(mock_stdscr)

    mock_stdscr.vline.assert_any_call(3, 35, "|", 13)
    mock_stdscr.vline.assert_any_call(3, 3, "|", 13)
    mock_stdscr.hline.assert_any_call(16, 4, "-", 31)
    mock_stdscr.hline.assert_any_call(2, 4, "-", 31)

    mock_stdscr.addch.assert_any_call(2, 3, "+")
    mock_stdscr.addch.assert_any_call(2, 35, "+")
    mock_stdscr.addch.assert_any_call(16, 35, "+")
    mock_stdscr.addch.assert_any_call(16, 3, "+")
