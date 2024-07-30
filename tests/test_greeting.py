import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import MagicMock
from components.greeting import Greeting

def test_greeting_draw():
    # Set up the test data
    message = "Hello, World!"
    y = 5
    x = 10
    attr = 0  # No special attributes

    # Create a Greeting instance
    greeting = Greeting(message, y, x, attr)

    # Create a mock stdscr object
    mock_stdscr = MagicMock()

    # Call the draw method
    greeting.draw(mock_stdscr)

    # Verify that addstr was called with the correct parameters
    mock_stdscr.addstr.assert_called_once_with(y, x, message, attr)
