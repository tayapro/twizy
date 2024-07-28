import sys
import curses
import random
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
from lib import local_storage, spreadsheet_storage

def fetch_quiz_data():
    return [
        (question, correct_option, option_0,
        optiopn_1, option_2, option_3) 
        for question, correct_option, option_0,
            optiopn_1, option_2, option_3 
        in spreadsheet_storage.get_table("quiz")[1:]
    ]

def set_quiz(quiz_arr):
    random.shuffle(quiz_arr)
    return quiz_arr[:10]

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
    score = 0

    quiz_storage_data = fetch_quiz_data()
    quiz = set_quiz(quiz_storage_data)
    print(f"QUIZ: {quiz}", file=sys.stderr)
    print("----------------------------------------", file=sys.stderr)

    # Initialize answers
    i = 0
    answers_list = quiz[i][2:6]
    question = CenteredText(quiz[i][0], 10, color)
    # answers = Menu(12, 10, "", *answers_list)
    # question = AnimatedText(quiz[i][0], 10, 10, 0.1)
    # print(f"answers_list: {answers_list}", file=sys.stderr)
    # print(f"question: {quiz[0][0]}", file=sys.stderr)

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
   
        answers = Menu(12, 10, "", *answers_list)
        answers.draw(stdscr)
        question.draw(stdscr)

        stdscr.refresh()

        # if not question.is_animation_finished():
        #     continue

        code = stdscr.getch()

        answers.update(code)

        character = chr(code)
        change, screen = navbar.update(stdscr, code)
        if change:
            return screen

        if question_counter == game.TOTAL_QUESTIONS:
            local_storage.set_item("score", score)
            return consts.OUTCOME_SCREEN

        if code in [10, 13, curses.KEY_ENTER]:
            question_counter += 1
            i += 1
            answers_list = quiz[i][2:6]
            answers.set_options(answers_list)
            question.message = quiz[i][0]
            continue

def on_load_game_screen(w):
    return w(game_screen_handler)