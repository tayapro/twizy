import curses
import logging
from config import screens, layout, palette
from components.text import Text
from components.frame import Frame
from components.right_text import RightText
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from lib import local_storage


def home_screen_handler(stdscr):
    """
    Main handler for the home screen, managing the display and
    user interactions.
    """
    color = curses.color_pair(palette.ACCENT_COLOR_INV)

    # Create the navbar with navigation actions
    navbar = Navbar(
        NavAction("c", screens.CHAMPIONS_SCREEN, "Champions  "),
        NavAction("g", screens.GAME_SCREEN, "Game  "),
        NavAction("q", None, "Quit  ")
    )

    height, width = stdscr.getmaxyx()

    # Retrieve the user name from local storage
    user_name = local_storage.get_item("user")
    if user_name is None or len(user_name) == 0:
        raise Exception("User name is not set")
    logging.info(f"User: {user_name}")

    # Define the elements to be displayed on the home screen
    # (the numbers are line's numbers)
    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT,
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING_TOP, 10,
                  color),
        CenteredText("   HOME   ", layout.FRAME_PADDING_TOP, color),
        CenteredText("Get ready to test your knowledge and have fun?", 9,
                     color),
        Text("RULES: ", 11, layout.MAIN_TEXT_MARGING_X, color),
        Text("1. Read Each Question Carefully.", 13,
             layout.MAIN_TEXT_MARGING_X, color),
        Text("2. Select Your Answer", 14, layout.MAIN_TEXT_MARGING_X, color),
        Text("3. Earn Points", 15, layout.MAIN_TEXT_MARGING_X, color),
        CenteredText("To start the game, press the `g` button.", 20, color),
    ]

    while True:
        # Clear screen
        stdscr.clear()

        # Draw elements
        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)

        stdscr.refresh()

        # Get user input and check for navigation change
        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen


def on_load_home_screen(w):
    """
    Wrapper function for setting up the home screen.
    """
    return w(home_screen_handler)
