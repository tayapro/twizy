class Text(object):
    """
    A class for displaying text on a curses screen.

    Attributes:
        message (str): The text message to display.
        y (int): The y-coordinate (row) where the text should be displayed.
        x (int): The x-coordinate (column) where the text should be displayed.
        args (tuple): Additional arguments for styling or formatting the text.
    """
    def __init__(self, message, y, x, *args):
        """
        Initializes a new instance of Text.
        """
        self.message = message
        self.y = y
        self.x = x
        self.args = args[:]

    def draw(self, stdscr):
        """
        Draw the text on the given curses screen.
        """
        if len(self.message) > 0:
            stdscr.addstr(self.y, self.x, self.message, *self.args)
