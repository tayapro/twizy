import curses
from consts import screens
from components.navbar import Navbar, NavAction
from components.menu import Menu

def main_menu_screen_handler(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    BLUE_AND_CYAN = curses.color_pair(1)
    YELLOW_AND_BLACK = curses.color_pair(2)
    height, width = stdscr.getmaxyx()

    navbar = Navbar(
        NavAction("h", screens.HOME_SCREEN, "Home"),
        NavAction("m", screens.MAIN_MENU_SCREEN, "Menu"),
        NavAction("q", None, "Quit")
    )

    menu = Menu(height//2 - 2, width//2, "Jabloki", "Fructi", "Kolbasa", "Producti")

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