import sys
import curses
import gspread
from google.oauth2.service_account import Credentials
from config import consts, layout, palette
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from components.menu import Menu
from lib import local_storage
from lib.spreadsheet_storage import set_column, get_column, get_table, set_table

def get_champions():
    return [(n, s) for n, s in get_table("champions")[1:]]

def update_champions(new_champion):
    return

def check_score(score):
    return

def content_screen_handler(stdscr, navbar, elements, data):
    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)

        max_name_length = max(len(name) for name, _ in data)

        # Define the start position
        start_y = 4
        start_x = 5
        name_header = "Name"
        score_header = "Score"
        gap = 20
        gap_filler = " "
        stdscr.addstr(start_y, start_x, name_header.ljust(max_name_length + len(name_header) + gap) + score_header)

        # Print a separator line
        stdscr.addstr(start_y + 1, start_x, "-" * (max_name_length + len(name_header) + len(score_header) + gap))

        # Print the data rows
        for i, (name, score) in enumerate(data):
            stdscr.addstr(start_y + 2 + i, start_x, f"{name.ljust(max_name_length + gap + len(name_header), gap_filler)}{str(score).rjust(len(score_header))}")

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def skeleton_screen_handler(stdscr, navbar, elements):
    stdscr.clear()
    navbar.draw(stdscr)
    for e in elements:
        e.draw(stdscr)
    banner = "Loading please wait..."
    stdscr.addstr(15, 20, banner)
    stdscr.refresh()
    return get_champions()


def champions_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)
 
    elements = [
        CenteredText("  CHAMPIONS BOARD  ", layout.FRAME_PADDING_TOP, color)
    ]

    navbar = Navbar(
        NavAction("h", consts.HOME_SCREEN, "Home  "),
        NavAction("g", consts.GAME_SCREEN, "Game  "),
        NavAction("q", None, "Quit  ")
    )

    data = skeleton_screen_handler(stdscr, navbar, elements)
    content_screen_handler(stdscr, navbar, elements, data)
    

def on_load_champions_screen(w):
    return w(champions_screen_handler)