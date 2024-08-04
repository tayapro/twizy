import curses


# Define color pair IDs for use in the UI
MAIN_COLOR = 1
MAIN_COLOR_INV = 2
ACCENT_COLOR = 3
ACCENT_COLOR_INV = 4


def init_colors():
    """
    Initialize color pairs for the UI.

    This function sets up color pairs using the curses library, which can be
    used to style text in the terminal. The color pairs are defined globally
    and include both regular and inverse color schemes for the main and
    accent colors.
    """
    def handle_colors(stdscr):
        """
        Configure color pairs for curses.

        Args:
            stdscr: The main screen object from curses for drawing on the
            terminal.
        """
        curses.init_pair(MAIN_COLOR, curses.COLOR_WHITE,
                         curses.COLOR_BLACK)
        curses.init_pair(MAIN_COLOR_INV, curses.COLOR_BLACK,
                         curses.COLOR_WHITE)

        curses.init_pair(ACCENT_COLOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(ACCENT_COLOR_INV, curses.COLOR_YELLOW,
                         curses.COLOR_BLACK)
    curses.wrapper(handle_colors)
