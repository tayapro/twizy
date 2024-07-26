from curses.textpad import rectangle
from config import layout

class Frame(object):
    def __init__(self, padding_x, padding_y, *args):
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.args = args[:]


    def draw(self, stdscr):
        height, width = stdscr.getmaxyx()
        rectangle(stdscr, self.padding_y, self.padding_x, 
                  height - self.padding_y, width - self.padding_x)