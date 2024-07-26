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
from components.animated_text import AnimatedText
from lib import local_storage

def game_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    navbar = Navbar(
        NavAction("a", consts.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
    )

    user_name = local_storage.get_item("user")

    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT, 
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   tWIZY GAME   ", layout.FRAME_PADDING_TOP, color)
    ]

    question_counter = 1

    # initialize answers
    answers_list = ["1. Alien", "2. Monster", "3. Programmer", "4. Who?"]
    answers = Menu(12, 10, "", *answers_list)
    question = AnimatedText("Who's Mr. Bean? ", 10, 10, 0.1)

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)

        for e in elements:
            e.draw(stdscr)

        # question_counter is different for every draw cycle, when we hit Enter
        Text(f"  QUESTION : {question_counter} / {game.TOTAL_QUESTIONS} ", 
            layout.FRAME_PADDING_TOP, 10
        ).draw(stdscr)
   
        answers.draw(stdscr)
        question.draw(stdscr)

        stdscr.refresh()

        if not question.is_animation_finished():
            continue

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
            answers.set_options("1. Alien", "2. Monster", "3. Programmer", f"4. Who? {question_counter}")
            question.message = "Are you sure that you are sure? "
            continue

def on_load_game_screen(w):
    return w(game_screen_handler)