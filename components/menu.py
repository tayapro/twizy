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

    def draw(self, stdscr):
        normal = curses.color_pair(palette.MAIN_COLOR)
        selected = curses.color_pair(palette.MAIN_COLOR_INV)

        rectangle(stdscr, 10, 30, 20, 90)
        stdscr.addstr(10, 15, self.title)

        for index, opt in enumerate(self.options):
            print(f"{self.cursor} -- {self.y} -- {self.x} -- {index} -- {opt}", file=sys.stderr)
            stdscr.addstr(self.y + index, self.x, opt, selected if self.cursor == index else normal)

    def update(self, character):
        if character == ord('o'):
            self.cursor -= 1
        elif character == ord('l'):
            self.cursor += 1

        print(f"{self.cursor}", file=sys.stderr)


        if self.cursor < 0:
            self.cursor = len(self.options) - 1
        elif self.cursor >= len(self.options):
            self.cursor = 0