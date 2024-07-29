class CenteredText(object):
    def __init__(self, message, y, *args):
        self.message = message
        self.y = y
        self.args = args[:]

    def draw(self, stdscr):
        height, width = stdscr.getmaxyx()
        x = width // 2 - len(self.message) // 2
        stdscr.addstr(self.y, x, self.message, *self.args)
