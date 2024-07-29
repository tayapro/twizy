import sys
import curses
import random
import time
from curses.textpad import rectangle
from config import screens, layout, palette, game
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.menu import Menu
from components.frame import Frame
from components.text import Text
from components.centered_text import CenteredText
from components.right_text import RightText
from lib import local_storage, spreadsheet_storage

def fetch_quiz_data():
    return [
        (question, correct_option, option_0,
        optiopn_1, option_2, option_3) 
        for question, correct_option, option_0,
            optiopn_1, option_2, option_3 
        in spreadsheet_storage.get_table("quiz")[1:]
    ]

def get_quiz():
    data = fetch_quiz_data()
    random.shuffle(data)
    return data[:10]

def game_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    navbar = Navbar(
        NavAction("a", screens.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
    )

    user_name = local_storage.get_item("user")

    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT, 
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   tWIZY GAME   ", layout.FRAME_PADDING_TOP, color)
    ]

    quiz = get_quiz()

    question_counter = 1
    correct_answers_counter = 0
    question, corrent_option_index, *options = quiz[0]

    options_menu = Menu(12, 10, "", True, *options)
    question_text = CenteredText(question + " ", 10, color) # Question

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
   
        options_menu.draw(stdscr)
        question_text.draw(stdscr)

        stdscr.refresh()
        
        start_time = time.time()

        code = stdscr.getch()

        options_menu.update(code)

        character = chr(code)
        change, screen = navbar.update(stdscr, code)
        if change:
            return screen

        # When answeeed all questions
        if question_counter == game.TOTAL_QUESTIONS:
            quiz_time = time.time() - start_time
            local_storage.set_item("total_mistakes", game.TOTAL_QUESTIONS - correct_answers_counter)
            local_storage.set_item("correct_answers", correct_answers_counter)
            local_storage.set_item("quiz_time", quiz_time)
            return screens.OUTCOME_SCREEN

        # When user hits enter
        if code in [10, 13, curses.KEY_ENTER]:
            user_option = options_menu.get_selection()
            if user_option == int(corrent_option_index):
                correct_answers_counter += 1

            question_counter += 1
            # question_counter -1 becaause of question starts from 1
            question, corrent_option_index, *options = quiz[question_counter - 1]

            options_menu.set_options(*options)
            question_text.message = question + " "
            continue

def on_load_game_screen(w):
    return w(game_screen_handler)