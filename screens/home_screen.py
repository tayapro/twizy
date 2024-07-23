import sys
import curses
from curses.textpad import rectangle
from config import consts
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from config import palette
from lib import local_storage

def home_screen_handler(stdscr):
    curses.initscr()
    curses.curs_set(0)
    curses.start_color()
    color = curses.color_pair(palette.ACCENT_COLOR_INV)

    navbar = Navbar(
        NavAction("c", consts.CHAMPIONS_SCREEN, "Champions  "),
        NavAction("g", consts.GAME_SCREEN, "Game  "),
        NavAction("q", None, "Quit  ")
    )

    height, width = stdscr.getmaxyx()

    user_name = local_storage.get_item("user")
    user = f"  USER : {user_name}  "
    user_x = width - len(user) - 10
    user_g = Greeting(user, 5, user_x, color | curses.A_ITALIC) 

    title = "   HOME PAGE   "  
    title_x = width // 2 - len(title) // 2
    title_g = Greeting(title, 5, title_x, color)

    welcome = "WELCOME to the tWIZY quiz!"
    welcome_x = width // 2 - len(welcome) // 2
    welcome_g = Greeting(welcome, 8, welcome_x, color)

    welcome1 =  "Get ready to test your knowledge and have fun."
    welcome1_x = width // 2 - len(welcome1) // 2
    welcome1_g = Greeting(welcome1, 9, welcome1_x, color)

    rules = "RULES: "
    rules_g = Greeting(rules, 11, 20, color)

    rule1 = "1. Read Each Question Carefully."
    rule1_g = Greeting(rule1, 13, 20, color)

    rule2 = "2. Select Your Answer"
    rule2_g = Greeting(rule2, 14, 20, color)

    rule3 = "3. Earn Points"
    rule3_g = Greeting(rule3, 15, 20, color)

    start_game = "To start the game, press the `g` button."
    start_game_g = Greeting(start_game, 20, 20, color)

    while True:
        # Clear screen
        stdscr.clear()

        rectangle(stdscr, 5, 5, height - 5, width - 5)

        navbar.draw(stdscr)
        user_g.draw(stdscr)
        title_g.draw(stdscr)
        welcome_g.draw(stdscr)
        welcome1_g.draw(stdscr)
        rules_g.draw(stdscr)
        rule1_g.draw(stdscr)
        rule2_g.draw(stdscr)
        rule3_g.draw(stdscr)
        start_game_g.draw(stdscr)

        stdscr.refresh()

        character = stdscr.getch()
        change, screen = navbar.update(stdscr, character)
        if change:
            return screen

def on_load_home_screen(w):
    return w(home_screen_handler)