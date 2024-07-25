import sys
import curses
from config import consts, layout, palette
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from lib import local_storage

def champions_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)
 
    title = CenteredText("  CHAMPIONS BOARD  ", layout.FRAME_PADDING, color)

    navbar = Navbar(
        NavAction("h", consts.HOME_SCREEN, "Home  "),
        NavAction("g", consts.GAME_SCREEN, "Game  "),
        NavAction("q", None, "Quit  ")
    )

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)
        title.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def on_load_champions_screen(w):
    return w(champions_screen_handler)