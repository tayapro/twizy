import sys
import curses
from config import consts
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from config import palette
from lib import local_storage

def home_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    height, width = stdscr.getmaxyx()
    msg = f"HOME Press M to main menu"
    x = int((width // 2) - (len(msg) // 2))
    g = Greeting(msg, 4, x, color | curses.A_ITALIC)   
    actions = [
        NavAction("h", consts.HOME_SCREEN, "Home"),
        NavAction("m", consts.MAIN_MENU_SCREEN, "Menu"),
        NavAction("q", None, "Quit")
    ]
    if local_storage.get_item("user") != None:
        actions.append(NavAction("g", None, "Game"))
    else:
        actions.append(NavAction("x", None, "Xxx"))

    navbar = Navbar(*actions)

    # navbar = Navbar(
    #     NavAction("h", consts.HOME_SCREEN, "Home"),
    #     NavAction("m", consts.MAIN_MENU_SCREEN, "Menu"),
    #     NavAction("q", None, "Quit")
    # )

    while True:
        # Clear screen
        stdscr.clear()
        curses.curs_set(1)
        curses.echo()  # Enable echoing of input characters

        navbar.draw(stdscr)
        g.draw(stdscr)

        instructions = "Enter your name: "
        stdscr.addstr(10, 30, instructions)
        input_window = curses.newwin(1, 12, 10, 30 + len(instructions))

        stdscr.refresh()

        user = input_window.getstr().decode('utf-8')
        local_storage.set_item("user", user)

        print(f"User: {local_storage.get_item('user')}", file=sys.stderr)

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

        if character == curses.KEY_ENTER or character in [10, 13]:
            print("OK", file=sys.stderr)
            return consts.MAIN_MENU_SCREEN
 

def on_load_home_screen(w):
    return w(home_screen_handler)