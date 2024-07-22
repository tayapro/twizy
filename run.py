import curses
from consts import screens
from screens.home_screen import on_load_home_screen

def main():
    screen = screens.HOME_SCREEN
    while True:
        if screen == screens.HOME_SCREEN:
            screen = on_load_home_screen(curses.wrapper)
        else:
            return

main()
