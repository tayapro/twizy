import curses
from config import palette

class NavAction(object):
    def __init__(self, key, screen, message):
        self.key = key
        self.screen = screen
        self.message = message

    def text(self):
        return f"{self.key}) {self.message}"

    def test_key(self, key):
        if key == ord(self.key):
            return True

        return False

class Navbar(object):
    def __init__(self, *args):
        if len(args) == 0:
            raise Exception("Invalid args")

        self.actions = args[:]
        self.message = ""
        for action in args:
            self.message = self.message + " " + action.text()

    def draw(self, stdscr):
        color = curses.color_pair(palette.ACCENT_COLOR)
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, " " * width, color)
        stdscr.addstr(1, 0, " " * width, color)
        stdscr.addstr(1, 0, "  tWIZY", color | curses.A_BOLD)
        nav_str = self.message + "  "
        stdscr.addstr(1, width - len(nav_str), nav_str, color)
        stdscr.addstr(2, 0, " " * width, color)

    def update(self, stdscr, character):
        for action in self.actions:
            change = action.test_key(character)
            if change:
                return True, action.screen

        return False, None