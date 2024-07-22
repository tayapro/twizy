from consts import screens
import curses

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
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        YELLOW_AND_BLACK = curses.color_pair(2)
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, " " * width, YELLOW_AND_BLACK)
        stdscr.addstr(0, 0, "  tWIZY", YELLOW_AND_BLACK)
        nav_str = self.message + "  "
        stdscr.addstr(0, width - len(nav_str), nav_str, YELLOW_AND_BLACK)

    def update(self, stdscr, character):
        for action in self.actions:
            change = action.test_key(character)
            if change:
                return True, action.screen

        return False, None