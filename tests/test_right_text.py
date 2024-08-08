import pytest

from components import right_text


@pytest.fixture
def right_text_instance():
    """
    Fixture to create an instance of the `RightText` component with a simple
    message and screen positions.
    """
    return right_text.RightText("Hello", 5, 3)


def test_right_text_draw(mock_stdscr, right_text_instance):
    right_text_instance.draw(mock_stdscr)

    mock_stdscr.getmaxyx.assert_called_once()

    expected_x = 40 - len("Hello") - 3
    mock_stdscr.addstr.assert_called_once_with(5, expected_x, "Hello")
