class RightText(object):
    """
    A class for displaying text aligned to the right side of the screen on a curses screen.

    Attributes:
        message (str): The text message to display.
        y (int): The y-coordinate (row) where the text should be displayed.
        right_marging (int): The margin from the right edge of the screen.
        args (tuple): Additional arguments for styling or formatting the text.
    """
    def __init__(self, message, y, right_marging, *args):
        """
        Initializes a new instance of RightText.
        """
        self.message = message
        self.y = y
        self.right_marging = right_marging
        self.args = args[:]

    def draw(self, stdscr):
        """
        Draw the text aligned to the right on the given curses screen.
        """
        if len(self.message) > 0:
            height, width = stdscr.getmaxyx()
            x = width - len(self.message) - self.right_marging
            stdscr.addstr(self.y, x, self.message, *self.args)
