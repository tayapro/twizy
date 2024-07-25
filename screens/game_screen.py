import sys
import curses
from curses.textpad import rectangle
from config import consts, layout, palette
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.menu import Menu
from lib import local_storage

def game_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    navbar = Navbar(
        NavAction("a", consts.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
    )

    height, width = stdscr.getmaxyx()

    title = "   tWIZY GAME   "  
    title_x = width // 2 - len(title) // 2
    title_g = Greeting(title, 5, title_x, color)

    user_name = local_storage.get_item("user")
    user = f"  USER : {user_name}  "
    user_x = width - len(user) - 10
    user_g = Greeting(user, 5, user_x, color | curses.A_ITALIC) 

    question_counter = 1
    TOTAL_QUESTIONS = 10

    # initialize answers
    answers = Menu(12, 10, "Options", "1. Alien", "2. Monster", "3. Programmer", "4. Who?")

    while True:
        # Clear screen
        stdscr.clear()

        border_padding = 5
        rectangle(stdscr, border_padding, border_padding, 
                  height - border_padding, width - border_padding)

        question_counter_text = f"  QUESTION : {question_counter} / {TOTAL_QUESTIONS} "
        stdscr.addstr(5, 10, question_counter_text)

        navbar.draw(stdscr)
        user_g.draw(stdscr)
        title_g.draw(stdscr)

        stdscr.addstr(10, 10, "Who's Mr. Bean?")
        answers.draw(stdscr)

        stdscr.refresh()

        code = stdscr.getch()

        answers.update(code)

        character = chr(code)
        change, screen = navbar.update(stdscr, code)
        if change:
            return screen

        if question_counter == TOTAL_QUESTIONS:
            return consts.OUTCOME_SCREEN

        if code in [10, 13, curses.KEY_ENTER]:
            question_counter += 1
            print(f"Answer: i={answers.cursor}, op={answers.get_selection()}", file=sys.stderr)
            answers.set_options("1. Alien", "2. Monster", "3. Programmer", f"4. Who? {question_counter}")
            print(f"QUESTION_COUNTER: --- {question_counter}", file=sys.stderr)
            continue

def on_load_game_screen(w):
    return w(game_screen_handler)