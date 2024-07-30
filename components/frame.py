from curses.textpad import rectangle
from config import layout
import curses


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
                  height - self.padding_bottom_y,
                  width - self.padding_bottom_x)

def safe_acs_vline():
    try:
        return curses.ACS_VLINE
    except AttributeError:
        return '|'

def safe_acs_hline():
    try:
        return curses.ACS_HLINE
    except AttributeError:
        return '-'

def rectangle(win, uly, ulx, lry, lrx):
    """Draw a rectangle with corners at the provided upper-left
    and lower-right coordinates.
    """
    vline = safe_acs_vline()
    hline = safe_acs_hline()

    win.vline(uly + 1, ulx, vline, lry - uly - 1)
    win.hline(uly, ulx + 1, hline, lrx - ulx - 1)
    win.hline(lry, ulx + 1, hline, lrx - ulx - 1)
    win.vline(uly + 1, lrx, vline, lry - uly - 1)
    win.addch(uly, ulx, curses.ACS_ULCORNER)
    win.addch(uly, lrx, curses.ACS_URCORNER)
    win.addch(lry, lrx, curses.ACS_LRCORNER)
    win.addch(lry, ulx, curses.ACS_LLCORNER)