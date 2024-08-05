import pytest
from unittest import mock
from config import palette


@pytest.fixture
def mock_curses():
    """
    Fixture to mock functions and constants from the curses module.

    This fixture replaces certain functions and constants from the `curses`
    module with mock objects to prevent actual terminal interactions during
    tests. The mocked `curses` functions include `init_pair` for color pair
    initialization, and `curses.wrapper` to simulate the curses initialization
    function.
    """
    #Fixture to mock curses module functions
    with mock.patch('curses.init_pair') as mock_init_pair, \
         mock.patch('curses.COLOR_WHITE', new=15), \
         mock.patch('curses.COLOR_BLACK', new=0), \
         mock.patch('curses.COLOR_YELLOW', new=3), \
         mock.patch('curses.wrapper') as mock_wrapper:

        yield {
            'init_pair': mock_init_pair,
            'wrapper': mock_wrapper
        }


def test_init_colors(mock_curses):
    """
    The test verifies that the `init_colors` function correctly initializes
    color pairs using `curses.init_pair` with the appropriate color values.
    It also ensures that the `curses.wrapper` function is called with
    a function that initializes the colors.
    """
    # Mock stdscr
    mock_stdscr = mock.Mock()

    # Call the function
    palette.init_colors()

    # Check if `curses.wrapper` was called with a function
    mock_curses['wrapper'].assert_called_once()
    handle_colors_func = mock_curses['wrapper'].call_args[0][0]

    # Call the passed function with a mock stdscr
    handle_colors_func(mock_stdscr)

    # Verify that init_pair is called with the expected color pairs
    mock_curses['init_pair'].assert_any_call(palette.MAIN_COLOR, 15, 0)
    mock_curses['init_pair'].assert_any_call(palette.MAIN_COLOR_INV, 0, 15)
    mock_curses['init_pair'].assert_any_call(palette.ACCENT_COLOR, 0, 3)
    mock_curses['init_pair'].assert_any_call(palette.ACCENT_COLOR_INV, 3, 0)
