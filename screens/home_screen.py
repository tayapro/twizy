import curses
from config import consts
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from config import palette

def home_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    height, width = stdscr.getmaxyx()
    msg = f"HOME Press M to main menu"
    x = int((width // 2) - (len(msg) // 2))
    g = Greeting(msg, 4, x, color | curses.A_ITALIC)    
    navbar = Navbar(
        NavAction("h", consts.HOME_SCREEN, "Home"),
        NavAction("m", consts.MAIN_MENU_SCREEN, "Menu"),
        NavAction("q", None, "Quit")
    )

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)
        g.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen
 

def on_load_home_screen(w):
    return w(home_screen_handler)