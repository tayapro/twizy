import sys 
import curses
from curses.textpad import rectangle  
from config import palette

class Menu(object):
    cursor = 0

    def __init__(self, y, x, title, show_numbers, *args):
        self.y = y
        self.x = x
        self.title = title
        self.show_numbers = show_numbers
        self.options = args[:]

    def set_options(self, *args):
        self.cursor = 0
        self.options = args[:]

    def get_selection(self):
        return self.cursor

    def draw(self, stdscr):
        normal = curses.color_pair(palette.MAIN_COLOR)
        selected = curses.color_pair(palette.MAIN_COLOR_INV)

        padding = 0

        if len(self.title) > 0:
            stdscr.addstr(self.y, self.x, self.title)
            padding = 1

        for index, opt in enumerate(self.options):
            text = f"{index+1}. {opt}" if self.show_numbers else opt
            stdscr.addstr(self.y + index + padding, self.x, text, selected if self.cursor == index else normal)

    def update(self, code):
        if code == curses.KEY_UP:
            self.cursor -= 1
        if code == curses.KEY_DOWN:
            self.cursor += 1

        if self.cursor < 0:
            self.cursor = len(self.options) - 1
        elif self.cursor >= len(self.options):
            self.cursor = 0