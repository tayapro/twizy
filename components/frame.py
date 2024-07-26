from curses.textpad import rectangle
from config import layout

class Frame(object):
    def __init__(self, padding_top_y, padding_top_x, 
                padding_bottom_y, padding_bottom_x, *args):
        self.padding_top_y = padding_top_y
        self.padding_top_x = padding_top_x
        self.padding_bottom_y = padding_bottom_y
        self.padding_bottom_x = padding_bottom_x
        self.args = args[:]


    def draw(self, stdscr):
        height, width = stdscr.getmaxyx()
        rectangle(stdscr, self.padding_top_y, self.padding_top_x, 
                  height - self.padding_bottom_y, width - self.padding_bottom_x)