import sys
import curses
from config import consts, layout, palette
from components.text import Text
from components.frame import Frame
from components.right_text import RightText
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from lib import local_storage


def home_screen_handler(stdscr):
    curses.initscr()
    curses.start_color()
    color = curses.color_pair(palette.ACCENT_COLOR_INV)
    stdscr.getyx()
    stdscr.move(0, 0)

    navbar = Navbar(
        NavAction("c", consts.CHAMPIONS_SCREEN, "Champions  "),
        NavAction("g", consts.GAME_SCREEN, "Game  "),
        NavAction("q", None, "Quit  ")
    )

    height, width = stdscr.getmaxyx()

    user_name = local_storage.get_item("user")

    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT, 
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   HOME   ", layout.FRAME_PADDING_TOP, color),
        CenteredText("WELCOME to the tWIZY quiz!", 8, color),
        CenteredText("Get ready to test your knowledge and have fun.", 9, color),
        Text("RULES: ", 11, layout.MAIN_TEXT_MARGING_X, color),
        Text("1. Read Each Question Carefully.", 13, layout.MAIN_TEXT_MARGING_X, color),
        Text("2. Select Your Answer", 14, layout.MAIN_TEXT_MARGING_X, color),
        Text("3. Earn Points", 15, layout.MAIN_TEXT_MARGING_X, color),
        CenteredText("To start the game, press the `g` button.", 20, color)
    ]

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)

        for e in elements:
            e.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def on_load_home_screen(w):
    return w(home_screen_handler)