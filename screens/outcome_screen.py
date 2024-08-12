import curses
import logging

from components.frame import Frame
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from components.right_text import RightText
from components import champions, score
from config import screens, layout, palette
from lib import local_storage


def get_quiz_outcome():
    """
    The function retrieves the quiz outcome details including score,
    tier, place, and correct answers.
    """
    # Get the quiz results from local storage
    user_name = local_storage.get_item("user")
    if user_name is None or len(user_name) == 0:
        raise Exception("User name is not set")
    logging.info(f"Username: {user_name}")

    total_miskates = local_storage.get_item("total_mistakes")
    if total_miskates is None:
        raise Exception("Total mistakes are not set")

    correct_answers = local_storage.get_item("correct_answers")
    if correct_answers is None:
        raise Exception("Correct answers are not set")

    quiz_time = local_storage.get_item("quiz_time")
    if quiz_time is None:
        raise Exception("Quiz time is not set")

    timestamp = local_storage.get_item("end_time")
    if timestamp is None:
        raise Exception("Timestamp is not set")

    # Calculate the score and tier
    the_score, tier = score.get_score_and_tier(total_miskates, quiz_time)
    place = champions.record_user_score(user_name, the_score, timestamp)
    logging.info(f"Score: {the_score}", f"Tier: {tier}")
    logging.info(f"Place: {place}")

    return {
        "score": the_score,
        "tier": tier,
        "place": place,
        "correct_answers": correct_answers
    }


def content_screen_handler(stdscr, navbar, elements, data):
    """
    The function handles the content of the outcome screen.
    """
    color = curses.color_pair(palette.MAIN_COLOR)
    color_yellow = curses.color_pair(palette.ACCENT_COLOR_INV)

    # Retrieve the user name from local storage
    user_name = local_storage.get_item("user")

    # # Define the elements to be displayed on the outcome screen
    # (the numbers are line's numbers)
    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT,
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ",
                  layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   GAME RESULTS   ", layout.FRAME_PADDING_TOP, color),
        CenteredText(f"{'* ' * data["tier"]}", 12, color),
        CenteredText(f"Your score: {data["score"]}", 16, color),
        CenteredText(f"Correct answers: {data["correct_answers"]}", 17, color),
        CenteredText("Do you want to play again? Press `g` button ", 20,
                     color_yellow),
    ]

    # Display the user's place if they made it onto the champions board
    # 14 is line by x axis
    if data["place"] != -1:
        place_text = f"YOUR PLACE: {data["place"]} on Champions's board "
        elements.append(CenteredText(place_text, 14, color))

    while True:
        # Clear screen
        stdscr.clear()

        # Draw elements
        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)

        stdscr.refresh()

        # Wait for user input
        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)

        # If navigation change is detected, clear the local storage and
        # set the user name
        if change:
            local_storage.clear()
            local_storage.set_item("user", user_name)
            return screen


def skeleton_screen_handler(stdscr, navbar, elements):
    """
    The function displays a loading screen while fetching the quiz
    outcome data.
    """
    color = curses.color_pair(palette.MAIN_COLOR)
    height, width = stdscr.getmaxyx()

    # Clear screen
    stdscr.clear()

    # Draw elements
    navbar.draw(stdscr)
    for e in elements:
        e.draw(stdscr)

    # Display a banner indicating the outcome is being fetched
    banner_text = "Your quiz outcome is on its way, please wait..."
    banner = CenteredText(banner_text, height // 2, color)
    banner.draw(stdscr)

    stdscr.refresh()

    return get_quiz_outcome()


def outcome_screen_handler(stdscr):
    """
    Main handler for the outcome screen, managing the display and
    user interactions.
    """
    color = curses.color_pair(palette.MAIN_COLOR)

    height, width = stdscr.getmaxyx()

    # Create the navbar with navigation actions
    navbar = Navbar(
        NavAction("h", screens.HOME_SCREEN, "Home  "),
        NavAction("g", screens.GAME_SCREEN, "Game  "),
        NavAction("c", screens.CHAMPIONS_SCREEN, "Champions  "),
        NavAction("q", None, "Quit  ")
    )

    # Retrieve the user name from local storage
    user_name = local_storage.get_item("user")
    if user_name is None or len(user_name) == 0:
        raise Exception("User name is not set")
    user_text = f"  USER : {user_name}  "

    # Define the elements to be displayed on the outcome screen
    # (the numbers are line's numbers)
    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT,
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        CenteredText("   GAME OUTCOME   ", layout.FRAME_PADDING_TOP, color),
        RightText(user_text, layout.FRAME_PADDING_TOP, 10, color),
    ]

    # Get the quiz outcome data
    data = skeleton_screen_handler(stdscr, navbar, elements)
    logging.info(f"Outcome data: {data}")

    # Handle the content screen display and interactions
    return content_screen_handler(stdscr, navbar, elements, data)


def on_load_outcome_screen(w):
    """
    Wrapper function for setting up the outcome screen.
    """
    return w(outcome_screen_handler)
