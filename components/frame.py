import curses
from curses.textpad import rectangle

from config import layout


class Frame(object):
    """
    A class to represent a frame on the screen.

    The Frame class draws a rectangular frame on a curses window with specified
    padding from the top, bottom, left, and right edges of the screen.

    Attributes:
        padding_top_y (int): The padding from the top edge.
        padding_top_x (int): The padding from the left edge.
        padding_bottom_y (int): The padding from the bottom edge.
        padding_bottom_x (int): The padding from the right edge.
        args (tuple): Additional arguments (if needed).
    """
    def __init__(self, padding_top_y, padding_top_x,
                 padding_bottom_y, padding_bottom_x, *args):
        """
        Initializes a new instance of Frame.
        """
        self.padding_top_y = padding_top_y
        self.padding_top_x = padding_top_x
        self.padding_bottom_y = padding_bottom_y
        self.padding_bottom_x = padding_bottom_x
        self.args = args[:]

    def draw(self, stdscr):
        """
        Draws the frame on the given curses window.

        Args:
            stdscr (curses.window): The curses window object where
                                    the frame will be drawn.
        """
        height, width = stdscr.getmaxyx()
        rectangle(stdscr, self.padding_top_y, self.padding_top_x,
                  height - self.padding_bottom_y,
                  width - self.padding_bottom_x)
