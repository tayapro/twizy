import sys
import curses
from config import consts
from components.greeting import Greeting
from components.navbar import Navbar, NavAction
from config import palette
from lib import local_storage

def login_screen_handler(stdscr):
    color = curses.color_pair(palette.MAIN_COLOR)

    height, width = stdscr.getmaxyx()
    msg = f"LOGIN screen"
    x = int((width // 2) - (len(msg) // 2))
    g = Greeting(msg, 4, x, color | curses.A_ITALIC)   

    user = ""
    error = ""
    instructions = "Enter your name: "
    height, width = stdscr.getmaxyx()

    while True:
        # Clear screen
        stdscr.clear()

        g.draw(stdscr)   
        if len(error) > 0:
            stdscr.addstr(height // 2 + 2, width // 2, error, curses.A_ITALIC)
            error = ""

        stdscr.addstr(height // 2, width // 2 - len(instructions), instructions)
        stdscr.addstr(height // 2, width // 2, user)
        stdscr.refresh()
        code = stdscr.getch()
        print(f"Code: {code}", file=sys.stderr)
        character = chr(code)
        if character.isalpha() and character.isascii():
            user += character

        if code in [curses.KEY_BACKSPACE]:
            user = user[:-1]
            continue

        if code == curses.KEY_ENTER or code in [10, 13]:
            if len(user) < 4:
                error = "too short"
                continue
            print(f"OK -- {user}", file=sys.stderr)
            local_storage.set_item("user", user)
            return

def on_load_login_screen(w):
    return w(login_screen_handler)