import curses
from consts import screens
from components.greeting import Greeting
from components.navbar import Navbar, NavAction

def main_menu_screen_handler(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    BLUE_AND_CYAN = curses.color_pair(1)
    YELLOW_AND_BLACK = curses.color_pair(2)

    height, width = stdscr.getmaxyx()
    msg = f"MAIN MENU Press H to home menu"
    x = int((width // 2) - (len(msg) // 2))
    g = Greeting(msg, 4, x, BLUE_AND_CYAN | curses.A_ITALIC)  
    navbar = Navbar(
        NavAction("h", screens.HOME_SCREEN, "Home"),
        NavAction("m", screens.MAIN_MENU_SCREEN, "Menu"),
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

def on_load_main_menu_screen(w):
    return w(main_menu_screen_handler)