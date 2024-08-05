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
    """
    The function fetches quiz data from the "quiz" spreadsheet.
    """

    return [
        (question, int(correct_option),
         option_0, optiopn_1, option_2, option_3)
        for question, correct_option, option_0, optiopn_1, option_2, option_3
        in spreadsheet_storage.get_table("quiz")[1:]
    ]


def get_quiz():
    """
    The function shuffles and returns a list of 10 quiz questions.
    """

    data = fetch_quiz_data()
    random.shuffle(data)

    return data[:10]


def content_screen_handler(stdscr, navbar, elements, data):
    """
    The function handles the content of the game screen.
    """

    color = curses.color_pair(palette.MAIN_COLOR)
    accent_color = curses.color_pair(palette.ACCENT_COLOR_INV)

    question_counter = 0
    correct_answers_counter = 0
    question, corrent_option_index, *options = data[0]

    # Initialize the menu (line 10) and question text (from line 13)
    options_menu = Menu(13, layout.MAIN_TEXT_MARGING_X, "", True, *options)
    # Draw it last to move cursor's position from options
    question_text = CenteredText(question + " ", 10, color)

    # Logging correct answer
    logging.debug(f"Hint: {corrent_option_index + 1}")

    # Hint text on lines 19-20
    elements += [
        CenteredText("Use the Up and Down arrow keys for navigate through",
                     19, accent_color),
        CenteredText("the options and Enter to confirm", 20, accent_color),
    ]

    start_time = time.time()

    while True:
        # Clear screen
        stdscr.clear()

        # Draw elements
        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)

        # Question_counter is different for every draw cycle, when we hit Enter
        Text(f"  QUESTION : {question_counter + 1} / {game.TOTAL_QUESTIONS} ",
             layout.FRAME_PADDING_TOP, 10).draw(stdscr)

        # Draw options and question
        options_menu.draw(stdscr)
        question_text.draw(stdscr)

        stdscr.refresh()

        code = stdscr.getch()

        options_menu.update(code)

        character = chr(code)
        change, screen = navbar.update(stdscr, code)
        if change:
            return screen

        # Check if user pressed Enter to select an option
        if code in [10, 13, curses.KEY_ENTER]:
            user_option = options_menu.get_selection()
            if user_option == corrent_option_index:
                # Increment correct answer count
                correct_answers_counter += 1

            question_counter += 1
            if question_counter < game.TOTAL_QUESTIONS:
                # Load next question and options
                (question, corrent_option_index,
                 *options) = data[question_counter]
                logging.debug(f"Hint: {corrent_option_index+1}")

            options_menu.set_options(*options)
            question_text.message = question + " "

        # When answered all questions
        if question_counter == game.TOTAL_QUESTIONS:
            end_time = time.time()
            quiz_time = end_time - start_time
            total_mistakes = game.TOTAL_QUESTIONS - correct_answers_counter

            # Store quiz results
            local_storage.set_item("total_mistakes", total_mistakes)
            local_storage.set_item("correct_answers", correct_answers_counter)
            local_storage.set_item("quiz_time", int(quiz_time))
            local_storage.set_item("end_time", int(end_time))

            logging.info(f"start_time: {start_time}",
                         f"end_time: {end_time}",
                         f"quiz_time: {quiz_time}")
            logging.info(f"total_mistakes: {total_mistakes}")

            return screens.OUTCOME_SCREEN


def skeleton_screen_handler(stdscr, navbar, elements):
    """
    The function displays a loading screen while fetching quiz data.
    """

    color = curses.color_pair(palette.MAIN_COLOR)
    height, width = stdscr.getmaxyx()

    # Clear screen
    stdscr.clear()

    # Draw elements
    navbar.draw(stdscr)
    for e in elements:
        e.draw(stdscr)

    banner = CenteredText("Your quiz is on its way, please wait...",
                          height // 2, color)
    banner.draw(stdscr)

    stdscr.refresh()

    return get_quiz()


def game_screen_handler(stdscr):
    """
    Main handler for the game screen, managing the display and
    user interactions.
    """

    color = curses.color_pair(palette.MAIN_COLOR)

    # Create the navbar with navigation actions
    navbar = Navbar(
        NavAction("a", screens.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
    )

    # Retrieve the user name from local storage
    user_name = local_storage.get_item("user")
    if user_name is None or len(user_name) == 0:
        raise Exception("User name is not set")
    logging.info(f"Username: {user_name}")

    # Define the elements to be displayed on the game screen
    # (the numbers are line's numbers)
    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT,
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ",
                  layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   tWIZY GAME   ", layout.FRAME_PADDING_TOP, color)
    ]

    # Fetch quiz data and handle quiz content
    data = skeleton_screen_handler(stdscr, navbar, elements)
    return content_screen_handler(stdscr, navbar, elements, data)


def on_load_game_screen(w):
    """
    Wrapper function for setting up the game screen.
    """

    return w(game_screen_handler)
