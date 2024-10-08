import curses
import logging

from config import screens, layout, palette, logo
from components.navbar import Navbar, NavAction
from components.text import Text
from components.centered_text import CenteredText
from lib import local_storage


def login_screen_handler(stdscr):
    """
    Main handler for the login screen, managing the display and
    user interactions.
    """
    # Clear any existing user data
    local_storage.clear()

    # Initialize curses and set colors
    color = curses.color_pair(palette.MAIN_COLOR)
    accent_color = curses.color_pair(palette.ACCENT_COLOR_INV)

    prompt = "Name (3-8 chars): "

    # Define the elements to be displayed on the login screen
    # (the numbers are line's numbers)
    elements = [
        Text("WELCOME", 10, layout.FRAME_PADDING_LEFT, accent_color),
        Text("TO THE tWIZY QUIZ!", 11, layout.FRAME_PADDING_LEFT, color),
        Text("Enter your name to start.", 13, layout.FRAME_PADDING_LEFT,
             color),
        CenteredText("Please log in first. Quit option is available "
                     "on the next screen", 21, color),
        CenteredText("You can find navigation hints in the navbar on every "
                     "screen", 22, color),
    ]

    # Add the logo lines as text elements, start from 9th line
    for i, line in enumerate(logo.LOGO.splitlines()):
        elements.append(Text(line, 9 + i, layout.MAIN_TEXT_MARGING_X + 15,
                             accent_color))

    # Error text on 15th line
    error_element = Text("", 15, layout.FRAME_PADDING_LEFT, color)
    elements.append(error_element)

    # Add the prompt and input field for the username on 14th line
    # Easy way to ensure cursor position on the screen
    elements.append(Text(prompt, 14, layout.FRAME_PADDING_LEFT, color))
    user_element = Text("", 14, layout.FRAME_PADDING_LEFT + len(prompt), color)
    elements.append(user_element)

    while True:
        # Clear screen
        stdscr.clear()

        # Draw elements
        for e in elements:
            e.draw(stdscr)
        error_element.message = ""

        stdscr.refresh()

        code = stdscr.getch()

        # Handle character input for the username
        character = chr(code)
        if (
            character.isalpha() and
            character.isascii() and
            len(user_element.message) < 8
        ):
            user_element.message += character
        else:
            error_element.message = "Hint: Only letters please"

        # Handle backspace
        if code in [263, curses.KEY_BACKSPACE]:
            user_element.message = user_element.message[:-1]
            error_element.message = ""
            continue

        # Handle Enter key
        if code in [10, 13, curses.KEY_ENTER]:
            if len(user_element.message) < 4:
                error_element.message = "Error: username too short"
                continue

            local_storage.set_item("user", user_element.message)
            logging.info(f"Username: {user_element.message}")
            return screens.HOME_SCREEN


def on_load_login_screen(w):
    """
    Wrapper function for setting up the login screen.
    """
    return w(login_screen_handler)
