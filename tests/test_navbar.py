import pytest
import curses

from unittest.mock import MagicMock, patch
from components.navbar import Navbar, NavAction


def test_navbar_draw(mock_stdscr, mock_color_pair):
    """
    The test verifies that the `draw` method correctly renders the navbar
    on the screen.
    It checks that the background color and text are displayed as expected.
    """
    mock_color_pair.side_effect = [10]

    action1 = NavAction(key='a', screen='screen1', message='Action 1')
    action2 = NavAction(key='b', screen='screen2', message='Action 2')

    navbar = Navbar(action1, action2)
    navbar.draw(mock_stdscr)

    mock_stdscr.addstr.assert_any_call(0, 0, ' ' * 40, 10)
    mock_stdscr.addstr.assert_any_call(1, 0, ' ' * 40, 10)
    mock_stdscr.addstr.assert_any_call(1, 0, '  tWIZY', 10 | curses.A_BOLD)

    expected_nav_text = ' a) Action 1 b) Action 2  '
    # Calculate the correct starting x position
    expected_x_pos = 40 - len(expected_nav_text)

    # Assertions for options text and background color
    mock_stdscr.addstr.assert_any_call(1, expected_x_pos,
                                       expected_nav_text, 10)
    mock_stdscr.addstr.assert_any_call(2, 0, ' ' * 40, 10)


def test_navbar_update(mock_stdscr):
    """
    The test verifies that the `update` method correctly processes key inputs
    and returns the appropriate result and screen.
    """
    action1 = NavAction(key='a', screen='screen1', message='Action 1')
    action2 = NavAction(key='b', screen='screen2', message='Action 2')

    navbar = Navbar(action1, action2)

    # Test for key 'a'
    result, screen = navbar.update(mock_stdscr, ord('a'))
    assert result is True
    assert screen == 'screen1'

    # Test for key 'b'
    result, screen = navbar.update(mock_stdscr, ord('b'))
    assert result is True
    assert screen == 'screen2'

    # Test for key 'u' (not defined in actions)
    result, screen = navbar.update(mock_stdscr, ord('u'))
    assert result is False
    assert screen is None
