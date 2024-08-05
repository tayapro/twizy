import sys
import curses
import gspread
from google.oauth2.service_account import Credentials
from config import screens, layout, palette
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from components.menu import Menu
from components.frame import Frame
from components.champions import fetch_champions
from lib import local_storage


def content_screen_handler(stdscr, navbar, elements, data):
    """
    The function handles the content of the champions screen.
    """

    while True:
        height, width = stdscr.getmaxyx()

        # Clear screen
        stdscr.clear()

        # Draw elements
        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)

        max_name_length = max(len(name) for name, _, _ in data)

        # Define the start position
        name_header = "Name"
        score_header = "Score"
        gap = 20
        gap_filler = " "
        start_x = width // 2 - (max_name_length + gap + len(score_header)) // 2
        start_y = height // 2 - len(data) // 2
        stdscr.addstr(start_y, start_x,
                      name_header.ljust(max_name_length + len(name_header)
                                        + gap) + score_header)

        # Print a separator line
        stdscr.addstr(start_y + 1, start_x, "-" * (max_name_length
                      + len(name_header) + len(score_header) + gap))

        # Print the data rows
        for i, (name, score, time) in enumerate(data):
            name_str = name.ljust(max_name_length + gap + len(name_header),
                                  gap_filler)
            score_str = str(score).rjust(len(score_header))
            stdscr.addstr(start_y + 2 + i, start_x,
                          f"{name_str}{score_str}")

        stdscr.refresh()

        # Get user input and check for navigation change
        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen


def skeleton_screen_handler(stdscr, navbar, elements):
    """
    The function displays a loading screen while fetching champions
    leaderboard data.
    """

    color = curses.color_pair(palette.MAIN_COLOR)
    height, width = stdscr.getmaxyx()

    # Clear screen
    stdscr.clear()

    # Draw elements
    navbar.draw(stdscr)
    for e in elements:
        e.draw(stdscr)

    banner = CenteredText("The champions board is on its way, please wait...",
                          height // 2, color)
    banner.draw(stdscr)

    stdscr.refresh()

    return fetch_champions()


def champions_screen_handler(stdscr):
    """
    Main handler for the champions screen, managing the display and
    user interactions.
    """

    color = curses.color_pair(palette.MAIN_COLOR)

    # Define the elements to be displayed on the champions screen
    # (the numbers are line's numbers)
    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT,
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        CenteredText("  CHAMPIONS BOARD  ", layout.FRAME_PADDING_TOP, color)
    ]

    # Create the navbar with navigation actions
    navbar = Navbar(
        NavAction("h", screens.HOME_SCREEN, "Home  "),
        NavAction("g", screens.GAME_SCREEN, "Game  "),
        NavAction("q", None, "Quit  ")
    )

    data = skeleton_screen_handler(stdscr, navbar, elements)
    return content_screen_handler(stdscr, navbar, elements, data)


def on_load_champions_screen(w):
    """
    Wrapper function for setting up the champions screen.
    """

    return w(champions_screen_handler)
