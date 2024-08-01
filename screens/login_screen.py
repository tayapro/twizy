import curses
from config import screens, layout, palette
from components.navbar import Navbar, NavAction
from components.text import Text
from components.centered_text import CenteredText
from lib import local_storage


logo = """
  ████████╗██╗    ██╗██╗███████╗██╗   ██╗
  ╚══██╔══╝██║    ██║██║╚══███╔╝╚██╗ ██╔╝
     ██║   ██║ █╗ ██║██║  ███╔╝  ╚████╔╝ 
     ██║   ██║███╗██║██║ ███╔╝    ╚██╔╝  
     ██║   ╚███╔███╔╝██║███████╗   ██║   
     ╚═╝    ╚══╝╚══╝ ╚═╝╚══════╝   ╚═╝
"""

def login_screen_handler(stdscr):
    local_storage.clear()

    curses.initscr()
    curses.start_color()
    color = curses.color_pair(palette.MAIN_COLOR)
    accent_color = curses.color_pair(palette.ACCENT_COLOR_INV)

    prompt = "Name (3-8 chars): "

    elements = [
        Text("WELCOME", 10, layout.FRAME_PADDING_LEFT, accent_color),
        Text("TO THE tWIZY QUIZ!", 11, layout.FRAME_PADDING_LEFT, color),
        Text("Enter your name to start.", 13, layout.FRAME_PADDING_LEFT, color),
        CenteredText("You can find navigation hints in the navbar on every screen.", 22, color),
    ]

    for i, line in enumerate(logo.splitlines()):
        elements.append(Text(line, 9 + i, layout.MAIN_TEXT_MARGING_X + 15, accent_color))

    error_element = Text("", 15, layout.FRAME_PADDING_LEFT, color)
    elements.append(error_element)

    # Easy way to ensure cursor position on the screen
    elements.append(Text(prompt, 14, layout.FRAME_PADDING_LEFT, color))

    user_element = Text("", 14, layout.FRAME_PADDING_LEFT + len(prompt), color)
    elements.append(user_element)

    while True:
        # Clear screen
        stdscr.clear()

        for e in elements:
            e.draw(stdscr)
        error_element.message = ""

        stdscr.refresh()

        code = stdscr.getch()

        character = chr(code)
        if character.isalpha() and character.isascii() and len(user_element.message) < 8:
            user_element.message += character

        if code in [263, curses.KEY_BACKSPACE]:
            user_element.message = user_element.message[:-1]
            continue

        if code in [10, 13, curses.KEY_ENTER]:
            if len(user_element.message) < 4:
                error_element.message = "Error: username too short"
                continue

            local_storage.set_item("user", user_element.message)
            return


def on_load_login_screen(w):
    return w(login_screen_handler)
