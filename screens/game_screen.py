import sys
import curses
from config import consts
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from config import palette
from lib import local_storage

def game_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    height, width = stdscr.getmaxyx()
    msg = f"GAME screen"
    x = int((width // 2) - (len(msg) // 2))
    g = Greeting(msg, 4, x, color | curses.A_ITALIC)   

    navbar = Navbar(
        NavAction("a", consts.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
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

def on_load_game_screen(w):
    return w(game_screen_handler)