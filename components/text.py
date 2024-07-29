class Text(object):
    def __init__(self, message, y, x, *args):
        self.message = message
        self.y = y
        self.x = x
        self.args = args[:]

    def draw(self, stdscr):
        stdscr.addstr(self.y, self.x, self.message, *self.args)
