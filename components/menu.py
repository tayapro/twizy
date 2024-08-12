import sys
import curses

from curses.textpad import rectangle
from config import palette


class Menu(object):
    """
    A class to represent a menu interface in a curses-based application.

    Attributes:
        y (int): The y-coordinate of the top-left corner of the menu.
        x (int): The x-coordinate of the top-left corner of the menu.
        title (str): The title displayed above the menu options.
        show_numbers (bool): Flag indicating whether to show option numbers.
        options (list): A list of strings representing the menu options.
        cursor (int): The current position of the cursor in the menu.
    """
    cursor = 0

    def __init__(self, y, x, title, show_numbers, *args):
        """
        Initializes a new instance of Menu.
        """
        self.y = y
        self.x = x
        self.title = title
        self.show_numbers = show_numbers
        self.options = args[:]

    def set_options(self, *args):
        """
        Set new options for the menu and reset the cursor.
        """
        self.cursor = 0
        self.options = args[:]

    def get_selection(self):
        """
        Get the index of the currently selected option.
        """
        return self.cursor

    def draw(self, stdscr):
        """
        Draw the menu on the given curses screen.
        """
        normal = curses.color_pair(palette.MAIN_COLOR)
        selected = curses.color_pair(palette.MAIN_COLOR_INV)

        padding = 0

        # Draw the title if it exists
        if len(self.title) > 0:
            stdscr.addstr(self.y, self.x, self.title)
            padding = 1

        # Draw each option with appropriate highlighting
        for index, opt in enumerate(self.options):
            text = f"{index+1}. {opt}" if self.show_numbers else opt
            stdscr.addstr(self.y + index + padding, self.x, text,
                          selected if self.cursor == index else normal)

    def update(self, code):
        """
        Update the cursor position based on user input.
        """
        if code == curses.KEY_UP:
            self.cursor -= 1
        if code == curses.KEY_DOWN:
            self.cursor += 1

        # Wrap around the cursor if it goes out of bounds
        if self.cursor < 0:
            self.cursor = len(self.options) - 1
        elif self.cursor >= len(self.options):
            self.cursor = 0
