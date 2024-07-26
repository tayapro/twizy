class RightText(object):
    def __init__(self, message, y, right_marging, *args):
        self.message = message
        self.y = y
        self.right_marging = right_marging
        self.args = args[:]

    def draw(self, stdscr):
        height, width = stdscr.getmaxyx()
        x = width - len(self.message) - self.right_marging
        stdscr.addstr(self.y, x, self.message, *self.args)