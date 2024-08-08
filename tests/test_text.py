import pytest

from components import text


@pytest.fixture
def text_instance():
    """
    Fixture to create an instance of the `Text` component with a simple message
    and coordinates.
    """
    return text.Text("Hello", 5, 10)


def test_text_draw(mock_stdscr, text_instance):
    """
    Test the `draw` method of the `Text` component to verify that it correctly
    renders the text on the screen at the specified coordinates.
    """
    text_instance.draw(mock_stdscr)

    mock_stdscr.addstr.assert_called_once_with(5, 10, "Hello")


@pytest.fixture
def text_with_attribute_instance():
    """
    Fixture to create an instance of the `Text` component with a message,
    coordinates, and additional text attributes.
    """
    return text.Text("Hello", 5, 10, 1)


def test_text_draw_with_attributes(mock_stdscr, text_with_attribute_instance):
    """
    Test the `draw` method of the `Text` component with attributes to verify
    that it correctly renders the text with the specified attributes on the
    screen at the given coordinates.
    """
    text_with_attribute_instance.draw(mock_stdscr)

    mock_stdscr.addstr.assert_called_once_with(5, 10, "Hello", 1)
