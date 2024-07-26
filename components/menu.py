import sys 
import curses
from curses.textpad import rectangle  
from config import palette

class Menu(object):
    cursor = 0

    def __init__(self, y, x, title, *args):
        self.y = y
        self.x = x
        self.options = args[:]
        self.title = title

    def set_options(self, *args):
        self.cursor = 0
        self.options = args[:]

    def get_selection(self):
        return self.options[self.cursor]

    def draw(self, stdscr):
        normal = curses.color_pair(palette.MAIN_COLOR)
        selected = curses.color_pair(palette.MAIN_COLOR_INV)

        padding = 0

        if len(self.title) > 0:
            stdscr.addstr(self.y, self.x, self.title)
            padding = 1

        for index, opt in enumerate(self.options):
            stdscr.addstr(self.y + index + padding, self.x, opt, selected if self.cursor == index else normal)

    def update(self, character):
        if character == ord('o'):
            self.cursor -= 1
        elif character == ord('l'):
            self.cursor += 1

        if self.cursor < 0:
            self.cursor = len(self.options) - 1
        elif self.cursor >= len(self.options):
            self.cursor = 0