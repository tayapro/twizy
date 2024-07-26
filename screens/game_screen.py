import sys
import curses
from curses.textpad import rectangle
from config import consts, layout, palette, game
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.menu import Menu
from components.frame import Frame
from components.text import Text
from components.centered_text import CenteredText
from components.right_text import RightText
from lib import local_storage

def game_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    navbar = Navbar(
        NavAction("a", consts.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
    )

    user_name = local_storage.get_item("user")

    elements = [
        Frame(layout.FRAME_PADDING, layout.FRAME_PADDING),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING, 10, color),
        CenteredText("   tWIZY GAME   ", layout.FRAME_PADDING, color)
    ]

    question_counter = 1

    # initialize answers
    answers = Menu(12, 10, "", "1. Alien", "2. Monster", "3. Programmer", "4. Who?")

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)

        for e in elements:
            e.draw(stdscr)

        # question_counter is different for every draw cycle, when we hit Enter
        Text(f"  QUESTION : {question_counter} / {game.TOTAL_QUESTIONS} ", 
            5, 10
        ).draw(stdscr)
   
        stdscr.addstr(10, 10, "Who's Mr. Bean?")
        answers.draw(stdscr)

        stdscr.refresh()

        code = stdscr.getch()

        answers.update(code)

        character = chr(code)
        change, screen = navbar.update(stdscr, code)
        if change:
            return screen

        if question_counter == game.TOTAL_QUESTIONS:
            return consts.OUTCOME_SCREEN

        if code in [10, 13, curses.KEY_ENTER]:
            question_counter += 1
            print(f"Answer: i={answers.cursor}, op={answers.get_selection()}", file=sys.stderr)
            answers.set_options("1. Alien", "2. Monster", "3. Programmer", f"4. Who? {question_counter}")
            print(f"QUESTION_COUNTER: --- {question_counter}", file=sys.stderr)
            continue

def on_load_game_screen(w):
    return w(game_screen_handler)