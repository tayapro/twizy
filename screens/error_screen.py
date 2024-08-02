import curses
from config import screens, layout, palette, logo
from components.navbar import Navbar, NavAction
from components.text import Text
from components.centered_text import CenteredText
from lib import local_storage
import logging

def next_screen():
    user = local_storage.get_item("user")
    logging.error(f"user: {user}")
    if user == None or len(user) == 0:
        logging.error("going login")
        return screens.LOGIN_SCREEN
    
    logging.error("going home")
    return screens.HOME_SCREEN

def error_screen_handler(stdscr):
    """
    Handles the display and functionality of the error screen.

    This function initializes the error screen, displays an error message,
    and provides navigation options. The user can navigate back to the home
    screen or quit the application.

    Args:
        stdscr: The main screen object from curses for drawing on the terminal.
    """

    user = local_storage.get_item("user")
    local_storage.clear()
    local_storage.set_item("user", user)

    # Initialize curses and set colors
    color = curses.color_pair(palette.MAIN_COLOR)
    accent_color = curses.color_pair(palette.ACCENT_COLOR_INV)

    navbar = Navbar(
        NavAction("q", None, "Quit  ")
    )

    # Create the UI elements (the numbers are line's numbers)
    elements = [
        Text("OOPS!", 10, layout.FRAME_PADDING_LEFT, accent_color),
        Text("SOMETHING WRONG...", 12, layout.FRAME_PADDING_LEFT, color),
        Text("Press any key", 13, layout.FRAME_PADDING_LEFT,
             color),
    ]

    # Add the logo lines as text elements, start from 9th line
    for i, line in enumerate(logo.LOGO.splitlines()):
        elements.append(Text(line, 9 + i, layout.MAIN_TEXT_MARGING_X + 15,
                             accent_color))

    elements.append(Text("start from home screen.", 14, layout.FRAME_PADDING_LEFT,
             color))

    # Clear screen
    stdscr.clear()

    for e in elements:
        e.draw(stdscr)

    stdscr.refresh()

    character = stdscr.getch()
    change, screen = navbar.update(stdscr, character)
    if change:
        return screen

    return next_screen()


def on_load_error_screen(w):
    """
    Wrapper function for setting up the error screen.

    Args:
        w (function): The function to be called with the error_screen_handler.
    """
    return w(error_screen_handler)
