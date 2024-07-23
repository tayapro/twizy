import sys
import curses
from curses.textpad import rectangle
from config import consts
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from config import palette
from lib import local_storage

def game_screen_handler(stdscr):
    stdscr.getyx()
    stdscr.move(0, 0)
    color = curses.color_pair(palette.MAIN_COLOR)

    navbar = Navbar(
        NavAction("a", consts.HOME_SCREEN, "Abort  "),
        NavAction("q", None, "Quit  ")
    )

    height, width = stdscr.getmaxyx()

    title = "   tWIZY GAME PAGE   "  
    title_x = width // 2 - len(title) // 2
    title_g = Greeting(title, 5, title_x, color)

    user_name = local_storage.get_item("user")
    user = f"  USER : {user_name}  "
    user_x = width - len(user) - 10
    user_g = Greeting(user, 5, user_x, color | curses.A_ITALIC) 

    score_num = 0
    score_x = 10

    while True:
        # Clear screen
        stdscr.clear()

        if score_num == 10:
            return

        score = f"  SCORE: {score_num}  "

        rectangle(stdscr, 5, 5, height - 5, width - 5)
        navbar.draw(stdscr)
        user_g.draw(stdscr)
        title_g.draw(stdscr)
        stdscr.addstr(5, 10, score)

        stdscr.refresh()

        code = stdscr.getch()
        if code in [10, 13, curses.KEY_ENTER] and score_num < 10:
            score_num += 1
            print(f"SCORE_NUM: --- {score_num}", file=sys.stderr)
            continue

        character = chr(code)
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def on_load_game_screen(w):
    return w(game_screen_handler)