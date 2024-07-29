import sys
import curses
from components.frame import Frame
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from components.right_text import RightText
from components.score import get_score_and_tier
from config import screens, layout, palette
from lib import local_storage

def outcome_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    height, width = stdscr.getmaxyx()

    navbar = Navbar(
        NavAction("h", screens.HOME_SCREEN, "Home  "),
        NavAction("g", screens.GAME_SCREEN, "Game  "),
        NavAction("c", screens.CHAMPIONS_SCREEN, "Champions  "),
        NavAction("q", None, "Quit  ")
    )

    user_name = local_storage.get_item("user")
    total_miskates = local_storage.get_item("total_mistakes")
    correct_answers = local_storage.get_item("correct_answers")
    quiz_time = local_storage.get_item("quiz_time")

    score, tier = get_score_and_tier(total_miskates, quiz_time)

    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT, 
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING_TOP, 10, color),
        CenteredText("   GAME OUTCOME   ", layout.FRAME_PADDING_TOP, color),
        CenteredText(f"CORRECT ANSWERS: {correct_answers}", 12, color),
        CenteredText(f"SCORE: {score}", 13, color),
        CenteredText(f"TIER: {'*' * tier}", 14, color)
    ]

    # score_msg = CenteredText(f"Score: {score}", height // 2, color)

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)
        # score_msg.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def on_load_outcome_screen(w):
    return w(outcome_screen_handler)