import sys
import curses
import random
import time
import logging
from curses.textpad import rectangle
from config import screens, layout, palette, game
from components.navbar import Navbar, NavAction
from components.menu import Menu
from components.frame import Frame
from components.text import Text
from components.centered_text import CenteredText
from components.right_text import RightText
from lib import local_storage, spreadsheet_storage


def fetch_quiz_data():
    return [
        (question, correct_option, option_0, optiopn_1, option_2, option_3)
        for question, correct_option, option_0, optiopn_1, option_2, option_3
        in spreadsheet_storage.get_table("quiz")[1:]
    ]


def get_quiz():
    data = fetch_quiz_data()
    random.shuffle(data)
    return data[:10]


def content_screen_handler(stdscr, navbar, elements, data):
    curses.initscr()
    curses.start_color()
    color = curses.color_pair(palette.MAIN_COLOR)
    question_counter = 0
    correct_answers_counter = 0
    question, corrent_option_index, *options = data[0]

    options_menu = Menu(13, layout.MAIN_TEXT_MARGING_X, "", True, *options)
    question_text = CenteredText(question + " ", 10, color)  
    logging.debug(f"Hint: {int(corrent_option_index) + 1}") # Logging correct answer

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)

        # Question_counter is different for every draw cycle, when we hit Enter
        Text(f"  QUESTION : {question_counter + 1} / {game.TOTAL_QUESTIONS} ",
             layout.FRAME_PADDING_TOP, 10).draw(stdscr)

        options_menu.draw(stdscr)
        question_text.draw(stdscr)

        # stdscr.addstr(1,1, f"Hint: {int(corrent_option_index)+1}")

        stdscr.refresh()

        start_time = time.time()

        code = stdscr.getch()

        options_menu.update(code)

        character = chr(code)
        change, screen = navbar.update(stdscr, code)
        if change:
            return screen

        # When user hits enter
        if code in [10, 13, curses.KEY_ENTER]:
            user_option = options_menu.get_selection()
            if user_option == int(corrent_option_index):
                correct_answers_counter += 1

            question_counter += 1
            if question_counter < game.TOTAL_QUESTIONS:
                (question, corrent_option_index,
                *options) = data[question_counter]
                logging.debug(f"Hint: {int(corrent_option_index)+1}")

            options_menu.set_options(*options)
            question_text.message = question + " "

        # When answeeed all questions
        if question_counter == game.TOTAL_QUESTIONS:
            end_time = time.time()
            quiz_time = end_time - start_time
            total_mistakes = game.TOTAL_QUESTIONS - correct_answers_counter
            local_storage.set_item("total_mistakes", total_mistakes)
            local_storage.set_item("correct_answers", correct_answers_counter)
            local_storage.set_item("quiz_time", quiz_time)
            local_storage.set_item("end_time", int(end_time))
            return screens.OUTCOME_SCREEN


def skeleton_screen_handler(stdscr, navbar, elements):
    curses.initscr()
    curses.start_color()
    color = curses.color_pair(palette.MAIN_COLOR)
    height, width = stdscr.getmaxyx()

    stdscr.clear()

    navbar.draw(stdscr)

    for e in elements:
        e.draw(stdscr)

    banner = CenteredText("Your quiz is on its way, please wait...",
                          height // 2, color)
    banner.draw(stdscr)

    stdscr.refresh()

    return get_quiz()


def game_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)
    color_yellow = curses.color_pair(palette.ACCENT_COLOR_INV)

    navbar = Navbar(
        NavAction("a", screens.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
    )

    user_name = local_storage.get_item("user")

    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT,
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ",
                  layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   tWIZY GAME   ", layout.FRAME_PADDING_TOP, color),
        CenteredText("Use the Up and Down arrow keys for navigate through", 19, color_yellow),
        CenteredText("the options and Enter to confirm", 20, color_yellow),
    ]
 
    data = skeleton_screen_handler(stdscr, navbar, elements)
    return content_screen_handler(stdscr, navbar, elements, data)


def on_load_game_screen(w):
    return w(game_screen_handler)
