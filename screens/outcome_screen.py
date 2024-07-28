import sys
import curses
from config import consts
from components.frame import Frame
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from components.right_text import RightText
from config import consts, layout, palette
from lib import local_storage

def outcome_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    height, width = stdscr.getmaxyx()

    navbar = Navbar(
        NavAction("h", consts.HOME_SCREEN, "Home  "),
        NavAction("g", consts.GAME_SCREEN, "Game  "),
        NavAction("c", consts.CHAMPIONS_SCREEN, "Champions  "),
        NavAction("q", None, "Quit  ")
    )

    user_name = local_storage.get_item("user")
    score = local_storage.get_item("score")

    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT, 
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   OUTCOME GAME   ", layout.FRAME_PADDING_TOP, color)
    ]

    score_msg = CenteredText(f"Score: {score}", height // 2, color)

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)
        score_msg.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def on_load_outcome_screen(w):
    return w(outcome_screen_handler)