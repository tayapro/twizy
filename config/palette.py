import curses


MAIN_COLOR = 1
MAIN_COLOR_INV = 2
ACCENT_COLOR = 3
ACCENT_COLOR_INV = 4


def init_colors():
    def handle_colors(stdscr):
        curses.init_pair(MAIN_COLOR, curses.COLOR_WHITE,
                         curses.COLOR_BLACK)
        curses.init_pair(MAIN_COLOR_INV, curses.COLOR_BLACK,
                         curses.COLOR_WHITE)

        curses.init_pair(ACCENT_COLOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(ACCENT_COLOR_INV, curses.COLOR_YELLOW,
                         curses.COLOR_BLACK)
    curses.wrapper(handle_colors)
