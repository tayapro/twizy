import sys
import curses
from components.frame import Frame
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from components.centered_text import CenteredText
from components.right_text import RightText
from components.score import get_score_and_tier
from components.champions import record_user_score
from config import screens, layout, palette
from lib import local_storage

def get_quiz_outcome():
    user_name = local_storage.get_item("user")
    total_miskates = local_storage.get_item("total_mistakes")
    correct_answers = local_storage.get_item("correct_answers")
    quiz_time = local_storage.get_item("quiz_time")
    timestamp = local_storage.get_item("end_time")

    score, tier = get_score_and_tier(total_miskates, quiz_time)
    place = record_user_score(user_name, score, timestamp)

    return {
        "score": score, 
        "tier": tier, 
        "place": place, 
        "correct_answers": correct_answers
    }

def content_screen_handler(stdscr, navbar, elements, data):
    color = curses.color_pair(palette.MAIN_COLOR)

    elements = [
        CenteredText(f"CORRECT ANSWERS: {data["correct_answers"]}", 12, color),
        CenteredText(f"SCORE: {data["score"]}", 13, color),
        CenteredText(f"TIER: {'*' * data["tier"]}", 14, color)
    ]

    if data["place"] != -1:
        elements.append(CenteredText(f"YOUR PLACE: {data["place"]}  ", 15, color))

    while True:
        # Clear screen
        stdscr.clear()

        navbar.draw(stdscr)
        for e in elements:
            e.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def skeleton_screen_handler(stdscr, navbar, elements):
    color = curses.color_pair(palette.MAIN_COLOR)
    height, width = stdscr.getmaxyx()

    stdscr.clear()

    navbar.draw(stdscr)

    for e in elements:
        e.draw(stdscr)

    banner = CenteredText("Your quiz outcome is on its way, please wait...", height // 2, color)
    banner.draw(stdscr)
    
    stdscr.refresh()
    
    return get_quiz_outcome()

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

    elements = [
        Frame(layout.FRAME_PADDING_TOP, layout.FRAME_PADDING_LEFT, 
              layout.FRAME_PADDING_BOTTOM, layout.FRAME_PADDING_RIGHT),
        CenteredText("   GAME OUTCOME   ", layout.FRAME_PADDING_TOP, color),
        RightText(f"  USER : {user_name}  ", layout.FRAME_PADDING_TOP, 10, color),
    ]

    data = skeleton_screen_handler(stdscr, navbar, elements)
    print(f"DATA: {data}", file=sys.stderr)
    return content_screen_handler(stdscr, navbar, elements, data)

def on_load_outcome_screen(w):
    return w(outcome_screen_handler)