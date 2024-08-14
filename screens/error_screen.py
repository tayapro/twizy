import curses
import logging

from config import screens, layout, palette, logo
from components.navbar import Navbar, NavAction
from components.text import Text
from components.centered_text import CenteredText
from lib import local_storage


def next_screen():
    """
    The function determines the next screen to navigate to based on
    the user's login status.
    """
    user = local_storage.get_item("user")
    logging.info(f"Username: {user}")

    if user is None or len(user) == 0:
        logging.error("Going to login screen")
        return screens.LOGIN_SCREEN

    logging.info("Going home screen")

    return screens.HOME_SCREEN


def error_screen_handler(stdscr):
    """
    Main handler for the error screen, managing the display and
    user interactions.
    """
    user = local_storage.get_item("user")
    local_storage.clear()
    local_storage.set_item("user", user)

    # Initialize curses and set colors
    color = curses.color_pair(palette.MAIN_COLOR)
    accent_color = curses.color_pair(palette.ACCENT_COLOR_INV)

    # Create the navbar with navigation actions
    navbar = Navbar(
        NavAction("q", None, "Quit  ")
    )

    # Define the elements to be displayed on the error screen
    # (the numbers are line's numbers)
    elements = [
        Text("OOPS!", 10, layout.FRAME_PADDING_LEFT, accent_color),
        Text("SOMETHING WRONG...", 12, layout.FRAME_PADDING_LEFT, color),
        Text("Press any key", 13, layout.FRAME_PADDING_LEFT,
             color),
        CenteredText("To exit the tWIZY app, press `q` ", 21, color)
    ]

    # Add the logo lines as text elements,
    # start from 9th line with left padding = layout.MAIN_TEXT_MARGING_X + 15
    for i, line in enumerate(logo.LOGO.splitlines()):
        elements.append(Text(line, 9 + i, layout.MAIN_TEXT_MARGING_X + 15,
                             accent_color))

    # Add hint text on 14th line
    elements.append(Text("start from home screen ", 14,
                    layout.FRAME_PADDING_LEFT, color))

    # Clear screen
    stdscr.clear()

    # Draw elements
    for e in elements:
        e.draw(stdscr)

    stdscr.refresh()

    # Get user input and check for navigation change
    character = stdscr.getch()
    change, screen = navbar.update(stdscr, character)
    if change:
        return screen

    return next_screen()


def on_load_error_screen(w):
    """
    Wrapper function for setting up the error screen.
    """
    return w(error_screen_handler)
