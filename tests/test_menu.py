import pytest
import curses
from unittest.mock import MagicMock, patch
from components.menu import Menu

# Mocking palette attributes for testing
class MockPalette:
    MAIN_COLOR = 1
    MAIN_COLOR_INV = 2

palette = MockPalette()

@patch('config.palette', palette)  # Mocking the palette from config
@patch('curses.color_pair')
def test_menu_draw(mock_color_pair):
    # Mock return values for color pairs
    mock_color_pair.side_effect = [10, 20]  # Normal and selected colors

    # Set up the menu
    title = "Main Menu"
    options = ["Option 1", "Option 2", "Option 3"]
    show_numbers = True
    menu = Menu(5, 10, title, show_numbers, *options)

    # Mock stdscr
    mock_stdscr = MagicMock()

    # Draw the menu
    menu.draw(mock_stdscr)

    # Assertions for title
    mock_stdscr.addstr.assert_any_call(5, 10, title)

    # Assertions for options
    expected_calls = [
        ((6, 10, "1. Option 1", 20),),  # Selected (cursor == 0)
        ((7, 10, "2. Option 2", 10),),  # Normal
        ((8, 10, "3. Option 3", 10),),  # Normal
    ]
    mock_stdscr.addstr.assert_has_calls(expected_calls, any_order=False)

def test_menu_update():
    options = ["Option 1", "Option 2", "Option 3"]
    menu = Menu(5, 10, "", False, *options)

    # Initially cursor should be 0
    assert menu.get_selection() == 0

    # Simulate down key press
    menu.update(curses.KEY_DOWN)
    assert menu.get_selection() == 1

    # Simulate another down key press
    menu.update(curses.KEY_DOWN)
    assert menu.get_selection() == 2

    # Simulate down key press (should wrap around)
    menu.update(curses.KEY_DOWN)
    assert menu.get_selection() == 0

    # Simulate up key press (should wrap around)
    menu.update(curses.KEY_UP)
    assert menu.get_selection() == 2

    # Simulate up key press
    menu.update(curses.KEY_UP)
    assert menu.get_selection() == 1
