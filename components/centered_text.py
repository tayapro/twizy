class CenteredText(object):
    """
    A class for displaying centered text on a curses screen.

    Attributes:
        message (str): The text message to display.
        y (int): The vertical position (y-coordinate) on the screen
        where the text will be displayed.
        args (tuple): Additional arguments for the curses addstr method,
        such as color attributes.
    """
    def __init__(self, message, y, *args):
        """
        Initializes a new instance of CenteredText.
        """
        self.message = message
        self.y = y
        self.args = args[:]

    def draw(self, stdscr):
        """
        Draws the centered text on the given curses window.

        This method calculates the horizontal position (x-coordinate)
        to center the text on the screen, then draws the text using
        the curses library.

        Args:
            stdscr (curses.window): The curses window object on which
            to draw the text.
        """
        if len(self.message) > 0:
            height, width = stdscr.getmaxyx()
            x = width // 2 - len(self.message) // 2
            stdscr.addstr(self.y, x, self.message, *self.args)
