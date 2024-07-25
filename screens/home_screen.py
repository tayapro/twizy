import sys
import curses
from curses.textpad import rectangle
from config import consts, layout, palette
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from lib import local_storage
from components.centered_text import CenteredText
from components.text import Text

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
    user_text = f"  USER : {user_name}  "
    user_text_x = width - len(user_text) - 10

    texts = [
        Text(user_text, layout.FRAME_PADDING, user_text_x, color),
        CenteredText("   HOME   ", layout.FRAME_PADDING, color),
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

        rectangle(stdscr, layout.FRAME_PADDING, layout.FRAME_PADDING, 
                  height - layout.FRAME_PADDING, width - layout.FRAME_PADDING)

        navbar.draw(stdscr)

        for t in texts:
            t.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def on_load_home_screen(w):
    return w(home_screen_handler)