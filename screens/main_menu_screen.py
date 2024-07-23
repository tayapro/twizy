import curses
from config import consts
from components.navbar import Navbar, NavAction
from components.menu import Menu
from config import palette

def main_menu_screen_handler(stdscr):
    curses.noecho()           # Prevent input from displaying in the screen
    curses.curs_set(0)        # Cursor invisible (0)

    height, width = stdscr.getmaxyx()

    navbar = Navbar(
        NavAction("h", consts.HOME_SCREEN, "Home"),
        NavAction("m", consts.MAIN_MENU_SCREEN, "Menu"),
        NavAction("q", None, "Quit")
    )

    menu = Menu(height//2 - 2, width//2, "MENU", "Game", "Champions board", "Quit")

    while True:
        # Clear screen
        stdscr.clear()
        navbar.draw(stdscr)
        menu.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        menu.update(character)

        change, screen = navbar.update(stdscr, character)
        if change:
            return screen 


def on_load_main_menu_screen(w):
    return w(main_menu_screen_handler)