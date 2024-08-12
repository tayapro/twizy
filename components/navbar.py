import curses

from config import palette


class NavAction(object):
    """
    Represents an individual navigation action in a navbar.

    Attributes:
        key (str): The key to trigger the action.
        screen (any): The screen or function to navigate to.
        message (str): The display message for this action.
    """

    def __init__(self, key, screen, message):
        """
        Initializes a new instance of NavAction.
        """
        self.key = key
        self.screen = screen
        self.message = message

    def text(self):
        """
        Generate the display text for the navigation action.
        """
        return f"{self.key}) {self.message}"

    def test_key(self, key):
        """
        Check if the provided key matches the action's key.
        """
        if key == ord(self.key):
            return True

        return False


class Navbar(object):
    """
    Represents a navigation bar containing multiple navigation actions.

    Attributes:
        actions (list): A list of NavAction objects.
        message (str): The combined message of all actions.
    """

    def __init__(self, *args):
        """
        Initializes a new instance of Navbar.
        """
        if len(args) == 0:
            raise Exception("Invalid args")

        self.actions = args[:]
        self.message = ""
        for action in args:
            self.message = self.message + " " + action.text()

    def draw(self, stdscr):
        """
        Draw the navigation bar on the screen.
        """
        color = curses.color_pair(palette.ACCENT_COLOR)
        height, width = stdscr.getmaxyx()

        # Draw two empty lines at the top of the screen, covering rows 0 and 1
        # Start from the left edge (x = 0)
        stdscr.addstr(0, 0, " " * width, color)
        stdscr.addstr(1, 0, " " * width, color)

        # Draw the application title on 1 row, starts from left edge (x = 0)
        stdscr.addstr(1, 0, "  tWIZY", color | curses.A_BOLD)

        # Draw the navigation options
        nav_str = self.message + "  "
        stdscr.addstr(1, width - len(nav_str), nav_str, color)

        # Draw an empty line below the navbar at 2 row(y = 2) from
        # left edge (x = 0)
        stdscr.addstr(2, 0, " " * width, color)

    def update(self, stdscr, character):
        """
        Update the navbar based on user input.
        The function returns tuple: (bool, any) where the bool indicates
        if a change should occur, and 'any' is the screen to navigate
        to (if any).
        """
        # Check each action to see if the input character matches
        # an action key
        for action in self.actions:
            change = action.test_key(character)
            if change:
                return True, action.screen

        return False, None
