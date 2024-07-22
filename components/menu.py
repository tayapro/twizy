import sys 
import curses

class Menu(object):
    cursor = 0

    def __init__(self, y, x, *args):
        self.y = y
        self.x = x
        self.options = args[:]


    def draw(self, stdscr):
        curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(11, curses.COLOR_BLACK, curses.COLOR_WHITE)
        normal = curses.color_pair(10)
        selected = curses.color_pair(11)

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