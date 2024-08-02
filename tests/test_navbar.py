import pytest
import curses
from unittest.mock import MagicMock, patch
from components.navbar import Navbar, NavAction

# Mocking palette attributes for testing
class MockPalette:
    ACCENT_COLOR = 1

palette = MockPalette()

@patch('config.palette', palette)  # Mocking the palette from config
@patch('curses.color_pair')
def test_navbar_draw(mock_color_pair):
    # Mock return values for color pairs
    mock_color_pair.return_value = 10

    # Create NavAction instances
    action1 = NavAction(key='a', screen='screen1', message='Action 1')
    action2 = NavAction(key='b', screen='screen2', message='Action 2')

    # Create Navbar instance
    navbar = Navbar(action1, action2)

    # Mock stdscr
    mock_stdscr = MagicMock()
    mock_stdscr.getmaxyx.return_value = (3, 40)  # height = 3, width = 40

    # Draw the navbar
    navbar.draw(mock_stdscr)

    # Assertions for background and text
    mock_stdscr.addstr.assert_any_call(0, 0, ' ' * 40, 10)  # background color
    mock_stdscr.addstr.assert_any_call(1, 0, ' ' * 40, 10)  # background color
    mock_stdscr.addstr.assert_any_call(1, 0, '  tWIZY', 10 | curses.A_BOLD)  # title

    # Adjust expected call to match the actual string and position used
    # Ensure the text is in the right position and matches the length of the string
    # Here, we assume `nav_str` starts at position width - len(nav_str)
    expected_nav_text = ' a) Action 1 b) Action 2  '
    expected_x_pos = 40 - len(expected_nav_text)  # Calculate the correct starting x position

    # Assertions for options text
    mock_stdscr.addstr.assert_any_call(1, expected_x_pos, expected_nav_text, 10)
    mock_stdscr.addstr.assert_any_call(2, 0, ' ' * 40, 10)  # background color

def test_navbar_update():
    # Create NavAction instances
    action1 = NavAction(key='a', screen='screen1', message='Action 1')
    action2 = NavAction(key='b', screen='screen2', message='Action 2')

    # Create Navbar instance
    navbar = Navbar(action1, action2)

    # Mock stdscr
    mock_stdscr = MagicMock()

    # Test for key 'a'
    result, screen = navbar.update(mock_stdscr, ord('a'))
    assert result is True
    assert screen == 'screen1'

    # Test for key 'b'
    result, screen = navbar.update(mock_stdscr, ord('b'))
    assert result is True
    assert screen == 'screen2'

    # Test for key 'c' (not defined in actions)
    result, screen = navbar.update(mock_stdscr, ord('c'))
    assert result is False
    assert screen is None

